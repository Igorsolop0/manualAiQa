# Learning Sync Model

Date: 2026-03-15
Scope: Nexus, Clawver, Cipher

This document defines how QA learnings should move through OpenClaw without creating memory noise.

The goal is:

- keep raw execution detail close to the run
- promote only durable truths into project knowledge
- update agent memory only when behavior should actually change

## 1. Learning Layers

### Layer 1: Run Learnings

Ticket- or run-specific learnings discovered during execution.

Examples:

- a page requires login before a key request appears
- a modal blocks the intended path
- a QA-only endpoint behaves differently than expected

These belong close to the run artifacts.

### Layer 2: Project Learnings

Reusable truths about the product, environment, or common flows.

Examples:

- social-linking checks should include profile state after linking or unlinking
- GetClientByToken behavior matters for linked registration source validation
- Smartico can alter expected modal behavior

These belong in project knowledge.

### Layer 3: Agent Learnings

Behavior rules that should improve a specific agent.

Examples:

- Nexus should split UI and API concerns more clearly
- Clawver should check reusable session paths before improvising login
- Cipher should validate GraphQL response bodies, not only HTTP status

These belong in agent memory.

## 2. Storage Destinations

### Run-Specific

- `workspace/shared/test-results/<ticket>/`
- `shared/runs/<run_id>/` when pilot is active
- `workspace/memory/insights/<ticket>-insights.md`

### Cross-Agent Daily Intake

- `workspace/shared/DAILY_INSIGHTS.md`

### Durable Project Knowledge

- `workspace/PROJECT_KNOWLEDGE.md`

### Durable Agent Behavior

- `workspace/MEMORY.md`
- `workspace-qa-agent/MEMORY.md`
- `workspace-api-docs/MEMORY.md`

## 3. Ownership Model

### Clawver and Cipher

They do not promote raw findings directly into durable memory.

They should:

1. create or update a ticket insight note
2. append a short learning candidate to `DAILY_INSIGHTS.md`
3. keep the learning grounded in actual evidence

### Nexus

Nexus is the curator.

Nexus should:

1. review candidate learnings
2. classify them as run-only, project, or agent-specific
3. update `PROJECT_KNOWLEDGE.md` or the correct `MEMORY.md` only when the learning is durable
4. avoid copying raw logs into durable files

## 4. Learning Candidate Format

Each learning candidate should answer:

- `Observed`: what actually happened
- `Impact`: why it matters
- `Applies to`: which flow, project, or agent it affects
- `Promote to`: `run-only`, `project`, `nexus-memory`, `clawver-memory`, or `cipher-memory`

Optional:

- `Evidence`: file path or artifact reference

## 5. Promotion Rules

Promote to project knowledge only if the learning is:

- reusable
- evidence-backed
- likely to matter again

Promote to agent memory only if the learning should change future agent behavior.

Keep as run-only if the finding is:

- one-off
- too specific to the ticket
- not yet verified as a recurring pattern

## 6. What Not To Sync

Do not promote:

- raw console dumps
- full request or response logs
- vague suspicions
- unverified hypotheses
- one-time noise without future value

## 7. Operational Flow

1. execution finishes
2. executor writes run artifacts
3. executor creates a short insight note
4. executor appends a short candidate to `DAILY_INSIGHTS.md`
5. Nexus reviews and curates
6. durable truths move to project knowledge or agent memory

## 8. Quality Bar

A good synced learning should:

- be short
- be true
- be reusable
- improve future planning or execution

If it does not clear that bar, keep it local to the run.
