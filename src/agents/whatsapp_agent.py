"""
WhatsApp Agent
"""
import logging
from typing import Dict, Any
from skills.whatsapp_skill.skill import WhatsAppSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class WhatsAppAgent:
    """Agent for WhatsApp communication"""
    
    def __init__(self):
        self.skill = WhatsAppSkill(enabled=Config.WHATSAPP_ENABLED)
        
    def send_alert(self, message: str) -> Dict[str, Any]:
        """Send an alert to the admin"""
        admin_number = Config.ADMIN_WHATSAPP
        return self.skill.send_message(admin_number, message)
        
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "WhatsAppAgent",
            "enabled": self.skill.enabled
        }
