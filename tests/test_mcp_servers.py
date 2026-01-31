
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from mcp.whatsapp_server import WhatsAppMCPServer
from mcp.gmail_server import GmailMCPServer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestMCP")

def test_whatsapp_mcp():
    logger.info("--- Testing WhatsApp MCP Server ---")
    server = WhatsAppMCPServer()
    target_number = os.getenv("WHATSAPP_FORWARD_MESSAGES", "+46764305834")
    
    # Sending 3 messages
    for i in range(1, 4):
        msg = f"Test Message MCP {i}/3 - Verification"
        logger.info(f"Calling Tool send_message: {msg}")
        try:
            result = server.call_tool("send_message", {"number": target_number, "message": msg})
            logger.info(f"Result: {result}")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed MCP call {i}: {e}")

def test_gmail_mcp():
    logger.info("--- Testing Gmail MCP Server ---")
    server = GmailMCPServer()
    target_email = os.getenv("EMAIL_FORWARD_EMAIL", "khansarwar1@hotmail.com")
    
    # Sending 3 emails
    for i in range(1, 4):
        subject = f"Test Email MCP {i}/3"
        body = f"This is a verification email {i}/3 sent via GmailMCPServer tool."
        logger.info(f"Calling Tool send_notification: {subject}")
        try:
            result = server.call_tool("send_notification", {"subject": subject, "body": body})
            logger.info(f"Result: {result}")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Failed MCP call {i}: {e}")

if __name__ == "__main__":
    test_whatsapp_mcp()
    test_gmail_mcp()
