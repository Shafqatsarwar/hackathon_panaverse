"""
WhatsApp Skill Implementation (Playwright Edition) - V3.0 ASYNC REFACTOR
Uses browser automation to send and read messages via WhatsApp Web.
Fully async implementation with proper Windows event loop handling.
"""
import logging
import asyncio
import sys
import os
import time
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Page, BrowserContext, Playwright

# Configure Logging
logger = logging.getLogger(__name__)

class WhatsAppSkill:
    """
    Skill to handle WhatsApp interactions using Playwright.
    V3.0: Fully async, no sync wrappers, clean architecture.
    """
    
    def __init__(self, enabled: bool = True, headless: bool = False, session_dir: str = "./whatsapp_session"):
        self.enabled = enabled
        self.headless = headless
        self.session_dir = os.path.abspath(session_dir)
        
        # Ensure session directory exists
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir, exist_ok=True)
        
        # Playwright instances (managed per operation)
        self._playwright: Optional[Playwright] = None
        self._context: Optional[BrowserContext] = None

    async def _wait_for_login(self, page: Page) -> bool:
        """
        Waits for the user to be logged in. 
        Returns True if logged in, False if timeout.
        """
        logger.info("WhatsApp Skill: Waiting for login (QR Scan might be needed)...")
        try:
            # Wait for the main chat list wrapper
            await page.wait_for_selector(
                '[data-testid="chat-list"], #pane-side, [data-icon="new-chat-outline"]', 
                timeout=60000
            )
            logger.info("WhatsApp Skill: Login detected successfully.")
            return True
        except Exception as e:
            logger.error(f"WhatsApp Skill: Login timeout: {e}")
            return False

    async def _init_browser(self) -> Optional[Page]:
        """Initialize browser and return page, or None if failed"""
        try:
            self._playwright = await async_playwright().start()
            
            self._context = await self._playwright.chromium.launch_persistent_context(
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
            
            page = self._context.pages[0] if self._context.pages else await self._context.new_page()
            
            if "web.whatsapp.com" not in page.url:
                await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
            
            if not await self._wait_for_login(page):
                await self._cleanup()
                return None
                
            return page
            
        except Exception as e:
            logger.error(f"WhatsApp Skill: Browser init error: {e}")
            await self._cleanup()
            return None

    async def _cleanup(self):
        """Clean up browser resources"""
        try:
            if self._context:
                await self._context.close()
            if self._playwright:
                await self._playwright.stop()
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")
        finally:
            self._context = None
            self._playwright = None

    async def send_message_async(self, number: str, message: str) -> Dict[str, Any]:
        """
        Send a WhatsApp message (async version).
        This is the primary async interface.
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled"}
        
        page = await self._init_browser()
        if not page:
            return {"success": False, "error": "Failed to initialize browser or login"}
        
        try:
            clean_number = number.replace("+", "").replace(" ", "").replace("-", "")
            from urllib.parse import quote
            encoded_message = quote(message)
            
            send_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
            logger.info(f"WhatsApp Skill: Navigating to send message to {clean_number}...")
            
            await page.goto(send_url)
            
            # Wait for input box OR invalid number popup
            input_selector = 'footer div[contenteditable="true"]'
            
            start_time = time.time()
            found_input = False
            
            while time.time() - start_time < 30:
                # Check for invalid number popup
                if await page.locator('div[data-testid="popup-controls-ok"]').is_visible():
                    logger.warning("WhatsApp Skill: Invalid number detected.")
                    await self._cleanup()
                    return {"success": False, "error": "Invalid WhatsApp number."}
                
                # Check for input box
                if await page.locator(input_selector).is_visible():
                    found_input = True
                    break
                    
                await asyncio.sleep(1)
            
            if not found_input:
                raise TimeoutError("Chat input did not appear in time.")
            
            # Focus and send
            await page.locator(input_selector).focus()
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            
            logger.info("WhatsApp Skill: Message submitted, waiting for network sync...")
            await page.wait_for_timeout(3000)
            
            logger.info("WhatsApp Skill: Message sent successfully.")
            return {"success": True, "status": "sent"}
            
        except Exception as e:
            logger.error(f"WhatsApp Skill: Send error: {e}")
            try:
                await page.screenshot(path="whatsapp_error.png")
            except:
                pass
            return {"success": False, "error": str(e)}
        finally:
            await self._cleanup()

    async def check_messages_async(
        self, 
        keywords: List[str] = None, 
        check_archived: bool = True, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Check WhatsApp messages (async version).
        This is the primary async interface.
        """
        if not self.enabled:
            return [{"error": "WhatsApp skill is disabled"}]
        
        page = await self._init_browser()
        if not page:
            return [{"error": "Failed to initialize browser or login"}]
        
        messages_found = []
        
        try:
            logger.info("WhatsApp Skill: Logged in, starting scan...")
            
            # Helper to parse visible chats
            async def parse_chats():
                rows = await page.locator('div[role="row"]').all()
                results = []
                for row in rows[:limit]:
                    try:
                        # Get Title
                        title_el = row.locator('[dir="auto"][title]')
                        if not await title_el.count():
                            continue
                        title = await title_el.first.text_content()
                        
                        # Get Last Message preview
                        preview_el = row.locator('span[dir="auto"]').last
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
                        continue  # Skip buggy row
                return results

            # 1. Scan Main Chat List
            logger.info("WhatsApp Skill: Scanning main chat list...")
            main_chats = await parse_chats()
            messages_found.extend(main_chats)
            
            # 2. Check Archived (if requested)
            if check_archived:
                logger.info("WhatsApp Skill: Checking Archived folder...")
                try:
                    archived_btn = page.locator('button[aria-label="Archived"], [data-testid="archived"]')
                    if await archived_btn.count() > 0 and await archived_btn.first.is_visible():
                        await archived_btn.first.click()
                        await page.wait_for_timeout(1000)
                        
                        archived_chats = await parse_chats()
                        for c in archived_chats:
                            c['source'] = 'archived'
                        messages_found.extend(archived_chats)
                        
                        # Go back
                        await page.locator('[data-icon="back"], [data-testid="back"]').first.click()
                        await page.wait_for_timeout(500)
                    else:
                        logger.info("No Archived button found (maybe no archived chats).")
                except Exception as e:
                    logger.warning(f"Failed to check archived: {e}")
            
            return messages_found
            
        except Exception as e:
            logger.error(f"WhatsApp Scan Error: {e}")
            return [{"error": str(e)}]
        finally:
            await self._cleanup()

    # ========================================
    # SYNC WRAPPERS (for backward compatibility)
    # ========================================
    
    def send_message(self, number: str, message: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for send_message_async.
        Use this from non-async code.
        """
        return self._run_async(self.send_message_async(number, message))
    
    def check_messages(
        self, 
        keywords: List[str] = None, 
        check_archived: bool = True, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for check_messages_async.
        Use this from non-async code.
        """
        return self._run_async(self.check_messages_async(keywords, check_archived, limit))
    
    def _run_async(self, coro):
        """
        Helper to run async code from sync context.
        Handles Windows event loop properly.
        """
        if sys.platform == 'win32':
            # Set Windows-specific event loop policy
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        try:
            # Try to get existing loop
            loop = asyncio.get_running_loop()
            # If we're already in an async context, we can't use asyncio.run()
            # This should not happen with proper architecture, but handle it
            logger.warning("WhatsApp Skill: Called sync method from async context. Use async methods instead!")
            # Create new loop in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        except RuntimeError:
            # No running loop, we can use asyncio.run()
            return asyncio.run(coro)


if __name__ == '__main__':
    # Test Block
    print('Testing WhatsApp Skill V3.0...')
    skill = WhatsAppSkill(headless=False)
    
    print('Test 1: Sending message...')
    result = skill.send_message('+923244279017', 'Test from WhatsApp Skill V3.0 🚀')
    print(f'Send result: {result}')
    
    print('\nTest 2: Checking messages...')
    msgs = skill.check_messages(keywords=['Test', 'Panaverse'])
    print(f'Found {len(msgs)} messages: {msgs}')
