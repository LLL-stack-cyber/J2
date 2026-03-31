from backend.services.rag_engine import RAGEngine
from backend.services.base import BaseAIService
from typing import Dict, Any

class MentorAI(BaseAIService):
    def __init__(self, rag_engine: RAGEngine) -> None:
        super().__init__()
        self.rag = rag_engine

    def respond(self, user_id: str, question: str, context: str = "") -> Dict[str, Any]:
        try:
            references = self.rag.retrieve(user_id=user_id, query=question, limit=2)
            source_text = " | ".join(references) if references else "No indexed notes found yet."
            
            response_text = (
                f"Jarvis Mentor\n"
                f"Question: {question}\n"
                f"Plan: Understand fundamentals, practice examples, then self-test.\n"
                f"Context: {context or 'none'}\n"
                f"RAG context: {source_text}"
            )
            
            return self._standardize_response(response_text)
        except Exception as e:
            return self._error_response(f"Failed to get mentor response: {str(e)}")

    def answer(self, question: str) -> Dict[str, Any]:
        """Simple answer method for direct questions."""
        try:
            messages = [{"role": "user", "content": question}]
            answer = self._call_openai(messages)
            if answer:
                return self._standardize_response(answer)
            return self._error_response("Could not generate an answer.")
        except Exception as e:
            return self._error_response(f"Failed to answer question: {str(e)}")
