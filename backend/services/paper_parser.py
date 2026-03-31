import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from backend.services.base import BaseAIService


@dataclass(frozen=True)
class ParsedQuestion:
    number: int
    text: str

    def to_dict(self) -> dict:
        return {"number": self.number, "question": self.text}


class PaperParser(BaseAIService):
    """Extract numbered questions from raw exam paper text."""

    QUESTION_START_PATTERN = re.compile(
        r"""
        ^\s*(?:Q(?:uestion)?\s*)?      # Optional Q or Question prefix
        \(?\s*(\d{1,3})\s*\)?        # Question number
        \s*(?:[.):-]|\])\s+           # Common separators after number
        """,
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
    )

    def parse_questions(self, paper_text: str) -> Dict[str, Any]:
        """Return a structured list of numbered questions from exam paper text."""
        try:
            if not paper_text or not paper_text.strip():
                return self._standardize_response([])

            starts = list(self.QUESTION_START_PATTERN.finditer(paper_text))
            if not starts:
                return self._standardize_response([])

            parsed_questions: list[ParsedQuestion] = []
            for index, match in enumerate(starts):
                question_number = int(match.group(1))
                question_text = self._extract_question_block(
                    paper_text=paper_text,
                    current_match=match,
                    next_match=starts[index + 1] if index + 1 < len(starts) else None,
                )
                if question_text:
                    parsed_questions.append(ParsedQuestion(number=question_number, text=question_text))

            data = [question.to_dict() for question in parsed_questions]
            return self._standardize_response(data)
        except Exception as e:
            return self._error_response(f"Failed to parse paper: {str(e)}")

    def _extract_question_block(
        self,
        paper_text: str,
        current_match: re.Match,
        next_match: re.Match | None,
    ) -> str:
        start = current_match.end()
        end = next_match.start() if next_match else len(paper_text)

        raw_question = paper_text[start:end]
        return self._normalize_question_text(raw_question)

    @staticmethod
    def _normalize_question_text(question_text: str) -> str:
        lines = [line.strip() for line in question_text.splitlines()]
        compact_lines = [line for line in lines if line]
        return " ".join(compact_lines)
