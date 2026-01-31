
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.chat_agent import ChatAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyFix")

def test_tool_signature():
    logger.info("Verifying ChatAgent._check_whatsapp_tool signature...")
    
    # Initialize minimal agent (without real skills if possible, or just catch init errors)
    # ChatAgent __init__ loads many things. We might need to mock if it's too heavy/fails.
    # But usually it just initializes objects.
    
    try:
        agent = ChatAgent()
        logger.info("ChatAgent initialized.")
        
        # Test calling the tool with 'query' argument
        try:
            # We don't care if the actual logic fails (e.g. auth), just that the call signature is accepted
            # "query" is the extra arg that was causing TypeError
            result = agent._check_whatsapp_tool(query="test query", check_archived=True)
            logger.info(f"Tool call success (signature valid). Result: {result}")
        except TypeError as te:
            logger.error(f"FAIL: TypeError still persists: {te}")
        except Exception as e:
            logger.info(f"Tool called successfully (signature valid), specific error: {e}")
            
    except Exception as e:
        logger.error(f"Agent init failed: {e}")

if __name__ == "__main__":
    test_tool_signature()
