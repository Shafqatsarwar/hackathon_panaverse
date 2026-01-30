"""
MASTER LOGIN & SERVICE VERIFICATION
Checks login for all services. Pauses for manual intervention if needed.
"""
import sys
import os
import asyncio
import logging
sys.path.insert(0, os.path.abspath('.'))

from src.utils.config import Config
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from skills.whatsapp_skill.skill import WhatsAppSkill
from skills.linkedin_skill.skill import LinkedInSkill
from skills.odoo_skill.skill import OdooSkill

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def main():
    print("\n" + "="*60)
    print("🔐 MASTER LOGIN VERIFICATION")
    print("="*60)
    
    # 1. GMAIL
    print("\n📧 CHECKING GMAIL...")
    try:
        gmail = GmailMonitoringSkill(Config.GMAIL_CREDENTIALS_PATH, Config.GMAIL_TOKEN_PATH, Config.FILTER_KEYWORDS)
        if gmail.authenticate():
            print("✅ Gmail: Connected")
        else:
            print("❌ Gmail: Login Failed")
            print("👉 Action: Check credentials.json or delete token.json to re-auth")
            input("Press Enter to continue...")
    except Exception as e:
        print(f"❌ Gmail Error: {e}")

    # 2. ODOO
    print("\n📊 CHECKING ODOO CRM...")
    try:
        odoo = OdooSkill()
        if odoo.authenticate():
            print(f"✅ Odoo: Connected (UID: {odoo.uid})")
        else:
            print("❌ Odoo: Login Failed")
            print("👉 Action: Check .env ODOO credentials")
            input("Press Enter to continue...")
    except Exception as e:
        print(f"❌ Odoo Error: {e}")

    # 3. LINKEDIN
    print("\n🔗 CHECKING LINKEDIN (Headless)...")
    if Config.LINKEDIN_ENABLED:
        try:
            li = LinkedInSkill(enabled=True, headless=True) # Try headless first
            res = li.scrape_leads() # This triggers login check
            if res.get('success'):
                print("✅ LinkedIn: Connected")
            else:
                print(f"❌ LinkedIn: Failed ({res.get('error')})")
                print("👉 Switching to Non-Headless for Manual Login...")
                li_headed = LinkedInSkill(enabled=True, headless=False)
                res_headed = li_headed.scrape_leads()
                if res_headed.get('success'):
                    print("✅ LinkedIn: Connected Manually")
                else:
                    print(f"❌ LinkedIn: Still Failed ({res_headed.get('error')})")
                    input("Press Enter if you fixed it manually...")
        except Exception as e:
            print(f"❌ LinkedIn Error: {e}")
    else:
        print("⚠️ LinkedIn Disabled in Config")

    # 4. WHATSAPP
    print("\n💬 CHECKING WHATSAPP (Headless)...")
    if Config.WHATSAPP_ENABLED:
        try:
            # Check if session exists
            if not os.path.exists("./whatsapp_session"):
                print("⚠️ No WhatsApp Session found. Starting Manual Login...")
                wa_headed = WhatsAppSkill(enabled=True, headless=False)
                # Just init browser to allow login
                await wa_headed._init_browser()
                input("👉 Scan QR Code in Browser. Press Enter when Chat list appears...")
                print("✅ Assuming Login Complete due to user confirmation.")
            else:
                wa = WhatsAppSkill(enabled=True, headless=True)
                res = await wa.check_messages_async(limit=1)
                
                if isinstance(res, dict) and res.get('success'):
                    print("✅ WhatsApp: Connected")
                else:
                    print(f"❌ WhatsApp: Failed ({res})")
                    print("👉 Starting Non-Headless for Reset...")
                    wa_headed = WhatsAppSkill(enabled=True, headless=False)
                    await wa_headed._init_browser()
                    input("👉 Verify Login in Browser. Press Enter when ready...")
        except Exception as e:
            print(f"❌ WhatsApp Error: {e}")
    else:
        print("⚠️ WhatsApp Disabled in Config")

    print("\n" + "="*60)
    print("🎉 VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
