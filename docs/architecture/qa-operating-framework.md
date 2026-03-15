# QA Operating Framework

Date: 2026-03-15
Scope: Nexus, Clawver, Cipher

This document is the shared QA cognition layer for the OpenClaw core trio.

It is not:

- a full ISTQB textbook
- a project-specific knowledge base
- a replacement for agent role files

It is:

- the shared way the agents should think about QA work
- the canonical order for analyzing and decomposing testing tasks
- the reference point for behavior-aware, evidence-first QA execution

## 1. Core Mindset

OpenClaw agents should approach QA as behavior-aware specialists.

That means:

- understand expected behavior before generating checks
- reason from visible system behavior, business rules, and evidence
- prefer narrow, testable scope over broad fake coverage
- separate planning, execution, validation, and review clearly
- treat ambiguity as something to surface and reduce, not ignore

## 2. Shared Definitions

### Testing Level

The layer where a check primarily happens.

Examples:

- UI
- API
- integration
- backend state

### Testing Type

The intent of the testing activity.

Examples:

- functional
- regression
- exploratory
- smoke

For ordinary product tickets, default to functional coverage first unless the user asks for something else.

### Test Design Technique

The thinking tool used to cut the feature into meaningful checks.

Examples:

- equivalence partitioning
- boundary value analysis
- decision tables
- state transition
- scenario-based testing
- exploratory testing

### Evidence

Artifacts that prove what was actually executed and observed.

Examples:

- screenshots
- browser console findings
- network findings
- response payloads
- logs
- result files

### Assumption

A temporary statement used because a requirement is missing or unclear.

Assumptions must be explicit and should not be hidden inside the final result.

### Ambiguity

A meaningful gap in requirements, expected behavior, environment, access, or scope that can change how the test should be designed or executed.

## 3. QA Cognition Flow

Use this order whenever the task requires QA thinking:

1. memory check
2. feature framing
3. scope selection
4. technique selection
5. risk prioritization
6. scenario generation
7. execution or delegation choice
8. evidence review
9. learning extraction

Do not jump directly from ticket text to long test-case lists.

## 4. Memory Check

Before designing tests, look for relevant prior knowledge:

- similar tickets or flows
- known weak spots
- known flaky or unstable areas
- reusable credentials, sessions, scripts, helpers, or fixtures
- prior bugs or domain rules that should influence the plan

Output should stay short and useful:

- what is relevant
- what is missing
- what may change the plan

## 5. Feature Framing

Before choosing tools or scenarios, define:

- what changed
- who is affected
- what the expected behavior is
- what dependencies exist
- what environment matters
- what is still unclear

Good feature framing should produce:

- a short feature summary
- known requirements
- constraints
- explicit unknowns or assumptions

## 6. Scope Selection

Choose only the scope that is justified by the task.

For standard Minebit or NextCode tickets, the default practical scope is usually:

- functional
- black-box
- positive and negative coverage
- UI, API, or data-level checks where actually relevant

Do not automatically expand into:

- security testing
- performance testing
- load testing
- usability testing

unless the ticket or user explicitly asks for that scope.

## 7. Technique Selection

Pick test design techniques based on the actual shape of the feature.

Use:

- equivalence partitioning for input groups and rule buckets
- boundary value analysis for limits, ranges, thresholds, timers, and counters
- decision tables for combinations of conditions and rules
- state transition for flows that move through meaningful statuses
- scenario-based testing for user journeys
- exploratory testing when the path, behavior, or UI is unclear

The key rule:

- do not list techniques for decoration
- say what part of the feature each technique is cutting

## 8. Risk Prioritization

Prioritize checks by business and product risk, not by theoretical completeness.

Typical high-priority risk areas:

- auth and access
- money movement
- bonus eligibility and bonus state
- KYC and compliance states
- player state transitions
- backend and UI mismatch
- destructive or unsafe PROD actions

Use risk to answer:

- what must be tested first
- what can be sampled
- what can be deferred

## 9. Scenario Generation

Generate scenarios only after the structure above is clear.

Good scenarios should be:

- traceable to a requirement or risk
- linked to an expected behavior
- small enough to execute and verify honestly
- assignable to the right agent

Each scenario should imply:

- what is being checked
- why it matters
- where it should be checked
- what evidence would prove the result

## 10. Delegation Model

### Nexus

Best for:

- ticket analysis
- test planning
- routing
- review
- final synthesis

### Clawver

Best for:

- browser execution
- exploratory UI work
- Stagehand-assisted path discovery
- Playwright-based deterministic verification
- user-visible evidence

### Cipher

Best for:

- API validation
- backend truth checks
- data preparation
- auth or session support
- contract and payload verification

The key rule:

- route work by evidence need and specialization, not by habit

## 11. Ambiguity And Discovery

When the task is unclear:

- do not invent certainty
- identify the ambiguity explicitly
- ask one narrow question if needed
- or run a narrow discovery slice

Discovery is valid when it reduces uncertainty.

Examples:

- Stagehand to find an unstable path or modal entry point
- API inspection to understand backend state requirements
- small reproduction pass before full test execution

Ambiguity should become:

- a clarified assumption
- a refined plan
- or a real blocker

not silent improvisation.

## 12. Evidence And Confidence

Evidence is the source of truth.

Not all evidence is equally strong.

Examples:

- screenshot only = weak proof of behavior
- screenshot + console + network = stronger UI proof
- API response + verified state effect = stronger backend proof
- consistent artifacts across UI and API = highest confidence

Use actual status language consistently:

- `completed`
- `partial`
- `blocked`
- `failed`

Do not use optimistic language when artifacts are missing.

## 13. Learning Extraction

After execution, capture only durable learnings:

- new product behavior
- repeated weak spots
- reusable paths
- domain rules
- handoff improvements
- better routing patterns

Do not dump raw logs into long-term memory.

The goal is:

- improve future planning
- improve future execution
- improve future confidence

## 14. Behavior-Aware QA In Practice

Behavior-aware QA means:

- thinking about what the user does
- what the system should do next
- what can go wrong at each visible transition
- what evidence is needed to prove the actual outcome

It does not require source code access to be valuable.

It does require:

- product understanding
- domain awareness
- structured test thinking
- honest evidence review

## 15. Relationship To Other Documents

Use this framework together with:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`
- agent-specific `SOUL.md` files
- project knowledge such as Minebit or Lorypten docs
- `/Users/ihorsolopii/.openclaw/workspace/TESTRAIL_STANDARDS.md` when working on TestRail output

For deeper explanation of the original practical test-design idea, see:

- `/Users/ihorsolopii/.openclaw/workspace/QA_TEST_DESIGN_APPROACH.md`

That file is a source and extended explanation.
This file is the compact canonical operating framework.
