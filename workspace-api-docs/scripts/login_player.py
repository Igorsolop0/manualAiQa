#!/usr/bin/env python3
"""
Login player via Website API to get fresh session token.
"""

import requests
import json

EMAIL = "demo1772613196064@nextcode.tech"
PASSWORD = "Qweasd123!"
PARTNER_ID = 5
BASE_URL = "https://websitewebapi.qa.sofon.one"

def login_player():
    """Login player and return session token."""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Login"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
    }
    
    data = {
        "email": EMAIL,
        "password": PASSWORD,
        "partnerId": PARTNER_ID,
        "deviceType": 1  # Desktop
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    print(f"Login response: {json.dumps(result, indent=2)}")
    
    if result.get("ResponseCode") == "Success":
        token = result.get("ResponseObject", {}).get("Token")
        if token:
            print(f"\n✅ Login successful!")
            print(f"Session token: {token}")
            return token
        else:
            raise Exception("No token in response")
    else:
        raise Exception(f"Login failed: {result.get('Description', 'Unknown error')}")

def get_balance(token):
    """Get balance with session token."""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientBalance"
    
    headers = {
        "Authorization": token,
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

if __name__ == "__main__":
    try:
        print(f"🔐 Logging in player {EMAIL}...")
        token = login_player()
        
        print(f"\n💰 Getting balance...")
        balance_data = get_balance(token)
        print(f"Balance: {json.dumps(balance_data, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()