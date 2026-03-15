# Cipher Startup Guide

This workspace belongs to Cipher.

## File Meaning Standard

Use these meanings consistently:

- `AGENTS.md` - startup order and session rules
- `SOUL.md` - role, execution modes, boundaries, stop rules
- `IDENTITY.md` - short identity and mission
- `USER.md` - what matters to Ihor for backend and API work
- `TOOLS.md` - local environment and script notes
- `MEMORY.md` - curated backend operational memory
- `HEARTBEAT.md` - recurring checks, if any

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

Do not repeat the same policy across all files.

## Session Start

Before acting:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `MEMORY.md`
4. Read the assigned task file or handoff from Nexus
5. Check whether `RUN_ID.txt` exists in `workspace/shared/test-results/<ticket>/`

If pilot is active:

1. Keep writing legacy evidence under `workspace/shared/test-results/<ticket>/`
2. Run `phase2_pilot.py sync-legacy --ticket <ticket>` after execution
3. Emit `result-packet` for Nexus review

## Startup Rules

- Check the actual Swagger, script, or endpoint before making claims.
- Prefer existing local scripts over inventing new tooling.
- Keep `api.execute` and `data.prepare` conceptually separate in your head and report.
- Do not simulate UI work.
- Prefer structured evidence over prose summaries.

## Safety

- Do not run risky PROD mutations without explicit instruction.
- Do not send raw tokens in prose.
- Do not guess payloads or endpoint semantics.
- Do not post directly to Slack or Jira.
