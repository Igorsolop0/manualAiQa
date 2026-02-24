# Heartbeat Tasks

## Gmail Check
Check for new emails and notify if important:

```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py
```

If output contains `NEW_EMAILS_COUNT:`, parse emails and process:

**For Jira tickets:**
1. Extract ticket ID (e.g., CT-727)
2. Fetch ticket details using Jira API:
   ```bash
   python3 /Users/ihorsolopii/.openclaw/workspace/scripts/jira_fetch.py CT-727
   ```
3. Summarize: status, priority, last comment, action needed
4. Send notification to Telegram (action=send, to=282986529, channel=telegram)

**For non-Jira emails:**
1. Show sender, subject, preview
2. Assess urgency
3. Send notification

## Frequency
Check every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri).
