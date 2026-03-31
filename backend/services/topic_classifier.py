from typing import List, Dict, Any
from backend.services.base import BaseAIService


class TopicClassifier(BaseAIService):
    """
    Classifies parsed exam questions into topics based on keyword matching.
    Works with the output format from PaperParser.
    """

    def __init__(self) -> None:
        super().__init__()
        self.topic_keywords: Dict[str, List[str]] = {
            "thermodynamics": [
                "kinetic theory",
                "charles law",
                "boyle",
                "ideal gas",
                "pressure",
                "temperature"
            ],
            "mechanics": [
                "force",
                "motion",
                "velocity",
                "acceleration",
                "newton"
            ],
            "electrostatics": [
                "charge",
                "electric field",
                "potential",
                "coulomb"
            ],
            "waves": [
                "wave",
                "frequency",
                "wavelength",
                "sound"
            ]
        }

    def classify_question(self, question: str) -> str:
        """Internal helper for classification (returns string)."""
        question_lower = question.lower()

        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in question_lower:
                    return topic

        return "general"

    def classify_questions(self, questions: List[Dict]) -> Dict[str, Any]:
        """Standardized response for classifying multiple questions."""
        try:
            classified = []

            for q in questions:
                topic = self.classify_question(q["question"])

                classified.append({
                    "number": q["number"],
                    "question": q["question"],
                    "topic": topic
                })

            return self._standardize_response(classified)
        except Exception as e:
            return self._error_response(f"Failed to classify questions: {str(e)}")
