"""
Notification Agent - Uses Email Notification Skill
"""
import logging
from typing import Dict, Any
from skills.email_notifications.email_notifications import EmailNotificationSkill

logger = logging.getLogger(__name__)

class NotificationAgent:
    """Agent that handles notifications using skills"""
    
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
        # Initialize notification skill
        self.notification_skill = EmailNotificationSkill(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password=smtp_password
        )
    
    def send_email_alert(self, admin_email: str, email_data: Dict[str, Any]) -> bool:
        """Send email notification"""
        safe_subject = email_data.get('subject', '').encode('ascii', 'ignore').decode('ascii')
        logger.info(f"Notification Agent: Sending alert for '{safe_subject}'")
        
        success = self.notification_skill.notify_new_email(
            admin_email=admin_email,
            email_data=email_data
        )
        
        if success:
            logger.info("Notification Agent: Alert sent successfully")
        else:
            logger.error("Notification Agent: Failed to send alert")
        
        return success
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": "NotificationAgent",
            "smtp_configured": bool(self.notification_skill.smtp_password)
        }
