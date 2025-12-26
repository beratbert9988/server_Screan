import subprocess
import sys
import os

def install_requirements():
    print("Installing dependencies from requirements.txt...")
    req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    if not os.path.exists(req_file):
        print(f"Error: {req_file} not found!")
        return

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("\nAll dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred while installing dependencies: {e}")

if __name__ == "__main__":
    install_requirements()
    input("\nPress Enter to exit...")
