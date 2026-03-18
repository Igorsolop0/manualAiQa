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
3. Pilot tickets still write legacy evidence first, then sync.
4. If auth is blocked, document the login wall instead of improvising risky actions.
5. One ticket or one charter per run keeps failures and context drift manageable.
6. Use `playwright-cli` for all browser interaction (Stagehand is deprecated).
7. Do NOT write .spec.ts files — Clawver does manual QA, not automation.
8. Every run MUST emit at least one learning via `run_manager.py emit-learning`.

## Existing Test Infrastructure (MUST CHECK FIRST)

**Before creating anything from scratch, check the existing E2E project:**

`/Users/ihorsolopii/Documents/minebit-e2e-playwright`

This project has ready-made:
- **Registration:** `src/gui/minebit/modals/auth/SignUpModal.ts` + `src/fixtures/player.fixture.ts`
- **Login:** `src/gui/minebit/modals/auth/LogInModal.ts`
- **Homepage:** `src/gui/minebit/pages/home/HomePage.ts`
- **Recent Winners:** `src/gui/minebit/components/widgets/RecentTopWinsWidget.ts`
- **API Client:** `src/utils/api/ApiClient.ts`
- **Test Data:** `src/fixtures/test-data.fixture.ts` + `src/utils/DataGenerator.ts`
- **Global Users:** `src/constants/GlobalUsers.ts` (pre-configured test accounts)

**Rule:** Read the relevant Page Object or fixture BEFORE attempting UI actions. It contains selectors, flows, and edge case handling that has already been tested.

Full inventory: see `PROJECT_KNOWLEDGE.md` section 3.

## Known Weak Spots

1. Exploratory tasks can drift into oversized Playwright smoke suites if scope is not kept narrow.
2. Generated artifacts may accidentally use wrong ticket naming such as adding an unwanted `CT-` prefix.
3. Overly broad runs lose the original browser goal and produce untrustworthy summaries.

## Practical Reminders

1. Read the task file fully before opening the browser.
2. Match output folder exactly to the task.
3. Use console and network when UI behavior is unclear.
4. Return only evidence-backed conclusions.
