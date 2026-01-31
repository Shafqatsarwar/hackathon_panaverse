
import sys
import os
import asyncio
import logging
from playwright.async_api import async_playwright

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DebugLinkedIn")

async def debug_linkedin():
    logger.info("--- Debugging LinkedIn Login (Headful) ---")
    logger.info(f"Target Email: {Config.LINKEDIN_EMAIL}")
    
    async with async_playwright() as p:
        # Launch browser visibly
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # 1. Go to Login
            logger.info("Navigating to https://www.linkedin.com/login")
            await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            # 2. Check Fields
            logger.info("Checking for fields...")
            if await page.locator("#username").count() > 0:
                logger.info("Found #username")
                await page.fill("#username", Config.LINKEDIN_EMAIL)
            elif await page.locator('input[name="session_key"]').count() > 0:
                 logger.info("Found input[name='session_key']")
                 await page.fill('input[name="session_key"]', Config.LINKEDIN_EMAIL)
            else:
                logger.error("No username field found! Dumping HTML...")
                content = await page.content()
                logger.error(content[:500]) # First 500 chars
                return

            if await page.locator("#password").count() > 0:
                 logger.info("Found #password")
                 await page.fill("#password", Config.LINKEDIN_PASSWORD)
            elif await page.locator('input[name="session_password"]').count() > 0:
                 logger.info("Found input[name='session_password']")
                 await page.fill('input[name="session_password"]', Config.LINKEDIN_PASSWORD)
            
            # 3. Submit
            logger.info("Clicking Submit...")
            await page.click('button[type="submit"]')
            
            # 4. Wait
            logger.info("Waiting for navigation...")
            await page.wait_for_timeout(5000)
            
            logger.info(f"Current URL: {page.url}")
            
            if "feed" in page.url or "check/challenge" not in page.url:
                 logger.info("SUCCESS: Seems to be logged in (or at least past login form)")
            else:
                 logger.warning("WARNING: Startup might be blocked or challenged.")
            
            # Keep open briefly to see
            await page.wait_for_timeout(5000)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await page.screenshot(path="debug_linkedin_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(debug_linkedin())
