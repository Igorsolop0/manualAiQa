#!/usr/bin/env python3
"""
Search for Jira tickets where the current user has commented.
Returns a list of ticket keys with comment count.
"""
import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import requests
except ImportError:
    print("ERROR: requests module not installed. Run: pip install requests")
    sys.exit(1)

# Load API token
token_path = Path.home() / ".openclaw" / "workspace" / ".jira_token"
if not token_path.exists():
    print("ERROR: .jira_token not found")
    sys.exit(1)

JIRA_API_TOKEN = token_path.read_text().strip()
JIRA_EMAIL = "ihor.so@nextcode.tech"
JIRA_BASE_URL = "https://next-t-code.atlassian.net"

def get_current_user():
    """Get current user's accountId"""
    response = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/myself",
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()
    return response.json()["accountId"]

def search_issues_with_comments(account_id, max_results=50):
    """Search for issues where user has commented"""
    # Using a combination of queries to find relevant issues
    # Note: commentedBy JQL doesn't work reliably, so we'll get recent issues
    # and filter by comments
    
    queries = [
        f"assignee = {account_id}",
        f"reporter = {account_id}",
        "project = CT ORDER BY updated DESC"
    ]
    
    all_issues = {}
    
    for jql in queries:
        try:
            response = requests.post(
                f"{JIRA_BASE_URL}/rest/api/3/search/jql",
                auth=(JIRA_EMAIL, JIRA_API_TOKEN),
                headers={"Content-Type": "application/json"},
                json={
                    "jql": jql,
                    "fields": ["key", "summary", "status", "updated", "comment"],
                    "maxResults": 50
                }
            )
            
            if response.status_code != 200:
                continue
                
            data = response.json()
            
            for issue in data.get("issues", []):
                key = issue["key"]
                if key not in all_issues:
                    all_issues[key] = {
                        "key": key,
                        "summary": issue["fields"]["summary"],
                        "status": issue["fields"]["status"]["name"],
                        "updated": issue["fields"]["updated"],
                        "user_comments": []
                    }
                
                # Check comments
                comments = issue["fields"].get("comment", {}).get("comments", [])
                for comment in comments:
                    if comment.get("author", {}).get("accountId") == account_id:
                        all_issues[key]["user_comments"].append({
                            "created": comment.get("created"),
                            "body": comment.get("body", "")
                        })
        except Exception as e:
            print(f"Warning: Query failed: {e}", file=sys.stderr)
            continue
    
    # Filter to only issues with user comments
    issues_with_comments = {
        k: v for k, v in all_issues.items() 
        if v["user_comments"]
    }
    
    return issues_with_comments

def main():
    try:
        # Get current user
        account_id = get_current_user()
        print(f"Current user: {account_id}", file=sys.stderr)
        
        # Search for issues
        issues = search_issues_with_comments(account_id)
        
        # Output as JSON
        output = {
            "total": len(issues),
            "issues": issues
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
