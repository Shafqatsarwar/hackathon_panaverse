# Panaversity Assistant - Quick Start & Credentials Guide 🚀

Welcome to the **Panaversity Student Assistant**! This guide focuses on **Setting up your Environment** and **Getting your Credentials**.

---

## ⚡ Step 1: Environment Variables (`.env`)

To run the assistant, you must create a `.env` file in the root directory.
**Never share this file.** It contains your secrets.

1.  Copy `.env.example` -> `.env`.
2.  Fill in the keys as described below.

---

## 🔐 How to Get Your Credentials

### 1. 🤖 Google Gemini API (Free tier available)
*Required for the Brain to think and Chat to work.*
1.  Go to **[Google AI Studio](https://aistudio.google.com/)**.
2.  Click **"Get API key"** in the top left.
3.  Click **"Create API key"**.
4.  Copy the string starting with `AIza...`.
5.  **Update `.env`**:
    ```ini
    GOOGLE_API_KEY=AIzaSyB...
    ```

### 2. 📧 Gmail App Password (NOT your normal password)
*Required for monitoring emails safely.*
1.  Go to your **[Google Account Security](https://myaccount.google.com/security)** page.
2.  Enable **2-Step Verification** if it's off.
3.  Search for **"App passwords"** in the search bar at the top (or look under 2-Step Verification options).
4.  Create a new app name: `PanaversityBot`.
5.  It will show you a 16-character code (e.g., `abcd efgh ijkl mnop`).
6.  **Update `.env`**:
    ```ini
    GMAIL_ADDRESS=your.email@gmail.com
    GMAIL_PASSWORD=abcdefghijklmnop  # No spaces needed
    ```

### 3. 📊 Odoo CRM Configuration
*Required for Lead Management.*
1.  **URL**: The link you use to login (e.g., `https://my-company.odoo.com`).
2.  **Database (`ODOO_DB`)**:
    - For Odoo Online (SaaS): This is usually the **subdomain** (e.g., `my-company` if url is `my-company.odoo.com`).
    - *Tip*: Click your profile icon -> "My Databases" to confirm the exact name.
3.  **Username/Password**: Your login credentials.
4.  **Update `.env`**:
    ```ini
    ODOO_URL=https://excellence-links.odoo.com
    ODOO_DB=excellence-links          # Just the name, NOT the URL
    ODOO_USERNAME=admin@example.com
    ODOO_PASSWORD=your_password
    ```

### 4. 💬 WhatsApp Integration
*Uses Web Automation (No API key required).*
1.  **Enable**: Set `WHATSAPP_ENABLED=true` in `.env`.
2.  **Run**: When you start the watcher (`python watchers.py`), a browser window (or QR code in logs) will appear.
3.  **Scan**: Use your phone (WhatsApp -> Linked Devices) to scan the QR code.
4.  *Session is saved locally for future runs.*

### 5. 💼 LinkedIn Integration (Optional)
*Uses Browser Automation.*
1.  **Enable**: Set `LINKEDIN_ENABLED=true` in `.env`.
2.  **Credentials**:
    ```ini
    LINKEDIN_EMAIL=your.linkedin@email.com
    LINKEDIN_PASSWORD=your_password
    ```

---

## 🏃‍♀️ Step 2: How to Run (Quick Modes)

### Option A: The "Developer" (Recommended)
Use the menu to pick exactly what you want to run.
```powershell
python manage.py
```

### Option B: The "One-Click" (Windows)
Double-click `start.bat`. This opens the API and Frontend automatically.

---

## � System Dashboard
Once running at `http://localhost:3000`:
- **Green Dot**: Connected to API.
- **Odoo Button**: Green = Connected to CRM.
- **Email Button**: Green = Gmail Authenticated.

---

## ❓ Troubleshooting
- **"Authentication Failed" (Gmail)**: You used your real password. Use an **App Password**.
- **"Database not found" (Odoo)**: Double check `ODOO_DB`. It is usually *not* the full URL.
- **"Browser closed" (WhatsApp)**: The automation needs the browser open to work. Don't close the automation window manually.
