# 🚀 Quick Start - Panaversity Student Assistant

## Prerequisites
- ✅ Python 3.10+ installed
- ✅ Dependencies installed: `pip install -r requirements.txt`

## Setup (5 minutes)

### 1. Get Gmail API Credentials
1. Visit: https://console.cloud.google.com/
2. Create project → Enable Gmail API → Create OAuth credentials
3. Download as `credentials.json` → Place in project root

### 2. Get Gmail App Password
1. Visit: https://myaccount.google.com/apppasswords
2. Generate password for "Mail"
3. Copy 16-character password

### 3. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env and add:
SMTP_PASSWORD=your_16_char_password_here
```

### 4. First Run
```bash
# This will open browser for Gmail authentication
python src/main.py check
```

## Usage

### Manual Check
```bash
python src/main.py check
```
or double-click `check.bat`

### Background Mode (Auto-check every 15 min)
```bash
python src/main.py start
```
or double-click `start.bat`

### Show Config
```bash
python src/main.py config
```

## Test It

1. Send email to `exellencelinks@gmail.com`:
   - Subject: "PIAIC Quiz Tomorrow"
   
2. Run: `python src/main.py check`

3. Check `khansarwar1@hotmail.com` for notification

## Files You Need

| File | Status | Action |
|------|--------|--------|
| `credentials.json` | ❌ You provide | Download from Google Cloud |
| `.env` | ❌ You create | Copy from `.env.example` |
| `token.json` | ✅ Auto-created | Created on first run |

## Troubleshooting

**No credentials.json?**
→ See CREDENTIALS.md

**SMTP error?**
→ Use app password, not regular password

**No emails detected?**
→ Check email is unread and contains keywords

## What's Next?

- ✅ Phase 1: Email monitoring (DONE)
- 🚧 Phase 2: WhatsApp integration (Coming)
- 🚧 Phase 3: LinkedIn + GitHub (Coming)
- 🚧 Phase 4: AI enhancement (Coming)

## Support

📧 khansarwar1@hotmail.com
📚 See README.md for full documentation
