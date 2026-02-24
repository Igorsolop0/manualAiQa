# LEARNINGS.md — Lessons Learned

**Purpose:** Document corrections, better approaches, and key learnings to avoid repeating mistakes.

**Updated:** 2026-02-23

---

## 🎯 Section 1: Data Sources — ALWAYS Verify

### Learning: BO Prod Data = Source of Truth

**Date:** 2026-02-23  
**Context:** Writing test cases for Regular Bonuses  
**Mistake:** I assumed Weekly bonuses have wagering because documentation mentioned it  
**Correction:** Ihor pointed out that BO Prod data shows `TurnoverCount: null` for ALL Regular Bonuses  
**Lesson:** 
- **ALWAYS** fetch real data from BO Prod before making assumptions
- Documentation (Confluence) may be outdated
- Verify with actual API responses: `curl adminwebapi.prod.sofon.one`

**Applied to:** All bonus-related testing

---

## 🎯 Section 2: Bonus System — Real Data

### Learning: Regular Bonuses Have NO Wagering

**Date:** 2026-02-23  
**Source:** BO Prod Data (adminwebapi)  
**Fact:**
```
Monthly (ID 8301): TurnoverCount: null, BonusTypeId: 11
Weekly (ID 8299): TurnoverCount: null, BonusTypeId: 11  
Cashback (ID 7207): TurnoverCount: null, BonusTypeId: 11
```

**Implications:**
- NO wagering progress bar on Regular Bonus cards
- Progress bar shows TIME until next period, NOT wagering
- Amount credited directly to real balance (no "Active Bonuses" entry)

**DO NOT:**
- Create test cases about wagering for Regular Bonuses
- Assume Weekly/Monthly have different logic

---

### Learning: Regular Bonus States (Real Names)

**Date:** 2026-02-23  
**Source:** Ihor correction + HTML inspection  
**States:**
1. **Waiting for reward** — Timer visible, waiting for calculation
2. **Ready for claim** — Amount calculated, button "Claim ${amount}"
3. **Claimed** — Amount credited to balance

**DO NOT USE (invented):**
- ❌ AwaitingForActivation
- ❌ ReadyForActivation
- ❌ Closed
- ❌ Finished

---

### Learning: CT-45 Applies to ALL Regular Bonuses

**Date:** 2026-02-23  
**Source:** Ihor correction  
**Fact:** CT-45 (parallel claim) applies to **ALL** Regular Bonuses (Cashback, Rakeback, Weekly, Monthly)

**Reason:** All have `BonusTypeId: 11` (CampaignCash) and `TurnoverCount: null`

**DO NOT:**
- Create test cases claiming Weekly "cannot claim parallel"
- Differentiate between Regular Bonus types for parallel claim logic

---

## 🎯 Section 3: Special vs Regular Bonuses — Key Differences

### Learning: Special Bonuses HAVE Wagering (Most)

**Date:** 2026-02-23  
**Source:** BO Prod Data  
**Fact:**
- Special Bonuses: `TurnoverCount > 0` (most have wagering)
- Regular Bonuses: `TurnoverCount: null` (NO wagering)

**Differences:**

| Parameter | Regular | Special |
|-----------|---------|---------|
| Wagering | ❌ None | ✅ Most have |
| States | 3 | 5 |
| Parallel Claim | ✅ Yes (CT-45) | ❌ Mono-bonus |
| Active Bonus Position | In list | Always FIRST |
| Progress Bar | TIME % | Wagering % |

---

## 🎯 Section 4: Test Case Design

### Learning: E2E Flow, Not Short Checks

**Date:** 2026-02-23  
**Source:** Ihor feedback  
**Correction:** "Test cases should have E2E flow, not short checks"

**Before (WRONG):**
```
TC-RB-002: State Transition AwaitingForActivation → ReadyForActivation
Steps: 1. Wait for timer, 2. Check state
```

**After (CORRECT):**
```
TC-RB-002: Cashback — Ready for Claim State
Steps: 1. Login, 2. Navigate, 3. Check state, 4. Check amount, 5. Click Claim, 6. Verify balance, 7. Check return to Waiting
```

**Lesson:** Each test case should cover a complete user journey

---

### Learning: TestRail Format — Follow Existing Structure

**Date:** 2026-02-23  
**Source:** TestRail Footer section analysis  
**Format:**
```json
{
  "title": "Verify ...",
  "priority_id": 2 (Critical) | 3 (High) | 4 (Medium),
  "type_id": 11 (Acceptance),
  "custom_preconds": "<p>Precondition 1</p><p>Precondition 2</p>",
  "custom_steps_separated": [
    {
      "content": "<p>Step description</p>",
      "expected": "<p>Expected result</p>"
    }
  ]
}
```

**DO:**
- Use HTML tags (`<p>`) in preconds and steps
- Separate steps logically (not too many in one step)
- Always include expected result

---

## 🎯 Section 5: API Documentation

### Learning: BonusTypeId Meanings

**Date:** 2026-02-23  
**Source:** BO Prod Data  
**Mapping:**
- **11** = CampaignCash (Regular Bonuses)
- **10** = Unknown (Cash Drop, Low Balance bonuses)
- **14** = FreeSpin-related
- **16** = Deposit+FS combination

**Action:** When unsure, check BO Prod for examples

---

## 🎯 Section 6: Clarification Questions

### Learning: Ask Before Assuming

**Date:** 2026-02-23  
**Context:** I invented bonus states and wagering logic  
**Correction:** Ihor had to correct multiple assumptions

**Better Approach:**
1. Fetch real data from BO Prod
2. Check HTML/UI if user provides it
3. Ask clarification questions if documentation unclear
4. Mark unclear info as "TBD" instead of guessing

---

## 🎯 Section 7: Cron Jobs & Automation

### Learning: Cron Job Failures Need Investigation

**Date:** 2026-02-23  
**Source:** Multiple cron failures  
**Fact:** Gmail Check cron was failing systematically with "LLM request timed out" (33-35s runtime, 0 output)

**Issue:**
- z.ai API timeout ~33-35 seconds
- Model not responding within timeout limit
- Multiple failures in one day

**Actions:**
1. Monitor cron job failures
2. Report systematic issues immediately
3. Suggest solutions (increase timeout, change model)

---

## 🎯 Section 8: Integration Knowledge

### Learning: Gmail + Jira Integration Setup

**Date:** 2026-02-14  
**Source:** Session memory  
**Components:**
- Gmail IMAP with App Password
- `go-jira` CLI for API access
- Cron job for automatic checks (every 30 min, 9:00-18:00 CET)
- Jira ticket extraction and summarization
- Telegram notifications

**Files:**
- `scripts/gmail_checker.py` — Email detector
- `scripts/jira_fetch.py` — Ticket fetcher
- `.gmail_config` — App Password
- `.jira_token` — API Token

**Usage:** Use `jira_fetch.py CT-XXX` to get ticket details quickly

---

## 🎯 Section 9: Wallet Service API

### Learning: Wallet Service — Alternative to BO API for Balance Operations

**Date:** 2026-02-24  
**Source:** Ihor discovery  
**Swagger:** https://wallet.dev.sofon.one/swagger/index.html

**Environments:**
- **Dev:** https://wallet.dev.sofon.one
- **QA:** https://wallet.qa.sofon.one
- **Prod:** https://wallet.prod.sofon.one

**Auth:** No authentication required (open API)

---

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **GET** | `/{partnerId}/api/v1/balance/{clientId}/{currency}` | Check client balance |
| **GET** | `/{partnerId}/api/v1/client-state/{clientId}/{currency}` | Get client state |
| **GET** | `/{partnerId}/api/v1/transaction/list/client/{clientId}` | List transactions |
| **GET** | `/{partnerId}/api/v1/transaction/{transactionId}` | Transaction details |
| **POST** | `/{partnerId}/api/v1/transaction/correction/credit` | Remove money ❌ |
| **POST** | `/{partnerId}/api/v1/transaction/correction/debit` | Add money ✅ |
| **POST** | `/{partnerId}/api/v1/transaction/payment/direct-deposit` | Direct deposit |
| **POST** | `/{partnerId}/api/v1/transaction/payment/withdrawal` | Withdrawal |
| **POST** | `/{partnerId}/api/v1/transaction/bet/credit` | Bet credit |
| **POST** | `/{partnerId}/api/v1/transaction/bet/debit` | Bet debit |
| **POST** | `/{partnerId}/api/v1/transaction/rollback` | Rollback transaction |

---

### Balance Check (Verified Working!)

```bash
curl 'https://wallet.dev.sofon.one/5/api/v1/balance/59107/USD'
```

**Response:**
```json
{
  "Balances": {
    "Unused": 30.91
  },
  "AvailableMain": 30.91,
  "AvailableBonus": 0.0,
  "Currency": "USD",
  "SportBonus": 0.0
}
```

---

### Operation Types

- `BetCredit` / `BetDebit` — Bets
- `Deposit` / `Withdrawal` — Deposit/Withdrawal
- `CorrectionCredit` / `CorrectionDebit` — Corrections
- `BonusAwarding` / `BonusRelease` / `BonusCancel` — Bonuses
- `Rollback` — Rollback

---

### Direct Deposit Issue

**Problem:** `direct-deposit` returns `InvalidRateBalances` error  
**Workaround:** Use `correction/debit` instead  
**BO API Alternative:** `/api/Client/CreateDebitCorrection` works on adminwebapi

---

### Comparison: BO API vs Wallet API

| Feature | BO API (adminwebapi) | Wallet API |
|---------|---------------------|------------|
| Balance Check | ❌ Complex | ✅ Simple GET |
| Add Money | ✅ CreateDebitCorrection | ✅ correction/debit |
| Auth | `UserId` header | None (open) |
| Transaction History | ✅ Available | ✅ Available |
| Best For | Admin operations | Balance operations |

**Recommendation:** Use Wallet API for balance checks, BO API for complex admin operations

---

## 📊 Summary of Key Principles

1. **Source of Truth:** BO Prod data > Documentation
2. **Verify:** Always fetch real data before writing tests
3. **Names:** Use exact names from UI/API, don't invent
4. **Flow:** Write E2E tests, not short checks
5. **Ask:** If uncertain, ask instead of assuming
6. **Learn:** Record corrections immediately
7. **Monitor:** Watch for systematic failures (cron jobs, API issues)

---

## 🔄 Update Log

| Date | Learning | Section |
|------|----------|---------|
| 2026-02-23 | BO Prod = Source of Truth | 1 |
| 2026-02-23 | Regular Bonuses NO Wagering | 2 |
| 2026-02-23 | Regular Bonus States | 2 |
| 2026-02-23 | CT-45 Applies to ALL Regular | 2 |
| 2026-02-23 | Special vs Regular Differences | 3 |
| 2026-02-23 | E2E Flow Tests | 4 |
| 2026-02-23 | TestRail Format | 4 |
| 2026-02-23 | BonusTypeId Mapping | 5 |
| 2026-02-23 | Ask Before Assuming | 6 |
| 2026-02-24 | Wallet Service API | 9 |
| 2026-02-23 | Cron Job Failure Monitoring | 7 |
| 2026-02-14 | Gmail + Jira Integration | 8 |
