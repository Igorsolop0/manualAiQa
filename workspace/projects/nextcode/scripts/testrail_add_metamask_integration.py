#!/usr/bin/env python3
"""
Script to add Metamask Integration test cases to TestRail
Creates a subsection "Metamask Integration" under "Authentication" section.
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
SUITE_ID = 631          # Regular Bonuses Section (contains Authentication)
PARENT_SECTION_ID = 6839  # "Authentication" section

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

# Metamask Integration test cases (13 E2E tests)
metamask_integration_cases = [
    {
        'title': 'Metamask Integration – Desktop with extension installed',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser (Chrome/Firefox/Safari) with Metamask extension installed</p><p>Metamask wallet is unlocked and has at least one account</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page</p>', 'expected': '<p>Login page loads with Metamask button visible</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Metamask extension popup opens</p>'},
            {'content': '<p>Sign the message in Metamask popup</p>', 'expected': '<p>Message signed successfully</p>'},
            {'content': '<p>Observe the button state during signing</p>', 'expected': '<p>Button shows loader and is disabled during the process</p>'},
            {'content': '<p>Wait for authentication to complete</p>', 'expected': '<p>User logged in successfully, redirected to main page</p>'},
        ],
        'custom_expected': '<p>User authenticated via Metamask, session token stored, loader shown during process</p>',
    },
    {
        'title': 'Metamask Integration – Desktop without extension (popup flow)',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser (Chrome/Firefox/Safari) WITHOUT Metamask extension</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page</p>', 'expected': '<p>Login page loads with Metamask button visible</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Popup appears with download link and QR code</p>'},
            {'content': '<p>Check popup content</p>', 'expected': '<p>Popup shows: (1) Download extension link, (2) QR code for mobile app</p>'},
            {'content': '<p>Scan QR code with mobile device</p>', 'expected': '<p>QR code links to Metamask mobile app download page</p>'},
        ],
        'custom_expected': '<p>Popup provides clear instructions for users without Metamask extension, QR code links to mobile app</p>',
    },
    {
        'title': 'Metamask Integration – Mobile with app installed (deep-link flow)',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Mobile device (iOS Safari or Android Chrome) with Metamask app installed</p><p>Metamask app is configured with at least one wallet</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page on mobile browser</p>', 'expected': '<p>Login page loads with Metamask button visible</p>'},
            {'content': '<p>Tap on Metamask button</p>', 'expected': '<p>Prompt appears to open Metamask app</p>'},
            {'content': '<p>Confirm opening Metamask app</p>', 'expected': '<p>Metamask app opens with sign request</p>'},
            {'content': '<p>Sign the message in Metamask app</p>', 'expected': '<p>Message signed successfully</p>'},
            {'content': '<p>Return to browser</p>', 'expected': '<p>User logged in automatically, session active</p>'},
        ],
        'custom_expected': '<p>Deep-link flow works seamlessly, user authenticated after signing in Metamask mobile app</p>',
    },
    {
        'title': 'Metamask Integration – Mobile without app (fallback flow)',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Mobile device (iOS Safari or Android Chrome) WITHOUT Metamask app</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page on mobile browser</p>', 'expected': '<p>Login page loads with Metamask button visible</p>'},
            {'content': '<p>Tap on Metamask button</p>', 'expected': '<p>Fallback UI appears (instructions to install app or use browser wallet)</p>'},
        ],
        'custom_expected': '<p>Clear fallback instructions provided for users without Metamask mobile app</p>',
    },
    {
        'title': 'Metamask Integration – Signature rejection',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Metamask wallet is unlocked</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page</p>', 'expected': '<p>Login page loads</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Metamask extension popup opens</p>'},
            {'content': '<p>Reject/cancel the signing request in Metamask</p>', 'expected': '<p>Signing cancelled</p>'},
            {'content': '<p>Observe button state and error message</p>', 'expected': '<p>Button re-enabled, clear error message shown to user</p>'},
        ],
        'custom_expected': '<p>Signature rejection handled gracefully, button re-enabled, user notified with clear error message</p>',
    },
    {
        'title': 'Metamask Integration – Multiple accounts selection',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Metamask wallet has 2+ accounts configured</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page</p>', 'expected': '<p>Login page loads</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Metamask extension popup opens</p>'},
            {'content': '<p>Select a specific account in Metamask (not the first one)</p>', 'expected': '<p>Account selected</p>'},
            {'content': '<p>Sign the message with selected account</p>', 'expected': '<p>Message signed</p>'},
            {'content': '<p>Check user profile after login</p>', 'expected': '<p>User logged in with correct wallet address (selected account)</p>'},
        ],
        'custom_expected': '<p>Correct wallet address associated with user account after login</p>',
    },
    {
        'title': 'Metamask Integration – Network switching during auth',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Metamask wallet supports multiple networks</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login/registration page</p>', 'expected': '<p>Login page loads</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Metamask extension popup opens</p>'},
            {'content': '<p>Switch network in Metamask during signing</p>', 'expected': '<p>Network switched</p>'},
            {'content': '<p>Sign the message</p>', 'expected': '<p>Authentication completes or appropriate error shown</p>'},
        ],
        'custom_expected': '<p>Network switching handled gracefully (nonce refreshed if needed, or clear error message)</p>',
    },
    {
        'title': 'Metamask Integration – Session persistence',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>User already authenticated via Metamask</p><p>Website (Minebit) is loaded on DEV environment</p>',
        'custom_steps_separated': [
            {'content': '<p>Login via Metamask successfully</p>', 'expected': '<p>User logged in</p>'},
            {'content': '<p>Refresh the page (F5 or Ctrl+R)</p>', 'expected': '<p>Page reloads</p>'},
            {'content': '<p>Check authentication state</p>', 'expected': '<p>User still logged in (session persisted)</p>'},
            {'content': '<p>Close browser and reopen</p>', 'expected': '<p>Session may persist depending on configuration</p>'},
        ],
        'custom_expected': '<p>JWT session token stored correctly, user remains authenticated after page refresh</p>',
    },
    {
        'title': 'Metamask Integration – Cross-browser compatibility',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Multiple browsers available: Chrome, Firefox, Safari (Desktop), Safari iOS, Chrome Android</p><p>Metamask extension/app installed on each platform</p>',
        'custom_steps_separated': [
            {'content': '<p>Test Metamask login on Chrome Desktop</p>', 'expected': '<p>Login works correctly</p>'},
            {'content': '<p>Test Metamask login on Firefox Desktop</p>', 'expected': '<p>Login works correctly</p>'},
            {'content': '<p>Test Metamask login on Safari Desktop (if supported)</p>', 'expected': '<p>Login works correctly or clear message about unsupported browser</p>'},
            {'content': '<p>Test Metamask login on Safari iOS</p>', 'expected': '<p>Deep-link flow works</p>'},
            {'content': '<p>Test Metamask login on Chrome Android</p>', 'expected': '<p>Deep-link flow works</p>'},
        ],
        'custom_expected': '<p>Metamask authentication works across all supported browsers and platforms</p>',
    },
    {
        'title': 'Metamask Integration – Responsive UI',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop and mobile devices available</p><p>Browser DevTools for responsive testing</p>',
        'custom_steps_separated': [
            {'content': '<p>Open login page on desktop browser</p>', 'expected': '<p>Metamask button and popup adapt to desktop layout</p>'},
            {'content': '<p>Resize browser to mobile viewport (e.g., 375px width)</p>', 'expected': '<p>UI elements adapt to mobile breakpoints (per Figma)</p>'},
            {'content': '<p>Test popup on mobile viewport</p>', 'expected': '<p>Popup displays correctly on small screens</p>'},
        ],
        'custom_expected': '<p>Button and popup UI responsive across mobile and desktop breakpoints</p>',
    },
    {
        'title': 'Metamask Integration – Loader states',
        'priority_id': 4,  # Medium
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Metamask wallet is unlocked</p>',
        'custom_steps_separated': [
            {'content': '<p>Navigate to login page</p>', 'expected': '<p>Login page loads</p>'},
            {'content': '<p>Click on Metamask button</p>', 'expected': '<p>Button shows loader spinner, becomes disabled</p>'},
            {'content': '<p>Sign the message (success case)</p>', 'expected': '<p>Loader disappears after successful auth</p>'},
            {'content': '<p>Repeat test and reject signing (failure case)</p>', 'expected': '<p>Loader disappears, button re-enabled</p>'},
        ],
        'custom_expected': '<p>Loader state managed correctly: button disabled with spinner during process, re-enabled after success/failure</p>',
    },
    {
        'title': 'Metamask Integration – BE API integration (nonce, signature, JWT)',
        'priority_id': 3,  # High
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Network monitoring tools (DevTools Network tab)</p><p>Backend API endpoints deployed and accessible</p>',
        'custom_steps_separated': [
            {'content': '<p>Open DevTools Network tab</p>', 'expected': '<p>Network monitoring active</p>'},
            {'content': '<p>Click Metamask button</p>', 'expected': '<p>Request to nonce endpoint observed</p>'},
            {'content': '<p>Sign the message</p>', 'expected': '<p>Signature sent to verification endpoint</p>'},
            {'content': '<p>Check response</p>', 'expected': '<p>JWT token received in response</p>'},
        ],
        'custom_expected': '<p>SIWE flow works: nonce request → signature submission → JWT response</p>',
    },
    {
        'title': 'Metamask Integration – Security (replay attack prevention, signature validation)',
        'priority_id': 5,  # Low (important but requires deeper testing)
        'type_id': 11,     # Acceptance
        'custom_preconds': '<p>Desktop browser with Metamask extension installed</p><p>Understanding of SIWE security mechanisms</p>',
        'custom_steps_separated': [
            {'content': '<p>Login via Metamask and capture the nonce</p>', 'expected': '<p>Nonce value recorded</p>'},
            {'content': '<p>Attempt to reuse the same nonce for another login</p>', 'expected': '<p>Request rejected (nonce already used)</p>'},
            {'content': '<p>Check signature validation with tampered message</p>', 'expected': '<p>Invalid signature rejected</p>'},
            {'content': '<p>Verify wallet address not exposed in logs/UI unnecessarily</p>', 'expected': '<p>Wallet address handled securely</p>'},
        ],
        'custom_expected': '<p>Replay attack prevented, signature validated correctly, wallet address not exposed in logs</p>',
    },
]

def main():
    print("🚀 Adding Metamask Integration test cases to TestRail...")
    print(f"  Project ID: {PROJECT_ID}")
    print(f"  Suite ID: {SUITE_ID}")
    print(f"  Parent Section ID: {PARENT_SECTION_ID} (Authentication)")
    
    # Check if section already exists
    section_name = "Metamask Integration"
    existing_section = find_section(section_name, PARENT_SECTION_ID)
    
    if existing_section:
        section_id = existing_section['id']
        print(f"ℹ️  Section '{section_name}' already exists with ID {section_id}")
    else:
        print(f"📦 Creating section '{section_name}'...")
        section_id = create_section(section_name, PARENT_SECTION_ID)
        if not section_id:
            print("❌ Failed to create section. Exiting.")
            sys.exit(1)
    
    # Add test cases
    print(f"\n📝 Adding {len(metamask_integration_cases)} test cases...")
    added_cases = []
    for i, case in enumerate(metamask_integration_cases, 1):
        print(f"\n{i}. {case['title']}")
        case_id = add_test_case(section_id, case)
        if case_id:
            added_cases.append({
                'title': case['title'],
                'id': case_id,
            })
    
    # Summary
    print("\n" + "="*60)
    print(f"✅ Added {len(added_cases)} test cases to section '{section_name}'")
    print(f"📍 TestRail URL: {TESTRAIL_URL}/index.php?/suites/view/{SUITE_ID}&group_by=cases:section_id&group_id={section_id}")
    print("="*60)
    
    # Save summary
    summary = {
        'section_id': section_id,
        'section_name': section_name,
        'cases_added': len(added_cases),
        'cases': added_cases,
    }
    with open('/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/testrail_metamask_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"💾 Summary saved to: testrail_metamask_summary.json")

if __name__ == '__main__':
    main()
