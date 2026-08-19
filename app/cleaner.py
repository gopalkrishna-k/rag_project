import re


def clean_text(text: str) -> str:
    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove trailing spaces from each line
    lines = [line.strip() for line in text.split("\n")]

    # Remove excessive blank lines
    cleaned_lines = []

    previous_blank = False

    for line in lines:
        if line == "":
            if not previous_blank:
                cleaned_lines.append(line)

            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    text = "\n".join(cleaned_lines)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text
