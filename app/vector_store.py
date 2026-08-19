import chromadb


DB_PATH = "../vector_db"


client = chromadb.PersistentClient(
    path=DB_PATH
)


collection = client.get_or_create_collection(
    name="royal_enfield"
)

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
