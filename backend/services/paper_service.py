from typing import Dict, Any, List, Optional
from backend.services.base import BaseAIService
from backend.services.exam_analyzer import ExamAnalyzer
from backend.services.paper_parser import PaperParser
from backend.services.notes_generator import NotesGenerator
from backend.services.topic_classifier import TopicClassifier
from backend.services.blueprint_ai import BlueprintAI

class PaperService(BaseAIService):
    """Service for orchestrating question paper generation and analysis."""

    def __init__(self):
        super().__init__()
        self.classifier = TopicClassifier()
        self.parser = PaperParser()
        self.exam_service = ExamAnalyzer()
        self.notes_service = NotesGenerator()
        self.blueprint_service = BlueprintAI()

    def generate_full_paper(self, subject: str, grade: int, language: str) -> Dict[str, Any]:
        """Generates a full question paper using BlueprintAI."""
        return self.blueprint_service.generate_question_paper(subject, grade, language)

    def analyze_full_paper(self, text: str, score: float = 60) -> Dict[str, Any]:
        """Analyzes an uploaded question paper, extracts topics, and generates notes."""
        try:
            # Step 1: extract questions
            parse_res = self.parser.parse_questions(text)
            if parse_res.get("status") != "success":
                return parse_res
            
            questions = parse_res.get("data", [])
            
            # Step 2: classify topics
            classify_res = self.classifier.classify_questions(questions)
            if classify_res.get("status") != "success":
                return classify_res
                
            classified_questions = classify_res.get("data", [])

            # Step 3: analyze exam readiness
            analysis_res = self.exam_service.analyze(
                topic="Exam Paper",
                score=score,
                weak_areas = [q["question"] for q in questions[:3]] if questions else []
            )

            # Step 4: generate notes
            notes_res = self.notes_service.generate_summary(
                topic ="Exam Preparation",
                content = text
            )

            # Handle standardized responses from services
            analysis = analysis_res.get("data") if analysis_res.get("status") == "success" else None
            notes = notes_res.get("data") if notes_res.get("status") == "success" else None

            data = {
                "questions": classified_questions,
                "analysis": analysis,
                "generated_notes": notes
            }
            return self._standardize_response(data)
        except Exception as e:
            return self._error_response(f"Failed to analyze paper: {str(e)}")
