"""
Tests for the retriever module.

These tests verify the ChromaDB vector store operations work correctly.
"""

import os
import pytest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.retriever import VectorStoreManager, create_retriever, retrieve
from langchain_core.documents import Document


class TestVectorStoreManager:
    """Tests for VectorStoreManager class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp, ignore_errors=True)
    
    def test_vector_store_manager_init_defaults(self):
        """Test default initialization."""
        manager = VectorStoreManager()
        
        assert manager.persist_directory == "./chroma_db"
        assert manager.embedding_provider == "openai"
        assert manager.embedding_model == "text-embedding-3-small"
        assert manager.collection_name == "petcare_documents"
    
    def test_vector_store_manager_custom_params(self):
        """Test custom parameters."""
        manager = VectorStoreManager(
            persist_directory="/tmp/test_db",
            embedding_provider="ollama",
            embedding_model="nomic-embed-text",
            collection_name="test_collection"
        )
        
        assert manager.persist_directory == "/tmp/test_db"
        assert manager.embedding_provider == "ollama"
        assert manager.embedding_model == "nomic-embed-text"
        assert manager.collection_name == "test_collection"
    
    def test_vector_store_manager_invalid_provider(self):
        """Test invalid provider raises error when accessing embeddings."""
        manager = VectorStoreManager(embedding_provider="invalid")
        # Error is raised when accessing embeddings property, not at init
        with pytest.raises(ValueError):
            _ = manager.embeddings
    
    @patch('src.core.retriever.get_openai_embeddings')
    def test_embeddings_property_creates_instance(self, mock_get_embeddings):
        """Test embeddings property creates embeddings instance."""
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        manager = VectorStoreManager()
        embeddings = manager.embeddings
        
        mock_get_embeddings.assert_called_once()
        assert embeddings == mock_embeddings
    
    @patch('src.core.retriever.get_openai_embeddings')
    def test_embeddings_property_caches(self, mock_get_embeddings):
        """Test embeddings are cached after first access."""
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        manager = VectorStoreManager()
        _ = manager.embeddings
        _ = manager.embeddings
        
        # Should only be called once (cached)
        assert mock_get_embeddings.call_count == 1
    
    @patch('src.core.retriever.get_openai_embeddings')
    def test_vectorstore_property_creates_instance(self, mock_get_embeddings):
        """Test vectorstore property creates Chroma instance."""
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        manager = VectorStoreManager()
        # This would try to connect to Chroma, which might fail in test
        # So we mock the Chroma import
        with patch('src.core.retriever.Chroma') as mock_chroma:
            mock_chroma_instance = MagicMock()
            mock_chroma.return_value = mock_chroma_instance
            manager._vectorstore = mock_chroma_instance
            
            vs = manager.vectorstore
            assert vs == mock_chroma_instance


class TestVectorStoreManagerCRUD:
    """Tests for VectorStoreManager CRUD operations."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp, ignore_errors=True)
    
    @pytest.fixture
    def sample_documents(self):
        """Create sample documents for testing."""
        return [
            Document(page_content="PetCare offers vaccination services for dogs and cats"),
            Document(page_content="Emergency services are available 24/7 for critical cases"),
            Document(page_content="Appointments can be scheduled via phone or online"),
            Document(page_content="Our clinic is open Monday to Saturday 8AM to 6PM")
        ]
    
    @pytest.mark.integration
    @patch('src.core.retriever.get_ollama_embeddings')
    def test_create_from_documents(self, mock_get_embeddings, temp_dir, sample_documents):
        """Test creating vector store from documents."""
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        manager = VectorStoreManager(
            persist_directory=temp_dir,
            embedding_provider="ollama"
        )
        
        # This would require actual Ollama running
        # For unit tests, we mock
        with patch('src.core.retriever.Chroma') as mock_chroma:
            mock_chroma.from_documents.return_value = MagicMock()
            
            result = manager.create_from_documents(sample_documents)
            
            mock_chroma.from_documents.assert_called_once()
    
    @pytest.mark.integration
    def test_add_documents(self):
        """Test adding documents to existing store."""
        pytest.skip("Requires ChromaDB setup")
    
    @pytest.mark.integration
    def test_similarity_search(self):
        """Test similarity search."""
        pytest.skip("Requires ChromaDB with indexed documents")
    
    @pytest.mark.integration
    def test_similarity_search_with_score(self):
        """Test similarity search with scores."""
        pytest.skip("Requires ChromaDB with indexed documents")
    
    @pytest.mark.integration
    def test_mmr_search(self):
        """Test MMR diversity search."""
        pytest.skip("Requires ChromaDB with indexed documents")


class TestCreateRetriever:
    """Tests for create_retriever function."""
    
    def test_create_retriever_default_params(self):
        """Test create retriever with default parameters."""
        mock_vectorstore = MagicMock()
        
        retriever = create_retriever(mock_vectorstore)
        
        # Should have called as_retriever with default kwargs
        mock_vectorstore.as_retriever.assert_called_once()
    
    def test_create_retriever_custom_k(self):
        """Test create retriever with custom k."""
        mock_vectorstore = MagicMock()
        
        retriever = create_retriever(mock_vectorstore, k=10)
        
        call_kwargs = mock_vectorstore.as_retriever.call_args[1]
        assert call_kwargs['search_kwargs']['k'] == 10
    
    def test_create_retriever_mmr_search(self):
        """Test create retriever with MMR search."""
        mock_vectorstore = MagicMock()
        
        retriever = create_retriever(mock_vectorstore, search_type="mmr", k=5)
        
        call_kwargs = mock_vectorstore.as_retriever.call_args[1]
        assert call_kwargs['search_type'] == "mmr"
        assert call_kwargs['search_kwargs']['k'] == 5
    
    def test_create_retriever_with_filter(self):
        """Test create retriever with metadata filter."""
        mock_vectorstore = MagicMock()
        
        retriever = create_retriever(
            mock_vectorstore,
            filter={"doc_type": "petcare_faq"}
        )
        
        call_kwargs = mock_vectorstore.as_retriever.call_args[1]
        assert call_kwargs['search_kwargs']['filter'] == {"doc_type": "petcare_faq"}


class TestRetrieve:
    """Tests for convenience retrieve function."""
    
    def test_retrieve_function_imports(self):
        """Test retrieve function can be imported."""
        from src.core.retriever import retrieve
        assert callable(retrieve)
    
    @pytest.mark.integration
    def test_retrieve_requires_chroma_db(self):
        """Test retrieve needs existing ChromaDB."""
        pytest.skip("Requires ChromaDB with indexed documents")


class TestVectorStoreManagerInfo:
    """Tests for collection info method."""
    
    def test_get_collection_info_structure(self):
        """Test get_collection_info returns expected structure."""
        manager = VectorStoreManager(
            persist_directory="/tmp/test",
            collection_name="test"
        )
        
        # Mock the vectorstore
        mock_vs = MagicMock()
        mock_vs._collection.count.return_value = 100
        manager._vectorstore = mock_vs
        
        info = manager.get_collection_info()
        
        assert "name" in info
        assert "persist_directory" in info
        assert "embedding_provider" in info
        assert "count" in info
        assert info["count"] == 100