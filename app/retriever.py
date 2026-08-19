import re

from embedding import generate_embeddings
from vector_store import collection
from query_analyzer import analyze_query


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RELEVANCE_THRESHOLD = 1.40


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
    n_results=20
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

    return results


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
                n_results=20
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

def format_context(results):
    """
    Convert retrieval results into clean textual
    context for the LLM.
    """

    context_parts = []

    for result_group in results:

        if not isinstance(result_group, dict):
            continue

        # ------------------------------------------
        # CATEGORY RESULT
        #
        # {
        #     "document": "...",
        #     "metadata": {...}
        # }
        # ------------------------------------------

        if "document" in result_group:

            document = result_group.get(
                "document",
                ""
            )

            metadata = result_group.get(
                "metadata",
                {}
            )

            bike = metadata.get(
                "bike",
                "Unknown"
            )

            page = metadata.get(
                "page",
                "Unknown"
            )

            context_parts.append(
                f"""
--- SOURCE ---
Bike: {bike}
Page: {page}

{document}
"""
            )

            continue

        # ------------------------------------------
        # NORMAL CHROMADB RESULT
        #
        # {
        #     "documents": [...],
        #     "metadatas": [...]
        # }
        # ------------------------------------------

        if "documents" in result_group:

            documents = result_group.get(
                "documents"
            ) or [[]]

            metadatas = result_group.get(
                "metadatas"
            ) or [[]]

            documents = documents[0] if documents else []
            metadatas = metadatas[0] if metadatas else []

            # --------------------------------------
            # IMPORTANT:
            # ChromaDB metadata can sometimes
            # behave like a dictionary rather than
            # a list depending on the returned
            # structure.
            # --------------------------------------

            if isinstance(metadatas, dict):
                metadata_list = [
                    metadatas
                ] * len(documents)
            else:
                metadata_list = metadatas

            for i, document in enumerate(documents):

                metadata = (
                    metadata_list[i]
                    if i < len(metadata_list)
                    and isinstance(metadata_list[i], dict)
                    else {}
                )

                bike = metadata.get(
                    "bike",
                    "Unknown"
                )

                page = metadata.get(
                    "page",
                    "Unknown"
                )

                context_parts.append(
                    f"""
--- SOURCE ---
Bike: {bike}
Page: {page}

{document}
"""
                )

            continue

        # ------------------------------------------
        # COMPARISON RESULT
        #
        # {
        #     "bike": "Himalayan 450",
        #     "results": {...}
        # }
        # ------------------------------------------

        if "results" in result_group:

            bike = result_group.get(
                "bike",
                "Unknown"
            )

            nested_results = result_group.get(
                "results",
                {}
            )

            documents = nested_results.get(
                "documents"
            ) or [[]]

            metadatas = nested_results.get(
                "metadatas"
            ) or [[]]

            documents = documents[0] if documents else []
            metadatas = metadatas[0] if metadatas else []

            if isinstance(metadatas, dict):
                metadata_list = [
                    metadatas
                ] * len(documents)
            else:
                metadata_list = metadatas

            for i, document in enumerate(documents):

                metadata = (
                    metadata_list[i]
                    if i < len(metadata_list)
                    and isinstance(metadata_list[i], dict)
                    else {}
                )

                page = metadata.get(
                    "page",
                    "Unknown"
                )

                context_parts.append(
                    f"""
--- SOURCE ---
Bike: {bike}
Page: {page}

{document}
"""
                )

    return "\n".join(context_parts)