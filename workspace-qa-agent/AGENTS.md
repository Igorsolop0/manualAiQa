# QA Agent Startup Guide

This workspace belongs to Clawver.

## File Meaning Standard

Use these meanings consistently:

- `AGENTS.md` - startup order and session rules
- `SOUL.md` - role, execution rules, boundaries, stop rules
- `IDENTITY.md` - short identity and mission
- `USER.md` - what matters to Ihor when reviewing QA work
- `TOOLS.md` - local environment notes
- `MEMORY.md` - curated QA operational memory
- `HEARTBEAT.md` - recurring checks, if any

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

Do not spread the same rule across every file.

## Session Start

Before acting:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `MEMORY.md`
4. Read the assigned task file in `workspace/shared/tasks/`
5. Check whether `RUN_ID.txt` exists in `workspace/shared/test-results/<ticket>/`

If pilot is active:

1. Keep writing legacy evidence under `workspace/shared/test-results/<ticket>/`
2. Run `phase2_pilot.py sync-legacy --ticket <ticket>` after execution
3. Run `phase2_pilot.py stagehand-guard ...` before normal result emission for Stagehand tasks
4. Emit `result-packet` for Nexus review
5. Run `phase2_pilot.py emit-learning ...` (mandatory — every run must emit at least one learning candidate)
6. Use `/Users/ihorsolopii/.openclaw/docs/runbooks/core-trio-ops-checklist.md` as the strict command order

## Startup Rules

- Read the whole task before opening the browser.
- Follow Nexus scope exactly.
- Keep one ticket or one charter per execution.
- Prefer evidence over explanation.
- If the task is backend-only, hand it off instead of improvising UI work.

## Safety

- Do not create users unless the task explicitly allows it.
- Do not do risky PROD actions.
- Do not invent evidence or claim execution from generated code alone.
- Do not post directly to Slack or Jira.
