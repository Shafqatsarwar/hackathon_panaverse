"""
Deep Dive Verification for WhatsApp Skill V3.
Tests the Robust Text-Locator logic for Archived and Smart Search.
"""
import asyncio
import logging
from skills.whatsapp_skill.skill import WhatsAppSkill

# Configure logging to show us details
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def test_deep_dive():
    print("="*60)
    print("WHATSAPP SKILL V3 - DEEP DIVE TEST")
    print("="*60)
    
    skill = WhatsAppSkill(headless=False)
    
    # Test 1: Archived Folder Scan
    print("\n[TEST 1] Scanning Archived Folder (using 'Archived' text locator)...")
    try:
        messages = await skill.check_messages_async(
            keywords=None, # Get ALL to verify visibility
            check_archived=True,
            limit=10
        )
        
        print(f"\n> Found {len(messages)} chats total.")
        archived_count = sum(1 for m in messages if m.get('source') == 'archived')
        print(f"> Archived chats found: {archived_count}")
        
        for msg in messages:
            if msg.get('source') == 'archived':
                print(f"  - [ARCHIVED] {msg['title']} (Unread: {msg['unread']})")
                
    except Exception as e:
        print(f"❌ Test 1 Failed: {e}")

    # Test 2: Smart Search (Dry Run)
    print("\n[TEST 2] Verifying Smart Search UI (Searching 'Panaverse')...")
    # We won't send a message, just verify we can search and find a result.
    # This uses internal methods to "peek".
    try:
        page = await skill._init_browser()
        if page:
            # Locate search
            search_box = page.get_by_placeholder("Search", exact=False).first
            if await search_box.count() > 0:
                print("✅ Smart Search Box LOCATED.")
                await search_box.click()
                await page.keyboard.type("Panaverse")
                await asyncio.sleep(2)
                print("✅ Typed 'Panaverse'. Checking results...")
                
                # Check if results appeared
                pane = page.locator('#pane-side') # Result list container
                if await pane.count() > 0:
                     print("✅ Search Results visible.")
                else:
                     print("⚠️ Search Results pane not standard.")
            else:
                 print("❌ Smart Search Box NOT found.")
            
            await skill._cleanup()
            
    except Exception as e:
        print(f"❌ Test 2 Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_deep_dive())
