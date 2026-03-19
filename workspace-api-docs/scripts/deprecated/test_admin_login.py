#!/usr/bin/env python3
"""
Test AdminWebAPI Login to get proper UserId
"""

import requests
import json

BACKOFFICE_API_URL = "https://adminwebapi.dev.sofon.one/api"
ADMIN_EMAIL = "admin@minebit.com"
ADMIN_PASSWORD = "Admin123!@#"

def test_login():
    """Test AdminWebAPI login"""
    print("=" * 60)
    print("TESTING ADMINWEBAPI LOGIN")
    print("=" * 60)
    
    url = f"{BACKOFFICE_API_URL}/Authentication/Login"
    
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    print(f"\nURL: {url}")
    print(f"Email: {ADMIN_EMAIL}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if login successful
            if result.get("ResponseCode") == 0 or result.get("ResponseCode") == "Success":
                user_data = result.get("ResponseObject", {})
                user_id = user_data.get("Id")
                email = user_data.get("Email")
                
                print(f"\n✅ LOGIN SUCCESSFUL!")
                print(f"   User ID: {user_id}")
                print(f"   Email: {email}")
                
                return user_id
            else:
                print(f"\n⚠️ Login failed: {result.get('Description')}")
                return None
        else:
            print(f"\n❌ Login failed with HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_deactivate_with_user_id(user_id):
    """Test deactivation with correct UserId"""
    print("\n" + "=" * 60)
    print("TESTING DEACTIVATION WITH LOGIN USER ID")
    print("=" * 60)
    
    url = f"{BACKOFFICE_API_URL}/Client/DeactivateClients"
    
    headers = {
        "Content-Type": "application/json",
        "UserId": str(user_id)  # Use logged-in user ID
    }
    
    payload = [3563473]
    
    print(f"\nURL: {url}")
    print(f"UserId: {user_id}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"\nHTTP Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("ResponseCode") == 0 or result.get("ResponseCode") == "Success":
                print(f"\n✅ DEACTIVATION SUCCESSFUL!")
                return True
            else:
                print(f"\n⚠️ Deactivation failed: {result.get('Description')}")
                return False
        else:
            print(f"\n❌ Deactivation failed with HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("ADMINWEBAPI LOGIN & DEACTIVATION TEST")
    print("=" * 60)
    
    # Step 1: Login
    user_id = test_login()
    
    if not user_id:
        print("\n❌ Cannot proceed without successful login")
        return
    
    # Step 2: Deactivate
    success = test_deactivate_with_user_id(user_id)
    
    # Example command
    if success:
        print("\n" + "=" * 60)
        print("EXAMPLE CURL COMMAND")
        print("=" * 60)
        
        print(f"\n# Step 1: Login")
        print(f"curl -X POST \"{BACKOFFICE_API_URL}/Authentication/Login\" \\")
        print(f"  -H \"Content-Type: application/json\" \\")
        print(f"  -d '{{\"email\": \"{ADMIN_EMAIL}\", \"password\": \"{ADMIN_PASSWORD}\"}}'")
        
        print(f"\n# Step 2: Deactivate player (use UserId from step 1)")
        print(f"curl -X POST \"{BACKOFFICE_API_URL}/Client/DeactivateClients\" \\")
        print(f"  -H \"Content-Type: application/json\" \\")
        print(f"  -H \"UserId: <YOUR_USER_ID>\" \\")
        print(f"  -d \"[3563473]\"")

if __name__ == "__main__":
    main()
