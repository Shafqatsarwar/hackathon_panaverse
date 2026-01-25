import asyncio
import os
import sys
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)

# Set policy for Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from skills.whatsapp_skill.skill import WhatsAppSkill

async def test_whatapp():
    print("Testing WhatsApp Skill...")
    skill = WhatsAppSkill(headless=True)
    try:
        results = skill.check_unread_messages(keywords=["Panaversity"], limit=1)
        if results and isinstance(results[0], dict) and "error" in results[0]:
            print(f"STATUS: Disconnected - {results[0]['error']}")
        else:
            print(f"STATUS: Connected! Found {len(results)} messages.")
        print(f"Raw Results: {results}")
    except Exception as e:
        print(f"FAILED with exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # Simulate a running loop to test _run_async's detection logic
    async def wrapper():
        await test_whatapp()
        
    asyncio.run(wrapper())
