# Safe Cleanup Plan - 2026-03-15

Purpose: reduce top-level workspace noise without deleting historical material or active runtime inputs.

## Principles

- Do not move active agent bootstrap files.
- Do not move files explicitly referenced by active skills or shared runtime flow.
- Prefer `docs/archive/legacy/` for legacy docs and one-off plans.
- Prefer `workspace/archive/` for raw artifacts and ad-hoc scripts.
- Keep `QA_TEST_DESIGN_APPROACH.md` in place for later review.

## Keep In Place

- `workspace/AGENTS.md`
- `workspace/SOUL.md`
- `workspace/IDENTITY.md`
- `workspace/USER.md`
- `workspace/TOOLS.md`
- `workspace/HEARTBEAT.md`
- `workspace/MEMORY.md`
- `workspace/ERRORS.md`
- `workspace/LEARNINGS.md`
- `workspace/PROJECT_KNOWLEDGE.md`
- `workspace/TESTRAIL_STANDARDS.md`
- `workspace/QA_TEST_DESIGN_APPROACH.md`
- `workspace/package.json`
- `workspace/package-lock.json`
- runtime state files such as `.gmail_seen_ids.json`, `.austria_summary_state.json`, `.reminder`

## Move To docs/archive/legacy/workspace-root/

- `workspace/JIRA_REPORT_BURGER_MENU.md`
- `workspace/PLAYWRIGHT_CLI.md`
- `workspace/PLAYWRIGHT_DEVICES.md`
- `workspace/QA_AGENT_RECOMMENDATIONS.md`
- `workspace/MODEL_BENCHMARK.md`
- `workspace/MEMORY_ARCHITECTURE_SDD.md`
- `workspace/MEMORY.md.bak_split`
- `workspace/openclaw_visualization.html`
- `workspace/migration-checklist-mac.md`

Reason: legacy reference docs, design notes, or one-off artifacts that are not part of current agent startup or runtime flow.

## Move To docs/archive/legacy/workspace-qa-agent/

- `workspace-qa-agent/BOOTSTRAP.md`
- `workspace-qa-agent/CT-773_TEST_PLAN.md`

Reason: bootstrap template and one-off ticket plan; not part of current Clawver runtime surface.

## Move To workspace/archive/raw-artifacts/

- `workspace/austria_summary_2026-03-01.txt`
- `workspace/summary.txt`
- `workspace/summary_2026-02-28.txt`
- `workspace/screen.b64`

Reason: output artifacts and historical summaries, not agent instructions.

## Move To workspace/archive/scripts/

- `workspace-qa-agent/test_google_play.js`

Reason: ad-hoc experimental script, not part of the current delegated execution path.

## Deferred

- `workspace/QA_TEST_DESIGN_APPROACH.md`
  - Review separately as a possible practical test-design framework for Nexus.
- `workspace/package.json` and `workspace/package-lock.json`
  - Keep for now because they may still support local workspace tooling.
