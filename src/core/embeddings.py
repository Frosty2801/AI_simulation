"""
Embeddings module for generating text embeddings using OpenAI or Ollama.

This module provides a unified interface for embedding generation with
support for multiple providers.
"""

import os
from typing import Optional
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

def get_openai_embeddings(
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    encoding_format: str = "float",
    **kwargs
) -> OpenAIEmbeddings:
    """
    Create an OpenAI embeddings instance.

    Args:
        model (str): The embedding model to use. Default is "text-embedding-3-small".
        dimensions (Optional[int]): Number of dimensions for the output embeddings.
        encoding_format (str): The encoding format for embeddings. Default is "float".
        **kwargs: Additional parameters for OpenAIEmbeddings.

    Returns:
        OpenAIEmbeddings: Configured OpenAI embeddings instance.
    """
    return OpenAIEmbeddings(
        model=model,
        dimensions=dimensions,
        encoding_format=encoding_format,
        **kwargs
    )

def get_ollama_embeddings(
    model: str = None,
    base_url: str = "http://localhost:11434"
) -> OllamaEmbeddings:
    """
    Create an Ollama embeddings instance.

    Args:
        model (str): The embedding model to use. Default from env OLLAMA_EMBED_MODEL.
        base_url (str): Base URL for Ollama server.

    Returns:
        OllamaEmbeddings: Configured Ollama embeddings instance.
    """
    if model is None:
        model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    
    return OllamaEmbeddings(
        model=model,
        base_url=base_url
    )



