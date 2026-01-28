"""
Verify WhatsApp Login Script
Run this to open WhatsApp Web and scan the QR code.
"""
import asyncio
import logging
from skills.whatsapp_skill.skill import WhatsAppSkill

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_login():
    print("Initializing WhatsApp Skill...")
    # Headless=False to see the browser
    skill = WhatsAppSkill(headless=False)
    
    print("Opening WhatsApp Web...")
    print("Please scan the QR code if prompted.")
    print("If you are already logged in, the window will close automatically after verification.")
    
    # We use a dummy number to trigger the browser open flow, 
    # but we just want to reach the main page.
    # Actually, let's call a specific login_only method if we implement it, 
    # or just use the internal browser method with a dummy check.
    
    try:
        # Custom logic similar to internal _send_via_browser but just for login
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            user_data_dir = "./whatsapp_session"
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            await page.goto("https://web.whatsapp.com")
            
            try:
                # Wait up to 10s for session to be recognized
                await page.wait_for_selector("#pane-side", timeout=10000)
                print("SUCCESS: WhatsApp session is ACTIVE!")
            except Exception:
                print("TIMEOUT: Login failed or QR code not scanned.")
            
            print("Closing browser...")
            await context.close()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_login())
