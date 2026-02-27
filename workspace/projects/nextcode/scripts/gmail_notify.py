#!/usr/bin/env python3
"""Gmail notifier - checks new emails, summarizes Jira tickets, sends to Telegram."""

import subprocess
import sys
import json
import re

def parse_email_output(output):
    """Parse email checker output."""
    emails = []
    current_email = None
    
    for line in output.split("\n"):
        line = line.strip()
        
        if line == "---EMAIL_START---":
            current_email = {}
        elif line == "---EMAIL_END---":
            if current_email:
                emails.append(current_email)
            current_email = None
        elif current_email is not None and ":" in line:
            key, value = line.split(":", 1)
            current_email[key.lower()] = value
    
    return emails


def summarize_jira_ticket(ticket_id):
    """Fetch and summarize Jira ticket (placeholder - needs Jira API)."""
    # For now, return ticket URL
    return f"https://next-t-code.atlassian.net/browse/{ticket_id}"


def format_email_notification(email):
    """Format email for Telegram notification."""
    msg = f"📬 **Новий лист**\n\n"
    msg += f"📧 **Від:** {email.get('from', 'Unknown')}\n"
    msg += f"📋 **Тема:** {email.get('subject', 'No subject')}\n"
    msg += f"📅 **Дата:** {email.get('date', 'Unknown')}\n"
    
    if email.get('is_jira') == 'True':
        ticket = email.get('jira_ticket')
        if ticket:
            msg += f"\n🎫 **Jira Ticket:** {ticket}\n"
            msg += f"🔗 {summarize_jira_ticket(ticket)}\n"
            msg += f"\n⚠️ **Потрібна дія:** Перевір тікет в Jira\n"
        else:
            msg += f"\n📢 **Оновлення Jira** (без номера тікета)\n"
    else:
        # Not Jira - show body preview
        body = email.get('body', '')[:300]
        msg += f"\n📝 **Preview:**\n{body}...\n"
    
    return msg


if __name__ == "__main__":
    # Run email checker
    result = subprocess.run(
        ["python3", "/Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py"],
        capture_output=True,
        text=True
    )
    
    output = result.stdout.strip()
    
    if "NO_NEW_EMAILS" in output:
        print("HEARTBEAT_OK")
        sys.exit(0)
    
    if "ERROR:" in output:
        print(f"❌ Gmail check error: {output}")
        sys.exit(1)
    
    # Parse emails
    emails = parse_email_output(output)
    
    if not emails:
        print("HEARTBEAT_OK")
        sys.exit(0)
    
    # Format notifications
    print(f"NEW_EMAILS:{len(emails)}")
    
    for email in emails:
        notification = format_email_notification(email)
        print("---NOTIFICATION_START---")
        print(notification)
        print("---NOTIFICATION_END---")
