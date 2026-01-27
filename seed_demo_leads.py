"""
Seed Demo Leads into Odoo
"""
import sys
import os
sys.path.append(os.getcwd())

from skills.odoo_skill.odoo_skill import OdooSkill
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SeedDemoLeads")

DEMO_LEADS = [
    {"name": "Panaversity Inquiry - Ali Ahmed", "email": "ali.ahmed@example.com", "desc": "Interested in Cloud Computing course."},
    {"name": "PIAIC Follow-up - Sara Khan", "email": "sara.khan@email.pk", "desc": "Wants schedule for Batch 47."},
    {"name": "Website Visitor - John Doe", "email": "john.doe@mail.com", "desc": "Asked about GenAI certification."},
    {"name": "UMT Student Referral - Ayesha", "email": "ayesha@umt.edu.pk", "desc": "Referred by friend. Interested in agentic AI."},
    {"name": "LinkedIn Lead - Usman Tech", "email": "usman@techcorp.io", "desc": "Saw LinkedIn post. Inquiring about enrollment."},
]

def main():
    odoo = OdooSkill()
    if not odoo.authenticate():
        logger.error("Odoo authentication failed. Check your .env credentials.")
        return
    
    logger.info(f"Seeding {len(DEMO_LEADS)} demo leads into Odoo...")
    success_count = 0
    
    for lead in DEMO_LEADS:
        result = odoo.create_lead(
            name=lead["name"],
            email_from=lead["email"],
            description=lead["desc"]
        )
        if result.get("success"):
            logger.info(f"  ✅ Created: {lead['name']} (ID: {result.get('id')})")
            success_count += 1
        else:
            logger.error(f"  ❌ Failed: {lead['name']} - {result.get('error')}")
    
    logger.info(f"\n--- Done! {success_count}/{len(DEMO_LEADS)} leads created. ---")

if __name__ == "__main__":
    main()
