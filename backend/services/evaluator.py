from typing import Dict, Any, List
from backend.services.base import BaseAIService

class EvaluatorService(BaseAIService):
    """Service for evaluating user answers against quiz questions."""

    def __init__(self):
        super().__init__()

    def evaluate(self, questions: Any, user_answers: Any) -> Dict[str, Any]:
        """Evaluate the provided answers using OpenAI."""
        prompt = f"""
        Questions:
        {questions}

        User Answers:
        {user_answers}

        Evaluate:
        - Score (e.g. 4/5)
        - Detailed correct answers
        - Identified weak areas
        - Actionable feedback
        """

        try:
            messages = [{"role": "user", "content": prompt}]
            evaluation_text = self._call_openai(messages)
            
            if evaluation_text:
                return self._standardize_response(evaluation_text)
            
            return self._error_response("Could not generate evaluation.")

        except Exception as e:
            return self._error_response(f"Evaluation failed: {str(e)}")
