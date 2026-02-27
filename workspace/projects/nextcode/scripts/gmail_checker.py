#!/usr/bin/env python3
"""Gmail checker - detects new emails and notifies via Telegram."""

import imaplib
import email
from email.header import decode_header
import json
import os
import re
from pathlib import Path

# Gmail IMAP settings
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL = "ihor.so@nextcode.tech"
APP_PASSWORD = "kokldpdfgtasosjx"

# State file for tracking seen emails
STATE_FILE = Path("/Users/ihorsolopii/.openclaw/workspace/.gmail_seen_ids.json")


def decode_str(s):
    """Decode email header string."""
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="ignore"))
        else:
            result.append(part)
    return "".join(result)


def load_seen_ids():
    """Load previously seen email IDs."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen_ids(ids):
    """Save seen email IDs."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(list(ids), f)


def extract_jira_ticket(text):
    """Extract Jira ticket ID from text."""
    match = re.search(r'\b([A-Z]+-\d+)\b', text)
    return match.group(1) if match else None


def check_new_emails():
    """Check for new emails and return unseen ones."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("INBOX")
        
        # Search for UNSEEN emails (IMAP handles read/unread status)
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        
        if not email_ids:
            print("NO_NEW_EMAILS")
            return []
        
        emails = []
        for email_id in email_ids[-10:]:  # Check last 10 unseen emails
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_str(msg["Subject"])
                    sender = decode_str(msg["From"])
                    date_str = msg["Date"]
                    
                    # Get body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                except:
                                    pass
                                break
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except:
                            pass
                    
                    # Extract Jira ticket if present
                    jira_ticket = extract_jira_ticket(subject) or extract_jira_ticket(body)
                    
                    emails.append({
                        "id": email_id.decode(),
                        "from": sender,
                        "subject": subject,
                        "date": date_str,
                        "body": body[:1000],
                        "jira_ticket": jira_ticket,
                        "is_jira": "jira@next-t-code.atlassian.net" in sender.lower()
                    })
        
        mail.close()
        mail.logout()
        
        # Mark processed emails as seen (read)
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            mail.login(EMAIL, APP_PASSWORD)
            mail.select("INBOX")
            for email_id in [e["id"] for e in emails]:
                mail.store(email_id, "+FLAGS", "\\Seen")
            mail.close()
            mail.logout()
        except:
            pass  # Don't fail if marking as read fails
        
        return emails
        
    except Exception as e:
        print(f"ERROR: {e}")
        return []


if __name__ == "__main__":
    # Initialize mode - mark all current emails as seen
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            mail.login(EMAIL, APP_PASSWORD)
            mail.select("INBOX")
            
            status, messages = mail.search(None, "ALL")
            email_ids = [eid.decode() for eid in messages[0].split()]
            
            save_seen_ids(set(email_ids))
            print(f"INITIALIZED with {len(email_ids)} emails marked as seen")
            
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"INIT_ERROR: {e}")
        sys.exit(0)
    
    # Normal check mode
    emails = check_new_emails()
    
    if emails:
        print(f"NEW_EMAILS_COUNT:{len(emails)}")
        for em in emails:
            print(f"---EMAIL_START---")
            print(f"ID:{em['id']}")
            print(f"FROM:{em['from']}")
            print(f"SUBJECT:{em['subject']}")
            print(f"DATE:{em['date']}")
            print(f"IS_JIRA:{em['is_jira']}")
            print(f"JIRA_TICKET:{em['jira_ticket'] or 'NONE'}")
            print(f"BODY:{em['body'][:500]}")
            print(f"---EMAIL_END---")
    else:
        print("NO_NEW_EMAILS")
