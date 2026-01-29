# Panaversity Student Assistant - Comprehensive Developer Guide 📘

Welcome to the **Panaversity Student Assistant** development guide. This document provides everything you need to run, maintain, and extend the system.

## 📱 WhatsApp Integration - FIXED & READY
WhatsApp has been completely overhauled and is now **100% functional**. See:
- **Quick Start**: [`WHATSAPP_QUICKSTART.md`](WHATSAPP_QUICKSTART.md) - 3-step setup
- **Complete Fix**: [`WHATSAPP_FIX_SUMMARY.md`](WHATSAPP_FIX_SUMMARY.md) - All changes
- **Technical Deep Dive**: [`WHATSAPP_DEEP_DIVE_ANALYSIS.md`](WHATSAPP_DEEP_DIVE_ANALYSIS.md) - Root cause analysis

---

## ⚡ 1. Quick Start Commands (Top Priority)

### 🎯 Easiest Way - Double Click Batch Files
1. **Start Everything**: Double-click `start.bat` in the root folder
2. **Stop Everything**: Double-click `stop.bat` in the root folder

That's it! The batch files will:
- Start Backend API on port 8000
- Start Frontend UI on port 3000
- Open in separate windows so you can see the logs

### 📝 Simple Terminal Commands (If you prefer typing)

**Option 1 - Two separate terminals:**
```powershell
# Terminal 1: Start Backend
cd d:\Panavers\Projects\hackathon_panaverse
python src/api/chat_api.py

# Terminal 2: Start Frontend
cd d:\Panavers\Projects\hackathon_panaverse
cd frontend; npm run dev

```

**Option 2 - Stop everything:**
```powershell
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### 🔧 Advanced - Run Individual Components
```powershell
# Backend API only
python src/api/chat_api.py
# check status running
http://localhost:8000/api/status

# Troubleshooting
# Kill the old backend
taskkill /F /IM python.exe

# Wait 2 seconds
timeout /t 2

# ReStart new backend
python src/api/chat_api.py

# Frontend only
cd frontend
npm run dev

# Watchers (monitors Gmail/WhatsApp)
python watchers.py

# Brain Agent (processes tasks)
python brain_agent.py

# WhatsApp - First Time Setup (Scan QR Code)
python tests/verify_whatsapp.py

# WhatsApp - Send Test Message
python tests/test_wa_send.py
```

---

## 🏗️ 2. System Architecture (The Platinum Tier)

The system is built on the **Watcher → Vault → Brain** architecture, designed for 24/7 autonomous operations.

### 🔄 The Data Flow
1. **WATCHERS**: `watchers.py` monitors Gmail, WhatsApp, and LinkedIn. When a relevant update (Quiz, Assignment, Deadline) is found, it creates a `.md` file in `data/vault/Needs_Action/`.
2. **VAULT**: A folder-based persistent memory system.
   - `Needs_Action/`: Input queue for the AI.
   - `Plans/`: AI-generated step-by-step execution plans.
   - `Done/`: Historical archive of completed tasks.
3. **BRAIN**: `brain_agent.py` processes the vault using the `MainAgent`. It picks a task, uses specialized **Skills** to execute it, and moves the task to `Done`.

### 📂 Directory Structure
```text
├── data/vault/             # Persistent Task Memory (Markdown)
├── frontend/               # Next.js 15 App (Modern Glassmorphism UI)
├── logs/                   # System and activity logs
├── scripts/                # Utility and database seeding scripts
├── skills/                 # Modular AI Capabilities
│   ├── chatbot_skill/      # Gemini 2.5 Flash / Gemini 3.0 Fallback
│   ├── gmail_monitoring/   # OAuth2 Gmail Scanner
│   ├── odoo_skill/         # CRM & Lead Management integration
│   ├── whatsapp_skill/     # Playwright-based browser automation
│   ├── linkedin_skill/     # Pulse/Notice monitoring
│   └── web_search_skill/   # DuckDuckGo integration
├── src/
│   ├── agents/             # Logic for Main, Chat, and Sub-Agents
│   ├── api/                # FastAPI Endpoints & WebSockets
│   └── utils/              # Config, Logger, and Shared Helpers
├── tests/                  # Verification and unit tests
├── start.all               # Full System Launcher
├── stop.all                # Graceful System Stopper
├── watchers.py             # Background sensors (Emails/Socials)
└── brain_agent.py          # The core task execution engine
```

---

## 🛠️ 3. Troubleshooting & Fixes

### Port Conflicts
If you see `[WinError 10013]` or `Port already in use`:
```powershell
# Kill processes using the ports
taskkill /F /IM python.exe
taskkill /F /IM node.exe
# Or find specific PID
netstat -ano | findstr :8000
```

### AI Rate Limits (429 Errors)
The system  - We have migrated to `gemini-2.5-flash` as the primary model.
  - **Default**: `gemini-2.5-flash`
  - **Fallback**: `gemini-3.0-flash`u hit limits:
- Wait 60 seconds (Free tier usually resets per minute).
- Check `skills/chatbot_skill/skill.py` to ensure your model names match the latest available in your region.

### Environment & Dependencies
```powershell
# Refresh dependencies
pip install -r requirements.txt --upgrade
playwright install chromium

# Reset WhatsApp login
Remove-Item -Recurse -Force whatsapp_session
```

### WhatsApp Setup & Troubleshooting

#### Initial Setup
1. **Enable WhatsApp** in `.env`:
   ```bash
   WHATSAPP_ENABLED=true
   ADMIN_WHATSAPP=+923244279017  # Your number with country code
   ```

2. **Install Playwright Browser**:
   ```powershell
   playwright install chromium
   ```

3. **First Login** (QR Code Scan):
   ```powershell
   # Run this to open WhatsApp Web and scan QR code
   python tests/verify_whatsapp.py
   ```
   - Browser will open to WhatsApp Web
   - Scan QR code with your phone
   - Session saves to `./whatsapp_session` folder
   - You only need to do this ONCE

4. **Test Sending**:
   ```powershell
   # Send a test message
   python tests/test_wa_send.py
   ```

#### Common WhatsApp Issues

**Issue 1: "NotImplementedError" or Event Loop Errors**
- **Cause**: Windows event loop conflicts
- **Fix**: Already handled in skill.py v2.1
- **Verify**: Check you're using the latest skill version

**Issue 2: "Login timeout" or QR Code Not Scanning**
- **Cause**: Session expired or browser automation blocked
- **Fix**:
  ```powershell
  # Delete session and re-scan
  Remove-Item -Recurse -Force whatsapp_session
  python tests/verify_whatsapp.py
  ```

**Issue 3: "WhatsApp integration is disabled"**
- **Cause**: `WHATSAPP_ENABLED=false` in .env
- **Fix**: Set `WHATSAPP_ENABLED=true` in `.env` file

**Issue 4: Messages Not Sending**
- **Cause**: Invalid phone number format
- **Fix**: Use format `+923001234567` (country code + number, no spaces)

**Issue 5: Watcher Not Finding Messages**
- **Cause**: Keywords don't match or archived chats
- **Fix**: 
  - Check `FILTER_KEYWORDS` in `.env`
  - Watcher checks both main and archived chats
  - Verify messages contain your keywords

#### WhatsApp Architecture

```
┌─────────────────────────────────────────────┐
│  Entry Points (Choose One)                  │
├─────────────────────────────────────────────┤
│  1. Direct Skill:                           │
│     from skills.whatsapp_skill.skill import │
│     skill = WhatsAppSkill()                 │
│                                             │
│  2. MCP Server (Recommended):               │
│     whatsapp_server.call_tool()             │
│                                             │
│  3. Agent Wrapper:                          │
│     whatsapp_agent.send_alert()             │
│                                             │
│  4. Watcher (Automatic):                    │
│     Polls every 60 minutes                  │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│  WhatsAppSkill (Core Implementation)        │
│  - Playwright browser automation            │
│  - Session persistence                      │
│  - Windows event loop handling              │
│  - Send & check messages                    │
└─────────────────────────────────────────────┘
```

#### Testing WhatsApp Integration

```powershell
# Test 1: Verify login session
python tests/verify_whatsapp.py

# Test 2: Send a message
python tests/test_wa_send.py

# Test 3: Check for messages
python tests/test_whatsapp.py

# Test 4: Full skill test suite
python tests/test_skills.py
```

---

## 🚀 4. Adding New Features

### How to Add a New Skill
1. Create a folder in `skills/your_skill_name/`.
2. Implement a class that performs the specific task.
3. Add the skill to `src/agents/main_agent.py` so the Brain can use it.

### How to Add a New Watcher
1. Open `watchers.py`.
2. Add a new async function that polls your source (e.g., a new CRM or API).
3. Ensure it writes a formatted `.md` file to `data/vault/Needs_Action/`.

---

## 🧪 5. Testing & Verification
Always run tests before pushing changes:
```powershell
# Run the Comprehensive Skill Test
python test_skills.py
```
This verifies your API keys, Odoo authentication, and model responses in one go.

---
*Guide maintained by Antigravity AI - Last updated Jan 27, 2026*
