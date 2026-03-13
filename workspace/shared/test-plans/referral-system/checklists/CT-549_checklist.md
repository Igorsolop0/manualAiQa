# Test Checklist: CT-549 — BE: Processing Bets

**Status:** Open
**Component:** Backend Bet Processing Pipeline
**Priority:** Critical

---

## 🎯 Ticket Summary

Implement the core bet processing pipeline in the referral service that consumes settled bets from Kafka, calculates referral commission in real-time, accumulates it in the referral system, and synchronizes commission balances with the wallet service.

---

## ✅ Acceptance Criteria Checklist

### Kafka Consumer

- [ ] Consumes from topic: {env}.CorePlatform.BetItemCurrencyEvent
- [ ] Consumer group: referral-bet-processor
- [ ] Buffer pattern: TimeSpan.FromSeconds(1), 1000
- [ ] Dedup within batch by TransactionId (keep latest)

### Event Filtering

- [ ] Include: Type == Debit (wagers)
- [ ] Exclude: Type == Credit (wins) — for wager tracking
- [ ] Exclude: IsFreeRound == true
- [ ] Include: Real money only (RateAmounts[AccountType.Unused] > 0)
- [ ] Exclude: Bonus-only bets (no Unused amount)
- [ ] Currency conversion to EUR works correctly

### Idempotency & Duplicate Prevention

- [ ] ReferralProcessedBet table created
  - [ ] Id, EventKey (TransactionId), PartnerId, ProcessedAt
  - [ ] Unique index on EventKey
- [ ] Bulk-check before processing
- [ ] Bulk-insert after processing
- [ ] Cleanup job deletes records > 30 days

### Referral Lookup

- [ ] For each ClientId, check if referred user
- [ ] Redis cache: referral_client_{clientId}
  - [ ] Contains: referralId, referrerId, campaignId, refSharePercent
  - [ ] Or null for non-referred users
- [ ] TTL: 1 hour
- [ ] Null marker for non-referred users (skip immediately)

### Commission Calculation

- [ ] Real money wager extracted: RateAmounts[AccountType.Unused]
- [ ] EUR equivalent calculated: GetAmountByCurrency("EUR", amount)
- [ ] CoefficientPercent resolved from template
- [ ] Formula: commission = realWagerAmountEur * (CoefficientPercent / 100)

### Storage

- [ ] ReferralWager upsert (daily aggregate per ReferralId, Date, GameCategory)
  - [ ] Atomic increment via INSERT ... ON CONFLICT DO UPDATE
- [ ] ReferralCommission inserted (per-transaction record)
  - [ ] All required fields stored
  - [ ] Decimal precision: 18,4 for amounts, 5,2 for percent

### Daily Wallet Sync Job

- [ ] Aggregates previous day's commissions (00:00–24:00 UTC)
- [ ] Synchronous HTTP call to wallet
- [ ] Credits referrer's referral commission account
- [ ] ReferralTransaction record created (Type=Commission)
- [ ] ReferralAccount balance updated
- [ ] Idempotent: checks if transaction for date exists
- [ ] Failure handling: logs error, continues with others
- [ ] Missed days: auto-detect and process gaps

### Parallel Processing & Data Integrity

- [ ] Kafka partitioned by ClientId
- [ ] Batch-level DB transactions (rollback on error)
- [ ] ReferralWager atomic increment (no lost updates)
- [ ] ReferralProcessedBet unique constraint (prevents double-processing)
- [ ] Consumer offset commit after DB transaction
- [ ] Dead letter topic: referral-bet-processor.Errors
- [ ] Backpressure: buffer pauses when DB slow
- [ ] Metrics per batch: received, filtered, processed, skipped, errors

---

## 🧪 Test Scenarios

### 1. Event Filtering

- [ ] Verify that real money wager (Type=Debit, Unused=100) is processed
- [ ] Verify that bonus bet (Type=Debit, Unused=0, Bonus=100) is skipped
- [ ] Verify that free round (IsFreeRound=true) is skipped
- [ ] Verify that win event (Type=Credit) is skipped for wager tracking
- [ ] Verify that mixed account bet (Unused=50, Bonus=50) processes only Unused portion

### 2. Commission Calculation

- [ ] Verify that Slots wager $100 with Coefficient=15% generates Commission = $15.00 EUR
- [ ] Verify that Live wager $100 with Coefficient=5% generates Commission = $5.00 EUR
- [ ] Verify that Instant wager $100 with Coefficient=5% generates Commission = $5.00 EUR
- [ ] Verify that currency conversion works (Bet in USD, rate 0.92) produces Commission in EUR

### 3. Idempotency

- [ ] Verify that processing same TransactionId twice creates only one commission record
- [ ] Verify that consumer restart after processing does not create duplicate commissions
- [ ] Verify that replaying old events produces same result (idempotent behavior)

### 4. Referral Lookup

- [ ] Verify that referred user (ClientId in Redis cache) triggers commission calculation
- [ ] Verify that non-referred user (ClientId not in cache, null) skips event immediately
- [ ] Verify that cache expiry after TTL 1h triggers cache refresh from DB

### 5. Daily Wallet Sync

- [ ] Verify that successful daily job sync credits all commissions to referrers
- [ ] Verify that partial wallet failure for 1 referrer allows others to succeed with error logged
- [ ] Verify that missed day (job skipped yesterday) triggers auto-detect and backfill
- [ ] Verify that duplicate job run for same day is idempotent (no double credit)

### 6. Sub-1c Commission (PM Requirement)

- [ ] Verify that small wager ($0.01, Coefficient 5%) stores Commission = $0.0005 correctly
- [ ] Verify that multiple small wagers accumulate correctly in daily aggregate

---

## 🧪 Business Logic Tests (PM Requirements)

### From PM's List:

- [ ] Verify that different commission rates apply by category (Slots: 15%, Live/Instant: 5%)
- [ ] Verify that user with multiaccount tag does not accrue commission
- [ ] Verify that bonus funds exclusion works (user plays with bonus money, no commission accrued)
- [ ] Verify that sub-1c commission (< 1 cent) is stored correctly and accumulates

---

## 🔗 Integration Points

### Kafka

- [ ] Consumer connects to correct topic
- [ ] Consumer group unique (no conflict with other consumers)
- [ ] Offset commit strategy correct

### Redis

- [ ] Cache hit rate acceptable (majority non-referred)
- [ ] Cache invalidation works
- [ ] TTL enforced

### Wallet Service

- [ ] HTTP calls succeed
- [ ] Timeout handling
- [ ] Retry logic for failures

---

## 🔗 Dependencies

**Depends on:** CT-540 (Services), CT-546 (Templates)

**Blocks:** CT-545 (Claim needs commissions)

---

## 📝 Notes

- This is the **most critical** ticket — core business logic
- Test with high volume events (simulate production load)
- Verify performance: most events should be skipped at Redis cache (non-referred)
- Monitor dead letter topic for failures

---

**Test Type:** Backend Pipeline
**Estimated Effort:** 1 day 1 hour
**Test Environment:** QA
