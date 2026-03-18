#!/usr/bin/env python3
"""
Get full details for each ticket including description and linked tickets.
"""
import os
import sys
import json
import requests
from pathlib import Path

# Load configuration
def load_config():
    """Load Jira configuration."""
    config = {}

    # Load token from env
    api_token = os.getenv('JIRA_API_TOKEN', '').strip()
    if api_token:
        config['api_token'] = api_token
    else:
        token_path = os.getenv(
            'JIRA_TOKEN_PATH',
            str(Path.home() / '.openclaw/workspace/projects/nextcode/.jira_token')
        )
        token_file = Path(token_path)
        if token_file.exists():
            with open(token_file, 'r') as f:
                config['api_token'] = f.read().strip()
        else:
            print(f"❌ Jira token file not found: {token_file}")
            sys.exit(1)
    
    # Load endpoint
    endpoint_env = os.getenv('JIRA_DOMAIN', '').strip()
    if endpoint_env:
        config['endpoint'] = endpoint_env
    else:
        config['endpoint'] = 'https://next-t-code.atlassian.net'
    
    # Load user
    user_env = os.getenv('JIRA_USER', '').strip()
    if user_env:
        config['user'] = user_env
    else:
        config['user'] = 'ihor.so@nextcode.tech'
    
    return config

def get_ticket_details(config, ticket_key):
    """Get detailed information about a specific ticket."""
    fields = [
        'summary', 'status', 'assignee', 'reporter', 'created', 'updated',
        'description', 'priority', 'labels', 'components', 'issuetype',
        'project', 'comment', 'issuelinks', 'attachment'
    ]
    
    endpoint = f"/issue/{ticket_key}"
    params = {
        'fields': fields,
        'expand': 'renderedFields'
    }
    
    url = f"{config['endpoint']}/rest/api/3{endpoint}"
    auth_string = f"{config['user']}:{config['api_token']}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f"Basic {auth_encoded}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting details for {ticket_key}: {e}")
        return None

import base64

def get_text_value(obj):
    """Extract text value from Jira field (can be dict or string)."""
    if isinstance(obj, dict):
        return obj.get('value', '') or obj.get('text', '') or obj.get('body', '')
    return str(obj) if obj else ''

def main():
    """Main function."""
    config = load_config()
    
    ticket_keys = [
        'CT-846', 'CT-834', 'CT-798', 'CT-750', 
        'CT-723', 'CT-705', 'CT-548'
    ]
    
    print(f"📋 Getting full details for {len(ticket_keys)} tickets...")
    
    tickets_data = []
    for key in ticket_keys:
        print(f"  Fetching {key}...")
        details = get_ticket_details(config, key)
        if details:
            tickets_data.append(details)
    
    # Save to file
    output_path = Path.home() / '.openclaw/workspace/shared/json-sources/jira/tickets-full-details.json'
    with open(output_path, 'w') as f:
        json.dump(tickets_data, f, indent=2)
    
    print(f"\n✅ Saved full details to: {output_path}")
    
    # Print summary for Nexus
    print("\n" + "="*80)
    print("SUMMARY FOR NEXUS ORCHESTRATOR")
    print("="*80)
    
    for ticket in tickets_data:
        fields = ticket['fields']
        key = ticket['key']
        status = fields.get('status', {}).get('name', 'Unknown')
        summary = fields.get('summary', 'No summary')
        assignee = fields.get('assignee', {}).get('displayName', 'Unassigned') if fields.get('assignee') else 'Unassigned'
        priority = fields.get('priority', {}).get('name', 'Medium')
        description = get_text_value(fields.get('description'))
        issuetype = fields.get('issuetype', {}).get('name', 'Unknown')
        project = fields.get('project', {}).get('name', 'Unknown')
        url = f"{config['endpoint']}/browse/{key}"
        
        print(f"\n[Ticket] {key} [{status}]")
        print(f"        Project: {project}")
        print(f"        Type: {issuetype}")
        print(f"        Summary: {summary}")
        print(f"        Assignee: {assignee}")
        print(f"        Priority: {priority}")
        print(f"        URL: {url}")
        
        if description:
            print(f"        Description:")
            lines = description.split('\n')
            for line in lines[:10]:  # First 10 lines
                if line.strip():
                    print(f"          {line}")
            if len(lines) > 10:
                print(f"          ... ({len(lines) - 10} more lines)")
        
        # Linked tickets
        issuelinks = fields.get('issuelinks', [])
        if issuelinks:
            print(f"        Linked Tickets:")
            for link in issuelinks[:5]:
                inward = link.get('inwardIssue', {})
                outward = link.get('outwardIssue', {})
                linked_key = inward.get('key') or outward.get('key')
                linked_summary = (inward.get('fields', {}).get('summary') or 
                                 outward.get('fields', {}).get('summary'))
                linked_status = (inward.get('fields', {}).get('status', {}).get('name') or 
                                 outward.get('fields', {}).get('status', {}).get('name'))
                if linked_key:
                    print(f"          - {linked_key}: {linked_summary} [{linked_status}]")
            if len(issuelinks) > 5:
                print(f"          ... and {len(issuelinks) - 5} more")
        
        # Comments
        comments = fields.get('comment', {}).get('comments', [])
        if comments:
            print(f"        Comments: {len(comments)} recent comment(s)")
            for comment in comments[:2]:
                author = comment.get('author', {}).get('displayName', 'Unknown')
                body = get_text_value(comment.get('body'))
                print(f"          {author}: {body[:150]}..." if len(body) > 150 else f"          {author}: {body}")
        
        print("-"*80)

if __name__ == "__main__":
    main()
