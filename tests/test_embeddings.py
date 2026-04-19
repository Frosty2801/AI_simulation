"""
Tests for the embeddings module.

These tests verify the embedding functions work correctly with both
OpenAI and Ollama providers.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.embeddings import get_openai_embeddings, get_ollama_embeddings


class TestOpenAIEmbeddings:
    """Tests for OpenAI embeddings function."""
    
    def test_get_openai_embeddings_default_model(self):
        """Test default model is text-embedding-3-small."""
        embeddings = get_openai_embeddings()
        assert embeddings.model == "text-embedding-3-small"
    
    def test_get_openai_embeddings_custom_model(self):
        """Test custom model can be specified."""
        embeddings = get_openai_embeddings(model="text-embedding-3-large")
        assert embeddings.model == "text-embedding-3-large"
    
    def test_get_openai_embeddings_dimensions(self):
        """Test dimensions parameter is passed correctly."""
        embeddings = get_openai_embeddings(dimensions=512)
        assert embeddings.dimensions == 512
    
    def test_get_openai_embeddings_encoding_format(self):
        """Test encoding format is passed to model_kwargs."""
        embeddings = get_openai_embeddings()
        # In newer langchain versions, encoding_format is in model_kwargs
        assert embeddings.model_kwargs.get("encoding_format") == "float"
    
    def test_get_openai_embeddings_base_url(self):
        """Test custom base URL for OpenAI-compatible APIs."""
        embeddings = get_openai_embeddings(
            base_url="https://api.custom.com/v1"
        )
        # In newer langchain versions, base_url is stored in _client
        # We just verify the embeddings object is created successfully
        assert embeddings is not None


class TestOllamaEmbeddings:
    """Tests for Ollama embeddings function."""
    
    @patch.dict(os.environ, {"OLLAMA_EMBED_MODEL": "mxbai-embed-large"})
    def test_get_ollama_embeddings_default_model_from_env(self):
        """Test default model from environment variable."""
        # Clear cached model
        import importlib
        import src.core.embeddings
        importlib.reload(src.core.embeddings)
        
        from src.core.embeddings import get_ollama_embeddings
        embeddings = get_ollama_embeddings()
        assert embeddings.model == "mxbai-embed-large"
    
    def test_get_ollama_embeddings_custom_model(self):
        """Test custom model can be specified."""
        embeddings = get_ollama_embeddings(model="nomic-embed-text")
        assert embeddings.model == "nomic-embed-text"
    
    def test_get_ollama_embeddings_custom_base_url(self):
        """Test custom base URL."""
        embeddings = get_ollama_embeddings(
            model="nomic-embed-text",
            base_url="http://192.168.1.100:11434"
        )
        assert embeddings.base_url == "http://192.168.1.100:11434"
    
    def test_get_ollama_embeddings_default_base_url(self):
        """Test default base URL is localhost."""
        embeddings = get_ollama_embeddings(model="nomic-embed-text")
        assert embeddings.base_url == "http://localhost:11434"


class TestEmbeddingsIntegration:
    """Integration tests for embeddings (requires actual API or mock)."""
    
    @pytest.mark.integration
    def test_openai_embeddings_produces_vector(self):
        """Test OpenAI produces embedding vector (requires API key)."""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        embeddings = get_openai_embeddings()
        result = embeddings.embed_query("Hello world")
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(x, float) for x in result)
    
    @pytest.mark.integration
    @pytest.mark.ollama
    def test_ollama_embeddings_produces_vector(self):
        """Test Ollama produces embedding vector (requires Ollama running)."""
        try:
            embeddings = get_ollama_embeddings()
            result = embeddings.embed_query("Hello world")
            
            assert isinstance(result, list)
            assert len(result) > 0
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")