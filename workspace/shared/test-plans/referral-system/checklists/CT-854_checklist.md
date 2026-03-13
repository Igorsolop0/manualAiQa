# Test Checklist: CT-854 — BE: Mockups for Portal Dev

**Status:** Ready for Testing
**Component:** Backend Infrastructure
**Priority:** Low

---

## 🎯 Ticket Summary

Create mockups for Portal so they can start doing tasks before new endpoints are created. API endpoints described in CT-541.

---

## ✅ Acceptance Criteria Checklist

### Wiremock Configuration

- [ ] Wiremock stubs created for referral endpoints
- [ ] Endpoints match CT-541 specification
- [ ] Response codes defined
- [ ] Error responses configured

### Mocked Endpoints (from CT-541)

- [ ] GET /api/referral/stats
- [ ] GET /api/referral/defaultCampaign
- [ ] GET /api/referral/campaigns
- [ ] POST /api/referral/campaigns
- [ ] DELETE /api/referral/campaigns/{id}
- [ ] GET /api/referral/referrals
- [ ] GET /api/referral/claims

### Response Data

- [ ] Mock responses contain realistic data
- [ ] Pagination works (mock totalCount)
- [ ] Error scenarios covered

---

## 🧪 Test Scenarios

### 1. Endpoint Availability

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| GET /stats | Call endpoint | Mock response returned |
| GET /campaigns | Call endpoint | Mock response with pagination |
| POST /campaigns | Call endpoint | Mock response (created) |

### 2. Response Codes

| Test Case | Scenario | Expected Result |
|-----------|----------|-----------------|
| Success response | Valid request | 200 OK |
| Validation error | Invalid input | 400 with error message |
| Not found | Missing resource | 404 |

### 3. Portal Integration

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Portal dev uses mock | Portal team consumes mocks | Portal can start FE work |

---

## 🔗 Dependencies

**Depends on:** CT-541 (API specification)

**Blocks:** Portal FE development

---

## 📝 Notes

- This is **infrastructure** for parallel development
- Mocks will be replaced by real endpoints when CT-541 is complete
- Focus on response structure matching specification

---

**Test Type:** Backend Infrastructure (Mocks)
**Estimated Effort:** 2 hours
**Test Environment:** Dev
