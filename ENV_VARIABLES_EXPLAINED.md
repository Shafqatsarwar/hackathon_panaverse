# Environment Variables Explained

## 📋 Complete Guide to .env Configuration

This document explains **every variable** in your `.env` file, what it's used for, and whether you need to configure it.

---

## 🔐 Backend Configuration (Required for Core Functionality)

### 1. Gmail Configuration
**Purpose**: Monitor Gmail for assignments, quizzes, and important emails

```bash
GMAIL_ADDRESS=exellencelinks@gmail.com
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.json
```

**Used by**: 
- `skills/gmail_skill/` - Email monitoring
- `watchers.py` - Automated email checking
- Gmail agent for notifications

**Setup Required**: Yes (for email monitoring to work)

---

### 2. Admin Notifications
**Purpose**: Where to send alerts and notifications from the system

```bash
ADMIN_EMAIL=khansarwar1@hotmail.com
ADMIN_WHATSAPP=+923244279017
```

**Used by**:
- Alert system to notify you of important events
- WhatsApp skill for sending notifications
- Email filtering for urgent messages

**Setup Required**: Yes (these are YOUR contact details for receiving alerts)

---

### 3. SMTP Configuration
**Purpose**: Send email notifications from the system

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=exellencelinks@gmail.com
SMTP_PASSWORD=your_app_password_here
```

**Used by**:
- Email notification skill
- Sending alerts and summaries via email

**Setup Required**: Optional (only if you want to send emails)

---

### 4. WhatsApp Configuration
**Purpose**: Send/receive WhatsApp messages, check for PIAIC updates

```bash
WHATSAPP_ENABLED=true
```

**Used by**:
- `skills/whatsapp_skill/` - WhatsApp automation
- `watchers.py` - Monitor WhatsApp for keywords
- WhatsApp agent for messaging

**Setup Required**: Yes (if you want WhatsApp integration)
**Status**: ✅ WORKING

---

### 5. LinkedIn Configuration
**Purpose**: Post updates, extract connections, check notifications

```bash
LINKEDIN_ENABLED=true
LINKEDIN_EMAIL=exellencelinks@gmail.com
LINKEDIN_PASSWORD=your_password_here
```

**Used by**:
- `skills/linkedin_skill/` - LinkedIn automation
- Connection extraction for CRM
- Posting project updates

**Setup Required**: Optional (for LinkedIn features)
**Status**: ✅ POSTING WORKS

---

### 6. AI Configuration
**Purpose**: Power the chatbot and AI summarization

```bash
GOOGLE_API_KEY=**************
OPENAI_API_KEY=your_openai_key_here
```

**Used by**:
- `skills/chatbot_skill/` - AI conversations
- Summarization of emails/messages
- Intelligent task creation

**Setup Required**: Yes (for AI features)
**Status**: ⚠️ Current key expired

---

### 7. Odoo CRM Configuration
**Purpose**: Save LinkedIn connections as leads, manage CRM

```bash
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database_name
ODOO_USERNAME=your_odoo_username
ODOO_PASSWORD=your_odoo_password
```

**Used by**:
- `skills/odoo_skill/` - CRM integration
- LinkedIn to Odoo lead conversion
- Contact management

**Setup Required**: Optional (for CRM features)
**Status**: ❌ NOT CONFIGURED

---

### 8. Monitoring Intervals
**Purpose**: How often to check for new messages/emails

```bash
EMAIL_CHECK_INTERVAL=15
WHATSAPP_CHECK_INTERVAL=60
LINKEDIN_CHECK_INTERVAL=60
```

**Used by**:
- `watchers.py` - Background monitoring
- Automated task creation

**Setup Required**: No (defaults are fine)

---

### 9. Filter Keywords
**Purpose**: What keywords to look for in messages

```bash
FILTER_KEYWORDS=Panaversity,PIAIC,Panaverse,Quiz,Assignment,Exam,Deadline,Urgent
```

**Used by**:
- Email filtering
- WhatsApp message scanning
- Task priority detection

**Setup Required**: No (but you can customize)

---

## 🌐 Frontend Configuration (For Website Display Only)

### 10. Public Contact Information
**Purpose**: Display contact information on your website/frontend

```bash
NEXT_PUBLIC_EMAIL=exellencelinks@gmail.com
NEXT_PUBLIC_PHONE_PK=+923244279017
NEXT_PUBLIC_WHATSAPP=+46764305834
NEXT_PUBLIC_FACEBOOK_URL=https://www.facebook.com/profile.php?id=100079966850856
NEXT_PUBLIC_EMAIL_ID=khansarwar1@hotmail.com
```

**Used by**:
- Next.js frontend (if you build a public website)
- Contact page
- Footer information
- "Contact Us" sections

**Why NEXT_PUBLIC_?**
- In Next.js, variables starting with `NEXT_PUBLIC_` are exposed to the browser
- They're safe to show publicly (contact info, not passwords)
- They get embedded in the frontend JavaScript bundle

**Setup Required**: Optional (only if you want to display contact info on a website)

**Current Status**: 
- These are currently set to what appears to be **my information**
- If this project is for Panaversity/PIAIC, you might want to update these to Panaversity contact details
- If you're not building a public website, these can be ignored

---

## 🎯 Summary: What You Actually Need

### ✅ Essential (For Core Features):
1. **Gmail** - For email monitoring
2. **Admin WhatsApp** - Your number for receiving alerts
3. **WhatsApp Enabled** - For WhatsApp integration
4. **Google API Key** - For AI features

### ⚠️ Optional (For Extra Features):
5. **LinkedIn** - For LinkedIn integration
6. **Odoo CRM** - For lead management
7. **SMTP** - For sending email notifications
8. **NEXT_PUBLIC_*** - For website contact display

### ❌ Not Currently Used:
9. **GitHub Token** - Not implemented yet
10. **OpenAI API** - Fallback (using Gemini instead)

---

## 🔍 Specific Answer: NEXT_PUBLIC_* Variables

**Q: Why do we use these?**

**A: Two scenarios:**

### Scenario 1: You're Building a Public Website
If you're creating a public-facing website for Panaversity Student Assistant:
- These variables will show contact information on the website
- Students can see how to contact support
- Displayed in footer, contact page, etc.

**Example Frontend Code:**
```javascript
// In your Next.js component
<footer>
  <p>Email: {process.env.NEXT_PUBLIC_EMAIL}</p>
  <p>WhatsApp: {process.env.NEXT_PUBLIC_WHATSAPP}</p>
  <p>Phone UK: {process.env.NEXT_PUBLIC_PHONE_UK}</p>
</footer>
```

### Scenario 2: You're NOT Building a Public Website
If this is just a backend automation tool:
- **You can ignore these variables**
- They won't affect functionality
- They're just sitting there unused

---

## 💡 Recommendations

### For NEXT_PUBLIC_* Variables:

**Option 1: Keep Them (If building a website)**
Update to Panaversity contact information:
```bash
NEXT_PUBLIC_EMAIL=support@panaversity.com
NEXT_PUBLIC_PHONE_PK=+923001234567
NEXT_PUBLIC_WHATSAPP=+923001234567
```

**Option 2: Remove Them (If NOT building a website)**
These are safe to remove from `.env` if you're not using the frontend for public display.

**Option 3: Leave As-Is**
If these are your actual contact details for Online Quran teaching, and you might use them later, keep them.

---

## 🔐 Security Note

**NEXT_PUBLIC_* = Public Information**
- These variables are **intentionally public**
- They get embedded in browser JavaScript
- Never put passwords or API keys in NEXT_PUBLIC_* variables
- Only use for information you're okay with anyone seeing

**Regular Variables = Private**
- `GOOGLE_API_KEY`, `ODOO_PASSWORD`, etc. are **private**
- Never exposed to browser
- Stay on the server only

---

## 📝 Current Status of Your .env

Based on the values I see:

1. **NEXT_PUBLIC_EMAIL=onlinequran50@gmail.com**
   - This appears to be for Online Quran teaching
   - If this project is for Panaversity, consider updating

2. **NEXT_PUBLIC_WHATSAPP=+46764305834**
   - This is your second WhatsApp number (Sweden)
   - Makes sense if you want students to contact you there

3. **NEXT_PUBLIC_PHONE_UK/PK**
   - UK and Pakistan phone numbers
   - For international student contact

**Question for you**: 
- Is this project for **Panaversity/PIAIC** or **Online Quran teaching**?
- If Panaversity: Update NEXT_PUBLIC_* to Panaversity contact info
- If Online Quran: Keep as-is

---

## ✅ Action Items

1. **Immediate (For Odoo)**:
   - Follow `ODOO_SETUP_GUIDE.md`
   - Update Odoo credentials in `.env`

2. **Soon (For AI)**:
   - Get new Google API key
   - Update `GOOGLE_API_KEY`

3. **Optional (For NEXT_PUBLIC_*)**:
   - Decide if you're building a public website
   - If yes: Update to correct contact info
   - If no: Can ignore or remove

---

**Need help deciding?** Let me know what you want to use this project for, and I can advise on which variables you actually need!
