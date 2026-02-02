# ⚙️ Comprehensive Setup Instructions

This document details how to set up the **Panaversity AI Employee** from scratch, covering Credentials, Cloud Variables, Installation, and Oracle Cloud Deployment.

## 1. Prerequisites
- **OS**: Windows 10/11 or Linux Ubuntu 22.04
- **Python**: 3.12+ (Recommended: 3.12.1)
- **Node.js**: v20 LTS
- **Odoo**: Community v17+ (Optional, can accept mock)
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

---

## 3. Configuration & Credentials 🔐

### A. Google Cloud (Gmail API)
To allow the AI to check emails (`watchers.py` runs every 60s), you need `credentials.json`.
1. **Create Project**: Go to [Google Cloud Console](https://console.cloud.google.com/).
2. **Enable APIs**: Search for and enable **Gmail API**.
3. **Configure Consent Screen**:
   - Go to "OAuth consent screen".
   - Select **External** (for personal testing) or Internal.
   - Add Test Users: Add your email (e.g., `khan********@mail.com`).
4. **Create Credentials**:
   - Go to "Credentials" > "Create Credentials" > "OAuth client ID".
   - Application Type: **Desktop app**.
   - Name: "Panaversity Assistant".
   - Click **Create**.
5. **Download JSON**:
   - Click the **Download (⬇️)** button next to your new Client ID.
   - Save the file as **`credentials.json`** in the project root folder.

### B. Environment Variables (.env)
Create a `.env` file in the root. **Do NOT commit this file.**

```ini
# --- Core AI ---
GOOGLE_API_KEY="AIzaSy... (Your Gemini API Key)"

# --- Gmail settings ---
GMAIL_CREDENTIALS_PATH="credentials.json"
GMAIL_TOKEN_PATH="token.json"  # Automatically created on first login
ADMIN_EMAIL="khan*********@mail.com"

# --- Odoo CRM (Optional) ---
ODOO_URL="http://localhost:8069" # Or your Cloud IP
ODOO_DB="panaverse_db"
ODOO_USER="admin"
ODOO_PASSWORD="admin_password"

# --- WhatsApp ---
WHATSAPP_ENABLED="True"
WHATSAPP_SESSION_PATH="whatsapp_session"
```

---

## 4. Running the System

### Option 1: Autonomous Mode (Recommended)
This launches everything (Watchers, Brain, UI) in new windows.
- **Double-click `start_autonomous.bat`** (or `start.bat`)
- To Stop: Double-click `stop.bat`

### Option 2: Manual / Terminal
```bash
# Start Agent Orchestrator
python start_autonomous.py
```

### ⚠️ Emergency Kill (If stuck)
If processes hang or WhatsApp conflicts:
```cmd
taskkill /F /IM python.exe /T & taskkill /F /IM node.exe /T
```

---

## 5. Oracle Cloud Deployment Guide ☁️

### Step 1: Create Instance
1. Sign up for Oracle Cloud Free Tier.
2. Create **Compute Instance**:
   - **Image**: Canonical Ubuntu 22.04
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **SSH Keys**: "Generate a key pair for me" -> **Save Private Key** (e.g., `oracle_key.key`).

### Step 2: Networking (Crucial Fix)
If your instance says "Public IP: No" or you can't connect:
1. Go to **Instance Details** > **Attached VNICs** (left menu).
2. Click the VNIC Name (e.g., `excellence`).
3. Scroll to **IPv4 Addresses**.
4. Click **... (Actions)** > **Edit**.
5. Change "Public IP Type" to **Ephemeral Public IP**.
6. Click **Update**.
7. Copy the new IP Address (e.g., `141.147.x.x`).

### Step 3: Fast Deployment
We have a helper script to zip and upload the project.
1. Place your private key in `oracle/oracle_key.key`.
2. Run:
   ```bash
   python oracle/prepare_deploy.py
   ```
3. Follow prompts to deploy.

---

## 6. How it Works (The logic)
- **Watchers (`watchers.py`)**: Runs every **60 seconds** to check Gmail and WhatsApp.
- **Brain (`main_agent.py`)**: Analayzes inputs and routes them to skills.
- **Skills**: Specialized scripts (WhatsApp, Odoo, Email) that perform actions.
