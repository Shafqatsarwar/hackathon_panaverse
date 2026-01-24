import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.whatsapp_agent import WhatsAppAgent

def test_whatsapp_agent():
    print("Testing WhatsApp Agent...")
    agent = WhatsAppAgent()
    
    # Test status
    status = agent.get_status()
    print(f"Agent Status: {status}")
    
    # Test sending alert (should be skipped if disabled, or mock sent)
    result = agent.send_alert("Test message from Verification")
    print(f"Send Result: {result}")
    
    if result.get("success") or result.get("error") == "Disabled" or "WhatsApp integration is disabled" in result.get("error", ""):
        print("PASS: Agent handled request gracefully")
    else:
        print("FAIL: Unexpected response")

if __name__ == "__main__":
    test_whatsapp_agent()
