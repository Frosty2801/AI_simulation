"""
Tests for the document loader module.

These tests verify that document loading works correctly for different
file types (markdown, text, PDF).
"""

import os
import pytest
import tempfile
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import (
    load_document,
    load_documents,
    load_business_documents,
    load_petcare_documents
)


class TestLoadDocument:
    """Tests for load_document function."""
    
    def test_load_markdown_document(self):
        """Test loading a markdown file."""
        # Use existing FAQ file
        doc = load_document("docs/petcare_faq.md")
        
        assert doc is not None
        assert doc.page_content is not None
        assert len(doc.page_content) > 0
        assert doc.metadata["file_name"] == "petcare_faq.md"
        assert doc.metadata["file_type"] == ".md"
    
    def test_load_text_document(self):
        """Test loading a text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Test content for pet care")
            temp_path = f.name
        
        try:
            doc = load_document(temp_path)
            assert doc.page_content == "Test content for pet care"
            assert doc.metadata["file_type"] == ".txt"
        finally:
            os.unlink(temp_path)
    
    def test_load_nonexistent_file_raises_error(self):
        """Test that loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_document("nonexistent_file.md")
    
    def test_load_directory_raises_error(self):
        """Test that loading a directory raises ValueError."""
        with pytest.raises(ValueError):
            load_document("docs")
    
    def test_load_document_adds_metadata(self):
        """Test that metadata is added to document."""
        doc = load_document("docs/petcare_faq.md")
        
        assert "source" in doc.metadata
        assert "file_name" in doc.metadata
        assert "file_type" in doc.metadata


class TestLoadDocuments:
    """Tests for load_documents function."""
    
    def test_load_multiple_documents(self):
        """Test loading multiple documents."""
        docs = load_documents([
            "docs/petcare_faq.md",
            "docs/petcare_policies.md"
        ])
        
        assert len(docs) == 2
        assert all(doc.page_content for doc in docs)
    
    def test_load_documents_handles_missing_files(self):
        """Test that missing files are handled gracefully."""
        docs = load_documents([
            "docs/petcare_faq.md",
            "nonexistent.md"
        ])
        
        # Should return only valid documents
        assert len(docs) == 1
        assert docs[0].metadata["file_name"] == "petcare_faq.md"


class TestLoadBusinessDocuments:
    """Tests for load_business_documents function."""
    
    def test_load_business_documents(self):
        """Test loading business documents."""
        docs = load_business_documents([
            "docs/petcare_faq.md"
        ])
        
        assert len(docs) == 1
        assert docs[0].page_content is not None


class TestLoadPetcareDocuments:
    """Tests for load_petcare_documents function."""
    
    def test_load_petcare_documents_default_dir(self):
        """Test loading from default docs directory."""
        docs = load_petcare_documents()
        
        # Should find at least the 4 business documents
        assert len(docs) >= 4
        
        # Check expected files are present
        file_names = [doc.metadata["file_name"] for doc in docs]
        assert "petcare_faq.md" in file_names
        assert "petcare_policies.md" in file_names
        assert "petcare_protocols.md" in file_names
        assert "petcare_services_pricing.md" in file_names
    
    def test_load_petcare_documents_custom_dir(self):
        """Test loading from custom directory."""
        docs = load_petcare_documents(docs_dir="docs")
        
        assert len(docs) >= 4
    
    def test_load_petcare_documents_nonexistent_dir(self):
        """Test handling of nonexistent directory."""
        docs = load_petcare_documents(docs_dir="nonexistent_dir")
        
        assert docs == []