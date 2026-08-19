from loader import load_pdf
from cleaner import clean_text
from chunker import chunk_pages
from embedding import generate_embeddings
from vector_store import add_chunks


pdf_path = "../data/documents/royal_enfield_bikes_detailed_reference_2026.pdf"
pages = load_pdf(pdf_path)

for page in pages:
    page["text"] = clean_text(page["text"])

chunks = chunk_pages(pages)
texts = [chunk["text"] for chunk in chunks]
embeddings = generate_embeddings(texts)
add_chunks(chunks, embeddings)

print("Successfully stored chunks in ChromaDB.")
print("Number of chunks:", len(chunks))
