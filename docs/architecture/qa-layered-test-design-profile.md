# QA Layered Test Design Profile

Date: 2026-03-16
Scope: Nexus, Clawver, Cipher
Alias: "Burger" method

This profile is the practical layered test-design sequence for real ticket work.

It complements:

- `/Users/ihorsolopii/.openclaw/docs/architecture/qa-operating-framework.md`
- `/Users/ihorsolopii/.openclaw/docs/architecture/nexus-planning-format.md`

It does not replace:

- agent role boundaries in `SOUL.md`
- run/pilot execution contracts

## 1. Required Layer Order

Use this order for ticket analysis and test design:

0. Memory Check
1. Feature Container
2. Testing Types
3. Design Techniques
4. Principles and Risk Prioritization
5. Scenario Set

Do not jump directly to long scenario lists.

## 2. Layer Outputs

### 0) Memory Check

Output:

- similar tickets or flows
- known risks and recurring defects
- existing coverage and reusable helpers
- reusable auth/session/data references
- what is missing

### 1) Feature Container

Output:

- feature summary in behavior terms
- known requirements
- constraints and dependencies
- unknowns and assumptions

### 2) Testing Types

Default for daily Minebit ticket flow:

- functional
- black-box
- positive + negative

Expand to security/performance/usability only if explicitly requested.

### 3) Design Techniques

Pick techniques by feature shape and state what each one cuts:

- equivalence partitioning
- boundary value analysis
- decision tables
- state transition
- scenario/use-case
- exploratory

### 4) Principles and Risk Prioritization

Output:

- principles used (risk-based, no exhaustive testing, defect clustering, etc.)
- top risks
- test-first priority order

### 5) Scenario Set

Generate only after layers 0-4 are done.

Each scenario should include:

- requirement or behavior reference
- testing type
- technique origin
- risk being covered
- owner (`nexus`, `qa-agent`, `api-docs-agent`)
- expected evidence

## 3. Ambiguity Rule

If requirements are unclear:

1. state the ambiguity explicitly
2. ask one focused clarification question or mark assumptions
3. continue only on declared assumptions or return blocked/partial

No hidden assumptions.

## 4. Domain Overlay Rule

Use project/domain overlays from curated knowledge:

- `workspace/PROJECT_KNOWLEDGE.md`
- ticket/run artifacts
- agent memory

Examples of overlay concerns:

- Minebit: auth, payments, bonuses, KYC, Smartico behavior, backend/UI consistency
- Lorypten/Web3: wallet flows, signing, confirmation, network-specific behavior

Do not copy domain textbook material into every plan. Use only what changes execution.

## 5. Compact Output Template

Use this shape when producing a practical layered plan:

```md
Memory Check:
- ...

Feature Container:
- summary: ...
- requirements: ...
- constraints/dependencies: ...
- unknowns/assumptions: ...

Testing Types:
- ...

Design Techniques:
- technique -> target slice

Principles and Risk Prioritization:
- principles: ...
- top risks: ...
- execution order: ...

Scenario Set:
1) [type | technique | risk | owner] scenario ... -> evidence ...
```
