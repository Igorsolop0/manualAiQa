# Refactor Compliance Checklist

Date: 2026-03-15
Scope: review checklist for OpenClaw ticket runs after Phase 2 and during Phase 3

Use this checklist after any meaningful ticket run to decide whether the run matches the intended OpenClaw refactor model.

The goal is not to demand perfection on every run. The goal is to quickly classify:

- what already matches the target state
- what is still legacy behavior
- what should be fixed next

## How to score a run

Use one mark per line:

- `[x]` = confirmed
- `[~]` = partial / inconsistent
- `[ ]` = missing

At the end, summarize the run as:

- `aligned` = mostly `[x]`, no critical misses
- `partially aligned` = useful progress, but important gaps remain
- `not aligned` = execution happened outside the intended architecture

## 1. Intake And Planning

- [ ] Nexus produced a ticket summary before execution
- [ ] Planning followed the layered profile (`Memory -> Feature -> Types -> Techniques -> Risks -> Scenarios`)
- [ ] Nexus used a narrow scope instead of a broad generic suite
- [ ] The task clearly states environment, target URL/area, success check, and evidence path
- [ ] Approval gate was respected before execution
- [ ] The plan stayed close to the user request without major scope drift

## 2. Delegation And Ownership

- [ ] Nexus delegated real work to the correct executor
- [ ] Clawver owned UI/browser work
- [ ] Cipher owned API/data/backend work when needed
- [ ] UI and API concerns were split clearly when both were needed
- [ ] Nexus did not simulate execution through narration alone

## 3. Tool Discipline

- [ ] The chosen tool matched the task type
- [ ] `Stagehand REQUIRED` tasks stayed Stagehand-first
- [ ] `Stagehand ONLY` tasks did not create fallback Playwright test artifacts
- [ ] For `Stagehand ONLY`, `stagehand-guard-post.json` exists and indicates no violation
- [ ] Playwright was used only when the task or policy actually allowed it
- [ ] Existing project assets were reused when relevant instead of reinventing setup

## 4. Evidence Quality

- [ ] The expected result folder exists
- [ ] The run produced real artifacts, not only status text
- [ ] Screenshots or DOM snapshots exist for the important steps
- [ ] Primary result artifact exists (`summary`, `result json`, or equivalent)
- [ ] Reported status matches the actual evidence

## 5. Phase 2 Pilot Compliance

Check this section only for tickets that are supposed to use the pilot flow.

- [ ] A run exists under `shared/runs/<run_id>/`
- [ ] Legacy evidence was mirrored into the run-centric structure
- [ ] `RUN_ID.txt` or equivalent pilot linkage exists where expected
- [ ] `result-packet` was emitted
- [ ] `session-record` was used when auth/session handoff mattered
- [ ] Fail-fast guard was executed for Stagehand-only tasks before final status
- [ ] Final summary passed through the result-ready / validation gate

## 6. Learning Sync Compliance

- [ ] The run produced at least one evidence-backed learning candidate when something useful was discovered
- [ ] A ticket insight note was created when the finding was durable enough
- [ ] `DAILY_INSIGHTS.md` was updated when appropriate
- [ ] Learnings were short, reusable, and grounded in artifacts
- [ ] No noisy or speculative learning was promoted as durable truth

## 7. Naming And Traceability

- [ ] Ticket ID naming is consistent across task, result, and artifact paths
- [ ] Artifact paths are easy to follow from task to result
- [ ] Final summary references real files that exist
- [ ] No confusing duplicate task files were created without reason

## 8. Honest Status Behavior

- [ ] `completed` means the requested scope actually ran and evidence exists
- [ ] `partial` was used honestly when only part of the flow worked
- [ ] `blocked` or `failed` was used when execution could not continue
- [ ] The agent did not claim success from plans or generated files alone
- [ ] Escalation clearly explained what happened, what was tried, and what next action was needed

## 9. Review Summary Template

Use this short template when reviewing a run:

```md
## Refactor Compliance Review

- Run: <ticket or run id>
- Verdict: aligned | partially aligned | not aligned

### What matched
- ...

### What was partial
- ...

### What is still missing
- ...

### Next fix
- ...
```

## 10. Current Main Gaps To Watch

These are the most important recurring gaps during the current refactor stage:

- Phase 2 pilot not being used consistently for real CT runs
- `Stagehand ONLY` tasks still producing fallback Playwright artifacts
- learning sync not yet happening reliably after real runs
- inconsistent path naming such as `CT-548` vs `ct-548`
- Nexus still over-narrating execution in some flows instead of returning a clean artifact-backed state
