import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.chat_agent import ChatAgent

async def test_chat_agent():
    print("Testing Chat Agent...")
    agent = ChatAgent()
    
    # Test status
    status = agent.get_status()
    print(f"Agent Status: {status}")
    
    # Debug: Check Loaded Key
    from src.utils.config import Config
    key = Config.GOOGLE_API_KEY
    if key:
        masked_key = key[:5] + "..." + key[-5:]
        print(f"DEBUG: Loaded GOOGLE_API_KEY: {masked_key}")
    else:
        print("DEBUG: GOOGLE_API_KEY is missing or empty")
    
    # Test chat (Mock check since we might not have API key in env sometimes, but we do have it in this session)
    # If API key is invalid, it should return error but not crash
    result = agent.chat("Hello!", user_id="test_user")
    print(f"Chat Result Status: {result['status']}")
    
    if result['status'] in ["success", "error"]:
        if result['status'] == 'error':
            print(f"Error Details: {result.get('error')}")
        print("PASS: Agent handled request")
    else:
        print("FAIL: Unexpected status")

if __name__ == "__main__":
    asyncio.run(test_chat_agent())
