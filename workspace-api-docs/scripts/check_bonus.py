#!/usr/bin/env python3
"""
Check bonus information for a player via Website API.
"""

import requests
import json
import sys

# Player session token
SESSION_TOKEN = "1ddfcbfc0140423a9204dc9f3d940b6a"
PARTNER_ID = 5
BASE_URL = "https://websitewebapi.qa.sofon.one"

headers = {
    "Authorization": SESSION_TOKEN,
    "website-locale": "en",
    "website-origin": "https://minebit-casino.qa.sofon.one",
    "x-time-zone-offset": "-60",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def get_balance():
    """Get player balance."""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientBalance"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_active_bonuses():
    """Get active bonuses for player."""
    # Try to find the correct endpoint for bonuses
    # Based on API analysis, there might be endpoints like:
    # /Bonus/GetActiveBonuses, /Bonus/GetBonusHistory, etc.
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Bonus/GetActiveBonuses"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Try another endpoint
        url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Bonus/GetBonusHistory"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get bonuses: {response.status_code}"}

def get_rakeback_info():
    """Try to get specific rakeback information."""
    # This might be a custom endpoint for Realtime Rakeback
    # Check common bonus endpoints first
    endpoints = [
        "/Bonus/GetActiveBonuses",
        "/Bonus/GetBonusHistory",
        "/Bonus/GetBonusInfo",
        "/Bonus/GetAvailableBonuses",
        "/Campaign/GetActiveCampaigns",
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}/{PARTNER_ID}/api/v3{endpoint}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("ResponseCode") == "Success":
                    print(f"\n✅ Found data from {endpoint}:")
                    return data
        except Exception as e:
            continue
    
    return {"error": "No bonus endpoints responded successfully"}

if __name__ == "__main__":
    print("🔍 Checking player bonus information...")
    print(f"Session token: {SESSION_TOKEN[:20]}...")
    
    try:
        # Get balance
        print("\n💰 Getting balance...")
        balance_data = get_balance()
        print(f"Balance response: {json.dumps(balance_data, indent=2)}")
        
        # Get bonus info
        print("\n🎁 Getting bonus information...")
        bonus_data = get_rakeback_info()
        print(f"Bonus response: {json.dumps(bonus_data, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)