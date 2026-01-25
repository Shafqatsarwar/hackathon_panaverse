# Panaversity Student Assistant 🎓

A practical AI-powered assistant for Panaversity students using **Skills → Agents → Tasks** architecture.

## Architecture

```
Skills (Reusable capabilities)
  ↓
Agents (Use skills to perform actions)
  ↓
Tasks (Coordinate agents to achieve goals)
  ↓
Chat History (Log all activities)
```

## Project Structure

```
D:\Panavers\Projects\hackathon_khansarwar\
├── skills/                    # Reusable skills
├── src/agents/                # Agents that use skills
├── tasks/                     # Task definitions
├── chat_history/              # Daily activity logs (JSON)
├── requirements.txt           # Dependencies
├── .env.example               # Config template
└── README.md                  # This file
```

## Features

✅ **Email Monitoring** (Phase 1)
- Gmail API integration via `gmail_monitoring` skill
- Keyword filtering via `email_filtering` skill
- SMTP notifications via `email_notifications` skill
- Priority detection (High/Medium/Low)
- Quiz and deadline alerts

✅ **UI/UX Modernization** (Phase 2)
- **Glassmorphism Design** for a modern look
- **Sticky Chat Widget** (`ChatWidget.tsx`) for seamless access
- Minimized layout impact

✅ **Chatbot Intelligence** (Phase 3)
- **Google Gemini** Integration
- **Web Search** (DuckDuckGo) for general knowledge
- **Email Tools** (Check inbox from chat)

✅ **Integrations** (Phase 4-6)
- **WhatsApp**: Robust login & message sending (Playwright)
- **Odoo CRM**: Create/View Leads directly from chat (XML-RPC)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Credentials
See [INSTRUCTIONS.md](INSTRUCTIONS.md) for detailed instructions (API Keys, Odoo, WhatsApp).

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your secrets
```

### 4. Run
```bash
# Start Backend
python src/main.py start

# Start Frontend (in separate terminal)
cd frontend
npm run dev
```

## How It Works

### Skills Layer
- **gmail_monitoring**: Connects to Gmail API
- **whatsapp_skill**: Automates WhatsApp Web
- **odoo_skill**: Connects to Odoo CRM
- **web_search**: Uses DuckDuckGo

### Agents Layer
- **MainAgent**: Orchestrates background tasks
- **ChatAgent**: Handles user interactions + Tools

## Configuration

Edit `.env` to set your keys for Gemini, Gmail, Odoo, and WhatsApp.

## Documentation

- **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Setup & Secrets
- **[skills/README.md](skills/README.md)** - Skills documentation

## Future Phases

- ✅ **Phase 1-6**: Core Features (Email, Chat, WhatsApp, Odoo) implemented.
- 🚧 **Phase 7**: Advanced Orchestration (In Progress)
- 🚧 **Phase 8-9**: Final Deployment & Polish

## Support

📧 khansarwar1@hotmail.com
