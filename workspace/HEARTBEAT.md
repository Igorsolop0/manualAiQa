# Heartbeat Tasks

## ⚠️ Vacation Mode (2026-02-25 to 2026-03-02)
**NextCode vacation active** — skip Jira ticket notifications.

Gmail checks still run, but DO NOT process or send Jira alerts.

Resume normal monitoring on **Monday, 2026-03-03**.

---

## Gmail Check (NextCode)
Check for new emails and notify if important:

```bash
python3 /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/gmail_checker.py
```

**VACATION MODE (2026-02-25 to 2026-03-02): Skip Jira processing**

If output contains `NEW_EMAILS_COUNT:`, parse emails and process:

**For Jira tickets:**
1. Extract ticket ID (e.g., CT-727)
2. Fetch ticket details using Jira API:
   ```bash
   python3 /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/jira_fetch.py CT-727
   ```
3. Summarize: status, priority, last comment, action needed
4. Send notification to Telegram (action=send, to=282986529, channel=telegram)

**For non-Jira emails:**
1. Show sender, subject, preview
2. Assess urgency
3. Send notification

## Frequency
Check every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri).

---

## ConfAdapt Technology Monitor (Weekly)
Monitor developments in multi-token prediction / ConfAdapt research.

**Schedule:** Every Monday at 10:00 AM (or during Monday heartbeat)

**Check if:** Today is Monday AND last check was >6 days ago

**Script:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/confadapt_monitor.py
```

**State file:** `memory/confadapt_state.json`
**Log file:** `memory/confadapt_log.md`

**When changes detected:**
1. Read the report from script output
2. Send summary to Telegram (to=282986529, channel=telegram)
3. Update state file automatically

**Manual check anytime:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/confadapt_monitor.py
```
