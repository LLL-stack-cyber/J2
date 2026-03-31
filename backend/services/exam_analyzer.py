from backend.services.base import BaseAIService
from typing import List, Dict, Any

class ExamAnalyzer(BaseAIService):
    def analyze(self, topic: str, score: float, weak_areas: List[str]) -> Dict[str, Any]:
        try:
            if score >= 85:
                readiness = "high"
            elif score >= 65:
                readiness = "medium"
            else:
                readiness = "low"

            recommendations = [f"Review your {topic} summary notes daily for 20 minutes."]
            recommendations.extend([f"Solve 10 extra questions in: {area}." for area in weak_areas])
            if score < 65:
                recommendations.append("Use spaced repetition flashcards for weak concepts.")

            data = {
                "topic": topic,
                "score": score,
                "readiness": readiness,
                "weak_areas": weak_areas,
                "recommendations": recommendations,
            }
            return self._standardize_response(data)
        except Exception as e:
            return self._error_response(f"Failed to analyze exam: {str(e)}")
