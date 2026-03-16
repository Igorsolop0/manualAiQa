# OpenClaw Spec Delta vNext

Date: 2026-03-16
Status: Proposed additive delta to `/Users/ihorsolopii/.openclaw/docs/specs/openclaw_codex_refactor_spec.md`
Owner: Ihor + Codex

## 1. Purpose

This document does not replace the base spec.
It narrows and clarifies the target architecture so OpenClaw evolves as a reliable personal QA operating system, not as a custom observability or evaluation platform.

The main correction is:

- keep OpenClaw as the QA control plane and run-time source of truth
- introduce vendor-neutral integration adapters for telemetry, evaluation, experiments, and annotation
- use Phoenix or Langfuse as external observability and evaluation backends
- avoid building a custom tracing UI, experiment dashboard, or eval platform inside OpenClaw

## 2. Core architectural decision

### Keep inside OpenClaw

The following remain first-class internal responsibilities:

- Nexus routing and orchestration
- Clawver execution for UI/manual/browser QA
- Cipher execution for API/backend/data-prep QA
- canonical contracts under `/contracts/`
- run ledger under `shared/runs/`
- session registry and `session-record` flow
- evidence storage and evidence references
- stop-the-line rules and runtime policy enforcement
- learning sync, knowledge promotion, and project memory
- failure taxonomy for QA-specific outcomes

### Move outside OpenClaw via adapters

The following should not become large internal product areas:

- trace storage and trace visualization UI
- experiment comparison UI
- evaluator execution UI
- dashboards and alerts for run quality trends
- annotation workflow UI
- drift and regression monitoring dashboards

OpenClaw may emit data for these concerns, but should not become the primary platform for viewing or managing them.

## 3. vNext target operating model

The target operating model from the base spec remains valid, but the ops plane is refined.

Replace the broad idea of:

- watchers, heartbeat, cron jobs, evals, metrics

with this more precise model:

- watchers and heartbeat stay internal operational mechanisms
- metrics and eval signals are defined internally as contracts
- telemetry, trace visualization, evaluator execution, and experiment analysis are delegated to external backends through adapters

### Updated target model

- **Control plane:** Nexus
- **Execution plane:** Clawver + Cipher
- **Data/env plane:** capability inside Cipher, later optionally standalone
- **Knowledge plane:** curated project knowledge and reusable facts
- **Integration plane:** telemetry adapter, evaluation adapter, experiment adapter, annotation adapter
- **External observability plane:** Phoenix and/or Langfuse

## 4. Source-of-truth rule

OpenClaw must preserve a strict source-of-truth rule:

- primary run state lives in `shared/runs/`
- primary contracts live in `/contracts/`
- primary session references live in `shared/sessions/`
- primary ticket/task/result artifacts remain stored inside OpenClaw
- external platforms receive mirrored or exported telemetry, not exclusive ownership of runtime state

This prevents vendor lock-in and keeps OpenClaw operable even if the external telemetry backend is unavailable.

## 5. New internal interfaces

The base spec already defines contracts for handoffs and results.
This delta adds integration contracts and adapter boundaries.

### 5.1 Telemetry adapter

Purpose:

- export run and span-level execution events from OpenClaw to an external backend
- preserve artifact references and runtime outcomes without exporting secrets

Required interface shape:

```text
telemetry.emit_run_started(run_event)
telemetry.emit_run_finished(run_event)
telemetry.emit_span(span_event)
telemetry.emit_tool_call(tool_event)
telemetry.emit_artifact_ref(artifact_event)
telemetry.emit_failure(failure_event)
```

### 5.2 Evaluation adapter

Purpose:

- run external evaluations on existing OpenClaw artifacts and traces
- compare output quality without making external tooling the runtime authority

Required interface shape:

```text
eval.register_dataset(dataset)
eval.run_evaluation(eval_request)
eval.record_score(eval_score)
```

### 5.3 Experiment adapter

Purpose:

- compare prompt/policy/runtime variants using real historical runs or curated datasets

Required interface shape:

```text
experiment.create(input)
experiment.compare(compare_request)
experiment.record_outcome(result)
```

### 5.4 Annotation adapter

Purpose:

- send candidate items for human review or labeling
- pull review outcomes back into OpenClaw knowledge and evaluation loops

Required interface shape:

```text
annotation.create_review_item(item)
annotation.sync_review_outcome(outcome)
```

## 6. New contract set for vNext

The current contract family remains valid.
Add the following optional-but-recommended contracts when Phase 7 work begins:

```text
contracts/
  telemetry-span.schema.json
  failure-event.schema.json
  eval-request.schema.json
  eval-score.schema.json
  experiment-record.schema.json
```

These are not replacements for `result-packet`.
They are secondary integration contracts that sit on top of the existing run/result model.

## 7. Failure taxonomy must remain internal

External backends can store or display failures, but OpenClaw should define the failure language.

Recommended starting taxonomy:

- `blocked_auth`
- `blocked_env`
- `blocked_external_provider`
- `blocked_oracle`
- `ambiguous_requirement`
- `runtime_policy_violation`
- `weak_evidence`
- `session_handoff_failed`
- `agent_timeout`
- `stagehand_discovery_failed`

This taxonomy should be shared by Nexus, Clawver, Cipher, and any external evaluation backend.

## 8. Security and redaction rule

Telemetry export must never treat raw prompts, session secrets, cookies, storage state, or PII as safe by default.

Required rules:

- export references rather than raw secret payloads
- redact or hash sensitive fields before export
- keep browser storage state and auth materials inside OpenClaw-controlled storage
- allow external telemetry to reference artifacts by path or opaque ID only

If a backend requires raw payloads for debugging, that must be an explicit opt-in mode, not the default.

## 9. Evaluation philosophy for OpenClaw

Evaluation should not replace deterministic QA assertions.

Use this order:

1. deterministic checks and contract validation
2. evidence completeness checks
3. policy compliance checks
4. rubric-based review
5. LLM-as-judge only where deterministic checks are insufficient

The system should never depend on a judge-style LLM score to decide whether a run "really happened."
That remains the role of evidence, contracts, and execution artifacts.

## 10. Preferred backend strategy

OpenClaw should stay vendor-neutral.
However, the recommended rollout order is:

### Primary recommendation

- first pilot backend: Phoenix

Reason:

- strong fit for tracing + evals + experiments
- aligns well with open and OTEL-friendly architecture
- lower conceptual overlap with OpenClaw as a control plane

### Secondary recommendation

- second backend option: Langfuse

Reason:

- strong product UX for traces, evals, and engineering workflows
- useful if prompt/version/metrics workflows become more important later

### Explicit non-goal

Do not integrate multiple external backends in the first pilot.
One backend is enough for the first telemetry/eval loop.

## 11. Spec patch map

This section describes how the base spec should be updated.

### 11.1 Section 5.1 Primary goals

Keep goal 7, but narrow its implementation meaning.

Current wording:

- Create measurable autonomy metrics.

Replacement intent:

- Create measurable autonomy metrics through vendor-neutral contracts and external telemetry/evaluation adapters.

### 11.2 Section 6.1 Core model

Current wording includes:

- Ops plane: watchers, heartbeat, cron jobs, evals, metrics

Replacement wording:

- Ops plane: watchers, heartbeat, cron jobs, runtime health
- Integration plane: telemetry adapter, evaluation adapter, experiment adapter, annotation adapter
- External observability plane: Phoenix and/or Langfuse

### 11.3 Section 8 Canonical contracts

Keep the existing contracts.
Change the interpretation of `metrics-event.schema.json`.

Updated meaning:

- `metrics-event.schema.json` is a lightweight internal event contract
- it is not the foundation of a large in-house analytics product
- future integration contracts may be added for spans, eval requests, scores, and experiments

### 11.4 Phase 7 — Metrics and evals

Replace the phase title and scope.

Current title:

- Phase 7 - Metrics and evals

New title:

- Phase 7 - Telemetry and external evaluation integration

New goal:

- make autonomy and execution quality measurable without building a custom observability platform

Replace tasks with:

1. define internal telemetry and failure contracts
2. emit run-level and span-level telemetry from Nexus, Clawver, and Cipher
3. mirror key runtime events to one external backend
4. create a small golden dataset of representative runs
5. add a minimal first evaluator set
6. compare at least one policy or prompt variant using real runs
7. keep dashboards and trace UI out of OpenClaw itself

Replace definition of done with:

- there is a measurable way to tell whether the system is saving QA time
- at least one external backend receives run telemetry successfully
- at least one dataset-backed evaluator loop exists
- OpenClaw remains the source of truth for runtime state and artifacts

### 11.5 Appendix C — Recommended first evaluation questions

Keep the appendix, but add these two questions:

7. Did we add signal, or just another dashboard?
8. Are we exporting telemetry cleanly without leaking secrets or surrendering source-of-truth ownership?

## 12. Updated phased implementation sequence

This delta does not invalidate Phases 0-3.
They remain correct and useful.

Recommended next sequence:

### Phase 3 finish

- complete runtime hardening and learning consistency
- stabilize artifact naming, run flow, and policy enforcement

### Phase 4

- formalize Data/Env capability under Cipher
- keep this internal to OpenClaw

### Phase 5

- strengthen Nexus Analyze mode
- improve ticket-to-plan quality and context retrieval discipline

### Phase 6

- refine project knowledge promotion and human review loops
- keep these internal to OpenClaw

### Phase 7 vNext

- add telemetry/failure/eval contracts
- implement Phoenix adapter first
- emit spans and run summaries for one pilot flow
- create the first golden dataset from real OpenClaw runs
- add minimal evaluators for plan quality, evidence completeness, and policy compliance

### Phase 8 optional

- add Langfuse adapter if there is a clear benefit beyond Phoenix
- only after one backend pilot proves useful

## 13. First implementation slice after adopting this delta

The recommended first concrete implementation after approving this delta is:

1. add `docs/architecture/openclaw-core-vs-observability.md`
2. add telemetry and failure contracts
3. implement `adapters/telemetry/base`
4. implement `adapters/telemetry/phoenix`
5. emit telemetry for:
   - Nexus planning run
   - Clawver execution run
   - Cipher execution run
6. keep export payloads minimal and redacted
7. validate one real ticket flow end-to-end

## 14. Human review questions for this delta

Before implementation, confirm the following:

1. Are we keeping OpenClaw as a control plane rather than expanding it into a platform product?
2. Are we comfortable choosing one backend first instead of integrating multiple tools immediately?
3. Do we agree that contracts, run ledger, and evidence remain primary over dashboards?
4. Do we agree that LLM-based judging stays secondary to deterministic evidence and policy checks?

If the answer is yes, this delta should be accepted.
