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
                    await page.wait_for_selector("#pane-side", timeout=60000) 
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
                await page.wait_for_selector('div[contenteditable="true"]', timeout=30000)
                await page.locator('div[contenteditable="true"]').focus()
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

    def send_message(self, number: str, message: str) -> Dict[str, Any]:
        """Send a message to a number"""
        if not self.enabled:
            logger.warning("WhatsApp skill is disabled")
            return {"success": False, "error": "Disabled"}
            
        logger.info(f"WhatsApp Skill: Initializing browser for {number}...")
        
        # Run async code synchronously for the synchronous interface
        try:
            return asyncio.run(self._send_via_browser(number, message))
        except Exception as e:
            logger.error(f"WhatsApp Async Execution Error: {e}")
            return {"success": False, "error": str(e)}
