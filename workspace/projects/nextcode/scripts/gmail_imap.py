#!/usr/bin/env python3
"""Gmail IMAP client for fetching emails."""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os

# Gmail IMAP settings
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Credentials
EMAIL = "ihor.so@nextcode.tech"
APP_PASSWORD = "kokldpdfgtasosjx"  # Spaces removed


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


def get_emails(limit=10, unread_only=True):
    """Fetch emails from Gmail via IMAP."""
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, APP_PASSWORD)
        
        # Select inbox
        mail.select("INBOX")
        
        # Search for emails
        if unread_only:
            status, messages = mail.search(None, "UNSEEN")
        else:
            status, messages = mail.search(None, "ALL")
        
        email_ids = messages[0].split()
        
        if not email_ids:
            print("📭 No unread emails found.")
            return []
        
        # Get latest emails (reverse order)
        email_ids = email_ids[-limit:][::-1]
        
        emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Parse email
                    subject = decode_str(msg["Subject"])
                    sender = decode_str(msg["From"])
                    date_str = msg["Date"]
                    
                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
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
                    
                    emails.append({
                        "id": email_id.decode(),
                        "from": sender,
                        "subject": subject,
                        "date": date_str,
                        "body": body  # Full body
                    })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


if __name__ == "__main__":
    print(f"📧 Checking Gmail for {EMAIL}...")
    print("=" * 60)
    
    emails = get_emails(limit=10, unread_only=False)
    
    for i, em in enumerate(emails, 1):
        print(f"\n{'='*60}")
        print(f"[{i}] 📨 {em['subject']}")
        print(f"{'='*60}")
        print(f"From: {em['from']}")
        print(f"Date: {em['date']}")
        print(f"\n{'─'*60}")
        print("BODY:")
        print(f"{'─'*60}")
        print(em['body'])
    
    print(f"\n✅ Total unread: {len(emails)}")
