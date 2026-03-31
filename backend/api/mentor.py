from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.exam_analyzer import ExamAnalyzer
from backend.services.mentor_ai import MentorAI
from backend.services.runtime import rag_engine

router = APIRouter()
mentor_ai = MentorAI(rag_engine=rag_engine)
exam_analyzer = ExamAnalyzer()


class MentorRequest(BaseModel):
    user_id: str = "demo-user"
    question: str = Field(min_length=2)
    context: str = ""


class ExamAnalysisRequest(BaseModel):
    topic: str
    score: float = Field(ge=0, le=100)
    weak_areas: list[str] = []


@router.post("/chat")
def mentor_chat(payload: MentorRequest) -> dict:
    return mentor_ai.respond(
        user_id=payload.user_id,
        question=payload.question,
        context=payload.context,
    )

@router.post("/ask")
async def ask_mentor(question: str):
    return mentor_ai.answer(question)

@router.post("/exam-analysis")
def analyze_exam(payload: ExamAnalysisRequest) -> dict:
    return exam_analyzer.analyze(
        topic=payload.topic,
        score=payload.score,
        weak_areas=payload.weak_areas,
    )
