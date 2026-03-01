#!/usr/bin/env python3
"""Test TestRail authentication with different API keys."""

import base64
import requests
import sys

# Test both keys
KEYS = [
    ("9HzAh7TTACJ1Bl./vt5c-Nm5PMePLW7szuzFvyFDV", "from .testrail_config"),
    ("WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT", "from old testrail_api.py"),
]

EMAIL = "ihor.so@nextcode.tech"
URL = "https://nexttcode.testrail.io/index.php?/api/v2/get_projects"

for api_key, source in KEYS:
    print(f"\n🔑 Testing API key from {source}:")
    print(f"   Key: {api_key[:10]}...{api_key[-10:]}")
    
    auth_string = f"{EMAIL}:{api_key}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_bytes}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! API key works!")
            projects = response.json()
            print(f"   Found {len(projects)} project(s)")
            for project in projects[:3]:
                print(f"     - {project['id']}: {project['name']}")
            if len(projects) > 3:
                print(f"     ... and {len(projects) - 3} more")
            break
        else:
            print(f"   ❌ Failed: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("If both keys fail, you may need to:")
print("1. Generate a new API key in TestRail")
print("2. Check if account is active")
print("3. Check network/VPN access")