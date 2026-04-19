import re
from typing import List

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    characterTextSplitter
)
from langchain.docstore.document import Document

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Chunks the input text into smaller pieces using a recursive character text splitter.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk. Default is 1000 characters.
        chunk_overlap (int): The number of characters to overlap between chunks. Default is 200 characters.

    Returns:
        List[Document]: A list of Document objects containing the chunked text.
    """
    # Create a RecursiveCharacterTextSplitter instance
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    # Create Document objects for each chunk
    documents = [Document(page_content=chunk) for chunk in chunks]

    return documents

def chunk_by_regrex(text: str, pattern: str) -> List[Document]:
    """
    Chunks the input text based on a regular expression pattern.

    Args:
        text (str): The input text to be chunked.
        pattern (str): The regular expression pattern to split the text.

    Returns:
        List[Document]: A list of Document objects containing the chunked text.
    """
    # Split the text using the provided regular expression pattern
    chunks = re.split(pattern, text)

    # Create Document objects for each chunk
    documents = [Document(page_content=chunk) for chunk in chunks if chunk.strip()]

    return documents


