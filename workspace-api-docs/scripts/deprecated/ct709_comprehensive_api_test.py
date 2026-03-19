#!/usr/bin/env python3
"""
CT-709 Extended Backend OAuth Testing
Comprehensive API testing for OAuth refactor with mock data
"""

import requests
import json
import sys
from datetime import datetime
import time

BASE_URL = "https://websitewebapi.dev.sofon.one"
WEBSITE_URL = "https://minebit-casino.dev.sofon.one"
PARTNER_ID = 5

def get_headers():
    """Standard headers for Website API requests"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }

def test_google_oauth_variations():
    """Test Google OAuth with different payload variations"""
    print("\n" + "=" * 60)
    print("TEST: Google OAuth Payload Variations")
    print("=" * 60)

    url = f"{BASE_URL}/api/v3/GoogleAccount/OneTapJwtAuth"

    test_cases = [
        {
            "name": "Minimal payload",
            "payload": {
                "token": "mock.jwt.token",
                "signInState": {
                    "partnerId": PARTNER_ID,
                    "returnUrl": WEBSITE_URL
                }
            }
        },
        {
            "name": "Full payload with all fields",
            "payload": {
                "token": "mock.jwt.token",
                "signInState": {
                    "partnerId": PARTNER_ID,
                    "deviceFingerPrint": "test-fingerprint",
                    "deviceTypeId": 1,
                    "returnUrl": WEBSITE_URL,
                    "redirectUrl": f"{WEBSITE_URL}/callback",
                    "languageId": "en",
                    "currencyId": "USD",
                    "countryCode": "UA"
                }
            }
        },
        {
            "name": "Missing returnUrl (required)",
            "payload": {
                "token": "mock.jwt.token",
                "signInState": {
                    "partnerId": PARTNER_ID,
                    "deviceFingerPrint": "test"
                }
            }
        }
    ]

    results = []
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        try:
            response = requests.post(url, json=test_case['payload'], headers=get_headers(), timeout=10)
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"ResponseCode: {result.get('ResponseCode')}")
            print(f"Description: {result.get('Description')}")

            results.append({
                "name": test_case['name'],
                "status": response.status_code,
                "responseCode": result.get('ResponseCode'),
                "description": result.get('Description')
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "name": test_case['name'],
                "status": "ERROR",
                "error": str(e)
            })

    return results

def test_telegram_oauth_variations():
    """Test Telegram OAuth with different payload variations"""
    print("\n" + "=" * 60)
    print("TEST: Telegram OAuth Payload Variations")
    print("=" * 60)

    url = f"{BASE_URL}/api/v3/TelegramAccount/HashJwtAuth"

    test_cases = [
        {
            "name": "Minimal with hash",
            "payload": {
                "userData": {
                    "id": 123456789,
                    "authDate": int(time.time()),
                    "hash": "test_hash_value"
                },
                "state": {
                    "partnerId": PARTNER_ID,
                    "returnUrl": WEBSITE_URL
                }
            }
        },
        {
            "name": "Full user data",
            "payload": {
                "userData": {
                    "id": 987654321,
                    "firstName": "Test",
                    "lastName": "User",
                    "username": "testuser",
                    "photoUrl": "https://example.com/photo.jpg",
                    "authDate": int(time.time()),
                    "hash": "test_hash_value_full"
                },
                "state": {
                    "partnerId": PARTNER_ID,
                    "deviceFingerPrint": "test-fingerprint",
                    "deviceTypeId": 1,
                    "returnUrl": WEBSITE_URL,
                    "redirectUrl": f"{WEBSITE_URL}/callback"
                },
                "botId": "123456789:ABCdef"
            }
        },
        {
            "name": "Missing hash (should fail validation)",
            "payload": {
                "userData": {
                    "id": 111222333,
                    "firstName": "NoHash"
                },
                "state": {
                    "partnerId": PARTNER_ID,
                    "returnUrl": WEBSITE_URL
                }
            }
        }
    ]

    results = []
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        try:
            response = requests.post(url, json=test_case['payload'], headers=get_headers(), timeout=10)
            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"ResponseCode: {result.get('ResponseCode')}")
            print(f"Description: {result.get('Description')}")

            results.append({
                "name": test_case['name'],
                "status": response.status_code,
                "responseCode": result.get('ResponseCode'),
                "description": result.get('Description')
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "name": test_case['name'],
                "status": "ERROR",
                "error": str(e)
            })

    return results

def test_client_endpoints_with_token():
    """Test client endpoints that might reveal ExternalIdentity info"""
    print("\n" + "=" * 60)
    print("TEST: Client Endpoints for ExternalIdentity Info")
    print("=" * 60)

    # First create a test user
    register_url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Register"
    timestamp = int(time.time())
    email = f"ct709-api-test-{timestamp}@nextcode.tech"

    register_data = {
        "partnerId": PARTNER_ID,
        "email": email,
        "password": "TestPass123!",
        "currencyId": "USD",
        "languageId": "en",
        "deviceTypeId": 1
    }

    print(f"\nCreating test user: {email}")
    reg_response = requests.post(register_url, json=register_data, headers=get_headers(), timeout=10)
    reg_result = reg_response.json()

    if reg_result.get("ResponseCode") != "Success":
        print("❌ Failed to create test user")
        return None

    token = reg_result.get("ResponseObject", {}).get("Token")
    client_id = reg_result.get("ResponseObject", {}).get("Id")
    print(f"✅ User created: ID={client_id}")

    # Test endpoints with token
    auth_headers = get_headers()
    auth_headers["Authorization"] = token

    endpoints_to_test = [
        {
            "name": "GetClientIdentityModels",
            "method": "POST",
            "url": f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientIdentityModels"
        },
        {
            "name": "GetClientBalance",
            "method": "GET",
            "url": f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientBalance"
        },
        {
            "name": "GetClientAccounts",
            "method": "GET",
            "url": f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/GetClientAccounts"
        }
    ]

    results = []
    for endpoint in endpoints_to_test:
        print(f"\n--- {endpoint['name']} ---")
        try:
            if endpoint['method'] == "GET":
                response = requests.get(endpoint['url'], headers=auth_headers, timeout=10)
            else:
                response = requests.post(endpoint['url'], headers=auth_headers, timeout=10)

            result = response.json()
            print(f"Status: {response.status_code}")
            print(f"ResponseCode: {result.get('ResponseCode')}")

            # Check for ExternalIdentity info
            response_str = json.dumps(result)
            has_external = "external" in response_str.lower() or "identity" in response_str.lower()

            results.append({
                "name": endpoint['name'],
                "status": response.status_code,
                "responseCode": result.get('ResponseCode'),
                "has_external_identity_info": has_external,
                "responseObject_keys": list(result.get('ResponseObject', {}).keys()) if isinstance(result.get('ResponseObject'), dict) else None
            })

            if has_external:
                print(f"⚠️ Found External/Identity in response!")
                print(json.dumps(result, indent=2))

        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "name": endpoint['name'],
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "test_user": {
            "email": email,
            "client_id": client_id,
            "token": token
        },
        "endpoints": results
    }

def main():
    print("=" * 60)
    print("CT-709: Extended Backend OAuth Testing")
    print("Environment: DEV")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    results = {
        "ticket": "CT-709",
        "environment": "dev",
        "timestamp": datetime.now().isoformat(),
        "test_suites": []
    }

    # Test 1: Google OAuth variations
    google_results = test_google_oauth_variations()
    results["test_suites"].append({
        "suite": "Google OAuth Payload Tests",
        "tests": google_results
    })

    # Test 2: Telegram OAuth variations
    telegram_results = test_telegram_oauth_variations()
    results["test_suites"].append({
        "suite": "Telegram OAuth Payload Tests",
        "tests": telegram_results
    })

    # Test 3: Client endpoints for ExternalIdentity info
    client_results = test_client_endpoints_with_token()
    if client_results:
        results["test_suites"].append({
            "suite": "Client Endpoints for ExternalIdentity",
            "tests": client_results
        })

    # Save results
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-709"
    import os
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/extended-api-test-results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")

    return results

if __name__ == "__main__":
    main()
