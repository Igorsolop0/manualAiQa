# OpenClaw Current State (Phase 0-lite Baseline)

Date: 2026-03-13
Scope: Controlled baseline snapshot before contract-driven refactor.

## Core Operating Model

- Core trio is active and production-relevant:
- `Nexus` (main orchestrator: intake, planning, routing, review, summary)
- `Clawver` (UI/manual/browser QA execution, evidence collection)
- `Cipher` (API/backend/data-prep execution)

## Supporting Components

- `Researcher` exists but should be treated as async digest capability only.
- `Jira Watcher` exists and runs as deterministic scheduled intake; target shape is watcher/service style behavior.
- `Vision Scout` is deprecated for ticket-critical routing and should not be selected for mandatory execution.
- `Stagehand` is helper-only for unstable UI path discovery, not the primary test engine.

## Shared State Reality

- Existing active paths still rely on legacy shared folders under `workspace/shared/`:
- `workspace/shared/tasks/`
- `workspace/shared/credentials/`
- `workspace/shared/test-results/`

- This phase introduces top-level governance artifacts in `shared/registry/` without migrating active execution flows yet.

## Why This Baseline Exists

- Freeze current architecture before introducing contracts.
- Make maturity visible before changing routing logic.
- Reduce ambiguity without rewriting all persona/agent docs.
