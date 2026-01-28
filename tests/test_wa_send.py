
import logging
import sys
import os
import json

# Adjust path
sys.path.append(os.getcwd())

from skills.whatsapp_skill.skill import WhatsAppSkill

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestWhatsApp")

def run_test():
    logger.info("--- Starting WhatsApp Test Message ---")
    
    # Use environment variable or hardcoded for test
    # The user posted phone numbers earlier in environment: 
    # NEXT_PUBLIC_PHONE_PK="+923244279017"
    # We will use this number.
    
    target_number = "+923244279017"
    message = "Hello! This is a test message from your autonomous AI employee. 🤖"
    
    # Headless=False to see it happening
    wa_skill = WhatsAppSkill(enabled=True, headless=False)
    
    logger.info(f"Sending message to {target_number}...")
    result = wa_skill.send_message(target_number, message)
    
    logger.info(f"Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    run_test()
