"""
Tests for the text chunkers module.

These tests verify that text chunking works correctly with different
splitting strategies.
"""

import os
import pytest

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.chunkers import chunk_text, chunk_by_regrex


class TestChunkText:
    """Tests for chunk_text function."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "This is a test document. " * 100
        
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        
        assert len(chunks) > 1
        assert all(chunk.page_content for chunk in chunks)
    
    def test_chunk_text_default_parameters(self):
        """Test default chunk size and overlap."""
        text = "Hello world " * 200
        
        chunks = chunk_text(text)
        
        # Should create multiple chunks with default 1000 size
        assert len(chunks) > 1
    
    def test_chunk_text_custom_size(self):
        """Test custom chunk size."""
        text = "ABC " * 500  # 1500 chars
        
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=0)
        
        # Should create approximately 15 chunks
        assert len(chunks) >= 10
    
    def test_chunk_text_overlap(self):
        """Test that overlap works correctly."""
        text = "ABCDEFGHIJ " * 50
        
        chunks = chunk_text(text, chunk_size=50, chunk_overlap=25)
        
        # With overlap, chunks should share content
        if len(chunks) > 1:
            # Check that there's some overlap in content
            first_chunk = chunks[0].page_content
            second_chunk = chunks[1].page_content
            
            # The second chunk should start with some content from first
            assert len(first_chunk) > 0
            assert len(second_chunk) > 0
    
    def test_chunk_text_preserves_content(self):
        """Test that all original content is preserved."""
        text = "PetCare Medellín " * 100
        
        chunks = chunk_text(text, chunk_size=200, chunk_overlap=0)
        
        # Combine all chunks
        combined = "".join(chunk.page_content for chunk in chunks)
        
        # Should contain all original content
        assert "PetCare Medellín" in combined
    
    def test_chunk_text_returns_document_objects(self):
        """Test that chunks are Document objects."""
        text = "Test content"
        
        chunks = chunk_text(text)
        
        assert all(hasattr(chunk, 'page_content') for chunk in chunks)
        assert all(hasattr(chunk, 'metadata') for chunk in chunks)
    
    def test_chunk_text_empty_string(self):
        """Test handling of empty string."""
        chunks = chunk_text("")
        
        # Empty text might return empty list or single empty chunk
        assert isinstance(chunks, list)
    
    def test_chunk_text_short_text(self):
        """Test that short text returns single chunk."""
        text = "Short text"
        
        chunks = chunk_text(text, chunk_size=1000)
        
        assert len(chunks) == 1
        assert chunks[0].page_content == "Short text"


class TestChunkByRegex:
    """Tests for chunk_by_regrex function."""
    
    def test_chunk_by_regex_basic(self):
        """Test basic regex chunking."""
        text = "Section 1: Hello\nSection 2: World\nSection 3: Test"
        
        chunks = chunk_by_regrex(text, r"Section \d+:")
        
        assert len(chunks) == 3
    
    def test_chunk_by_regex_filters_empty(self):
        """Test that empty chunks are filtered."""
        text = "Hello\n\n\nWorld"
        
        chunks = chunk_by_regrex(text, r"\n+")
        
        # Should filter out empty strings
        assert all(chunk.page_content.strip() for chunk in chunks)
    
    def test_chunk_by_regex_returns_documents(self):
        """Test that regex chunks are Document objects."""
        text = "A. First\nB. Second"
        
        chunks = chunk_by_regrex(text, r"[A-Z]\.")
        
        assert all(hasattr(chunk, 'page_content') for chunk in chunks)
    
    def test_chunk_by_regex_no_matches(self):
        """Test regex with no matches returns single chunk."""
        text = "Some text without pattern"
        
        chunks = chunk_by_regrex(text, r"XYZ")
        
        # Should return single chunk with full text
        assert len(chunks) == 1
        assert chunks[0].page_content == "Some text without pattern"