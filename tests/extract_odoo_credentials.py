"""
Extract Odoo API credentials from Excel file and update .env
"""
import sys
import os
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_odoo_credentials():
    """Extract Odoo credentials from Excel file"""
    
    excel_path = r"D:\Panavers\Projects\hackathon_panaverse\public\User API Key (res.users.apikeys).xlsx"
    
    print("="*70)
    print("  Odoo API Key Extractor")
    print("="*70)
    print(f"\nReading: {excel_path}")
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        
        print(f"\nFound {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print("\nData preview:")
        print(df.to_string())
        
        # Extract credentials
        print("\n" + "="*70)
        print("  Extracted Odoo Credentials")
        print("="*70)
        
        # Try to find relevant columns
        for col in df.columns:
            print(f"\n{col}:")
            print(f"  {df[col].iloc[0] if len(df) > 0 else 'N/A'}")
        
        # Look for common Odoo fields
        odoo_info = {}
        
        # Common field names in Odoo API key exports
        field_mappings = {
            'url': ['url', 'server', 'host', 'odoo_url'],
            'database': ['database', 'db', 'db_name'],
            'username': ['username', 'user', 'login', 'email'],
            'api_key': ['api_key', 'key', 'token', 'access_key'],
            'password': ['password', 'pwd']
        }
        
        for key, possible_names in field_mappings.items():
            for col in df.columns:
                if any(name.lower() in col.lower() for name in possible_names):
                    if len(df) > 0:
                        odoo_info[key] = df[col].iloc[0]
        
        if odoo_info:
            print("\n" + "="*70)
            print("  Suggested .env Configuration")
            print("="*70)
            print("\nAdd these to your .env file:")
            print()
            
            if 'url' in odoo_info:
                print(f"ODOO_URL={odoo_info['url']}")
            if 'database' in odoo_info:
                print(f"ODOO_DB={odoo_info['database']}")
            if 'username' in odoo_info:
                print(f"ODOO_USERNAME={odoo_info['username']}")
            if 'api_key' in odoo_info:
                print(f"ODOO_API_KEY={odoo_info['api_key']}")
            if 'password' in odoo_info:
                print(f"ODOO_PASSWORD={odoo_info['password']}")
            
            print("\n" + "="*70)
        
        return odoo_info
        
    except Exception as e:
        print(f"\nError reading Excel file: {e}")
        print("\nPlease check:")
        print("1. File exists at the specified path")
        print("2. pandas and openpyxl are installed:")
        print("   pip install pandas openpyxl")
        return None

if __name__ == "__main__":
    try:
        credentials = extract_odoo_credentials()
        
        if credentials:
            print("\n✓ Credentials extracted successfully!")
            print("\nNext steps:")
            print("1. Copy the suggested configuration above")
            print("2. Update your .env file")
            print("3. Run: python tests/test_odoo_connection.py")
        else:
            print("\n✗ Could not extract credentials")
            print("\nPlease manually check the Excel file and update .env")
            
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
