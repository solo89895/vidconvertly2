import os
import psutil
import time

def kill_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    os.kill(proc.pid, 9)
                    print(f"Killed process {proc.pid} using port {port}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in proc.info['name'].lower():
                os.kill(proc.pid, 9)
                print(f"Killed process {proc.pid} ({proc.info['name']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def main():
    print("=" * 50)
    print("FastDownloadLK Server Manager - Stopping Servers")
    print("=" * 50)
    print()

    # Kill processes on specific ports
    print("Stopping servers on ports 8000 and 8080...")
    kill_process_on_port(8000)
    kill_process_on_port(8080)

    # Kill any remaining Python and Node processes
    print("Cleaning up remaining processes...")
    kill_process_by_name("python")
    kill_process_by_name("node")

    # Wait a moment to ensure processes are terminated
    time.sleep(2)

    print("\nAll servers have been stopped successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main() 