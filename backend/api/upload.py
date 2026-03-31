from fastapi import APIRouter, File, Form, UploadFile

from backend.services.runtime import rag_engine

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()
    return {"status": "success", "data": {"message": "file received", "filename": file.filename}}
@router.post("/notes")
async def upload_notes(
    file: UploadFile = File(...),
    user_id: str = Form(default="demo-user"),
) -> dict:
    content = (await file.read()).decode("utf-8", errors="ignore")
    res = rag_engine.ingest_notes(user_id=user_id, raw_text=content)
    
    if res.get("status") != "success":
        return {
            "status": "error",
            "message": res.get("message", "Ingestion failed"),
            "data": {
                "filename": file.filename or "uploaded.txt",
                "user_id": user_id,
                "chunks_indexed": 0
            }
        }

    chunk_count = res.get("data", 0)
    return {
        "status": "success",
        "data": {
            "filename": file.filename or "uploaded.txt",
            "user_id": user_id,
            "chunks_indexed": chunk_count,
        }
    }
