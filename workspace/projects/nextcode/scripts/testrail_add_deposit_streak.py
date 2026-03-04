#!/usr/bin/env python3
"""
Script to add Deposit Streak test cases to TestRail
Creates a subsection "Deposit Streak" under "Bonuses" section.
"""

import json
import subprocess

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

# Deposit Streak test cases (6 tests)
deposit_streak_cases = [
    {
        'title': 'Basic Flow — 2 Deposits → Bonus → Claim',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>New player with non‑test email (e.g., john.doe123@nextcode.tech)</p><p>Player has at least $60 USD balance (or payment method ready for two $30 deposits)</p><p>Deposit Streak campaign is active on the environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the new player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Navigate to Bonuses page</p>', 'expected': '<p>Bonuses page loads</p>'},
            {'content': '<p>Make first deposit of $30 USD through the payment UI</p>', 'expected': '<p>Deposit succeeds, balance updates</p>'},
            {'content': '<p>Refresh Bonuses page</p>', 'expected': '<p>No Deposit Streak bonus card appears</p>'},
            {'content': '<p>Make second deposit of $30 USD</p>', 'expected': '<p>Deposit succeeds, balance updates</p>'},
            {'content': '<p>Refresh Bonuses page</p>', 'expected': '<p>Deposit Streak bonus card appears with status "Ready to claim"</p>'},
            {'content': '<p>Click the "Claim" button on the bonus card</p>', 'expected': '<p>Toast notification "Bonus claimed successfully" appears</p>'},
            {'content': '<p>Verify player balance</p>', 'expected': '<p>Balance increases by the bonus amount</p>'},
            {'content': '<p>Return to Bonuses page</p>', 'expected': '<p>Deposit Streak card is no longer visible</p>'},
        ]
    },
    {
        'title': 'Deposit Below Minimum Amount — No Bonus',
        'priority_id': 4,  # Medium
        'type_id': 11,
        'custom_preconds': '<p>New player with non‑test email</p><p>Player has at least $58 USD balance</p><p>Minimum deposit for Deposit Streak is $30 (confirm with campaign settings)</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the new player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Make first deposit of $29 USD (below minimum)</p>', 'expected': '<p>Deposit succeeds, balance updates</p>'},
            {'content': '<p>Make second deposit of $29 USD</p>', 'expected': '<p>Deposit succeeds, balance updates</p>'},
            {'content': '<p>Navigate to Bonuses page</p>', 'expected': '<p>No Deposit Streak bonus card appears</p>'},
            {'content': '<p>(Optional) Make a third deposit of $30 USD</p>', 'expected': '<p>Bonus still does not appear (only consecutive deposits ≥ $30 count)</p>'},
        ]
    },
    {
        'title': 'Full Cycle — 10 Deposits (4 Bonuses)',
        'priority_id': 4,  # Medium
        'type_id': 11,
        'custom_preconds': '<p>New player with non‑test email</p><p>Player has at least $300 USD balance (or payment method for 10 deposits)</p><p>Deposit Streak campaign active</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the new player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Make 10 consecutive deposits of $30 USD each</p>', 'expected': '<p>All deposits succeed</p>'},
            {'content': '<p>After each deposit, refresh Bonuses page</p>', 'expected': '<p>Track when bonus cards appear</p>'},
            {'content': '<p>Verify bonus appearance pattern</p>', 'expected': '<p>Bonuses appear <strong>only</strong> after deposits 2, 4, 8, 10</p>'},
            {'content': '<p>Claim each bonus as it appears</p>', 'expected': '<p>Each bonus is claimed successfully, balance increases accordingly</p>'},
            {'content': '<p>After 10 deposits, count total bonuses claimed</p>', 'expected': '<p>Exactly 4 bonuses have been claimed</p>'},
        ]
    },
    {
        'title': 'Different Currencies (If Supported)',
        'priority_id': 4,  # Low (1:Critical, 2:High, 3:Medium, 4:Low)
        'type_id': 11,
        'custom_preconds': '<p>Deposit Streak campaign supports multiple currencies (USD, EUR, CAD)</p><p>Player registered with supported non‑USD currency</p><p>Player has sufficient balance in that currency</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Make two deposits in the non‑USD currency (≥ minimum equivalent)</p>', 'expected': '<p>Deposits succeed</p>'},
            {'content': '<p>Navigate to Bonuses page</p>', 'expected': '<p>Deposit Streak bonus card appears with correct currency symbol</p>'},
            {'content': '<p>Claim the bonus</p>', 'expected': '<p>Bonus amount is credited in the player’s currency</p>'},
        ]
    },
    {
        'title': 'Wallet Correction Does Not Trigger Bonus',
        'priority_id': 4,  # Low
        'type_id': 11,
        'custom_preconds': '<p>New player with non‑test email</p><p>Access to BackOffice/Wallet API for balance corrections</p>',
        'custom_steps_separated': [
            {'content': '<p>Login as the player</p>', 'expected': '<p>Player logged in successfully</p>'},
            {'content': '<p>Via Wallet API, credit $30 to player’s balance (CreateDebitCorrection)</p>', 'expected': '<p>Balance increases</p>'},
            {'content': '<p>Repeat with another $30 credit</p>', 'expected': '<p>Balance increases again</p>'},
            {'content': '<p>Navigate to Bonuses page</p>', 'expected': '<p><strong>No</strong> Deposit Streak bonus card appears</p>'},
        ]
    },
    {
        'title': 'Bonus Card Elements & States',
        'priority_id': 4,  # Low
        'type_id': 11,
        'custom_preconds': '<p>Player has triggered a Deposit Streak bonus (after 2 deposits)</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to Bonuses page</p>', 'expected': '<p>Deposit Streak card is visible</p>'},
            {'content': '<p>Check card title</p>', 'expected': '<p>Shows "Deposit Streak" (or campaign‑specific name)</p>'},
            {'content': '<p>Check bonus amount</p>', 'expected': '<p>Displays correct amount (e.g., "$5")</p>'},
            {'content': '<p>Check claim button</p>', 'expected': '<p>Button is enabled, reads "Claim"</p>'},
            {'content': '<p>Check any progress indicator</p>', 'expected': '<p>If present, shows correct progress (e.g., "2/2 deposits")</p>'},
            {'content': '<p>Click "Claim"</p>', 'expected': '<p>Button becomes disabled, toast "Bonus claimed successfully" appears</p>'},
            {'content': '<p>Refresh page</p>', 'expected': '<p>Card disappears</p>'},
        ]
    },
]

def main():
    print("🚀 Adding Deposit Streak test cases to TestRail")
    
    # Check if Deposit Streak section already exists
    print("🔍 Looking for existing 'Deposit Streak' section...")
    existing = find_section('Deposit Streak', parent_id=PARENT_SECTION_ID)
    if existing:
        section_id = existing['id']
        print(f"✅ Using existing section ID: {section_id}")
    else:
        print("📁 Creating 'Deposit Streak' subsection under 'Bonuses'...")
        section_id = create_section('Deposit Streak', parent_id=PARENT_SECTION_ID)
        if not section_id:
            print("❌ Cannot continue without section")
            return
    
    # Add test cases
    print(f"📝 Adding {len(deposit_streak_cases)} test cases...")
    for i, case in enumerate(deposit_streak_cases):
        print(f"[{i+1}/{len(deposit_streak_cases)}] {case['title']}")
        add_test_case(section_id, case)
    
    print("🎉 Deposit Streak test cases added successfully!")

if __name__ == '__main__':
    main()