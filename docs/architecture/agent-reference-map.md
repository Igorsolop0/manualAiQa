# Agent Reference Map

Date: 2026-03-15
Scope: current active core trio after Phase 2 pilot and Phase 3 cleanup

Purpose: show which files Nexus, Clawver, and Cipher are expected to read at startup and during normal work.

## Shared Canonical Reference

All three agents share:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

This is the common meaning map for `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `MEMORY.md`, and `HEARTBEAT.md`.

## Nexus

Workspace root:

- `/Users/ihorsolopii/.openclaw/workspace/AGENTS.md`
- `/Users/ihorsolopii/.openclaw/workspace/SOUL.md`
- `/Users/ihorsolopii/.openclaw/workspace/IDENTITY.md`
- `/Users/ihorsolopii/.openclaw/workspace/USER.md`
- `/Users/ihorsolopii/.openclaw/workspace/TOOLS.md`
- `/Users/ihorsolopii/.openclaw/workspace/HEARTBEAT.md`
- `/Users/ihorsolopii/.openclaw/workspace/MEMORY.md`
- `/Users/ihorsolopii/.openclaw/workspace/ERRORS.md`
- `/Users/ihorsolopii/.openclaw/workspace/LEARNINGS.md`
- `/Users/ihorsolopii/.openclaw/workspace/PROJECT_KNOWLEDGE.md`

### Startup Reads

Always:

1. `workspace/SOUL.md`
2. `workspace/USER.md`
3. `workspace/memory/YYYY-MM-DD.md` for today and yesterday if present
4. `workspace/ERRORS.md`
5. `workspace/LEARNINGS.md`

Direct chat with Ihor:

1. `workspace/MEMORY.md`

Before routing:

1. `/Users/ihorsolopii/.openclaw/shared/registry/capabilities.yaml`
2. `/Users/ihorsolopii/.openclaw/shared/registry/maturity.yaml`

### Runtime Reads

When preparing tasks:

1. `workspace/shared/tasks/<ticket>.md`

When reviewing executor work:

1. `workspace/shared/test-results/<ticket>/`
2. `workspace/shared/test-results/<ticket>/results.json` when present

Phase 2 pilot only:

1. `/Users/ihorsolopii/.openclaw/shared/runs/active-pilot-runs.json`
2. `/Users/ihorsolopii/.openclaw/docs/runbooks/phase2-pilot-dual-write.md`
3. `/Users/ihorsolopii/.openclaw/shared/runs/<run_id>/`
4. `/Users/ihorsolopii/.openclaw/shared/sessions/registry.json`

Heartbeat only:

1. `workspace/HEARTBEAT.md`
2. scripts referenced inside it

## Clawver

Workspace root:

- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/AGENTS.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/SOUL.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/IDENTITY.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/USER.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/TOOLS.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/HEARTBEAT.md`
- `/Users/ihorsolopii/.openclaw/workspace-qa-agent/MEMORY.md`

### Startup Reads

Always:

1. `workspace-qa-agent/SOUL.md`
2. `workspace-qa-agent/USER.md`
3. `workspace-qa-agent/MEMORY.md`
4. assigned task file in `workspace/shared/tasks/`

Per task:

1. `workspace/shared/tasks/<ticket>.md`
2. `workspace/shared/test-results/<ticket>/RUN_ID.txt` if present

### Runtime Reads

During execution:

1. browser/profile details from `workspace-qa-agent/TOOLS.md`
2. credentials or session references named in the task file
3. task-specific evidence folder under `workspace/shared/test-results/<ticket>/`

Stagehand-specific:

1. task flag `Stagehand REQUIRED`, `auto`, or `off`
2. local Stagehand runner path from `workspace-qa-agent/TOOLS.md`

Phase 2 pilot only:

1. `workspace/shared/test-results/<ticket>/RUN_ID.txt`
2. `/Users/ihorsolopii/.openclaw/shared/runs/<run_id>/`
3. optional session refs registered under `/Users/ihorsolopii/.openclaw/shared/sessions/`

Heartbeat only:

1. `workspace-qa-agent/HEARTBEAT.md`

Default state: no recurring reads because heartbeat is intentionally empty.

## Cipher

Workspace root:

- `/Users/ihorsolopii/.openclaw/workspace-api-docs/AGENTS.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/SOUL.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/IDENTITY.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/USER.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/TOOLS.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/HEARTBEAT.md`
- `/Users/ihorsolopii/.openclaw/workspace-api-docs/MEMORY.md`

### Startup Reads

Always:

1. `workspace-api-docs/SOUL.md`
2. `workspace-api-docs/USER.md`
3. `workspace-api-docs/MEMORY.md`
4. assigned task file or handoff from Nexus

Per task:

1. `workspace/shared/tasks/<ticket>.md`
2. `workspace/shared/test-results/<ticket>/RUN_ID.txt` if present

### Runtime Reads

During execution:

1. local scripts under `workspace-api-docs/scripts/` when task requires them
2. Swagger/OpenAPI or endpoint references named in the task
3. auth/session refs passed by task or pilot metadata
4. task-specific evidence folder under `workspace/shared/test-results/<ticket>/`

Phase 2 pilot only:

1. `workspace/shared/test-results/<ticket>/RUN_ID.txt`
2. `/Users/ihorsolopii/.openclaw/shared/runs/<run_id>/`
3. `/Users/ihorsolopii/.openclaw/shared/sessions/registry.json`

Heartbeat only:

1. `workspace-api-docs/HEARTBEAT.md`

Default state: no recurring reads because heartbeat is intentionally empty.

## What Is Not On The Live Path

The following are not part of the current core agent startup/runtime surface:

- archived legacy docs under `/Users/ihorsolopii/.openclaw/docs/archive/legacy/`
- archived raw artifacts under `/Users/ihorsolopii/.openclaw/workspace/archive/`
- one-off screenshots, summaries, and experimental scripts unless a task explicitly points to them

Those files may still be useful as historical context, but agents should not rely on them implicitly.
