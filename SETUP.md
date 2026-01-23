# Panaversity Student Assistant - Setup Guide

## Prerequisites

- Python 3.10 or higher
- Gmail account (exellencelinks@gmail.com)
- Google Cloud Console access

## Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
cd D:\Panavers\Projects\hackathon_khansarwar
pip install -r requirements.txt
```

### Step 2: Set Up Gmail API Credentials

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com/

2. **Create/Select Project**:
   - Click "Select a project" → "New Project"
   - Name: "Panaversity Assistant"
   - Click "Create"

3. **Enable Gmail API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Panaversity Assistant Desktop"
   - Click "Create"

5. **Download Credentials**:
   - Click the download icon next to your OAuth client
   - Save as `credentials.json` in project root: `D:\Panavers\Projects\hackathon_khansarwar\credentials.json`

### Step 3: Get Gmail App Password (for sending notifications)

1. **Enable 2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Find "2-Step Verification" and enable it

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password (remove spaces)

### Step 4: Configure Environment Variables

1. **Copy example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** and update these values:
   ```env
   # Gmail Configuration
   GMAIL_ADDRESS=exellencelinks@gmail.com
   
   # Admin Notifications
   ADMIN_EMAIL=khansarwar1@hotmail.com
   ADMIN_WHATSAPP=+923244279017
   
   # SMTP Configuration (paste the app password from Step 3)
   SMTP_USERNAME=exellencelinks@gmail.com
   SMTP_PASSWORD=your_16_char_app_password_here
   
   # Optional: Add your API keys if you have them
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_API_KEY=AIzaSyBHUooUJ2D0ALNx_oVPPYdPO9XCxn5hrMw
   ```

### Step 5: First Run (Authentication)

Run the assistant for the first time to authenticate with Gmail:

```bash
python src/main.py check
```

**What happens:**
1. A browser window will open
2. Sign in with `exellencelinks@gmail.com`
3. Grant permissions to the app
4. Browser will show "The authentication flow has completed"
5. A `token.json` file will be created (stores your auth token)

### Step 6: Test Email Monitoring

1. **Send a test email** to `exellencelinks@gmail.com`:
   - Subject: "PIAIC Quiz Tomorrow"
   - Body: "Don't forget the quiz!"

2. **Run manual check**:
   ```bash
   python src/main.py check
   ```

3. **Check admin email** (`khansarwar1@hotmail.com`):
   - You should receive a notification with the email summary

### Step 7: Start Background Mode

Once testing is successful, start the assistant in background mode:

```bash
python src/main.py start
```

**This will:**
- Check emails every 15 minutes
- Send notifications automatically
- Log all activity to `panaversity_assistant.log`
- Run until you press Ctrl+C

## Verification Checklist

- [ ] Python dependencies installed
- [ ] `credentials.json` downloaded from Google Cloud Console
- [ ] Gmail API enabled in Google Cloud Console
- [ ] `.env` file created and configured
- [ ] Gmail app password generated and added to `.env`
- [ ] First run authentication completed (`token.json` created)
- [ ] Test email sent and notification received
- [ ] Background mode started successfully

## Common Issues

### Issue: "credentials.json not found"
**Solution**: Download OAuth credentials from Google Cloud Console and save as `credentials.json` in project root.

### Issue: "SMTP authentication failed"
**Solution**: 
- Use Gmail app password, not your regular password
- Ensure 2-Step Verification is enabled
- Remove spaces from the 16-character app password

### Issue: "Gmail API not enabled"
**Solution**: Go to Google Cloud Console → APIs & Services → Library → Enable Gmail API

### Issue: "No emails detected"
**Solution**:
- Ensure test email is unread
- Check keywords match (Panaversity, PIAIC, Quiz, etc.)
- Review logs: `panaversity_assistant.log`

## File Structure After Setup

```
D:\Panavers\Projects\hackathon_khansarwar\
├── credentials.json          # ✓ Downloaded from Google Cloud
├── token.json               # ✓ Created after first authentication
├── .env                     # ✓ Created from .env.example
├── .env.example             # Template
├── requirements.txt         # Dependencies
├── README.md               # Main documentation
├── SETUP.md                # This file
├── panaversity_assistant.log  # Created when running
└── src/                    # Source code
```

## Next Steps

After successful setup:

1. **Customize keywords**: Edit `FILTER_KEYWORDS` in `.env`
2. **Adjust check interval**: Edit `EMAIL_CHECK_INTERVAL` in `.env`
3. **Review logs**: Monitor `panaversity_assistant.log`
4. **Add WhatsApp**: (Phase 2 - coming soon)
5. **Add LinkedIn**: (Phase 3 - coming soon)

## Support

If you encounter issues:
1. Check logs: `panaversity_assistant.log`
2. Review this setup guide
3. Contact: khansarwar1@hotmail.com
