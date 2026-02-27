#!/usr/bin/env python3
"""
Script to add missing Regular Bonuses test cases to TestRail
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section ID for "Regular Bonuses Section"
SECTION_ID = 6478

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

# Test cases to add
test_cases = [
    {
        "title": "Timer — Daily Bonus Countdown",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player with Daily bonus in \"Waiting for reward\" state</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Daily card visible</p>"
            },
            {
                "content": "<p>Note timer value and progress bar %</p>",
                "expected": "<p>Timer: \"XXh:YYm:ZZs\", Progress bar shows time elapsed %</p>"
            },
            {
                "content": "<p>Wait 1 minute and refresh page</p>",
                "expected": "<p>Timer decreased by ~1 minute, progress bar % increased</p>"
            }
        ]
    },
    {
        "title": "Timer — Weekly Bonus (Next Saturday)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Current day is NOT Saturday</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Weekly card visible</p>"
            },
            {
                "content": "<p>Check timer format and days count</p>",
                "expected": "<p>Timer: \"Xd XXh:YYm:ZZs\", days match calculation to next Saturday</p>"
            },
            {
                "content": "<p>Check frequency label and availability date</p>",
                "expected": "<p>Label: \"Every Saturday\", Date shows next Saturday: \"DD.MM.YY\"</p>"
            }
        ]
    },
    {
        "title": "Timer — Monthly Bonus (1st of Month)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Current date is NOT 1st of month</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Monthly card visible</p>"
            },
            {
                "content": "<p>Check timer format and days count</p>",
                "expected": "<p>Timer: \"Xd XXh:YYm:ZZs\", days match calculation to 1st of next month</p>"
            },
            {
                "content": "<p>Check frequency label and availability date</p>",
                "expected": "<p>Label: \"Every 1st of month\", Date shows 1st of next month</p>"
            }
        ]
    },
    {
        "title": "Cashback — Parallel Claim with Active Bonus (CT-45 Critical)",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus (e.g., Welcome Pack)</p><p>Player has Cashback in \"Ready for claim\" state</p><p>Tuesday or Friday</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as test player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses and verify active bonus exists</p>",
                "expected": "<p>Active bonus visible</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses and check Cashback shows \"Ready for claim\" with amount</p>",
                "expected": "<p>Cashback card shows \"Ready for claim\" state with amount displayed</p>"
            },
            {
                "content": "<p>Click \"Claim $X\" on Cashback</p>",
                "expected": "<p>Claim successful, amount credited to real balance</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>ORIGINAL BONUS STILL ACTIVE (CT-45 — parallel claim allowed)</p>"
            }
        ]
    },
    {
        "title": "Weekly — Parallel Claim with Active Bonus",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus</p><p>Player has Weekly in \"Ready for claim\" state</p><p>Saturday (Weekly calculation day)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as test player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses and verify active bonus exists</p>",
                "expected": "<p>Active bonus visible</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses and check Weekly shows \"Ready for claim\" with amount</p>",
                "expected": "<p>Weekly card shows \"Ready for claim\" state with amount displayed</p>"
            },
            {
                "content": "<p>Click \"Claim $X\" on Weekly</p>",
                "expected": "<p>Claim successful, amount credited to real balance</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>Original bonus still active (CT-45 — parallel claim allowed for ALL Regular Bonuses)</p>"
            }
        ]
    },
    {
        "title": "Monthly — Parallel Claim with Active Bonus",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus</p><p>Player Loyalty Level ≥ 2</p><p>Player has Monthly in \"Ready for claim\" state</p><p>1st day of month</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as test player (Level 2+)</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses and verify active bonus exists</p>",
                "expected": "<p>Active bonus visible</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses and check Monthly shows \"Ready for claim\" with amount</p>",
                "expected": "<p>Monthly card shows \"Ready for claim\" state with amount displayed</p>"
            },
            {
                "content": "<p>Click \"Claim $X\" on Monthly</p>",
                "expected": "<p>Claim successful, amount credited to real balance</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>Original bonus still active (CT-45 — parallel claim allowed)</p>"
            }
        ]
    },
    {
        "title": "Cashback — No Net Loss = No Bonus",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has profit (won more than lost)</p><p>Tuesday or Friday</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player with profit</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Calculate: deposits - withdrawals - balance = negative (profit)</p>",
                "expected": "<p>Net loss calculation shows negative value (profit)</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Cashback card visible</p>"
            },
            {
                "content": "<p>Check Cashback state and amount</p>",
                "expected": "<p>State = \"Waiting for reward\" (no amount), timer shows countdown to next period, no claim button</p>"
            }
        ]
    },
    {
        "title": "Monthly — Loyalty Level Requirement",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player with Loyalty Level 1</p><p>1st day of month</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as Level 1 player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Monthly card visible</p>"
            },
            {
                "content": "<p>Check Monthly card state</p>",
                "expected": "<p>State = \"Waiting for reward\" or locked state</p>"
            },
            {
                "content": "<p>Check info modal (click info button)</p>",
                "expected": "<p>Modal shows \"Available from Loyalty Level 2\"</p>"
            },
            {
                "content": "<p>Increase Loyalty Level to 2 and refresh page</p>",
                "expected": "<p>Monthly shows \"Ready for claim\" with amount</p>"
            }
        ]
    },
    {
        "title": "Multiple Regular Bonuses — Claim All in One Session",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has multiple Regular Bonuses in \"Ready for claim\" state: Daily, Cashback, Weekly, Monthly</p><p>Player Loyalty Level ≥ 2</p><p>Player has active bonus</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses and verify active bonus exists</p>",
                "expected": "<p>Active bonus visible</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses and check all 4 cards show \"Ready for claim\" with amounts</p>",
                "expected": "<p>All 4 cards show amounts: Daily $X, Cashback $Y, Weekly $Z, Monthly $W</p>"
            },
            {
                "content": "<p>Claim Daily, Cashback, Weekly, Monthly one by one</p>",
                "expected": "<p>All claims successful, balance increased by total amount</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>ORIGINAL BONUS STILL ACTIVE (CT-45)</p>"
            },
            {
                "content": "<p>Check Regular Bonuses page</p>",
                "expected": "<p>All cards show \"Waiting for reward\" state</p>"
            }
        ]
    },
    {
        "title": "Info Modal — Bonus Details Verification",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page</p>",
                "expected": "<p>Page loads</p>"
            },
            {
                "content": "<p>Click info (ℹ) on Cashback card</p>",
                "expected": "<p>Modal opens with: description, frequency \"Twice a week\" (Tue, Fri), cashback %, minimum amount $0.3</p>"
            },
            {
                "content": "<p>Click info on Daily card</p>",
                "expected": "<p>Modal opens with: description, frequency \"Every day\"</p>"
            },
            {
                "content": "<p>Click info on Weekly card</p>",
                "expected": "<p>Modal opens with: description, frequency \"Every Saturday\", minimum amount $0.3</p>"
            },
            {
                "content": "<p>Click info on Monthly card</p>",
                "expected": "<p>Modal opens with: description, \"Available from Loyalty Level 2\", frequency \"1st of month\", minimum amount $0.3</p>"
            }
        ]
    },
    {
        "title": "Negative — Cannot Claim Below Minimum Amount ($0.3)",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has Regular Bonus calculated with amount &lt; $0.3</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player with minimal activity</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Bonus card visible</p>"
            },
            {
                "content": "<p>Check calculated amount</p>",
                "expected": "<p>Amount &lt; $0.3 (e.g., $0.15)</p>"
            },
            {
                "content": "<p>Check bonus state</p>",
                "expected": "<p>State = \"Waiting for reward\" (cannot claim), no \"Claim\" button</p>"
            }
        ]
    },
    {
        "title": "Ready for Claim — Amount Display on Card and Button",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has net loss in period</p><p>Tuesday or Friday (Cashback calculation day)</p><p>Smartico calculation complete</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Login as player with net loss</p>",
                "expected": "<p>Player logged in</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Cashback card visible</p>"
            },
            {
                "content": "<p>Check Cashback card state</p>",
                "expected": "<p>State = \"Ready for claim\"</p>"
            },
            {
                "content": "<p>Check amount displayed on card</p>",
                "expected": "<p>Amount shown on card (e.g., \"$8.50\")</p>"
            },
            {
                "content": "<p>Check button text</p>",
                "expected": "<p>Button text: \"Claim $8.50\" (with actual amount)</p>"
            },
            {
                "content": "<p>Click \"Claim $X\" button</p>",
                "expected": "<p>Claim successful, amount credited to real balance (NO wagering)</p>"
            },
            {
                "content": "<p>Refresh page</p>",
                "expected": "<p>Cashback card shows \"Waiting for reward\" state with timer</p>"
            }
        ]
    }
]

# Add test cases
print(f"Adding {len(test_cases)} test cases to TestRail...\n")

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result['id']}")
    
print("\nDone!")
