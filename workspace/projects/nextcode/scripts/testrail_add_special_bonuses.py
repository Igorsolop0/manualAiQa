#!/usr/bin/env python3
"""
Script to create Special Bonuses subsection and add test cases to TestRail
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Parent section ID for "Bonuses"
PARENT_SECTION_ID = 6216

def create_section(name, parent_id, suite_id):
    """Create a new section"""
    data = {
        "name": name,
        "parent_id": parent_id,
        "suite_id": suite_id
    }
    
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_section/1"  # Project ID = 1
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def add_test_case(section_id, case_data):
    """Add a test case to TestRail"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(case_data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{section_id}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# Test cases to add
test_cases = [
    # Critical Tests (7)
    {
        "title": "AwaitingForDeposit — Deposit Required After Activation",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has no active bonus</p><p>Player activated deposit bonus</p><p>No deposit made yet</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate deposit bonus</p>",
                "expected": "<p>Bonus activated, state = AwaitingForDeposit</p>"
            },
            {
                "content": "<p>Check bonus card shows \"Deposit\" button</p>",
                "expected": "<p>\"Deposit\" button visible</p>"
            },
            {
                "content": "<p>Click \"Deposit\" → navigate to payment</p>",
                "expected": "<p>Payment page opens</p>"
            },
            {
                "content": "<p>Make qualifying deposit</p>",
                "expected": "<p>Deposit successful</p>"
            },
            {
                "content": "<p>Return to Bonuses page</p>",
                "expected": "<p>Bonus state changed to CurrentlyWagering or PlayingFreespins</p>"
            }
        ]
    },
    {
        "title": "PlayingFreespins — Complete FS Phase",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has FreeSpin bonus activated</p><p>FS not yet played</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Special Bonuses</p>",
                "expected": "<p>Bonus shows \"Choose game\" button</p>"
            },
            {
                "content": "<p>Click \"Choose game\" → game opens</p>",
                "expected": "<p>Game launches in specified slot</p>"
            },
            {
                "content": "<p>Play all Free Spins</p>",
                "expected": "<p>All FS completed, winnings accumulated</p>"
            },
            {
                "content": "<p>Return to Bonuses page</p>",
                "expected": "<p>State = CurrentlyWagering, progress bar shows wagering progress</p>"
            }
        ]
    },
    {
        "title": "CurrentlyWagering — Complete Wagering Phase",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus in CurrentlyWagering state</p><p>Wagering requirement > $0</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Special Bonuses</p>",
                "expected": "<p>Bonus shows \"Play game\" button</p>"
            },
            {
                "content": "<p>Note wagering progress bar percentage</p>",
                "expected": "<p>Progress bar visible (e.g., 30% complete)</p>"
            },
            {
                "content": "<p>Play games to complete wagering</p>",
                "expected": "<p>Wagering progress increases</p>"
            },
            {
                "content": "<p>Reach 100% wagering</p>",
                "expected": "<p>Progress bar shows 100%</p>"
            },
            {
                "content": "<p>Check bonus state</p>",
                "expected": "<p>State = ReadyForClaiming, button changes to \"Claim $X\"</p>"
            }
        ]
    },
    {
        "title": "Welcome Pack — Progressive Unlocking (Bonus 1 → 2 → 3 → 4)",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>New player registered</p><p>Welcome Pack configured (4 bonuses)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Check Bonuses page after registration</p>",
                "expected": "<p>Welcome Pack visible, Bonus 1 available, Bonus 2-4 locked</p>"
            },
            {
                "content": "<p>Activate and complete Bonus 1</p>",
                "expected": "<p>Bonus 1 claimed successfully</p>"
            },
            {
                "content": "<p>Check Bonus 2 status</p>",
                "expected": "<p>Bonus 2 unlocked and available</p>"
            },
            {
                "content": "<p>Try to activate Bonus 3 without completing Bonus 2</p>",
                "expected": "<p>Bonus 3 still locked</p>"
            },
            {
                "content": "<p>Complete Bonus 2, check Bonus 3 unlocks</p>",
                "expected": "<p>Bonuses unlock sequentially, cannot skip</p>"
            }
        ]
    },
    {
        "title": "Welcome Pack — Only 1 Active at a Time (Mono-Bonus)",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active Welcome Pack Bonus 1</p><p>Welcome Pack Bonus 2 available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Check Welcome Pack Bonus 1 is active</p>",
                "expected": "<p>Bonus 1 shows as active</p>"
            },
            {
                "content": "<p>Try to activate Bonus 2</p>",
                "expected": "<p>Cannot activate Bonus 2</p>"
            },
            {
                "content": "<p>Complete and claim Bonus 1</p>",
                "expected": "<p>Bonus 1 closed, Bonus 2 unlocked</p>"
            },
            {
                "content": "<p>Activate Bonus 2</p>",
                "expected": "<p>Bonus 2 activates successfully</p>"
            }
        ]
    },
    {
        "title": "Special Bonus — Cannot Activate with Active Bonus (Mono-Bonus)",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active Special Bonus</p><p>Another Special Bonus available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Special Bonuses</p>",
                "expected": "<p>Active bonus shows in first position</p>"
            },
            {
                "content": "<p>Check another bonus availability</p>",
                "expected": "<p>Another bonus shows \"Activate\" button</p>"
            },
            {
                "content": "<p>Try to activate second bonus</p>",
                "expected": "<p>Cannot activate, error message: \"Active bonus exists\"</p>"
            },
            {
                "content": "<p>Complete and claim active bonus</p>",
                "expected": "<p>Active bonus closed</p>"
            },
            {
                "content": "<p>Try to activate second bonus again</p>",
                "expected": "<p>Activation successful (mono-bonus system)</p>"
            }
        ]
    },
    {
        "title": "Regular Bonus — Can Claim with Active Special Bonus (CT-45)",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active Special Bonus</p><p>Regular Bonus in ReadyForClaiming state</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>Active Special Bonus visible</p>"
            },
            {
                "content": "<p>Navigate to Regular Bonuses</p>",
                "expected": "<p>Regular Bonus shows \"Ready for claim\" with amount</p>"
            },
            {
                "content": "<p>Click \"Claim $X\" on Regular Bonus</p>",
                "expected": "<p>Claim successful, amount credited to real balance</p>"
            },
            {
                "content": "<p>Navigate to Active Bonuses</p>",
                "expected": "<p>ORIGINAL SPECIAL BONUS STILL ACTIVE (CT-45 parallel claim)</p>"
            }
        ]
    },
    # High Priority Tests (12)
    {
        "title": "Welcome Pack — Deposit Tiers",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Welcome Pack with deposit tiers configured</p><p>Player eligible for Welcome Pack</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Check Welcome Pack bonus structure</p>",
                "expected": "<p>Tiers visible: Tier 1 (min deposit), Tier 2 (medium), Tier 3 (max)</p>"
            },
            {
                "content": "<p>Deposit minimum amount → Tier 1</p>",
                "expected": "<p>Tier 1 bonus activated</p>"
            },
            {
                "content": "<p>Check bonus amount</p>",
                "expected": "<p>Base % + FS credited</p>"
            },
            {
                "content": "<p>Complete and claim, then deposit medium amount → Tier 2</p>",
                "expected": "<p>Tier 2 bonus activated with increased % + more FS</p>"
            }
        ]
    },
    {
        "title": "Promo Code — Hidden Until Entered",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Promo code bonus configured</p><p>Player not entered code yet</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page</p>",
                "expected": "<p>Page loads</p>"
            },
            {
                "content": "<p>Check for promo code bonus in Special Bonuses section</p>",
                "expected": "<p>Promo code bonus NOT visible</p>"
            },
            {
                "content": "<p>Enter valid promo code in input field</p>",
                "expected": "<p>Code accepted, success message</p>"
            },
            {
                "content": "<p>Check Special Bonuses section</p>",
                "expected": "<p>Promo code bonus now visible in Available Bonuses</p>"
            }
        ]
    },
    {
        "title": "Promo Code — Cannot Reuse Same Code",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player already used promo code</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Bonuses page</p>",
                "expected": "<p>Page loads</p>"
            },
            {
                "content": "<p>Enter same promo code again</p>",
                "expected": "<p>Code rejected</p>"
            },
            {
                "content": "<p>Check error message</p>",
                "expected": "<p>Message: \"Code already used\" or \"Invalid code\"</p>"
            }
        ]
    },
    {
        "title": "Deposit Bonus — Full Flow (Activate → Deposit → Wager → Claim)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has deposit bonus available (e.g., Ultimate Rush)</p><p>No active bonus</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate deposit bonus</p>",
                "expected": "<p>Bonus activated, state = AwaitingForDeposit</p>"
            },
            {
                "content": "<p>Make qualifying deposit</p>",
                "expected": "<p>Deposit successful, bonus amount credited</p>"
            },
            {
                "content": "<p>Check wagering requirement</p>",
                "expected": "<p>TurnoverCount visible (e.g., x15), progress bar at 0%</p>"
            },
            {
                "content": "<p>Complete wagering</p>",
                "expected": "<p>Progress bar at 100%, state = ReadyForClaiming</p>"
            },
            {
                "content": "<p>Claim bonus</p>",
                "expected": "<p>Amount credited to real balance, bonus closed</p>"
            }
        ]
    },
    {
        "title": "FreeSpin Bonus — Full Flow (Activate → Play FS → Wager → Claim)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has FS bonus available</p><p>No active bonus</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate FS bonus</p>",
                "expected": "<p>Bonus activated, state = PlayingFreespins</p>"
            },
            {
                "content": "<p>Click \"Choose game\" and play all FS</p>",
                "expected": "<p>All FS played, winnings accumulated</p>"
            },
            {
                "content": "<p>Check bonus state after FS</p>",
                "expected": "<p>State = CurrentlyWagering (if wager required) or ReadyForClaiming</p>"
            },
            {
                "content": "<p>Complete wagering on FS winnings (if applicable)</p>",
                "expected": "<p>Wagering complete</p>"
            },
            {
                "content": "<p>Claim bonus</p>",
                "expected": "<p>FS winnings credited to balance</p>"
            }
        ]
    },
    {
        "title": "Cash Bonus — No Deposit Required, No Wagering",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has cash bonus (no deposit required)</p><p>TurnoverCount = None</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Special Bonuses</p>",
                "expected": "<p>Cash bonus visible</p>"
            },
            {
                "content": "<p>Click \"Activate\"</p>",
                "expected": "<p>Bonus activated</p>"
            },
            {
                "content": "<p>Check bonus state</p>",
                "expected": "<p>State = ReadyForClaiming (no deposit, no wagering)</p>"
            },
            {
                "content": "<p>Click \"Claim\"</p>",
                "expected": "<p>Amount credited directly to real balance</p>"
            }
        ]
    },
    {
        "title": "Mixed Bonus — Deposit + FS Combination",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has mixed bonus available (e.g., 150% + 50 FS)</p><p>No active bonus</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate mixed bonus</p>",
                "expected": "<p>Bonus activated</p>"
            },
            {
                "content": "<p>Make qualifying deposit</p>",
                "expected": "<p>Deposit successful, 150% bonus credited</p>"
            },
            {
                "content": "<p>Play all 50 FS</p>",
                "expected": "<p>All FS played, FS winnings accumulated</p>"
            },
            {
                "content": "<p>Complete wagering on both deposit bonus and FS winnings</p>",
                "expected": "<p>Wagering complete on both components</p>"
            },
            {
                "content": "<p>Claim bonus</p>",
                "expected": "<p>Total winnings credited (deposit bonus + FS winnings)</p>"
            }
        ]
    },
    {
        "title": "Active Bonus — Always First in Special Bonuses Section",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active Special Bonus</p><p>Multiple Special Bonuses available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Special Bonuses</p>",
                "expected": "<p>Section loads</p>"
            },
            {
                "content": "<p>Check first bonus card</p>",
                "expected": "<p>Active bonus appears FIRST in the section</p>"
            },
            {
                "content": "<p>Check other bonuses</p>",
                "expected": "<p>Other available bonuses appear after active bonus</p>"
            }
        ]
    },
    {
        "title": "Wagering Expiration — Bonus Lost After Time Limit",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus with wagering</p><p>Wagering time limit configured</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate bonus with wagering</p>",
                "expected": "<p>Bonus active</p>"
            },
            {
                "content": "<p>Wait for expiration time (or manipulate time in BO)</p>",
                "expected": "<p>Time limit expires</p>"
            },
            {
                "content": "<p>Check bonus status</p>",
                "expected": "<p>Status = Expired or Lost</p>"
            },
            {
                "content": "<p>Check balance</p>",
                "expected": "<p>Winnings lost, balance unchanged</p>"
            },
            {
                "content": "<p>Check Active Bonuses</p>",
                "expected": "<p>Bonus removed from Active Bonuses</p>"
            }
        ]
    },
    {
        "title": "Bonus Cancellation — Lose Winnings When Not Finished",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player has active bonus (NOT finished)</p><p>Wagering incomplete</p><p>Some winnings accumulated</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate bonus</p>",
                "expected": "<p>Bonus active</p>"
            },
            {
                "content": "<p>Play partially (wagering incomplete)</p>",
                "expected": "<p>Wagering < 100%, some winnings in bonus balance</p>"
            },
            {
                "content": "<p>Note current real balance</p>",
                "expected": "<p>Balance recorded: $X</p>"
            },
            {
                "content": "<p>Cancel bonus</p>",
                "expected": "<p>Bonus cancelled</p>"
            },
            {
                "content": "<p>Check real balance</p>",
                "expected": "<p>Balance unchanged = $X (winnings LOST)</p>"
            }
        ]
    },
    {
        "title": "Minimum Deposit Not Met — Bonus Not Activated",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Deposit bonus requires minimum deposit</p><p>Player has less than minimum</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate deposit bonus</p>",
                "expected": "<p>Bonus activated, state = AwaitingForDeposit</p>"
            },
            {
                "content": "<p>Deposit amount < minimum required</p>",
                "expected": "<p>Deposit successful but below minimum</p>"
            },
            {
                "content": "<p>Check bonus status</p>",
                "expected": "<p>Bonus NOT activated or remains in AwaitingForDeposit</p>"
            },
            {
                "content": "<p>Check error message</p>",
                "expected": "<p>Message about minimum deposit requirement</p>"
            }
        ]
    },
    {
        "title": "FS Winnings — Lost If Bonus Cancelled During Wagering",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Player completed FS phase</p><p>Wagering on FS winnings incomplete</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Activate FS bonus</p>",
                "expected": "<p>Bonus active</p>"
            },
            {
                "content": "<p>Play all FS, accumulate winnings</p>",
                "expected": "<p>FS complete, winnings in bonus balance</p>"
            },
            {
                "content": "<p>Start wagering but do not complete</p>",
                "expected": "<p>Wagering < 100%</p>"
            },
            {
                "content": "<p>Cancel bonus</p>",
                "expected": "<p>Bonus cancelled</p>"
            },
            {
                "content": "<p>Check balance</p>",
                "expected": "<p>FS winnings LOST (not credited)</p>"
            }
        ]
    }
]

# Main execution
print("Creating Special Bonuses subsection...\n")

# Create subsection
section_result = create_section("Special Bonuses", PARENT_SECTION_ID, 631)  # Suite ID = 631

if 'error' in section_result:
    print(f"❌ Error creating section: {section_result['error']}")
    exit(1)

section_id = section_result['id']
print(f"✅ Section created: {section_result['name']} (ID: {section_id})\n")

# Add test cases
print(f"Adding {len(test_cases)} test cases to TestRail...\n")

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(section_id, case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result['id']}")

print("\nDone!")
print(f"\nTestRail URL: https://nexttcode.testrail.io/index.php?/suites/view/631&group_by=cases:section_id&group_order=asc&display=tree")
