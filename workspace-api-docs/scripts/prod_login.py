#!/usr/bin/env python3
"""
Login player on PROD via Website API to get session token for CT-476 testing.
"""

import requests
import json
import sys
from datetime import datetime

# Test credentials (should work across environments)
EMAIL = "demo1772613196064@nextcode.tech"
PASSWORD = "Qweasd123!"
PARTNER_ID = 5
BASE_URL = "https://websitewebapi.prod.sofon.one"
WEBSITE_URL = "https://minebit-casino.prod.sofon.one"

def login_player():
    """Login player on PROD and return session token."""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Login"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    data = {
        "token": EMAIL,  # Can be email or username
        "password": PASSWORD,
        "partnerId": PARTNER_ID,
        "deviceType": 1,  # Desktop
        "languageId": "en",
        "timeZone": -60
    }
    
    print(f"🔐 Attempting login for {EMAIL} on PROD...")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        print(f"\n📦 Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("ResponseCode") == "Success":
            token = result.get("ResponseObject", {}).get("Token")
            client_id = result.get("ResponseObject", {}).get("Id")
            
            if token:
                print(f"\n✅ Login successful!")
                print(f"Client ID: {client_id}")
                print(f"Session Token: {token}")
                
                return {
                    "token": token,
                    "client_id": client_id,
                    "email": EMAIL,
                    "partner_id": PARTNER_ID,
                    "environment": "prod",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise Exception("No token in response")
        else:
            raise Exception(f"Login failed: {result.get('Description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        raise

def test_token(token):
    """Test token by making authenticated request."""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientBalance"
    
    headers = {
        "Authorization": token,
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    print(f"\n🧪 Testing token with balance request...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        result = response.json()
        print(f"✅ Token is valid! Balance data received.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"❌ Token test failed: {e}")
        return False

def save_auth_data(auth_data):
    """Save auth data to workspace for Clawver to use."""
    import os
    
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-auth"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/prod-player-auth.json"
    
    with open(output_file, 'w') as f:
        json.dump(auth_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Auth data saved to: {output_file}")
    print(f"\n📋 Usage for Clawver:")
    print(f"   Token: {auth_data['token']}")
    print(f"   Header: Authorization: {auth_data['token']}")
    print(f"   OR Cookie: session_token={auth_data['token']}")
    
    return output_file

if __name__ == "__main__":
    try:
        auth_data = login_player()
        
        if test_token(auth_data['token']):
            output_file = save_auth_data(auth_data)
            print(f"\n✅ All done! Auth data ready for Clawver.")
            sys.exit(0)
        else:
            print(f"\n⚠️ Login succeeded but token validation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
