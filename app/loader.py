import pymupdf


def load_pdf(file_path: str):
    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        pages.append({
            "text": text,
            "metadata": {
                "source": file_path,
                "page": page_number + 1
            }
        })

    document.close()

    return pages
