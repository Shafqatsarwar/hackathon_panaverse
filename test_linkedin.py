import asyncio
import os
import logging
from skills.linkedin_skill.skill import LinkedInSkill

logging.basicConfig(level=logging.INFO)

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def test():
    skill = LinkedInSkill(headless=True)
    try:
        res = skill.check_notifications()
        if res.get("success"):
            print(f"STATUS: Connected! Notifications: {len(res.get('notifications', []))}")
        else:
            print(f"STATUS: Disconnected - {res.get('error')}")
        print(f"Raw: {res}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test())
