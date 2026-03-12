# Security Key Rotation Runbook

This runbook describes safe key rotation for the local OpenClaw setup without breaking gateway, agents, or cron jobs.

## Scope

Applies to secrets used by:
- OpenClaw gateway auth
- Slack and Telegram channels
- Model providers (`zai`, `zai-coding`, `deepseek`, `openai`)
- Jira/API helper scripts

## Files involved

- `/Users/ihorsolopii/.openclaw/openclaw.json`
- `/Users/ihorsolopii/Library/LaunchAgents/ai.openclaw.gateway.plist`
- `/Users/ihorsolopii/.openclaw/agents/*/agent/models.json`
- `/Users/ihorsolopii/.openclaw/workspace-jira-watcher/scripts/jira_watcher.py`
- `/Users/ihorsolopii/.openclaw/workspace-jira-watcher/check_pandasen_tickets.py`
- `/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/slack_message_helper.py`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/scripts/check_rakeback.py`

## Required env keys

- `GATEWAY_AUTH_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `ZAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `OPENAI_API_KEY`
- `JIRA_API_TOKEN`
- `TAVILY_API_KEY` (if used)

## Rotation checklist

1. Generate new keys in each provider console (do not revoke old ones yet).
2. Update `/Users/ihorsolopii/.openclaw/openclaw.json` `env` values with new keys.
3. Sync env keys into LaunchAgent plist:
```bash
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
CFG="$HOME/.openclaw/openclaw.json"
cp "$PLIST" "$PLIST.bak.$(date +%Y%m%d%H%M%S)"
for key in TELEGRAM_BOT_TOKEN SLACK_BOT_TOKEN SLACK_APP_TOKEN GATEWAY_AUTH_TOKEN DEEPSEEK_API_KEY ZAI_API_KEY OPENAI_API_KEY JIRA_API_TOKEN TAVILY_API_KEY; do
  val=$(jq -r --arg k "$key" '.env[$k] // empty' "$CFG")
  [ -n "$val" ] || continue
  /usr/libexec/PlistBuddy -c "Delete :EnvironmentVariables:$key" "$PLIST" >/dev/null 2>&1 || true
  /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:$key string $val" "$PLIST"
done
chmod 600 "$PLIST"
plutil -lint "$PLIST"
```
4. Restart gateway:
```bash
cd ~/.openclaw
openclaw gateway restart
openclaw gateway status --json
```
5. Validate config and secrets:
```bash
cd ~/.openclaw
openclaw config validate
openclaw secrets audit --json
```
Expected: `plaintextCount=0`, `unresolvedRefCount=0`, `shadowedRefCount=0`.
6. Smoke-check cron/jobs:
```bash
cd ~/.openclaw
openclaw cron status --json
openclaw cron runs --id jira-monitor-hourly --limit 1 --expect-final
openclaw cron runs --id api-docs-daily --limit 1 --expect-final
```
7. Revoke old keys in provider consoles only after successful validation.

## Fast rollback

If something fails after rotation:

1. Restore previous plist:
```bash
cp "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist.bak.<timestamp>" \
   "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
```
2. Restore previous `openclaw.json` from backup.
3. Restart gateway:
```bash
cd ~/.openclaw
openclaw gateway restart
openclaw gateway status --json
```

## Notes

- Keep `channels.*` and `gateway.auth.token` in `openclaw.json` as SecretRef objects (not plaintext).
- `agents/*/agent/models.json` may contain provider marker values (for audit compatibility).
- Never commit real secrets to git history.
