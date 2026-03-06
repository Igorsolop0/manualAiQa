# Jira Watcher

Autonomous monitoring agent running on a schedule (1h) to report Jira status changes.

## About

I poll Jira (e.g., project PandaSen) to check if any tickets moved to "Ready for Testing" or "On Production". If they do, I extract full context and trigger Nexus.

## Key Files

- `SOUL.md` — My instructions
- Output → `~/.openclaw/workspace/shared/json-sources/jira/sprint-current.json`
