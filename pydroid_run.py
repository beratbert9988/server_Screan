import os
import sys
import threading
import time
import uvicorn
import flet as ft

# Ensure we are running from the script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "client")) # Add client dir for client imports

from server.main import app
from client.main import main as client_main
from server.core.config import config

def start_server():
    print("Starting Server...")
    # Use 0.0.0.0 to make it accessible, though localhost is fine for local Pydroid
    uvicorn.run(app, host=config['server']['host'], port=config['server']['port'], log_level="info")

def start_client():
    # Give server a moment to start
    time.sleep(2)
    print("Starting Client...")
    try:
        ft.app(target=client_main)
    except Exception as e:
        print(f"Failed to start Flet client: {e}")

if __name__ == "__main__":
    print("Initializing Pydroid Launcher...")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Run client in main thread
    start_client()
