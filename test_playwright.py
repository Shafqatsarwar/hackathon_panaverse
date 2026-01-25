import asyncio
from playwright.async_api import async_playwright
import os

async def test():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            print("Chromium launched successfully!")
            await browser.close()
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
