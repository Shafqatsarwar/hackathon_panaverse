"""Quick test all skills - headless mode"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.utils.config import Config

print("Testing all skills...")

# 1. Gmail
print("\n1. Gmail...")
try:
    from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
    gm = GmailMonitoringSkill(Config.GMAIL_CREDENTIALS_PATH, Config.GMAIL_TOKEN_PATH, Config.FILTER_KEYWORDS)
    gm.authenticate()
    emails = gm.fetch_unread_emails(3)
    print(f"✅ Gmail: {len(emails)} emails")
except Exception as e:
    print(f"❌ Gmail: {e}")

# 2. WhatsApp
print("\n2. WhatsApp...")
try:
    from skills.whatsapp_skill.skill import WhatsAppSkill
    wa = WhatsAppSkill(enabled=Config.WHATSAPP_ENABLED, headless=True)
    result = wa.check_messages()
    print(f"✅ WhatsApp: {result.get('success', False)}")
except Exception as e:
    print(f"❌ WhatsApp: {e}")

# 3. LinkedIn  
print("\n3. LinkedIn...")
try:
    from skills.linkedin_skill.skill import LinkedInSkill
    li = LinkedInSkill(enabled=Config.LINKEDIN_ENABLED, headless=True)
    result = li.check_notifications()
    print(f"✅ LinkedIn: {result.get('success', False)}")
except Exception as e:
    print(f"❌ LinkedIn: {e}")

# 4. Odoo
print("\n4. Odoo...")
try:
    from skills.odoo_skill.skill import OdooSkill
    odoo = OdooSkill(Config.ODOO_URL, Config.ODOO_DB, Config.ODOO_USERNAME, Config.ODOO_PASSWORD)
    result = odoo.get_leads(5)
    print(f"✅ Odoo: {result.get('success', False)}")
except Exception as e:
    print(f"❌ Odoo: {e}")

# 5. Chatbot
print("\n5. Chatbot...")
try:
    from agents.chat_agent import ChatAgent
    chat = ChatAgent()
    result = chat.chat("Hello")
    print(f"✅ Chatbot: {result.get('status') == 'success'}")
except Exception as e:
    print(f"❌ Chatbot: {e}")

print("\nDone!")
