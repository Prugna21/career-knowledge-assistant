def split_text(text, chunk_size=800):
    chunks = []
    current_chunk = ""

    for line in text.split("\n"):
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks