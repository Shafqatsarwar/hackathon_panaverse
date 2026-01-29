import sys
import os
import asyncio
import logging
sys.path.append(os.getcwd())
from skills.whatsapp_skill.skill import WhatsAppSkill

logging.basicConfig(level=logging.INFO)

CONTACT = "Sir Junaid PIAIC"
MESSAGE = """Hello Sir Junaid, this is the Panaversity Student Assistant.
We need help with Playwright and the new WhatsApp skills to run 24/7.
The 24/7 deployment is failing to detect archived folders reliably.
Could you please guide us? Thanks!"""

async def send_help():
    skill = WhatsAppSkill(headless=False)
    print(f"Sending message to '{CONTACT}' using Smart Search...")
    
    # reliable wait for browser
    try:
        res = await skill.send_message_async(CONTACT, MESSAGE)
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_help())
