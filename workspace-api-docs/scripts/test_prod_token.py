#!/usr/bin/env python3
"""
Test if PROD session token works with proper GraphQL queries.
"""

import requests
import json
import sys

GRAPHQL_URL = "https://minebit-casino.prod.sofon.one/graphql"
WEBSITE_URL = "https://minebit-casino.prod.sofon.one"
TOKEN = "626d4eca402e4f61ae8629889300c03b"
PARTNER_ID = 5

def test_token():
    """Test session token with proper GraphQL query."""
    
    query = """
    query GetPlayerProfile($bmsPartnerId: Int!, $locale: Locale!) {
        player(bmsPartnerId: $bmsPartnerId, locale: $locale) {
            id
            email
            userName
            currencyId
            creationTime
        }
    }
    """
    
    variables = {
        "bmsPartnerId": PARTNER_ID,
        "locale": "en"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": TOKEN,
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
    }
    
    payload = {
        "operationName": "GetPlayerProfile",
        "query": query,
        "variables": variables
    }
    
    print(f"🧪 Testing session token with player profile query...")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        
        if "errors" in result:
            print(f"❌ Token validation failed:")
            print(json.dumps(result["errors"], indent=2, ensure_ascii=False))
            return False
        
        player = result.get("data", {}).get("player")
        if player:
            print(f"✅ Token is VALID! Player profile retrieved:")
            print(f"   ID: {player.get('id')}")
            print(f"   Email: {player.get('email')}")
            print(f"   Username: {player.get('userName')}")
            print(f"   Currency ID: {player.get('currencyId')}")
            print(f"   Created: {player.get('creationTime')}")
            return True
        else:
            print(f"⚠️ No player data in response")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return False
            
    except Exception as e:
        print(f"❌ Token test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_token()
    sys.exit(0 if success else 1)
