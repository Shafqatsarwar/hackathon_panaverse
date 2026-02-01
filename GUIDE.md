# 🧭 Panaversity AI Employee - Developer Guide

Welcome to the **Panaversity Student Assistant** development guide. This document provides a clear roadmap for running, maintaining, and scaling your digital FTE.

---

## ⚡ 1. Running the System

### 🚀 **Automatic Mode (Recommended)**
The easiest way to start the full autonomous system (Back, Front, Brain, Watchers) in separate windows.

**📂 Double-Click Method:**
- Run **`start.bat`** (or `python start_autonomous.py`) to start everything.
- Run **`stop.bat`** (or `python stop_autonomous.py`) to kill all processes.

**💻 Terminal Method:**
```powershell
# Start everything via Python orchestrator
python start_autonomous.py

# Force stop everything
python stop_autonomous.py
```

### 🛠 **Manual / Individual Launch (Debugging)**
Use these commands to run specific components if you need to see real-time logs in your active terminal.

| Component | Command | Description |
| :--- | :--- | :--- |
| **Backend API** | `python src/api/chat_api.py` | FastAPI server on port 8000 | Backend Status: http://localhost:8000/api/status
| **Frontend UI** | `cd frontend && npm run dev` | Next.js 15 on port 3000 |
http://localhost:3000/dashboard (Admin Login) ODOO="http://localhost:8069"
| **Watchers** | `python watchers.py` | Starts the "Senses" (Gmail/WA monitoring) |
| **Brain Agent** | `python agents/brain_agent.py` | Starts the "Reasoning" (Task processing) |
| **WhatsApp Auth** | `python tests/verify_whatsapp.py` | Scan QR code for the first time |
| **Odoo Sync** | `python mcp/odoo_server.py` | Manual test for Odoo bridge |

---

## 🏗️ 2. System Architecture
The AI Employee follows a **Local-First, Watcher-Brain-Vault** architecture.

### 🔄 The "Digital FTE" Loop
1. **Watchers (Senses)**: Monitor Gmail and WhatsApp. When a "Panaverse" keyword or lead is found, they write a `.md` file to `data/vault/Needs_Action/`.
2. **Vault (Memory)**: A folder-based persistent system.
    - `/Needs_Action`: The inbox for the AI.
    - `/Plans`: AI-generated execution steps.
    - `/Done`: Completed task history.
3. **Brain (Reasoning)**: The `brain_agent.py` runs the "Ralph Wiggum Persistence Loop". It picks up tasks from the Vault, creates a plan, executes it using MCP tools (Odoo/Gmail), and moves the file to `/Done`.

### 📂 Directory Map
- `agents/`: Orchestration logic (Brain, Chat, Email).
- `skills/`: Core capabilities (Gmail, WhatsApp, Odoo, Search).
- `mcp/`: Server-side bridges for external tools.
- `frontend//app/dashboard/`: The modern Sales Command Center.
- `data/vault/`: Local markdown memory.

---

## 🔑 3. Configuration (.env)
Your `.env` file must be in the root directory. Key requirements:

```ini
# Core AI
GOOGLE_API_KEY="AIzaSy..."  # Default: Gemini 2.5 Flash

# Odoo CRM
ODOO_URL="http://localhost:8069"
ODOO_DB="panaverse_crm"
ODOO_USER="admin***"
ODOO_PASS="password***"

# Gmail
GMAIL_CREDENTIALS_PATH="credentials.json"
GMAIL_TOKEN_PATH="token.json"

# WhatsApp
WHATSAPP_ENABLED=true
ADMIN_WHATSAPP="+923244279017" # Notification target

# Admin Login
ADMIN_EMAIL="kh*********@mail.com"
ADMIN_PASS="A********@123"
```

---

## 🛠️ 4. Troubleshooting

### ❌ Port 8000/3000 in Use
If the system fails to start due to port conflicts:
```powershell
# Kill all Python/Node processes hanging in background
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
```

### ❌ WhatsApp Not Ready
If WhatsApp fails to send:
1. Delete the `whatsapp_session/` folder.
2. Run `python tests/verify_whatsapp.py`.
3. Scan the QR code precisely.

### ❌ Odoo Connection Failure
Verify Odoo is running locally or your Docker instance is up. Check `xmlrpc.client` is working in Python.

---

## 🧪 5. Testing & Verification
Before updates, run the comprehensive verification suite:
```powershell
python tests/verify_system.py
```
This verifies **Read**, **Write**, and **Filter** capabilities for all major agents.

---
*Maintained by Team AI Force - Platinum Tier Hackathon Project (2026)*
