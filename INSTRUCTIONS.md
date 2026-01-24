# Setup Instructions: API Keys & Secrets

This project relies on several external services. All secrets are stored in the `.env` file. **NEVER share your `.env` file.**

## 1. Google Gemini (Chatbot)
**Purpose**: Powers the AI Brain.
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Click **"Get API Key"** -> **"Create API Key"**.
3.  Copy the key string.
4.  Update `.env`:
    ```ini
    GOOGLE_API_KEY="AIzaSy..."
    ```

## 2. Google Gmail (Email Monitoring)
**Purpose**: Allows the bot to read your emails.
1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a Project. Enable "Gmail API".
3.  **OAuth Consent Screen**:
    -   Set User Type to **External**.
    -   Publishing Status: **"In Production"** (to avoid user limits).
    -   Add your email as a Test User just in case.
4.  **Credentials**:
    -   Create Credentials -> OAuth Client ID -> Desktop App.
    -   Download JSON, rename it to `credentials.json`, and place it in the project root.
5.  **First Run**: The app will open a browser to login. Follow the prompts (Advanced -> Unsafe -> Continue).

## 3. Odoo CRM (Business Logic)
**Purpose**: Syncs emails to a CRM system.
1.  Go to [Odoo.com](https://www.odoo.com/).
2.  Sign up for **Founders/Free Trial** (Select 'CRM' app).
3.  Get your **Database Name** (usually your subdomain, e.g., `my-project` from `my-project.odoo.com`).
4.  Update `.env`:
    ```ini
    ODOO_URL=https://your-project.odoo.com
    ODOO_DB=your-project
    ODOO_USERNAME=your-email@gmail.com
    ODOO_PASSWORD=your-password
    ```

## 4. WhatsApp & LinkedIn
**Purpose**: Sending alerts.
-   **WhatsApp**: Handled locally via Browser Automation. Required `playwright install`.
-   **LinkedIn**: Configured in `.env` (Username/Password).

## 5. Final Checklist Before Git Push
1.  Check `.gitignore`: Ensure `.env`, `credentials.json`, `token.json` are listed.
2.  Check `.env`: Ensure no secrets are hardcoded in python files (use `os.getenv`).
3.  **Push**:
    ```bash
    git add .
    git commit -m "Final submission"
    git push origin main
    ```
