"""
AUTONOMOUS TEST 5: CHATBOT & MAIN AGENT
- Simple Query
- Tool usage (Gmail check)
- Web Search fallback
"""
import sys
import os
import logging
sys.path.insert(0, os.path.abspath('.'))

from agents.chat_agent import ChatAgent

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChatbotTest")

def test_chatbot():
    print("\n🧪 TESTING CHATBOT AGENT PROPERLY...")
    
    # 1. Initialize
    print("\n[1/3] Initializing ChatAgent...")
    try:
        agent = ChatAgent()
        print("   ✅ Initialization Successful")
    except Exception as e:
        print(f"   ❌ Initialization Error: {e}")
        return

    # 2. Simple Conversation
    print("\n[2/3] Testing Simple Query...")
    try:
        response = agent.chat("Hi, are you working autonomously?", user_id="test_user")
        
        if response.get('status') == 'success':
            print(f"   ✅ Response: {response.get('response')[:50]}...")
        else:
            print(f"   ❌ Chat Failed: {response.get('error')}")
            
    except Exception as e:
        print(f"   ❌ Chat Error: {e}")

    # 3. Tool Usage (Gmail)
    print("\n[3/3] Testing Tool Usage (Check Emails)...")
    try:
        # We ask something that triggers email check
        # We assume _check_email_tool is available to the model
        response = agent.chat("Check my latest emails for any updates.", user_id="test_user")
        
        text = response.get('response', '')
        # We check if the response mentions emails or indicates tool usage
        # Since we can't easily intercept the tool call in this integration test (unless we mock),
        # we check the response text.
        
        print(f"   ℹ️  Response: {text[:100]}...")
        
        if "email" in text.lower() or "checked" in text.lower():
            print("   ✅ Tool likely used (based on response context)")
        else:
            print("   ⚠️ Tool usage unclear from response")
            
    except Exception as e:
        print(f"   ❌ Tool Test Error: {e}")

if __name__ == "__main__":
    test_chatbot()
