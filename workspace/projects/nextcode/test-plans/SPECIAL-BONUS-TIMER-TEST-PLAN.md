# Test Plan: Special Bonus Timer Behavior

## Objective

Verify that `FinishTime` expiration:
1. Makes bonus unavailable for the specific user
2. Keeps bonus **ACTIVE** in BackOffice
3. Allows new users to receive bonus with fresh timer

---

## Test Scenarios

### Scenario 1: FinishTime Expiration — User Cannot Claim

**What to verify:**
After `FinishTime` passes, bonus becomes unavailable for the user who received it.

**API Test:**
```
1. Create special bonus with short FinishTime (e.g., 5 minutes from now)
2. Assign bonus to test user via BO API
3. Call GetEligibleBonuses — verify bonus is visible and isAvailable = true
4. Wait for FinishTime to expire
5. Call GetEligibleBonuses again — verify bonus is NOT available or isAvailable = false
```

**API Endpoints:**
- `POST /api/v3/Bonus/GetEligibleBonuses` — check availability
- BO API — assign bonus to user

**Expected Result:**
- Before expiration: `isAvailable: true`
- After expiration: `isAvailable: false` OR bonus not in list

**FE Validation Needed?** 
- ⚠️ Partially — FE should show expired state, but core logic is backend

---

### Scenario 2: FinishTime Expiration — Bonus Remains ACTIVE in BO

**What to verify:**
After `FinishTime` passes, bonus remains active in BackOffice and can be assigned to new users.

**API Test:**
```
1. Create special bonus with short FinishTime
2. Note the bonus ID and IsActive status in BO
3. Assign to User A
4. Wait for FinishTime to expire
5. Check BO API — verify bonus IsActive = true
6. Verify bonus appears in active bonuses list in BO
```

**BO API Endpoints:**
- `GET /api/Bonus/{id}` — check bonus status
- `GET /api/Bonus?isActive=true` — list active bonuses

**Expected Result:**
- `IsActive: true` in BO
- Bonus appears in active list
- `FinishTime` has no effect on `IsActive` field

**FE Validation Needed?** 
- ❌ No — this is purely backend/BO validation

---

### Scenario 3: New User Gets Fresh Timer After Previous User's Expiration

**What to verify:**
After one user's timer expires, new user can receive the same bonus with a fresh timer.

**API Test:**
```
1. Create special bonus with FinishTime = 10 minutes from creation
2. Assign to User A via BO
3. Wait for User A's FinishTime to expire
4. Create new User B (or use existing)
5. Assign same bonus to User B via BO
6. Call GetEligibleBonuses for User B
7. Verify:
   - Bonus is visible
   - isAvailable = true
   - nextAvailableAt / timer shows FULL duration (not expired)
```

**API Endpoints:**
- `POST /api/v3/Bonus/GetEligibleBonuses` — check User B's bonus
- BO API — assign bonus to User B

**Expected Result:**
- User B sees bonus as available
- Timer for User B starts from beginning (not affected by User A's expiration)

**FE Validation Needed?** 
- ⚠️ Partially — FE timer display, but backend provides the data

---

### Scenario 4: AvailableForSpending Timer — Relative Time Calculation

**What to verify:**
`AvailableForSpending` is relative to user's activation time, not bonus creation time.

**API Test:**
```
1. Create special bonus with AvailableForSpending = 24 hours
2. Assign to User A
3. User A activates (claims) the bonus
4. Record activation time T1
5. Check timer/availability at T1 + 12 hours — should be available
6. Check timer/availability at T1 + 24 hours — should be expired
```

**Expected Result:**
- Timer countdown starts from user's activation moment
- Each user gets their own timer based on their activation

**FE Validation Needed?**
- ⚠️ Yes — timer countdown display on FE

---

### Scenario 5: Both Timers — Interaction Test

**What to verify:**
Both timers work independently:
- `FinishTime` (activation deadline) — absolute
- `AvailableForSpending` (wagering deadline) — relative to activation

**API Test:**
```
1. Create bonus:
   - FinishTime = 7 days from now
   - AvailableForSpending = 3 days
2. Assign to User A
3. User A activates on Day 5
4. Check: User A should have 3 days for wagering (not affected by remaining FinishTime)
```

**Expected Result:**
- `FinishTime` = last moment to activate
- `AvailableForSpending` = time to wager AFTER activation
- Timers are independent

**FE Validation Needed?**
- ✅ Yes — two different timer displays on FE

---

## API vs FE Testing Matrix

| Scenario | API Test | FE Test | Notes |
|----------|----------|---------|-------|
| 1. User cannot claim after expiration | ✅ Full | ⚠️ Partial | API validates logic, FE shows UI state |
| 2. Bonus remains active in BO | ✅ Full | ❌ Not needed | Pure backend validation |
| 3. New user gets fresh timer | ✅ Full | ⚠️ Partial | API validates data, FE displays timer |
| 4. AvailableForSpending relative time | ✅ Full | ✅ Full | Timer countdown needs FE validation |
| 5. Both timers interaction | ✅ Full | ✅ Full | Complex scenario needs FE validation |

---

## Required Test Data Setup

### BO Configuration for Test Bonus

```json
{
  "name": "Test Special Bonus - Timer Validation",
  "type": "Special",
  "isActive": true,
  "finishTime": "<NOW + 10 minutes>",
  "availableForSpending": 1440,  // 24 hours in minutes
  "isScheduled": false
}
```

### Test Users
- User A — receives bonus, timer expires
- User B — receives same bonus after User A's expiration
- User C — activates on different day (for relative timer test)

---

## API Endpoints Summary

### Website API (User-facing)
| Endpoint | Purpose |
|----------|---------|
| `POST /api/v3/Bonus/GetEligibleBonuses` | Check bonus availability |
| `POST /api/v3/Bonus/ActivateEligibleBonus/{id}` | Activate/claim bonus |
| `POST /api/v3/Bonus/GetActiveBonuses` | Check active bonuses |

### BackOffice API (Admin)
| Endpoint | Purpose |
|----------|---------|
| `GET /api/Bonus/{id}` | Check bonus status |
| `POST /api/Bonus` | Create bonus |
| `POST /api/Bonus/AssignToUser` | Assign bonus to user |
| `GET /api/Bonus?isActive=true` | List active bonuses |

---

## Test Execution Plan

### Phase 1: API Only Tests (Can do remotely)
1. ✅ Scenario 2 — Bonus remains active in BO
2. ✅ Scenario 3 — New user gets fresh timer

### Phase 2: API + FE Tests (Need FE access)
1. Scenario 1 — User cannot claim after expiration
2. Scenario 4 — AvailableForSpending relative time
3. Scenario 5 — Both timers interaction

---

## Defect Report Template

If testing reveals the bug exists:

```
**Summary:** Special bonus becomes inactive in BO after FinishTime expiration

**Steps to Reproduce:**
1. Create special bonus with FinishTime = 10 minutes
2. Assign to User A
3. Wait for FinishTime to expire
4. Check bonus status in BO

**Expected Result:** 
- Bonus IsActive = true in BO
- Can assign to new users

**Actual Result:**
- Bonus IsActive = false in BO
- Cannot assign to new users

**Impact:**
- Long-running campaigns break
- Cannot reuse special bonuses
```

---

## Notes

- Coordinate with Mads for BO API access
- May need to check existing brand (transfer source) for reference behavior
- Document expects/proposed fields for relative vs absolute time bonuses
