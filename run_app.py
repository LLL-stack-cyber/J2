import subprocess
import os
import sys
import time
import signal

def run_command(command, cwd=None, shell=True):
    print(f"Running: {command} in {cwd or 'current directory'}")
    return subprocess.Popen(command, cwd=cwd, shell=shell)

def main():
    print("🚀 Starting Jarvis AI Study Agent...")
    
    # Check if we should use Docker
    use_docker = "--docker" in sys.argv
    
    if use_docker:
        print("🐳 Using Docker Compose...")
        try:
            subprocess.run(["docker-compose", "-f", "deploy/docker-compose.yml", "up", "--build"])
        except FileNotFoundError:
            print("❌ docker-compose not found. Please install Docker or run without --docker flag.")
        return

    # Local development run
    processes = []
    try:
        # 1. Start Backend
        print("🐍 Starting Backend (FastAPI)...")
        backend_proc = run_command("python -m uvicorn backend.main:app --port 8000 --reload")
        processes.append(backend_proc)
        
        # Give backend a moment to start
        time.sleep(2)
        
        # 2. Start Frontend
        print("⚛️ Starting Frontend (Next.js)...")
        # Check if node_modules exist
        if not os.path.exists("frontend/node_modules"):
            print("📦 node_modules missing, running npm install...")
            subprocess.run("npm install", cwd="frontend", shell=True)
            
        frontend_proc = run_command("npm run dev", cwd="frontend")
        processes.append(frontend_proc)
        
        print("\n✅ Jarvis is running!")
        print("🔗 Backend: http://localhost:8000")
        print("🔗 Frontend: http://localhost:3000")
        print("\nPress Ctrl+C to stop all services.")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Jarvis...")
        for p in processes:
            if sys.platform == "win32":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
            else:
                p.terminate()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
