"""
WhatsApp Integration Verification Script
Tests all integration points to ensure everything works correctly.
"""
import sys
import os
import logging
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WhatsAppVerification")

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_result(test_name, passed, details=""):
    """Print test result"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} - {test_name}")
    if details:
        print(f"    {details}")

async def main():
    print_section("WhatsApp Integration Verification")
    
    all_passed = True
    
    # Test 1: Import WhatsApp Skill
    print_section("Test 1: Import WhatsApp Skill")
    try:
        from skills.whatsapp_skill.skill import WhatsAppSkill
        print_result("Import WhatsAppSkill", True, "Module imported successfully")
    except Exception as e:
        print_result("Import WhatsAppSkill", False, f"Error: {e}")
        all_passed = False
        return
    
    # Test 2: Initialize Skill
    print_section("Test 2: Initialize Skill")
    try:
        skill = WhatsAppSkill(enabled=True, headless=True)
        print_result("Initialize skill", True, f"Session dir: {skill.session_dir}")
    except Exception as e:
        print_result("Initialize skill", False, f"Error: {e}")
        all_passed = False
        return
    
    # Test 3: Check Async Methods Exist
    print_section("Test 3: Check Async Methods")
    try:
        assert hasattr(skill, 'send_message_async'), "Missing send_message_async"
        assert hasattr(skill, 'check_messages_async'), "Missing check_messages_async"
        print_result("Async methods exist", True, "send_message_async, check_messages_async")
    except AssertionError as e:
        print_result("Async methods exist", False, str(e))
        all_passed = False
    
    # Test 4: Check Sync Methods Exist
    print_section("Test 4: Check Sync Methods")
    try:
        assert hasattr(skill, 'send_message'), "Missing send_message"
        assert hasattr(skill, 'check_messages'), "Missing check_messages"
        print_result("Sync methods exist", True, "send_message, check_messages")
    except AssertionError as e:
        print_result("Sync methods exist", False, str(e))
        all_passed = False
    
    # Test 5: Import MCP Server
    print_section("Test 5: Import MCP Server")
    try:
        from src.mcp_servers.whatsapp_server import WhatsAppMCPServer
        print_result("Import WhatsAppMCPServer", True, "Module imported successfully")
    except Exception as e:
        print_result("Import WhatsAppMCPServer", False, f"Error: {e}")
        all_passed = False
        return
    
    # Test 6: Initialize MCP Server
    print_section("Test 6: Initialize MCP Server")
    try:
        server = WhatsAppMCPServer()
        print_result("Initialize MCP server", True, f"Version: {server.version}")
    except Exception as e:
        print_result("Initialize MCP server", False, f"Error: {e}")
        all_passed = False
        return
    
    # Test 7: Check MCP Server Has Skill
    print_section("Test 7: Check MCP Server Integration")
    try:
        assert hasattr(server, 'skill'), "MCP server missing skill attribute"
        assert isinstance(server.skill, WhatsAppSkill), "MCP server skill is not WhatsAppSkill"
        print_result("MCP server has skill", True, "Real WhatsAppSkill instance found")
    except AssertionError as e:
        print_result("MCP server has skill", False, str(e))
        all_passed = False
    
    # Test 8: Check MCP Tools
    print_section("Test 8: Check MCP Tools")
    try:
        tools = server.list_tools()
        tool_names = [t['name'] for t in tools]
        assert 'send_message' in tool_names, "Missing send_message tool"
        assert 'check_messages' in tool_names, "Missing check_messages tool"
        assert 'check_status' in tool_names, "Missing check_status tool"
        print_result("MCP tools available", True, f"Tools: {', '.join(tool_names)}")
    except AssertionError as e:
        print_result("MCP tools available", False, str(e))
        all_passed = False
    
    # Test 9: Import WhatsApp Agent
    print_section("Test 9: Import WhatsApp Agent")
    try:
        from src.agents.whatsapp_agent import WhatsAppAgent
        agent = WhatsAppAgent()
        print_result("Import WhatsAppAgent", True, "Agent initialized")
    except Exception as e:
        print_result("Import WhatsAppAgent", False, f"Error: {e}")
        all_passed = False
    
    # Test 10: Check Configuration
    print_section("Test 10: Check Configuration")
    try:
        from src.utils.config import Config
        print_result("WhatsApp enabled", Config.WHATSAPP_ENABLED, 
                    f"WHATSAPP_ENABLED={Config.WHATSAPP_ENABLED}")
        print_result("Admin number set", bool(Config.ADMIN_WHATSAPP),
                    f"ADMIN_WHATSAPP={Config.ADMIN_WHATSAPP}")
        if not Config.WHATSAPP_ENABLED:
            print("\n[WARNING] WhatsApp is disabled in .env")
            print("    Set WHATSAPP_ENABLED=true to enable")
    except Exception as e:
        print_result("Check config", False, f"Error: {e}")
        all_passed = False
    
    # Test 11: Test Disabled Skill
    print_section("Test 11: Test Disabled Skill Behavior")
    try:
        disabled_skill = WhatsAppSkill(enabled=False)
        result = disabled_skill.send_message("+923001234567", "Test")
        assert result['success'] == False, "Disabled skill should return success=False"
        assert 'error' in result, "Disabled skill should return error"
        print_result("Disabled skill behavior", True, "Returns proper error when disabled")
    except Exception as e:
        print_result("Disabled skill behavior", False, f"Error: {e}")
        all_passed = False
    
    # Final Summary
    print_section("Verification Summary")
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED")
        print("\nWhatsApp integration is properly configured and ready to use!")
        print("\nNext steps:")
        print("1. Run: playwright install chromium")
        print("2. Run: python tests/verify_whatsapp.py (scan QR code)")
        print("3. Run: python tests/test_wa_send.py (send test message)")
    else:
        print("[ERROR] SOME TESTS FAILED")
        print("\nPlease review the errors above and fix the issues.")
        print("Check the documentation in WHATSAPP_QUICKSTART.md")
    
    print("\n" + "="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
