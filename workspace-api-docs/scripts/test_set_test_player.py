#!/usr/bin/env python3
"""
Test marking player as TEST player (alternative to deletion)
This allows testing with clean state without deleting player
"""

import requests
import json

BACKOFFICE_API_URL = "https://adminwebapi.dev.sofon.one/api"
ADMIN_USER_ID = 560
PLAYER_CLIENT_ID = 3563473
PLAYER_EMAIL = "pandasen@echoprx.cc"

def test_set_client_as_test():
    """Test setClientAsTest endpoint"""
    print("=" * 60)
    print("TESTING: Set Client as Test Player")
    print("=" * 60)
    
    url = f"{BACKOFFICE_API_URL}/Client/SetTest"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(ADMIN_USER_ID)
    }
    
    print(f"\nURL: {url}")
    print(f"UserId: {ADMIN_USER_ID}")
    print(f"Player ID: {PLAYER_CLIENT_ID}")
    print(f"Email: {PLAYER_EMAIL}")
    
    try:
        response = requests.post(url, json=PLAYER_CLIENT_ID, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("ResponseCode") == 0 or result.get("ResponseCode") == "Success":
                print(f"\n✅ SUCCESS: Player marked as TEST!")
                print(f"   This allows testing without deleting the player")
                return True
            else:
                print(f"\n⚠️ API returned error code: {result.get('ResponseCode')}")
                print(f"Description: {result.get('Description')}")
                return False
        else:
            print(f"\n❌ FAILED: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_get_client_details():
    """Check current client state"""
    print("\n" + "=" * 60)
    print("CHECKING: Current Client State")
    print("=" * 60)
    
    url = f"{BACKOFFICE_API_URL}/Client/GetClientById"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(ADMIN_USER_ID)
    }
    
    try:
        response = requests.post(url, json=PLAYER_CLIENT_ID, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get("ResponseObject")
        else:
            print(f"\n❌ Failed: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("MARK PLAYER AS TEST - ALTERNATIVE TO DELETION")
    print(f"Player: ID={PLAYER_CLIENT_ID}, Email={PLAYER_EMAIL}")
    print("=" * 60)
    
    results = {
        "player": {
            "id": PLAYER_CLIENT_ID,
            "email": PLAYER_EMAIL
        },
        "tests": []
    }
    
    # Step 1: Check current state
    current_state = test_get_client_details()
    
    if current_state:
        is_test = current_state.get("IsTest", False)
        state = current_state.get("State", "Unknown")
        
        print(f"\n📋 Current State:")
        print(f"   IsTest: {is_test}")
        print(f"   State: {state}")
    
    # Step 2: Set as test
    success = test_set_client_as_test()
    
    results["tests"].append({
        "endpoint": "/api/Client/SetTest",
        "method": "POST",
        "success": success,
        "notes": "Marks player as TEST - allows testing without deletion"
    })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if success:
        print(f"\n✅ WORKING ENDPOINT FOUND:")
        print(f"   POST /api/Client/SetTest")
        print(f"   Parameters: Client ID (number)")
        print(f"   Headers: UserId header required")
        print(f"   ")
        print(f"   📝 BENEFIT: Doesn't delete player, just marks as TEST")
        print(f"   📝 ALTERNATIVE: Test account can still be used with isTest=true filter")
    else:
        print(f"\n⚠️ Test failed")
        print(f"   Check API endpoint and credentials")
    
    # Save results
    output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-752/player-setas-test.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
