from loader import load_pdf
from cleaner import clean_text


pdf_path = "../data/documents/royal_enfield_bikes_detailed_reference_2026.pdf"
pages = load_pdf(pdf_path)

for page in pages:
    original_text = page["text"]
    cleaned_text = clean_text(original_text)

    print("=" * 100)
    print(f"PAGE: {page['metadata']['page']}")
    print("=" * 100)
    print("ORIGINAL:")
    print(original_text)
    print("\nCLEANED:")
    print(cleaned_text)
