# API Context: CT-773 - RecentBets Ordering Fix

## Summary
Backend logic change to return newest bets instead of oldest from cached data. No API contract changes - same DTOs and endpoints.

## 1. Get Recent Bets
`GET /{partnerId}/api/v3/Product/GetRecentBets`
`POST /{partnerId}/api/v3/Product/GetRecentBets`

**Auth:** Requires partner authentication.

**Parameters:**
- `partnerId` (path, required, int32): The Id of the partner
- `betsCount` (query, optional, int32): Number of bets to return

**Response (200 OK):**
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
        "timeAgo": "string (nullable)"  // Used for ordering display
      }
    ]
  },
  "success": true,
  "message": null,
  "errors": null
}
```

**Responses:**
- `200 OK`: Returns array of recent bets ordered newest → oldest
- `500 Internal Server Error`: Server error

**Status Codes:**
- All existing codes remain the same

---

## 2. Get Winners (Reference)
`GET /{partnerId}/api/v3/Product/GetWinners`
`POST /{partnerId}/api/v3/Product/GetWinners`

**Note:** The JIRA ticket mentions "recent bets/wins" but GetWinners endpoint exists with different schema (no timestamp field). Testing should focus on GetRecentBets.

**Parameters:**
- `partnerId` (path, required, int32): The Id of the partner
- `winnersCount` (query, optional, int32): Number of winners to return
- `fromDate` (query, optional, date-time): Filter winners from this date

---

## Testing Advice

### CT-773 Specific Requirements

1. **Primary Focus: GetRecentBets Ordering**
   - The backend cache now returns 15 NEWEST bets instead of 15 OLDEST from the cached 50 bets
   - The `timeAgo` field may be used for display ordering
   - Verify ordering is newest → oldest (most recent bet appears first in the array)

2. **Test Scenarios:**
   - Place several bets with different timestamps
   - Call GetRecentBets endpoint with betsCount parameter
   - Verify newest bet appears first in the response array
   - Verify ordering is consistent after cache receives multiple batches of events
   - Verify the list still respects takeCount parameter (e.g., requesting 10 returns max 10 items)

3. **Cache Behavior:**
   - Cache stores 50 most recent bets
   - When new bets come in, oldest are pushed out
   - Response should always be from newest to oldest, regardless of cache state

4. **Regression Testing:**
   - No API contract changes - verify response structure is identical
   - Same DTOs: `GetRecentBetsOutput` and `RecentBetOutput`
   - Verify no errors in other Product endpoints
   - Change is isolated to in-memory cache sorting

### Example Test Steps

1. **Setup:** Use a test partnerId and ensure partner configuration allows bets

2. **Create Test Data:**
   - Place 20+ bets with intentional time gaps (e.g., 1 second between each)
   - Wait for cache to populate (cache has 50-bet capacity)

3. **Test with betsCount:**
   ```bash
   GET /{partnerId}/api/v3/Product/GetRecentBets?betsCount=10
   ```
   - Expect: 10 bets, array[0] = most recent, array[9] = oldest

4. **Verify Ordering:**
   - Check that bet at index 0 has latest timestamp
   - Check that bet at last index has oldest timestamp

5. **Cache Boundary Test:**
   - Place 60 total bets (10 beyond cache capacity)
   - Request 15 bets
   - Verify the 15 newest are returned (oldest 10 from original set should be gone)

6. **Empty/Edge Cases:**
   - Test with no bets (expect empty array)
   - Test with betsCount = 0 or negative
   - Test with betsCount > 50 (should return max available, up to 50)

### Acceptance Criteria

- ✅ Newest bet appears first in RecentBets response
- ✅ Ordering is consistent: newest → oldest
- ✅ betsCount parameter works correctly
- ✅ No regression on other endpoints
- ✅ Same response structure as before
- ✅ No new status codes or errors

---

## Related JIRA Info
- **Ticket:** CT-773 - "[BE] RecentBets return latest bets from cache"
- **Status:** Ready for testing
- **Priority:** Normal
- **Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/110
- **QA Environment:** https://alov-casino.qa.sofon.one/en/live-bets-new
- **Linked Issues:** CRYPTO-107, CRYPTO-86, PLT-4553

## Notes
- The ticket comments mention "missing sorting by time from newest - to oldest" as a bug
- Also mentions "categories in response aren't returned" - possible additional issue to investigate
- Backend MR 110 is the fix being tested
