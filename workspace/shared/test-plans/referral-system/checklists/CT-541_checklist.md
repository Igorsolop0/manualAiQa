# Test Checklist: CT-541 — BE: Referral Program API Implementation

**Status:** Open
**Component:** Backend API
**Priority:** High

---

## 🎯 Ticket Summary

Implement all backend API endpoints in the Referral service: user statistics, campaign CRUD, referral listing, commission claiming, and backoffice visibility.

---

## ✅ Acceptance Criteria Checklist

### User Statistics Endpoint

- [ ] GET /api/referral/stats returns correct data:
  - [ ] totalReferrals (count)
  - [ ] totalProfit (EUR)
  - [ ] amountAvailableForClaim
  - [ ] pendingCommission
  - [ ] totalClaimed

### Default Campaign

- [ ] GET /api/referral/defaultCampaign returns referralCode
- [ ] Default campaign auto-created on user registration
- [ ] Default campaign has isDefault = true flag
- [ ] Default campaign cannot be renamed
- [ ] Default campaign cannot be modified
- [ ] Default campaign cannot be deleted
- [ ] Migration creates default campaigns for existing users

### Campaign Listing

- [ ] GET /api/referral/campaigns supports pagination (page, pageSize)
- [ ] GET /api/referral/campaigns supports date filtering (dateFrom, dateTo)
- [ ] GET /api/referral/campaigns supports sorting (sortBy, asc/desc)
- [ ] Response includes totalCount for pagination
- [ ] Response includes all required fields:
  - [ ] id, name, referralCode, referralLink
  - [ ] isDefault, status, referralCount
  - [ ] createdAt, totalProfit

### Create Campaign

- [ ] POST /api/referral/campaigns creates new campaign
- [ ] Name validation:
  - [ ] Min 5, max 50 characters
  - [ ] Only Latin letters, spaces, underscores, hyphens, numbers
  - [ ] Unique per user
- [ ] Referral code validation:
  - [ ] Min 5, max 30 characters
  - [ ] Only Latin letters and numbers
  - [ ] Globally unique across all users/partners
- [ ] Max campaigns limit enforced (default 20, configurable)
- [ ] Validation errors return clear messages:
  - [ ] "This code already exists, try another one"
  - [ ] "Campaign name already exists"
  - [ ] "Maximum campaign limit reached"

### Validate Referral Code (Optional)

- [ ] GET /api/referral/campaigns/validate-code?code={code}
- [ ] Returns { isAvailable: bool }
- [ ] Checks global uniqueness

### Delete Campaign

- [ ] DELETE /api/referral/campaigns/{id} soft-deletes campaign
- [ ] Cannot delete default campaign → error: "Default campaign cannot be deleted"
- [ ] Cannot delete campaign with referrals → error: "Campaign has referrals and cannot be deleted"
- [ ] Sets Status = Deleted (soft delete)

### Referral Listing

- [ ] GET /api/referral/referrals supports pagination
- [ ] GET /api/referral/referrals supports campaignId filter
- [ ] GET /api/referral/referrals supports date filtering
- [ ] GET /api/referral/referrals supports sorting (default: registration date desc)
- [ ] Response includes totalCount
- [ ] Response includes all required fields:
  - [ ] username, registeredAt, campaignName
  - [ ] totalWager, commissionEarned

### Claimed History

- [ ] GET /api/referral/claims supports pagination
- [ ] GET /api/referral/claims supports campaignId filter
- [ ] GET /api/referral/claims supports date filtering
- [ ] GET /api/referral/claims supports sorting (default: date desc)
- [ ] Response includes: date, amount, currency

---

## 🧪 Test Scenarios

### 1. User Statistics

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Stats for new user | GET /stats for user with no referrals | All zeros |
| Stats for active referrer | GET /stats for user with referrals | Accurate counts and amounts |
| Stats after claim | GET /stats after user claims | totalClaimed updated, amountAvailableForClaim decreased |

### 2. Default Campaign

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Auto-create on registration | Register new user | Default campaign exists |
| Default campaign immutability | Try to rename/delete | Error: "Default campaign cannot be modified/deleted" |
| Migration for existing users | Run migration | All existing users have default campaigns |

### 3. Campaign CRUD

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Create valid campaign | POST with valid name/code | Campaign created |
| Duplicate name (same user) | POST with existing name | Error: "Campaign name already exists" |
| Duplicate code (global) | POST with existing code | Error: "This code already exists" |
| Max campaigns limit | Create 21st campaign | Error: "Maximum campaign limit reached" |
| Delete campaign with referrals | DELETE campaign with referrals | Error: "Campaign has referrals" |

### 4. Field Validation

| Test Case | Input | Expected Result |
|-----------|-------|-----------------|
| Name too short | "Ab" | Validation error (min 5 chars) |
| Name too long | "A" * 51 | Validation error (max 50 chars) |
| Name invalid chars | "Test@Campaign" | Validation error (only letters, numbers, space, underscore, hyphen) |
| Code too short | "Ab1" | Validation error (min 5 chars) |
| Code too long | "A" * 31 | Validation error (max 30 chars) |
| Code invalid chars | "Test-Code" | Validation error (only alphanumeric) |

### 5. Referral Listing

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| List all referrals | GET /referrals (no filters) | All referrals returned with pagination |
| Filter by campaign | GET /referrals?campaignId=X | Only referrals from campaign X |
| Filter by date | GET /referrals?dateFrom=X&dateTo=Y | Referrals in date range |
| Sort asc/desc | GET /referrals?sortBy=registeredAt&sortOrder=asc | Sorted correctly |

---

## 🔗 Cross-Cutting Concerns

### Security

- [ ] All endpoints require authentication
- [ ] User can only access their own data
- [ ] Admin endpoints require admin role

### Performance

- [ ] Pagination works correctly (default page size)
- [ ] Date filtering uses indexes (query performance acceptable)
- [ ] Response time < 500ms for list endpoints

### Error Handling

- [ ] Validation errors return 400 with clear message
- [ ] Unauthorized requests return 401
- [ ] Not found resources return 404
- [ ] Server errors return 500 with error ID (for logging)

---

## 🔗 Dependencies

**Depends on:** CT-540 (Services infrastructure)

**Blocks:** FE tickets (CT-674, CT-678, CT-683)

---

## 📝 Notes

- Validate all field constraints against PM requirements
- Test with real data scenarios (active referrers, multiple campaigns)
- Verify pagination math (totalCount vs actual items)

---

**Test Type:** Backend API
**Estimated Effort:** 4 hours
**Test Environment:** QA
