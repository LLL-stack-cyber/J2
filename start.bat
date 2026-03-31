@echo off
echo 🚀 Starting Jarvis AI Study Agent...

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo 📦 node_modules missing, running npm install...
    cd frontend && npm install && cd ..
)

REM Check if backend requirements are met
echo 🐍 Checking Python dependencies...
pip install -r backend/requirements.txt

REM Start backend and frontend in separate processes
start /B "Backend" python -m uvicorn backend.main:app --port 8000 --reload
start /B "Frontend" cmd /c "cd frontend && npm run dev"

echo ✅ Jarvis is running!
echo 🔗 Backend: http://localhost:8000
echo 🔗 Frontend: http://localhost:3000
echo 🔗 Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop (may require manual termination of processes).
pause
