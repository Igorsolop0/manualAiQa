# OpenClaw Refactor Specification for Codex

**Document status:** Draft v1.0  
**Audience:** ChatGPT Codex + human owner  
**Date:** 2026-03-13  
**Owner:** Ihor  
**Primary goal:** turn OpenClaw from a promising multi-agent prototype into a reliable personal QA operating system that can remove ~60–70% of routine work on a secondary project while keeping human judgment in requirements analysis, risk review, and final product decisions.

## Progress snapshot (updated 2026-03-15)

Current implementation status against this spec:

- `Phase 0` — completed
- `Phase 1` — completed
- `Phase 2` — completed
- `Phase 3` — in progress, with strong structural baseline completed
- `Phase 4` — not started
- `Phase 5` — not started
- `Phase 6` — not started
- `Phase 7` — not started

What is already materially implemented:

- architecture baseline and migration notes under `docs/architecture/`
- canonical contracts under `contracts/`
- capability and maturity registries under `shared/registry/`
- run-centric pilot helper and dual-write scaffolding
- session registry and session-record usage in pilot flow
- core trio file-meaning standard and role cleanup
- canonical QA framework, Nexus planning format, learning sync model
- cleanup/archive pass and live agent reference map

What is still open at the time of this update:

- Phase 3 runtime hardening so real ticket runs follow the new model more consistently
- stronger enforcement for `Stagehand ONLY` / `Stagehand REQUIRED` execution behavior
- consistent learning emission on live runs
- naming/traceability cleanup in runtime artifacts

---

## 1. Executive summary

OpenClaw already has a strong core trio:

- **Nexus** — orchestrator, reviewer, routing brain
- **Clawver** — UI/manual/browser QA executor
- **Cipher** — API/backend/data-prep executor

The current system is valuable, but it is not yet autonomous enough because it has:

1. strong persona/mission files (`SOUL.md`) but weaker operational contracts,
2. shared folders but not a true run-centric state model,
3. real execution agents but an under-defined data/env plane,
4. several half-alive roles (Researcher, Jira Watcher, Vision Scout) that increase routing noise,
5. too much general handbook content and not enough project memory.

This refactor should **not** try to build a generic "AI QA company" immediately.
This refactor should build a **reliable personal QA operating system** first.

Target outcome:

- one ticket can move through **analyze -> plan -> prepare state -> execute -> review -> summarize**,
- every handoff is explicit and machine-readable,
- every run has its own ledger and evidence folder,
- the system becomes **behavior-aware**, not code-aware,
- the human stays in charge of ambiguity resolution and final judgment.

---

## 2. Context and hard constraints

### 2.1 Real working context

This system is being built for a **manual/middle QA workflow**, not for a code-owner workflow.

Available inputs:

- Jira ticket
- Design files
- Product/domain understanding
- Browser execution
- API access
- Existing internal docs and learned patterns

Unavailable or limited inputs:

- No reliable Git/code-diff context from the product under test
- No direct code-review-based change analysis as primary signal

### 2.2 Implication

OpenClaw must be designed as a **behavior-aware QA system**.
It should reason from:

- ticket intent,
- acceptance criteria,
- design,
- observed behavior,
- API contracts,
- prepared data/state,
- historical project learnings.

It should **not** assume code access, AST inspection, PR review, or commit-level impact analysis.

### 2.3 Product direction

Near-term goal:

- offload a large portion of routine QA work on one secondary project.

Long-term goal:

- evolve this into a reusable AI-manual-QA kernel that can later be adapted to multiple domains.

---

## 3. What must be preserved

The refactor must preserve the strongest parts of the current architecture:

1. **Nexus as the main hub**
2. **Clawver and Cipher as the core execution pair**
3. **Stagehand as a selective helper, not the primary test engine**
4. **Shared state as the source of truth**
5. **Research outside the ticket critical path**
6. **Cron-based intake for deterministic external polling**
7. **Evidence-first QA execution**

Do **not** replace the whole system with a brand-new architecture.
This refactor is a **controlled evolution**, not a rewrite.

---

## 4. Current architecture diagnosis

### 4.1 Strengths

- Nexus is already acting like a true control plane.
- Clawver has meaningful UI/browser policy and execution logic.
- Cipher is mature enough to own API and data-prep responsibilities.
- Shared folders already establish the idea of externalized state.
- Stagehand is already treated as helper-level, which is correct.
- Research is conceptually outside the critical path, which is good.

### 4.2 Weaknesses

- No canonical source of truth for contracts and handoffs.
- Memory files are inconsistent in meaning across agents.
- Template files still exist in weak agents and create noise.
- Jira Watcher has contradictory operating rules.
- Vision Scout conflicts with current Nexus behavior and appears deprecated.
- Research Agent exists in routing more than in reality.
- The system lacks a first-class **data/env plane**.
- FE↔BE session exchange still relies on raw token-file patterns.

### 4.3 Main architectural conclusion

The biggest bottleneck is **not intelligence**.
The biggest bottleneck is **standardized work**:

- contracts,
- run state,
- session registry,
- project memory,
- data/env discipline,
- maturity gating.

---

## 5. Refactor goals

### 5.1 Primary goals

1. Make the system more autonomous on one secondary project.
2. Reduce routing ambiguity and agent sprawl.
3. Introduce explicit, validated handoff contracts.
4. Make runs traceable end-to-end.
5. Give Nexus an analysis/planning mode for shift-left use.
6. Formalize data/env work as a first-class capability.
7. Create measurable autonomy metrics.

### 5.2 Non-goals

This refactor does **not** aim to:

- replace human QA judgment,
- fully automate requirements quality,
- support every domain equally,
- invent a production SaaS platform yet,
- build a general-purpose code-review agent,
- make every agent fully autonomous from day one.

---

## 6. Target operating model

### 6.1 Core model

OpenClaw should operate as:

- **Control plane:** Nexus
- **Execution plane:** Clawver + Cipher
- **Data/env plane:** first as a capability inside Cipher, later optionally standalone
- **Knowledge plane:** curated project knowledge and reusable facts
- **Ops plane:** watchers, heartbeat, cron jobs, evals, metrics

### 6.2 Canonical workflow

Every ticket run should follow this state machine:

```text
INTAKE
  -> ANALYZE
  -> PLAN
  -> PREPARE_STATE
  -> EXECUTE_API and/or EXECUTE_UI
  -> REVIEW_EVIDENCE
  -> SUMMARIZE
  -> PROMOTE_LEARNINGS
  -> CLOSED
```

If ambiguity or instability is detected, the system must branch to:

```text
BLOCKED_AMBIGUITY
BLOCKED_ENV
BLOCKED_AUTH
BLOCKED_ORACLE
NEEDS_HUMAN_REVIEW
```

### 6.3 Human role

Human remains responsible for:

- requirements judgment,
- ambiguity resolution,
- risk prioritization,
- final bug/not-bug decision,
- final team communication.

Agents should take over:

- first-pass analysis,
- routine plan drafting,
- data preparation,
- repeatable execution,
- evidence collection,
- draft reporting,
- learning distillation.

---

## 7. Agent model after refactor

## 7.1 Core trio

### Nexus

**Role:** orchestrator, analyzer, planner, reviewer, promoter of learnings.  
**Must own:**

- task intake,
- scope split (UI/API/mixed),
- task charter creation,
- routing,
- result review,
- final summary,
- promotion of learnings into curated knowledge,
- stop-the-line decisions.

**Must not own:**

- heavy browser execution,
- heavy API execution,
- external research in the critical path,
- raw session secrets beyond references.

### Clawver

**Role:** UI/manual/browser executor.  
**Must own:**

- browser navigation,
- UI evidence,
- deterministic Playwright execution,
- selective Stagehand usage for discovery,
- UI result packet creation,
- session artifact creation when UI login is needed.

**Must not own:**

- API decision logic,
- bonus/data/business seed logic,
- product-level final conclusions.

### Cipher

**Role:** API/backend/data-prep executor.  
**Must own:**

- API checks,
- payload validation,
- token/API auth flows,
- data preparation,
- player/balance/bonus/flag operations,
- cleanup/reset recipes,
- API result packet creation.

**Must not own:**

- UI evidence collection,
- final review,
- generic project orchestration.

## 7.2 Supporting capabilities

### Data/Env capability (phase 1 inside Cipher)

This is a first-class capability even if it is not a separate agent yet.

Must support:

- player/account creation,
- balance top-up,
- bonus activation/assignment,
- feature flag setup,
- reusable fixture recipes,
- environment cleanup/reset,
- auth/session preparation,
- mock/stub lanes for external identity providers.

### Requirements Analysis mode (inside Nexus)

Must produce:

- ambiguity list,
- assumptions list,
- scenario matrix,
- risks,
- expected test levels,
- open questions for refinement,
- required data/env setup.

## 7.3 Non-core components

### Jira Watcher -> Scope Watcher

This should be refactored from an agent persona into a deterministic service/job.

Purpose:

- watch Jira ticket changes,
- compare snapshots,
- emit scope deltas,
- alert Nexus when test-relevant context changes.

### Researcher

Keep only as an async digest service.

Rules:

- never block ticket execution,
- never sit in the mandatory routing path,
- only publish short actionable updates,
- optionally repurpose into regression historian / bug-pattern analyst later.

### Vision Scout

Not part of the core refactor path.

Decision:

- either archive it,
- or repurpose it later for batch visual acceptance / screenshot review.

It must not remain as a half-deprecated routed capability.

---

## 8. Canonical contracts

Create a single source of truth under:

```text
/contracts/
```

Required contracts:

```text
contracts/
  task-charter.schema.json
  handoff-packet.schema.json
  result-packet.schema.json
  session-record.schema.json
  knowledge-card.schema.json
  ticket-delta.schema.json
  ambiguity-report.schema.json
  metrics-event.schema.json
```

### 8.1 Task Charter

Created by Nexus.

Purpose:

- define what is being tested,
- define scope,
- define expected outcomes,
- define next owner.

Example shape:

```json
{
  "task_id": "CT-123",
  "run_id": "CT-123-20260313-01",
  "project": "minebit",
  "title": "Deposit streak bonus appears on second qualifying deposit",
  "goal": "Validate streak eligibility and UI visibility after two qualifying deposits",
  "source": {
    "jira_key": "CT-123",
    "design_refs": [],
    "ticket_snapshot_ref": "shared/runs/CT-123-20260313-01/intake/jira_snapshot.json"
  },
  "scope": {
    "ui": true,
    "api": true,
    "research": false
  },
  "preconditions": [
    "campaign is active",
    "test player exists or can be created"
  ],
  "data_needs": [
    "player",
    "wallet",
    "bonus eligibility state"
  ],
  "assertions": [
    "first qualifying deposit is accepted",
    "second qualifying deposit increments streak",
    "bonus is visible in UI"
  ],
  "success_criteria": [
    "review-ready evidence exists for UI and API"
  ],
  "status": "planned",
  "owner": "nexus",
  "next_owner": "cipher"
}
```

### 8.2 Handoff Packet

Used for agent-to-agent transfer.

Purpose:

- pass state without prose-only coordination,
- reference sessions and entity IDs,
- declare expected next step.

Example shape:

```json
{
  "run_id": "CT-123-20260313-01",
  "from": "cipher",
  "to": "clawver",
  "state_refs": [
    "shared/runs/CT-123-20260313-01/plan/task-charter.json"
  ],
  "session_refs": [
    "shared/sessions/sess-player-ct123.json"
  ],
  "entity_ids": {
    "player_id": "p_123",
    "wallet_id": "w_456",
    "bonus_id": "b_789"
  },
  "pending_assertions": [
    "bonus visible in promotions UI",
    "wallet history reflects second deposit"
  ],
  "expected_next_step": "Open player session and verify UI evidence",
  "recommended_owner": "clawver"
}
```

### 8.3 Result Packet

Produced by any executor.

Purpose:

- standardize what a completed step means,
- simplify Nexus review,
- enable metrics and evals.

Example shape:

```json
{
  "run_id": "CT-123-20260313-01",
  "agent": "clawver",
  "status": "completed",
  "assertions_passed": [
    "bonus banner visible"
  ],
  "assertions_failed": [],
  "blockers": [],
  "evidence_refs": [
    "shared/runs/CT-123-20260313-01/evidence/ui/bonus-banner.png",
    "shared/runs/CT-123-20260313-01/evidence/ui/trace.zip"
  ],
  "notes": [
    "banner was visible after page refresh"
  ],
  "confidence": "medium",
  "recommended_next_owner": "nexus"
}
```

### 8.4 Session Record

Must replace ad-hoc raw token handoffs.

Example shape:

```json
{
  "session_id": "sess-player-ct123",
  "project": "minebit",
  "subject_type": "player",
  "owner": "clawver",
  "storage_state_ref": "shared/runs/CT-123-20260313-01/sessions/player-auth.json",
  "token_ref": "vault://sessions/sess-player-ct123",
  "created_at": "2026-03-13T10:00:00Z",
  "expires_at": "2026-03-13T11:00:00Z",
  "refresh_strategy": "ui_login",
  "status": "active"
}
```

### 8.5 Knowledge Card

For curated project truth, not raw notes.

Example shape:

```json
{
  "project": "minebit",
  "fact_type": "auth-entrypoint",
  "title": "Player login entrypoint for promotions flow",
  "fact": "Promotions UI is reachable only after wallet bootstrap completes.",
  "source_run": "CT-123-20260313-01",
  "confidence": "high",
  "last_verified": "2026-03-13",
  "ttl_days": 30,
  "invalidates_when": [
    "auth flow changes",
    "wallet bootstrap redesign"
  ]
}
```

---

## 9. File and folder structure

## 9.1 High-level target structure

```text
/agents/
  /nexus/
  /clawver/
  /cipher/
  /researcher/
  /scope-watcher/

/contracts/

/shared/
  /runs/
  /sessions/
  /knowledge/
  /registry/
  /evals/

/docs/
  /architecture/
  /runbooks/
  /specs/
```

## 9.2 Run-centric storage model

Introduce a canonical run folder:

```text
shared/runs/<run_id>/
  intake/
    jira_snapshot.json
    design_refs.md
  plan/
    task-charter.json
    ambiguity-report.json
    risk-notes.md
  handoffs/
    nexus-to-cipher.json
    cipher-to-clawver.json
  sessions/
    player-auth.json
  evidence/
    api/
    ui/
  results/
    cipher-result.json
    clawver-result.json
    nexus-summary.md
  learning/
    candidate-knowledge.json
```

Rule:

- every active ticket run must have its own folder,
- new evidence must land in the run folder,
- only promoted/distilled learnings should leave the run folder and enter curated knowledge.

## 9.3 Session registry

Introduce:

```text
shared/sessions/
  registry.json
  sess-player-ct123.json
```

Rule:

- agents exchange session **references**, not raw secrets in prose.

## 9.4 Backward compatibility

During migration, legacy paths such as:

- `shared/tasks/`
- `shared/credentials/`
- `shared/test-results/`

may continue to exist temporarily.

But Codex must add a migration layer or compatibility note and gradually shift all active flows toward the new run-centric structure.

---

## 10. Standard meaning of agent files

Do not allow each agent to interpret file names differently.

Keep the existing file names for now to reduce churn, but standardize their meaning.

### `AGENTS.md`

Bootstrap manifest:

- role summary,
- inputs,
- outputs,
- routes,
- can/cannot do,
- startup checklist.

### `SOUL.md`

Decision policy and operating model:

- how the agent thinks,
- routing or execution rules,
- escalation/stop rules,
- evidence philosophy.

### `MEMORY.md`

Only curated operational/project memory.

Allowed content:

- project truths,
- reusable recipes,
- known flaky areas,
- known good entrypoints,
- known bugs,
- locators/endpoints/patterns,
- last verified facts.

Not allowed:

- generic QA theory,
- motivational text,
- broad personal notes unrelated to the role,
- duplicated tool docs.

### `TOOLS.md`

Operational cheat sheet only:

- tool names,
- commands,
- ports,
- environments,
- safe usage rules,
- exact invocation patterns.

### `USER.md`

Stable human-specific preferences and interaction style only.

### `IDENTITY.md`

Role boundaries and self-definition only.

### `HEARTBEAT.md`

Only for components that really have scheduled/light check behavior.

If an agent does not have heartbeat-like behavior, this file should be minimal or absent.

---

## 11. Memory redesign requirements

## 11.1 Nexus memory

Must become:

- project glossary,
- routing patterns,
- risk taxonomy,
- ambiguity patterns,
- review checklist,
- escalation rules,
- summary/report templates.

## 11.2 Clawver memory

Must become:

- auth entrypoints,
- stable locators,
- flaky zones,
- modal/iframe quirks,
- reusable browser fixtures,
- known UI regressions,
- project-specific execution hints.

## 11.3 Cipher memory

Must become:

- endpoint families,
- auth handshake recipes,
- player/wallet/bonus/flag recipes,
- fixture templates,
- known contract drift,
- reset/cleanup routines,
- service boundaries.

## 11.4 Required cleanup rule

Any file that is mostly template or generic theory must be either:

- rewritten into real operational knowledge,
- reduced to minimal scope,
- or archived.

---

## 12. Capability registry and maturity model

Introduce:

```text
shared/registry/capabilities.yaml
shared/registry/maturity.yaml
```

Example capability registry:

```yaml
capabilities:
  ticket.analyze:
    owner: nexus
    maturity: beta
  ticket.plan:
    owner: nexus
    maturity: beta
  ui.execute:
    owner: clawver
    maturity: stable
  ui.discover_path:
    owner: stagehand-helper
    maturity: stable
  api.execute:
    owner: cipher
    maturity: stable
  data.prepare:
    owner: cipher
    maturity: beta
  jira.delta.poll:
    owner: scope-watcher
    maturity: alpha
  research.digest:
    owner: researcher
    maturity: alpha
  visual.batch_review:
    owner: vision-scout
    maturity: deprecated
```

Routing rule:

- Nexus routes by **capability**, not by hard-coded agent name whenever possible.

Maturity levels:

- `stable`
- `beta`
- `alpha`
- `deprecated`
- `disabled`

Rule:

- Nexus must not route critical ticket work to `deprecated` or `disabled` capabilities.

---

## 13. Stop-the-line policy

A more autonomous agent system must also know when to stop.

Introduce a standard stop taxonomy:

```text
AMBIGUOUS_REQUIREMENT
MISSING_ORACLE
ENVIRONMENT_DRIFT
AUTH_FLOW_CHANGED
SESSION_EXPIRED
FLAKY_UI_PATH
MISSING_TEST_DATA
CONTRACT_DRIFT
HUMAN_DECISION_REQUIRED
```

Rules:

- every blocker must be explicit,
- every blocked run must still produce a partial result packet,
- Nexus must summarize the blocker in review-ready form,
- no agent should silently improvise through critical uncertainty.

---

## 14. Phased implementation plan for Codex

## Phase 0 — Freeze and inventory

**Status (2026-03-15):** completed

### Goal
Create a safe baseline before structural changes.

### Tasks

1. Add this spec into the repository under `docs/specs/`.
2. Create `docs/architecture/current-state.md` summarizing the existing system.
3. Create `shared/registry/maturity.yaml` and mark current capabilities.
4. Mark Vision Scout as `deprecated` unless actively repurposed immediately.
5. Mark Researcher as `alpha` and remove it from mandatory ticket routing.

### Definition of done

- a new contributor can see what is core, what is experimental, and what is deprecated.

### Implemented

- spec copied into `docs/specs/`
- `docs/architecture/current-state.md` created
- `shared/registry/maturity.yaml` created
- Vision Scout marked as deprecated in maturity/governance
- Researcher marked as alpha/advisory and removed from mandatory ticket-critical path in docs/routing

---

## Phase 1 — Contracts and registry

**Status (2026-03-15):** completed

### Goal
Introduce the canonical contracts and capability registry.

### Tasks

1. Create `/contracts/` with JSON schemas.
2. Create `shared/registry/capabilities.yaml`.
3. Update Nexus docs to emit/consume these contracts.
4. Add lightweight validation helpers or scripts if the repo supports it.
5. Add examples for one mixed ticket.

### Definition of done

- one dry-run ticket can produce task charter, handoff packet, and result packet with valid structure.

### Implemented

- canonical schemas created under `contracts/`
- example JSON artifacts created under `contracts/examples/`
- `shared/registry/capabilities.yaml` created
- Nexus docs updated to route by capability + maturity
- lightweight validation support added through pilot helper / `ajv-cli`

---

## Phase 2 — Run ledger and session registry

**Status (2026-03-15):** completed

### Goal
Replace folder-level ambiguity with run-level traceability.

### Tasks

1. Introduce `shared/runs/<run_id>/` structure.
2. Introduce `shared/sessions/registry.json`.
3. Replace raw FE↔BE token file handoff with session records.
4. Update Clawver and Cipher docs to write outputs into run folders.
5. Keep migration notes for old folders.

### Definition of done

- a mixed UI+API test leaves all major artifacts inside one run folder,
- session exchange happens via session references.

### Implemented

- `shared/runs/<run_id>/` pilot scaffolding added
- `shared/sessions/registry.json` added
- `session-record` flow added via `run_manager.py register-session`
- `result-packet` flow added via `run_manager.py emit-result`
- dual-write migration path documented and working for pilot tickets
- `bootstrap-dispatch` and `pre-summary-gate` added

### Note

Phase 2 is considered complete as infrastructure and operating path.
Real ticket runs still need stronger default adoption, which is being handled as Phase 3 runtime hardening rather than Phase 2 redesign.

---

## Phase 3 — Core trio cleanup

**Status (2026-03-15):** in progress

### Goal
Make Nexus, Clawver, and Cipher consistent and production-lean.

### Tasks

1. Standardize meaning of `AGENTS.md`, `SOUL.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, `IDENTITY.md`, `HEARTBEAT.md`.
2. Remove duplicated policy text when a single shared policy is enough.
3. Rewrite `MEMORY.md` files from theory into project memory.
4. Add explicit input/output contracts to each core agent.
5. Add stop rules to each core agent.

### Definition of done

- the core trio is internally consistent,
- template noise is removed,
- each core agent has clear input/output boundaries.

### Implemented so far

- standardized meanings of `AGENTS.md`, `SOUL.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, `IDENTITY.md`, `HEARTBEAT.md`
- cleaned Nexus, Clawver, and Cipher docs
- reduced Nexus `MEMORY.md` into operational memory
- added shared standards:
  - `docs/architecture/core-trio-shared-standard.md`
  - `docs/architecture/qa-operating-framework.md`
  - `docs/architecture/nexus-planning-format.md`
  - `docs/architecture/learning-sync-model.md`
- added cleanup/reference docs:
  - `docs/architecture/safe-cleanup-plan-2026-03-15.md`
  - `docs/architecture/agent-reference-map.md`
  - `docs/architecture/refactor-compliance-checklist.md`

### Still open

- runtime hardening so live runs consistently follow pilot + tooling policy
- stronger enforcement for Stagehand-only behavior
- consistent learning sync on real runs
- final decision on what else to promote from `workspace/QA_TEST_DESIGN_APPROACH.md`

---

## Phase 4 — Data/Env capability inside Cipher

### Goal
Make test-state preparation a first-class, reusable capability.

### Tasks

1. Add a dedicated Data/Env section or submodule under Cipher docs/code.
2. Define recipes for:
   - player creation,
   - balance top-up,
   - bonus assignment,
   - feature flags,
   - cleanup/reset,
   - social-auth test setup.
3. Split `api.execute` from `data.prepare` conceptually, even if both belong to Cipher for now.
4. Define what parts can use real providers and what parts must use stubs/mocks.

### Definition of done

- deposit-streak-like scenarios can be prepared in a repeatable way,
- data preparation is no longer hidden inside generic API testing behavior.

---

## Phase 5 — Nexus Analyze mode

### Goal
Add a true shift-left analysis capability.

### Tasks

1. Add `ticket.analyze` mode to Nexus.
2. Define `ambiguity-report.schema.json`.
3. Make analysis output include:
   - ambiguities,
   - assumptions,
   - scenario matrix,
   - suggested test levels,
   - data/env needs,
   - open questions.
4. Add one example based on a realistic ticket.

### Definition of done

- Nexus can generate a reviewable first-pass QA analysis from Jira + design context.

---

## Phase 6 — Scope Watcher and async support cleanup

### Goal
Reduce routing entropy and conflicting instructions.

### Tasks

1. Refactor Jira Watcher into `scope-watcher` service/job.
2. Remove persona/template clutter from watcher.
3. Make the watcher emit `ticket-delta` outputs instead of vague snapshots.
4. Keep Researcher as async digest only.
5. Archive or repurpose Vision Scout decisively.

### Definition of done

- ticket-critical routing uses only reliable, intentionally supported capabilities.

---

## Phase 7 — Metrics and evals

### Goal
Measure whether autonomy is actually improving.

### Tasks

1. Add `metrics-event.schema.json`.
2. Store per-run metrics.
3. Track baseline and trend for:
   - autonomy rate,
   - false positive rate,
   - time to first evidence,
   - blocked by ambiguity,
   - blocked by data/env,
   - blocked by auth,
   - review effort,
   - time saved.
4. Add a simple markdown or JSON summary format.

### Definition of done

- there is a measurable way to tell whether the system is saving real QA time.

---

## 15. Acceptance criteria for the whole refactor

The refactor is successful when all of the following are true:

1. Nexus, Clawver, and Cipher form a consistent core trio.
2. Researcher is not in the mandatory ticket critical path.
3. Vision Scout is either archived or explicitly repurposed.
4. Jira Watcher becomes a clean deterministic watcher/service.
5. Every active run has a run folder.
6. Handoffs use explicit packets.
7. Session sharing uses references, not raw secret files in ad-hoc locations.
8. Core `MEMORY.md` files contain real project memory, not general QA filler.
9. Nexus can produce an analyze/plan output from Jira+design context.
10. One mixed UI+API ticket can go end-to-end with review-ready evidence.

---

## 16. Suggested first real scenario for validation

Use one mixed scenario as the validation scenario for the refactor.

Recommended scenario:

**Deposit streak / qualifying bonus flow**

Validation path:

1. Nexus analyzes the ticket.
2. Cipher prepares the test player and bonus state.
3. Cipher executes API-level validation of deposit eligibility.
4. Clawver uses a session reference to verify UI visibility and wallet history.
5. Nexus reviews both result packets and writes the final summary.
6. Useful learnings are promoted to curated knowledge.

This scenario is strong because it crosses:

- business rules,
- data/env setup,
- API validation,
- UI validation,
- handoff quality,
- evidence quality.

---

## 17. Codex implementation rules

Codex must follow these rules while implementing this spec.

1. **Work phase-by-phase.** Do not attempt a repo-wide rewrite in one pass.
2. **Prefer additive changes before destructive changes.**
3. **Preserve existing working behavior whenever possible.**
4. **Do not route critical ticket work through alpha/deprecated capabilities.**
5. **If a file is mostly template, rewrite or archive it rather than expanding the template.**
6. **When changing contracts, update examples and agent docs in the same task.**
7. **When touching an agent, keep its role narrow and explicit.**
8. **When uncertain, introduce a compatibility shim and document migration.**
9. **Every implementation task must end with a short report:**
   - what changed,
   - what was not changed,
   - risks,
   - suggested next step.
10. **Never replace evidence with prose.** Evidence artifacts remain the source of truth.

---

## 18. Suggested Codex task backlog

These tasks should be executed as separate Codex threads/tasks whenever possible.

### Task 1
Create `/contracts/` and draft all schema files plus examples.

### Task 2
Create `shared/registry/capabilities.yaml` and `shared/registry/maturity.yaml`, then align Nexus routing docs.

### Task 3
Introduce `shared/runs/<run_id>/` and migrate one example flow to the run-centric model.

### Task 4
Introduce `shared/sessions/registry.json` and replace the token-file handoff pattern with session records.

### Task 5
Refactor the core trio docs so each file has a single standard meaning.

### Task 6
Rewrite `MEMORY.md` for Nexus, Clawver, and Cipher into real project memory.

### Task 7
Split Cipher docs into `api.execute` and `data.prepare` responsibilities.

### Task 8
Add Nexus Analyze mode and ambiguity report output.

### Task 9
Refactor Jira Watcher into Scope Watcher and remove contradictions.

### Task 10
Archive or repurpose Vision Scout and remove dead routing references.

### Task 11
Add minimal metrics/evals support for autonomy tracking.

---

## 19. Definition of success in human terms

The system is successful if it behaves like this:

- human receives a ticket,
- Nexus produces a useful first-pass QA view,
- Cipher prepares state without constant manual babysitting,
- Clawver executes the repeatable browser work,
- Nexus returns a review-ready summary with evidence,
- human spends time on judgment, not setup and repetition.

This refactor is not about making the system look more agentic.
It is about making it **more reliable, more legible, and more useful**.

---

## 20. Appendix A — Copy/paste kickoff prompt for Codex

```text
You are refactoring the OpenClaw multi-agent QA system.

Read and follow docs/specs/openclaw_codex_refactor_spec.md as the source of truth.

Your task now is ONLY: <INSERT SINGLE PHASE OR SINGLE TASK HERE>.

Constraints:
- preserve current working behavior,
- prefer additive changes over rewrites,
- do not expand deprecated agents,
- keep Nexus + Clawver + Cipher as the core trio,
- treat Data/Env as a first-class capability under Cipher,
- move the system toward run-centric state and explicit contracts,
- do not keep template-only files alive,
- update any related docs/examples when you change a contract.

Expected output:
1. concise implementation plan,
2. files to change,
3. actual changes,
4. migration notes if needed,
5. risks and follow-ups.
```

---

## 21. Appendix B — Recommended first Codex prompt

```text
Implement Phase 1 from docs/specs/openclaw_codex_refactor_spec.md.

Specifically:
- create /contracts/ with the schema files named in the spec,
- add example JSON files for task charter, handoff packet, result packet, session record, and knowledge card,
- create shared/registry/capabilities.yaml and shared/registry/maturity.yaml,
- update Nexus docs so routing references capabilities and maturity instead of assuming every listed agent is production-ready,
- keep changes minimal and additive,
- provide a short report of changed files, open questions, and suggested next task.
```

---

## 22. Appendix C — Recommended first evaluation questions

After each phase, the human reviewer should ask:

1. Did this phase reduce ambiguity or just add files?
2. Did it remove a real bottleneck for autonomy?
3. Is the new structure easier for Codex to work with?
4. Does the system become more deterministic where it should?
5. Did we preserve the strong parts of Nexus/Clawver/Cipher?
6. Can one real ticket be handled with less manual coordination than before?

---

**End of spec**
