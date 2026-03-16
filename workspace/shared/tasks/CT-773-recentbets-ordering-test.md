# CT-773: RecentBets Ordering Fix — Test Plan

**Jira:** https://next-t-code.atlassian.net/browse/CT-773
**Status:** Ready for testing
**Type:** Backend
**Priority:** Normal
**Environment:** QA
**Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/110

---

## 📋 Objective

Валідація зміни логіки повернення ставок з кешу: тепер повинні повертатися найновіші ставки (newest → oldest), а не найстаріші з 50 закешованих.

---

## 🧪 Test Scenarios

### 1. Basic Ordering — Newest First (Happy Path)

**Preconditions:**
- Partner configured for testing
- Test environment: QA (https://alov-casino.qa.sofon.one/en/live-bets-new)

**Steps:**
1. Place 20 bets with intentional time gaps (1-2 seconds between each)
2. Wait for cache to populate (cache stores 50 max bets)
3. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=10`
4. Verify response structure:
   ```json
   {
     "data": {
       "bets": [
         {
           "clientName": "string",
           "clientId": 12345,
           "clientIdWithMask": "string",
           "betAmount": 100.50,
           "winAmount": 250.75,
           "multiplier": 2.5,
           "currencyId": "USD",
           "gameId": 789,
           "isWin": true,
           "timeAgo": "string"
         }
       ]
     },
     "success": true
   }
   ```

**Expected Result:**
- ✅ Array[0] contains the MOST RECENT bet
- ✅ Array[9] contains the OLDEST of the 10 returned
- ✅ Ordering is newest → oldest (timeAgo descending or actual timestamp ascending)

---

### 2. Consistency After Multiple Batches

**Preconditions:**
- Empty cache at start

**Steps:**
1. Place 15 bets (batch_1) → Cache: 15/50
2. Call GetRecentBets → Should return batch_1 (newest to oldest)
3. Place 15 more bets (batch_2) → Cache: 30/50
4. Call GetRecentBets → Should return batch_2 + batch_1 (newest 15)
5. Place 15 more bets (batch_3) → Cache: 45/50
6. Call GetRecentBets → Should return batch_3 + batch_2 (newest 15)
7. Place 15 more bets (batch_4) → Cache: 60/50 (10 oldest pushed out)
8. Call GetRecentBets → Should return batch_4 + batch_3 + 5 from batch_2

**Expected Result:**
- ✅ After each step, the response contains the 15 NEWEST bets from cache
- ✅ Oldest bets are pushed out when cache exceeds 50
- ✅ Always newest → oldest ordering

---

### 3. BetsCount Parameter Validation

**Steps:**
1. Place 30 bets
2. Call with `betsCount=5` → Should return 5 newest bets
3. Call with `betsCount=10` → Should return 10 newest bets
4. Call with `betsCount=50` → Should return all cached bets
5. Call with `betsCount=100` → Should return max available (up to 50)
6. Call with `betsCount=0` → Should return empty array or error
7. Call with `betsCount=-5` → Should return empty array or error

**Expected Result:**
- ✅ Respects betsCount parameter
- ✅ Never returns more than cache capacity (50)
- ✅ Handles edge cases (0, negative, >50) gracefully

---

### 4. Empty Cache Scenario

**Preconditions:**
- No bets placed yet (empty cache)

**Steps:**
1. Call GetRecentBets with betsCount=10

**Expected Result:**
- ✅ Returns empty bets array: `{"data": {"bets": []}, "success": true}`
- ✅ No errors

---

### 5. Cache Boundary Test

**Preconditions:**
- Empty cache at start

**Steps:**
1. Place exactly 50 bets
2. Call GetRecentBets with betsCount=50
3. Verify all 50 bets are returned, newest → oldest
4. Place 1 more bet (51 total)
5. Call GetRecentBets with betsCount=50
6. Verify the OLDEST bet (from step 1) is NOT in response
7. Verify the newest bet (from step 4) IS in response at index 0

**Expected Result:**
- ✅ Oldest bet pushed out when cache exceeds 50
- ✅ Newest bet appears first
- ✅ Cache maintains exactly 50 most recent bets

---

### 6. Regression — Other Product Endpoints

**Steps:**
1. Call `GET /{partnerId}/api/v3/Product/GetWinners` (if exists)
2. Verify response structure is unchanged
3. Call any other Product endpoints

**Expected Result:**
- ✅ No changes to other endpoints
- ✅ Response structures identical
- ✅ No new errors introduced

---

### 7. Response Structure Validation

**Preconditions:**
- Bets already placed

**Steps:**
1. Call GetRecentBets
2. Validate each RecentBetOutput object:
   - `clientName` (nullable string)
   - `clientId` (int)
   - `clientIdWithMask` (nullable string)
   - `betAmount` (decimal)
   - `winAmount` (decimal)
   - `multiplier` (decimal)
   - `currencyId` (string)
   - `gameId` (int)
   - `isWin` (boolean)
   - `timeAgo` (nullable string)

**Expected Result:**
- ✅ All fields present with correct types
- ✅ No new fields added
- ✅ No fields removed

---

### 8. Ordering via timeAgo Field

**Preconditions:**
- Bets placed with different timestamps

**Steps:**
1. Call GetRecentBets
2. Verify `timeAgo` values are consistent:
   - Array[0] should have smallest timeAgo (most recent)
   - Array[last] should have largest timeAgo (oldest)
3. Note: timeAgo format may vary ("5 seconds ago", "2 minutes ago")

**Expected Result:**
- ✅ timeAgo values indicate newest → oldest ordering
- ✅ Display order matches actual timestamp order

---

### 9. GET vs POST Method Equivalence

**Steps:**
1. Call `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=10`
2. Call `POST /{partnerId}/api/v3/Product/GetRecentBets` with betsCount=10 in body
3. Compare responses

**Expected Result:**
- ✅ Both methods return identical data
- ✅ Ordering is consistent

---

### 10. Real-Time Updates

**Preconditions:**
- Bets already placed

**Steps:**
1. Call GetRecentBets → Record bet at index 0
2. Place 1 new bet
3. Wait 1-2 seconds
4. Call GetRecentBets again
5. Verify the new bet appears at index 0
6. Verify previous index 0 is now at index 1

**Expected Result:**
- ✅ New bet appears first after placement
- ✅ Older bets shift down in the array

---

## 🔧 Testing Approach

### Option 1: API Testing via Swagger/Curl (Recommended)
```bash
# Example curl request
curl -X GET "https://{partnerId}.qa.sofon.one/api/v3/Product/GetRecentBets?betsCount=10"
```
- Execute GetRecentBets endpoint directly
- Verify ordering by timestamps
- Test with different betsCount values

### Option 2: UI Testing (QA Environment)
- Navigate to https://alov-casino.qa.sofon.one/en/live-bets-new
- Place bets and observe "Recent Bets" section
- Verify newest bets appear first

### Option 3: Automated Script
- Create Python script to place N bets
- Call GetRecentBets endpoint
- Validate ordering programmatically
- Compare timestamps

---

## 🗂️ Test Data Requirements

- **Partner ID:** Test partner with RecentBets enabled
- **Game ID:** Any live game for placing bets
- **Test User:** Valid player account with balance
- **Bet Amounts:** Small amounts for testing (e.g., $1-$5)
- **Time Gaps:** 1-2 seconds between bets for clear ordering

---

## 📊 Evidence

Save evidence to: `shared/test-results/CT-773/`
- API request/response JSON
- Screenshots of UI (if using Option 2)
- Ordering validation results (timestamp comparison)
- Cache behavior logs

---

## ⚠️ Notes

- **No API contract changes** — Same DTOs and endpoints
- **No database changes** — Isolated to in-memory cache sorting
- **Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/110
- **Linked issues:** CRYPTO-107, CRYPTO-86, PLT-4553
- **QA Environment:** https://alov-casino.qa.sofon.one/en/live-bets-new
- **Comment from JIRA:** "missing sorting by time from newest - to oldest"

---

## 📌 Swagger Endpoints to Test

### Get Recent Bets
- `GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount={count}`
- `POST /{partnerId}/api/v3/Product/GetRecentBets`

**Response Structure:**
```json
{
  "data": {
    "bets": [
      {
        "clientName": "string (nullable)",
        "clientId": 12345,
        "clientIdWithMask": "string (nullable)",
        "betAmount": 100.50,
        "winAmount": 250.75,
        "multiplier": 2.5,
        "currencyId": "USD",
        "gameId": 789,
        "isWin": true,
        "timeAgo": "string (nullable)"
      }
    ]
  },
  "success": true,
  "message": null,
  "errors": null
}
```

**Key Test Focus:**
- Ordering: newest → oldest (array[0] = most recent)
- betsCount parameter works correctly
- Cache boundary behavior (50 max bets)
- No regression on other endpoints

---

## 🎯 Acceptance Criteria

- ✅ Newest bet appears first in RecentBets response
- ✅ Ordering is consistent: newest → oldest
- ✅ betsCount parameter works correctly
- ✅ No regression on other Product endpoints
- ✅ Same response structure as before (no contract changes)
- ✅ Cache capacity limit of 50 bets respected
- ✅ Oldest bets pushed out when cache exceeds 50
- ✅ No new status codes or errors introduced
