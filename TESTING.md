# Quick Test Guide

## Before Running Tests

1. **Set up Gmail API credentials** (see SETUP.md for detailed instructions)
2. **Configure .env file** with your settings
3. **Install dependencies**: `pip install -r requirements.txt`

## Test 1: Configuration Check

```bash
python src/main.py config
```

**Expected output:**
- Shows your configuration settings
- Verifies environment variables are loaded

## Test 2: Manual Email Check (First Run)

```bash
python src/main.py check
```

**What happens:**
1. Browser opens for Gmail authentication
2. Sign in with exellencelinks@gmail.com
3. Grant permissions
4. Assistant checks for emails
5. Sends notifications if relevant emails found

## Test 3: Send Test Email

1. Send email to `exellencelinks@gmail.com`:
   - Subject: "PIAIC Quiz Tomorrow"
   - Body: "Test notification"

2. Run check:
   ```bash
   python src/main.py check
   ```

3. Check `khansarwar1@hotmail.com` for notification

## Test 4: Background Mode

```bash
python src/main.py start
```

**Expected behavior:**
- Runs initial check
- Schedules checks every 15 minutes
- Logs to `panaversity_assistant.log`
- Press Ctrl+C to stop

## Troubleshooting

**Error: "credentials.json not found"**
- Download from Google Cloud Console
- Place in project root

**Error: "SMTP authentication failed"**
- Use Gmail app password (not regular password)
- Check SMTP_PASSWORD in .env

**No emails detected:**
- Ensure email is unread
- Check keywords match
- Review logs

## Next Steps After Testing

1. Adjust check interval in .env
2. Customize keywords
3. Add WhatsApp integration (Phase 2)
4. Add LinkedIn monitoring (Phase 3)
