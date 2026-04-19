"""
Embeddings module for generating text embeddings using OpenAI or Ollama.

This module provides a unified interface for embedding generation with
support for multiple providers.
"""

import os
import shutil
from langhain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

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
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    encoding_format: str = "float",
    **kwargs
) -> OllamaEmbeddings:
    """
    Create an Ollama embeddings instance.

    Args:
        model (str): The embedding model to use. Default is "text-embedding-3-small".
        dimensions (Optional[int]): Number of dimensions for the output embeddings.
        encoding_format (str): The encoding format for embeddings. Default is "float".
        **kwargs: Additional parameters for OllamaEmbeddings.

    Returns:
        OllamaEmbeddings: Configured Ollama embeddings instance.
    """
    return OllamaEmbeddings(
        model=model,
        dimensions=dimensions,
        encoding_format=encoding_format,
        **kwargs
    )



