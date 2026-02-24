# Test Plan: CT-756

## Ticket Summary

**CT-756:** [BE] Set NextAvailableAt for scheduled bonuses for users without bonus claim history

**Status:** Ready for testing
**Assignee:** Panda Sensei
**Priority:** Normal

### Problem
Currently, `nextAvailableAt` returns `null` (default datetime) when user has never claimed a bonus and has no `AvailableBonus` record. FE cannot show countdown timer for new users.

### Solution
Return actual next cron occurrence for `nextAvailableAt` even when user has never claimed.

**New field added:** `previousAvailableAt` — used to display progress bar for users without claim history.

---

## Related Tickets

| Ticket | Type | Status | Description |
|--------|------|--------|-------------|
| CT-767 | FE Task | Testing | Support `previousAvailableAt` field for regular promotions |
| CT-558 | Blocker | Done | — |
| CRYPTO-459 | Blocker | Testing | — |
| PLT-4337 | Dependency | Tested | — |

---

## Feature Deployment Status

| Environment | Status | previousAvailableAt field |
|-------------|--------|---------------------------|
| **Dev** | ✅ Deployed | Present |
| **QA** | ✅ Deployed | Present |
| **Prod** | ❌ Not deployed | Missing |

---

## Test Environment

- **Dev:** https://minebit-casino.dev.sofon.one/bonuses
- **QA:** https://minebit-casino.qa.sofon.one/bonuses
- **API Dev:** https://websitewebapi.dev.sofon.one
- **API QA:** https://websitewebapi.qa.sofon.one

---

## API Endpoint Details

### GetEligibleBonuses

**Method:** `POST`
**Path:** `/{partnerId}/api/v3/Bonus/GetEligibleBonuses`

**Swagger (QA):** https://websitewebapi.qa.sofon.one/swagger/index.html

**Response Schema (EligibleBonusSchemaDto):**
```json
{
  "required": [
    "availableUntil",
    "campaignFinishTime", 
    "hasDepositTrigger",
    "hasFreeSpins",
    "hasWagering",
    "id",
    "isAvailable",
    "isPendingCalculation"
  ],
  "properties": {
    "id": { "type": "integer" },
    "isAvailable": { "type": "boolean" },
    "hasDepositTrigger": { "type": "boolean" },
    "hasFreeSpins": { "type": "boolean" },
    "hasWagering": { "type": "boolean" },
    "isPendingCalculation": { "type": "boolean" },
    "bonusActivationId": { "type": "integer", "nullable": true },
    "availableUntil": { "type": "string", "format": "date-time", "nullable": true },
    "campaignFinishTime": { "type": "string", "format": "date-time", "nullable": true },
    "previousAvailableAt": { "type": "string", "format": "date-time", "nullable": true },
    "nextAvailableAt": { "type": "string", "format": "date-time", "nullable": true },
    "lastClaimedAt": { "type": "string", "format": "date-time", "nullable": true },
    "amount": { "type": "number", "format": "double", "nullable": true }
  }
}
```

**CT-756 New Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `nextAvailableAt` | datetime | Next cron occurrence for scheduled bonuses |
| `previousAvailableAt` | datetime | Previous cron occurrence (for progress bar) |
| `lastClaimedAt` | datetime \| null | When user last claimed this bonus |

---

## Test Data Setup

### Bonus Configuration (via BackOffice)
1. Create Regular Cashback Bonus with cron schedule (e.g., daily at 12:00 UTC)
2. Bonus should have:
   - `IsScheduled: true`
   - Cron expression configured
   - Active status

### Test Users
1. **New user** — never claimed any bonus, no AvailableBonus record
2. **User with available bonus** — has AvailableBonus from Smartico
3. **User who claimed in current period** — claimed bonus, waiting for next cron
4. **User who claimed in previous period** — Smartico pending
5. **User who claimed in previous period** — Smartico sent amount

---

## Test Cases

### TC-01: New user without claim history — nextAvailableAt returns cron

**Preconditions:**
- User never claimed any bonus
- No AvailableBonus record exists

**Steps:**
1. Register new user via API
2. Call `GET /bonus/GetEligibleBonuses`
3. Verify response for the scheduled bonus

**Expected Result:**
```
{
  "nextAvailableAt": "<next cron datetime>", // NOT null/0001-01-01
  "isPendingCalculation": false,
  "isAvailable": false,
  "previousAvailableAt": "<previous cron datetime>",
  "lastClaimedAt": null
}
```

**API Endpoint:**
```
GET /api/v3/bonus/GetEligibleBonuses
```

---

### TC-02: New user with available bonus — can claim immediately

**Preconditions:**
- User never claimed any bonus
- AvailableBonus exists (Smartico sent)

**Steps:**
1. Create user with available bonus (via Smartico or BO)
2. Call `GET /bonus/GetEligibleBonuses`
3. Verify response

**Expected Result:**
```
{
  "nextAvailableAt": null, // or 0001-01-01
  "isPendingCalculation": false,
  "isAvailable": true
}
```

---

### TC-03: User claimed in current period — shows next cron

**Preconditions:**
- User claimed bonus in current cron period
- Next cron hasn't occurred yet

**Steps:**
1. Claim bonus for test user
2. Call `GET /bonus/GetEligibleBonuses`
3. Verify response

**Expected Result:**
```
{
  "nextAvailableAt": "<next cron datetime>",
  "isPendingCalculation": false,
  "isAvailable": false,
  "lastClaimedAt": "<claim datetime>"
}
```

---

### TC-04: Progress bar display for new users (FE integration)

**Preconditions:**
- CT-767 deployed (FE changes)
- User never claimed bonus
- No AvailableBonus record

**Steps:**
1. Login as new user on frontend
2. Navigate to Bonuses page
3. Verify progress bar is displayed for scheduled bonus

**Expected Result:**
- Progress bar shown with:
  - Start: `previousAvailableAt` (or fallback)
  - End: `nextAvailableAt`
- Timer countdown visible

---

### TC-05: Scenario Matrix Validation

| Scenario | nextAvailableAt | isPendingCalculation | isAvailable |
|----------|-----------------|---------------------|-------------|
| Never claimed + no available bonus | `<next cron>` | `false` | `false` |
| Never claimed + has available bonus | `null` | `false` | `true` |
| Claimed in current period | `<next cron>` | `false` | `false` |
| Claimed in previous period, Smartico pending | `null` | `true` | `false` |
| Claimed in previous period, Smartico sent | `null` | `false` | `true` |

---

### TC-06: previousAvailableAt fallback logic

**Preconditions:**
- User never claimed bonus
- `lastClaimedAt` is null

**Steps:**
1. Call `GET /bonus/GetEligibleBonuses`
2. Verify `previousAvailableAt` is populated

**Expected Result:**
- `previousAvailableAt` contains valid datetime
- Frontend can use: `previousDate = lastClaimedAt || previousAvailableAt`

---

## API Test Examples

### Get Eligible Bonuses
```bash
curl -X GET "https://websitewebapi.dev.sofon.one/api/v3/bonus/GetEligibleBonuses" \
  -H "Authorization: Bearer <session_token>" \
  -H "website-locale: en" \
  -H "x-time-zone-offset: -60"
```

### Create Test User (GraphQL)
```graphql
mutation PlayerRegisterUniversal {
  playerRegisterUniversal(
    input: {
      email: "test-ct756-$(date +%s)@nextcode.tech"
      password: "Qweasd123!"
      partnerId: 5
    }
  ) {
    player {
      id
      email
    }
    token
  }
}
```

---

## Notes from Comments

- Kevin tested on Dev with Bonus ID 25125
- For new user without bonus activation:
  - `IsAvailable: false`
  - Has Previous and Next available dates
  - `LastClaimedAt: null`
  - `IsPendingCalculation: false`

---

---

## Automated Tests

**Playwright Test File:** `tests/api/tickets/CT-756-next-available-at.spec.ts`

**Run Command:**
```bash
cd /Users/ihorsolopii/Documents/minebit-e2e-playwright
npx playwright test --project=api-tickets CT-756
```

**Test Cases:**
| TC | Description | Status |
|----|-------------|--------|
| TC-01 | New user without claim history — nextAvailableAt returns cron datetime | Implemented |
| TC-02 | Validate response schema for EligibleBonusSchemaDto | Implemented |
| TC-03 | Scenario matrix — validate different user states | Implemented |

---

## Definition of Done

- [ ] All test cases pass
- [ ] Scenario matrix validated
- [ ] FE progress bar works for new users
- [ ] No regression for existing claim flow
- [ ] API response matches expected schema
- [ ] Tested on Dev and QA environments
