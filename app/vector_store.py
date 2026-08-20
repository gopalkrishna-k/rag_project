import chromadb


DB_PATH = "../vector_db"


client = chromadb.PersistentClient(
    path=DB_PATH
)


COLLECTION_NAME = "royal_enfield"
COLLECTION_METADATA = {"hnsw:space": "cosine"}


def _create_or_migrate_collection():
    """
    Return the Royal Enfield collection configured for cosine distance.

    ChromaDB fixes the HNSW distance space when a collection is created, so
    ``get_or_create_collection`` alone cannot update an existing L2 collection.
    When a legacy collection is found, preserve its stored records while
    recreating that collection with the required metric.
    """

    try:
        existing_collection = client.get_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        return client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata=COLLECTION_METADATA
        )

    if (
        existing_collection.metadata or {}
    ).get("hnsw:space") == "cosine":
        return existing_collection

    records = existing_collection.get(
        include=["documents", "metadatas", "embeddings"]
    )

    client.delete_collection(name=COLLECTION_NAME)

    cosine_collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata=COLLECTION_METADATA
    )

    if records["ids"]:
        cosine_collection.add(
            ids=records["ids"],
            documents=records["documents"],
            metadatas=records["metadatas"],
            embeddings=records["embeddings"]
        )

    return cosine_collection


collection = _create_or_migrate_collection()

def add_chunks(chunks, embeddings):

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(f"chunk_{index}")

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            chunk["metadata"]
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )
