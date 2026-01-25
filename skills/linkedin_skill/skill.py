"""
LinkedIn Skill Implementation (Playwright)
"""
import logging
import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class LinkedInSkill:
    """Skill to handle LinkedIn interactions using Playwright"""
    
    def __init__(self, enabled: bool = True, headless: bool = False):
        self.enabled = enabled
        self.headless = headless 
        
    async def _check_via_browser(self, limit: int = 5) -> List[str]:
        """Internal method to check notifications via browser"""
        async with async_playwright() as p:
            try:
                # Use persistent context to save login session
                user_data_dir = "./linkedin_session"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                
                logger.info("LinkedIn Skill: Loading LinkedIn...")
                await page.goto("https://www.linkedin.com/notifications/")
                
                # Check login
                try:
                    # If we are logged in, we should see the nav bar or notifications
                    await page.wait_for_selector('.authentication-outlet', state='hidden', timeout=5000) 
                    # Alternative: check for a known element like the search bar or nav
                    await page.wait_for_selector('#global-nav', timeout=30000)
                except:
                    logger.error("LinkedIn Skill: Login required.")
                    await context.close()
                    return ["Error: Login required. Please log in to LinkedIn in the opening browser manually once."]

                logger.info("LinkedIn Skill: Scraping notifications...")
                
                # Wait for notifications to load
                # Selectors change often, look for generic article/card structure in notifications page
                try:
                    await page.wait_for_selector('div.nt-card-content', timeout=10000)
                    cards = await page.locator('div.nt-card-content').all()
                except:
                     return ["No notifications found or selector changed."]
                
                notifications = []
                count = 0
                for card in cards:
                    if count >= limit: break
                    text = await card.text_content()
                    clean_text = " ".join(text.split()) # Remove extra whitespace
                    notifications.append(clean_text)
                    count += 1
                
                await context.close()
                return notifications
                
            except Exception as e:
                logger.error(f"LinkedIn Playwright Error: {e}")
                return [f"Error: {str(e)}"]
        
    def post_update(self, content: str) -> Dict[str, Any]:
        """Post a status update (Not fully implemented for safety, returning placeholder)"""
        if not self.enabled:
             return {"success": False, "error": "Disabled"}
        return {"success": True, "message": "Posting not fully automated yet for safety."}
        
    def _run_async(self, coro):
        """Helper to run async code safely, especially on Windows with Playwright"""
        import sys
        
        try:
            loop = asyncio.get_running_loop()
            is_running = True
        except RuntimeError:
            loop = None
            is_running = False

        if sys.platform == 'win32':
            needs_new_loop = False
            if is_running:
                # Type name check is robust across different asyncio versions/implementations
                if type(loop).__name__ == 'SelectorEventLoop':
                    needs_new_loop = True

            if needs_new_loop:
                logger.info("LinkedIn Skill: Running in separate thread to support ProactorEventLoop")
                from concurrent.futures import ThreadPoolExecutor
                
                def _threaded_run(c):
                    # Set up a new Proactor loop for this thread
                    new_loop = asyncio.WindowsProactorEventLoop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(c)
                    finally:
                        new_loop.close()
                
                with ThreadPoolExecutor(max_workers=1) as executor:
                    return executor.submit(_threaded_run, coro).result()

        if is_running:
            import nest_asyncio
            nest_asyncio.apply(loop)
            return loop.run_until_complete(coro)
        else:
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            return asyncio.run(coro)

    def check_notifications(self) -> Dict[str, Any]:
        """Check notifications"""
        if not self.enabled:
            return {"success": False, "notifications": []}
            
        logger.info("LinkedIn Skill: Checking notifications...")
        try:
             results = self._run_async(self._check_via_browser())
             return {"success": True, "notifications": results}
        except Exception as e:
             logger.error(f"LinkedIn Async Error: {e}")
             return {"success": False, "error": f"LinkedIn execution failed: {str(e) or type(e).__name__}"}
