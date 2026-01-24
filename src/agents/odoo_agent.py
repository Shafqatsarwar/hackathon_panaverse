"""
Odoo Agent
"""
import logging
from typing import Dict, Any
from skills.odoo_skill.odoo_skill import OdooSkill
from src.utils.config import Config

logger = logging.getLogger(__name__)

class OdooAgent:
    """Agent for Odoo ERP interaction"""
    
    def __init__(self):
        self.skill = OdooSkill()
        self.enabled = self.skill.enabled
        
    def create_lead_from_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a CRM lead from an email"""
        if not self.enabled:
            return {"success": False, "error": "Odoo disabled"}
            
        subject = email_data.get("subject", "No Subject")
        sender = email_data.get("sender", "Unknown")
        body = email_data.get("body", "")
        
        description = f"Generated from Email.\nSender: {sender}\n\nBody:\n{body}"
        
        logger.info(f"OdooAgent: Creating Lead for '{subject}'...")
    def get_recent_leads_summary(self) -> str:
        """Get a text summary of recent leads for the chatbot"""
        if not self.enabled:
            return "Odoo Integration is disabled."
            
        leads = self.skill.get_leads(limit=5)
        if not leads:
            return "No recent leads found in Odoo."
            
        summary = "Recent Odoo CRM Leads:\n"
        for lead in leads:
            name = lead.get('name', 'N/A')
            contact = lead.get('contact_name') or lead.get('email_from') or 'Unknown'
            # stage_id is usually [id, "Stage Name"]
            stage = lead.get('stage_id')
            stage_name = stage[1] if stage and isinstance(stage, list) and len(stage) > 1 else "Unknown"
            
            summary += f"- '{name}' from {contact} (Stage: {stage_name})\n"
            
        return summary
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "OdooAgent",
            "enabled": self.enabled,
            "url": Config.ODOO_URL
        }
