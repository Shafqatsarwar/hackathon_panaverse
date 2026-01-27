"""
WhatsApp Skill Implementation (Playwright Edition) - Stable V2.1
Uses browser automation to send and read messages via WhatsApp Web.
Optimized for Windows, robust session handling, and message scanning.
"""
import logging
import asyncio
import sys
import os
import time
from typing import Dict, Any, List, Optional
import nest_asyncio
from playwright.async_api import async_playwright, Page, BrowserContext, Playwright

# Configure Logging
logger = logging.getLogger(__name__)

class WhatsAppSkill:
    """
    Skill to handle WhatsApp interactions using Playwright.
    Robustly handles Windows EventLoop issues and Selector changes.
    """
    
    def __init__(self, enabled: bool = True, headless: bool = False, session_dir: str = "./whatsapp_session"):
        self.enabled = enabled
        self.headless = headless # If True, browser is hidden. Set False to see it work.
        self.session_dir = os.path.abspath(session_dir)
        
        # Ensure session directory exists or is created by Playwright
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir, exist_ok=True)

    async def _wait_for_login(self, page: Page) -> bool:
        """
        Waits for the user to be logged in. 
        Returns True if logged in, False if timeout.
        """
        logger.info("WhatsApp Skill: Waiting for login (QR Scan might be needed)...")
        try:
            # Wait for the main chat list wrapper or the side pane
            # [data-testid="chat-list"] is the standard
            await page.wait_for_selector('[data-testid="chat-list"], #pane-side, [data-icon="new-chat-outline"]', timeout=60000)
            logger.info("WhatsApp Skill: Login detected successfully.")
            return True
        except Exception:
            logger.error("WhatsApp Skill: Login timeout. You may need to scan the QR code.")
            return False

    async def _scan_messages(self, keywords: List[str] = None, check_archived: bool = True, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Scans for messages matching keywords, including in Archived.
        """
        playwright: Optional[Playwright] = None
        context: Optional[BrowserContext] = None
        messages_found = []

        try:
            playwright = await async_playwright().start()
            
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_dir,
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            if "web.whatsapp.com" not in page.url:
                 await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
            
            if not await self._wait_for_login(page):
                 await context.close()
                 await playwright.stop()
                 return [{"error": "Login timeout"}]

            logger.info("WhatsApp Skill: Logged in, starting scan...")
            
            # Helper to parse visible chats
            async def parse_chats():
                # Get all chat rows
                # Selector for chat row usually: div[role="row"] or similar inside chat-list
                rows = await page.locator('[data-testid="chat-list"] > div').all()
                results = []
                for row in rows[:limit]:
                    try:
                        # Get Title
                        title_el = row.locator('[dir="auto"][title]')
                        if not await title_el.count(): continue
                        title = await title_el.first.text_content()
                        
                        # Get Last Message preview (sometimes hidden, but usually visible)
                        # class usually contains 'message-in' or similar? No, in list it's just text.
                        # We use a broad selector for the second line
                        preview_el = row.locator('div[class*="_"] span[dir="auto"]').last
                        preview = await preview_el.text_content() if await preview_el.count() else ""
                        
                        # Check unread badge
                        unread_el = row.locator('[aria-label*="unread message"]')
                        unread_count = await unread_el.text_content() if await unread_el.count() else "0"
                        
                        chat_data = {
                            "title": title,
                            "last_message": preview,
                            "unread": unread_count
                        }

                        # Filter by keyword if provided
                        if keywords:
                            match = False
                            for k in keywords:
                                if k.lower() in title.lower() or k.lower() in preview.lower():
                                    match = True
                                    chat_data['matched_keyword'] = k
                                    break
                            if match:
                                results.append(chat_data)
                        else:
                            results.append(chat_data)
                            
                    except Exception as e:
                        continue # Skip buggy row
                return results

            # 1. Scan Main Chat List
            logger.info("WhatsApp Skill: Scanning main chat list...")
            main_chats = await parse_chats()
            messages_found.extend(main_chats)
            
            # 2. Check Archived (if requested)
            if check_archived:
                logger.info("WhatsApp Skill: Checking Archived folder...")
                # Search for "Archived" button. It's usually at the top of the chat list
                # Selector: [data-testid="archived"] or button with text "Archived"
                
                # Sometimes it is behind the "More" menu? 
                # Usually it is a persistent row at the top if there are archived chats.
                
                # Try simple click
                try:
                    archived_btn = page.locator('button[aria-label="Archived"], [data-testid="archived"]')
                    if await archived_btn.count() > 0 and await archived_btn.first.is_visible():
                        await archived_btn.first.click()
                        await page.wait_for_timeout(1000) # Wait for animation
                        
                        archived_chats = await parse_chats()
                        for c in archived_chats:
                            c['source'] = 'archived'
                        messages_found.extend(archived_chats)
                        
                        # Go back? (Click back button)
                        # [data-testid="back"], [data-icon="back"]
                        await page.locator('[data-icon="back"], [data-testid="back"]').first.click()
                        await page.wait_for_timeout(500)
                    else:
                        logger.info("No Archived button found (maybe no archived chats).")
                except Exception as e:
                    logger.warning(f"Failed to check archived: {e}")

            # Stay online for a bit if user requested "stable connection"
            # But we must return results.
            # We can't keep it open forever in this function.
            
            await context.close()
            await playwright.stop()
            
            return messages_found

        except Exception as e:
            logger.error(f"WhatsApp Scan Error: {e}")
            if context: await context.close()
            if playwright: await playwright.stop()
            return [{"error": str(e)}]

    async def _send_via_browser(self, number: str, message: str) -> Dict[str, Any]:
        """
        Internal async method to send message.
        """
        playwright: Optional[Playwright] = None
        context: Optional[BrowserContext] = None
        
        try:
            playwright = await async_playwright().start()
            
            # Use persistent context to keep login session
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_dir,
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            if "web.whatsapp.com" not in page.url:
                 await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
            
            is_logged_in = await self._wait_for_login(page)
            if not is_logged_in:
                await context.close()
                await playwright.stop()
                return {"success": False, "error": "Login timeout or QR Code not scanned."}

            clean_number = number.replace("+", "").replace(" ", "").replace("-", "")
            from urllib.parse import quote
            encoded_message = quote(message)
            
            send_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
            logger.info(f"WhatsApp Skill: Navigating to send message to {clean_number}...")
            
            await page.goto(send_url)
            
            try:
                # Wait for input box OR invalid number popup
                input_selector = 'footer div[contenteditable="true"]'
                
                start_time = time.time()
                found_input = False
                
                while time.time() - start_time < 30: 
                    if await page.locator('div[data-testid="popup-controls-ok"]').is_visible():
                        logger.warning("WhatsApp Skill: Invalid number detected.")
                        await context.close()
                        await playwright.stop()
                        return {"success": False, "error": "Invalid WhatsApp number."}
                    
                    if await page.locator(input_selector).is_visible():
                        found_input = True
                        break
                        
                    await asyncio.sleep(1)
                
                if not found_input:
                     raise TimeoutError("Chat input did not appear in time.")
                
                await page.locator(input_selector).focus()
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Enter")
                
                logger.info("WhatsApp Skill: Message submitted, waiting for network sync...")
                await page.wait_for_timeout(3000)
                
                logger.info("WhatsApp Skill: Message sent successfully.")
                await context.close()
                await playwright.stop()
                return {"success": True, "status": "sent"}

            except Exception as e:
                logger.error(f"WhatsApp Skill: Error during send flow: {e}")
                # Capture screenshot
                try:
                    await page.screenshot(path="whatsapp_error.png")
                except:
                    pass
                raise e

        except Exception as e:
            logger.error(f"WhatsApp Playwright Error: {e}")
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
                     # Need thread
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

    def send_message(self, number: str, message: str) -> Dict[str, Any]:
        """Send a message to a number"""
        if not self.enabled: return {"success": False, "error": "Disabled"}
        return self._run_async_safe(self._send_via_browser(number, message))

    def check_messages(self, keywords: List[str] = None, check_archived: bool = True) -> List[Dict[str, Any]]:
        """Check for messages matching keywords, optionally in archived"""
        if not self.enabled: return [{"error": "Disabled"}]
        return self._run_async_safe(self._scan_messages(keywords, check_archived))
