# Panaversity Student Assistant - Developer Guide 📘

## 🌟 Project Overview
The **Panaversity Student Assistant** is an Autonomous AI Agent designed to act as a *Personal AI Employee*. It uses a **File-System Based Architecture** (Platinum Tier) to manage tasks, monitor communications, and automate workflows across WhatsApp, Gmail, LinkedIn, and Odoo CRM.

---

## 🏗️ Architecture (The Platinum Tier)

The system works on a decoupled **Watcher -> Vault -> Brain** model, ensuring robustness and 24/7 reliability.

### 1. The Vault (`data/vault/`) 🗄️
The central memory functionality of the agent. It is a file-system based queue.
- **`Inbox/`**: Raw incoming data (logs, temp files).
- **`Needs_Action/`**: The "To-Do List". Watchers place Markdown files here.
- **`Done/`**: Archive of completed tasks.
- **`Company_Handbook.md`**: The rulebook defining how the Brain should react.

### 2. The Watchers (`watchers.py`) 👀
"The Senses" of the AI. These run continuously in the background.
- **Role**: Monitor external inputs (WhatsApp, Gmail, LinkedIn).
- **Action**: When a relevant event occurs (e.g., email with "Assignment"), it creates a standardized `.md` file in `Needs_Action/`.
- **Key Feature**: Zero logic overlap with the Brain. It only *observes* and *reports*.

### 3. The Brain (`brain_agent.py`) 🧠
"The Muscle" of the AI. It processes the Vault.
- **Role**: Watches the `Needs_Action/` folder for new files.
- **Action**: Reads the task, determines the necessary skill (e.g., Odoo Sync, Reply), executes it via `MainAgent`, and moves the file to `Done/`.
- **Loop**: The "Autonomous Loop" that ensures no task is ever dropped.

### 4. The API & Frontend 💻
- **Backend**: FastAPI (`src/api/chat_api.py`) providing endpoints/WebSockets.
- **Frontend**: Next.js (`frontend/`) providing a Glassmorphic UI for user interaction.

---

## 📂 Project Structure

```bash
Panaversity_Hackathon/
├── data/
│   └── vault/              # The "Memory" of the agent
├── frontend/               # Next.js User Interface
├── skills/                 # Modular Capabilities
│   ├── chatbot_skill/      # Gemini AI Wrapper
│   ├── email_filtering/    # Regex & NLP Filters
│   ├── gmail_monitoring/   # Gmail API logic
│   ├── linkedin_skill/     # Playwright Automation
│   ├── odoo_skill/         # XML-RPC CRM Integration
│   └── whatsapp_skill/     # WhatsApp Web Automation
├── src/
│   ├── agents/             # Logic Layers (Chat, Email, Odoo Agents)
│   ├── api/                # FastAPI Endpoints
│   └── mcp_servers/        # Model Context Protocol Servers
├── brain_agent.py          # The Autonomous Processor
├── watchers.py             # The Monitoring System
├── manage.py               # CLI Management Utility
└── start.bat               # Windows Quick Start Script
```

---

## 🛠️ Developer Setup Guide

### 1. Prerequisites
- **Python 3.10+**: Ensure it's in your PATH.
- **Node.js 18+**: For the frontend.
- **Odoo Account**: URL, DB Name, Username, Password.
- **Google API Key**: For Gemini.
- **Gmail App Password**: For email access.

### 2. Installation
```powershell
# 1. Clone & Install Python Deps
git clone <repo_url>
cd hackathon_panaverse
pip install -r requirements.txt
playwright install chromium

# 2. Install Frontend Deps
cd frontend
npm install
cd ..
```

### 3. Configuration (`.env`)
Refer to `INSTRUCTIONS.md` for the exact variables required.

---

## 🚀 Running the Project (Developer Mode)

### A. Full System (Recommended)
Use the management script to see all options:
```powershell
python manage.py
```
*Select "Run Full System" to start Backend, Frontend, and Autonomous Agents.*

### B. Manual Component Start
If you crave control, run each component in a separate terminal:

**Terminal 1: The API (Backend)**
```powershell
# Serves the Chatbot & API at http://localhost:8000
$env:PYTHONPATH='.'; python src/api/chat_api.py
```

**Terminal 2: The Frontend (UI)**
```powershell
# Serves the UI at http://localhost:3000
cd frontend
npm run dev
```

**Terminal 3: The Watchers (Sensors)**
```powershell
# Monitors Email/WhatsApp and populates Vault
python watchers.py
```

**Terminal 4: The Brain (Processor)**
```powershell
# Processes Vault tasks autonomously
python brain_agent.py
```

---

## ☁️ Oracle Cloud Deployment Strategy
To deploy this as a true "AI Employee" on a VPS (like Oracle Free Tier):

1.  **Provision**: Ubuntu 22.04 VM (ARM/Ampere recommended).
2.  **Setup**:
    ```bash
    sudo apt update && sudo apt install python3-pip nodejs npm
    git clone <your_repo>
    pip install -r requirements.txt
    playwright install-deps
    playwright install chromium
    ```
3.  **Headless Mode**: Ensure `headless=True` is set in `skills/whatsapp_skill/skill.py` and other Playwright scripts.
4.  **Persistence**: Use `systemd` or `pm2` to keep scripts running.
    ```bash
    # Example PM2 usage
    pm2 start src/api/chat_api.py --name "backend" --interpreter python3
    pm2 start watchers.py --name "watchers" --interpreter python3
    pm2 start brain_agent.py --name "brain" --interpreter python3
    ```

---

## 🧪 Testing Tools
We provided scripts to test specific integrations in isolation:
- `verify_whatsapp.py`: Test WhatsApp Connection.
- `seed_linkedin.py`: Scrape LinkedIn & Feed Odoo.
- `check_email_script.py`: Debug Gmail Filter logic.
- `test_general_chat.py`: Verify Chatbot responses.

---

*For credential setup and 'how-to' users, please refer to* `INSTRUCTIONS.md`.
