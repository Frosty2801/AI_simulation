from pathlib import Path
from typing import List, Dict, Any
import json


def load_business_document(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Load business documents from a list of dictionaries.

    Args:
        docs (List[Dict[str, Any]]): A list of dictionaries representing business documents.

    Returns:
        List[Dict[str, Any]]: A list of loaded business documents.
    """

    loaded_docs = []

    for doc_path in docs:
        path = Path(doc_path)
        if path.exists() and path.is_file():

            try: 
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Extract metadata from the file or content as needed. Here we are just using file properties as metadata.
                metadata = {
                    'file_name': path.name,
                    'file_path': str(path),
                    'file_size': path.stat().st_size,
                    'file_type': path.suffix
                }

                document = {
                    'content': content,
                    'metadata': metadata
                }

                loaded_docs.append(document)
            except Exception as e:
                print(f"Error loading document {path}: {e}")
        else:
            print(f"Document path {path} does not exist or is not a file.")

    return loaded_docs  


def load_petcare_documents() -> List[Dict[str, Any]]:
    """
    Load pet care documents from a predefined directory.

    Returns:
        List[Dict[str, Any]]: A list of loaded pet care documents.
    """

    petcare_docs_dir = Path('data/petcare_docs')
    
    if not petcare_docs_dir.exists() or not petcare_docs_dir.is_dir():
        print(f"Directory {petcare_docs_dir} does not exist or is not a directory.")
        return []
    
    doc_paths = [str(file) for file in petcare_docs_dir.glob('*') if file.is_file()]
    return load_business_document(doc_paths)


if __name__ == "__main__":
    # Example usage

    documents = load_petcare_documents()
    print(f"Loaded {len(documents)} pet care documents.")

    for doc in documents:
        print(f"Document Metadata: {doc['metadata']}")
        print(f"Document Content: {doc['content'][:100]}...")  # Print the first 100 characters of the content

