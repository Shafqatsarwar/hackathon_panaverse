"""
LinkedIn Agent
"""
import logging
from typing import Dict, Any
from skills.linkedin_skill.skill import LinkedInSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class LinkedInAgent:
    """Agent for LinkedIn interaction"""
    
    def __init__(self):
        self.skill = LinkedInSkill(enabled=Config.LINKEDIN_ENABLED)
        
    def post_update(self, message: str) -> Dict[str, Any]:
        """Post a status update"""
        return self.skill.post_update(message)
    
    def check_notifications(self) -> Dict[str, Any]:
        """
        Check for notifications.
        Returns:
             Dict containing 'notifications' (List[str]) and 'success' (bool)
        """
        return self.skill.check_notifications()
        
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "LinkedInAgent",
            "enabled": self.skill.enabled
        }
