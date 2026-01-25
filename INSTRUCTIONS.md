# Quick Start Instructions 🚀

Welcome to the **Panaversity Student Assistant**! 
Follow these steps to get up and running quickly.

---

## ⚡ Step 1: Credentials Setup
**STOP!** Have you set up your API keys?

To run the Panaversity Student Assistant, you need to configure several API keys and credentials. These should be stored in your `.env` file.

**⚠️ SECURITY WARNING:** Never commit your `.env` file or these credentials to GitHub.

---

## 1. Quick Setup
1. Copy `.env.example` to `.env` (if you haven't already).
2. Fill in the values below.

---

## 2. Required Credentials

### 🤖 Google Gemini (AI Chatbot)
Required for the chatbot to answer questions.
- **Variable**: `GOOGLE_API_KEY`
- **How to Get**: 
  1. Go to [Google AI Studio](https://aistudio.google.com/).
  2. Create a new API Key.

### 📧 Gmail (Email Monitoring)
Required for checking emails and sending alerts.
- **Variable**: `GMAIL_ADDRESS` (Your email)
- **Variable**: `GMAIL_PASSWORD` (App Password, NOT your login password)
- **How to Get**:
  1. Go to Google Account > Security > 2-Step Verification (Enable it).
  2. Go to "App passwords" (search for it).
  3. Generate a new App Password for "Mail".

### 📊 Odoo (CRM/ERP)
Required for creating and reading leads.
- **Variable**: `ODOO_URL` (e.g., https://your-company.odoo.com)
- **Variable**: `ODOO_DB` (Database name)
- **Variable**: `ODOO_USERNAME` (Your login email)
- **Variable**: `ODOO_PASSWORD` (API Key or Password)

### 💬 WhatsApp (Alerts & Reading)
Required for WhatsApp integration.
- **Variable**: `WHATSAPP_ENABLED=true`
- **Note**: This uses **WhatsApp Web automation**. No API key is strictly required, but you must scan the QR code on the first run.

---

## 3. Optional Configuration

### Social Media
- **LinkedIn**: Set `LINKEDIN_ENABLED=true` and provide `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD`.

### Admin Alerts
- **Variable**: `ADMIN_EMAIL` (Where to send email alerts)
- **Variable**: `ADMIN_WHATSAPP` (Your phone number for alerts, e.g., +923001234567)

---

## 4. Troubleshooting Credentials
- **Error: "Authentication Failed"**: Check if your App Password is correct.
- **Error: "Odoo Connection Refused"**: Ensure your Odoo URL is reachable and DB name is exact.
- **WhatsApp not working**: Make sure to scan the QR code in the terminal window.

---

## 🚀 Step 2: How to Run
Choose the method that suits you best:

### Option A: The "Double-Click" (Easiest) 🖱️
1. Go to the project folder.
2. Double-click **`start.bat`**.
3. Wait for two windows to open.
4. The App will open in your browser automatically.

### Option B: The "Management Console" (For Testers) 🛠️
1. Open a terminal.
2. Run: `python manage.py`
3. Select an option from the menu (e.g., "Run Backend Only" or "Run Manual Check").

### Option C: The "Dev Command" (For Coders) ⚡
1. Open a terminal.
2. Run: `.\start`
3. Uses the same logic as Option A but keeps the main terminal open.

---

## 💡 Step 3: How to Use

### 💬 Chat with the AI
Once the app is open at `http://localhost:3000`:
- **Ask General Questions**: "What is Panaversity?" or "Find recent AI news".
- **Check Emails**: "do I have any unread emails?"
- **Check WhatsApp**: "Check my WhatsApp messages" or "Any messages about PIAIC?".

### 🟢 Status Dashboard
- **Top Right Buttons**:
  - `Odoo`: Click to see connection status or toggle checks.
  - `Email`: Shows if Gmail is authenticated.
  - `WhatsApp`: Shows if automation is active.

### 📱 WhatsApp Automation
- **First Run**: Look at the *Backend Terminal*. If it says "Scan QR Code", you must scan it with your phone to log in.
- **Alerts**: The system will automatically check for new messages every hour (or when you ask).

---

See **[GUIDE.md](GUIDE.md)** for detailed developer documentation.
