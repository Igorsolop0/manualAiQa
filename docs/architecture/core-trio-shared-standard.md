# Core Trio Shared Standard

Date: 2026-03-15
Scope: Nexus, Clawver, Cipher

This document is the shared standard for the active OpenClaw core trio.

## 1. Core Roles

- `Nexus` = analyze, plan, route, review, summarize
- `Clawver` = UI execute, discover, verify, document
- `Cipher` = API execute, data prepare, backend validate

No agent should drift into another core role without explicit instruction.

## 2. File Meaning Standard

All three agents use the same meaning for the core files:

- `AGENTS.md` = startup order and session rules
- `SOUL.md` = role, boundaries, execution rules, stop rules
- `IDENTITY.md` = short mission and self-definition
- `USER.md` = what matters to Ihor
- `TOOLS.md` = local environment and execution notes only
- `MEMORY.md` = curated long-term operational memory
- `HEARTBEAT.md` = recurring checks only

Do not duplicate the same policy across all files.

## 3. Shared QA Cognition

All three agents also share the canonical QA operating framework:

- `/Users/ihorsolopii/.openclaw/docs/architecture/qa-operating-framework.md`
- `/Users/ihorsolopii/.openclaw/docs/architecture/qa-layered-test-design-profile.md`
- `/Users/ihorsolopii/.openclaw/docs/architecture/learning-sync-model.md`

This is the shared thinking model for:

- memory check before test design
- feature framing
- scope selection
- technique selection
- risk prioritization
- scenario generation
- evidence review
- learning extraction

## 4. Shared Communication Model

### Step 1: Intake

`Nexus` receives the request from Slack, Telegram, or internal context.

Nexus decides:

- answer directly
- route to `Clawver`
- route to `Cipher`
- split into UI + API work with explicit boundaries

### Step 2: Plan

Before execution, `Nexus` creates a narrow task scope:

- exact environment
- exact URL or endpoint family
- exact output folder
- auth expectation
- success check

If testing is required, Nexus asks for approval first.

### Step 3: Delegation

Nexus delegates by real execution, not simulated narration.

UI work:

- `openclaw agent --id qa-agent --message "..."`

API/data work:

- `openclaw agent --id api-docs-agent --message "..."`

### Step 4: Execution

`Clawver` or `Cipher` executes the assigned scope and writes evidence to:

- `workspace/shared/test-results/<ticket>/`

If Phase 2 pilot is active, the executor still writes legacy evidence first, then syncs to the run mirror.

### Step 5: Handoff Back

Executors return:

- real file paths
- actual status: `completed`, `partial`, `blocked`, or `failed`
- evidence-backed notes only

No agent may report success from plans, generated files, or assumptions alone.

### Step 6: Review

`Nexus` reviews the actual artifacts before summarizing.

If pilot is active, `pre-summary-gate` must pass before final summary.

## 5. Shared Evidence Standard

Evidence is the source of truth.

Minimum expectation:

- requested output folder exists
- primary result artifact exists
- screenshots, logs, or API results match the requested scope

If evidence is missing, status must not be reported as success.

## 6. Shared Status Language

Use these meanings consistently:

- `completed` = requested scope executed and evidence exists
- `partial` = some scope executed, but important part missing or blocked
- `blocked` = execution could not proceed because of a real blocker
- `failed` = execution attempted and failed in a way that invalidates the result

## 7. Shared Stop Rules

Any core agent must stop and escalate when:

1. environment or target is ambiguous
2. approval is required but not given
3. evidence path is missing or inconsistent
4. the task drifts beyond requested scope
5. a different core agent should own the task
6. success cannot be proven by artifacts

Escalation must include:

- what happened
- what was tried
- what evidence exists
- what next action is needed

## 8. Shared Pilot Rules

If Phase 2 pilot is active:

1. keep writing legacy evidence
2. sync legacy evidence to run mirror
3. emit result packet
4. use session references instead of raw token prose
5. gate final summary through `pre-summary-gate`

## 9. Tool Selection Standard

- `Stagehand` = discovery/path-finding for unstable or exploratory UI
- `Playwright` = deterministic verification and evidence capture
- local Python scripts = preferred execution path for API/data prep
- Swagger/OpenAPI = contract source of truth

If a task explicitly says `Stagehand REQUIRED`, the flow must stay Stagehand-first and narrow.

## 10. Heartbeat Standard

- `Nexus` may own recurring operational checks
- `Clawver` and `Cipher` should keep `HEARTBEAT.md` empty unless there is a specific recurring need
- do not duplicate Nexus heartbeat responsibilities in executor workspaces
