#!/usr/bin/env python3
"""
CT-709 Urgent Test - Alov Brand (PartnerId: 2)
"""

import requests
import json
import time

BASE_URL = "https://websitewebapi.dev.sofon.one"
# Try with MineBit URL first (same backend serves multiple brands)
WEBSITE_URL = "https://minebit-casino.dev.sofon.one"
PARTNER_ID = 2  # Alov

def test_google_oauth_partner2():
    """Test Google OAuth with partnerId: 2"""
    print("\n" + "=" * 60)
    print("URGENT TEST: Google OAuth - PartnerId: 2 (Alov)")
    print("=" * 60)

    url = f"{BASE_URL}/api/v3/GoogleAccount/OneTapJwtAuth"

    payload = {
        "token": "mock.jwt.token.alov.test",
        "signInState": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-alov",
            "deviceTypeId": 1,
            "returnUrl": WEBSITE_URL,
            "redirectUrl": f"{WEBSITE_URL}/callback"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()

        print(f"Status: {response.status_code}")
        print(f"ResponseCode: {result.get('ResponseCode')}")
        print(f"Description: {result.get('Description')}")
        print(f"TraceId: {result.get('TraceId')}")

        return {
            "test": "Google OAuth - Alov (PartnerId: 2)",
            "status": "PASS" if response.status_code == 200 else "FAIL",
            "http_status": response.status_code,
            "response": result
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Google OAuth - Alov",
            "status": "ERROR",
            "error": str(e)
        }

def test_telegram_oauth_partner2():
    """Test Telegram OAuth with partnerId: 2"""
    print("\n" + "=" * 60)
    print("URGENT TEST: Telegram OAuth - PartnerId: 2 (Alov)")
    print("=" * 60)

    url = f"{BASE_URL}/api/v3/TelegramAccount/HashJwtAuth"

    payload = {
        "userData": {
            "id": 987654321,
            "firstName": "AlovTest",
            "lastName": "User",
            "username": "alov_test_user",
            "authDate": int(time.time()),
            "hash": "mock_hash_alov_test"
        },
        "state": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-alov",
            "deviceTypeId": 1,
            "returnUrl": WEBSITE_URL,
            "redirectUrl": f"{WEBSITE_URL}/callback"
        },
        "botId": "987654321:ABCdefTest"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()

        print(f"Status: {response.status_code}")
        print(f"ResponseCode: {result.get('ResponseCode')}")
        print(f"Description: {result.get('Description')}")
        print(f"TraceId: {result.get('TraceId')}")

        return {
            "test": "Telegram OAuth - Alov (PartnerId: 2)",
            "status": "PASS" if response.status_code in [200, 400] else "FAIL",
            "http_status": response.status_code,
            "response": result
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Telegram OAuth - Alov",
            "status": "ERROR",
            "error": str(e)
        }

# Execute tests immediately
print("=" * 60)
print("CT-709 URGENT: Alov Brand Testing (PartnerId: 2)")
print("=" * 60)

results = {
    "ticket": "CT-709",
    "test_type": "URGENT - Alov Brand",
    "partner_id": 2,
    "brand": "Alov",
    "tests": []
}

results["tests"].append(test_google_oauth_partner2())
results["tests"].append(test_telegram_oauth_partner2())

print("\n" + "=" * 60)
print("SUMMARY FOR IHOR")
print("=" * 60)

for test in results["tests"]:
    print(f"{test['test']}: {test['status']}")

# Save
output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-709/alov-urgent-test.json"
import os
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n💾 Results: {output_file}")
