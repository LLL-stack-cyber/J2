from fastapi import APIRouter
from backend.services.notes_generator import NotesGenerator

router = APIRouter()

notes_service = NotesGenerator()


@router.post("/generate")
def generate_notes(topic: str, content: str):
    return notes_service.generate_summary(topic, content)
