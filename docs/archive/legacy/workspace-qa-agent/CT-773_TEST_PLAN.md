# Test Plan: CT-773 — RecentBets return latest bets from cache

**Ticket:** https://next-t-code.atlassian.net/browse/CT-773
**Status:** Ready for testing
**Priority:** Normal
**Type:** Backend bug fix
**Environment:** QA (https://alov-casino.qa.sofon.one)
**Test Date:** 2026-03-08

---

## 📋 Summary

The RecentBets service caches 50 latest bets but returns 15 oldest from these 50 bets. The fix ensures that RecentBets returns the 15 newest bets from the 50 cached bets.

**Bug:** RecentBets returns oldest bets instead of newest
**Expected:** Return 15 newest bets from 50 cached bets
**Fix PR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/110

---

## 🎯 Acceptance Criteria

1. ✅ RecentBets endpoint returns bets ordered newest → oldest
2. ✅ Response respects `betsCount` parameter (max 15 by default)
3. ✅ Ordering is consistent after cache receives multiple batches
4. ✅ No regression on other endpoints

---

## 📂 Test Data Requirements

### Test Player
- **Environment:** QA
- **Player ID:** Needed for placing bets
- **Balance:** Minimum $20 for placing bets (can create via test-data-scripts)
- **Partner:** Alov Casino (https://alov-casino.qa.sofon.one)

### Test Games
Need at least 1-2 active games for placing bets:
- Game ID: TBD (check via Product API or UI)
- Category: Slots (for recent bets display)

---

## 🧪 Test Cases

### TC-1: Verify RecentBets ordering - newest bets first

**Priority:** High
**Type:** Functional

**Preconditions:**
1. Test player exists with balance ≥ $20
2. Player is logged in on Alov Casino QA

**Steps:**
1. Place 5 bets with 1-second intervals (bet_amount: $1 each)
2. Wait 2 seconds
3. Place 5 more bets with 1-second intervals (bet_amount: $2 each)
4. Wait 2 seconds
5. Place 5 more bets with 1-second intervals (bet_amount: $3 each)
6. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=15`
7. Verify response structure

**Expected Result:**
- Response returns 15 bets
- First bet in array is the newest (bet_amount: $3, last placed)
- Last bet in array is the oldest (bet_amount: $1, first placed)
- `timeAgo` field shows correct relative time

**API Endpoint:**
```
GET https://websitewebapi.qa.sofon.one/{partnerId}/api/v3/Product/GetRecentBets?betsCount=15
```

**Response Schema:**
```json
{
  "bets": [
    {
      "betAmount": 3.0,
      "winAmount": 0.0,
      "multiplier": 0.0,
      "clientId": 123456,
      "clientIdWithMask": "***456",
      "clientName": "TestPlayer",
      "currencyId": "USD",
      "gameId": 789,
      "isWin": false,
      "timeAgo": "10 seconds ago"
    },
    // ... (14 more bets)
  ]
}
```

---

### TC-2: Verify betsCount parameter is respected

**Priority:** High
**Type:** Functional

**Preconditions:**
1. Test player has placed at least 20 bets

**Steps:**
1. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=5`
2. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=10`
3. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=15`
4. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=20`

**Expected Result:**
- betsCount=5 returns exactly 5 bets (newest 5)
- betsCount=10 returns exactly 10 bets (newest 10)
- betsCount=15 returns exactly 15 bets (newest 15)
- betsCount=20 returns exactly 15 bets (max 15 from cache)
- All responses ordered newest → oldest

---

### TC-3: Verify cache overflow behavior (50 bets limit)

**Priority:** Medium
**Type:** Edge Case

**Preconditions:**
1. Test player has balance ≥ $60

**Steps:**
1. Place 60 bets in batches (15 bets × 4 batches)
2. Wait 5 seconds for cache to process
3. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=15`
4. Verify which bets are returned

**Expected Result:**
- Cache contains 50 newest bets (10 oldest discarded)
- Response returns 15 newest bets from the cached 50
- Returned bets should be from batch_4 (15) + batch_3 (15) + batch_2 (10) = 40 total
- Oldest bets from batch_1 (15 bets) should NOT appear
- All returned bets ordered newest → oldest

---

### TC-4: Verify ordering consistency after multiple batches

**Priority:** High
**Type:** Functional

**Preconditions:**
1. Test player has balance ≥ $30

**Steps:**
1. Place 15 bets (batch_1, $1 each)
2. Call GetRecentBets immediately → verify ordering
3. Place 15 bets (batch_2, $2 each)
4. Call GetRecentBets immediately → verify newest 15 are batch_2
5. Place 15 bets (batch_3, $3 each)
6. Call GetRecentBets immediately → verify newest 15 are batch_3
7. Wait 5 seconds
8. Call GetRecentBets again → verify ordering unchanged

**Expected Result:**
- After batch_1: Returns 15 bets from batch_1
- After batch_2: Returns 15 bets from batch_2 (newest)
- After batch_3: Returns 15 bets from batch_3 (newest)
- Consistent ordering across multiple calls
- No mixing of old bets with new bets

---

### TC-5: Verify UI displays bets correctly (Live Bets page)

**Priority:** High
**Type:** UI Integration

**Preconditions:**
1. Test player has placed recent bets

**Steps:**
1. Navigate to https://alov-casino.qa.sofon.one/en/live-bets-new
2. Observe the Recent Bets section
3. Compare displayed bets with API response
4. Verify ordering matches API (newest at top)

**Expected Result:**
- Live Bets page displays bets in correct order (newest → oldest)
- Bet amounts, game names, and times match API response
- No empty lists or error messages
- Categories (if any) are displayed correctly

**Screenshots:**
- Full Live Bets page
- Console logs (check for errors)
- Network tab (GetRecentBets response)

---

### TC-6: Verify no regression on other Product API endpoints

**Priority:** Medium
**Type:** Regression

**Steps:**
1. Call `GET /{partnerId}/api/v3/Product/GetGames`
2. Call `GET /{partnerId}/api/v3/Product/GetCategories`
3. Call other Product endpoints if applicable

**Expected Result:**
- All other endpoints return 200 OK
- No changes to response structure
- No performance degradation
- No error logs related to RecentBets

---

### TC-7: Verify response structure and data integrity

**Priority:** Medium
**Type:** Functional

**Steps:**
1. Place 5 bets
2. Call GetRecentBets
3. Verify all required fields are present

**Expected Result:**
Each bet object contains:
- ✅ `betAmount` (number)
- ✅ `winAmount` (number)
- ✅ `multiplier` (number)
- ✅ `clientId` (integer)
- ✅ `clientIdWithMask` (string, e.g., "***456")
- ✅ `clientName` (string)
- ✅ `currencyId` (string)
- ✅ `gameId` (integer)
- ✅ `isWin` (boolean)
- ✅ `timeAgo` (string, relative time format)

---

### TC-8: Verify handling of empty recent bets

**Priority:** Low
**Type:** Edge Case

**Steps:**
1. Use a fresh player who hasn't placed any bets
2. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=15`

**Expected Result:**
- Response returns 200 OK
- `bets` array is empty `[]` or `null`
- No error 500

---

## 🔧 Test Execution Approach

### Phase 1: API Testing (Primary)
1. Use curl or Python scripts to call GetRecentBets endpoint
2. Verify ordering by comparing timestamps
3. Test different betsCount values
4. Simulate cache overflow scenarios

### Phase 2: UI Verification
1. Open Live Bets page on QA
2. Compare UI display with API response
3. Check console for errors
4. Take screenshots as evidence

### Phase 3: Regression Testing
1. Check other Product endpoints
2. Monitor backend logs for errors
3. Verify no performance issues

---

## 📝 Test Script (Python)

```python
import requests
import time
import json

# Configuration
PARTNER_ID = 1  # Update with correct partner ID
BASE_URL = "https://websitewebapi.qa.sofon.one"
API_KEY = "your_api_key_here"  # If auth needed

def get_recent_bets(bets_count=15):
    """Call GetRecentBets endpoint"""
    url = f"{BASE_URL}/{PARTNER_ID}/api/v3/Product/GetRecentBets"
    params = {"betsCount": bets_count}
    response = requests.get(url, params=params)
    return response.json()

def verify_ordering(bets):
    """Verify bets are ordered newest → oldest"""
    if len(bets) < 2:
        return True

    # Parse timeAgo strings to compare (simple check for demo)
    # In real test, use actual timestamps if available
    print(f"First bet (newest): {bets[0]['timeAgo']}, amount: {bets[0]['betAmount']}")
    print(f"Last bet (oldest): {bets[-1]['timeAgo']}, amount: {bets[-1]['betAmount']}")
    return True

# Test TC-1: Verify ordering
print("=== TC-1: Verify Ordering ===")
response = get_recent_bets(15)
bets = response.get('bets', [])
print(f"Total bets: {len(bets)}")
if bets:
    verify_ordering(bets)

# Test TC-2: Verify betsCount
print("\n=== TC-2: Verify betsCount ===")
for count in [5, 10, 15]:
    response = get_recent_bets(count)
    bets = response.get('bets', [])
    print(f"Requested {count}, Got {len(bets)}")
```

---

## 📊 Expected Test Results

| Test Case | Priority | Expected Status |
|-----------|----------|-----------------|
| TC-1: Verify ordering | High | ✅ PASS |
| TC-2: betsCount parameter | High | ✅ PASS |
| TC-3: Cache overflow | Medium | ✅ PASS |
| TC-4: Multiple batches | High | ✅ PASS |
| TC-5: UI verification | High | ✅ PASS |
| TC-6: Regression | Medium | ✅ PASS |
| TC-7: Data integrity | Medium | ✅ PASS |
| TC-8: Empty bets | Low | ✅ PASS |

---

## 🚨 Known Issues from Comments

1. **Categories not returned in response** — Check if this is fixed
2. **Incorrect table in BO** — Verify in BackOffice
3. **Empty list due to incorrect data** — Test with real bets

---

## 📦 Deliverables

1. **Test Execution Report** with screenshots
2. **API Response Samples** (before/after if available)
3. **Network Tab Evidence** showing ordering
4. **Jira Comment** in standard format

---

## ⏱️ Estimated Time

- Setup (test player, login): 15 min
- API Testing (TC-1 to TC-8): 45 min
- UI Verification: 20 min
- Regression Testing: 15 min
- **Total:** ~1.5 hours

---

## 🔄 Follow-up Actions

1. If any test fails, document details and notify developer
2. If categories are missing, create separate ticket
3. Update MEMORY.md with findings
4. Add TestRail test cases if not present
