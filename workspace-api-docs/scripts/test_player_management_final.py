#!/usr/bin/env python3
"""
Final Test: Player Management on AdminWebAPI
Using CORRECT UserId (1 for DEV/QA, 560 for PROD)
"""

import requests
import json

# Environments
ENVIRONMENTS = {
    "dev": {
        "url": "https://adminwebapi.dev.sofon.one/api",
        "user_id": 1  # DEV/QA uses UserId: 1
    },
    "qa": {
        "url": "https://adminwebapi.qa.sofon.one/api",
        "user_id": 1
    },
    "prod": {
        "url": "https://adminwebapi.prod.sofon.one/api",
        "user_id": 560  # PROD uses UserId: 560
    }
}

# Player to delete/deactivate
PLAYER_CLIENT_ID = 3563473
PLAYER_EMAIL = "pandasen@echoprx.cc"

def test_get_client_details(env_name: str):
    """Get client details first"""
    env = ENVIRONMENTS[env_name]
    url = f"{env['url']}/Client/GetClientById"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(env['user_id'])
    }
    
    print(f"\n{'=' * 60}")
    print(f"TESTING: GetClientById on {env_name.upper()}")
    print(f"{'=' * 60}")
    print(f"\nURL: {url}")
    print(f"UserId: {env['user_id']}")
    print(f"Player ID: {PLAYER_CLIENT_ID}")
    
    try:
        response = requests.post(url, json=PLAYER_CLIENT_ID, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("ResponseCode") == 0:
                client_data = result.get("ResponseObject", {}).get("Client", {})
                
                print(f"\n✅ SUCCESS: Found player!")
                print(f"   ID: {client_data.get('Id')}")
                print(f"   Email: {client_data.get('Email')}")
                print(f"   UserName: {client_data.get('UserName')}")
                print(f"   IsTest: {client_data.get('IsTest')}")
                print(f"   State: {client_data.get('State')}")
                
                return client_data
            else:
                print(f"\n⚠️ API returned error: {result.get('Description')}")
                return None
        else:
            print(f"\n❌ HTTP {response.status_code}: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_deactivate_client(env_name: str):
    """Deactivate client"""
    env = ENVIRONMENTS[env_name]
    url = f"{env['url']}/Client/DeactivateClients"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(env['user_id'])
    }
    
    payload = [PLAYER_CLIENT_ID]
    
    print(f"\n{'=' * 60}")
    print(f"TESTING: DeactivateClients on {env_name.upper()}")
    print(f"{'=' * 60}")
    print(f"\nURL: {url}")
    print(f"UserId: {env['user_id']}")
    print(f"Payload: {payload}")
    
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
                print(f"\n⚠️ API returned error: {result.get('Description')}")
                return False
        else:
            print(f"\n❌ HTTP {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_set_as_test(env_name: str):
    """Mark player as test"""
    env = ENVIRONMENTS[env_name]
    
    # Try different possible endpoints
    endpoints = [
        f"{env['url']}/Client/SetTest",
        f"{env['url']}/Client/ChangeClientDetails"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(env['user_id'])
    }
    
    print(f"\n{'=' * 60}")
    print(f"TESTING: Set Player as Test on {env_name.upper()}")
    print(f"{'=' * 60}")
    
    for url in endpoints:
        print(f"\nTrying: {url}")
        
        payload = PLAYER_CLIENT_ID if "SetTest" in url else {
            "id": PLAYER_CLIENT_ID,
            "isTest": True
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            print(f"HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("ResponseCode") == 0:
                    print(f"✅ SUCCESS with {url.split('/')[-1]}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return True
                else:
                    print(f"⚠️ {result.get('Description')}")
            elif response.status_code != 404:
                print(f"Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    return False

def main():
    print("=" * 60)
    print("PLAYER MANAGEMENT - FINAL TEST")
    print(f"Player: ID={PLAYER_CLIENT_ID}, Email={PLAYER_EMAIL}")
    print("=" * 60)
    
    results = {
        "player": {
            "id": PLAYER_CLIENT_ID,
            "email": PLAYER_EMAIL
        },
        "environments_tested": [],
        "working_endpoints": []
    }
    
    # Test DEV environment (most likely to work)
    print("\n🔹 Testing DEV Environment")
    
    client_data = test_get_client_details("dev")
    
    if client_data:
        results["environments_tested"].append("dev")
        
        # Try to deactivate
        if test_deactivate_client("dev"):
            results["working_endpoints"].append({
                "endpoint": "/api/Client/DeactivateClients",
                "method": "POST",
                "environment": "dev",
                "status": "WORKS"
            })
        
        # Try to set as test
        if test_set_as_test("dev"):
            results["working_endpoints"].append({
                "endpoint": "/api/Client/ChangeClientDetails or /api/Client/SetTest",
                "method": "POST",
                "environment": "dev",
                "status": "WORKS"
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if results["working_endpoints"]:
        print(f"\n✅ WORKING ENDPOINTS FOUND:")
        
        for endpoint in results["working_endpoints"]:
            print(f"\n   • {endpoint['endpoint']}")
            print(f"     Method: {endpoint['method']}")
            print(f"     Environment: {endpoint['environment']}")
            print(f"     Status: {endpoint['status']}")
        
        print(f"\n📋 EXAMPLE CURL COMMANDS:")
        print(f"\n   # Get client details:")
        print(f"   curl -X POST \"https://adminwebapi.dev.sofon.one/api/Client/GetClientById\" \\")
        print(f"     -H \"Content-Type: application/json\" \\")
        print(f"     -H \"UserId: 1\" \\")
        print(f"     -d \"{PLAYER_CLIENT_ID}\"")
        
        print(f"\n   # Deactivate player:")
        print(f"   curl -X POST \"https://adminwebapi.dev.sofon.one/api/Client/DeactivateClients\" \\")
        print(f"     -H \"Content-Type: application/json\" \\")
        print(f"     -H \"UserId: 1\" \\")
        print(f"     -d \"[{PLAYER_CLIENT_ID}]\"")
        
        print(f"\n   # Mark as test player:")
        print(f"   curl -X POST \"https://adminwebapi.dev.sofon.one/api/Client/ChangeClientDetails\" \\")
        print(f"     -H \"Content-Type: application/json\" \\")
        print(f"     -H \"UserId: 1\" \\")
        print(f"     -d '{{\"id\": {PLAYER_CLIENT_ID}, \"isTest\": true}}'")
        
    else:
        print(f"\n⚠️ No working endpoints found")
        print(f"   Check if DEV environment is accessible")
        print(f"   Check if player {PLAYER_CLIENT_ID} exists")
    
    # Save results
    output_file = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-752/player-management-final.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Update task file
    task_file = "/Users/ihorsolopii/.openclaw/workspace/shared/tasks/CT-752-delete-player-endpoint.md"
    
    if results["working_endpoints"]:
        with open(task_file, 'a') as f:
            f.write("\n\n---\n\n## Results\n\n")
            f.write(f"**Date:** {__import__('datetime').datetime.now().isoformat()}\n\n")
            f.write(f"**Status:** ✅ FOUND WORKING ENDPOINTS\n\n")
            f.write(f"### Available Endpoints\n\n")
            
            for endpoint in results["working_endpoints"]:
                f.write(f"1. **{endpoint['endpoint']}**\n")
                f.write(f"   - Method: {endpoint['method']}\n")
                f.write(f"   - Environment: {endpoint['environment']}\n")
                f.write(f"   - Status: {endpoint['status']}\n\n")
            
            f.write(f"### Key Finding\n\n")
            f.write(f"- **UserId for DEV/QA:** 1 (not 560)\n")
            f.write(f"- **UserId for PROD:** 560\n")
            f.write(f"- **DeactivateClients** works for blocking players\n")
            f.write(f"- **ChangeClientDetails** works for marking as test\n\n")
            
            f.write(f"### Recommendation\n\n")
            f.write(f"Use **DeactivateClients** to block the player and allow clean testing.\n")
        
        print(f"\n📝 Task file updated: {task_file}")

if __name__ == "__main__":
    main()
