# ERRORS.md — Mistakes to Avoid

**Purpose:** Document specific mistakes to NEVER repeat.

**Updated:** 2026-02-23

---

## ❌ Error #1: Invented Weekly Bonus Wagering

**Date:** 2026-02-23  
**Context:** Writing test cases for Regular Bonuses  
**What I did:** Created TC-RB-005 claiming Weekly bonus has wagering and cannot be claimed parallel  
**Why it was wrong:** BO Prod shows `TurnoverCount: null` for Weekly (ID 8299)  
**Impact:** Created misleading test case, Ihor had to correct  
**How to avoid:**
- ALWAYS fetch bonus data from BO Prod before assuming wagering
- Check `TurnoverCount` field in API response
- If `null` → NO wagering

**Corrected:** Removed TC-RB-005, added correct logic to all Regular Bonus tests

---

## ❌ Error #2: Invented Bonus States

**Date:** 2026-02-23  
**Context:** Describing Regular Bonus states  
**What I did:** Used states "AwaitingForActivation", "ReadyForActivation", "Closed"  
**Why it was wrong:** Real states are "Waiting for reward", "Ready for claim", "Claimed"  
**Impact:** Wrong terminology in 15+ test cases, confusion  
**How to avoid:**
- Check HTML class names (e.g., `RegularAwaitingBonus`)
- Ask user for real state names
- Don't invent terms based on other systems

**Corrected:** Rewrote all test cases with correct states

---

## ❌ Error #3: Created Invalid Test Case (Weekly Exception)

**Date:** 2026-02-23  
**Context:** TC-RB-005 "Weekly Bonus — Cannot Claim Parallel"  
**What I did:** Assumed Weekly has wagering and created exception to CT-45  
**Why it was wrong:** 
1. Weekly has NO wagering (`TurnoverCount: null`)
2. CT-45 applies to ALL Regular Bonuses
3. Weekly CAN be claimed parallel

**Impact:** Wrong test case that would fail on prod  
**How to avoid:**
- Verify assumptions with BO data BEFORE writing tests
- Check if CT-45 or other tickets apply to ALL or specific types

**Corrected:** Deleted TC-RB-005 entirely

---

## ❌ Error #4: Assumed Documentation is Current

**Date:** 2026-02-23  
**Context:** Read Confluence docs about Cashback wagering  
**What I did:** Added "Wagering x3 for Loyalty Level 1" to test cases  
**Why it was wrong:** BO Prod shows `TurnoverCount: null` — documentation is outdated  
**Impact:** Added incorrect info to test cases  
**How to avoid:**
- BO Prod data = Source of Truth
- If doc contradicts BO → trust BO
- Mark documentation as "may be outdated" if discrepancy found

**Corrected:** Removed all wagering references for Regular Bonuses

---

## ❌ Error #5: Invented "Closed" Status

**Date:** 2026-02-23  
**Context:** Describing bonus lifecycle  
**What I did:** Added "Closed" status after claiming bonus  
**Why it was wrong:** Real status is "Claimed" (no "Closed" exists)  
**Impact:** Wrong terminology  
**How to avoid:**
- Don't invent statuses
- Check API responses or ask user

**Corrected:** Changed to "Claimed"

---

## ❌ Error #6: Short Tests Instead of E2E Flow

**Date:** 2026-02-23  
**Context:** Initial test case design  
**What I did:** Created tests like "TC-RB-002: State Transition" with 2-3 steps  
**Why it was wrong:** Ihor wants E2E flows (complete user journey)  
**Impact:** Had to rewrite 15 tests  
**How to avoid:**
- Each test should cover: Setup → Action → Verification → Cleanup
- Minimum 5+ steps per test
- Think "user journey" not "single check"

**Corrected:** Rewrote all 15 tests as E2E flows

---

## ❌ Error #7: Didn't Check Existing TestRail Structure

**Date:** 2026-02-23  
**Context:** Adding test cases to TestRail  
**What I did:** Started writing before checking existing format  
**Why it was wrong:** TestRail has specific format (HTML tags, steps structure)  
**Impact:** Could have created wrong format tests  
**How to avoid:**
- ALWAYS check existing tests first (Footer section)
- Follow same format exactly
- Use API to inspect existing cases

**Corrected:** Checked Footer section, followed correct format

---

## ❌ Error #8: Didn't Report Cron Failures Proactively

**Date:** 2026-02-23  
**Context:** Gmail Check cron was failing repeatedly  
**What I did:** Only reported when user asked, didn't proactively investigate  
**Why it was wrong:** Systematic failures (3+ times) should be reported immediately  
**Impact:** User didn't know cron was broken until they checked  
**How to avoid:**
- Track cron failures
- Report systematic issues after 2nd failure
- Suggest solutions proactively

**Corrected:** Now will monitor and report cron failures

---

## 📊 Error Statistics (2026-02-23)

| Error Type | Count | Severity |
|------------|-------|----------|
| Invented data | 3 | High |
| Assumed docs correct | 1 | High |
| Wrong test design | 2 | Medium |
| Didn't check existing | 1 | Low |
| Didn't report failures | 1 | Medium |

**Total:** 8 errors in one session  
**User corrections required:** Multiple  
**Tests rewritten:** 15/30 (50%)

---

## 🎯 Prevention Checklist

Before writing ANY test case:

- [ ] Fetched real data from BO Prod
- [ ] Verified `TurnoverCount` field
- [ ] Checked exact state names (UI/API)
- [ ] Confirmed CT-XX tickets applicability
- [ ] Verified documentation is current
- [ ] Checked existing TestRail format
- [ ] Designed E2E flow (5+ steps)
- [ ] No invented terms or statuses

After ANY session:

- [ ] Updated LEARNINGS.md if learned something new
- [ ] Updated ERRORS.md if made mistakes
- [ ] Reported systematic issues (cron failures, API problems)

---

## 💡 Key Principle

> "If I'm guessing or assuming, I'm probably wrong. ALWAYS verify with real data."

---

## 🔄 Update Log

| Date | Error ID | Description | Corrected |
|------|----------|-------------|-----------|
| 2026-02-23 | #1 | Weekly wagering | ✅ Yes |
| 2026-02-23 | #2 | Bonus states | ✅ Yes |
| 2026-02-23 | #3 | Weekly exception | ✅ Yes |
| 2026-02-23 | #4 | Docs outdated | ✅ Yes |
| 2026-02-23 | #5 | Closed status | ✅ Yes |
| 2026-02-23 | #6 | Short tests | ✅ Yes |
| 2026-02-23 | #7 | TestRail format | ✅ Yes |
| 2026-02-23 | #8 | Cron failures | ✅ Yes |
