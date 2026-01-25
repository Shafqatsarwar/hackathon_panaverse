# Panaversity Student Assistant - Developer Guide 📘

> **A Multi-Agent AI System for Student Success**  
> Powered by Google Gemini 2.5, Odoo ERP, and Next.js 14.

---
### Run backend:
python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000

###Run frontend:
cd frontend
npm run dev

## 📚 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture & Agents](#2-architecture--agents)
3. [Project Structure](#3-project-structure)
4. [Setup & Credentials](#4-setup--credentials)
5. [Running the Project](#5-running-the-project)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Project Overview
This tool acts as a **autonomous 24/7 personal assistant** for students and staff. It unifies communication channels (Email, WhatsApp) with business data (Odoo CRM) through a single AI interface.

**Core Capabilities:**
- **🧠 Intelligent Chat**: Uses Google Gemini to understand natural language requests.
- **📧 Email Autopilot**: Monitors Gmail for keywords ("Deadline", "Exam"), categorizes them, and notifies the user.
- **📊 Odoo Integration**: Automatically creates Leads in Odoo CRM from important emails or chat commands.
- **💬 WhatsApp Bridge**: Sends alerts to your phone and lets you check messages from the web UI.

---

## 2. Architecture & Agents
The system is built on a **Multi-Agent Architecture**:

### 🤖 Main Agent (`src/agents/main_agent.py`)
The "Brain" that orchestrates background tasks. It runs on a schedule (e.g., every 15 mins) to check emails and sync data.

### 💬 Chat Agent (`src/agents/chat_agent.py`)
Handles real-time user interaction via the Web UI. It has access to **Tools**:
- `_check_email_tool`: Reads unread emails.
- `_check_whatsapp_tool`: Scrapes WhatsApp Web for messages.
- `web_search`: Uses DuckDuckGo to answer general questions.

### 📧 Email Agent (`src/agents/email_agent.py`)
Connects to Gmail via IMAP/SMTP. Handles authentication and parsing.

### 💼 Odoo Agent (`src/agents/odoo_agent.py`)
Uses XML-RPC to talk to your Odoo instance. Can Read/Write Leads and Opportunities.

---

## 3. Project Structure
Understanding the codebase folder by folder:

```bash
hackathon_panaverse/
├── src/                    # BACKEND (Python) 🐍
│   ├── agents/             # The logic for each agent (Chat, Email, Odoo)
│   ├── api/                # FastAPI Server (Routes, Websockets)
│   ├── utils/              # Config, Logging, Helper functions
│   └── main.py             # Background Process Entry Point
│
├── frontend/               # FRONTEND (Next.js/React) ⚛️
│   ├── app/                # Page Logic (page.tsx) and Global Styles
│   ├── public/             # Static Assets (Images, Icons)
│   └── ...config files     # Tailwind, Next.js config
│
├── skills/                 # REUSABLE SKILLS 🛠️
│   ├── whatsapp_skill/     # Browser Automation for WhatsApp
│   ├── chatbot_skill/      # Gemini SDK integration
│   └── web_search_skill/   # Search Engine integration
│
├── start.bat               # ⚡ ONE-CLICK RELEASE LAUNCHER
├── manage.py               # 🛠️ DEVELOPER CLI TOOL
└── INSTRUCTIONS.md         # 🔐 KEY SETUP & USAGE GUIDE
```

---

## 4. Setup & Credentials
Before running the code, you **must configure your credentials**.
Please see the dedicated guide (it includes detailed steps for Gmail, Odoo, etc.):

👉 **[READ: INSTRUCTIONS.md](INSTRUCTIONS.md)**

---

## 5. Running the Project
We provide 3 ways to run the application. See **[INSTRUCTIONS.md](INSTRUCTIONS.md)** for the quick-start guide.

**For Developers (Recommended Flow):**
1.  Open `run_local_dev.bat` or use `python manage.py` (Option 1).
2.  Edit code in `src/` or `frontend/`.
3.  The servers (FastAPI and Next.js) will **auto-reload** upon saving changes.

---

## 6. Troubleshooting
- **"Hydration Error"**: Usually a mismatch between server/client HTML. Check `frontend/app/layout.tsx`.
- **"WhatsApp Login Failed"**: You need to scan the QR code. Check the *Terminal Window* running the backend.
- **"Odoo Access Denied"**: Verify your `ODOO_DB` and `ODOO_PASSWORD` in `.env`.

---
*Created for the Agents v3.0 Hackathon.*
