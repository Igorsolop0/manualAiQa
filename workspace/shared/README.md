# Shared Workspace

Inter-agent data exchange directory for the Nexus multi-agent system.

## Structure

- `screenshots/` — UI screenshots for Vision Scout analysis
- `test-results/` — QA Agent test results and evidences (per-ticket: `CT-XXX/`)
- `json-sources/` — Raw data from external systems
  - `swagger/` — Swagger JSON schemas
  - `jira/` — Jira ticket snapshots
  - `gmail/` — Gmail parsed summaries
- `SECURITY_KEY_ROTATION_RUNBOOK.md` — Step-by-step key rotation runbook for gateway/channels/providers

## Contracts

| Producer | Consumer | File |
|----------|----------|------|
| Vision Scout | QA Agent | `UI_ELEMENTS.md` |
| QA Agent | Nexus | `test-results/CT-XXX/report.md` |
| Jira Watcher | Nexus | `json-sources/jira/sprint-current.json` |
| API Docs Agent | QA Agent | `json-sources/swagger/*.json` |
| Gmail Cron | Nexus | `json-sources/gmail/latest.json` |
