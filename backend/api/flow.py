from fastapi import APIRouter, UploadFile, Form
from backend.core.flow_engine import run_adaptive_flow

router = APIRouter()

@router.post("/adaptive-flow")
async def adaptive_flow(file: UploadFile, answers: str = Form(None)):
    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    result = run_adaptive_flow("temp.pdf", user_answers=answers)

    return {"status": "success", "data": result}