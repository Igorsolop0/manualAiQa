#!/usr/bin/env python3
"""
Compare mgw/admin/api vs adminwebapi endpoints for GetBonusInfo
"""

import requests
import json

# Both endpoints to test
ENDPOINTS = {
    "adminwebapi": {
        "url": "https://adminwebapi.prod.sofon.one/api/Bonus/GetBonusInfo",
        "name": "adminwebapi"
    },
    "mgw_admin": {
        "url": "https://backoffice.prod.sofon.one/mgw/admin/api/Bonus/GetBonusInfo",
        "name": "mgw/admin/api (microgateway)"
    }
}

BONUS_ID = 11439
ADMIN_USER_ID = 560  # For adminwebapi (without login)

def test_adminwebapi():
    """Test adminwebapi endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: adminwebapi/Bonus/GetBonusInfo")
    print("=" * 60)
    
    url = ENDPOINTS["adminwebapi"]["url"]
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(ADMIN_USER_ID)
    }
    
    print(f"\nURL: {url}")
    print(f"Headers: UserId={ADMIN_USER_ID}")
    print(f"Body: {BONUS_ID}")
    
    try:
        response = requests.post(url, json=BONUS_ID, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("ResponseCode") == 0 or result.get("ResponseCode") == "Success":
                print(f"✅ SUCCESS")
                print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # Extract BonusTagId
                bonus = result.get("ResponseObject", {})
                print(f"\n📋 BonusTagId: {bonus.get('BonusTagId', 'NULL')}")
                print(f"   Name: {bonus.get('Name', 'N/A')}")
                print(f"   Template: {bonus.get('TemplateBonusName', 'N/A')}")
                
                return {
                    "endpoint": "adminwebapi",
                    "http_status": 200,
                    "bonus_tag_id": bonus.get("BonusTagId"),
                    "bonus_name": bonus.get("Name"),
                    "response": result
                }
            else:
                print(f"❌ API Error: {result.get('Description')}")
                return {
                    "endpoint": "adminwebapi",
                    "http_status": 200,
                    "error": result.get("Description")
                }
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return {
                "endpoint": "adminwebapi",
                "http_status": response.status_code,
                "error": response.text[:100]
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "endpoint": "adminwebapi",
            "error": str(e)
        }

def test_mgw_admin():
    """Test mgw/admin/api endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: mgw/admin/api/Bonus/GetBonusInfo (microgateway)")
    print("=" * 60)
    
    url = ENDPOINTS["mgw_admin"]["url"]
    
    print(f"\nURL: {url}")
    print(f"Body: {BONUS_ID}")
    print("Note: Requires Bearer Authorization token")
    
    # Try without auth
    print("\n--- Test 1: WITHOUT Authorization ---")
    try:
        response = requests.post(url, json=BONUS_ID, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Correct: Returns 401 Unauthorized (needs Bearer token)")
        elif response.status_code == 200:
            print(f"Response: {response.text[:100]}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Note about Bearer token
    print("\n--- NOTE ---")
    print("⚠️ mgw endpoint requires Bearer token from login")
    print("⚠️ Cannot test without valid Bearer token")
    print("⚠️ User needs to provide token or login credentials")

def compare_endpoints():
    """Compare responses and explain difference"""
    print("\n" + "=" * 60)
    print("COMPARISON & ANALYSIS")
    print("=" * 60)
    
    # Test adminwebapi (we can use this)
    adminwebapi_result = test_adminwebapi()
    
    # Test mgw (we know it needs auth)
    print(f"\n--- Test mgw endpoint ---")
    
    url = ENDPOINTS["mgw_admin"]["url"]
    
    try:
        response = requests.post(url, json=BONUS_ID, headers={"Content-Type": "application/json"}, timeout=10)
        mgw_http_status = response.status_code
        print(f"HTTP Status: {mgw_http_status}")
        
        mgw_result = {
            "http_status": mgw_http_status,
            "note": "Requires Bearer token" if mgw_http_status == 401 else "Other error"
        }
    except Exception as e:
        mgw_result = {"error": str(e)}
        mgw_http_status = 999
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"\nadminwebapi endpoint:")
    print(f"  - URL: {ENDPOINTS['adminwebapi']['url']}")
    print(f"  - Auth: UserId header (no Bearer token)")
    print(f"  - Status: {adminwebapi_result.get('http_status', 'ERROR')}")
    
    if "bonus_tag_id" in adminwebapi_result:
        print(f"  - BonusTagId: {adminwebapi_result['bonus_tag_id']}")
    
    print(f"\nmgw/admin/api endpoint:")
    print(f"  - URL: {ENDPOINTS['mgw_admin']['url']}")
    print(f"  - Auth: Bearer token required")
    print(f"  - Status: {mgw_result.get('http_status', 'ERROR')}")
    
    # Conclusion
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    
    if "bonus_tag_id" in adminwebapi_result:
        tag_id = adminwebapi_result["bonus_tag_id"]
        
        print(f"\n✅ adminwebapi returns BonusTagId: {tag_id}")
        
        if tag_id == 7:
            print(f"   ✅ This matches 'Weekly' tag user saw!")
            print(f"   ✅ GetBonusInfo shows different data than GetBonuses")
            print(f"   💡 Explanation:")
            print(f"      - GetBonusInfo returns detailed info")
            print(f"      - GetBonuses returns summary list")
            print(f"      - Different data sources or caching")
            print(f"      - mgw endpoint might return different data")
        else:
            print(f"   ⚠️ BonusTagId is {tag_id} (not 7)")
            print(f"   ⚠️ User likely saw stale data or different bonus")
            print(f"   ⚠️ Possible data inconsistency between endpoints")
    else:
        print(f"\n⚠️ adminwebapi failed")
        print(f"   Error: {adminwebapi_result.get('error', 'Unknown')}")
        print(f"   Cannot compare BonusTagId values")
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"   Use adminwebapi endpoint (no Bearer token needed)")
    print(f"   Endpoint: {ENDPOINTS['adminwebapi']['url']}")
    print(f"   Headers: UserId: {ADMIN_USER_ID}")
    
    # Save results
    results = {
        "bonus_id": BONUS_ID,
        "adminwebapi_result": adminwebapi_result,
        "mgw_admin_result": mgw_result,
        "comparison": {
            "adminwebapi_url": ENDPOINTS["adminwebapi"]["url"],
            "mgw_admin_url": ENDPOINTS["mgw_admin"]["url"],
            "recommendation": "Use adminwebapi (simpler auth)"
        }
    }
    
    output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-657/endpoint-comparison.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("BONUS 11439 - ENDPOINT COMPARISON")
    print("Comparing: adminwebapi vs mgw/admin/api")
    print("=" * 60)
    
    compare_endpoints()
