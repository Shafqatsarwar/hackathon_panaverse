"""
Step 1: LinkedIn Login and Session Save
This script opens LinkedIn and waits for you to log in.
Keep the browser open until you see the success message.
"""
import asyncio
import sys
from playwright.async_api import async_playwright

async def save_linkedin_session():
    print("=" * 70)
    print("🔐 STEP 1: LinkedIn Login & Session Save")
    print("=" * 70)
    print("\n📝 Instructions:")
    print("1. A browser window will open")
    print("2. Log in to LinkedIn if needed")
    print("3. Wait for your feed to fully load")
    print("4. Press Enter in this terminal when you see your LinkedIn feed")
    print("\n" + "=" * 70)
    
    input("\nPress Enter to open LinkedIn browser...")
    
    playwright = await async_playwright().start()
    
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="./linkedin_session",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--window-size=1280,800"
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    page = context.pages[0] if context.pages else await context.new_page()
    
    print("\n🌐 Opening LinkedIn...")
    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
    
    print("\n✅ Browser opened!")
    print("\n⏳ Waiting for you to log in...")
    print("   - If you see a login page, please log in")
    print("   - Wait for your feed to load completely")
    print("   - You should see your posts and connections")
    
    input("\n👉 Press Enter when you're logged in and can see your feed...")
    
    # Verify login
    print("\n🔍 Verifying login...")
    try:
        await page.wait_for_selector('#global-nav', timeout=5000)
        print("✅ Login verified! Session saved successfully!")
    except:
        print("⚠️ Could not verify login, but session may still be saved.")
    
    await context.close()
    await playwright.stop()
    
    print("\n" + "=" * 70)
    print("✅ SESSION SAVED!")
    print("=" * 70)
    print("\nYou can now run the sync script:")
    print("  python tests/sync_linkedin_to_odoo.py")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(save_linkedin_session())
