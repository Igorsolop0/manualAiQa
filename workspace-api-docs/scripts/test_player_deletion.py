#!/usr/bin/env python3
"""
Test Player Deactivation on AdminWebAPI
Goal: Deactivate player 3563473 to allow clean testing
"""

import requests
import json
import sys

# Test environments
ENVIRONMENTS = {
    "dev": "https://adminwebapi.dev.sofon.one/api",
    "qa": "https://qa-adminwebapi.minebit.com/api"
}

# Test player
PLAYER_CLIENT_ID = 3563473
PLAYER_EMAIL = "pandasen@echoprx.cc"

# Admin credentials
ADMIN_USER_ID = 560

def test_deactivate_clients(endpoint: str):
    """Test DeactivateClients endpoint"""
    print(f"\n{'=' * 60}")
    print(f"Testing: {endpoint}")
    print(f"{'=' * 60}")
    
    url = f"{endpoint}/Client/DeactivateClients"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(ADMIN_USER_ID)
    }
    
    payload = [PLAYER_CLIENT_ID]
    
    print(f"\nURL: {url}")
    print(f"Headers: UserId={ADMIN_USER_ID}")
    print(f"Payload: {json.dumps(payload)}")
    print(f"\nPlayer to deactivate: ID={PLAYER_CLIENT_ID}, Email={PLAYER_EMAIL}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("ResponseCode") == 0:
                print(f"\n✅ SUCCESS: Player deactivated!")
                return True
            else:
                print(f"\n⚠️ API returned error code: {result.get('ResponseCode')}")
                print(f"Description: {result.get('Description')}")
                return False
        else:
            print(f"\n❌ FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def test_other_delete_endpoints(endpoint: str):
    """Test other possible deletion endpoints"""
    print(f"\n{'=' * 60}")
    print(f"Testing other deletion endpoints")
    print(f"{'=' * 60}")
    
    # Possible endpoints
    endpoints_to_test = [
        f"{endpoint}/Client/Delete",
        f"{endpoint}/Client/DeleteClient",
        f"{endpoint}/Client/RemoveClient",
        f"{endpoint}/Players/Delete",
        f"{endpoint}/Players/Remove",
        f"{endpoint}/Client/SetTest/{PLAYER_CLIENT_ID}",
    ]
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(ADMIN_USER_ID)
    }
    
    for url in endpoints_to_test:
        try:
            print(f"\nTrying: {url}")
            
            # Try different methods
            for method in ["DELETE", "POST"]:
                try:
                    if method == "DELETE":
                        resp = requests.delete(url, headers=headers, timeout=5)
                    else:
                        resp = requests.post(url, json=PLAYER_CLIENT_ID, headers=headers, timeout=5)
                    
                    if resp.status_code != 404 and resp.status_code != 405:
                        print(f"  ✅ Method {method}: HTTP {resp.status_code}")
                        if resp.status_code == 200:
                            print(f"  Response: {resp.json()}")
                        break
                except:
                    pass
            
        except Exception as e:
            pass

def main():
    print("=" * 60)
    print("PLAYER DEACTIVATION/DELETION TEST")
    print(f"Player: ID={PLAYER_CLIENT_ID}, Email={PLAYER_EMAIL}")
    print("=" * 60)
    
    results = {
        "player": {
            "id": PLAYER_CLIENT_ID,
            "email": PLAYER_EMAIL
        },
        "tests": []
    }
    
    # Test DEV environment
    print("\n🔹 Testing DEV environment")
    dev_success = test_deactivate_clients(ENVIRONMENTS["dev"])
    
    results["tests"].append({
        "environment": "dev",
        "endpoint": "/api/Client/DeactivateClients",
        "method": "POST",
        "success": dev_success
    })
    
    # Test QA environment
    print("\n🔹 Testing QA environment")
    qa_success = test_deactivate_clients(ENVIRONMENTS["qa"])
    
    results["tests"].append({
        "environment": "qa",
        "endpoint": "/api/Client/DeactivateClients",
        "method": "POST",
        "success": qa_success
    })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"\nDEV Environment: {'✅ WORKS' if dev_success else '❌ FAILED'}")
    print(f"QA Environment: {'✅ WORKS' if qa_success else '❌ FAILED'}")
    
    if dev_success:
        print(f"\n✅ FOUND WORKING ENDPOINT:")
        print(f"   POST /api/Client/DeactivateClients")
        print(f"   Parameters: Array of client IDs (e.g., [3563473])")
        print(f"   Headers: UserId header required")
        print(f"   Authentication: Admin credentials")
    else:
        print(f"\n⚠️ DEV environment failed, check API or credentials")
    
    if qa_success:
        print(f"\n✅ QA Environment works!")
        print(f"   URL: {ENVIRONMENTS['qa']}/Client/DeactivateClients")
    
    # Save results
    output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-752/player-deletion-test.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Example curl command
    if dev_success:
        print("\n" + "=" * 60)
        print("EXAMPLE CURL COMMAND")
        print("=" * 60)
        
        print(f"\n# Deactivate player {PLAYER_CLIENT_ID}")
        print(f"curl -X POST \"{ENVIRONMENTS['dev']}/Client/DeactivateClients\" \\")
        print(f"  -H \"Content-Type: application/json\" \\")
        print(f"  -H \"UserId: {ADMIN_USER_ID}\" \\")
        print(f"  -d \"[{PLAYER_CLIENT_ID}]\"")

if __name__ == "__main__":
    main()
