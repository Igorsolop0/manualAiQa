#!/usr/bin/env python3
"""
Add CT-799 WebSocket Live Bets test cases to TestRail
"""

import json
import subprocess

TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

SECTION_ID = 7596  # WebSocket — Live Bets & Events (CT-799)

def api_call(method, endpoint, data=None):
    """Make TestRail API call"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
    ]
    
    if method == 'POST':
        cmd.extend(['-X', 'POST', '-d', json.dumps(data)])
    
    cmd.append(f"{TESTRAIL_URL}/index.php?/api/v2/{endpoint}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def add_test_case(section_id, case_data):
    """Add a test case to TestRail"""
    return api_call('POST', f"add_case/{section_id}", case_data)

# Test cases for CT-799
test_cases = [
    {
        "title": "WebSocket Connection — Anonymous User",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Not logged in user</p><p>Open DevTools → Network → WS</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open main page (without RecentBets)</p>",
                "expected": "<p>Page loaded</p>"
            },
            {
                "content": "<p>Check WebSocket connections in DevTools</p>",
                "expected": "<p>No active 'basehub' connection</p>"
            },
            {
                "content": "<p>Navigate to page with RecentBets</p>",
                "expected": "<p>Page with RecentBets loaded</p>"
            },
            {
                "content": "<p>Check WebSocket connections in DevTools</p>",
                "expected": "<p>Active 'basehub' connection visible (Status: Pending)</p><p>Request contains 'RegisterAnonymousForNotification'</p>"
            }
        ]
    },
    {
        "title": "WebSocket Connection — Authenticated User",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Logged in user</p><p>Open DevTools → Network → WS</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open any page of the site</p>",
                "expected": "<p>Page loaded</p>"
            },
            {
                "content": "<p>Check WebSocket connections in DevTools</p>",
                "expected": "<p>Active 'basehub' connection visible (Status: Pending) on ALL pages</p><p>Request contains 'RegisterClientForNotifications' + token</p>"
            },
            {
                "content": "<p>Navigate to different pages</p>",
                "expected": "<p>WebSocket remains active on all pages</p>"
            },
            {
                "content": "<p>Count active WebSocket connections</p>",
                "expected": "<p>Only ONE active 'basehub' connection (no duplicates)</p>"
            }
        ]
    },
    {
        "title": "Live Bets Update — Real-time Rendering",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Open page with RecentBets (anonymous or authenticated)</p><p>Open DevTools → Network → WS → basehub → Messages</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Observe RecentBets table</p>",
                "expected": "<p>Table visible with bet entries</p>"
            },
            {
                "content": "<p>Watch for new bets appearing in table</p>",
                "expected": "<p>New bets appear in table</p>"
            },
            {
                "content": "<p>Check time interval between new bets</p>",
                "expected": "<p>Update interval ≈ 1 second</p>"
            },
            {
                "content": "<p>Check DevTools Messages for 'RecentBetAdded' events</p>",
                "expected": "<p>'RecentBetAdded' events visible in Messages</p><p>No duplicate bets</p>"
            }
        ]
    },
    {
        "title": "No Duplicate Bets in RecentBets",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Open page with RecentBets</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Observe RecentBets table for 30+ seconds</p>",
                "expected": "<p>Multiple bets appeared</p>"
            },
            {
                "content": "<p>Compare bet entries in table</p>",
                "expected": "<p>Each bet is unique (no duplicate ClientId + BetTime combinations)</p>"
            },
            {
                "content": "<p>Check order of bets</p>",
                "expected": "<p>Newest bets appear at top</p>"
            }
        ]
    },
    {
        "title": "UI Limit for Displayed Items in RecentBets",
        "priority_id": 4,  # Medium
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Open page with RecentBets</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Count visible bet entries in table</p>",
                "expected": "<p>Number of entries is limited (N items)</p>"
            },
            {
                "content": "<p>Watch for new bets being added</p>",
                "expected": "<p>Old bets are removed when new ones added</p>"
            },
            {
                "content": "<p>Check scroll functionality (if applicable)</p>",
                "expected": "<p>Scroll works correctly</p>"
            }
        ]
    },
    {
        "title": "Game Navigation During WebSocket Connection",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Logged in user</p><p>WebSocket active</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Open RecentBets page</p>",
                "expected": "<p>RecentBets visible, WebSocket active (Pending)</p>"
            },
            {
                "content": "<p>Click on a game in bet list</p>",
                "expected": "<p>Game opens</p>"
            },
            {
                "content": "<p>Navigate back to RecentBets</p>",
                "expected": "<p>Navigation works without delays</p><p>WebSocket still active (Pending)</p>"
            },
            {
                "content": "<p>Check bets update in real-time</p>",
                "expected": "<p>Bets continue updating in real-time</p>"
            }
        ]
    },
    {
        "title": "Global Events — Authenticated User",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Logged in user</p><p>WebSocket active</p><p>Open DevTools → Network → WS → basehub → Messages</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Perform action that triggers event (e.g., deposit)</p>",
                "expected": "<p>Action completed</p>"
            },
            {
                "content": "<p>Check DevTools Messages for events</p>",
                "expected": "<p>Events 'ClientDepositCompleted', 'ClientBalanceChanges' visible in Messages</p>"
            },
            {
                "content": "<p>Check balance update in UI</p>",
                "expected": "<p>Balance updates in real-time</p>"
            },
            {
                "content": "<p>Check browser console for errors</p>",
                "expected": "<p>No errors in console</p>"
            }
        ]
    },
    {
        "title": "Socket Closure When Not Needed (Anonymous)",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Not logged in user</p><p>Open DevTools → Network → WS</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to RecentBets page (anonymous mode)</p>",
                "expected": "<p>WebSocket 'basehub' active (Pending)</p>"
            },
            {
                "content": "<p>Navigate to another page without RecentBets</p>",
                "expected": "<p>Page loaded</p>"
            },
            {
                "content": "<p>Check WebSocket status in DevTools</p>",
                "expected": "<p>Socket closed (shows closing time)</p><p>'basehub' shows status with closing time in Network</p>"
            }
        ]
    },
    {
        "title": "Socket Reconnection After Network Interruption",
        "priority_id": 3,  # High
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Open RecentBets (WebSocket active)</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Disable internet for 5 seconds</p>",
                "expected": "<p>Connection lost</p>"
            },
            {
                "content": "<p>Enable internet</p>",
                "expected": "<p>Connection restored</p>"
            },
            {
                "content": "<p>Observe RecentBets table</p>",
                "expected": "<p>Socket reconnects automatically</p><p>Bets continue updating</p><p>No duplicate connections</p>"
            }
        ]
    },
    {
        "title": "No Multiple Active WebSocket Connections",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>Open DevTools → Network → WS</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Perform various actions: page navigation, login/logout</p>",
                "expected": "<p>Actions completed</p>"
            },
            {
                "content": "<p>Check Network → WS for active connections</p>",
                "expected": "<p>Only ONE active 'basehub' connection (Status: Pending)</p>"
            },
            {
                "content": "<p>Check other connections</p>",
                "expected": "<p>All other connections show closing time (closed)</p>"
            }
        ]
    }
]

def main():
    print("=" * 60)
    print("CT-799 WebSocket Live Bets — Adding Test Cases to TestRail")
    print("=" * 60)
    print(f"Section ID: {SECTION_ID}")
    
    # Add test cases
    print(f"\n[1] Adding {len(test_cases)} test cases...\n")
    
    success_count = 0
    for i, case in enumerate(test_cases, 1):
        print(f"  [{i}/{len(test_cases)}] Adding: {case['title']}")
        result = add_test_case(SECTION_ID, case)
        
        if 'error' in result:
            print(f"      ❌ Error: {result['error']}")
        else:
            print(f"      ✅ Success! Case ID: {result['id']}")
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Done! Added {success_count}/{len(test_cases)} test cases")
    print(f"Section URL: https://nexttcode.testrail.io/index.php?/suites/view/sections&group_by=sections:section-{SECTION_ID}")
    print("=" * 60)

if __name__ == "__main__":
    main()
