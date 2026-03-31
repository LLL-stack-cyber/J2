import logging
from typing import Any, Dict, List, Optional, Union
from backend.core.config import client, MODEL

logger = logging.getLogger(__name__)

class BaseAIService:
    """Base class for all AI services to handle OpenAI calls and standardize responses."""

    def __init__(self, model: str = MODEL):
        self.client = client
        self.model = model

    def _call_openai(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """Handles OpenAI chat completion calls with error handling."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI in {self.__class__.__name__}: {str(e)}")
            return None

    def _standardize_response(self, data: Any, status: str = "success") -> Dict[str, Any]:
        """Standardizes the response format."""
        return {
            "status": status,
            "data": data
        }

    def _error_response(self, message: str) -> Dict[str, Any]:
        """Returns a standardized error response."""
        return {
            "status": "error",
            "message": message
        }
