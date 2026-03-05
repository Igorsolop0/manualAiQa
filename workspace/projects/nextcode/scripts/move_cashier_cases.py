#!/usr/bin/env python3
"""
Script to move Cashier Navigation test cases from Profile section to Cashier Navigation section
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section IDs
SOURCE_SECTION_ID = 6840  # Profile/Wallet modal (wrong section)
DEST_SECTION_ID = 7216    # Cashier Navigation (new correct section)

def get_cases(section_id):
    """Get all test cases in a section"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        f"{TESTRAIL_URL}/index.php?/api/v2/get_cases/{section_id}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        try:
            response = json.loads(result.stdout)
            if 'cases' in response:
                return response['cases']
            return []
        except json.JSONDecodeError:
            print(f"JSON decode error: {result.stdout}")
            return []
    else:
        print(f"No output from API call: {result.stderr}")
        return []

def move_case(case_id, destination_section_id):
    """Move a test case to another section"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        f"{TESTRAIL_URL}/index.php?/api/v2/move_case/{case_id}",
        '-d', json.dumps({
            'section_id': destination_section_id
        })
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        try:
            response = json.loads(result.stdout)
            if 'error' in response:
                print(f"  ❌ Error moving case {case_id}: {response['error']}")
                return False
            else:
                print(f"  ✅ Moved case {case_id} to section {destination_section_id}")
                return True
        except json.JSONDecodeError:
            print(f"JSON decode error: {result.stdout}")
            return False
    else:
        print(f" ❌ No output from API call: {result.stderr}")
        return False

def main():
    print("🚀 Moving Cashier Navigation test cases to correct section...")
    
    # Get all cases from source section
    print("📋 Getting test cases from source section...")
    cases = get_cases(SOURCE_SECTION_ID)
    
    if not cases:
        print(f"❌ No cases found in source section {SOURCE_SECTION_ID}")
        return
    
    print(f"📊 Found {len(cases)} test cases to move")
    
    # Move each case to destination section
    success_count = 0
    failed_count = 0
    
    for i, case in enumerate(cases, 1):
        title = case.get('title', 'Unknown')
        print(f"[{i}/{len(cases)}] Moving: {title}")
        
        if move_case(case['id'], DEST_SECTION_ID):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n✅ Done! {success_count} moved, {failed_count} failed")
    print(f"\n🔗 Test cases are now in correct section!")
    print(f"View: https://nexttcode.testrail.io/index.php?/suites/view/631&group_by=cases:section_id&group_order=asc&display=tree&display_deleted_cases=0&group_id=7216")

if __name__ == '__main__':
    main()
