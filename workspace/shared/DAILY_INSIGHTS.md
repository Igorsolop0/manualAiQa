# Daily Agent Insights & Errors

_This file is used by Clawver and Cipher to append short, evidence-backed learning candidates._

_Every night at 23:00, Nexus Orchestrator reads this file, abstracts the learned rules into `PROJECT_KNOWLEDGE.md`, and then clears this file._

---

## Entry Format

Use compact entries only:

```markdown
### 2026-03-15 - CT-750 - qa-agent
- Observed: unlink is blocked when user would lose the last valid login method
- Impact: social unlink plans must validate remaining login methods, not only UI success
- Applies to: Minebit social linking and unlinking flows
- Promote to: project
- Evidence: workspace/shared/test-results/CT-750/results.json
```

Valid `Promote to` values:

- `run-only`
- `project`
- `nexus-memory`
- `clawver-memory`
- `cipher-memory`

Do not paste raw logs or long narratives here.

## Summary of Rules (Last Updated: 2026-03-10)

See PROJECT_KNOWLEDGE.md for the full abstracted rules.

---

<!-- insight-id: d5ef2a8875c2 -->
### 2026-03-18 - CT-798 - qa-agent
- Observed: WebSocket connection to /wwa/basehub uses SignalR JSON hub protocol v1 with anonymous notification registration. WS establishes on first page load without auth. RegisterAnonymousForNotification called with arguments:[5] returns ResponseCode:0. Keep-alive ping/pong every ~15s. No live win events observed in 10s window for anonymous users. Recent Winners element found via data-cp selector showing static data.
- Impact: WebSocket infrastructure is working but live win streaming may require enableLiveUpdates Strapi config or authenticated session
- Applies to: CT-798,minebit-recent-winners,websocket-integration
- Promote to: run-only
- Evidence: workspace/shared/test-results/CT-798/results.json

<!-- insight-id: 096a905fbe2f -->
### 2026-03-18 - CT-548 - qa-agent
- Observed: test-social-linking page uses Connect buttons (not Link Google). OAuth flow opens popup to Google with linkToken in Base64-encoded state param. GetAuthUrl not called client-side - OAuth URL constructed directly in browser. Auth validation happens at callback not page load. FedCM provider not configured causes console warnings.
- Impact: linkToken confirmed present in OAuth state, AuthTokenMode=1, full E2E linking requires real Google account or callback mock
- Applies to: CT-548,CT-752,google-linking,social-linking
- Promote to: run-only
- Evidence: workspace/shared/test-results/CT-548/results.json
