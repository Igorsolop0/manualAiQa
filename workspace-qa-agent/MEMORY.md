# MEMORY.md - Clawver Long-Term Memory

Use this file for curated QA execution memory only.

Keep:

- proven browser execution rules
- recurring UI/auth/evidence pitfalls
- stable environment truths
- lessons that improve future browser runs

Do not keep generic QA theory here.

## Current Operational Truths

1. Clawver must execute the task, not just generate test code.
2. Evidence path correctness is mandatory; wrong ticket id means broken output.
3. `Stagehand REQUIRED` means Stagehand-first discovery, not broad Playwright substitution.
4. Pilot tickets still write legacy evidence first, then sync.
5. If auth is blocked, document the login wall instead of improvising risky actions.
6. One ticket or one charter per run keeps failures and context drift manageable.

## Known Weak Spots

1. Exploratory tasks can drift into oversized Playwright smoke suites if scope is not kept narrow.
2. Generated artifacts may accidentally use wrong ticket naming such as adding an unwanted `CT-` prefix.
3. Overly broad runs lose the original browser goal and produce untrustworthy summaries.

## Practical Reminders

1. Read the task file fully before opening the browser.
2. Match output folder exactly to the task.
3. Use console and network when UI behavior is unclear.
4. Return only evidence-backed conclusions.
