"""
WhatsApp Login Verification Script
Run this to open WhatsApp Web and verify/scan QR code.
"""
import sys
import os
from pathlib import Path

# Add project root to path so we can import skills
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_login():
    print("=" * 60)
    print("WhatsApp Web Login Verification")
    print("=" * 60)
    print("\nOpening WhatsApp Web in browser...")
    print("This window will stay open for 60 seconds.")
    print("\nWhat to do:")
    print("1. If you see a QR code, scan it with your phone")
    print("2. If you're already logged in, you'll see your chats")
    print("3. Wait for the verification to complete")
    print("\n" + "=" * 60 + "\n")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            user_data_dir = "./whatsapp_session"
            
            print(f"[INFO] Using session directory: {Path(user_data_dir).absolute()}")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("[INFO] Navigating to WhatsApp Web...")
            await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
            
            print("\n[WAITING] Checking login status (60 seconds)...")
            print("Please scan QR code if shown, or wait for chats to load...\n")
            
            # Try multiple selectors and give more time
            success = False
            for i in range(6):  # 6 attempts x 10 seconds = 60 seconds total
                try:
                    # Check for chat list (means logged in)
                    await page.wait_for_selector(
                        '#pane-side, [data-testid="chat-list"], div[aria-label="Chat list"]',
                        timeout=10000
                    )
                    print("\n✅ SUCCESS: WhatsApp is logged in!")
                    print("✅ Session saved. You can now use WhatsApp features.")
                    success = True
                    break
                except:
                    if i < 5:  # Don't print on last attempt
                        print(f"[{(i+1)*10}s] Still waiting... (scan QR if visible)")
            
            if not success:
                print("\n[TIMEOUT] Could not verify login.")
                # Capture screenshot for debugging
                try:
                    await page.screenshot(path="login_failed.png")
                    print("[INFO] Saved screenshot to 'login_failed.png' - please check this image.")
                except:
                    pass
                
                print("\nPossible reasons:")
                print("1. QR code wasn't scanned in time")
                print("2. WhatsApp Web is having connection issues")
                print("3. Browser was blocked by WhatsApp")
                print("\nTry running this script again and scan faster.")
            
            print("\n[INFO] Keeping browser open for 5 more seconds...")
            await asyncio.sleep(5)
            
            print("[INFO] Closing browser...")
            await context.close()
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure Playwright is installed:")
        print("  playwright install chromium")

if __name__ == "__main__":
    # Set Windows event loop policy
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(verify_login())
