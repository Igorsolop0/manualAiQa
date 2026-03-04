#!/usr/bin/env python3
"""
Check bonus details using GraphQL.
"""

import requests
import json

GRAPHQL_URL = "https://minebit-casino.qa.sofon.one/graphql"
BONUS_ID = 2469229
PARTNER_ID = 5

# Try without auth token first
headers = {
    "content-type": "application/json",
    "accept": "*/*",
    "website-locale": "en",
    "website-origin": "https://minebit-casino.qa.sofon.one",
    "x-time-zone-offset": "-60",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Origin": "https://minebit-casino.qa.sofon.one",
    "Referer": f"https://minebit-casino.qa.sofon.one/bonuses-new?modal-promo=rakeback",
}

def query_bonus_details():
    """Query bonus details without auth."""
    query = """
    query BonusDetails($bmsPartnerId: Int!, $bonusId: Int) {
      bonusDetails(bmsPartnerId: $bmsPartnerId, bonusId: $bonusId) {
        id
        name
        validTill
        availableInProducts
        turnOverCount
        __typename
      }
    }
    """
    
    variables = {
        "bmsPartnerId": PARTNER_ID,
        "bonusId": BONUS_ID
    }
    
    payload = {
        "operationName": "BonusDetails",
        "variables": variables,
        "query": query
    }
    
    print(f"🔍 Querying bonus details for ID {BONUS_ID}...")
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=10)
    
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response text: {response.text}")
        return None
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if "errors" in data:
        print(f"❌ GraphQL errors: {data['errors']}")
        return None
    
    return data.get("data", {}).get("bonusDetails")

def check_backoffice_bonus():
    """Try to get bonus info from BackOffice API."""
    url = f"https://adminwebapi.qa.sofon.one/api/Bonus/GetBonusById"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "UserId": "1",  # QA user ID
    }
    
    data = {
        "bonusId": BONUS_ID
    }
    
    print(f"\n🏢 Checking bonus in BackOffice...")
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"BackOffice response: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    print("🔍 Checking Realtime Rakeback Bonus...")
    print(f"Bonus ID: {BONUS_ID}")
    
    # Try GraphQL first
    details = query_bonus_details()
    
    if details:
        print(f"\n✅ Bonus Details:")
        print(f"   ID: {details.get('id')}")
        print(f"   Name: {details.get('name')}")
        print(f"   Valid Till: {details.get('validTill')}")
        print(f"   Turnover Count: {details.get('turnOverCount')}")
        print(f"   Available in Products: {details.get('availableInProducts')}")
        
        # Check if this looks like rakeback
        name = details.get('name', '').lower()
        if 'rake' in name or 'rakeback' in name or 'real-time' in name:
            print("   🎯 This appears to be a Realtime Rakeback bonus!")
        else:
            print("   ℹ️  Bonus name doesn't contain 'rake' or 'rakeback'")
    
    # Check BackOffice
    backoffice_info = check_backoffice_bonus()
    
    if backoffice_info:
        response_obj = backoffice_info.get("ResponseObject", {})
        if response_obj:
            print(f"\n🏢 BackOffice Bonus Info:")
            print(f"   Name: {response_obj.get('Name')}")
            print(f"   Bonus Type: {response_obj.get('BonusTypeId')}")
            print(f"   Is Active: {response_obj.get('IsActive')}")
            print(f"   Is Test: {response_obj.get('IsTest')}")
            print(f"   Turnover Count: {response_obj.get('TurnoverCount')}")
            print(f"   Min Amount: {response_obj.get('MinAmount')}")
            print(f"   Max Amount: {response_obj.get('MaxAmount')}")
            print(f"   Is Smartico: {response_obj.get('IsSmartico')}")
            
            # Check for rakeback-specific fields
            if response_obj.get('Name', '').lower().find('rake') >= 0:
                print("   🎯 This is likely the Realtime Rakeback bonus in BO!")
    
    print("\n📋 Next steps for testing:")
    print("1. Wait for 30-minute batch to complete (if just passed 10:10)")
    print("2. Check UI for bonus card with amount $0.25")
    print("3. Click 'Claim' button")
    print("4. Verify balance increases by $0.25")
    print("5. Verify button changes to 'Play Game' and timer appears")