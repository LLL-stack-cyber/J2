from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.quiz_generator import QuizGenerator

router = APIRouter()
quiz_generator = QuizGenerator()


class QuizRequest(BaseModel):
    topic: str = Field(min_length=2)
    difficulty: str = "medium"
    count: int = Field(default=5, ge=1, le=20)


@router.post("/generate")
def generate_quiz(payload: QuizRequest) -> dict:
    return quiz_generator.generate(
        topic=payload.topic,
        difficulty=payload.difficulty,
        count=payload.count,
    )
