#!/usr/bin/env python3
"""
Script to add Cashier Navigation test cases to TestRail for CT-476
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section ID for Cashier (Minebit)
# Note: Using Profile section (6840) as parent, will create/locate proper cashier section
SECTION_ID = 6840

def add_test_case(case_data):
    """Add a test case to TestRail"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(case_data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{SECTION_ID}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# Test cases for CT-476
test_cases = [
    {
        "title": "Cashier navigation - Select screen",
        "priority_id": 3,  # Normal
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL with wallet modal: /{base_url}/?modal=wallet</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Select screen (method selection) is displayed</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Deposit Crypto",
        "priority_id": 4,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=depositcrypto</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Deposit Crypto step</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Buy Crypto",
        "priority_id": 4,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=buycrypto</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Buy Crypto step</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Buy Crypto with amount prefill",
        "priority_id": 4,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=buycrypto&cashiersum=100</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Buy Crypto step</p>"
            },
            {
                "content": "<p>Check You send input field</p>",
                "expected": "<p>Amount field is pre-filled with 100</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Withdraw Crypto",
        "priority_id": 4,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=withdrawcrypto</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Withdraw Crypto step</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Invalid step (fallback)",
        "priority_id": 2,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=invalid</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Select screen (fallback behavior)</p>"
            },
            {
                "content": "<p>Verify invalid step value is ignored</p>",
                "expected": "<p>Invalid step value is ignored</p>"
            }
        ]
    },
    {
        "title": "Cashier navigation - Deposit Crypto with sum parameter",
        "priority_id": 2,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is registered and logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Minebit URL: /{base_url}/?modal=wallet&cashierstep=depositcrypto&cashiersum=500</p>",
                "expected": "<p>Wallet modal opens</p>"
            },
            {
                "content": "<p>Verify that Wallet modal opens</p>",
                "expected": "<p>Modal opens on Deposit Crypto step</p>"
            },
            {
                "content": "<p>Check for any amount input field</p>",
                "expected": "<p>Sum parameter is ignored (no amount field on depositcrypto step)</p>"
            }
        ]
    }
]

# Add test cases
print(f"Adding {len(test_cases)} test cases to TestRail...")

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result['id']}")
    
print("\nDone!")
