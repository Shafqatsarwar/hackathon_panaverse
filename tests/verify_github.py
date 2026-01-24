import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.github_agent import GitHubAgent

def test_github_agent():
    print("Testing GitHub Agent...")
    agent = GitHubAgent()
    
    # Test status
    status = agent.get_status()
    print(f"Agent Status: {status}")
    
    # Test checking updates
    result = agent.check_updates()
    print(f"Check Result: {result}")
    
    if result.get("success") or result.get("error") == "Disabled" or "GITHUB_TOKEN" in result.get("error", ""):
        print("PASS: Agent handled request gracefully")
    else:
        print("FAIL: Unexpected response")

if __name__ == "__main__":
    test_github_agent()
