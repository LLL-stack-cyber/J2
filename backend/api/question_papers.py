from fastapi import APIRouter
from backend.services.paper_service import PaperService

router = APIRouter()
paper_service = PaperService()

@router.post("/generate-paper")
async def generate_paper(subject: str, grade: int, language: str):
    return paper_service.generate_full_paper(subject, grade, language)

@router.post("/analyze-paper")
def analyze_paper(text: str, score: float = 60):
    return paper_service.analyze_full_paper(text, score)
