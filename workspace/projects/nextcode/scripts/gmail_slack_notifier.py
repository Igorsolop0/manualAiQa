#!/usr/bin/env python3
"""Gmail Slack notifier - sends new email alerts to Slack."""

import subprocess
import sys
import json
import re
import os
from datetime import datetime

# Slack channel IDs
SLACK_CHANNEL_GMAIL = "C0AH7CRFQES"      # #gmail channel
SLACK_CHANNEL_QA = "C0AH10XDKM2"         # #qa-testing channel

def parse_email_output(output):
    """Parse email checker output."""
    emails = []
    current_email = {} # type: ignore

    for line in output.split("\n"):
        line = line.strip()

        if line == "---EMAIL_START---":
            current_email = {}
        elif line == "---EMAIL_END---":
            if current_email:
                emails.append(current_email)
            current_email = {} # type: ignore
        elif current_email and ":" in line:
            key, value = line.split(":", 1)
            current_email[key.lower()] = value

    return emails


def format_slack_notification(email):
    """Format email for Slack notification based on content type."""
    is_jira = email.get('is_jira') == 'True'
    
    if is_jira:
        ticket = email.get('jira_ticket')
        ticket_link = f"<https://next-t-code.atlassian.net/browse/{ticket}|{ticket}>" if ticket else "Jira Update"
        subject = email.get('subject', 'No subject')
        
        # Clean subject for header (remove ticket ID if present)
        clean_subject = str(subject.replace(f"[{ticket}]", "").strip()) if ticket else str(subject)
        header_text = f"🎫 {ticket}: {clean_subject}"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header_text[:150],  # type: ignore
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🔗 *Link:* {ticket_link}\n📅 *Date:* {email.get('date', 'Unknown')}\n👤 *From:* {email.get('from', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📝 *Details:*\n```{email.get('body', '')[:1000]}```"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🤖 _Reply to this thread to trigger the AI Testing Pipeline for this ticket._"
                    }
                ]
            }
        ]
        return json.dumps(blocks)
    
    # Normal email formatting
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📬 Новий лист в Gmail",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Від:*\n{email.get('from', 'Unknown')}\n\n*Дата:*\n{email.get('date', 'Unknown')}\n\n*Тема:*\n{email.get('subject', 'No subject')}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"📝 *Preview:*\n```{email.get('body', '')[:500]}```"
            }
        }
    ]

    return json.dumps(blocks)


def send_to_slack(message, channel_id):
    """Send message to Slack using slack_message_helper.py."""
    try:
        helper_path = os.path.join(os.path.dirname(__file__), "slack_message_helper.py")
        result = subprocess.run(
            [
                sys.executable, helper_path,
                "--channel", channel_id,
                "--blocks", message
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"ERROR: Failed to send to Slack: {result.stderr} {result.stdout}")
            return None

        try:
            res_data = json.loads(result.stdout)
            return res_data.get("ts")
        except json.JSONDecodeError:
            return True
            
    except subprocess.TimeoutExpired:
        print("ERROR: Slack send timeout")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def save_jira_thread(ticket, ts):
    """Save Jira ticket thread timestamp for the agent to use."""
    if not ticket or not ts:
        return
        
    thread_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "jira_threads.json")
    threads = {} # type: ignore
    
    if os.path.exists(thread_file):
        try:
            with open(thread_file, 'r') as f:
                threads = json.load(f)
        except Exception:
            pass
            
    threads[str(ticket)] = str(ts) # type: ignore
    
    with open(thread_file, 'w') as f:
        json.dump(threads, f, indent=2)


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

    # Send notifications to Slack
    for email in emails:
        notification = format_slack_notification(email)
        is_jira = email.get('is_jira') == 'True'
        target_channel = SLACK_CHANNEL_QA if is_jira else SLACK_CHANNEL_GMAIL
        
        ts = send_to_slack(notification, target_channel)
        if ts:
            print(f"✅ Sent to Slack ({target_channel}): {email.get('subject', 'No subject')}")
            # If it's a Jira ticket, save the thread_ts for the agent
            if is_jira and email.get('jira_ticket'):
                save_jira_thread(email.get('jira_ticket'), ts)
        else:
            print(f"❌ Failed ({target_channel}): {email.get('subject', 'No subject')}")

    print(f"TOTAL: {len(emails)} email(s) sent to Slack")
