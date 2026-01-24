# Panaversity Student Assistant - Complete Guide

## 1. Project Overview
A multi-agent AI assistant designed for Panaversity students. It integrates email monitoring, WhatsApp alerts, LinkedIn automation, and Odoo ERP synchonization into a unified chat interface.

**Key Features:**
-   **Chatbot**: Powered by Google Gemini (2.5-Flash), capable of answering student queries and reading Odoo leads.
-   **Smart Email Agent**: Monitors Gmail, filters for "Exams/Deadlines", and creates Odoo Leads automatically.
-   **Odoo Integration**: Syncs important emails to your Odoo CRM as Leads.
-   **WhatsApp & LinkedIn**: Automated alerts for critical updates.

## 2. Project Structure
```
hackathon_panaverse/
├── src/
│   ├── agents/           # AI Agents (Chat, Email, Odoo, WhatsApp, etc.)
│   ├── api/              # FastAPI Backend Server (chat_api.py)
│   ├── utils/            # Helper functions and Config
│   └── main.py           # Background Worker Entry Point
├── skills/               # Reusable Skills (gemini, odoo_xmlrpc, etc.)
├── frontend/             # Next.js 14 Modern UI
├── tests/                # Verification Scripts
├── start_demo.bat        # ONE-CLICK LAUNCHER (Windows)
├── GUIDE.md              # This file
└── INSTRUCTIONS.md       # API Key Setup Guide
```

## 3. How to Run (Local Host)

### Option A: The "One-Click" Method (Recommended)
Simply double-click the **`start_demo.bat`** file in the root directory.
It will open two windows:
1.  Backend (FastAPI)
2.  Frontend (Next.js)

### Option B: Manual Command Line
Open **Two Terminal Windows**:

**Terminal 1: Backend API**
```bash
python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2: Background Worker (Email/Odoo Sync)**
*Optional: Only needed if you want emails to sync in real-time.*
```bash
python -m src.main start
```

**Terminal 3: Frontend**
```bash
cd frontend
npm run dev
```

**Access the App:**
Open your browser to: **[http://localhost:3000](http://localhost:3000)**

## 4. Deployment
Since this is a Hackathon project using local automation (Selenium/Playwright for WhatsApp), **Local Deployment is recommended**. Cloud deployment (Vercel) was skipped to preserve these local automation features.

To showcase this project:
1.  Record a video of the local functionality.
2.  Push to GitHub (Secrets are safe, see `.gitignore`).
3.  Present from Localhost.
