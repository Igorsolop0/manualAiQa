# Referral System Test Plan (CRYPTO-70)

**Created:** 2026-03-13
**Author:** Nexus (AI QA Assistant)
**Project:** Minebit / NextCode
**Status:** Planning Phase

---

## 📋 Executive Summary

This master document coordinates test planning for the **Referral System (CRYPTO-70)** and its linked CT tickets. Each CT ticket will have a dedicated checklist document that can be added to Jira for PM review.

---

## 🎯 Testing Approach

### Format Decision: **Separate Checklists per Ticket**

**Why separate checklists?**
1. Each checklist will be added to its corresponding Jira ticket
2. PM can review and approve test scope per ticket independently
3. Easier tracking of test coverage per component
4. Allows parallel work when multiple tickets move to "Ready for Testing"

**Master Document Purpose:**
- Cross-cutting concerns and dependencies
- Integration testing scenarios (spanning multiple tickets)
- End-to-end user journey testing
- Risk-based prioritization

---

## 📦 Ticket Status Overview

| Ticket | Status | Component | Priority |
|--------|--------|-----------|----------|
| CT-540 | In Progress | BE: Services | High |
| CT-541 | Open | BE: Referral Program API | High |
| CT-545 | Open | BE: Reward Claim | High |
| CT-546 | Open | BE: Commission Templates | High |
| CT-549 | Open | BE: Processing Bets | Critical |
| CT-674 | Open | FE: First Page Layout | Medium |
| CT-678 | In Progress | FE: Share Referral Links Form | Medium |
| CT-683 | Open | FE: Share Referral Links Layout | Medium |
| CT-854 | Ready for Testing | BE: Mockups for Portal | Low (Infrastructure) |

---

## 🔗 Cross-Cutting Test Categories

### 1. **Functional Testing**
- Commission calculation accuracy
- Referral tracking integrity
- Claim flow correctness
- Campaign management CRUD
- API endpoint contracts

### 2. **Business Logic Testing** (from PM's list)
- ✅ Commission rates by game category (Slots 15%, Live/Instant 5%)
- ✅ Multiaccount tag blocking
- ✅ Bonus funds exclusion (real money only)
- ✅ Claim to Unused balance
- ✅ Field validation (name, RefCode)
- ✅ Default campaign behavior
- ✅ Sub-1c commission handling
- ✅ 24h claim cooldown
- ✅ Max 20 campaigns limit

### 3. **Integration Testing**
- Kafka event processing
- Wallet service synchronization
- CorePlatform API integration
- Redis cache consistency
- Database idempotency

### 4. **Edge Cases & Error Handling**
- Zero balance claims
- Duplicate claim prevention
- Wallet timeout handling
- Concurrent request handling
- Missing product structure data

### 5. **UI/UX Testing** (FE tickets)
- Layout matches Figma design
- Responsive (mobile + desktop)
- Copy functionality
- Navigation flow
- Error message clarity

---

## 🧪 Test Execution Strategy

### Phase 1: Backend Unit Tests (BE Tickets)
**Execution:** API-level testing via Swagger / Postman / Python scripts
**Focus:**
- Endpoint contracts
- Business logic correctness
- Error handling
- Data integrity

### Phase 2: Backend Integration Tests
**Execution:** End-to-end API flows
**Focus:**
- Kafka → Referral Service → Wallet flow
- Cross-service communication
- Data consistency

### Phase 3: Frontend UI Tests
**Execution:** Manual UI testing + Playwright automation
**Focus:**
- Visual layout (Figma compliance)
- User interactions
- Responsive design
- Error states

### Phase 4: End-to-End User Journey
**Execution:** Full flow simulation
**Focus:**
- Complete referral lifecycle
- Commission earning and claiming
- Campaign management
- Statistics accuracy

---

## 🔍 Test Data Requirements

### User Scenarios Needed:
1. **New User** (no referral activity)
2. **Referrer** (active referrer with commissions)
3. **Referred User** (registered via referral)
4. **Multiaccount Tag User** (blocked from referral system)
5. **User at Campaign Limit** (20 campaigns)

### Game Data Needed:
1. Slots games (15% commission category)
2. Live casino games (5% commission category)
3. Instant games (5% commission category)
4. Games with bonus bets (exclusion test)
5. Free round games (exclusion test)

### Financial Data Needed:
1. Users with claimable balance > min threshold ($1.50)
2. Users with claimable balance < min threshold
3. Users with pending commissions
4. Users who already claimed today (24h cooldown test)

---

## 📊 Checklist Files Structure

```
test-plans/referral-system/
├── MASTER_TEST_PLAN.md (this file)
├── checklists/
│   ├── CT-540_checklist.md  (BE: Services)
│   ├── CT-541_checklist.md  (BE: Referral Program API)
│   ├── CT-545_checklist.md  (BE: Reward Claim)
│   ├── CT-546_checklist.md  (BE: Commission Templates)
│   ├── CT-549_checklist.md  (BE: Processing Bets)
│   ├── CT-674_checklist.md  (FE: First Page Layout)
│   ├── CT-678_checklist.md  (FE: Share Referral Links Form)
│   ├── CT-683_checklist.md  (FE: Share Referral Links Layout)
│   └── CT-854_checklist.md  (BE: Mockups for Portal)
└── test-results/
    └── (execution artifacts)
```

---

## 🎯 Next Steps

1. ✅ Master test plan created
2. ⏳ Create individual checklists for each CT ticket
3. ⏳ Review with PM
4. ⏳ Add approved checklists to Jira tickets
5. ⏳ Execute tests as tickets move to "Ready for Testing"

---

## 📝 Notes

- All checklists will be in English (for TestRail compatibility)
- Checklists will include both positive and negative test scenarios
- Each checklist will reference acceptance criteria from the Jira ticket
- Test data setup scripts will be documented separately

---

**Last Updated:** 2026-03-13
