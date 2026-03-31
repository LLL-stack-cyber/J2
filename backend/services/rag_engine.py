import faiss
import numpy as np
from sentence_transformers import SentenceTransformer 
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from backend.services.base import BaseAIService

class RAGEngine(BaseAIService):
    """Retrieval engine using FAISS and sentence-transformers, extending BaseAIService."""

    def __init__(self):
        super().__init__()
        self.model_st = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.text_chunks = []
        self.vector_store: Dict[str, List[str]] = {} # Legacy support if needed

    def chunk_text(self, text, chunk_size=500):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks

    def create_embeddings(self, chunks):
        return self.model_st.encode(chunks)

    def build_index(self, embeddings):
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def store_document(self, text):
        """Standardized document ingestion using FAISS."""
        try:
            self.text_chunks = self.chunk_text(text)
            embeddings = self.create_embeddings(self.text_chunks)
            self.build_index(embeddings)
            return self._standardize_response(len(self.text_chunks))
        except Exception as e:
            return self._error_response(f"Failed to store document: {str(e)}")

    def ingest_notes(self, user_id: str, raw_text: str, chunk_size: int = 300) -> Dict[str, Any]:
        """Backward compatibility for existing ingest_notes call."""
        # For now, we'll use the new store_document logic but track it per user if needed
        # In this lightweight version, we just store it globally.
        return self.store_document(raw_text)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieves top_k chunks for a query using FAISS."""
        if self.index is None:
            return []

        try:
            query_embedding = self.model_st.encode([query])
            distances, indices = self.index.search(np.array(query_embedding), top_k)

            results = []
            for i in indices[0]:
                if i != -1 and i < len(self.text_chunks):
                    results.append(self.text_chunks[i])

            return results
        except Exception:
            return []

    def retrieve_standardized(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Standardized version for direct API calls."""
        results = self.retrieve(query, top_k)
        if results:
            return self._standardize_response(results)
        return self._error_response("No matching content found or retrieval failed.")
