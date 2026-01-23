# Panaversity Student Assistant - Credentials Setup

## Required Credentials

You need to provide the following credentials to run the assistant:

### 1. Gmail API Credentials (`credentials.json`)

**How to get:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select project "Panaversity Assistant"
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json`
6. Place in project root: `D:\Panavers\Projects\hackathon_khansarwar\credentials.json`

**Template:** See `credentials.json.example`

### 2. Gmail App Password (for SMTP)

**How to get:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate password for "Mail" on "Windows Computer"
5. Copy 16-character password (remove spaces)
6. Add to `.env` file as `SMTP_PASSWORD`

### 3. Environment Variables (`.env`)

**Required:**
```env
# Gmail Configuration
GMAIL_ADDRESS=exellencelinks@gmail.com

# Admin Notifications
ADMIN_EMAIL=khansarwar1@hotmail.com

# SMTP Configuration
SMTP_USERNAME=exellencelinks@gmail.com
SMTP_PASSWORD=your_16_char_app_password_here
```

**Optional (for future phases):**
```env
# GitHub (Phase 3)
GITHUB_TOKEN=your_github_token

# OpenAI (Phase 4)
OPENAI_API_KEY=your_openai_key

# Google AI (Phase 4)
GOOGLE_API_KEY=your_google_api_key
```

## Setup Checklist

- [ ] Download `credentials.json` from Google Cloud Console
- [ ] Place `credentials.json` in project root
- [ ] Generate Gmail app password
- [ ] Copy `.env.example` to `.env`
- [ ] Add SMTP password to `.env`
- [ ] Run first authentication: `python src/main.py check`
- [ ] Verify `token.json` is created

## Security Notes

⚠️ **Never commit these files to Git:**
- `credentials.json` - OAuth credentials
- `token.json` - Authentication token
- `.env` - Environment variables with passwords

✅ **These are already in `.gitignore`**

## Troubleshooting

**"credentials.json not found"**
- Download from Google Cloud Console
- Ensure it's named exactly `credentials.json`
- Place in project root (not in subdirectories)

**"SMTP authentication failed"**
- Use app password, not regular Gmail password
- Ensure 2-Step Verification is enabled
- Remove spaces from 16-character password

**"Gmail API not enabled"**
- Go to Google Cloud Console
- APIs & Services → Library
- Search "Gmail API" → Enable

## When You Have Credentials

1. Place `credentials.json` in project root
2. Update `.env` with SMTP password
3. Run: `python src/main.py check`
4. Browser will open for authentication
5. Sign in and grant permissions
6. `token.json` will be created automatically
7. You're ready to go! 🎉
