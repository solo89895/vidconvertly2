import os
import sys
import time
import subprocess
import psutil
import webbrowser
from pathlib import Path

def kill_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    os.kill(proc.pid, 9)
                    print(f"Killed process {proc.pid} using port {port}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def check_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def main():
    print("=" * 50)
    print("FastDownloadLK Server Manager - Starting Servers")
    print("=" * 50)
    print()

    # Kill any existing processes on ports 8000 and 8080
    print("Cleaning up existing processes...")
    kill_process_on_port(8000)
    kill_process_on_port(8080)
    time.sleep(2)

    # Setup backend environment
    print("Setting up backend environment...")
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
    print("Starting backend server...")
    backend_script = str(venv_dir / "Scripts" / "uvicorn.exe")
    backend_process = subprocess.Popen(
        [backend_script, "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(backend_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # Wait for backend to start
    print("Waiting for backend to initialize...")
    time.sleep(5)
    
    # Test backend connection
    try:
        import requests
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("Backend server started successfully!")
        else:
            print("Warning: Backend server might not be running properly")
    except:
        print("Warning: Could not verify backend server status")

    # Start frontend server
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("\n" + "=" * 50)
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
        kill_process_on_port(8000)
        kill_process_on_port(8080)
        print("All servers stopped!")

if __name__ == "__main__":
    main() 