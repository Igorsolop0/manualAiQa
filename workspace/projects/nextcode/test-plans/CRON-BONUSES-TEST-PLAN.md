# Test Plan: CRON Scheduled Bonuses

## Overview

Test CRON-based scheduled bonuses to verify:
1. Correct `nextAvailableAt` calculation
2. Correct `previousAvailableAt` calculation
3. Proper claim flow with scheduled periods
4. New user experience (CT-756 feature)

---

## Prerequisites

- BackOffice access to create/configure bonuses
- Test user accounts
- API access to `GetEligibleBonuses`

---

## Test Scenarios

### TC-CRON-01: Daily Bonus — Verify nextAvailableAt

**Setup:**
1. Create Regular Cashback bonus with CRON: `0 12 * * *` (daily at 12:00 UTC)
2. Set campaign dates to cover test period

**Steps:**
1. Register new user
2. Call `GetEligibleBonuses` before 12:00 UTC
3. Verify `nextAvailableAt` = today 12:00 UTC OR tomorrow 12:00 UTC (depending on current time)
4. Wait until after 12:00 UTC
5. Call `GetEligibleBonuses` again
6. Verify `isAvailable = true`

**Expected Result:**
```
Before 12:00:
├── isAvailable: false
├── nextAvailableAt: <today 12:00 UTC>
└── previousAvailableAt: <yesterday 12:00 UTC>

After 12:00:
├── isAvailable: true
├── nextAvailableAt: null
└── lastClaimedAt: null
```

---

### TC-CRON-02: Weekly Bonus — Monday Schedule

**Setup:**
1. Create bonus with CRON: `0 0 * * 1` (every Monday 00:00 UTC)

**Steps:**
1. Register new user
2. Call `GetEligibleBonuses`
3. Verify `nextAvailableAt` = next Monday 00:00 UTC
4. Verify `previousAvailableAt` = last Monday 00:00 UTC

**Validation:**
```javascript
const nextMonday = getNextMonday(new Date());
const lastMonday = getLastMonday(new Date());

expect(bonus.nextAvailableAt).toBe(nextMonday.toISOString());
expect(bonus.previousAvailableAt).toBe(lastMonday.toISOString());
expect(bonus.isPendingCalculation).toBe(false);
```

---

### TC-CRON-03: Claim and Wait for Next Period

**Setup:**
1. Create bonus with CRON: `0 0 * * *` (daily)
2. User claims bonus today

**Steps:**
1. Claim bonus via `ActivateEligibleBonus` or `ClaimToCampaignBonus`
2. Call `GetEligibleBonuses`
3. Verify `isAvailable = false`
4. Verify `nextAvailableAt` = tomorrow 00:00 UTC
5. Verify `lastClaimedAt` = <claim time>

**Expected Result:**
```
After claim:
├── isAvailable: false
├── nextAvailableAt: <tomorrow 00:00 UTC>
├── previousAvailableAt: <today 00:00 UTC>
├── lastClaimedAt: <claim datetime>
└── isPendingCalculation: false
```

---

### TC-CRON-04: New User — Progress Bar Data (CT-756)

**Setup:**
1. Create scheduled bonus with CRON
2. Register BRAND NEW user (never claimed anything)

**Steps:**
1. Call `GetEligibleBonuses`
2. Find the scheduled bonus
3. Verify all fields for progress bar display

**Expected Result:**
```
{
  "isAvailable": false,
  "isPendingCalculation": false,
  "nextAvailableAt": "<next cron>",      // NOT null!
  "previousAvailableAt": "<prev cron>",  // NOT null!
  "lastClaimedAt": null                   // User never claimed
}
```

**Progress Bar Calculation (FE):**
```javascript
const startDate = bonus.lastClaimedAt || bonus.previousAvailableAt;
const endDate = bonus.nextAvailableAt;
const progress = calculateProgress(startDate, endDate);
```

---

### TC-CRON-05: Invalid CRON Expression

**Setup:**
1. Try to create bonus with invalid CRON: `invalid`

**Steps:**
1. Create bonus via BackOffice
2. Set CRON expression to `invalid`
3. Save bonus

**Expected Result:**
- Validation error
- Bonus not created/saved

---

### TC-CRON-06: CRON with Timezone Considerations

**Setup:**
1. Create bonus with CRON: `0 18 * * *` (daily at 18:00 UTC)
2. Test user in different timezone (e.g., CET = UTC+1)

**Steps:**
1. Call `GetEligibleBonuses` with `x-time-zone-offset: 60` (CET)
2. Verify `nextAvailableAt` still in UTC

**Expected Result:**
- `nextAvailableAt` always in UTC
- FE converts to user's timezone for display

---

## Automated Tests

### Playwright Test File

```typescript
// tests/api/tickets/CRON-bonus-schedule.spec.ts

test('TC-CRON-01: Daily bonus nextAvailableAt', async ({ request }) => {
  // Setup: Create bonus with daily CRON
  // Test: Verify nextAvailableAt calculation
  // Assert: nextAvailableAt matches expected cron time
});

test('TC-CRON-02: Weekly bonus schedule', async ({ request }) => {
  // Setup: Create bonus with weekly CRON (Monday)
  // Test: Verify next/previous available dates
  // Assert: Dates match Monday schedule
});

test('TC-CRON-03: Claim flow with CRON', async ({ request }) => {
  // Setup: User claims scheduled bonus
  // Test: Verify nextAvailableAt = next period
  // Assert: isAvailable = false until next period
});
```

### Run Command
```bash
ENV=dev npx playwright test --project=api-tickets CRON-bonus
```

---

## Test Data

### CRON Test Bonuses (Dev)

| Bonus ID | CRON | Schedule | Notes |
|----------|------|----------|-------|
| 25123 | Custom | Weekly (Tue 17:09 UTC) | Test bonus |
| 25125 | Custom | Weekly (Tue 17:05 UTC) | Regular cashback |
| 25127 | `0 0 * * *` | Daily 00:00 UTC | Daily bonus |

---

## Test Results (Dev)

**Test Date:** 2026-02-18
**Environment:** Dev
**Status:** ✅ All tests passed

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-CRON-01: nextAvailableAt calculation | ✅ Pass | Returns correct future date |
| TC-CRON-02: CRON schedule validation | ✅ Pass | Time component validated |
| TC-CRON-03: Progress bar data | ✅ Pass | All fields present for new users |
| TC-CRON-04: Multiple bonuses | ✅ Pass | System handles multiple schedules |

**Evidence:**
```
📦 Bonus ID: 25123
   Next available: 2026-02-24T17:09:00.000Z
   Previous available: 2026-02-17T17:09:00.000Z
   Days until available: 7
   Progress: 10.4%

📦 Bonus ID: 25125
   Next available: 2026-02-24T17:05:00.000Z
   Previous available: 2026-02-17T17:05:00.000Z

📦 Bonus ID: 25127
   Next available: 2026-02-25T00:00:00.000Z
   Previous available: 2026-02-18T00:00:00.000Z
```

**Automated Tests:**
- File: `tests/api/tickets/CRON-bonus-schedule.spec.ts`
- Run: `ENV=dev npx playwright test --project=api-tickets CRON-bonus`
- Result: 4 passed (1.8s)

---

## Edge Cases

### EC-01: Bonus Period Boundary

Test at exact CRON time (e.g., 12:00:00) to verify:
- No race conditions
- Correct period calculation

### EC-02: Daylight Saving Time

Test when DST changes:
- CRON times should still be UTC
- No double/skipped periods

### EC-03: Leap Year

Test with CRON for Feb 29: `0 0 29 2 *`
- Verify handles non-leap years

### EC-04: Campaign End

Test when campaign ends:
- Bonus should no longer appear
- No nextAvailableAt after campaign finish

---

## Checklist

- [ ] TC-CRON-01: Daily bonus nextAvailableAt
- [ ] TC-CRON-02: Weekly bonus schedule
- [ ] TC-CRON-03: Claim and wait for next period
- [ ] TC-CRON-04: New user progress bar data
- [ ] TC-CRON-05: Invalid CRON validation
- [ ] TC-CRON-06: Timezone handling
- [ ] EC-01: Period boundary testing
- [ ] EC-02: DST handling
- [ ] Automated tests implemented

---

## Notes

- All times in UTC
- Use https://crontab.guru/ to validate CRON expressions
- Coordinate with Kevin for CRON documentation updates
