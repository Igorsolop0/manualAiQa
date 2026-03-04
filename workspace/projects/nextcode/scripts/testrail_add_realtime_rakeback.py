#!/usr/bin/env python3
"""
Script to add Realtime Rakeback test cases to TestRail
Creates a subsection "Realtime Rakeback" under "Bonuses" section.
"""

import json
import subprocess
import sys

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Project and parent section IDs
PROJECT_ID = 1
SUITE_ID = 631          # from Regular Bonuses Section
PARENT_SECTION_ID = 6216  # "Bonuses" section

def call_api(method, endpoint, data=None):
    """Make API call using curl"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', method,
    ]
    if data:
        cmd.extend(['-d', json.dumps(data)])
    cmd.append(f"{TESTRAIL_URL}/index.php?/api/v2/{endpoint}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"JSON decode error: {result.stdout}")
            return None
    else:
        print(f"No output from API call: {result.stderr}")
        return None

def get_sections():
    """Get all sections in suite"""
    response = call_api('GET', f'get_sections/{PROJECT_ID}&suite_id={SUITE_ID}')
    if response and 'sections' in response:
        return response['sections']
    return None

def find_section(name, parent_id=None):
    """Find section by name and optional parent_id"""
    sections = get_sections()
    if not sections:
        return None
    for section in sections:
        if section['name'] == name:
            if parent_id is None or section.get('parent_id') == parent_id:
                return section
    return None

def create_section(name, parent_id=None):
    """Create a new section"""
    data = {
        'suite_id': SUITE_ID,
        'name': name,
    }
    if parent_id:
        data['parent_id'] = parent_id
    
    result = call_api('POST', f'add_section/{PROJECT_ID}', data)
    if result and 'id' in result:
        print(f"✅ Section '{name}' created with ID {result['id']}")
        return result['id']
    else:
        print(f"❌ Failed to create section '{name}': {result}")
        return None

def add_test_case(section_id, case_data):
    """Add a test case to a section"""
    result = call_api('POST', f'add_case/{section_id}', case_data)
    if result and 'id' in result:
        print(f"  ✅ Case added: {case_data['title']} (ID: {result['id']})")
        return result['id']
    else:
        print(f"  ❌ Failed to add case: {case_data['title']} - {result}")
        return None

# Realtime Rakeback test cases (5 E2E tests)
realtime_rakeback_cases = [
    {
        'title': 'Realtime Rakeback – basic wager and claim flow',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Player registered and has balance ≥ $100 real money (Unused balance)</p><p>Rakeback campaign is active on the environment</p><p>Player has no active bonuses</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Navigate to any real‑money game (e.g., slots, trading game)</p>', 'expected': '<p>Game loads</p>'},
            {'content': '<p>Place a $100 real‑money wager (not bonus money)</p>', 'expected': '<p>Wager placed successfully</p>'},
            {'content': '<p>Wait 30 minutes (rakeback accrual interval)</p>', 'expected': '<p>Rakeback batch processing completes</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Check for Rakeback bonus card</p>', 'expected': '<p>Rakeback card appears with status "Ready for claim"</p>'},
            {'content': '<p>Verify reward amount</p>', 'expected': '<p>Amount displayed matches formula: $100 × House Edge × 10%</p>'},
            {'content': '<p>Click the "Claim" button</p>', 'expected': '<p>Toast notification "Bonus claimed successfully" appears</p>'},
            {'content': '<p>Verify player balance</p>', 'expected': '<p>Unused balance increases by the reward amount</p>'},
            {'content': '<p>Return to Bonuses page</p>', 'expected': '<p>Rakeback card changes to "Play Game" state with 30‑minute timer</p>'},
        ]
    },
    {
        'title': 'Realtime Rakeback – different House Edge per game category',
        'priority_id': 3,  # High
        'type_id': 11,
        'custom_preconds': '<p>Player has balance ≥ $200 real money (Unused balance)</p><p>Rakeback campaign active</p><p>No active bonuses</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Navigate to a classic slot game (e.g., Book of Dead)</p>', 'expected': '<p>Slot game loads</p>'},
            {'content': '<p>Place a $100 real‑money wager</p>', 'expected': '<p>Wager placed</p>'},
            {'content': '<p>Wait 30 minutes</p>', 'expected': '<p>Rakeback accrual interval passes</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Note the reward amount for slot game</p>', 'expected': '<p>Amount A recorded (e.g., $0.25)</p>'},
            {'content': '<p>Claim the bonus (optional)</p>', 'expected': '<p>Bonus claimed, balance updated</p>'},
            {'content': '<p>Navigate to a trading game (e.g., trade‑smarter‑1000x)</p>', 'expected': '<p>Trading game loads</p>'},
            {'content': '<p>Place a $100 real‑money wager</p>', 'expected': '<p>Wager placed</p>'},
            {'content': '<p>Wait 30 minutes</p>', 'expected': '<p>Rakeback accrual interval passes</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Note the reward amount for trading game</p>', 'expected': '<p>Amount B recorded (e.g., $0.0278)</p>'},
            {'content': '<p>Compare amounts and calculate House Edge</p>', 'expected': '<p>House Edge for slots = (A × 100) / ($100 × 10%); for trading = (B × 100) / ($100 × 10%)</p>'},
        ]
    },
    {
        'title': 'Realtime Rakeback – bonus‑money wagers do NOT trigger rakeback',
        'priority_id': 4,  # Medium
        'type_id': 11,
        'custom_preconds': '<p>Player has bonus balance (AvailableBonus) ≥ $100 and real balance (Unused) = $0</p><p>Rakeback campaign active</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Verify Unused balance is $0, bonus balance ≥ $100</p>', 'expected': '<p>Correct balances displayed</p>'},
            {'content': '<p>Navigate to any game</p>', 'expected': '<p>Game loads</p>'},
            {'content': '<p>Place a $100 wager using bonus money</p>', 'expected': '<p>Wager placed using bonus balance</p>'},
            {'content': '<p>Wait 30 minutes</p>', 'expected': '<p>Rakeback accrual interval passes</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Check for Rakeback card</p>', 'expected': '<p>No Rakeback card appears (or amount $0)</p>'},
            {'content': '<p>Verify player balances</p>', 'expected': '<p>No unexpected rakeback credited to Unused balance</p>'},
        ]
    },
    {
        'title': 'Realtime Rakeback – UI states and timers after claim',
        'priority_id': 4,  # Medium
        'type_id': 11,
        'custom_preconds': '<p>Player has just received a rakeback reward (Ready for claim)</p><p>Player has not yet claimed it</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Check Rakeback card state before claim</p>', 'expected': '<p>State: "Ready for claim"; button: "Claim $X"; amount displayed</p>'},
            {'content': '<p>Click "Claim $X" button</p>', 'expected': '<p>Claim successful; toast notification appears</p>'},
            {'content': '<p>Check Rakeback card state after claim (1‑2 minutes)</p>', 'expected': '<p>Button changes to "Play Game"; timer appears (~30 minutes); nextAvailableAt field populated</p>'},
            {'content': '<p>Refresh the page</p>', 'expected': '<p>State persists ("Play Game" + timer)</p>'},
            {'content': '<p>Check Network tab for ClaimBonus request</p>', 'expected': '<p>POST request to ClaimBonus endpoint returns 200 OK</p>'},
        ]
    },
    {
        'title': 'Realtime Rakeback – new accrual cycle after timer ends',
        'priority_id': 3,  # High
        'type_id': 11,
        'custom_preconds': '<p>Player has just claimed a rakeback reward (timer active)</p><p>Player has additional balance ≥ $100 for new wager</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Wait for the 30‑minute timer to complete (or simulate timer end)</p>', 'expected': '<p>Timer expires; Rakeback card shows "Bonus available" or disappears if no new wagers</p>'},
            {'content': '<p>Place a new $100 real‑money wager in any game</p>', 'expected': '<p>Wager placed</p>'},
            {'content': '<p>Wait 30 minutes</p>', 'expected': '<p>Rakeback accrual interval passes</p>'},
            {'content': '<p>Navigate to /bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Check for new Rakeback reward</p>', 'expected': '<p>New Rakeback card appears with amount based on new wager only</p>'},
            {'content': '<p>Claim the new reward</p>', 'expected': '<p>Claim successful; Unused balance increases</p>'},
            {'content': '<p>Verify that wagers placed during the timer period were not counted</p>', 'expected': '<p>Reward amount corresponds only to wagers after timer ended</p>'},
        ]
    },
]

def main():
    print("🚀 Adding Realtime Rakeback test cases to TestRail")
    
    # Check if Realtime Rakeback section already exists
    print("🔍 Looking for existing 'Realtime Rakeback' section...")
    existing = find_section('Realtime Rakeback', parent_id=PARENT_SECTION_ID)
    if existing:
        section_id = existing['id']
        print(f"✅ Using existing section ID: {section_id}")
    else:
        print("📁 Creating 'Realtime Rakeback' subsection under 'Bonuses'...")
        section_id = create_section('Realtime Rakeback', parent_id=PARENT_SECTION_ID)
        if not section_id:
            print("❌ Cannot continue without section")
            return
    
    # Add test cases
    print(f"📝 Adding {len(realtime_rakeback_cases)} test cases...")
    for i, case in enumerate(realtime_rakeback_cases):
        print(f"[{i+1}/{len(realtime_rakeback_cases)}] {case['title']}")
        add_test_case(section_id, case)
    
    print("🎉 Realtime Rakeback test cases added successfully!")
    print(f"\n📊 Summary:")
    print(f"   Project ID: {PROJECT_ID}")
    print(f"   Suite ID: {SUITE_ID}")
    print(f"   Parent Section ID: {PARENT_SECTION_ID}")
    print(f"   New Section ID: {section_id}")
    print(f"   Test Cases Added: {len(realtime_rakeback_cases)}")

if __name__ == '__main__':
    main()