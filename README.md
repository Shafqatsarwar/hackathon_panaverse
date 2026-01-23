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
│   ├── gmail_monitoring/      # Gmail API integration
│   ├── email_filtering/       # Email categorization
│   └── email_notifications/   # SMTP notifications
├── src/agents/                # Agents that use skills
│   ├── email_agent.py         # Monitors Gmail
│   ├── notification_agent.py  # Sends notifications
│   └── main_agent.py          # Orchestrates everything
├── tasks/                     # Task definitions
│   └── email_monitoring.json  # Email monitoring task
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

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Credentials
See [CREDENTIALS.md](CREDENTIALS.md) for detailed instructions.

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your SMTP password
```

### 4. Run
```bash
# Manual check
python src/main.py check

# Background mode
python src/main.py start
```

## Commands

| Command | Description |
|---------|-------------|
| `python src/main.py check` | Manual email check |
| `python src/main.py start` | Background mode (15 min intervals) |
| `python src/main.py config` | Show configuration |
| `python src/main.py status` | Show agent status |

Or use batch files:
- `check.bat` - Quick email check
- `start.bat` - Start background mode

## How It Works

### Skills Layer
1. **gmail_monitoring**: Connects to Gmail API, fetches emails
2. **email_filtering**: Filters by keywords, detects priority
3. **email_notifications**: Sends formatted HTML emails

### Agents Layer
1. **EmailAgent**: Uses `gmail_monitoring` + `email_filtering` skills
2. **NotificationAgent**: Uses `email_notifications` skill
3. **MainAgent**: Coordinates EmailAgent + NotificationAgent

### Tasks Layer
1. **email_monitoring**: Defined in `tasks/email_monitoring.json`
   - Runs every 15 minutes
   - Uses EmailAgent + NotificationAgent
   - Logs to `chat_history/`

### Chat History
- Daily JSON logs: `chat_history/YYYY-MM-DD.json`
- Tracks all email checks and notifications
- Queryable for analytics

## Configuration

Edit `.env`:
```env
# Required
GMAIL_ADDRESS=exellencelinks@gmail.com
ADMIN_EMAIL=khansarwar1@hotmail.com
SMTP_PASSWORD=your_app_password_here

# Optional
EMAIL_CHECK_INTERVAL=15
FILTER_KEYWORDS=Panaversity,PIAIC,Quiz,Assignment
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[CREDENTIALS.md](CREDENTIALS.md)** - How to get API credentials
- **[TESTING.md](TESTING.md)** - Test scenarios
- **[skills/README.md](skills/README.md)** - Skills documentation
- **[tasks/README.md](tasks/README.md)** - Tasks documentation

## Example Usage

### Check Chat History
```bash
# View today's activity
cat chat_history/2026-01-23.json
```

### Customize Keywords
Edit `.env`:
```env
FILTER_KEYWORDS=Panversity,PIAIC,Quiz,Exam,Assignment,Deadline,Meeting
```

### Change Check Interval
Edit `.env`:
```env
EMAIL_CHECK_INTERVAL=10  # Check every 10 minutes
```

## Future Phases

- 🚧 **Phase 2**: WhatsApp integration
- 🚧 **Phase 3**: LinkedIn + GitHub monitoring
- 🚧 **Phase 4**: AI-powered summarization

## Support

📧 khansarwar1@hotmail.com
