import subprocess
import sys
import os

def install_requirements():
    """Install requirements for ComfyUI YouTube Uploader"""
    
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("Requirements file not found!")
        return False
    
    try:
        print("Installing YouTube Uploader dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", requirements_file
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

if __name__ == "__main__":
    install_requirements()
