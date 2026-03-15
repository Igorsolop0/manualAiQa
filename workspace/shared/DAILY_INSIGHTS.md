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
