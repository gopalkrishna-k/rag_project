from loader import load_pdf
from cleaner import clean_text
from chunker import chunk_pages
from embedding import generate_embeddings


pdf_path = "../data/documents/royal_enfield_bikes_detailed_reference_2026.pdf"
pages = load_pdf(pdf_path)

for page in pages:
    page["text"] = clean_text(page["text"])

chunks = chunk_pages(pages)
texts = [chunk["text"] for chunk in chunks]
embeddings = generate_embeddings(texts)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding shape:", embeddings.shape)

for index, chunk in enumerate(chunks):
    print("=" * 80)
    print("Chunk:", index + 1)
    print("Bike:", chunk["metadata"]["bike"])
    print("Page:", chunk["metadata"]["page"])
    print("Embedding dimensions:", len(embeddings[index]))
    print("First 10 values:", embeddings[index][:10])
