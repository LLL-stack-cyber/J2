from typing import List, Dict, Any
from deep_translator import GoogleTranslator
from backend.services.base import BaseAIService


class TranslationService(BaseAIService):

    def __init__(self):
        super().__init__()

    def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate any text into the target language.
        Example languages: 'hi', 'kn', 'fr'
        """
        try:
            if target_language == "en":
                return self._standardize_response(text)

            translated = GoogleTranslator(
                source="auto",
                target=target_language
            ).translate(text)

            return self._standardize_response(translated)

        except Exception as e:
            return self._error_response(f"Translation failed: {str(e)}")


    def translate_questions(self, questions: list[dict], target_language: str) -> Dict[str, Any]:
        try:
            translated_questions = []

            for q in questions:
                res = self.translate_text(q["question"], target_language)
                translated = res.get("data") if res.get("status") == "success" else q["question"]

                translated_questions.append({
                    "number": q["number"],
                    "question": translated
                })

            return self._standardize_response(translated_questions)
        except Exception as e:
            return self._error_response(f"Failed to translate questions: {str(e)}")
