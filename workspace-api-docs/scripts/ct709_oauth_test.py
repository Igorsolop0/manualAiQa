#!/usr/bin/env python3
"""
CT-709 Backend OAuth Testing on Dev Environment
Tests Google and Telegram OAuth flows with mock data
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "https://websitewebapi.dev.sofon.one"
WEBSITE_URL = "https://minebit-casino.dev.sofon.one"
PARTNER_ID = 5

def test_google_oauth_mock():
    """Test Google OAuth endpoint with mock JWT token"""
    print("\n" + "=" * 60)
    print("Test: Google OAuth - OneTapJwtAuth with Mock Token")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/GoogleAccount/OneTapJwtAuth"
    
    # Mock Google JWT (not signed by Google, will fail validation)
    mock_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJzdWIiOiIxMjM0NTY3ODkwMTIzNDU2Nzg5MCIsImF1ZCI6InlvdXItY2xpZW50LWlkLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiaWF0IjoxNzczMTM4Njc0LCJleHAiOjE3NzMxNDIyNzQsImVtYWlsIjoidGVzdC5jdDcwOUBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiVGVzdCBVc2VyIn0=.mock-signature"
    
    payload = {
        "token": mock_jwt,
        "signInState": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-ct709",
            "deviceTypeId": 1,
            "returnUrl": "https://minebit-casino.dev.sofon.one",
            "redirectUrl": "https://minebit-casino.dev.sofon.one/callback"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        
        return {
            "test": "Google OAuth Mock Token",
            "status": "PASS" if response.status_code == 200 else "FAIL",
            "http_status": response.status_code,
            "response": result,
            "notes": "Mock token test - backend validation behavior"
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Google OAuth Mock Token",
            "status": "ERROR",
            "error": str(e)
        }

def test_telegram_oauth_mock():
    """Test Telegram OAuth endpoint with mock data"""
    print("\n" + "=" * 60)
    print("Test: Telegram OAuth - HashJwtAuth with Mock Data")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/TelegramAccount/HashJwtAuth"
    
    # Mock Telegram user data
    payload = {
        "userData": {
            "id": 123456789,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser_ct709",
            "language_code": "en"
        },
        "state": {
            "partnerId": PARTNER_ID,
            "deviceFingerPrint": "test-fingerprint-ct709-telegram",
            "deviceTypeId": 1,
            "returnUrl": "https://minebit-casino.dev.sofon.one",
            "redirectUrl": "https://minebit-casino.dev.sofon.one/callback"
        },
        "botId": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Mock bot ID
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        
        return {
            "test": "Telegram OAuth Mock Data",
            "status": "PASS" if response.status_code == 200 else "FAIL",
            "http_status": response.status_code,
            "response": result,
            "notes": "Mock data test - backend validation behavior"
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Telegram OAuth Mock Data",
            "status": "ERROR",
            "error": str(e)
        }

def test_registration_fallback():
    """Test traditional registration to ensure fallback works"""
    print("\n" + "=" * 60)
    print("Test: Registration Fallback - Email/Password")
    print("=" * 60)
    
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Client/Register"
    
    timestamp = int(datetime.now().timestamp())
    email = f"ct709-fallback-{timestamp}@nextcode.tech"
    
    payload = {
        "partnerId": PARTNER_ID,
        "email": email,
        "password": "TestPass123!",
        "currencyId": "USD",
        "languageId": "en",
        "countryCode": "UA",
        "deviceTypeId": 1
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60"
    }
    
    print(f"URL: {url}")
    print(f"Email: {email}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        print(f"\nStatus: {response.status_code}")
        
        if result.get("ResponseCode") == "Success":
            client_id = result.get("ResponseObject", {}).get("Id")
            token = result.get("ResponseObject", {}).get("Token")
            print(f"✅ Registration successful")
            print(f"Client ID: {client_id}")
            print(f"Token: {token[:50] if token else 'None'}...")
            
            return {
                "test": "Registration Fallback",
                "status": "PASS",
                "http_status": response.status_code,
                "client_id": client_id,
                "email": email,
                "notes": "Traditional registration still works"
            }
        else:
            print(f"❌ Registration failed: {result.get('Description')}")
            return {
                "test": "Registration Fallback",
                "status": "FAIL",
                "http_status": response.status_code,
                "error": result.get("Description"),
                "response": result
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Registration Fallback",
            "status": "ERROR",
            "error": str(e)
        }

def test_swagger_endpoints():
    """Verify OAuth endpoints exist in Swagger"""
    print("\n" + "=" * 60)
    print("Test: Swagger Endpoint Validation")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/swagger/v3/swagger.json", timeout=10)
        swagger = response.json()
        
        required_endpoints = [
            "/api/v3/GoogleAccount/OneTapAuth",
            "/api/v3/GoogleAccount/OneTapJwtAuth",
            "/api/v3/TelegramAccount/HashAuth",
            "/api/v3/TelegramAccount/HashJwtAuth"
        ]
        
        found_endpoints = []
        missing_endpoints = []
        
        for endpoint in required_endpoints:
            if endpoint in swagger.get("paths", {}):
                found_endpoints.append(endpoint)
                print(f"✅ {endpoint}")
            else:
                missing_endpoints.append(endpoint)
                print(f"❌ {endpoint} - NOT FOUND")
        
        return {
            "test": "Swagger Endpoints",
            "status": "PASS" if len(missing_endpoints) == 0 else "FAIL",
            "found": found_endpoints,
            "missing": missing_endpoints,
            "total_required": len(required_endpoints)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "test": "Swagger Endpoints",
            "status": "ERROR",
            "error": str(e)
        }

def main():
    print("=" * 60)
    print("CT-709: Backend OAuth Refactor Testing")
    print("Environment: DEV")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    results = {
        "ticket": "CT-709",
        "environment": "dev",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Test 1: Swagger endpoints
    results["tests"].append(test_swagger_endpoints())
    
    # Test 2: Google OAuth with mock token
    results["tests"].append(test_google_oauth_mock())
    
    # Test 3: Telegram OAuth with mock data
    results["tests"].append(test_telegram_oauth_mock())
    
    # Test 4: Registration fallback
    results["tests"].append(test_registration_fallback())
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    errors = sum(1 for t in results["tests"] if t["status"] == "ERROR")
    
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    
    # Save results
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-709"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/backend-oauth-test-results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
