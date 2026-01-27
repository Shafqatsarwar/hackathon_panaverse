
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
        if not self.whatsapp_skill.enabled: return
        
        logger.info("Watcher: Scanning WhatsApp...")
        keywords = Config.FILTER_KEYWORDS + ["Panaversity", "Panaverse", "PIAIC", "Urgent", "Help"]
        
        loop = asyncio.get_running_loop()
        msgs = await loop.run_in_executor(None, self.whatsapp_skill.check_messages, keywords)
        
        if msgs and isinstance(msgs, list) and len(msgs) > 0 and ("error" not in msgs[0]):
            for msg in msgs:
                if "error" in msg: continue
                # Unique ID: Sender + part of content
                uid = f"{msg.get('title')}_{str(msg.get('last_message'))[:20]}"
                self.create_markdown_task("whatsapp", msg, uid)

    async def _poll_gmail(self):
        if not self.gmail_authenticated: return
        
        logger.info("Watcher: Scanning Gmail...")
        loop = asyncio.get_running_loop()
        emails = await loop.run_in_executor(None, self.gmail_skill.check_emails)
        
        if emails:
            for email in emails:
                self.create_markdown_task("email", email, email.get('id'))

    async def start(self, interval=60):
        self.initialize()
        logger.info(f"Watcher: Online. Writing to {self.needs_action}")
        
        while True:
            await self._poll_whatsapp()
            await self._poll_gmail()
            await asyncio.sleep(interval)

if __name__ == "__main__":
    watcher = WatcherOrchestrator()
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(watcher.start(60))
    except KeyboardInterrupt:
        pass
