#!/usr/bin/env python3
"""
Jira API Poller - directly query Jira for tickets ready for testing.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Load configuration
def load_config():
    """Load Jira configuration from token file and yaml config."""
    config = {}
    
    # Load token
    token_file = Path(__file__).parent.parent / '.jira_token'
    if token_file.exists():
        with open(token_file, 'r') as f:
            config['api_token'] = f.read().strip()
    else:
        print(f"❌ Jira token file not found: {token_file}")
        sys.exit(1)
    
    # Load endpoint from ~/.jira.yml
    jira_yml = Path.home() / '.jira.yml'
    if jira_yml.exists():
        with open(jira_yml, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'endpoint:' in line:
                    config['endpoint'] = line.split(':', 1)[1].strip()
                    break
    else:
        # Default endpoint
        config['endpoint'] = 'https://next-t-code.atlassian.net'
    
    # User from ~/.jira.yml or default
    config['user'] = 'ihor.so@nextcode.tech'
    if jira_yml.exists():
        with open(jira_yml, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'user:' in line:
                    config['user'] = line.split(':', 1)[1].strip()
                    break
    
    return config

def jira_api_request(config, method='GET', endpoint_path='', params=None, data=None):
    """Make a request to Jira REST API."""
    url = f"{config['endpoint']}/rest/api/3{endpoint_path}"
    
    # Basic auth with email:api_token
    import base64
    auth_string = f"{config['user']}:{config['api_token']}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f"Basic {auth_encoded}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            response = requests.request(method, url, headers=headers, json=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Jira API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
        return None

def search_tickets(config, jql, fields=None, max_results=50):
    """Search tickets using JQL."""
    if fields is None:
        fields = ['summary', 'status', 'assignee', 'created', 'updated', 'priority', 'labels']
    
    params = {
        'jql': jql,
        'fields': fields,
        'maxResults': max_results,
        'expand': 'names'
    }
    
    result = jira_api_request(config, 'GET', '/search/jql', params=params)
    return result

def get_ticket_details(config, ticket_key):
    """Get detailed information about a specific ticket."""
    fields = [
        'summary', 'status', 'assignee', 'reporter', 'created', 'updated',
        'description', 'priority', 'labels', 'components', 'issuetype',
        'project', 'comment'
    ]
    
    endpoint = f"/issue/{ticket_key}"
    params = {
        'fields': fields,
        'expand': 'renderedFields'
    }
    
    return jira_api_request(config, 'GET', endpoint, params=params)

def check_tickets_ready_for_testing(config):
    """
    Check for tickets with status "Ready for Testing" assigned to Ihor.
    Returns list of ticket keys and details.
    """
    # JQL query
    jql = 'status = "Ready for Testing" AND assignee = "Ihor Solopii"'
    
    print(f"🔍 Searching Jira for: {jql}")
    search_result = search_tickets(config, jql, max_results=20)
    
    if not search_result:
        print("❌ No results or API error")
        return []
    
    tickets = search_result.get('issues', [])
    print(f"✅ Found {len(tickets)} ticket(s) ready for testing")
    
    # Parse ticket details
    ticket_details = []
    for ticket in tickets:
        key = ticket['key']
        fields = ticket['fields']
        
        # Get status name
        status_name = fields.get('status', {}).get('name', 'Unknown')
        
        # Get assignee
        assignee = fields.get('assignee', {})
        assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
        
        # Get summary
        summary = fields.get('summary', 'No summary')
        
        # Get priority
        priority = fields.get('priority', {}).get('name', 'Medium')
        
        # Get created date
        created = fields.get('created', '')
        
        ticket_details.append({
            'key': key,
            'summary': summary,
            'status': status_name,
            'assignee': assignee_name,
            'priority': priority,
            'created': created,
            'url': f"{config['endpoint']}/browse/{key}",
            'raw': ticket  # Keep raw data for reference
        })
    
    return ticket_details

def save_thread_timestamp(ticket_key, thread_ts, file_path=None):
    """Save Jira ticket thread timestamp for Slack threading."""
    if file_path is None:
        file_path = Path(__file__).parent.parent / 'jira_threads.json'
    
    threads = {}
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                threads = json.load(f)
        except json.JSONDecodeError:
            pass
    
    threads[ticket_key] = thread_ts
    
    with open(file_path, 'w') as f:
        json.dump(threads, f, indent=2)
    
    print(f"💾 Saved thread_ts for {ticket_key}")

def main():
    """Main function."""
    print("🎫 Jira API Poller")
    print("=" * 50)
    
    # Load config
    config = load_config()
    print(f"📡 Endpoint: {config['endpoint']}")
    print(f"👤 User: {config['user']}")
    print(f"🔑 API Token: {config['api_token'][:10]}...{config['api_token'][-10:]}")
    
    # Test API access with a simple request
    print("\n🧪 Testing Jira API access...")
    test_result = jira_api_request(config, 'GET', '/myself')
    if test_result:
        print(f"✅ Jira API access successful!")
        print(f"   Logged in as: {test_result.get('displayName', 'Unknown')}")
        print(f"   Email: {test_result.get('emailAddress', 'Unknown')}")
    else:
        print("❌ Cannot access Jira API. Check token and network.")
        sys.exit(1)
    
    # Check for tickets ready for testing
    tickets = check_tickets_ready_for_testing(config)
    
    if tickets:
        print("\n📋 Tickets ready for testing:")
        for i, ticket in enumerate(tickets, 1):
            print(f"\n  {i}. {ticket['key']}: {ticket['summary']}")
            print(f"     Status: {ticket['status']}")
            print(f"     Priority: {ticket['priority']}")
            print(f"     Created: {ticket['created'][:10] if ticket['created'] else 'N/A'}")
            print(f"     URL: {ticket['url']}")
        
        # Save to JSON file for other scripts
        output_file = Path(__file__).parent / 'jira_tickets_ready.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'count': len(tickets),
                'tickets': tickets
            }, f, indent=2)
        
        print(f"\n💾 Ticket list saved to: {output_file}")
        
        # Return ticket keys for integration
        ticket_keys = [t['key'] for t in tickets]
        print(f"\n🎯 Ticket keys: {', '.join(ticket_keys)}")
        return ticket_keys
    else:
        print("\n✅ No tickets currently ready for testing.")
        return []

if __name__ == "__main__":
    main()