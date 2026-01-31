
import logging
import socket
import xmlrpc.client
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OdooDiag")

def check_socket(host, port):
    logger.info(f"Checking connectivity to {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            logger.info("SUCCESS: Socket is OPEN.")
            return True
        else:
            logger.error(f"FAILURE: Socket is CLOSED (Error code: {result})")
            return False
    except Exception as e:
        logger.error(f"FAILURE: Exception during check: {e}")
        return False

def check_xmlrpc(url, db, username, password):
    logger.info(f"Checking XML-RPC authentication at {url}...")
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        version = common.version()
        logger.info(f"Server Version: {version}")
        
        uid = common.authenticate(db, username, password, {})
        if uid:
             logger.info(f"SUCCESS: Authentication Successful! UID: {uid}")
        else:
             logger.error("FAILURE: Authentication Failed (Invalid Credentials)")
    except Exception as e:
        logger.error(f"FAILURE: XML-RPC Error: {e}")

if __name__ == "__main__":
    # Parse URL
    url = Config.ODOO_URL
    # Remove http:// to get host
    host = url.replace("http://", "").replace("https://", "").split(":")[0]
    port = 8069
    if ":" in url.split("//")[-1]:
        port = int(url.split(":")[-1])
        
    if check_socket(host, port):
        check_xmlrpc(Config.ODOO_URL, Config.ODOO_DB, Config.ODOO_USERNAME, Config.ODOO_PASSWORD)
    else:
        logger.warning("\nIf Odoo is running, ensure it is binding to 0.0.0.0 or localhost, and the port is correct.")
