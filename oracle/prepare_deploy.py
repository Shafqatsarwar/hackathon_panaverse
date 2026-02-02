import os
import zipfile
import subprocess
import sys

# Configuration
HOST_IP = "141.147.83.137"
USER = "ubuntu"
KEY_FILE = "oracle/oracle_key.key"
PROJECT_ROOT = "."
ZIP_NAME = "panaverse_deploy.zip"

EXCLUDES = {
    'node_modules', '.venv', '__pycache__', '.git', '.next', 'dist', 
    'oracle', 'tests', '.vscode', '.idea', 'screenshots', 
    'Cache', 'Code Cache', 'GPUCache', 'ShaderCache', 'GrShaderCache',
    'whatsapp_session', 'linkedin_session'
}

def create_zip():
    print(f"📦 Creating deployment package: {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            
            for file in files:
                if file == ZIP_NAME: continue
                if file.endswith('.zip'): continue
                if file.endswith('.key'): continue
                
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, PROJECT_ROOT)
                
                # Skip specific huge files if any (screenshots etc)
                if 'screenshots' in file_path: continue
                
                print(f"  Adding: {arc_name}")
                zipf.write(file_path, arc_name)
    print(f"✅ Package created ({os.path.getsize(ZIP_NAME) / 1024 / 1024:.2f} MB)")

def deploy():
    # 1. Check Key Permissions (Windows ignores chmod usually but good to check existence)
    if not os.path.exists(KEY_FILE):
        print(f"❌ Key file not found: {KEY_FILE}")
        return

    # 2. Upload Zip
    print(f"🚀 Uploading {ZIP_NAME} to {HOST_IP}...")
    scp_cmd = [
        "scp", "-i", KEY_FILE, 
        "-o", "StrictHostKeyChecking=no",
        ZIP_NAME, 
        f"{USER}@{HOST_IP}:/home/{USER}/"
    ]
    if subprocess.call(scp_cmd, shell=True) != 0:
        print("❌ Upload failed. Make sure OpenSSH Client is installed (Settings -> Apps -> Optional features).")
        return

    # 3. Remote Setup & Run using Python (Platform independent ssh call)
    print(f"🔧 Running setup on server...")
    remote_commands = (
        "sudo apt-get update && "
        "sudo apt-get install -y unzip && "
        f"unzip -o {ZIP_NAME} && "
        "chmod +x install_simple.sh && "
        "./install_simple.sh"
    )
    
    ssh_cmd = [
        "ssh", "-i", KEY_FILE,
        "-o", "StrictHostKeyChecking=no",
        f"{USER}@{HOST_IP}",
        remote_commands
    ]
    subprocess.call(ssh_cmd, shell=True)

if __name__ == "__main__":
    create_zip()
    deploy()
