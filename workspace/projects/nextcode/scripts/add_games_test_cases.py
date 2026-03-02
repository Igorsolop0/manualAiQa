#!/usr/bin/env python3
"""
Script to add Games test cases to TestRail for Minebit project.
All test cases are written in upper-intermediate English.
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section ID for "Games"
SECTION_ID = 6843

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

# Test cases for Games section
# 19 test cases covering all critical aspects of game functionality
test_cases = [
    {
        "title": "GAME-001: Launch game - Pragmatic Play provider (desktop)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with balance > $1</p><p>Pragmatic Play game available in lobby (e.g., Gates of Olympus)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Game Lobby → Slots category</p>",
                "expected": "<p>Slots category displays multiple games</p>"
            },
            {
                "content": "<p>Locate a Pragmatic Play game (e.g., Gates of Olympus)</p>",
                "expected": "<p>Game tile shows Pragmatic Play provider logo</p>"
            },
            {
                "content": "<p>Click 'Play' button (desktop) or 'Play game' (mobile)</p>",
                "expected": "<p>Game loads within an iframe, game interface is displayed</p>"
            },
            {
                "content": "<p>Verify player balance is accessible and correctly shown</p>",
                "expected": "<p>Balance displayed matches player's actual balance</p>"
            }
        ]
    },
    {
        "title": "GAME-002: Launch game - Evolution Gaming Live Casino",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with sufficient balance</p><p>Live Casino section accessible</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to Live Casino section</p>",
                "expected": "<p>Live Casino games displayed (roulette, blackjack, etc.)</p>"
            },
            {
                "content": "<p>Select a Live Roulette table (Evolution provider)</p>",
                "expected": "<p>Table information shows Evolution branding</p>"
            },
            {
                "content": "<p>Click 'Join Table' button</p>",
                "expected": "<p>Live stream opens with dealer, betting interface available</p>"
            },
            {
                "content": "<p>Verify chat functionality and betting controls</p>",
                "expected": "<p>Chat works, bet placement controls are functional</p>"
            }
        ]
    },
    {
        "title": "GAME-003: Launch game - NetEnt provider (demo mode for guest)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is a guest (not authorized)</p><p>NetEnt game available (e.g., Starburst)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Visit site as guest user</p>",
                "expected": "<p>Homepage loads without login prompt</p>"
            },
            {
                "content": "<p>Navigate to Slots and locate a NetEnt game</p>",
                "expected": "<p>NetEnt game tile shows 'Demo Play' option</p>"
            },
            {
                "content": "<p>Click 'Demo Play' button</p>",
                "expected": "<p>Game loads in demo mode, demo balance shown</p>"
            },
            {
                "content": "<p>Verify no registration required for demo play</p>",
                "expected": "<p>Game plays without requesting login/registration</p>"
            }
        ]
    },
    {
        "title": "GAME-004: Game launch error - provider temporarily unavailable",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Simulate provider service disruption</p><p>Game from affected provider exists in lobby</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Attempt to launch a game from temporarily unavailable provider</p>",
                "expected": "<p>Game launch attempt initiated</p>"
            },
            {
                "content": "<p>Observe error handling behavior</p>",
                "expected": "<p>'Game temporarily unavailable' modal appears</p>"
            },
            {
                "content": "<p>Check if alternative game suggestions are provided</p>",
                "expected": "<p>Modal suggests similar available games</p>"
            }
        ]
    },
    {
        "title": "GAME-005: Switch from demo mode to real money mode (authorized player)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player playing in demo mode</p><p>Player has sufficient real balance</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch any game in demo mode</p>",
                "expected": "<p>Game loads with demo balance</p>"
            },
            {
                "content": "<p>Click 'Play for real' button within game interface</p>",
                "expected": "<p>Confirmation modal appears</p>"
            },
            {
                "content": "<p>Confirm switch in modal</p>",
                "expected": "<p>Game reloads with real money balance</p>"
            },
            {
                "content": "<p>Verify balance displays real money amount</p>",
                "expected": "<p>Real balance shown, betting uses real funds</p>"
            }
        ]
    },
    {
        "title": "GAME-006: Switch from real money to demo mode",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player playing with real money</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch any game in real money mode</p>",
                "expected": "<p>Game loads with real balance</p>"
            },
            {
                "content": "<p>Open game menu and select 'Switch to demo' option</p>",
                "expected": "<p>Confirmation prompt appears</p>"
            },
            {
                "content": "<p>Confirm demo mode switch</p>",
                "expected": "<p>Game reloads with demo balance</p>"
            },
            {
                "content": "<p>Verify demo balance is displayed</p>",
                "expected": "<p>Demo credits shown, no real money used</p>"
            }
        ]
    },
    {
        "title": "GAME-007: Demo mode accessibility for guest users",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is a guest (not logged in)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Browse game lobby as guest</p>",
                "expected": "<p>All games show 'Demo Play' button</p>"
            },
            {
                "content": "<p>Attempt to launch any game</p>",
                "expected": "<p>Game automatically launches in demo mode</p>"
            },
            {
                "content": "<p>Verify no registration prompts appear</p>",
                "expected": "<p>No login/registration required for demo play</p>"
            }
        ]
    },
    {
        "title": "GAME-008: Game categories navigation and content",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate through all main categories: Slots, Live Casino, Table Games, Jackpots</p>",
                "expected": "<p>Each category loads appropriate games</p>"
            },
            {
                "content": "<p>Verify game count per category matches backend data</p>",
                "expected": "<p>Displayed game count is accurate</p>"
            },
            {
                "content": "<p>Check category-specific UI elements</p>",
                "expected": "<p>Each category shows relevant filters and sorting options</p>"
            }
        ]
    },
    {
        "title": "GAME-009: Game search functionality with various inputs",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Enter exact game name 'Roulette' in search field</p>",
                "expected": "<p>All roulette games displayed</p>"
            },
            {
                "content": "<p>Enter partial match 'Wolf' in search field</p>",
                "expected": "<p>Games containing 'Wolf' in title displayed</p>"
            },
            {
                "content": "<p>Enter non-existent game name 'XYZ123'</p>",
                "expected": "<p>'No games found' message displayed</p>"
            },
            {
                "content": "<p>Clear search and verify lobby returns to normal state</p>",
                "expected": "<p>Full game lobby restored</p>"
            }
        ]
    },
    {
        "title": "GAME-010: Game filters application (provider and features)",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player in Slots category</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open filter panel in Slots section</p>",
                "expected": "<p>Filter options displayed (provider, features, etc.)</p>"
            },
            {
                "content": "<p>Select 'Pragmatic Play' in provider filter</p>",
                "expected": "<p>Only Pragmatic Play games displayed</p>"
            },
            {
                "content": "<p>Add 'Buy Feature' in features filter</p>",
                "expected": "<p>Only Pragmatic Play games with Buy Feature displayed</p>"
            },
            {
                "content": "<p>Clear filters and verify all games restored</p>",
                "expected": "<p>Full slots catalog displayed</p>"
            }
        ]
    },
    {
        "title": "GAME-011: Add and remove game from favorites",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Locate any game and click heart icon to add to favorites</p>",
                "expected": "<p>Heart icon changes to filled state</p>"
            },
            {
                "content": "<p>Navigate to Favorites page</p>",
                "expected": "<p>Added game appears in favorites list</p>"
            },
            {
                "content": "<p>Return to game lobby and click heart icon again to remove</p>",
                "expected": "<p>Heart icon returns to empty state</p>"
            },
            {
                "content": "<p>Refresh Favorites page</p>",
                "expected": "<p>Game removed from favorites list</p>"
            }
        ]
    },
    {
        "title": "GAME-012: Recent games history tracking",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch three different games sequentially</p>",
                "expected": "<p>Each game loads successfully</p>"
            },
            {
                "content": "<p>Navigate to 'Recently Played' section</p>",
                "expected": "<p>Last three played games displayed in correct order (newest first)</p>"
            },
            {
                "content": "<p>Launch a fourth game</p>",
                "expected": "<p>Fourth game appears at top of recent list</p>"
            }
        ]
    },
    {
        "title": "GAME-013: Favorites synchronization across devices",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player adds game to favorites on desktop</p><p>Player accesses mobile version</p>",
        "custom_steps_separated": [
            {
                "content": "<p>On desktop, add a game to favorites</p>",
                "expected": "<p>Game appears in desktop favorites</p>"
            },
            {
                "content": "<p>Open mobile version (or mobile browser)</p>",
                "expected": "<p>Mobile lobby loads</p>"
            },
            {
                "content": "<p>Navigate to Favorites on mobile</p>",
                "expected": "<p>Same game appears in mobile favorites list</p>"
            }
        ]
    },
    {
        "title": "GAME-014: Basic gameplay - bet placement and win calculation",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with balance > $10</p><p>Slot game available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch a slot game in real money mode</p>",
                "expected": "<p>Game interface loads</p>"
            },
            {
                "content": "<p>Place a $1 bet and record balance before spin</p>",
                "expected": "<p>Bet accepted, balance decreases by $1</p>"
            },
            {
                "content": "<p>Execute spin and record result</p>",
                "expected": "<p>Spin completes, win/loss calculated</p>"
            },
            {
                "content": "<p>Verify balance update matches win/loss</p>",
                "expected": "<p>Balance correctly reflects bet outcome</p>"
            }
        ]
    },
    {
        "title": "GAME-015: Autoplay functionality with stop conditions",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player with balance > $20</p><p>Slot game with autoplay feature available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch a slot game</p>",
                "expected": "<p>Game interface loads</p>"
            },
            {
                "content": "<p>Activate Autoplay with 10 spins limit</p>",
                "expected": "<p>Autoplay panel opens with configuration options</p>"
            },
            {
                "content": "<p>Set stop condition (if available) and start autoplay</p>",
                "expected": "<p>Autoplay executes spins automatically</p>"
            },
            {
                "content": "<p>Verify autoplay stops after 10 spins or condition met</p>",
                "expected": "<p>Autoplay stops correctly, balance updated after each spin</p>"
            }
        ]
    },
    {
        "title": "GAME-016: Game rules and paytable accessibility",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player logged in</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch any game</p>",
                "expected": "<p>Game interface loads</p>"
            },
            {
                "content": "<p>Click 'Rules' or 'Paytable' button</p>",
                "expected": "<p>Game rules/paytable modal opens</p>"
            },
            {
                "content": "<p>Verify information clarity and completeness</p>",
                "expected": "<p>Clear rules, symbol values, special features explained</p>"
            }
        ]
    },
    {
        "title": "GAME-017: Mobile game launch and touch interface",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player on mobile device (iPhone/Android)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Access mobile version via browser</p>",
                "expected": "<p>Mobile-optimized lobby loads</p>"
            },
            {
                "content": "<p>Navigate to a game and launch it</p>",
                "expected": "<p>Game loads in mobile-adapted interface</p>"
            },
            {
                "content": "<p>Verify touch controls work correctly</p>",
                "expected": "<p>Buttons respond to touch, game plays smoothly</p>"
            }
        ]
    },
    {
        "title": "GAME-018: Mobile device orientation change handling",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player on mobile device</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch a game in portrait orientation</p>",
                "expected": "<p>Game loads in portrait mode</p>"
            },
            {
                "content": "<p>Rotate device to landscape orientation</p>",
                "expected": "<p>Game adapts to landscape mode</p>"
            },
            {
                "content": "<p>Verify UI elements remain functional</p>",
                "expected": "<p>All controls accessible, no layout breaks</p>"
            },
            {
                "content": "<p>Rotate back to portrait</p>",
                "expected": "<p>Game returns to portrait mode correctly</p>"
            }
        ]
    },
    {
        "title": "GAME-019: Touch gestures support in games (swipe, pinch)",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Authorized player on touch-enabled device</p><p>Game with swipe/pinch controls available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Launch a game with swipe controls (e.g., some slot games)</p>",
                "expected": "<p>Game loads</p>"
            },
            {
                "content": "<p>Perform swipe gesture on appropriate area</p>",
                "expected": "<p>Swipe triggers intended action (spin, navigation)</p>"
            },
            {
                "content": "<p>Launch a game with pinch-to-zoom capability</p>",
                "expected": "<p>Game loads</p>"
            },
            {
                "content": "<p>Perform pinch-to-zoom gesture</p>",
                "expected": "<p>Game view zooms in/out as expected</p>"
            }
        ]
    }
]

# Add test cases
print(f"Adding {len(test_cases)} test cases to TestRail (Games section)...\n")

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result.get('id', 'Unknown')}")
    
print("\nDone!")