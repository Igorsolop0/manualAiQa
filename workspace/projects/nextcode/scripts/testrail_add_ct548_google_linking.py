#!/usr/bin/env python3
"""
Add Priority 1 test cases for CT-548: Google Linking & Unlinking to TestRail
"""

import json
import subprocess

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Section ID for CT-548 (will need to find or create)
# For now, let's use a general section or create one
SECTION_ID = None  # Will be determined

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

def get_or_create_section(project_id, suite_id, section_name, parent_id=None):
    """Get existing section or create new one"""
    # First, try to get existing sections
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    response = json.loads(result.stdout)
    
    # Handle paginated response
    if isinstance(response, dict) and 'sections' in response:
        sections = response['sections']
    elif isinstance(response, list):
        sections = response
    else:
        sections = []
    
    # Look for existing section
    for section in sections:
        if isinstance(section, dict) and section.get('name') == section_name:
            return section['id']
    
    # Create new section if not found
    section_data = {
        "name": section_name,
        "suite_id": suite_id
    }
    if parent_id:
        section_data["parent_id"] = parent_id
    
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(section_data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_section/{project_id}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    new_section = json.loads(result.stdout)
    
    if 'error' in new_section:
        print(f"Error creating section: {new_section['error']}")
        return None
    
    return new_section['id']

# Priority 1 Test Cases for CT-548
test_cases = [
    {
        "title": "Link Google Account from Client Profile",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is logged in</p><p>Google account is NOT linked</p><p>User is on /test-social-linking page</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Verify \"Link social media\" section is visible</p>",
                "expected": "<p>Section visible with Google and Telegram options</p>"
            },
            {
                "content": "<p>Verify \"Connect\" button for Google is displayed</p>",
                "expected": "<p>Google Connect button visible and clickable</p>"
            },
            {
                "content": "<p>Click Google \"Connect\" button</p>",
                "expected": "<p>Google OAuth popup opens</p>"
            },
            {
                "content": "<p>Verify OAuth URL contains required parameters (client_id, redirect_uri, scope, state)</p>",
                "expected": "<p>OAuth URL has all required parameters</p>"
            },
            {
                "content": "<p>Complete Google OAuth authentication</p>",
                "expected": "<p>OAuth completes successfully</p>"
            },
            {
                "content": "<p>Verify redirect back to application</p>",
                "expected": "<p>User redirected to /test-social-linking or ReturnUrl</p>"
            },
            {
                "content": "<p>Verify success message is displayed</p>",
                "expected": "<p>Success message or notification shown</p>"
            },
            {
                "content": "<p>Verify Google account is shown as \"Linked\" in profile</p>",
                "expected": "<p>Google status shows \"Linked\" or similar state</p>"
            }
        ]
    },
    {
        "title": "Verify linkToken in OAuth State Parameter",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is logged in</p><p>User initiates Google linking</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Click Google \"Connect\" button</p>",
                "expected": "<p>OAuth URL generated with state parameter</p>"
            },
            {
                "content": "<p>Capture OAuth URL and extract state parameter</p>",
                "expected": "<p>State parameter extracted from URL</p>"
            },
            {
                "content": "<p>Decode Base64 state parameter</p>",
                "expected": "<p>State decoded to JSON object</p>"
            },
            {
                "content": "<p>Verify decoded state contains LinkToken (non-empty string)</p>",
                "expected": "<p>LinkToken present with valid value (e.g., 3a03e43b12aa4545...)</p>"
            },
            {
                "content": "<p>Verify decoded state contains AuthTokenMode (value: 1)</p>",
                "expected": "<p>AuthTokenMode = 1</p>"
            },
            {
                "content": "<p>Verify decoded state contains PartnerId</p>",
                "expected": "<p>PartnerId present with correct value</p>"
            },
            {
                "content": "<p>Verify decoded state contains ReturnUrl</p>",
                "expected": "<p>ReturnUrl points to correct page (e.g., /test-social-linking)</p>"
            },
            {
                "content": "<p>Verify decoded state contains ErrorBackUrl</p>",
                "expected": "<p>ErrorBackUrl points to error page (e.g., /en/)</p>"
            }
        ]
    },
    {
        "title": "Unlink Google Account from Client Profile",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User is logged in</p><p>Google account is linked</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Navigate to /test-social-linking page</p>",
                "expected": "<p>Page loads successfully</p>"
            },
            {
                "content": "<p>Verify Google account shows \"Linked\" status</p>",
                "expected": "<p>Google status shows \"Linked\" or similar</p>"
            },
            {
                "content": "<p>Click \"Unlink\" button for Google</p>",
                "expected": "<p>Confirmation dialog appears</p>"
            },
            {
                "content": "<p>Confirm unlink action</p>",
                "expected": "<p>Unlink action initiated</p>"
            },
            {
                "content": "<p>Verify success message is displayed</p>",
                "expected": "<p>Success message shown</p>"
            },
            {
                "content": "<p>Verify Google account is no longer shown as linked</p>",
                "expected": "<p>Google status shows unlinked state</p>"
            },
            {
                "content": "<p>Verify \"Connect\" button is available again</p>",
                "expected": "<p>Google Connect button visible</p>"
            }
        ]
    },
    {
        "title": "Link Google — Invalid Auth Token",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User session is invalid or expired</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Clear session cookies or invalidate auth token</p>",
                "expected": "<p>Session cleared</p>"
            },
            {
                "content": "<p>Navigate to /test-social-linking page</p>",
                "expected": "<p>Page loads</p>"
            },
            {
                "content": "<p>Click Google \"Connect\" button</p>",
                "expected": "<p>Action initiated</p>"
            },
            {
                "content": "<p>Verify appropriate error handling</p>",
                "expected": "<p>Error detected (error message, redirect, or denied action)</p>"
            },
            {
                "content": "<p>Verify user is redirected to login page or shown auth error</p>",
                "expected": "<p>User prompted to re-authenticate or shown auth error message</p>"
            }
        ]
    },
    {
        "title": "Link Google — Duplicate Email Address",
        "priority_id": 2,  # Critical
        "type_id": 11,  # Acceptance
        "custom_preconds": "<p>User A has Google account linked with email test@gmail.com</p><p>User B attempts to link the same Google account</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Log in as User B</p>",
                "expected": "<p>User B logged in</p>"
            },
            {
                "content": "<p>Navigate to /test-social-linking page</p>",
                "expected": "<p>Page loads</p>"
            },
            {
                "content": "<p>Click Google \"Connect\" button</p>",
                "expected": "<p>OAuth popup opens</p>"
            },
            {
                "content": "<p>Authenticate with Google account already linked to User A</p>",
                "expected": "<p>OAuth flow proceeds</p>"
            },
            {
                "content": "<p>Verify appropriate error message</p>",
                "expected": "<p>Error message shown (e.g., \"This Google account is already linked to another user\")</p>"
            },
            {
                "content": "<p>Verify Google account is NOT linked to User B</p>",
                "expected": "<p>Google status for User B remains unlinked</p>"
            },
            {
                "content": "<p>Verify Google account remains linked to User A (check User A profile)</p>",
                "expected": "<p>User A still has Google linked</p>"
            }
        ]
    },
    {
        "title": "Verify linkedRegistrationSources in Player Object",
        "priority_id": 2,  # Critical
        "type_id": 12,  # API
        "custom_preconds": "<p>User has linked Google account</p><p>API access available</p>",
        "custom_steps_separated": [
            {
                "content": "<p>Call Player API endpoint with player ID</p>",
                "expected": "<p>API returns 200 OK with player object</p>"
            },
            {
                "content": "<p>Verify linkedRegistrationSources field exists in response</p>",
                "expected": "<p>linkedRegistrationSources field present</p>"
            },
            {
                "content": "<p>Verify linkedRegistrationSources contains \"google\"</p>",
                "expected": "<p>Array contains \"google\" (e.g., [\"google\"] or [\"email\", \"google\"])</p>"
            },
            {
                "content": "<p>Unlink Google account via UI or API</p>",
                "expected": "<p>Unlink successful</p>"
            },
            {
                "content": "<p>Call Player API endpoint again</p>",
                "expected": "<p>API returns 200 OK</p>"
            },
            {
                "content": "<p>Verify linkedRegistrationSources no longer contains \"google\"</p>",
                "expected": "<p>Array does not contain \"google\" or field is empty/null</p>"
            }
        ]
    }
]

# Main execution
print("=" * 60)
print("CT-548: Google Linking & Unlinking — TestRail Test Cases")
print("=" * 60)
print()

# Get project and suite info
# Based on previous scripts, project_id is likely 1, suite_id needs to be determined
# For CT-548, we'll use the same project and find or create a section

project_id = 1  # NextCode project

# Get all suites to find the right one
cmd = [
    'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
    f"{TESTRAIL_URL}/index.php?/api/v2/get_suites/{project_id}"
]

result = subprocess.run(cmd, capture_output=True, text=True)
response = json.loads(result.stdout)

print("API Response received")

# Handle paginated response
if isinstance(response, dict) and 'suites' in response:
    suites = response['suites']
elif isinstance(response, list):
    suites = response
else:
    print(f"❌ Unexpected response format: {response.get('error', 'Unknown')}")
    suites = []

if isinstance(suites, list):
    print(f"Found {len(suites)} suites:")
    for suite in suites:
        if isinstance(suite, dict):
            print(f"  Suite ID: {suite['id']}, Name: {suite['name']}")
else:
    print("Using default suite_id = 631")
    suite_id = 631

# Use suite 631 (from previous scripts) or first available suite
if 'suite_id' not in locals():
    if isinstance(suites, list) and suites:
        suite_id = 631 if any(s.get('id') == 631 for s in suites if isinstance(s, dict)) else suites[0].get('id', 631)
    else:
        suite_id = 631
print(f"\nUsing Suite ID: {suite_id}")

# Get or create section for CT-548
section_name = "CT-548: Google Linking & Unlinking"
print(f"\nLooking for section: {section_name}")

section_id = get_or_create_section(project_id, suite_id, section_name)

if not section_id:
    print("❌ Could not find or create section. Using default section.")
    # Fall back to existing section from previous scripts
    section_id = 6478  # Regular Bonuses section (temporary fallback)

print(f"Using Section ID: {section_id}\n")

# Add test cases
print(f"Adding {len(test_cases)} Priority 1 test cases to TestRail...\n")

success_count = 0
error_count = 0

for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(section_id, case)
    
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
        error_count += 1
    else:
        print(f"  ✅ Success! Case ID: {result['id']}")
        success_count += 1

print()
print("=" * 60)
print(f"Summary: {success_count} success, {error_count} errors")
print("=" * 60)
