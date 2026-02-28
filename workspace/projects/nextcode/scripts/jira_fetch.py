#!/usr/bin/env python3
"""Fetch Jira ticket details using go-jira CLI."""

import subprocess
import sys
import os


def fetch_ticket(ticket_id):
    """Fetch Jira ticket details."""
    try:
        # Read API token
        with open("/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/.jira_token") as f:
            token = f.read().strip()
        
        # Set environment
        env = os.environ.copy()
        env["JIRA_API_TOKEN"] = token
        
        # Run jira command
        result = subprocess.run(
            [
                "jira", "view", ticket_id,
                "-e", "https://next-t-code.atlassian.net",
                "-u", "ihor.so@nextcode.tech"
            ],
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode != 0:
            return f"ERROR: {result.stderr}"
        
        return result.stdout
        
    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 jira_fetch.py <TICKET-ID>")
        sys.exit(1)
    
    ticket_id = sys.argv[1]
    print(fetch_ticket(ticket_id))
