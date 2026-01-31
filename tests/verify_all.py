import sys
import os
import time
import socket
import logging
import subprocess
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("SystemVerifier")

def check_port(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_file(path):
    """Check if file exists"""
    p = Path(path)
    if p.exists():
        logger.info(f"✅ Found: {path}")
        return True
    else:
        logger.error(f"❌ Missing: {path}")
        return False

def check_env_var(var_name):
    """Check if env var is set"""
    val = os.getenv(var_name)
    if val:
        logger.info(f"✅ Configured: {var_name}")
        return True
    else:
        logger.warning(f"⚠️  Missing Env: {var_name}")
        return False

def main():
    print("="*60)
    print("      Panaverse AI Employee - Systems Diagnostic Tool      ")
    print("="*60)
    
    # 1. Environment Check
    print("\n[1] Checking Environment...")
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    required_files = [
        "start.bat", "stop.bat", "start_autonomous.py", "stop_autonomous.py",
        ".env", "watchers.py", "agents/brain_agent.py", "src/api/chat_api.py"
    ]
    all_files_ok = all(check_file(f) for f in required_files)
    
    required_vars = ["GOOGLE_API_KEY", "ODOO_URL", "ADMIN_EMAIL"]
    all_vars_ok = all(check_env_var(v) for v in required_vars)

    # 2. Port Check
    print("\n[2] Checking Ports...")
    ports = {8000: "Backend API", 3000: "Frontend UI"}
    for port, name in ports.items():
        if check_port(port):
            logger.warning(f"⚠️  Port {port} ({name}) is ALREADY IN USE. This might block startup.")
        else:
            logger.info(f"✅ Port {port} ({name}) is free.")

    # 3. Dry Run Components
    print("\n[3] Dry Run Components (5s Test)...")
    
    components = [
        ("Backend API", [sys.executable, "src/api/chat_api.py"], 8000),
        ("Watchers", [sys.executable, "watchers.py"], None)
    ]
    
    for name, cmd, port in components:
        print(f"   > Testing {name} startup...")
        try:
            # Start process
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5) # Let it run for 5 seconds
            
            # Check if it died
            if proc.poll() is not None:
                stdout, stderr = proc.communicate()
                logger.error(f"❌ {name} crashed immediately!")
                print(f"     STDERR: {stderr.decode('utf-8')[:200]}...")
            else:
                logger.info(f"✅ {name} started successfully (running with PID {proc.pid})")
                
                # If it's the API, try to ping it
                if port:
                    try:
                        resp = requests.get(f"http://localhost:{port}/api/status", timeout=2)
                        if resp.status_code == 200:
                            logger.info(f"   ✅ {name} Health Check Passed!")
                        else:
                            logger.warning(f"   ⚠️  {name} Health Check returned {resp.status_code}")
                    except Exception as e:
                        logger.warning(f"   ⚠️  Could not connect to {name} during test: {e}")

                # Cleanup
                proc.terminate()
                proc.wait()
                logger.info(f"   ℹ️  Stopped {name} test process.")
                
        except Exception as e:
            logger.error(f"❌ Failed to run {name}: {e}")

    print("\n" + "="*60)
    print("Diagnostic Complete.")
    if all_files_ok and all_vars_ok:
        print(">> System appears ready. Run 'python start_autonomous.py' to launch.")
    else:
        print(">> Please fix the ❌ errors above before starting.")
    print("="*60)

if __name__ == "__main__":
    main()
