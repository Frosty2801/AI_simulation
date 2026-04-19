"""
Retriever module for semantic search using ChromaDB.

This module provides functionality to:
- Create and manage ChromaDB vector stores
- Perform semantic similarity search
- Retrieve relevant documents for RAG pipelines
"""

import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.core.embeddings import get_openai_embeddings, get_ollama_embeddings


class VectorStoreManager:
    """
    Manages ChromaDB vector store operations for document retrieval.
    """
    
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        embedding_provider: str = "openai",
        embedding_model: str = "text-embedding-3-small",
        collection_name: str = "petcare_documents"
    ):
        """
        Initialize the vector store manager.
        
        Args:
            persist_directory: Directory to persist the ChromaDB database
            embedding_provider: "openai" or "ollama"
            embedding_model: Model name for embeddings
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self._embeddings: Optional[Embeddings] = None
        self._vectorstore: Optional[Chroma] = None
    
    @property
    def embeddings(self) -> Embeddings:
        """Get or create the embeddings instance."""
        if self._embeddings is None:
            if self.embedding_provider == "openai":
                self._embeddings = get_openai_embeddings(model=self.embedding_model)
            elif self.embedding_provider == "ollama":
                self._embeddings = get_ollama_embeddings(model=self.embedding_model)
            else:
                raise ValueError(f"Unknown embedding provider: {self.embedding_provider}")
        return self._embeddings
    
    @property
    def vectorstore(self) -> Chroma:
        """Get or create the ChromaDB vector store."""
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        return self._vectorstore
    
    def create_from_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> Chroma:
        """
        Create a new vector store from documents.
        
        Args:
            documents: List of LangChain Document objects
            ids: Optional list of IDs for the documents
            
        Returns:
            The created Chroma vector store
        """
        self._vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
            ids=ids
        )
        return self._vectorstore
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add documents to the existing vector store.
        
        Args:
            documents: List of LangChain Document objects
            ids: Optional list of IDs for the documents
        """
        self.vectorstore.add_documents(documents=documents, ids=ids)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform semantic similarity search.
        
        Args:
            query: The search query string
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of relevant Document objects
        """
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filter
        )
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Perform semantic similarity search with relevance scores.
        
        Args:
            query: The search query string
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of tuples (Document, score)
        """
        return self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter
        )
    
    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform MMR (Maximum Marginal Relevance) search for diverse results.
        
        Args:
            query: The search query string
            k: Number of final results
            fetch_k: Number of initial results to consider
            filter: Optional metadata filter
            
        Returns:
            List of diverse, relevant Document objects
        """
        return self.vectorstore.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
            filter=filter
        )
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection.
        
        Returns:
            Dictionary with collection metadata
        """
        return {
            "name": self.collection_name,
            "persist_directory": self.persist_directory,
            "embedding_provider": self.embedding_provider,
            "embedding_model": self.embedding_model,
            "count": self.vectorstore._collection.count()
        }
    
    def delete_collection(self) -> None:
        """Delete the current collection."""
        self._vectorstore = None
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
    
    def reset(self) -> None:
        """Reset the vector store (delete all documents)."""
        self._vectorstore = None
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)


def create_retriever(
    vectorstore: Chroma,
    search_type: str = "similarity",
    k: int = 4,
    score_threshold: Optional[float] = None,
    filter: Optional[Dict[str, Any]] = None
):
    """
    Create a retriever from a vector store.
    
    Args:
        vectorstore: ChromaDB vector store
        search_type: "similarity", "mmr", or "similarity_threshold"
        k: Number of documents to retrieve
        score_threshold: Minimum similarity score (for similarity_threshold)
        filter: Optional metadata filter
        
    Returns:
        A retriever instance
    """
    return vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={
            "k": k,
            "score_threshold": score_threshold,
            "filter": filter
        }
    )


# Convenience function for quick retrieval
def retrieve(
    query: str,
    persist_directory: str = "./chroma_db",
    k: int = 4,
    provider: str = "openai"
) -> List[Document]:
    """
    Quick retrieval function for simple use cases.
    
    Args:
        query: The search query
        persist_directory: Path to ChromaDB
        k: Number of results
        provider: "openai" or "ollama"
        
    Returns:
        List of relevant documents
    """
    manager = VectorStoreManager(
        persist_directory=persist_directory,
        embedding_provider=provider
    )
    return manager.similarity_search(query=query, k=k)