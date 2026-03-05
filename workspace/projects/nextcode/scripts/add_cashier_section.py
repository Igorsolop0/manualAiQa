#!/usr/bin/env python3
"""
Script to create Cashier Navigation section in TestRail for Minebit
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Minebit Project Configuration
PROJECT_ID = 1
SUITE_ID = 631  # Bonuses suite (parent for Cashier section)

def create_section(name):
    """Create a new section under Bonuses suite"""
    data = {
        'suite_id': SUITE_ID,
        'name': name,
        'description': f'Test cases for {name}'
    }
    
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_section/{PROJECT_ID}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        try:
            response = json.loads(result.stdout)
            if 'error' in response:
                print(f"❌ Error creating section '{name}': {response['error']}")
                return None
            else:
                print(f"✅ Section '{name}' created successfully!")
                print(f"   Section ID: {response['id']}")
                return response['id']
        except json.JSONDecodeError:
            print(f"❌ JSON decode error: {result.stdout}")
            return None
    else:
        print(f"❌ No output from API: {result.stderr}")
        return None

def main():
    print("🚀 Creating Cashier Navigation section...")
    
    section_name = "Cashier Navigation"
    section_id = create_section(section_name)
    
    if section_id:
        print(f"\n🎉 SUCCESS! Cashier Navigation section created!")
        print(f"   Section ID: {section_id}")
        print(f"   View: https://nexttcode.testrail.io/index.php?/suites/view/631")
        print(f"   Please use this Section ID to move test cases: {section_id}")
    else:
        print(f"❌ Failed to create section")

if __name__ == '__main__':
    main()
