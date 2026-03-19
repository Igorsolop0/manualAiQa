#!/usr/bin/env python3
"""
Test Social Account Management on QA AdminWebAPI
Find endpoints for: GetClientLogins, LinkSocialAccount, UnlinkSocialAccount
"""

import requests
import json

# QA Environment
QA_WEBSITE_API = "https://minebit-casino.qa.sofon.one"
QA_BACKOFFICE_API = "https://qa-adminwebapi.minebit.com/api"
PARTNER_ID = 5
QA_USER_EMAIL = "pandasen@echoprx.cc"
QA_USER_PASSWORD = "Qweasd123!"

PLAYER_CLIENT_ID = 3563473  # Test player to delete

def get_client_logins_api():
    """Test GetClientLogins via Website API"""
    print("\n" + "=" * 60)
    print("TEST 1: GetClientLogins (Website API)")
    print("=" * 60)
    
    # First, login to get token
    login_url = f"{QA_WEBSITE_API}/{PARTNER_ID}/api/v3/Client/Login"
    
    login_response = requests.post(login_url, json={
        "partnerId": PARTNER_ID,
        "languageId": "en",
        "token": QA_USER_EMAIL,
        "password": QA_USER_PASSWORD,
        "timeZone": -60
    }, timeout=10)
    
    print(f"\nLogin URL: {login_url}")
    print(f"Status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("❌ Login failed - cannot proceed")
        return None
    
    login_data = login_response.json()
    if login_data.get("ResponseCode") != "Success":
        print(f"❌ Login failed: {login_data.get('Description')}")
        return None
    
    token = login_data.get("ResponseObject", {}).get("Token")
    print(f"✅ Login successful, token: {token[:50]}...")
    
    # Now get client logins
    logins_url = f"{QA_WEBSITE_API}/{PARTNER_ID}/api/v3/Client/GetClientLogins"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60"
    }
    
    logins_response = requests.post(logins_url, headers=headers, json={
        "partnerId": PARTNER_ID,
        "token": token,
        "languageId": "en",
        "timeZone": -60
    }, timeout=10)
    
    print(f"\nGetClientLogins URL: {logins_url}")
    print(f"Status: {logins_response.status_code}")
    print(f"Response:\n{json.dumps(logins_response.json(), indent=2, ensure_ascii=False)}")
    
    return logins_response.json()

def test_unlink_social_account():
    """Test UnlinkSocialAccount endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: UnlinkSocialAccount (BackOffice API)")
    print("=" * 60)
    
    # Try different possible endpoints
    endpoints = [
        f"{QA_BACKOFFICE_API}/Client/UnlinkSocialAccount",
        f"{QA_BACKOFFICE_API}/Client/UnlinkGoogle",
        f"{QA_BACKOFFICE_API}/Client/UnlinkTelegram",
        f"{QA_BACKOFFICE_API}/Client/RemoveSocialAccount",
    ]
    
    for endpoint in endpoints:
        print(f"\nTrying: {endpoint}")
        
        try:
            # Try different payload structures
            payloads = [
                {
                    "clientId": PLAYER_CLIENT_ID,
                    "provider": "Google"
                },
                {
                    "clientId": PLAYER_CLIENT_ID,
                    "registrationSourceId": 3  # Google
                },
                PLAYER_CLIENT_ID
            ]
            
            for payload in payloads:
                response = requests.post(endpoint, json=payload, timeout=10)
                print(f"   Payload: {payload}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)}")
                    
                    if result.get("ResponseCode") == 0 or result.get("ResponseCode") == "Success":
                        print(f"   ✅ SUCCESS!")
                        return endpoint, payload, result
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None, None, None

def main():
    print("=" * 60)
    print("SOCIAL ACCOUNT MANAGEMENT - QA TESTING")
    print(f"Player: ID={PLAYER_CLIENT_ID}, Email={QA_USER_EMAIL}")
    print("=" * 60)
    
    results = {
        "player": {
            "id": PLAYER_CLIENT_ID,
            "email": QA_USER_EMAIL
        },
        "tests": []
    }
    
    # Test 1: GetClientLogins
    logins_data = get_client_logins_api()
    
    if logins_data:
        results["tests"].append({
            "name": "GetClientLogins",
            "status": "executed",
            "details": logins_data
        })
    
    # Test 2: UnlinkSocialAccount
    endpoint, payload, result = test_unlink_social_account()
    
    if endpoint:
        results["tests"].append({
            "name": "UnlinkSocialAccount",
            "endpoint": endpoint,
            "payload": payload,
            "result": result,
            "status": "tested"
        })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal tests: {len(results['tests'])}")
    print(f"GetClientLogins: {'✅ Works' if logins_data else '❌ Failed'}")
    print(f"UnlinkSocialAccount: {'✅ Found' if endpoint else '❌ Not found'}")
    
    # Save results
    output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-752/social-account-management.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
