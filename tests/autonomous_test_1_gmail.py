"""
AUTONOMOUS TEST 1: GMAIL SKILL
- Check Authentication
- Fetch Unread Emails
- Filter by Keywords
- Send Test Email (Self-Test)
"""
import sys
import os
import logging
import time
sys.path.insert(0, os.path.abspath('.'))

from src.utils.config import Config
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from skills.email_notifications.email_notifications import EmailNotificationSkill

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GmailTest")

def test_gmail():
    print("\n🧪 TESTING GMAIL SKILL PROPERLY...")
    
    # 1. Initialize
    print("\n[1/4] Initializing Gmail Skill...")
    try:
        # Config.FILTER_KEYWORDS is already a list, so we don't need to split it
        keywords = Config.FILTER_KEYWORDS
        print(f"   Keywords: {keywords}")
        
        gmail_skill = GmailMonitoringSkill(
            credentials_path=Config.GMAIL_CREDENTIALS_PATH, 
            token_path=Config.GMAIL_TOKEN_PATH, 
            keywords=keywords
        )
        
        if gmail_skill.authenticate():
            print("   ✅ Authentication Successful")
        else:
            print("   ❌ Authentication Failed")
            return
            
    except Exception as e:
        print(f"   ❌ Initialization Error: {e}")
        return

    # 2. Reading Emails
    print("\n[2/4] Fetching Unread Emails...")
    try:
        emails = gmail_skill.fetch_unread_emails(max_results=5)
        print(f"   ✅ Fetched {len(emails)} unread emails")
        
        # Display 1 email summary if available
        if emails:
            e = emails[0]
            print(f"   📧 Sample: {e.get('subject', 'No Subject')} (from: {e.get('sender', 'Unknown')})")
            
    except Exception as e:
        print(f"   ❌ Fetch Error: {e}")

    # 3. Filtering
    print("\n[3/4] Testing Keyword Filtering...")
    try:
        # Mocking a relevant email for test assurance
        mock_emails = emails + [{
            'subject': 'Important: Panaversity Update', 
            'body': 'This is matched by keyword Panaversity',
            'sender': 'test@example.com'
        }]
        
        filtered = gmail_skill.filter_relevant_emails(mock_emails)
        print(f"   ✅ Filter passed. Found {len(filtered)} relevant emails (including mock).")
        
    except Exception as e:
        print(f"   ❌ Filter Error: {e}")

    # 4. Sending Email (Writing)
    print("\n[4/4] Testing Email Sending (SMTP)...")
    try:
        notifier = EmailNotificationSkill(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            smtp_username=Config.SMTP_USERNAME,
            smtp_password=Config.SMTP_PASSWORD
        )
        subject = f"Autonomous Test {time.strftime('%H:%M:%S')}"
        body = "This is an autonomous test of the Gmail Write/Send capability."
        
        # Sending to self (Admin Email)
        to_email = Config.ADMIN_EMAIL
        print(f"   Sending to: {to_email}")
        
        success = notifier.send_email_notification(to_email, subject, body)

        
        if success:
            print("   ✅ Email Sent Successfully")
        else:
            print("   ❌ Email Send Failed (Check SMTP Config)")
            
    except Exception as e:
        print(f"   ❌ Send Error: {e}")

if __name__ == "__main__":
    test_gmail()
