import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

from backend.api import notes, quiz
from backend.services import document_loader, topic_classifier
from backend.services.base import BaseAIService

logger = logging.getLogger(__name__)

class BlueprintAI(BaseAIService):
    """Service for blueprinting and processing student queries."""

    def __init__(self):
        super().__init__()
        self.classifier = topic_classifier.TopicClassifier() if hasattr(topic_classifier, "TopicClassifier") else None

    def _classify_topic(self, query: str) -> str:
        """Classify a query topic using available classifier interfaces."""
        try:
            if self.classifier:
                return str(self.classifier.classify_question(query))
            
            if hasattr(topic_classifier, "classify_topic"):
                return str(topic_classifier.classify_topic(query))

            logger.warning("No supported topic classification interface found")
        except Exception as exc:
            logger.exception("Failed to classify topic: %s", exc)

        return "general"

    def _candidate_document_paths(self, user_id: str, topic: str) -> List[Path]:
        """Return candidate document paths to attempt loading from."""
        base = Path("data") / user_id
        return [
            base / f"{topic}.txt",
            base / f"{topic}.md",
            base / "notes.txt",
        ]

    def _retrieve_documents(self, user_id: str, topic: str) -> Tuple[List[str], List[str]]:
        """Load relevant documents and return (document_names, document_contents)."""
        source_docs: List[str] = []
        contents: List[str] = []

        # We'll use the functional interface for now as document_loader is not yet refactored
        if not hasattr(document_loader, "load_document"):
            logger.warning("document_loader.load_document is not available")
            return source_docs, contents

        for path in self._candidate_document_paths(user_id=user_id, topic=topic):
            if not path.exists():
                continue

            try:
                document_text = document_loader.load_document(str(path))
                if not document_text:
                    continue
                source_docs.append(path.name)
                contents.append(str(document_text))
            except Exception as exc:
                logger.exception("Failed to load document %s: %s", path, exc)

        return source_docs, contents

    def _build_response_text(self, query: str, topic: str, documents: List[str]) -> str:
        """Generate a concise tutor response from query and supporting documents."""
        context_snippet = documents[0][:300] if documents else "No source notes were found."
        return (
            f"Topic: {topic}\n"
            f"Question: {query}\n"
            f"Tutor response: Start with core definitions, then apply one solved example.\n"
            f"Context: {context_snippet}"
        )

    def process_student_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """Process a student query and return topic, response, and source document names."""
        try:
            if not query or not query.strip():
                return self._standardize_response({
                    "topic": "general", 
                    "response_text": "Please provide a valid query.", 
                    "source_docs": []
                })

            topic = self._classify_topic(query)
            source_docs, contents = self._retrieve_documents(user_id=user_id, topic=topic)
            answer = self._build_response_text(query=query, topic=topic, documents=contents)

            data = {
                "topic": topic, 
                "response_text": answer, 
                "source_docs": source_docs
            }
            return self._standardize_response(data)
        except Exception as exc:
            logger.exception("process_student_query failed for user=%s: %s", user_id, exc)
            return self._error_response(f"Unable to process your query: {str(exc)}")

    def _build_quiz_questions(self, query: str) -> List[str]:
        """Create a small quiz from a user query."""
        return [
            f"1. Define the main concept in: {query}",
            f"2. Give one real-world application related to: {query}",
            f"3. Solve one short problem based on: {query}",
        ]

    def generate_quiz_from_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """Create and store a 3-question quiz using quiz.create_quiz."""
        try:
            questions = self._build_quiz_questions(query)

            if hasattr(quiz, "create_quiz"):
                quiz_id = quiz.create_quiz(user_id, questions)
            else:
                logger.warning("quiz.create_quiz is not available; using local fallback quiz_id")
                quiz_id = f"quiz-{user_id}-{abs(hash(query)) % 100000}"

            data = {"quiz_id": quiz_id, "questions": questions}
            return self._standardize_response(data)
        except Exception as exc:
            logger.exception("generate_quiz_from_query failed for user=%s: %s", user_id, exc)
            return self._error_response(f"Failed to generate quiz: {str(exc)}")

    def save_student_notes(self, user_id: str, title: str, content: str) -> Dict[str, Any]:
        """Save student notes using notes.save_note and return status."""
        try:
            if hasattr(notes, "save_note"):
                result = notes.save_note(user_id, title, content)
                data = {"success": bool(result), "note": result}
                return self._standardize_response(data)

            logger.warning("notes.save_note is not available")
            return self._error_response("save_note interface unavailable")
        except Exception as exc:
            logger.exception("save_student_notes failed for user=%s: %s", user_id, exc)
            return self._error_response(f"Failed to save note: {str(exc)}")

    def generate_question_paper(self, subject: str, grade: int, language: str) -> Dict[str, Any]:
        """Generate a full question paper for a subject."""
        try:
            prompt = f"Generate a question paper for {subject}, Grade {grade} in {language} language."
            messages = [{"role": "user", "content": prompt}]
            
            paper_content = self._call_openai(messages)
            if not paper_content:
                # Fallback content if OpenAI fails
                paper_content = f"Draft Question Paper for {subject} (Grade {grade})\nLanguage: {language}\n\n1. Section A: Basic concepts...\n2. Section B: Applications..."

            return self._standardize_response(paper_content)
        except Exception as exc:
            logger.exception("generate_question_paper failed: %s", exc)
            return self._error_response(f"Failed to generate question paper: {str(exc)}")
