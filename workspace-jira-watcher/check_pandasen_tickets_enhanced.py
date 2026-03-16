#!/usr/bin/env python3
"""
Enhanced Jira Watcher - Check PandaSen tickets in Ready for Testing or On Production states.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# Load configuration
def load_config():
    """Load Jira configuration from token file and yaml config."""
    config = {}

    # Load token from env first; fallback to token file for backward compatibility.
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
            print("   Set JIRA_API_TOKEN or JIRA_TOKEN_PATH")
            sys.exit(1)
    
    # Load endpoint from env first, then ~/.jira.yml
    endpoint_env = os.getenv('JIRA_DOMAIN', '').strip()
    if endpoint_env:
        config['endpoint'] = endpoint_env

    jira_yml = Path.home() / '.jira.yml'
    if 'endpoint' not in config and jira_yml.exists():
        with open(jira_yml, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'endpoint:' in line:
                    config['endpoint'] = line.split(':', 1)[1].strip()
                    break
    if 'endpoint' not in config:
        # Default endpoint
        config['endpoint'] = 'https://next-t-code.atlassian.net'
    
    # User from env first, then ~/.jira.yml, then default.
    user_env = os.getenv('JIRA_USER', '').strip()
    if user_env:
        config['user'] = user_env
    else:
        config['user'] = 'ihor.so@nextcode.tech'

    if not user_env and jira_yml.exists():
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
        fields = ['summary', 'status', 'assignee', 'created', 'updated', 'priority', 'labels', 'project']
    
    params = {
        'jql': jql,
        'fields': fields,
        'maxResults': max_results,
        'expand': 'names'
    }
    
    result = jira_api_request(config, 'GET', '/search/jql', params=params)
    return result

def get_ticket_details(config, ticket_key):
    """Get detailed information about a specific ticket including description and linked tickets."""
    fields = [
        'summary', 'status', 'assignee', 'reporter', 'created', 'updated',
        'description', 'priority', 'labels', 'components', 'issuetype',
        'project', 'comment', 'issuelinks'
    ]
    
    endpoint = f"/issue/{ticket_key}"
    params = {
        'fields': fields,
        'expand': 'renderedFields'
    }
    
    return jira_api_request(config, 'GET', endpoint, params=params)

def get_ticket_comments(config, ticket_key):
    """Get comments for a ticket."""
    endpoint = f"/issue/{ticket_key}/comment"
    params = {
        'maxResults': 50,
        'expand': 'renderedBody'
    }
    
    result = jira_api_request(config, 'GET', endpoint, params=params)
    if not result:
        return []
    
    comments = result.get('comments', [])
    return comments

def check_pandasen_tickets(config):
    """
    Check for PandaSen project tickets in Ready for Testing or On Production.
    Returns list of ticket details.
    """
    # JQL query - PandaSen project with Ready for Testing OR On Production
    jql = 'project = "CT" AND (status in ("Ready for testing", "On Production"))'
    
    print(f"🔍 Searching Jira for: {jql}")
    search_result = search_tickets(config, jql, max_results=20)
    
    if not search_result:
        print("❌ No results or API error")
        return []
    
    tickets = search_result.get('issues', [])
    print(f"✅ Found {len(tickets)} ticket(s) in target states")
    
    # Parse ticket details with enhanced information
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
        
        # Get project
        project = fields.get('project', {})
        project_name = project.get('name', 'Unknown')
        
        # Get description
        description = fields.get('description', '')
        
        # Get issue type
        issuetype = fields.get('issuetype', {})
        issuetype_name = issuetype.get('name', 'Unknown')
        
        # Get linked tickets
        issuelinks = fields.get('issuelinks', [])
        linked_tickets = []
        for link in issuelinks:
            inward = link.get('inwardIssue', {})
            outward = link.get('outwardIssue', {})
            
            # Prefer inward (this ticket links to) or outward (this ticket is linked by)
            linked_key = inward.get('key') or outward.get('key')
            linked_summary = inward.get('fields', {}).get('summary') or outward.get('fields', {}).get('summary')
            linked_status = inward.get('fields', {}).get('status', {}).get('name') or outward.get('fields', {}).get('status', {}).get('name')
            
            if linked_key:
                linked_tickets.append({
                    'key': linked_key,
                    'summary': linked_summary or 'No summary',
                    'status': linked_status or 'Unknown'
                })
        
        # Get comments
        comments = get_ticket_comments(config, key)
        formatted_comments = []
        for comment in comments[:10]:  # Limit to 10 recent comments
            comment_body = comment.get('body', '')
            # Handle both string and dict body
            if isinstance(comment_body, str):
                body_text = comment_body[:200] if comment_body else 'No content'
            elif isinstance(comment_body, dict):
                body_text = comment_body.get('content', [{}])[0].get('content', [{}])[0].get('text', '')[:200]
            else:
                body_text = str(comment_body)[:200]
            
            formatted_comments.append({
                'author': comment.get('author', {}).get('displayName', 'Unknown'),
                'body': body_text,
                'created': comment.get('created', ''),
                'updated': comment.get('updated', '')
            })
        
        ticket_details.append({
            'key': key,
            'project': project_name,
            'summary': summary,
            'status': status_name,
            'assignee': assignee_name,
            'priority': priority,
            'issuetype': issuetype_name,
            'created': created,
            'updated': fields.get('updated', ''),
            'description': description,
            'linked_tickets': linked_tickets,
            'comments': formatted_comments,
            'url': f"{config['endpoint']}/browse/{key}"
        })
    
    return ticket_details

def save_results(ticket_details, output_path):
    """Save results to JSON file."""
    with open(output_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'count': len(ticket_details),
            'tickets': ticket_details
        }, f, indent=2)
    print(f"\n💾 Results saved to: {output_path}")
    return output_path

def main():
    """Main function."""
    print("🎫 Enhanced Jira Watcher - PandaSen Project Check")
    print("=" * 50)
    
    # Load config
    config = load_config()
    print(f"📡 Endpoint: {config['endpoint']}")
    print(f"👤 User: {config['user']}")
    
    # Check for PandaSen tickets
    tickets = check_pandasen_tickets(config)
    
    if tickets:
        print("\n📋 Tickets found:")
        for i, ticket in enumerate(tickets, 1):
            print(f"\n  {i}. {ticket['key']} [{ticket['status']}]")
            print(f"     Summary: {ticket['summary']}")
            print(f"     Assignee: {ticket['assignee']}")
            print(f"     Priority: {ticket['priority']}")
            print(f"     Type: {ticket['issuetype']}")
            print(f"     Created: {ticket['created'][:10] if ticket['created'] else 'N/A'}")
            print(f"     URL: {ticket['url']}")
            
            if ticket['linked_tickets']:
                print(f"     Linked Tickets:")
                for link in ticket['linked_tickets'][:3]:  # Show first 3
                    print(f"       - {link['key']}: {link['summary']} [{link['status']}]")
                if len(ticket['linked_tickets']) > 3:
                    print(f"       ... and {len(ticket['linked_tickets']) - 3} more")
            
            if ticket['comments']:
                print(f"     Comments ({len(ticket['comments'])}):")
                for comment in ticket['comments'][:2]:  # Show first 2 comments
                    print(f"       - {comment['author']}: {comment['body'] if comment['body'] else 'No content'}...")
        
        # Save to output file
        output_path = Path.home() / '.openclaw/workspace/shared/json-sources/jira/sprint-current.json'
        save_results(tickets, output_path)
        
        print("\n✅ Successfully processed tickets for Nexus")
        return tickets
    else:
        print("\n✅ No PandaSen tickets in Ready for Testing or On Production states")
        return []

if __name__ == "__main__":
    main()
