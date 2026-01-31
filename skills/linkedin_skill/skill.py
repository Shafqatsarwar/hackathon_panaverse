"""
LinkedIn Skill Implementation (Playwright Edition) - Stable V2
Uses browser automation to share updates and check notifications/messages.
Optimized for Windows stability.
"""
import logging
import asyncio
import sys
import os
import time
from typing import Dict, Any, List, Optional
import nest_asyncio
from playwright.async_api import async_playwright, Page, BrowserContext, Playwright
from src.utils.config import Config

logger = logging.getLogger(__name__)

class LinkedInSkill:
    """Skill to handle LinkedIn interactions using Playwright"""
    
    def __init__(self, enabled: bool = True, headless: bool = False, session_dir: str = "./linkedin_session"):
        self.enabled = enabled
        self.headless = headless 
        self.session_dir = os.path.abspath(session_dir)
        
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir, exist_ok=True)
            
    async def _wait_for_login(self, page: Page) -> bool:
        """Waits for login to complete"""
        try:
            # Wait for global nav or feed
            # #global-nav is standard
            await page.wait_for_selector('#global-nav', timeout=15000) # Reduced timeout for faster check
            return True
        except:
            return False

    async def _scrape_data(self, scan_messages: bool = True) -> Dict[str, Any]:
        """Internal scraping method"""
        playwright: Optional[Playwright] = None
        context: Optional[BrowserContext] = None
        results = {"notifications": [], "messages": []}

        try:
            playwright = await async_playwright().start()
            
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_dir,
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            # 1. Login Check
            logger.info("LinkedIn Skill: Checking login...")
            if "linkedin.com/feed" not in page.url:
                await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            
            if not await self._wait_for_login(page):
                logger.info("LinkedIn Skill: Session invalid. Attempting autonomous login...")

                try:
                    # Navigate to login if not there
                    if "login" not in page.url and "checkpoint" not in page.url:
                        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
                        await page.wait_for_timeout(2000)

                    # Try multiple selectors for username
                    user_selectors = ['#username', 'input[name="session_key"]', '.login-email']
                    user_filled = False
                    for sel in user_selectors:
                        if await page.locator(sel).count() > 0:
                            await page.fill(sel, Config.LINKEDIN_EMAIL)
                            user_filled = True
                            break
                    
                    if not user_filled:
                         raise Exception("Could not find username field")

                    # Try multiple selectors for password
                    pass_selectors = ['#password', 'input[name="session_password"]', '.login-password']
                    for sel in pass_selectors:
                        if await page.locator(sel).count() > 0:
                            await page.fill(sel, Config.LINKEDIN_PASSWORD)
                            break
                            
                    # Click submit (robustly)
                    await page.click('button[type="submit"]')
                    
                    # Wait for feed
                    await page.wait_for_selector('#global-nav', timeout=30000)
                    logger.info("LinkedIn Skill: Autonomous login successful!")
                    
                except Exception as e:
                    logger.error(f"LinkedIn Skill: Autonomous login failed. Current URL: {page.url} - Error: {e}")
                    # Capture screenshot for debugging
                    try:
                         await page.screenshot(path="linkedin_login_fail.png")
                         logger.info("Saved screenshot to linkedin_login_fail.png")
                    except: pass
                    
                    await context.close()
                    await playwright.stop()
                    return {"success": False, "error": f"Login failed: {e}"}

            # 2. Get Notifications
            logger.info("LinkedIn Skill: Checking notifications...")
            await page.goto("https://www.linkedin.com/notifications/", wait_until="domcontentloaded")
            try:
                await page.wait_for_selector('.nt-card-content', timeout=10000)
                cards = await page.locator('.nt-card-content').all()
                for card in cards[:5]:
                    text = await card.text_content()
                    results["notifications"].append(" ".join(text.split()))
            except Exception as e:
                logger.warning(f"LinkedIn Notification Scan error: {e}")

            # 3. Get Messages (Potential Leads)
            if scan_messages:
                logger.info("LinkedIn Skill: Checking messages...")
                await page.goto("https://www.linkedin.com/messaging/", wait_until="domcontentloaded")
                try:
                    # Wait for message list
                    await page.wait_for_selector('div[class*="msg-conversation-card"]', timeout=10000)
                    
                    conversations = await page.locator('div[class*="msg-conversation-card"]').all()
                    
                    for conv in conversations[:5]:
                        try:
                            # Extract sender
                            sender_el = conv.locator('h3, .msg-conversation-listitem__participant-names')
                            sender = await sender_el.first.text_content() if await sender_el.count() else "Unknown"
                            
                            # Extract preview
                            preview_el = conv.locator('p, .msg-conversation-card__message-snippet')
                            preview = await preview_el.first.text_content() if await preview_el.count() else ""
                            
                            results["messages"].append({
                                "sender": sender.strip(),
                                "content": preview.strip(),
                                "type": "message"
                            })
                        except: continue
                except Exception as e:
                    logger.warning(f"LinkedIn Message Scan error: {e}")

            await context.close()
            await playwright.stop()
            results["success"] = True
            return results

        except Exception as e:
            logger.error(f"LinkedIn Playwright Error: {e}")
            if context: await context.close()
            if playwright: await playwright.stop()
            return {"success": False, "error": str(e)}

    def _run_async_safe(self, coro):
        """Helper to run async code safely on Windows"""
        try:
            nest_asyncio.apply()
        except: pass

        if sys.platform == 'win32':
             try:
                 loop = asyncio.get_running_loop()
                 if 'SelectorEventLoop' in type(loop).__name__:
                     from concurrent.futures import ThreadPoolExecutor
                     def run_in_thread():
                        new_loop = asyncio.WindowsProactorEventLoop()
                        asyncio.set_event_loop(new_loop)
                        try:
                            return new_loop.run_until_complete(coro)
                        finally:
                            new_loop.close()
                     with ThreadPoolExecutor(max_workers=1) as executor:
                        return executor.submit(run_in_thread).result()
                 else:
                     return loop.run_until_complete(coro)
             except RuntimeError:
                 asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                 return asyncio.run(coro)
        else:
            try:
                loop = asyncio.get_running_loop()
                return loop.run_until_complete(coro)
            except RuntimeError:
                return asyncio.run(coro)

    def scrape_leads(self) -> Dict[str, Any]:
        """Scrape notifications and messages"""
        if not self.enabled: return {"success": False, "error": "LinkedIn integration is disabled"}
        return self._run_async_safe(self._scrape_data(scan_messages=True))

    def check_notifications(self) -> Dict[str, Any]:
        """Check notifications only"""
        # Kept for backward compatibility
        return self.scrape_leads()

    async def _post_update_async(self, content: str) -> Dict[str, Any]:
        """Post an update to LinkedIn (Async)"""
        playwright: Optional[Playwright] = None
        context: Optional[BrowserContext] = None
        
        try:
            playwright = await async_playwright().start()
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_dir,
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            # 1. Login Check (with auto-login fallback)
            logger.info("LinkedIn Skill: Checking login...")
            if "linkedin.com/feed" not in page.url:
                await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

            # Double check if we are really logged in
            if await page.locator('#global-nav').count() == 0:
                logger.info("LinkedIn Skill: Not logged in (no global-nav). Attempting login...")
                try:
                    if "login" not in page.url:
                        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
                    
                    await page.fill('#username', Config.LINKEDIN_EMAIL)
                    await page.fill('#password', Config.LINKEDIN_PASSWORD)
                    await page.click('button[type="submit"]')
                    await page.wait_for_selector('#global-nav', timeout=30000)
                except Exception as e:
                     logger.error(f"Login failed: {e}")
                     return {"success": False, "error": "Login failed"}

            # 2. Click Start a Post
            logger.info("LinkedIn Skill: Clicking 'Start a post'...")
            # Try finding the button by text first as it's most reliable across UI versions
            try:
                await page.get_by_text("Start a post").first.click(timeout=5000)
            except:
                # Fallback to selectors
                selectors = ['button.share-box-feed-entry__trigger', 'button[aria-label="Start a post"]']
                clicked = False
                for sel in selectors:
                    if await page.locator(sel).count() > 0:
                        await page.locator(sel).first.click()
                        clicked = True
                        break
                if not clicked:
                     return {"success": False, "error": "Could not find 'Start a post' button"}

            # 3. Type Content
            logger.info("LinkedIn Skill: Typing content...")
            # Wait for modal
            await page.wait_for_selector('.share-creation-state__text-editor', timeout=10000)
            
            # Focus and type
            await page.click('.share-creation-state__text-editor .ql-editor')
            await page.keyboard.type(content)
            await page.wait_for_timeout(2000)

            # 4. Click Post
            logger.info("LinkedIn Skill: Clicking 'Post'...")
            # The button usually has class share-actions__primary-action
            # And text "Post"
            
            post_btn = page.locator('button.share-actions__primary-action')
            if await post_btn.count() > 0 and await post_btn.is_enabled():
                await post_btn.click()
            else:
                # Try getting by text
                await page.get_by_text("Post", exact=True).click()
            
            await page.wait_for_timeout(5000) # Wait for post to process
            
            await context.close()
            await playwright.stop()
            return {"success": True}

        except Exception as e:
            logger.error(f"LinkedIn Post Error: {e}")
            if context: await context.close()
            if playwright: await playwright.stop()
            return {"success": False, "error": str(e)}

    def post_update(self, content: str) -> Dict[str, Any]:
        """Post an update (Sync wrapper)"""
        if not self.enabled: return {"success": False, "error": "LinkedIn integration is disabled"}
        return self._run_async_safe(self._post_update_async(content))
