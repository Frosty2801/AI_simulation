"""
Document loading utilities using LangChain.

This module provides functions to load business documents and convert them
into LangChain Document objects for use with RAG pipelines.
"""

from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    PyPDFLoader,
    UnstructuredFileLoader,
)


def load_document(file_path: str, encoding: str = "utf-8") -> Document:
    """
    Load a single document using the appropriate LangChain loader based on file type.

    Args:
        file_path (str): Path to the document file.
        encoding (str): Encoding for text files. Default is "utf-8".

    Returns:
        Document: A LangChain Document object with page_content and metadata.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    suffix = path.suffix.lower()
    metadata = {
        "source": str(path.absolute()),
        "file_name": path.name,
        "file_type": suffix,
    }

    # Select appropriate loader based on file extension
    if suffix == ".md":
        loader = UnstructuredMarkdownLoader(file_path, encoding=encoding)
    elif suffix == ".txt":
        loader = TextLoader(file_path, encoding=encoding)
    elif suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        # Fallback to UnstructuredFileLoader for other file types
        loader = UnstructuredFileLoader(file_path, encoding=encoding)

    # Load and add metadata
    docs = loader.load()
    if docs:
        docs[0].metadata.update(metadata)
        return docs[0]

    raise ValueError(f"Failed to load document: {file_path}")


def load_documents(file_paths: List[str], encoding: str = "utf-8") -> List[Document]:
    """
    Load multiple documents from a list of file paths.

    Args:
        file_paths (List[str]): List of file paths to load.
        encoding (str): Encoding for text files. Default is "utf-8".

    Returns:
        List[Document]: A list of LangChain Document objects.
    """
    documents = []

    for file_path in file_paths:
        try:
            doc = load_document(file_path, encoding)
            documents.append(doc)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    return documents


def load_business_documents(docs: List[str], encoding: str = "utf-8") -> List[Document]:
    """
    Load business documents from a list of file paths.

    Args:
        docs (List[str]): A list of file paths for business documents.
        encoding (str): Encoding for text files. Default is "utf-8".

    Returns:
        List[Document]: A list of loaded LangChain Document objects.
    """
    return load_documents(docs, encoding)


def load_petcare_documents(docs_dir: Optional[str] = None) -> List[Document]:
    """
    Load pet care documents from a predefined directory.

    Args:
        docs_dir (Optional[str]): Path to the documents directory. 
                                  Defaults to "docs" in the project root.

    Returns:
        List[Document]: A list of loaded pet care documents.
    """
    if docs_dir is None:
        docs_dir = "docs"

    docs_path = Path(docs_dir)

    if not docs_path.exists() or not docs_path.is_dir():
        print(f"Directory {docs_dir} does not exist or is not a directory.")
        return []

    # Find all supported files (md, txt, pdf)
    supported_extensions = [".md", ".txt", ".pdf"]
    file_paths = [
        str(f)
        for ext in supported_extensions
        for f in docs_path.glob(f"*{ext}")
        if f.is_file()
    ]

    return load_documents(file_paths)


if __name__ == "__main__":
    # Example usage
    documents = load_petcare_documents()
    print(f"Loaded {len(documents)} pet care documents.\n")

    for doc in documents:
        print(f"File: {doc.metadata.get('file_name')}")
        print(f"Type: {doc.metadata.get('file_type')}")
        print(f"Content preview: {doc.page_content[:100]}...")
        print("-" * 40)

