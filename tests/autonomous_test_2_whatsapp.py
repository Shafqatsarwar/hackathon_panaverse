"""
AUTONOMOUS TEST 2: WHATSAPP SKILL
- Check Messages (Main + Archived)
- Filter by Keywords
- Send Test Message (Self-Test)
- Verify Forwarding Logic
"""
import sys
import os
import logging
import asyncio
sys.path.insert(0, os.path.abspath('.'))

from src.utils.config import Config
from skills.whatsapp_skill.skill import WhatsAppSkill

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WhatsAppTest")

async def test_whatsapp():
    print("\n🧪 TESTING WHATSAPP SKILL PROPERLY...")
    
    # 1. Initialize
    print("\n[1/4] Initializing WhatsApp Skill...")
    try:
        # Use headless=False initially if debugging needed, but aim for headless=True later
        # User requested autonomous, so we try normally. 
        # If session exists, it should work without specific login.
        wa_skill = WhatsAppSkill(enabled=True, headless=True) # Headless for autonomy
        print("   ✅ Initialization Successful")
    except Exception as e:
        print(f"   ❌ Initialization Error: {e}")
        return

    # 2. Sending Message (Write)
    print("\n[2/4] Testing Message Sending...")
    try:
        # Send to Admin Number from Config
        target = Config.ADMIN_WHATSAPP
        message = "🤖 Autonomous WhatsApp Test: Check & Send capability verified."
        print(f"   Sending to: {target}")
        
        # Using the sync wrapper or async? Let's use the provided public method
        result = wa_skill.send_message(target, message)
        
        if result.get('success'):
            print("   ✅ Message Sent Successfully")
        else:
            print(f"   ❌ Message Send Failed: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ Send Error: {e}")

    # 3. Reading & Archiving
    print("\n[3/4] Testing Message Reading (Main + Archived)...")
    try:
        # Check messages with keywords from Config
        keywords = Config.FILTER_KEYWORDS
        print(f"   Keywords: {keywords}")
        
        # Check messages (this should cover archived too based on internal logic)
        messages_result = wa_skill.check_messages(keywords=keywords, check_archived=True, limit=10)
        
        # It returns a list of dicts based on previous code, let's verify format
        if isinstance(messages_result, dict) and messages_result.get('success'):
            msgs = messages_result.get('messages', [])
            print(f"   ✅ Fetched {len(msgs)} messages")
            
            archived_count = sum(1 for m in msgs if m.get('source') == 'archived')
            print(f"   📂 Archived Messages found: {archived_count}")
            
            if msgs:
                m = msgs[0]
                print(f"   💬 Sample: {m.get('title')} - {m.get('last_message')}")
        else:
             print(f"   ❌ Read Failed: {messages_result}")

    except Exception as e:
        print(f"   ❌ Read Error: {e}")

    # 4. Forwarding Logic (Simulation)
    print("\n[4/4] Verifying Forwarding Logic...")
    try:
        forward_number = Config.WHATSAPP_FORWARD_MESSAGES
        forward_email = Config.EMAIL_FORWARD_EMAIL
        
        print(f"   Forwarding Configured: WA->{forward_number}, Email->{forward_email}")
        
        if forward_number or forward_email:
            print("   ✅ Forwarding configuration present")
        else:
            print("   ⚠️ Forwarding configuration missing (check .env)")
            
    except Exception as e:
        print(f"   ❌ Forwarding Check Error: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_whatsapp())
