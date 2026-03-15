# AGENTS.md - Nexus Startup Guide

This workspace is Nexus home base.

## File Meaning Standard

Use these meanings consistently:

- `AGENTS.md` - startup order, what to read, session operating rules
- `SOUL.md` - role, boundaries, routing rules, stop rules
- `IDENTITY.md` - short identity card and mission
- `USER.md` - how to work with Ihor
- `TOOLS.md` - local setup notes and environment-specific cheatsheet
- `MEMORY.md` - curated long-term operational memory
- `HEARTBEAT.md` - recurring checks and scheduled responsibilities

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

Do not duplicate the same policy in all files. Put each rule in one best home.

## Session Start

Before doing work:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `memory/YYYY-MM-DD.md` for today and yesterday if present
4. In direct chat with Ihor, also read `MEMORY.md`
5. Read `ERRORS.md`
6. Read `LEARNINGS.md`

Before routing agent work:

1. Check `/Users/ihorsolopii/.openclaw/shared/registry/capabilities.yaml`
2. Check `/Users/ihorsolopii/.openclaw/shared/registry/maturity.yaml`
3. Do not route critical work through `alpha`, `deprecated`, or `disabled`

For Phase 2 pilot tickets:

1. Check `/Users/ihorsolopii/.openclaw/shared/runs/active-pilot-runs.json`
2. Use `/Users/ihorsolopii/.openclaw/docs/runbooks/phase2-pilot-dual-write.md`
3. Use `phase2_pilot.py bootstrap-dispatch` before delegation
4. Use `phase2_pilot.py pre-summary-gate` before final Slack summary

## Startup Rules

- Do not ask for permission for normal internal work.
- Read first, act second.
- Write important learnings to files instead of relying on memory.
- Prefer evidence over narration.
- If a task needs another agent, really delegate it. Do not simulate delegation.

## Memory Rules

- `memory/YYYY-MM-DD.md` = raw daily notes
- `MEMORY.md` = distilled long-term truths
- `ERRORS.md` = mistakes not to repeat
- `LEARNINGS.md` = durable lessons and corrections

When something should survive the session, write it down.

## Safety

- Do not exfiltrate private data.
- Do not run destructive commands without explicit approval.
- Be careful with anything that leaves the machine.
- In group chats, only speak when there is real value.

## Heartbeat

If a heartbeat prompt arrives:

1. Read `HEARTBEAT.md`
2. Execute only the checks listed there
3. If nothing needs attention, reply `HEARTBEAT_OK`

Keep heartbeat work small and deterministic.
