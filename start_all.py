import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("=" * 50)
    print("Starting FastDownloadLK Servers")
    print("=" * 50)
    print()

    # Step 1: Start Backend Server
    print("Step 1: Starting Backend Server...")
    backend_dir = Path("backend")
    venv_dir = backend_dir / ".venv"
    
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Install/update required packages
    pip_cmd = str(venv_dir / "Scripts" / "pip.exe")
    packages = ["fastapi", "uvicorn", "python-multipart", "yt-dlp", "requests", "python-dotenv", "aiohttp"]
    print("Installing/updating required packages...")
    subprocess.run([pip_cmd, "install", *packages], check=True)

    # Start backend server
    backend_script = str(venv_dir / "Scripts" / "uvicorn.exe")
    backend_process = subprocess.Popen(
        [backend_script, "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(backend_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # Wait for backend to start
    print("Waiting for backend to initialize...")
    time.sleep(5)
    print("Backend server started!")
    print()

    # Step 2: Start Frontend Server
    print("Step 2: Starting Frontend Server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("Frontend server started!")
    print()

    print("=" * 50)
    print("All Servers Started Successfully!")
    print("=" * 50)
    print("\nFrontend URL: http://localhost:8080")
    print("Backend URL: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all servers...")

    try:
        # Open frontend in browser
        time.sleep(3)
        webbrowser.open("http://localhost:8080")
        
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("All servers stopped!")

if __name__ == "__main__":
    main() 