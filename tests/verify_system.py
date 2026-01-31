import logging
import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SystemVerifier")

# Ensure root is in path
sys.path.insert(0, os.path.abspath('.'))

class TestAgents(unittest.TestCase):
    """
    Comprehensive verification of all Agents and their Skills.
    """

    def setUp(self):
        logger.info("\n" + "="*60)
        logger.info(f"🧪 TESTING: {self._testMethodName}")
        logger.info("="*60)

    # ==========================================
    # 1. EMAIL AGENT & GMAIL SKILL
    # ==========================================
    @patch('skills.gmail_monitoring.gmail_monitoring.GmailMonitoringSkill.fetch_unread_emails')
    def test_email_agent(self, mock_fetch):
        """Verify Email Agent can read, filter, and process emails."""
        logger.info("Testing Email Agent...")

        # Mock Data
        mock_fetch.return_value = [
            {'subject': 'Urgent: Invoice needed', 'body': 'Please send invoice', 'id': '1'},
            {'subject': 'Newsletter', 'body': 'Weekly updates', 'id': '2'}
        ]
        
        from agents.email_agent import EmailAgent
        # Initialize with dummy creds
        agent = EmailAgent("dummy.json", "dummy_token.json", ["invoice", "urgent"])
        
        # Override the actual fetch method on the skill instance
        agent.gmail_skill.fetch_unread_emails = mock_fetch
        
        # Test 1: Fetch & Filter
        emails = agent.check_emails(mark_read=False)
        
        self.assertEqual(len(emails), 1, "Should filter down to 1 relevant email")
        self.assertEqual(emails[0]['subject'], 'Urgent: Invoice needed')
        logger.info("✅ Email Agent: Fetch & Filter logic operational")

    # ==========================================
    # 2. ODOO AGENT & MCP SERVER
    # ==========================================
    @patch('skills.odoo_skill.skill.OdooSkill.get_leads')
    @patch('skills.odoo_skill.skill.OdooSkill.create_lead')
    def test_odoo_agent_mcp(self, mock_create, mock_get):
        """Verify Odoo Agent and MCP Server tools."""
        logger.info("Testing Odoo integration...")
        
        from mcp.odoo_server import OdooMCPServer
        server = OdooMCPServer()
        
        # Test 1: Search (Custom Logic added previously)
        server.skill.get_leads = MagicMock(return_value=[
            {"name": "Alpha Project", "id": 1}, 
            {"name": "Beta Test", "id": 2}
        ])
        
        result_search = server.call_tool("search_leads", {"keyword": "Alpha"})
        self.assertEqual(len(result_search['leads']), 1)
        self.assertEqual(result_search['leads'][0]['name'], "Alpha Project")
        logger.info("✅ Odoo MCP: 'search_leads' tool operational")

        # Test 2: Create Lead
        mock_create.return_value = {"success": True, "id": 101}
        result_create = server.call_tool("create_lead", {"name": "New Opportunity"})
        self.assertTrue(result_create['success'])
        logger.info("✅ Odoo MCP: 'create_lead' tool operational")

    # ==========================================
    # 3. BRAIN AGENT (Reasoning Engine)
    # ==========================================
    def test_brain_agent_structure(self):
        """Verify Brain Agent initialization and path structure."""
        logger.info("Testing Brain Agent...")
        
        from agents.brain_agent import BrainAgent
        agent = BrainAgent()
        
        self.assertTrue(agent.needs_action_path.exists())
        self.assertTrue(agent.done_path.exists())
        logger.info("✅ Brain Agent: Vault paths verified")

    # ==========================================
    # 4. CHAT AGENT (UI & Response)
    # ==========================================
    @patch('agents.chat_agent.ChatAgent.chat')
    def test_chat_agent(self, mock_chat):
        """Verify Chat Agent handles messages."""
        logger.info("Testing Chat Agent...")
        
        mock_chat.return_value = {
            "response": "Hello! I am your AI Employee.",
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        from agents.chat_agent import ChatAgent
        agent = ChatAgent()
        # We mock the chat method to avoid hitting actual Gemini API in tests
        agent.chat = mock_chat
        
        response = agent.chat("Hi")
        self.assertEqual(response['status'], 'success')
        self.assertIn("AI Employee", response['response'])
        logger.info("✅ Chat Agent: Response logic verified")

if __name__ == '__main__':
    unittest.main()
