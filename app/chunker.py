import re


def chunk_pages(pages):
    chunks = []

    for page in pages:
        text = page["text"]
        metadata = page["metadata"]

        # Find the bike heading.
        match = re.search(r"^\d+\.\s+(.+)$", text, re.MULTILINE)

        if match:
            bike_name = match.group(1).strip()

            chunks.append({
                "text": text,
                "metadata": {
                    **metadata,
                    "bike": bike_name
                }
            })

    return chunks
