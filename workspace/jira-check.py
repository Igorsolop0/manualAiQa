#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import base64

# Jira credentials from config
JIRA_DOMAIN = "minebit-casino.prod.sofon.one"
JIRA_EMAIL = "testqa_7457ba9d@mail.com"
JIRA_SESSION_TOKEN = "99e717e199644b78bbbd820eefe41408"

# Try both API versions
JIRA_BASE = f"https://{JIRA_DOMAIN}"
HEADERS_BASIC = {
    "Authorization": f"Basic {base64.b64encode(f'{JIRA_EMAIL}:{JIRA_SESSION_TOKEN}'.encode()).decode()}",
    "Content-Type": "application/json"
}
HEADERS_BEARER = {
    "Authorization": f"Bearer {JIRA_SESSION_TOKEN}",
    "Content-Type": "application/json"
}

def test_connection(domain, headers, api_version):
    """Test connection to Jira"""
    try:
        response = requests.get(
            f"https://{domain}/rest/api/{api_version}/myself",
            headers=headers,
            timeout=10
        )
        print(f"Testing https://{domain}/rest/api/{api_version}/myself: {response.status_code}")
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 401:
            return False, "Unauthorized - credentials may be invalid"
        return False, f"Status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    print("Checking Jira connectivity...")
    
    # Try different combinations
    combinations = [
        (JIRA_DOMAIN, HEADERS_BASIC, 2),
        (JIRA_DOMAIN, HEADERS_BASIC, 3),
        (JIRA_DOMAIN, HEADERS_BEARER, 2),
        (JIRA_DOMAIN, HEADERS_BEARER, 3),
    ]
    
    working_config = None
    for domain, headers, api_ver in combinations:
        success, result = test_connection(domain, headers, api_ver)
        if success:
            print(f"✓ Connected to Jira: https://{domain}/rest/api/{api_ver}")
            print(f"  Authenticated as: {result.get('displayName', result.get('name'))}")
            working_config = (domain, headers, api_ver)
            break
        else:
            print(f"✗ Failed: {result}")
    
    if not working_config:
        print("\n❌ Could not connect to Jira with provided credentials.")
        print("Please verify:")
        print("  - Jira domain is correct")
        print("  - Session token is valid and not expired")
        print("  - Account has proper permissions")
        
        # Save empty result
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": "Could not connect to Jira",
            "issues": []
        }
        with open("~/.openclaw/workspace/shared/json-sources/jira/sprint-current.json", "w") as f:
            json.dump(result, f, indent=2)
        
        return "No updates"
    
    domain, headers, api_ver = working_config
    
    # Try to search for tickets
    try:
        print("\nSearching for PandaSen tickets in target states...")
        jql = "project = PandaSen AND status in (\"Ready for Testing\", \"On Production\")"
        params = {
            "jql": jql,
            "maxResults": 50,
            "fields": ["id", "key", "summary", "status", "assignee", "updated"]
        }
        
        response = requests.get(
            f"https://{domain}/rest/api/{api_ver}/search",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        issues = data.get("issues", [])
        
        if not issues:
            print("No tickets found in target states")
            result = {
                "timestamp": datetime.utcnow().isoformat(),
                "project": "PandaSen",
                "states": ["Ready for Testing", "On Production"],
                "total_tickets": 0,
                "issues": []
            }
            with open("~/.openclaw/workspace/shared/json-sources/jira/sprint-current.json", "w") as f:
                json.dump(result, f, indent=2)
            return "No updates"
        
        print(f"Found {len(issues)} tickets")
        
        # Format output
        nexus_message = f"Jira Watcher: Found {len(issues)} PandaSen ticket(s) in target states:\n\n"
        for issue in issues:
            fields = issue.get("fields", {})
            nexus_message += f"📋 {issue['key']} - {fields.get('summary', 'No summary')}\n"
            nexus_message += f"   Status: {fields.get('status', {}).get('name', 'Unknown')}\n"
            nexus_message += f"   URL: https://{domain}/browse/{issue['key']}\n"
            nexus_message += f"   Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}\n"
            nexus_message += f"   Updated: {fields.get('updated', 'Unknown')}\n\n"
        
        # Save to JSON
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "project": "PandaSen",
            "states": ["Ready for Testing", "On Production"],
            "total_tickets": len(issues),
            "issues": issues
        }
        with open("~/.openclaw/workspace/shared/json-sources/jira/sprint-current.json", "w") as f:
            json.dump(result, f, indent=2)
        
        return nexus_message
        
    except Exception as e:
        print(f"Error querying tickets: {e}")
        import traceback
        traceback.print_exc()
        return "No updates"

if __name__ == "__main__":
    main()
