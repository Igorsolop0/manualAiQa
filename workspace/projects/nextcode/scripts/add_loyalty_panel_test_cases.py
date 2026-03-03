#!/usr/bin/env python3
"""
Script to add Loyalty Panel (Player Dashboard) test cases to TestRail for Minebit project.
All test cases are written in upper-intermediate English.
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section ID for "Bonuses" (from testrail_gap_analysis.json)
SECTION_ID = 6216

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
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": f"Failed to parse response: {result.stdout[:200]}"}

# Test cases for Loyalty Panel on Bonuses page
# 5 test cases total: 1 combined verification + 4 separate functionality tests
test_cases = [
    {
        "title": "Loyalty panel (player dashboard) display and functionality verification",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with loyalty rank 'Pawn Pioneer'</p><p>Player has 20/300 EXP (7% progress)</p><p>Player has known balance amounts (e.g., $0.00 for testing)</p><p>System time is synchronized</p><p>Player has an avatar set</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page.</p>",
                "expected": "<p>Bonuses page loads successfully.</p>"
            },
            {
                "content": "<p>Locate the loyalty panel (player dashboard) section.</p>",
                "expected": "<p>Loyalty panel is visible on the page.</p>"
            },
            {
                "content": "<p>Verify current rank displays 'Pawn Pioneer' with its icon visible.</p>",
                "expected": "<p>Current rank text and icon are displayed correctly.</p>"
            },
            {
                "content": "<p>Check progress bar shows 7% fill and verify visual representation matches percentage.</p>",
                "expected": "<p>Progress bar is filled to 7% and visual bar matches percentage.</p>"
            },
            {
                "content": "<p>Verify 'Your prize: $1' label is present and correctly positioned.</p>",
                "expected": "<p>Prize label displays '$1' and is positioned near progress bar.</p>"
            },
            {
                "content": "<p>Check EXP counter displays '20/300' (current/maximum) format.</p>",
                "expected": "<p>EXP counter shows '20/300' indicating current progress.</p>"
            },
            {
                "content": "<p>Verify next rank shows 'Love Learner' with 'Next rank' indicator/icon.</p>",
                "expected": "<p>Next rank is correctly displayed with indicator.</p>"
            },
            {
                "content": "<p>Check UTC timer displays correct time in HH:MM:SS format and updates in real‑time (observe for at least 2 seconds).</p>",
                "expected": "<p>Timer shows current UTC time, format is HH:MM:SS, and seconds increment.</p>"
            },
            {
                "content": "<p>Click 'See all levels' button and observe page navigation.</p>",
                "expected": "<p>Page redirects to /loyalty page showing all loyalty levels.</p>"
            },
            {
                "content": "<p>Verify balance displays: 'My balance', 'Cash Balance', 'Bonus Balance' amounts.</p>",
                "expected": "<p>All three balance amounts are displayed with correct currency formatting (e.g., $0.00).</p>"
            },
            {
                "content": "<p>Check player ID displays correctly (876062528 / 1176185).</p>",
                "expected": "<p>Player ID numbers are shown as expected.</p>"
            },
            {
                "content": "<p>Verify avatar image loads without errors (no broken image icon).</p>",
                "expected": "<p>Avatar image loads successfully and displays clearly.</p>"
            }
        ]
    },
    {
        "title": "Enter promo code button opens promo modal",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page.</p>",
                "expected": "<p>Bonuses page loads with loyalty panel visible.</p>"
            },
            {
                "content": "<p>Locate the 'Enter promo code' button in the loyalty panel.</p>",
                "expected": "<p>Button is present and clickable.</p>"
            },
            {
                "content": "<p>Click the 'Enter promo code' button.</p>",
                "expected": "<p>Promo code entry modal/popup appears with input field and submit button.</p>"
            }
        ]
    },
    {
        "title": "Smartico nickname change integration",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with Smartico enabled</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page.</p>",
                "expected": "<p>Bonuses page loads with loyalty panel visible.</p>"
            },
            {
                "content": "<p>Locate the nickname change button (Smartico integration).</p>",
                "expected": "<p>Button is present and clickable.</p>"
            },
            {
                "content": "<p>Click the nickname change button.</p>",
                "expected": "<p>Smartico modal opens for nickname change with 'dp:gf_change_nickname' integration.</p>"
            }
        ]
    },
    {
        "title": "Smartico avatar change integration",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with Smartico enabled</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page.</p>",
                "expected": "<p>Bonuses page loads with loyalty panel visible.</p>"
            },
            {
                "content": "<p>Locate the avatar change button (Smartico integration).</p>",
                "expected": "<p>Button is present and clickable.</p>"
            },
            {
                "content": "<p>Click the avatar change button.</p>",
                "expected": "<p>Smartico modal opens for avatar change with 'dp:gf_change_avatar' integration.</p>"
            }
        ]
    },
    {
        "title": "Loyalty panel mobile responsiveness",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Mobile device viewport (iPhone/Android)</p><p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open Bonuses page on mobile device (simulate mobile viewport).</p>",
                "expected": "<p>Bonuses page loads in mobile-optimized layout.</p>"
            },
            {
                "content": "<p>Check layout adaptation of loyalty panel.</p>",
                "expected": "<p>Panel adapts to small screen, no elements cut off.</p>"
            },
            {
                "content": "<p>Verify all elements remain accessible (buttons, text, images).</p>",
                "expected": "<p>All interactive elements are touch‑friendly and properly spaced.</p>"
            }
        ]
    }
]

# Add test cases
print(f"Adding {len(test_cases)} test cases to TestRail (Bonuses section, ID: {SECTION_ID})...\n")

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result.get('id', 'Unknown')}")
    
print("\nDone!")