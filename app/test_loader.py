from loader import load_pdf


pdf_path = "../data/documents/royal_enfield_bikes_detailed_reference_2026.pdf"

pages = load_pdf(pdf_path)

print("Number of pages:", len(pages))

for page in pages:
    print("=" * 100)
    print(f"PAGE: {page['metadata']['page']}")
    print("=" * 100)
    print(page["text"])
