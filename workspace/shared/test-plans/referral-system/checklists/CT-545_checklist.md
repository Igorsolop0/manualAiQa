# Test Checklist: CT-545 — BE: Reward Claim

**Status:** Open
**Component:** Backend Claim Flow
**Priority:** High

---

## 🎯 Ticket Summary

Implement the commission claim flow that allows referrers to withdraw their earned commission. The claimable balance must be stored as a separate account type in the wallet service. When a user claims, the service transfers the amount from the referral account to the wallet, records the claim transaction, and ensures full atomicity to prevent double-claiming.

---

## ✅ Acceptance Criteria Checklist

### Wallet Account Type

- [ ] New account type registered in wallet service (ReferralCommissionBalance)
- [ ] Commission accumulates in this account type
- [ ] Claimable amount read from this wallet account

### Claim Flow

- [ ] POST /api/referral/claim endpoint works
- [ ] Claim flow steps:
  1. [ ] Check no claim in Processing state for this user
  2. [ ] Validate claimable balance >= minClaimAmount (default $1.50)
  3. [ ] Insert ReferralClaim with Status = Processing
  4. [ ] Call wallet: deduct from referral account, credit to real balance
  5. [ ] On success: update claim to Completed, set WalletTransactionId
  6. [ ] On failure: update claim to Failed, return error
- [ ] Response includes: { claimedAmount, currency, remainingBalance }

### Double-Claim Prevention

- [ ] Processing state check prevents concurrent claims
- [ ] Idempotency key per claim (clientId_timestamp) unique constraint
- [ ] Duplicate submissions rejected at DB level

### Claim History

- [ ] ReferralClaim table created with all fields:
  - [ ] Id, ClientId, Amount, Currency
  - [ ] Status (Processing=1, Completed=2, Failed=3)
  - [ ] IdempotencyKey (unique)
  - [ ] WalletTransactionId
  - [ ] CreatedAt, CompletedAt
- [ ] History queryable with pagination and date sorting

### Edge Cases

- [ ] Claim during commission job run — only claimable amount eligible
- [ ] Wallet timeout — claim stays in Processing, background job retries
- [ ] Partial network failure — idempotency key prevents double credit

---

## 🧪 Test Scenarios

### 1. Successful Claim

- [ ] Verify that POST /claim with balance > $1.50 processes claim and transfers amount
- [ ] Verify that wallet after claim shows decreased referral balance and increased real balance
- [ ] Verify that ReferralClaim table records Status = Completed with WalletTransactionId set

### 2. Minimum Threshold

- [ ] Verify that POST /claim with balance < $1.50 returns rejection: "Minimum claim amount is $1.50"
- [ ] Verify that POST /claim with balance = $1.50 processes claim successfully
- [ ] Verify that changing partner setting enforces new threshold

### 3. Double-Claim Prevention

- [ ] Verify that sending 2 claim requests simultaneously results in only one success, other rejected
- [ ] Verify that sending same claim twice returns rejection: duplicate idempotency key
- [ ] Verify that concurrent request sees claim in Processing state and rejects

### 4. Zero/Negative Balance

- [ ] Verify that POST /claim with zero balance returns rejection: "No claimable balance"
- [ ] Verify that POST /claim with negative balance returns rejection

### 5. Wallet Failures

- [ ] Verify that simulating wallet timeout sets claim status = Failed and returns error
- [ ] Verify that wallet returning error sets claim status = Failed with no balance change
- [ ] Verify that retrying failed claim allows new claim attempt

### 6. 24h Cooldown (PM Requirement)

- [ ] Verify that claiming twice within 24h returns error: "You can claim once per 24 hours"
- [ ] Verify that waiting 24h and claiming again allows second claim to succeed

---

## 🧪 Business Logic Tests (PM Requirements)

### From PM's List:

- [ ] Verify that claiming commission transfers funds to Unused balance (real money)
- [ ] Verify that claiming < $1.50 returns rejection
- [ ] Verify that claiming within 24h of previous claim displays error message

---

## 🔗 Integration Points

### Wallet Service

- [ ] Synchronous HTTP call to wallet
- [ ] Deduct from ReferralCommissionBalance
- [ ] Credit to ClientUnusedBalance
- [ ] Transaction ID returned

### Background Jobs

- [ ] Reconciliation job for stuck Processing claims
- [ ] Retry mechanism for failed claims
- [ ] Monitoring for failed claims

---

## 🔗 Dependencies

**Depends on:** CT-540 (Services), CT-541 (API), CT-549 (Processing Bets)

**Blocks:** None (standalone claim flow)

---

## 📝 Notes

- Test with concurrent users to verify idempotency
- Simulate wallet failures to verify rollback behavior
- Verify reconciliation job works for orphaned claims

---

**Test Type:** Backend Claim Flow
**Estimated Effort:** 3 hours
**Test Environment:** QA
