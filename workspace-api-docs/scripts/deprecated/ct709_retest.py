#!/usr/bin/env python3
"""
CT-709 Retest - Compare with 2026-03-10 Results
"""

import requests
import json
import sys
from datetime import datetime
import time

BASE_URL = "https://websitewebapi.dev.sofon.one"
WEBSITE_URL = "https://minebit-casino.dev.sofon.one"
PARTNER_ID = 5

# Previous test results for comparison
PREVIOUS_TEST = {
    "google_oauth": {
        "status": 200,
        "responseCode": "Success",
        "responseObject": None,
        "traceId": "354a8d3a8b405a378fa4980de8a6fb4c"
    },
    "telegram_oauth": {
        "status": 400,
        "responseCode": 284,
        "description": "NotConfigured"
    },
    "registration": {
        "status": 200,
        "responseCode": "Success",
        "clientId": 59177
    }
}

def get_headers():
    """Standard headers"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }

def compare_results(test_name, previous, current):
    """Compare previous and current test results"""
    changes = []
    
    if previous.get("status") != current.get("status"):
        changes.append(f"Status changed: {previous.get('status')} → {current.get('status')}")
    
    if previous.get("responseCode") != current.get("responseCode"):
        changes.append(f"ResponseCode changed: {previous.get('responseCode')} → {current.get('responseCode')}")
    
    if previous.get("description") != current.get("description"):
        changes.append(f"Description changed: {previous.get('description')} → {current.get('description')}")
    
    return changes

def test_google_oauth():
    """Test Google OAuth endpoint"""
    print("\n" + "=" * 60)
    print("TEST: Google OAuth - OneTapJwtAuth")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/GoogleAccount/OneTapJwtAuth"
    
    payload = {
        "token": "mock.jwt.token.retest.20260311",
        "signInState": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-retest",
            "deviceTypeId": 1,
            "returnUrl": WEBSITE_URL,
            "redirectUrl": f"{WEBSITE_URL}/callback"
        }
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # Compare with previous
        current = {
            "status": response.status_code,
            "responseCode": result.get("ResponseCode"),
            "responseObject": result.get("ResponseObject"),
            "description": result.get("Description")
        }
        
        changes = compare_results("Google OAuth", PREVIOUS_TEST["google_oauth"], current)
        
        return {
            "test": "Google OAuth",
            "status": "PASS" if response.status_code == 200 else "FAIL",
            "http_status": response.status_code,
            "response": result,
            "changes_from_previous": changes if changes else ["No changes"],
            "previous_result": PREVIOUS_TEST["google_oauth"]
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Google OAuth",
            "status": "ERROR",
            "error": str(e)
        }

def test_telegram_oauth():
    """Test Telegram OAuth endpoint"""
    print("\n" + "=" * 60)
    print("TEST: Telegram OAuth - HashJwtAuth")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/TelegramAccount/HashJwtAuth"
    
    payload = {
        "userData": {
            "id": 123456789,
            "firstName": "Retest",
            "lastName": "User",
            "username": "retest_user",
            "authDate": int(time.time()),
            "hash": "mock_hash_retest_20260311"
        },
        "state": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-retest",
            "deviceTypeId": 1,
            "returnUrl": WEBSITE_URL,
            "redirectUrl": f"{WEBSITE_URL}/callback"
        },
        "botId": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # Compare with previous
        current = {
            "status": response.status_code,
            "responseCode": result.get("ResponseCode"),
            "description": result.get("Description")
        }
        
        changes = compare_results("Telegram OAuth", PREVIOUS_TEST["telegram_oauth"], current)
        
        return {
            "test": "Telegram OAuth",
            "status": "PASS" if response.status_code in [200, 400] else "FAIL",
            "http_status": response.status_code,
            "response": result,
            "changes_from_previous": changes if changes else ["No changes"],
            "previous_result": PREVIOUS_TEST["telegram_oauth"]
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Telegram OAuth",
            "status": "ERROR",
            "error": str(e)
        }

def test_registration():
    """Test traditional registration"""
    print("\n" + "=" * 60)
    print("TEST: Traditional Registration - Email/Password")
    print("=" * 60)
    
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Register"
    
    timestamp = int(time.time())
    email = f"ct709-retest-{timestamp}@nextcode.tech"
    
    payload = {
        "partnerId": PARTNER_ID,
        "email": email,
        "password": "TestPass123!",
        "currencyId": "USD",
        "languageId": "en",
        "deviceTypeId": 1
    }
    
    print(f"URL: {url}")
    print(f"Email: {email}")
    
    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        
        if result.get("ResponseCode") == "Success":
            client_id = result.get("ResponseObject", {}).get("Id")
            token = result.get("ResponseObject", {}).get("Token")
            print(f"✅ Registration successful")
            print(f"Client ID: {client_id}")
            print(f"Token: {token[:50] if token else 'None'}...")
            
            # Compare with previous
            previous_client_id = PREVIOUS_TEST["registration"]["clientId"]
            changes = [
                f"Previous client_id: {previous_client_id}",
                f"New client_id: {client_id}",
                "✅ Registration still working"
            ]
            
            return {
                "test": "Traditional Registration",
                "status": "PASS",
                "http_status": response.status_code,
                "client_id": client_id,
                "email": email,
                "changes_from_previous": changes,
                "previous_result": PREVIOUS_TEST["registration"]
            }
        else:
            print(f"❌ Registration failed: {result.get('Description')}")
            return {
                "test": "Traditional Registration",
                "status": "FAIL",
                "http_status": response.status_code,
                "error": result.get("Description"),
                "response": result
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Traditional Registration",
            "status": "ERROR",
            "error": str(e)
        }

def main():
    print("=" * 60)
    print("CT-709: Retest - Compare with 2026-03-10 Results")
    print("Environment: DEV")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    results = {
        "ticket": "CT-709",
        "test_type": "Retest",
        "environment": "dev",
        "timestamp": datetime.now().isoformat(),
        "previous_test_date": "2026-03-10T18:52:36",
        "tests": []
    }
    
    # Test 1: Google OAuth
    results["tests"].append(test_google_oauth())
    
    # Test 2: Telegram OAuth
    results["tests"].append(test_telegram_oauth())
    
    # Test 3: Registration
    results["tests"].append(test_registration())
    
    # Summary
    print("\n" + "=" * 60)
    print("CHANGES SUMMARY")
    print("=" * 60)
    
    for test in results["tests"]:
        print(f"\n{test['test']}:")
        print(f"  Status: {test['status']}")
        if "changes_from_previous" in test:
            for change in test["changes_from_previous"]:
                print(f"  - {change}")
    
    # Save results
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-709"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/retest-20260311-1119.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
