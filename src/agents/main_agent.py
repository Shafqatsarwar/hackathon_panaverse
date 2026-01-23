"""
Main Orchestrator Agent - Coordinates Email and Notification Agents
"""
import logging
import schedule
import time
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from src.utils.config import Config
from src.agents.email_agent import EmailAgent
from src.agents.notification_agent import NotificationAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('panaversity_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MainAgent:
    """Main orchestrator coordinating all sub-agents"""
    
    def __init__(self):
        self.config = Config
        self.email_agent = None
        self.notification_agent = None
        self.running = False
        self.chat_history_dir = Path("chat_history")
        self.chat_history_dir.mkdir(exist_ok=True)
        
        # Validate configuration
        errors = self.config.validate()
        if errors:
            logger.error("Configuration errors:")
            for error in errors:
                logger.error(f"  - {error}")
            raise ValueError("Invalid configuration")
    
    def initialize(self):
        """Initialize all agents"""
        logger.info("Main Agent: Initializing Panaversity Student Assistant...")
        
        self.config.print_config()
        
        # Initialize Email Agent
        self.email_agent = EmailAgent(
            credentials_path=self.config.GMAIL_CREDENTIALS_PATH,
            token_path=self.config.GMAIL_TOKEN_PATH,
            filter_keywords=self.config.FILTER_KEYWORDS
        )
        
        if not self.email_agent.authenticate():
            raise Exception("Failed to authenticate Email Agent")
        
        logger.info("Main Agent: Email Agent initialized")
        
        # Initialize Notification Agent
        self.notification_agent = NotificationAgent(
            smtp_server=self.config.SMTP_SERVER,
            smtp_port=self.config.SMTP_PORT,
            smtp_username=self.config.SMTP_USERNAME,
            smtp_password=self.config.SMTP_PASSWORD
        )
        
        logger.info("Main Agent: Notification Agent initialized")
        logger.info("Main Agent: Initialization complete!")
    
    def check_emails(self):
        """Execute email check task"""
        logger.info("=" * 60)
        logger.info("Main Agent: Running email check task...")
        
        try:
            # Get relevant emails from Email Agent
            relevant_emails = self.email_agent.check_emails()
            
            if not relevant_emails:
                logger.info("Main Agent: No new relevant emails")
                self._log_to_chat_history("email_check", {
                    "status": "completed",
                    "emails_found": 0
                })
                return
            
            logger.info(f"Main Agent: Processing {len(relevant_emails)} email(s)")
            
            # Send notifications via Notification Agent
            for email in relevant_emails:
                logger.info(f"Main Agent: Processing '{email['subject']}'")
                
                success = self.notification_agent.send_email_alert(
                    admin_email=self.config.ADMIN_EMAIL,
                    email_data=email
                )
                
                if success:
                    logger.info(f"✓ Notification sent for: {email['subject']}")
                else:
                    logger.error(f"✗ Failed to send notification for: {email['subject']}")
            
            # Log to chat history
            self._log_to_chat_history("email_check", {
                "status": "completed",
                "emails_found": len(relevant_emails),
                "emails": [{"subject": e['subject'], "priority": e.get('priority')} for e in relevant_emails]
            })
        
        except Exception as e:
            logger.error(f"Main Agent: Error during email check: {str(e)}")
            self._log_to_chat_history("email_check", {
                "status": "error",
                "error": str(e)
            })
        
        logger.info("Main Agent: Email check task complete")
        logger.info("=" * 60)
    
    def _log_to_chat_history(self, task_name: str, data: Dict[str, Any]):
        """Log task execution to chat history"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "task": task_name,
            "data": data
        }
        
        # Create daily log file
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.chat_history_dir / f"{date_str}.json"
        
        # Append to log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def schedule_tasks(self):
        """Schedule periodic tasks"""
        logger.info("Main Agent: Scheduling periodic tasks...")
        
        schedule.every(self.config.EMAIL_CHECK_INTERVAL).minutes.do(self.check_emails)
        logger.info(f"Main Agent: Email checks scheduled every {self.config.EMAIL_CHECK_INTERVAL} minutes")
    
    def start(self):
        """Start the assistant in background mode"""
        logger.info("Main Agent: Starting Panaversity Student Assistant...")
        
        self.initialize()
        self.schedule_tasks()
        
        # Run initial check
        logger.info("Main Agent: Running initial email check...")
        self.check_emails()
        
        # Start scheduled loop
        self.running = True
        logger.info("Main Agent: Assistant is now running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Main Agent: Stopping assistant...")
            self.running = False
    
    def run_manual_check(self):
        """Run a single manual email check"""
        logger.info("Main Agent: Running manual email check...")
        self.initialize()
        self.check_emails()
        logger.info("Main Agent: Manual check complete!")
    
    def status(self):
        """Show current status"""
        logger.info("Main Agent: Status Report")
        logger.info("=" * 50)
        logger.info(f"Running: {self.running}")
        
        if self.email_agent:
            email_status = self.email_agent.get_status()
            logger.info(f"Email Agent: {email_status}")
        
        if self.notification_agent:
            notif_status = self.notification_agent.get_status()
            logger.info(f"Notification Agent: {notif_status}")
        
        logger.info("=" * 50)
