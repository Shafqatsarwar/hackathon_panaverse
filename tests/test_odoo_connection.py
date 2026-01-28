"""
Odoo CRM Connection Test and Setup Helper
Tests Odoo connection and provides setup guidance
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.odoo_skill.odoo_skill import OdooSkill
from src.utils.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OdooTest")

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def main():
    print_section("Odoo CRM Connection Test")
    
    # Check configuration
    print("[1/4] Checking Odoo Configuration...")
    print(f"  ODOO_URL: {Config.ODOO_URL}")
    print(f"  ODOO_DB: {Config.ODOO_DB}")
    print(f"  ODOO_USERNAME: {Config.ODOO_USERNAME}")
    print(f"  ODOO_PASSWORD: {'*' * len(Config.ODOO_PASSWORD) if Config.ODOO_PASSWORD else '(not set)'}")
    
    # Check if configured
    if not all([Config.ODOO_URL, Config.ODOO_DB, Config.ODOO_USERNAME, Config.ODOO_PASSWORD]):
        print("\n[ERROR] Odoo is not fully configured!")
        print("\nTo configure Odoo, you have two options:")
        print("\nOption 1: Use Odoo.com (Free Trial)")
        print("  1. Go to https://www.odoo.com/trial")
        print("  2. Sign up for a free trial")
        print("  3. You'll get:")
        print("     - URL: https://yourcompany.odoo.com")
        print("     - Database: yourcompany")
        print("     - Username: your email")
        print("     - Password: your password")
        print("\nOption 2: Use Odoo.sh or Self-hosted")
        print("  1. Set up your own Odoo instance")
        print("  2. Get the connection details")
        print("\nThen update your .env file:")
        print("  ODOO_URL=https://yourcompany.odoo.com")
        print("  ODOO_DB=yourcompany")
        print("  ODOO_USERNAME=your_email@example.com")
        print("  ODOO_PASSWORD=your_password")
        return False
    
    # Test connection
    print("\n[2/4] Initializing Odoo Skill...")
    odoo = OdooSkill()
    
    if not odoo.enabled:
        print("[ERROR] Odoo skill is not enabled (missing configuration)")
        return False
    
    print("[3/4] Testing Authentication...")
    if odoo.authenticate():
        print(f"[SUCCESS] Connected to Odoo!")
        print(f"  User ID: {odoo.uid}")
        print(f"  Database: {odoo.db}")
        print(f"  URL: {odoo.url}")
        
        # Test creating a lead
        print("\n[4/4] Testing Lead Creation...")
        test_lead = odoo.create_lead(
            name="Test Lead - LinkedIn Connection",
            email_from="test.user@linkedin.com",
            description="This is a test lead created by the Panaversity Student Assistant.\nSource: LinkedIn\nTest connection successful!"
        )
        
        if test_lead.get('success'):
            print(f"[SUCCESS] Test lead created!")
            print(f"  Lead ID: {test_lead['id']}")
            
            # Get recent leads
            print("\nFetching recent leads...")
            recent_leads = odoo.get_leads(limit=5)
            
            if recent_leads:
                print(f"\nFound {len(recent_leads)} recent leads:")
                for lead in recent_leads:
                    print(f"  - {lead.get('name')} ({lead.get('email_from', 'No email')})")
            
            print("\n" + "="*70)
            print("  ODOO CONNECTION TEST: PASSED")
            print("="*70)
            return True
        else:
            print(f"[ERROR] Failed to create test lead: {test_lead.get('error')}")
            return False
    else:
        print("[ERROR] Authentication failed!")
        print("\nPossible issues:")
        print("  1. Invalid credentials")
        print("  2. Wrong URL or database name")
        print("  3. Network/firewall issues")
        print("  4. Odoo server is down")
        print("\nPlease verify your Odoo credentials and try again.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
