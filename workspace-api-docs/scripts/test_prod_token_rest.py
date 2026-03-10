#!/usr/bin/env python3
"""
Test if PROD session token works with REST API.
"""

import requests
import json
import sys

WEBSITE_API = "https://websitewebapi.prod.sofon.one"
WEBSITE_URL = "https://minebit-casino.prod.sofon.one"
TOKEN = "626d4eca402e4f61ae8629889300c03b"
PARTNER_ID = 5
PLAYER_ID = 1184432

def test_rest_token():
    """Test session token with REST API endpoint."""
    
    # Test GetClient endpoint
    url = f"{WEBSITE_API}/{PARTNER_ID}/api/v3/Client/GetClient"
    
    headers = {
        "Authorization": TOKEN,
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    print(f"🧪 Testing session token with REST API (GetClient)...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        print(f"\n📦 Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("ResponseCode") == "Success":
            client = result.get("ResponseObject", {})
            print(f"\n✅ Token is VALID! Client data retrieved:")
            print(f"   ID: {client.get('Id')}")
            print(f"   Email: {client.get('Email')}")
            print(f"   Username: {client.get('UserName')}")
            print(f"   Currency: {client.get('CurrencyId')}")
            return True
        else:
            print(f"\n❌ Token validation failed: {result.get('Description')}")
            return False
            
    except Exception as e:
        print(f"❌ REST API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_rest_token()
    sys.exit(0 if success else 1)
