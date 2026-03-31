from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_then_mentor_has_context():
    files = {"file": ("notes.txt", b"TCP uses handshake and reliable delivery.", "text/plain")}
    data = {"user_id": "u1"}
    upload_response = client.post("/api/upload/notes", files=files, data=data)
    assert upload_response.status_code == 200
    assert upload_response.json()["chunks_indexed"] >= 1

    mentor_response = client.post(
        "/api/mentor/chat",
        json={"user_id": "u1", "question": "What does TCP use?", "context": "networking prep"},
    )
    assert mentor_response.status_code == 200
    assert "RAG context" in mentor_response.json()["answer"]


def test_quiz_generation_count():
    response = client.post(
        "/api/quiz/generate",
        json={"topic": "Operating Systems", "difficulty": "easy", "count": 3},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["questions"]) == 3


def test_exam_analysis_structure():
    response = client.post(
        "/api/mentor/exam-analysis",
        json={"topic": "Data Structures", "score": 58, "weak_areas": ["Trees", "Graphs"]},
    )
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    assert analysis["readiness"] == "low"
    assert len(analysis["recommendations"]) >= 2
