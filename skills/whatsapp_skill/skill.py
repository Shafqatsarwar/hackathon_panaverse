"""
WhatsApp Skill Implementation (Playwright Edition)
Uses browser automation to send messages via WhatsApp Web.
"""
import logging
import asyncio
from typing import Dict, Any
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class WhatsAppSkill:
    """Skill to handle WhatsApp interactions using Playwright"""
    
    def __init__(self, enabled: bool = True, headless: bool = False):
        self.enabled = enabled
        self.headless = headless # Set to False so user can scan QR code
        
    async def _send_via_browser(self, number: str, message: str) -> Dict[str, Any]:
        """Internal method to drive the browser with persistent context"""
        async with async_playwright() as p:
            try:
                # Use persistent context to save login session
                user_data_dir = "./whatsapp_session"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"] # Basic anti-detection
                )
                
                # Context already has a page, usually the first one
                page = context.pages[0] if context.pages else await context.new_page()
                
                logger.info("WhatsApp Skill: Loading WhatsApp Web...")
                await page.goto("https://web.whatsapp.com")
                
                # Wait for user to scan QR code (check for an element that exists only when logged in)
                # Looking for the chat list pane or similar
                logger.info("WhatsApp Skill: Checking login status...")
                try:
                    # If we have session, this selector should appear quickly. 
                    # If not, user needs to scan QR code.
                    # We wait longer here to allow manual QR scan on first run.
                    # Try multiple selectors for the main list
                    try:
                        await page.wait_for_selector("#pane-side", timeout=30000)
                    except:
                        # Fallback for newer versions
                        await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                        
                    logger.info("WhatsApp Skill: Logged in successfully!")
                except Exception:
                    logger.error("WhatsApp Skill: Login timeout. Please scan the QR code within 60s.")
                    await context.close()
                    return {"success": False, "error": "Login timeout or QR not scanned"}

                # Navigate/Search for contact
                clean_number = number.replace("+", "").replace(" ", "")
                send_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={message}"
                
                logger.info(f"WhatsApp Skill: Navigating to send URL for {clean_number}...")
                await page.goto(send_url)
                
                # Wait for "send" button to appear (the arrow icon)
                logger.info("WhatsApp Skill: Waiting to send...")
                
                # Check for input box
                inp_selector = 'div[contenteditable="true"][data-tab="10"]'
                try:
                     await page.wait_for_selector(inp_selector, timeout=20000)
                except:
                     # Fallback generic
                     inp_selector = 'footer div[contenteditable="true"]'
                     await page.wait_for_selector(inp_selector, timeout=20000)

                await page.locator(inp_selector).focus()
                # Type message instead of URL (URL sometimes fails on long msg) - wait, URL is already loaded
                # Just press enter
                await page.keyboard.press("Enter")
                
                # Wait a bit for send to register
                await page.wait_for_timeout(5000)
                
                logger.info("WhatsApp Skill: Message sent!")
                
                # We close the context, but the session is saved to disk
                await context.close()
                return {"success": True, "status": "sent_via_playwright"}
                
            except Exception as e:
                logger.error(f"WhatsApp Playwright Error: {e}")
                # Ensure context closes even on error if it exists
                # (Complex in this snippet, but 'async with' handles 'p' closure)
                return {"success": False, "error": str(e)}

    async def _read_via_browser(self, keywords: list = None, limit: int = 5) -> list:
        """Internal method to read unread messages via browser"""
        async with async_playwright() as p:
            try:
                # Use persistent context
                user_data_dir = "./whatsapp_session"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                page = context.pages[0] if context.pages else await context.new_page()
                await page.goto("https://web.whatsapp.com")
                
                # Check login
                try:
                    await page.wait_for_selector('[data-testid="chat-list"]', timeout=45000)
                except:
                    logger.error("WhatsApp Skill: Login failed/QR not scanned.")
                    await context.close()
                    return [{"error": "Login required. Please scan QR code."}]

                logger.info("WhatsApp Skill: Scanning for unread messages...")
                
                # Look for unread badges
                unread_chats = await page.locator('[aria-label*="unread message"]').all()
                
                messages = []
                count = 0
                
                for chat in unread_chats:
                    if count >= limit: break
                    
                    try:
                        # Click the chat to read it
                        await chat.click()
                        await page.wait_for_timeout(1000) # Wait for load
                        
                        # Get chat title
                        header_title = await page.locator('header [dir="auto"][title]').first.text_content()
                        
                        # Get last few messages
                        msg_elements = await page.locator('.message-in').all()
                        last_msgs = msg_elements[-3:] if len(msg_elements) > 3 else msg_elements
                        
                        chat_content = ""
                        for msg in last_msgs:
                             text = await msg.text_content()
                             chat_content += text + "\n"
                        
                        # Filter by keywords if provided
                        found_keywords = []
                        if keywords:
                            found_keywords = [k for k in keywords if k.lower() in chat_content.lower() or k.lower() in header_title.lower()]
                            if not found_keywords:
                                continue # Skip if no keywords found
                        
                        messages.append({
                            "sender": header_title,
                            "content": chat_content.strip(),
                            "matched_keywords": found_keywords
                        })
                        count += 1
                        
                    except Exception as e:
                        logger.error(f"Error reading chat: {e}")
                        continue
                
                await context.close()
                return messages
                
            except Exception as e:
                logger.error(f"WhatsApp Reading Error: {e}")
                return [{"error": str(e)}]

    def _run_async(self, coro):
        """Helper to run async code safely"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
            
        if loop and loop.is_running():
            # We are in a loop, use create_task/ensure_future?
            # No, if we need the result synchronously, we must use a thread-safe wrapper or failed design.
            # But the simplest hack for sync-calling-async inside loop is to install nest_asyncio if possible
            # OR just return a Future? No, the caller expects a result.
            
            # Use nest_asyncio approach manually or import it.
            import nest_asyncio
            nest_asyncio.apply()
            return asyncio.run(coro)
        else:
            return asyncio.run(coro)

    def check_unread_messages(self, keywords: list = None, limit: int = 5) -> list:
        """Check for unread messages matching keywords"""
        if not self.enabled:
            return [{"error": "WhatsApp disabled"}]
            
        return self._run_async(self._read_via_browser(keywords, limit))

    def send_message(self, number: str, message: str) -> Dict[str, Any]:
        """Send a message to a number"""
        if not self.enabled:
            logger.warning("WhatsApp skill is disabled")
            return {"success": False, "error": "Disabled"}
            
        logger.info(f"WhatsApp Skill: Initializing browser for {number}...")
        try:
            return self._run_async(self._send_via_browser(number, message))
        except Exception as e:
            logger.error(f"WhatsApp Async Execution Error: {e}")
            return {"success": False, "error": str(e)}
