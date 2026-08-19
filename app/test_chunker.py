from loader import load_pdf
from cleaner import clean_text
from chunker import chunk_pages


pdf_path = "../data/documents/royal_enfield_bikes_detailed_reference_2026.pdf"
pages = load_pdf(pdf_path)

for page in pages:
    page["text"] = clean_text(page["text"])

chunks = chunk_pages(pages)

print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print("=" * 100)
    print(f"CHUNK {index}")
    print(f"BIKE: {chunk['metadata']['bike']}")
    print(f"PAGE: {chunk['metadata']['page']}")
    print("=" * 100)
    print(chunk["text"])
