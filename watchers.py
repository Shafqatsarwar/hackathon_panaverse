
import asyncio
import logging
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Import Skills
from skills.whatsapp_skill.skill import WhatsAppSkill
from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
from src.utils.config import Config

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('watchers.log')
    ]
)
logger = logging.getLogger("Watchers")

class WatcherOrchestrator:
    """
    The 'Senses' of the Digital FTE.
    Polls data and writes .md files to /Needs_Action for the Brain to process.
    """
    def __init__(self):
        self.vault_path = Path("data/vault")
        self.needs_action = self.vault_path / "Needs_Action"
        self.inbox = self.vault_path / "Inbox"
        
        # Ensure dirs
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
        
        # Init Skills
        self.whatsapp_skill = WhatsAppSkill(enabled=Config.WHATSAPP_ENABLED, headless=True)
        self.gmail_skill = GmailMonitoringSkill(
            Config.GMAIL_CREDENTIALS_PATH, 
            Config.GMAIL_TOKEN_PATH,
            Config.FILTER_KEYWORDS
        )
        self.gmail_authenticated = False
        
        # Tracker to avoid duplicates
        self.processed_ids = set()
        
        # Track last check times
        self.last_email_check = 0
        self.last_whatsapp_check = 0

    def initialize(self):
        if self.gmail_skill.authenticate():
            self.gmail_authenticated = True
            logger.info("Watcher: Gmail Active.")
        else:
            logger.warning("Watcher: Gmail Failed.")

    def create_markdown_task(self, source_type: str, data: dict, identifier: str):
        """Create a standard Markdown task file"""
        if identifier in self.processed_ids:
            return

        timestamp = datetime.now().isoformat()
        safe_id = "".join([c for c in identifier if c.isalnum()])[:50]
        filename = f"{source_type.upper()}_{safe_id}_{int(time.time())}.md"
        filepath = self.needs_action / filename
        
        content = f"""---
type: {source_type}
source: {data.get('sender', 'Unknown')}
received: {timestamp}
status: pending
priority: {'high' if 'urgent' in str(data).lower() else 'normal'}
---

## Content
{data.get('body') or data.get('snippet') or data.get('last_message') or ''}

## Context
Full Data: {json.dumps(data, indent=2)}

## Suggested Actions
- [ ] Analyze content
- [ ] Draft reply
- [ ] Log to Odoo
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info(f"Watcher: Created Task {filename}")
        self.processed_ids.add(identifier)

    async def _poll_whatsapp(self):
        """Poll WhatsApp for new messages matching keywords"""
        if not self.whatsapp_skill.enabled:
            return
        
        logger.info("Watcher: Scanning WhatsApp...")
        keywords = Config.FILTER_KEYWORDS + ["Panaversity", "Panaverse", "PIAIC", "Urgent", "Help"]
        
        try:
            # Use the async interface directly (V3.0)
            msgs = await self.whatsapp_skill.check_messages_async(keywords=keywords, limit=20)
            
            if msgs and isinstance(msgs, list) and len(msgs) > 0 and ("error" not in msgs[0]):
                for msg in msgs:
                    if "error" in msg:
                        continue
                    
                    # Unique ID: Sender + part of content
                    uid = f"{msg.get('title')}_{str(msg.get('last_message'))[:20]}"
                    self.create_markdown_task("whatsapp", msg, uid)
                    
                    # Auto-forward to email if configured
                    if Config.EMAIL_FORWARD_EMAIL:
                        try:
                            from src.agents.notification_agent import NotificationAgent
                            notif_agent = NotificationAgent()
                            
                            subject = f"WhatsApp: {msg.get('title', 'Unknown')}"
                            body = f"""
New WhatsApp message matching your keywords:

From: {msg.get('title', 'Unknown')}
Message: {msg.get('last_message', 'No content')}
Unread Count: {msg.get('unread', '0')}

Keywords matched: {', '.join(Config.FILTER_KEYWORDS)}
"""
                            notif_agent.send_email(
                                to_email=Config.EMAIL_FORWARD_EMAIL,
                                subject=subject,
                                body=body
                            )
                            logger.info(f"Watcher: Forwarded WhatsApp message to email {Config.EMAIL_FORWARD_EMAIL}")
                        except Exception as e:
                            logger.error(f"Watcher: Failed to forward WhatsApp message to email: {e}")
                    
                    # Auto-forward to WhatsApp if configured
                    if Config.WHATSAPP_FORWARD_MESSAGES and Config.ADMIN_WHATSAPP:
                        try:
                            forward_msg = f"""🔔 New Message Alert

From: {msg.get('title', 'Unknown')}
Message: {msg.get('last_message', 'No content')}

Keywords: {', '.join(Config.FILTER_KEYWORDS[:3])}"""
                            
                            result = await self.whatsapp_skill.send_message_async(
                                number=Config.ADMIN_WHATSAPP,
                                message=forward_msg
                            )
                            if result.get("success"):
                                logger.info(f"Watcher: Forwarded WhatsApp message to {Config.ADMIN_WHATSAPP}")
                            else:
                                logger.error(f"Watcher: Failed to forward to WhatsApp: {result.get('error')}")
                        except Exception as e:
                            logger.error(f"Watcher: Failed to forward WhatsApp message to WhatsApp: {e}")
            else:
                logger.info("Watcher: No WhatsApp messages found matching keywords")
        except Exception as e:
            logger.error(f"Watcher: WhatsApp polling error: {e}")

    async def _poll_gmail(self):
        if not self.gmail_authenticated: return
        
        logger.info("Watcher: Scanning Gmail...")
        loop = asyncio.get_running_loop()
        emails = await loop.run_in_executor(None, self.gmail_skill.check_emails)
        
        if emails:
            for email in emails:
                self.create_markdown_task("email", email, email.get('id'))
                
                # Auto-forward to email if configured
                if Config.EMAIL_FORWARD_EMAIL:
                    try:
                        from src.agents.notification_agent import NotificationAgent
                        notif_agent = NotificationAgent()
                        
                        subject = f"Gmail Forward: {email.get('subject', 'No Subject')}"
                        body = f"""
New Gmail message matching your keywords:

From: {email.get('from', 'Unknown')}
Subject: {email.get('subject', 'No Subject')}
Priority: {email.get('priority', 'Normal')}
Snippet: {email.get('snippet', 'No preview available')}

Keywords matched: {', '.join(Config.FILTER_KEYWORDS)}
"""
                        notif_agent.send_email(
                            to_email=Config.EMAIL_FORWARD_EMAIL,
                            subject=subject,
                            body=body
                        )
                        logger.info(f"Watcher: Forwarded Gmail message to email {Config.EMAIL_FORWARD_EMAIL}")
                    except Exception as e:
                        logger.error(f"Watcher: Failed to forward Gmail message to email: {e}")
                
                # Auto-forward to WhatsApp if configured
                if Config.WHATSAPP_FORWARD_MESSAGES and Config.ADMIN_WHATSAPP:
                    try:
                        forward_msg = f"""📧 New Email Alert

From: {email.get('from', 'Unknown')}
Subject: {email.get('subject', 'No Subject')}
Priority: {email.get('priority', 'Normal')}

Keywords: {', '.join(Config.FILTER_KEYWORDS[:3])}"""
                        
                        result = await self.whatsapp_skill.send_message_async(
                            number=Config.ADMIN_WHATSAPP,
                            message=forward_msg
                        )
                        if result.get("success"):
                            logger.info(f"Watcher: Forwarded Gmail message to WhatsApp {Config.ADMIN_WHATSAPP}")
                        else:
                            logger.error(f"Watcher: Failed to forward Gmail to WhatsApp: {result.get('error')}")
                    except Exception as e:
                        logger.error(f"Watcher: Failed to forward Gmail message to WhatsApp: {e}")

    async def start(self):
        self.initialize()
        logger.info(f"Watcher: Online. Writing to {self.needs_action}")
        logger.info(f"Email check interval: {Config.EMAIL_CHECK_INTERVAL} minutes")
        logger.info(f"WhatsApp check interval: {Config.WHATSAPP_CHECK_INTERVAL} minutes")
        
        while True:
            current_time = time.time()
            
            # Check email based on EMAIL_CHECK_INTERVAL
            if current_time - self.last_email_check >= (Config.EMAIL_CHECK_INTERVAL * 60):
                logger.info("Watcher: Email check interval reached")
                await self._poll_gmail()
                self.last_email_check = current_time
            
            # Check WhatsApp based on WHATSAPP_CHECK_INTERVAL
            if current_time - self.last_whatsapp_check >= (Config.WHATSAPP_CHECK_INTERVAL * 60):
                logger.info("Watcher: WhatsApp check interval reached")
                await self._poll_whatsapp()
                self.last_whatsapp_check = current_time
            
            # Sleep for 1 minute before checking again
            await asyncio.sleep(60)

if __name__ == "__main__":
    watcher = WatcherOrchestrator()
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(watcher.start())
    except KeyboardInterrupt:
        pass
