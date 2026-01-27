
import logging
import sys
import os
import xmlrpc.client

# Adjust path
sys.path.append(os.getcwd())
from src.utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OdooTest")

def test_odoo():
    logger.info("--- Testing Odoo Connection ---")
    
    url = Config.ODOO_URL
    db = Config.ODOO_DB
    username = Config.ODOO_USERNAME
    # Do not log password
    
    logger.info(f"URL: {url}")
    logger.info(f"DB: {db}")
    logger.info(f"User: {username}")
    
    if not all([url, db, username, Config.ODOO_PASSWORD]):
        logger.error("FAIL: Missing Odoo credentials in .env")
        return

    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        version = common.version()
        logger.info(f"Server Version: {version}")
        
        uid = common.authenticate(db, username, Config.ODOO_PASSWORD, {})
        if uid:
            logger.info(f"SUCCESS: Authenticated as UID {uid}")
            
            # Try to read clean leads count
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            count = models.execute_kw(db, uid, Config.ODOO_PASSWORD, 'crm.lead', 'search_count', [[]])
            logger.info(f"Total Leads in DB: {count}")
            
        else:
            logger.error("FAIL: Authentication failed (check password/db)")
            
    except Exception as e:
        logger.error(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_odoo()
