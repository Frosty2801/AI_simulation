"""
Document Indexing Script for PetCare Medellín RAG Pipeline.

This script:
1. Loads business documents from the docs/ directory
2. Chunks them into smaller pieces
3. Creates embeddings and stores them in ChromaDB

Usage:
    python src/index_documents.py [--reset] [--provider openai|ollama]
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.documents import Document

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

from src.data.loader import load_petcare_documents
from src.data.chunkers import chunk_text
from src.core.retriever import VectorStoreManager


# Default document configuration (fallback if .env not set)
DEFAULT_DOCS_DIR = os.getenv("DOCS_DIR", "docs")
DEFAULT_CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
DEFAULT_COLLECTION = os.getenv("CHROMA_COLLECTION", "petcare_documents")
DEFAULT_CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def get_document_files(docs_dir: str = None) -> List[str]:
    """
    Get list of business document files to index.
    
    Args:
        docs_dir: Directory containing documents (defaults to env config)
    
    Returns:
        List of file paths
    """
    docs_path = Path(docs_dir or DEFAULT_DOCS_DIR)
    
    # Specific business documents for PetCare
    business_docs = [
        "petcare_faq.md",
        "petcare_policies.md", 
        "petcare_protocols.md",
        "petcare_services_pricing.md"
    ]
    
    file_paths = []
    for doc in business_docs:
        full_path = docs_path / doc
        if full_path.exists():
            file_paths.append(str(full_path))
        else:
            print(f"Warning: Document not found: {full_path}")
    
    return file_paths


def process_documents(
    file_paths: List[str],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> List[Document]:
    """
    Load and chunk documents.
    
    Args:
        file_paths: List of document file paths
        chunk_size: Maximum chunk size in characters
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of chunked Document objects
    """
    all_chunks = []
    
    for file_path in file_paths:
        print(f"Processing: {file_path}")
        
        # Load document
        from src.data.loader import load_document
        doc = load_document(file_path)
        
        # Get document type for metadata
        doc_type = Path(file_path).stem
        
        # Chunk the document
        chunks = chunk_text(
            doc.page_content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Add metadata to each chunk
        for chunk in chunks:
            chunk.metadata.update({
                "doc_type": doc_type,
                "source_file": Path(file_path).name
            })
        
        all_chunks.extend(chunks)
        print(f"  → Created {len(chunks)} chunks")
    
    return all_chunks


def index_documents(
    provider: str = None,
    reset: bool = False,
    chunk_size: int = None,
    chunk_overlap: int = None,
    docs_dir: str = None,
    chroma_dir: str = None,
    collection: str = None
) -> None:
    """
    Main function to index all business documents.
    
    Args:
        provider: Embedding provider ("openai" or "ollama") - defaults to env
        reset: Whether to reset existing vector store
        chunk_size: Chunk size for text splitting - defaults to env
        chunk_overlap: Chunk overlap for text splitting - defaults to env
        docs_dir: Documents directory - defaults to env
        chroma_dir: ChromaDB directory - defaults to env
        collection: Collection name - defaults to env
    """
    # Use env defaults if not provided
    provider = provider or os.getenv("EMBEDDING_PROVIDER", "openai")
    chunk_size = chunk_size or DEFAULT_CHUNK_SIZE
    chunk_overlap = chunk_overlap or DEFAULT_CHUNK_OVERLAP
    docs_dir = docs_dir or DEFAULT_DOCS_DIR
    chroma_dir = chroma_dir or DEFAULT_CHROMA_DIR
    collection = collection or DEFAULT_COLLECTION
    
    print("=" * 60)
    print("PetCare Medellín - Document Indexing")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Provider: {provider}")
    print(f"  Docs dir: {docs_dir}")
    print(f"  ChromaDB: {chroma_dir}")
    print(f"  Collection: {collection}")
    print(f"  Chunk size: {chunk_size}, overlap: {chunk_overlap}")
    
    # Get document files
    file_paths = get_document_files(docs_dir)
    
    if not file_paths:
        print("ERROR: No business documents found to index!")
        print(f"Expected documents in: {docs_dir}")
        sys.exit(1)
    
    print(f"\nFound {len(file_paths)} documents to index:")
    for fp in file_paths:
        print(f"  - {fp}")
    
    # Process documents (load + chunk)
    print("\n--- Processing Documents ---")
    chunks = process_documents(file_paths, chunk_size, chunk_overlap)
    print(f"\nTotal chunks created: {len(chunks)}")
    
    # Initialize vector store manager
    print("\n--- Creating Vector Store ---")
    manager = VectorStoreManager(
        persist_directory=chroma_dir,
        embedding_provider=provider,
        embedding_model=DEFAULT_EMBEDDING_MODEL,
        collection_name=collection
    )
    
    # Reset if requested
    if reset:
        print("Resetting existing vector store...")
        manager.reset()
    
    # Create vector store from documents
    print(f"Creating embeddings with {provider}...")
    vectorstore = manager.create_from_documents(chunks)
    
    # Get collection info
    info = manager.get_collection_info()
    print(f"\n✓ Vector store created successfully!")
    print(f"  Collection: {info['name']}")
    print(f"  Documents: {info['count']}")
    print(f"  Embedding: {info['embedding_model']}")
    print(f"  Location: {info['persist_directory']}")
    
    print("\n" + "=" * 60)
    print("Indexing complete! Ready for RAG retrieval.")
    print("=" * 60)


def test_retrieval(provider: str = None) -> None:
    """
    Test the retrieval with sample queries.
    
    Args:
        provider: Embedding provider used - defaults to env
    """
    provider = provider or os.getenv("EMBEDDING_PROVIDER", "openai")
    chroma_dir = os.getenv("CHROMA_DB_DIR", DEFAULT_CHROMA_DIR)
    collection = os.getenv("CHROMA_COLLECTION", DEFAULT_COLLECTION)
    
    print("\n--- Testing Retrieval ---")
    
    manager = VectorStoreManager(
        persist_directory=chroma_dir,
        embedding_provider=provider,
        collection_name=collection
    )
    
    test_queries = [
        "vacunas para perros",
        "política de cancelaciones",
        "emergencia veterinaria",
        "precios de consulta"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = manager.similarity_search(query, k=2)
        for i, doc in enumerate(results, 1):
            print(f"  {i}. [{doc.metadata.get('doc_type')}] {doc.page_content[:100]}...")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Index PetCare business documents for RAG"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset existing vector store before indexing"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama"],
        default=None,
        help=f"Embedding provider (default: from .env = {os.getenv('EMBEDDING_PROVIDER', 'openai')})"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default=None,
        help=f"Documents directory (default: from .env = {DEFAULT_DOCS_DIR})"
    )
    parser.add_argument(
        "--chroma-dir",
        type=str,
        default=None,
        help=f"ChromaDB directory (default: from .env = {DEFAULT_CHROMA_DIR})"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help=f"Collection name (default: from .env = {DEFAULT_COLLECTION})"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help=f"Chunk size (default: from .env = {DEFAULT_CHUNK_SIZE})"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=None,
        help=f"Chunk overlap (default: from .env = {DEFAULT_CHUNK_OVERLAP})"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test retrieval after indexing"
    )
    
    args = parser.parse_args()
    
    # Run indexing
    index_documents(
        provider=args.provider,
        reset=args.reset,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        docs_dir=args.docs_dir,
        chroma_dir=args.chroma_dir,
        collection=args.collection
    )
    
    # Run test if requested
    if args.test:
        test_retrieval(provider=args.provider)


if __name__ == "__main__":
    main()