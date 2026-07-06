from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text, chunk_size=800, chunk_overlap=150):
    """
    Splits a document into overlapping chunks for semantic search.

    Args:
        text (str): Complete document text.
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Number of overlapping characters.

    Returns:
        list[str]: List of text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",   # Paragraphs
            "\n",     # New lines
            ". ",     # Sentences
            " ",      # Words
            ""        # Characters (fallback)
        ]
    )

    return splitter.split_text(text)