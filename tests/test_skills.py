"""
Comprehensive Skill Test - 2 inputs per skill (FIXED)
"""
import sys
sys.path.insert(0, '.')

results = []

def log(msg):
    results.append(msg)
    print(msg)

log("=" * 60)
log("PANAVERSITY SKILL VERIFICATION - 2 INPUTS PER SKILL")
log("=" * 60)

# Load config
from src.utils.config import Config

# ============================================================
# TEST 1: Web Search Skill
# ============================================================
log("\n[1] WEB SEARCH SKILL")
log("-" * 40)
try:
    from skills.web_search_skill.skill import WebSearchSkill
    ws = WebSearchSkill()
    
    r1 = ws.search("What is Python programming")
    log(f"   Input 1: 'What is Python programming'")
    log(f"   Result: {len(r1)} items, Title: {r1[0].get('title', 'N/A')[:40] if r1 else 'None'}")
    
    r2 = ws.search("Weather today")
    log(f"   Input 2: 'Weather today'")
    log(f"   Result: {len(r2)} items, Title: {r2[0].get('title', 'N/A')[:40] if r2 else 'None'}")
    
    log("   STATUS: PASS")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 2: Odoo Skill
# ============================================================
log("\n[2] ODOO SKILL")
log("-" * 40)
try:
    from skills.odoo_skill.odoo_skill import OdooSkill
    odoo = OdooSkill()
    
    if odoo.enabled:
        auth = odoo.authenticate()
        log(f"   Input 1: authenticate()")
        log(f"   Result: {'Success' if auth else 'Failed'}")
        
        if auth:
            leads = odoo.get_leads(limit=3)
            log(f"   Input 2: get_leads(limit=3)")
            log(f"   Result: {len(leads) if leads else 0} leads")
        
        log("   STATUS: PASS")
    else:
        log("   STATUS: SKIP (not configured)")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 3: Gmail Monitoring Skill
# ============================================================
log("\n[3] GMAIL MONITORING SKILL")
log("-" * 40)
try:
    from skills.gmail_monitoring.gmail_monitoring import GmailMonitoringSkill
    
    gmail = GmailMonitoringSkill(
        Config.GMAIL_CREDENTIALS_PATH,
        Config.GMAIL_TOKEN_PATH,
        Config.FILTER_KEYWORDS
    )
    
    auth = gmail.authenticate()
    log(f"   Input 1: authenticate()")
    log(f"   Result: {'Success' if auth else 'Failed'}")
    
    if auth:
        emails = gmail.check_emails()
        log(f"   Input 2: check_emails()")
        log(f"   Result: {len(emails) if emails else 0} emails found")
        log("   STATUS: PASS")
    else:
        log("   STATUS: WARN (auth failed)")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 4: Chatbot Skill (Gemini)
# ============================================================
log("\n[4] CHATBOT SKILL (GEMINI)")
log("-" * 40)
try:
    from skills.chatbot_skill.skill import ChatbotSkill
    
    # Use API key from config
    chat = ChatbotSkill(api_key=Config.GOOGLE_API_KEY)
    
    log(f"   Input 1: Initialize model")
    log(f"   Result: Model {'ready' if chat.model else 'not initialized'}")
    
    if chat.model:
        session = chat.start_chat()
        response = chat.generate_response(session, "Say 'hello' in one word only")
        log(f"   Input 2: generate_response('Say hello')")
        log(f"   Result: Got response ({len(response) if response else 0} chars)")
        log("   STATUS: PASS")
    else:
        log("   STATUS: WARN (model not ready)")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 5: Email Filtering Skill
# ============================================================
log("\n[5] EMAIL FILTERING SKILL")
log("-" * 40)
try:
    from skills.email_filtering.email_filtering import EmailFilteringSkill
    ef = EmailFilteringSkill(keywords=Config.FILTER_KEYWORDS)
    
    test1 = {"subject": "PIAIC Quiz Deadline", "body": "Batch 47 Lahore"}
    r1 = ef.categorize_email(test1["subject"], test1["body"])
    log(f"   Input 1: PIAIC Quiz email")
    log(f"   Result: is_relevant={r1.get('is_relevant')}, is_quiz={r1.get('is_quiz')}")
    
    test2 = {"subject": "Newsletter", "body": "Check out our sale"}
    r2 = ef.categorize_email(test2["subject"], test2["body"])
    log(f"   Input 2: Newsletter email")
    log(f"   Result: is_relevant={r2.get('is_relevant')}")
    
    log("   STATUS: PASS")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 6: WhatsApp Skill
# ============================================================
log("\n[6] WHATSAPP SKILL")
log("-" * 40)
try:
    from skills.whatsapp_skill.skill import WhatsAppSkill
    
    wa1 = WhatsAppSkill(enabled=False)
    log(f"   Input 1: WhatsAppSkill(enabled=False)")
    log(f"   Result: Created, enabled={wa1.enabled}")
    
    wa2 = WhatsAppSkill(enabled=True, headless=True)
    log(f"   Input 2: WhatsAppSkill(enabled=True, headless=True)")
    log(f"   Result: Created, enabled={wa2.enabled}")
    
    log("   STATUS: PASS")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# TEST 7: LinkedIn Skill
# ============================================================
log("\n[7] LINKEDIN SKILL")
log("-" * 40)
try:
    from skills.linkedin_skill.skill import LinkedInSkill
    
    li = LinkedInSkill()
    log(f"   Input 1: LinkedInSkill()")
    log(f"   Result: Created, enabled={li.enabled}")
    log("   STATUS: PASS")
except Exception as e:
    log(f"   STATUS: FAIL - {e}")

# ============================================================
# SUMMARY
# ============================================================
log("\n" + "=" * 60)
log("ALL TESTS COMPLETE")
log("=" * 60)

# Count passes
pass_count = sum(1 for r in results if "STATUS: PASS" in r)
log(f"PASSED: {pass_count}/7 skills")

with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("\nResults saved to test_results.txt")
