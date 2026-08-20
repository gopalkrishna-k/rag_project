import re

from embedding import generate_embeddings
from vector_store import collection
from query_analyzer import analyze_query


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

# Embeddings are L2-normalized.  The previous ChromaDB squared-L2 threshold
# of 1.40 is equivalent to a cosine distance threshold of 0.70.
RELEVANCE_THRESHOLD = 0.70


# --------------------------------------------------
# ATTRIBUTE QUERIES
# --------------------------------------------------

ATTRIBUTE_QUERIES = {
    "engine": "Engine",
    "power": "Maximum power",
    "torque": "Maximum torque",
    "mileage": "Mileage fuel consumption",
    "top_speed": "Top speed",
    "fuel_tank": "Fuel tank",
    "weight": "Kerb weight",
    "seat_height": "Seat height",
    "ground_clearance": "Ground clearance",
    "wheelbase": "Wheelbase",
    "suspension": "Suspension",
    "brakes": "Brakes ABS",
    "tyres": "Tyres",
    "wheels": "Wheels",
    "colours": "Colours",
    "gearbox": "Gearbox",
    "clutch": "Clutch",
}


# --------------------------------------------------
# CATEGORY MAPPING
# --------------------------------------------------

CATEGORY_MAPPING = {
    "adventure_tourer": "Adventure Tourer",
    "adventure_crossover": "Adventure Crossover",
    "cruiser": "Cruiser",
    "roadster": "Roadster",
    "scrambler": "Scrambler",
    "heritage": "Heritage",
    "heritage_bobber": "Heritage / Bobber",
    "roadster_twin": "Roadster / Twin",
    "pure_sport_cafe_racer": "Pure Sport / Café Racer",
    "supermoto_custom": "Supermoto / Custom",
}


# --------------------------------------------------
# BASIC CHROMADB SEARCH
# --------------------------------------------------

def search_with_filter(
    query: str,
    bike: str | None = None,
    top_k: int = 3
):
    """
    Perform semantic search in ChromaDB.

    If a bike is provided, only chunks belonging
    to that bike are searched.
    """

    query_embedding = generate_embeddings([query])[0]

    where = None

    if bike:
        where = {
            "bike": bike
        }

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        where=where
    )

    return results


# --------------------------------------------------
# ENTITY RETRIEVAL
# --------------------------------------------------

def retrieve_by_entity(
    question: str,
    bike_name: str,
    top_k: int = 3
):
    """
    Retrieve chunks belonging to one specific bike.
    """

    results = search_with_filter(
        query=question,
        bike=bike_name,
        top_k=top_k
    )

    return results


# --------------------------------------------------
# COMPARISON RETRIEVAL
# --------------------------------------------------

def retrieve_comparison(
    question: str,
    entities: list[str],
    top_k: int = 3
):
    """
    Retrieve information separately for every bike
    involved in a comparison question.
    """

    all_results = []

    for bike in entities:

        results = retrieve_by_entity(
            question=question,
            bike_name=bike,
            top_k=top_k
        )

        # ------------------------------------------
        # Check whether anything was retrieved
        # ------------------------------------------

        documents = results.get("documents") or [[]]

        if not documents or not documents[0]:
            continue

        # ------------------------------------------
        # Check relevance
        # ------------------------------------------

        distances = results.get(
            "distances",
            [[]]
        )[0]

        if distances:

            best_distance = min(distances)

            if best_distance > RELEVANCE_THRESHOLD:
                continue

        all_results.append({
            "bike": bike,
            "results": results
        })

    return all_results


# --------------------------------------------------
# GLOBAL / ATTRIBUTE RETRIEVAL
# --------------------------------------------------

def retrieve_global(
    collection,
    question,
    n_results=20,
    attribute=None
):
    """
    Retrieve all bike records for global/aggregate
    questions.

    Global questions require information across
    multiple bikes.
    """

    results = collection.get(
        include=["documents", "metadatas"]
    )

    if not attribute:
        return results

    attribute_terms = re.findall(
        r"[a-z0-9]+",
        ATTRIBUTE_QUERIES.get(attribute, "").lower()
    )

    if not attribute_terms:
        return results

    label_pattern = re.compile(
        r"^\s*"
        + r"\s*[\W_]*\s*".join(
            re.escape(term) for term in attribute_terms
        )
        + r"\b(?P<remainder>.*)$",
        re.IGNORECASE
    )

    compact_documents = []
    compact_metadatas = []
    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    for index, document in enumerate(documents):
        if not isinstance(document, str):
            continue

        lines = document.splitlines()

        for line_index, line in enumerate(lines):
            label_match = label_pattern.match(line)

            if not label_match:
                continue

            value = label_match.group("remainder").strip(" :–—-")

            if value.startswith("(") and ")" in value:
                value = value.partition(")")[2].strip(" :–—-")

            # Most records place values on the following line.  Some place
            # them after the label, e.g. "Seat height: 825 mm".
            if not value:
                value = next(
                    (
                        candidate.strip()
                        for candidate in lines[line_index + 1:]
                        if candidate.strip()
                    ),
                    None
                )

            if value:
                compact_documents.append(
                    f"{line.strip()}\n{value}"
                )
                compact_metadatas.append(
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )

            break

    # Never perform a global comparison on a partial attribute set.  If a
    # document uses an unsupported label format, retain the existing complete
    # GLOBAL context instead of silently excluding that bike.
    if len(compact_documents) != len(documents):
        return results

    return {
        "documents": compact_documents,
        "metadatas": compact_metadatas,
    }



# --------------------------------------------------
# CATEGORY RETRIEVAL
# --------------------------------------------------

def retrieve_by_category(
    category: str,
    collection
):
    """
    Retrieve bikes belonging to a specific category.

    Example:

        category = "adventure_tourer"

    This is different from semantic search.

    For category questions, we inspect the stored
    documents and find the bike whose Category field
    matches the requested category.
    """

    target_category = CATEGORY_MAPPING.get(category)

    if not target_category:
        return []

    # ----------------------------------------------
    # Get all stored documents
    # ----------------------------------------------

    results = collection.get(
        include=["documents", "metadatas"]
    )

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    matched_results = []

    # ----------------------------------------------
    # Examine every bike document
    # ----------------------------------------------

    for i, document in enumerate(documents):

        if not document:
            continue

        metadata = (
            metadatas[i]
            if i < len(metadatas)
            else {}
        )

        # ------------------------------------------
        # Extract Category from document
        #
        # Example:
        #
        # Category
        # Adventure Tourer
        # ------------------------------------------

        category_match = re.search(
            r"Category\s*\n([^\n]+)",
            document,
            re.IGNORECASE
        )

        if not category_match:
            continue

        document_category = (
            category_match.group(1)
            .strip()
        )

        # ------------------------------------------
        # Compare category
        # ------------------------------------------

        if document_category.lower() == target_category.lower():

            matched_results.append({
                "document": document,
                "metadata": metadata
            })

    return matched_results


# --------------------------------------------------
# MAIN RETRIEVAL FUNCTION
# --------------------------------------------------

def retrieve(
    query: str,
    top_k: int = 3
):
    """
    Main query-aware retrieval function.

    ENTITY
        -> retrieve specific bike

    COMPARISON
        -> retrieve every mentioned bike

    CATEGORY
        -> retrieve bikes belonging to category

    GLOBAL
        -> retrieve information across all bikes

    GENERAL
        -> normal semantic retrieval
    """

    # ----------------------------------------------
    # STEP 1: Analyze question
    # ----------------------------------------------

    analysis = analyze_query(query)

    query_type = analysis["query_type"]
    entities = analysis["entities"]
    attribute = analysis.get("attribute")

    operation = analysis.get(
        "operation",
        "GET"
    )

    category = analysis.get(
        "category"
    )

    # ----------------------------------------------
    # CASE 1: ENTITY QUESTION
    # ----------------------------------------------

    if query_type == "ENTITY":

        if len(entities) == 1:

            bike = entities[0]

            results = retrieve_by_entity(
                question=query,
                bike_name=bike,
                top_k=top_k
            )

            documents = results.get(
                "documents"
            ) or [[]]

            if not documents or not documents[0]:
                return []

            distances = results.get(
                "distances",
                [[]]
            )[0]

            if distances:

                best_distance = min(distances)

                if best_distance > RELEVANCE_THRESHOLD:
                    return []

            return [results]

    # ----------------------------------------------
    # CASE 2: COMPARISON QUESTION
    # ----------------------------------------------

    if query_type == "COMPARISON":

        return retrieve_comparison(
            question=query,
            entities=entities,
            top_k=top_k
        )

    # ----------------------------------------------
    # CASE 3: CATEGORY QUESTION
    # ----------------------------------------------

    if (
        query_type == "GLOBAL"
        and operation == "CATEGORY"
    ):

        return retrieve_by_category(
            category=category,
            collection=collection
        )

    # ----------------------------------------------
    # CASE 4: GLOBAL QUESTION
    # ----------------------------------------------

    if query_type == "GLOBAL":

        return [
            retrieve_global(
                collection=collection,
                question=query,
                n_results=20,
                attribute=attribute
            )
        ]

    # ----------------------------------------------
    # CASE 5: GENERAL QUESTION
    # ----------------------------------------------

    results = search_with_filter(
        query=query,
        bike=None,
        top_k=top_k
    )

    documents = results.get(
        "documents"
    ) or [[]]

    if not documents or not documents[0]:
        return []

    distances = results.get(
        "distances",
        [[]]
    )[0]

    if distances:

        best_distance = min(distances)

        if best_distance > RELEVANCE_THRESHOLD:
            return []

    return [results]


# --------------------------------------------------
# FORMAT RETRIEVED CONTEXT
# --------------------------------------------------

def _normalize_chroma_records(documents, metadatas):
    """Normalize ChromaDB query and get result shapes into parallel lists."""

    # query() returns list[list[str]], whereas get() returns list[str].
    if isinstance(documents, str):
        document_list = [documents]
    elif isinstance(documents, list):
        document_list = (
            documents[0]
            if documents and isinstance(documents[0], list)
            else documents
        )
    else:
        document_list = []

    if isinstance(metadatas, dict):
        metadata_list = [metadatas] * len(document_list)
    elif isinstance(metadatas, list):
        metadata_list = (
            metadatas[0]
            if metadatas and isinstance(metadatas[0], list)
            else metadatas
        )
    else:
        metadata_list = []

    return document_list, metadata_list


def format_context(results):
    """Convert retrieval results into clean textual context for the LLM."""

    context_parts = []

    def add_source(document, metadata, bike_override=None):
        if not isinstance(document, str):
            return

        metadata = metadata if isinstance(metadata, dict) else {}
        bike = bike_override or metadata.get("bike", "Unknown")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"""
--- SOURCE ---
Bike: {bike}
Page: {page}

{document}
"""
        )

    for result_group in results:

        if not isinstance(result_group, dict):
            continue

        # CATEGORY retrieval returns one document/metadata pair per match.
        if "document" in result_group:
            add_source(
                result_group.get("document", ""),
                result_group.get("metadata", {})
            )
            continue

        # COMPARISON retrieval wraps one normal ChromaDB query result per bike.
        if "results" in result_group:
            nested_results = result_group.get("results", {})
            documents, metadatas = _normalize_chroma_records(
                nested_results.get("documents"),
                nested_results.get("metadatas")
            )

            for index, document in enumerate(documents):
                metadata = (
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )
                add_source(document, metadata, result_group.get("bike"))

            continue

        # ENTITY and GENERAL retrieval use query() (nested lists); GLOBAL
        # retrieval uses get() (flat lists). Both are normalized above.
        if "documents" in result_group:
            documents, metadatas = _normalize_chroma_records(
                result_group.get("documents"),
                result_group.get("metadatas")
            )

            for index, document in enumerate(documents):
                metadata = (
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )
                add_source(document, metadata)

    return "\n".join(context_parts)
