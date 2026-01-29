"""
Debug script to inspect WhatsApp Archived folder contents.
Run this to see exactly what the bot sees.
"""
import asyncio
import sys
import logging
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_archived():
    print("="*60)
    print("DEBUGGING WHATSAPP ARCHIVED FOLDER")
    print("="*60)
    
    async with async_playwright() as p:
        # Use existing session
        user_data_dir = "./whatsapp_session"
        print(f"Using session: {user_data_dir}")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://web.whatsapp.com")
        
        print("Waiting for login...")
        # Try multiple selectors
        selectors = [
            '[data-testid="chat-list"]', 
            '#pane-side', 
            'div[aria-label="Chat list"]',
            'div[role="grid"]' # Sometimes the list is a grid
        ]
        
        logged_in = False
        for s in selectors:
            try:
                await page.wait_for_selector(s, timeout=5000)
                print(f"Login detected via: {s}")
                logged_in = True
                break
            except:
                pass
                
        if not logged_in:
            print("Login check failed (timeout). Taking screenshot details...")
            await page.screenshot(path="debug_login_fail.png")
        
        print("Looking for Archived button...")
        archived_selectors = [
            'button[aria-label="Archived"]',
            '[data-testid="archived"]',
            'span[data-icon="archived"]',
            'div[title="Archived"]'
        ]
        
        found = False
        for sel in archived_selectors:
            if await page.locator(sel).count() > 0:
                print(f"Found Archived button: {sel}")
                await page.locator(sel).first.click()
                found = True
                break
        
        if not found:
            print("❌ Could not find Archived button!")
            await context.close()
            return
            
        print("Entered Archived folder. Waiting for list...")
        await asyncio.sleep(2)
        
        # Take screenshot
        await page.screenshot(path="debug_archived_view.png")
        print("📸 Saved 'debug_archived_view.png'")
        
        # Scan ROWS
        rows = await page.locator('div[role="row"]').all()
        print(f"Found {len(rows)} visible rows.")
        
        print("\n--- DETECTED CHATS ---")
        for i, row in enumerate(rows):
            try:
                # Try finding title
                title_el = row.locator('[dir="auto"][title]')
                if await title_el.count() > 0:
                    title = await title_el.first.text_content()
                else:
                    title = "[No Title]"
                    
                # Try finding unread badge
                unread_el = row.locator('[aria-label*="unread message"]')
                if await unread_el.count() > 0:
                    unread = await unread_el.first.text_content()
                else:
                    unread = "0"
                    
                print(f"{i+1}. Title: '{title}' | Unread: {unread}")
            except Exception as e:
                print(f"Error reading row {i}: {e}")
                
        print("----------------------\n")
        
        print("Closing in 5 seconds...")
        await asyncio.sleep(5)
        await context.close()

if __name__ == "__main__":
    asyncio.run(debug_archived())
