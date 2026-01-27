# Panaversity Student Assistant - Developer Guide 📘

## ⚡ Quick Commands (Copy-Paste Ready)

### Start Everything (Windows)
```powershell
# Option 1: Double-click start.bat
# Option 2: Use management menu
python manage.py
```

### Start Components Manually
```powershell
# Terminal 1: Backend API (port 8000)
$env:PYTHONPATH='.'; python src/api/chat_api.py

# Terminal 2: Frontend UI (port 3000)
cd frontend && npm run dev

# Terminal 3: Watchers (monitors Email/WhatsApp)
python watchers.py

# Terminal 4: Brain (processes tasks)
python brain_agent.py
```

### Stop / Restart Backend
```powershell
# Stop ALL Python processes (backend, watchers, brain)
taskkill /F /IM python.exe

# Restart Backend only
taskkill /F /IM python.exe; $env:PYTHONPATH='.'; python src/api/chat_api.py

# Stop Frontend (Ctrl+C in terminal, or)
taskkill /F /IM node.exe
```

### Troubleshooting Commands
```powershell
# Kill stuck Python processes
taskkill /F /IM python.exe

# Check what's using port 8000
netstat -ano | findstr :8000

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reset WhatsApp session (if login fails)
Remove-Item -Recurse -Force .wa_session
```

---

## 🌟 Project Overview
The **Panaversity Student Assistant** is an Autonomous AI Agent (Digital FTE) using the **Platinum Tier** architecture: Watchers → Vault → Brain.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PANAVERSITY ASSISTANT                        │
├─────────────────────────────────────────────────────────────────┤
│  WATCHERS (Sensors)    →    VAULT (Memory)    →    BRAIN (Exec) │
│  Gmail, WhatsApp,          /Needs_Action/          MainAgent    │
│  LinkedIn                  /Plans/                 ChatAgent    │
│                           /Done/                   OdooAgent    │
└─────────────────────────────────────────────────────────────────┘
```

### The Vault (`data/vault/`)
| Folder | Purpose |
|--------|---------|
| `Inbox/` | Raw incoming data |
| `Needs_Action/` | Tasks waiting for Brain |
| `Plans/` | Agent-generated plans |
| `Pending_Approval/` | HITL approval queue |
| `Approved/` | Human-approved actions |
| `Done/` | Completed tasks archive |
| `Logs/` | JSON audit logs |

### The Watchers (`watchers.py`)
Monitors Gmail, WhatsApp, LinkedIn. Creates `.md` files in `/Needs_Action` when relevant events occur.

### The Brain (`brain_agent.py`)
Processes `/Needs_Action` files, executes via agents, moves to `/Done`. Implements Ralph Wiggum loop (keep processing until complete).

---

## 📂 Project Structure

```
hackathon_panaverse/
├── data/vault/         # Agent memory (Markdown files)
├── frontend/           # Next.js UI
├── skills/             # 9 modular capabilities
│   ├── chatbot_skill/  # Gemini LLM
│   ├── gmail_monitoring/
│   ├── whatsapp_skill/
│   ├── linkedin_skill/
│   ├── odoo_skill/     # CRM integration
│   └── web_search_skill/
├── src/agents/         # Agent logic
├── src/api/            # FastAPI backend
├── brain_agent.py      # Task processor
├── watchers.py         # Monitors
└── manage.py           # CLI menu
```

---

## 🛠️ Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- Gmail App Password
- Odoo Account

### Installation
```powershell
pip install -r requirements.txt
playwright install chromium
cd frontend && npm install && cd ..
```

### Configuration
See `INSTRUCTIONS.md` for credential setup.

---

## ☁️ Cloud Deployment (Oracle Free Tier)

```bash
# On Ubuntu VM
pip install -r requirements.txt
playwright install-deps && playwright install chromium

# Keep running with PM2
npm install -g pm2
pm2 start src/api/chat_api.py --interpreter python3
pm2 start watchers.py --interpreter python3
pm2 start brain_agent.py --interpreter python3
pm2 save && pm2 startup
```

---

*For credentials and user guide, see `INSTRUCTIONS.md`*
