# Nexus Planning Format

Date: 2026-03-15
Scope: Nexus ticket summary, QA analysis, and test plan output

This document defines the canonical response shape Nexus should use when Ihor asks for:

- a ticket summary
- a QA analysis
- a test plan
- a delegation-ready testing outline

It complements:

- `/Users/ihorsolopii/.openclaw/docs/architecture/qa-operating-framework.md`
- `/Users/ihorsolopii/.openclaw/docs/architecture/qa-layered-test-design-profile.md`
- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

It does not replace:

- agent role rules in `workspace/SOUL.md`
- task file details in `workspace/shared/tasks/`

## 1. Preferred Output Shape

For ticket-centric QA planning, Nexus should usually answer in this order:

1. `Context Retrieval`
2. `Feature Framing`
3. `Risk Focus`
4. `Execution Split`
5. `Test Plan`
6. `Approval / Next Action`

This shape may be shortened for very small requests, but the internal thinking should stay the same.

Layer mapping:

- `Context Retrieval` = Layer 0 Memory Check
- `Feature Framing` = Layer 1 Feature Container
- `Risk Focus` + `Execution Split` = Layers 2-4 operationalized for ownership
- `Test Plan` = Layer 5 Scenario Set

## 2. Context Retrieval

Keep this section short and concrete.

Show:

- what prior knowledge was actually found
- what project assets were actually checked
- what important information is still missing

Good sources include:

- Jira description
- recent Jira comments
- related tickets
- prior task files
- project knowledge
- existing E2E assets, fixtures, helpers, scripts, or session references when relevant

Avoid fake retrieval claims. If an asset was not checked, do not imply that it was.

## 3. Feature Framing

Summarize the testing target in behavior terms:

- what changed
- what the user is trying to accomplish
- what visible behavior should happen
- what backend or data dependency matters
- what environment or page matters

The goal is to define the real testable behavior before listing scenarios.

## 4. Risk Focus

Call out the highest-value risks explicitly.

Examples:

- token missing or stale
- wrong token passed to backend
- backend accepts request but provider flow is wrong
- profile state not updated after success
- UI claims success while backend state is inconsistent

Do not hide the key risks inside a long scenario list.

## 5. Execution Split

Say clearly which part belongs to which agent:

- `Clawver`
- `Cipher`
- `Nexus only`

Examples:

- `Clawver` for UI flow, browser evidence, console, network, and visible profile state
- `Cipher` for backend verification, payload validation, state prep, or API truth checks

If the task is truly executor-specific, say that explicitly instead of mixing concerns.

## 6. Test Plan

The plan should be execution-oriented, not essay-like.

For each scenario or slice, make clear:

- what is checked
- why it matters
- what evidence should prove it
- which agent should execute it

Scenario wording should stay operational.

Weak example:

- `simulate missing token state`

Better example:

- `Clawver: capture network request when initiating link without active session, if reproducible through logout or expired session`
- `Cipher: validate backend response for invalid token path if the UI cannot safely generate that state`

## 7. Approval / Next Action

If execution is required:

- ask for approval clearly
- do not ask vague follow-up questions
- after approval, move directly into execution

## 8. Planning Quality Bar

A good Nexus planning response should:

- show real context retrieval
- frame the feature in behavior terms
- isolate the key risks
- split UI and API responsibilities when needed
- keep scenarios narrow and executable
- make approval the final step before execution

## 9. Relationship To Task Files

Task files should reflect this format in compact form.

Expected task-file fields include:

- context retrieval notes
- feature framing
- risk focus
- execution owner
- execution split
- scenarios
- evidence destination

See:

- `/Users/ihorsolopii/.openclaw/workspace/shared/tasks/README.md`
