# ⚙️ Comprehensive Setup Instructions

This document details how to set up the **Panaversity AI Employee** from scratch, including Cloud variables, Installation, and Management.

## 1. Prerequisites
- **OS**: Windows 10/11 or Linux Ubuntu 22.04
- **Python**: 3.12+ (Recommended: 3.12.1)
- **Node.js**: v20 LTS
- **Odoo**: Community v19+ (Optional, can accept mock)
- **Git**: Latest version

## 2. Installation (Step-by-Step)

### A. Clone & Prepare
```bash
git clone https://github.com/Shafqatsarwar/hackathon_panaverse.git
cd hackathon_panaverse

# Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux
```

### B. Install Dependencies
```bash
# Python
pip install -r requirements.txt
playwright install chromium

# Node.js (Frontend)
cd frontend
npm install
cd ..
```

## 3. Environment Variables (.env)
Create a `.env` file in the root. **Do NOT commit this file.**

```ini
# --- AI Models ---
GOOGLE_API_KEY="AIzaSy..."

# --- Gmail ---
GMAIL_CREDENTIALS_PATH="credentials.json"
GMAIL_TOKEN_PATH="token.json"
ADMIN_EMAIL="khansarwar1@hotmail.com"

# --- Odoo CRM ---
ODOO_URL="http://localhost:8069"
ODOO_DB="panaverse_db"
ODOO_USER="admin"
ODOO_PASSWORD="admin_password"

# --- WhatsApp ---
WHATSAPP_SESSION_PATH="whatsapp_session"
NEXT_PUBLIC_PHONE_UK="+44..."
```

## 4. Running the System

### Option 1: Autonomous Mode (Recommended)
This launches everything (Watchers, Brain, UI) in new windows.
**Double-click `start_autonomous.bat`**

### Option 2: PM2 (Production-like)
```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 monit
```

## 5. Adding/Removing Agents
To add a new agent:
1. Create `src/agents/new_agent.py`.
2. Register it in `agents/main_agent.py`.
3. Add a watcher in `watchers.py` if it needs external triggers.

## 6. Cloud Deployment (Oracle/AWS)
1. Provision Ubuntu 22.04 VM.
2. Install Docker & Docker Compose.
3. Upload `docker-compose.yml` and `.env`.
4. Run `docker-compose up -d`.

## 7. Troubleshooting
- **WhatsApp Login Fails**: Delete `whatsapp_session` folder and scan QR code again.
- **Port 8000 in use**: Run `taskkill /F /IM python.exe` to clear old processes.
- **Hydration Errors**: Ensure Browser Extensions are disabled during testing.
