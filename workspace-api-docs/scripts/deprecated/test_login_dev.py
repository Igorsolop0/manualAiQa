#!/usr/bin/env python3
"""
Test regular email/password login on DEV environment (regression test for CT-709).
"""

import requests
import json

BASE_URL = "https://websitewebapi.dev.sofon.one"
PARTNER_ID = 5

def test_login_registration():
    """Test that traditional registration/login still works after OAuth refactor."""
    
    print("=" * 60)
    print("CT-709 Regression Test: Email/Password Auth")
    print("=" * 60)
    
    # Test 1: Register new user
    print("\n📋 Test 1: Registration with email/password")
    timestamp = int(__import__('time').time())
    email = f"ct709-test-{timestamp}@nextcode.tech"
    password = "TestPass123!"
    
    register_url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Register"
    
    register_data = {
        "partnerId": PARTNER_ID,
        "email": email,
        "password": password,
        "currencyId": "USD",
        "languageId": "en",
        "countryCode": "UA",
        "timeZone": -60,
        "deviceTypeId": 1
    }
    
    headers = {
        "Content-Type": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit.dev.sofon.one",
        "x-time-zone-offset": "-60",
    }
    
    try:
        response = requests.post(register_url, json=register_data, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("ResponseCode") == "Success":
            print("✅ Registration successful")
            client_id = result.get("ResponseObject", {}).get("ClientId")
            token = result.get("ResponseObject", {}).get("Token")
            print(f"ClientId: {client_id}")
            print(f"Token: {token[:50] if token else 'None'}...")
            
            # Test 2: Login with registered user
            print(f"\n📋 Test 2: Login with {email}")
            login_url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Login"
            
            login_data = {
                "email": email,
                "password": password,
                "partnerId": PARTNER_ID,
                "deviceType": 1
            }
            
            login_response = requests.post(login_url, json=login_data, headers=headers, timeout=10)
            print(f"Status: {login_response.status_code}")
            login_result = login_response.json()
            print(f"Response: {json.dumps(login_result, indent=2, ensure_ascii=False)}")
            
            if login_result.get("ResponseCode") == "Success":
                print("✅ Login successful")
                return {
                    "registration": "PASS",
                    "login": "PASS",
                    "email": email,
                    "client_id": client_id
                }
            else:
                print(f"❌ Login failed: {login_result.get('Description')}")
                return {
                    "registration": "PASS",
                    "login": "FAIL",
                    "email": email,
                    "error": login_result.get("Description")
                }
        else:
            print(f"❌ Registration failed: {result.get('Description')}")
            return {
                "registration": "FAIL",
                "login": "SKIP",
                "email": email,
                "error": result.get("Description")
            }
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return {
            "registration": "ERROR",
            "login": "ERROR",
            "error": str(e)
        }

if __name__ == "__main__":
    result = test_login_registration()
    print("\n" + "=" * 60)
    print("RESULT:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
