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
        Uses a combined selector for efficiency (Playwright OR logic).
        """
        logger.info("WhatsApp Skill: Waiting for login (QR Scan might be needed)...")
        
        # Combined selector: Check for Chat List OR Pane Side OR New Chat Button
        # This matches verify_whatsapp.py logic which was successful
        login_selector = '#pane-side, [data-testid="chat-list"], div[aria-label="Chat list"], canvas'
        
        try:
            logger.info(f"WhatsApp Skill: Checking login with robust selector...")
            # Wait up to 60s
            await page.wait_for_selector(login_selector, timeout=60000, state='visible')
            logger.info("WhatsApp Skill: Login detected successfully!")
            return True
            
        except Exception as e:
            logger.warning(f"WhatsApp Skill: Login check timed out or failed: {e}")
            try:
                await page.screenshot(path="whatsapp_login_fail.png")
            except: 
                pass
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
                ]
                # user_agent removed to match verify_whatsapp.py default
            )
            
            page = self._context.pages[0] if self._context.pages else await self._context.new_page()
            
            if "web.whatsapp.com" not in page.url:
                # Increased timeout to 60 seconds
                await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)
            
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
        Supports Phone Number (+123...) OR Name ("Sir Junaid").
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled"}
        
        page = await self._init_browser()
        if not page:
            return {"success": False, "error": "Failed to initialize browser or login"}
        
        try:
            is_number = number.replace("+", "").replace("-", "").strip().isdigit()
            
            if is_number:
                # Direct Navigation for Numbers
                clean_number = number.replace("+", "").replace(" ", "").replace("-", "")
                from urllib.parse import quote
                encoded_message = quote(message)
                send_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
                logger.info(f"WhatsApp Skill: Navigating to send message to {clean_number}...")
                await page.goto(send_url)
            else:
                # SMART SEARCH for Names
                logger.info(f"WhatsApp Skill: Searching for contact/group '{number}'...")
                
                # 1. Click Search
                search_selectors = [
                    'div[contenteditable="true"][data-tab="3"]',
                    'div[aria-label="Search"]',
                    'div[title="Search input textbox"]',
                    'button[aria-label="Search or start new chat"]'
                ]
                
                search_box = None
                for sel in search_selectors:
                    if await page.locator(sel).count() > 0:
                        search_box = page.locator(sel).first
                        break
                        
                if not search_box:
                    # Fallback: Just type '/' to focus search usually? Or 'Ctrl+F' logic?
                    # Let's try locating by placeholder text
                    search_box = page.get_by_placeholder("Search", exact=False).first
                
                if search_box:
                    await search_box.click()
                    await page.wait_for_timeout(500)
                    await page.keyboard.type(number)
                    await page.wait_for_timeout(3000) # Wait for results
                    
                    # 2. Select Result (Avoiding Meta AI)
                    logger.info("WhatsApp Skill: analyzing search results...")
                    
                    # Get all rows in the results pane
                    pane = page.locator('#pane-side') # The scrolling list container
                    rows = pane.locator('div[role="row"]')
                    
                    found_contact = False
                    count = await rows.count()
                    
                    for i in range(count):
                        row = rows.nth(i)
                        text = await row.text_content()
                        
                        # SKIP Meta AI or "Ask Meta AI" or "Search for..."
                        if "Meta AI" in text or "Ask Meta AI" in text:
                            continue
                            
                        # If it matches our search largely, click it
                        # Or simply click the first NON-Meta result
                        logger.info(f"WhatsApp Skill: Clicking result: {text[:30]}...")
                        await row.click()
                        found_contact = True
                        break
                        
                    if not found_contact:
                        # Fallback: Try strict title match if fuzzy failed
                        logger.warning("WhatsApp Skill: No valid contact found in results. Trying strict match...")
                        strict_sel = f'span[title="{number}"]'
                        if await page.locator(strict_sel).count() > 0:
                            await page.locator(strict_sel).first.click()
                        else:
                            return {"success": False, "error": f"Contact '{number}' not found (and avoided Meta AI)."}
                else:
                    return {"success": False, "error": "Could not find search box"}

            # Wait for input box to appear (confirming chat open)
            input_selector = 'footer div[contenteditable="true"]'
            start_time = time.time()
            found_input = False
            
            while time.time() - start_time < 30:
                # Check for invalid number popup (only for phone numbers)
                if is_number and await page.locator('div[data-testid="popup-controls-ok"]').is_visible():
                    logger.warning("WhatsApp Skill: Invalid number detected.")
                    await self._cleanup()
                    return {"success": False, "error": "Invalid WhatsApp number."}
                
                if await page.locator(input_selector).is_visible():
                    found_input = True
                    break
                await asyncio.sleep(1)
            
            if not found_input:
                raise TimeoutError("Chat input did not appear in time (Contact not found?).")
            
            # Focus and send
            await page.locator(input_selector).focus()
            
            # If we used search, we still need to type the message
            if not is_number:
                for line in message.split('\n'):
                    await page.keyboard.type(line)
                    await page.keyboard.down("Shift")
                    await page.keyboard.press("Enter")
                    await page.keyboard.up("Shift")
            else:
                # Message is already in box from URL, just needs focus?
                # Sometimes URL navigation pre-fills but doesn't send.
                # Actually, URL param pre-fills it.
                pass
                
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            
            logger.info("WhatsApp Skill: Message submitted.")
            await page.wait_for_timeout(3000)
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
    ) -> Dict[str, Any]:
        """
        Check WhatsApp messages (async version).
        Robust Archived folder logic using text-based locators.
        """
        if not self.enabled:
            return {"success": False, "error": "WhatsApp skill is disabled", "messages": []}
        
        page = await self._init_browser()
        if not page:
            return {"success": False, "error": "Failed to initialize browser or login", "messages": []}
        
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
                            # Sometimes title doesn't have [title] attr, just text
                            title_el = row.locator('div._ak8q span') # Generic class fallback? Risky.
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

            # 1. Check Archived (PRIORITY)
            if check_archived:
                logger.info("WhatsApp Skill: Checking Archived folder (PRIORITY)...")
                try:
                    # ROBUST STRATEGY: Look for text "Archived" specifically
                    # This finds the Archived row/button regardless of CSS classes
                    archived_btn = page.get_by_text("Archived", exact=True).first
                    
                    if await archived_btn.is_visible():
                        logger.info("WhatsApp Skill: Found 'Archived' text, clicking...")
                        await archived_btn.click()
                        await page.wait_for_timeout(1000)
                        
                        archived_chats = await parse_chats()
                        for c in archived_chats:
                            c['source'] = 'archived'
                        messages_found.extend(archived_chats)
                        
                        # Go back
                        back_btn = page.locator('[data-icon="back"], button[aria-label="Back"]')
                        if await back_btn.count() > 0:
                            await back_btn.first.click()
                        else:
                            # If back button not found, try reloading to root
                            await page.goto("https://web.whatsapp.com")
                            await page.wait_for_timeout(2000)
                    else:
                        logger.warning("WhatsApp Skill: 'Archived' text not visible.")
                        
                except Exception as e:
                    logger.warning(f"WhatsApp Skill: Archived check failed: {e}")

            # 2. Scan Main Chat List
            logger.info("WhatsApp Skill: Scanning main chat list...")
            main_chats = await parse_chats()
            messages_found.extend(main_chats)
            
            return {"success": True, "messages": messages_found, "count": len(messages_found)}
            
        except Exception as e:
            logger.error(f"WhatsApp Scan Error: {e}")
            return {"success": False, "error": str(e), "messages": []}
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
