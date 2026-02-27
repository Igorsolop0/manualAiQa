# Open Questions & Gaps

**Оновлено:** 2026-02-27

---

## 1. Overview

Items below are not obvious from the codebase and should be clarified with the team before comprehensive test coverage.

---

## 2. Business Logic Questions

---

### 2.1 Buyout Price Formula

**Question:** What is the exact formula for buyout price increase after each buyout?

**Details:** The DB stores `currentBuyoutPrice` but the multiplication/increment logic is in the smart contract.

**Impact:** Cannot write precise test assertions for buyout price progression without this.

**Recommendation:** Clarify with smart contract developer or check smart contract code for buyout instruction.

---

### 2.2 Airdrop Distribution Model

**Question:** How are airdrop pool rewards distributed?

**Details:** Is it the same top-1 model as regular pools, or a different distribution mechanism (proportional, random, etc.)?

**Impact:** Cannot test airdrop payout correctness.

**Recommendation:** Document airdrop distribution logic in `DOMAIN.md` or separate airdrop documentation.

---

### 2.3 Jackpot Claim Flow

**Question:** What exactly happens when a user achieves the winning field `[1, 2, 3, ..., N]`?

**Details:** Is the jackpot auto-distributed, or does the user need to claim it? The backend has `process_jackpot_claim()` and `notify_jackpot_claim()` methods, but the on-chain flow for jackpot claim is not fully clear.

**Impact:** Cannot test jackpot end-to-end flow.

**Recommendation:** Clarify jackpot distribution mechanism with team.

---

### 2.4 Token Holder Pool — Tie Breaking

**Question:** What happens when two positions have the same amount of unlocked staked tokens?

**Details:** Who gets the Token Holder pool payout?

**Impact:** Edge case for epoch payout testing.

**Recommendation:** Define tie-breaking rules (first to stake, oldest position, split evenly, etc.).

---

### 2.5 Points Pool — Tie Breaking

**Question:** Same question for points pool — if two positions have the same score, who wins?

**Details:** Who gets the Points pool payout?

**Impact:** Edge case for epoch payout testing.

**Recommendation:** Define tie-breaking rules for all pools.

---

### 2.6 Protocol Completion — Remaining Funds

**Question:** When a protocol completes (maxParticipants/maxEpochs reached), what happens to remaining pool balances?

**Details:** Are the remaining funds distributed, locked, or refunded?

**Impact:** Cannot test protocol termination cleanup.

**Recommendation:** Clarify with backend team.

---

### 2.7 Hold Token Gating

**Question:** The `hold_token` and `hold_token_amount_per_ticket` fields on `LotteryAccount` suggest token gating.

**Details:**
- How is this enforced?
- Is a user required to hold specific tokens to buy a position?
- Is the check on-chain or off-chain?

**Impact:** Cannot test token-gated protocol access.

**Recommendation:** Clarify gating mechanism with smart contract developer.

---

## 3. Architecture Questions

---

### 3.1 KurrentDB vs PubSub

**Question:** The backend has both `KurrentDbProvider` and `PubSubProvider`.

**Details:** Which is the primary event source in production? Are they redundant/fallback, or do they serve different event types?

**Impact:** Affects test environment setup for integration tests.

**Recommendation:** Document primary event source per environment and fallback strategy.

---

### 3.2 Event Ordering Guarantees

**Question:** Are blockchain events guaranteed to arrive in order?

**Details:** What happens if `TicketFieldUpdatedEvent` arrives before `TicketCreatedEvent` for the same position?

**Impact:** Critical for orchestrator error handling tests.

**Recommendation:** Document event ordering behavior and orchestrator handling for out-of-order events.

---

### 3.3 Retry / Dead Letter Queue

**Question:** What happens when an orchestrator fails to process an event?

**Details:** Is there a retry mechanism, dead letter queue, or manual reprocessing?

**Impact:** Affects error recovery test scenarios.

**Recommendation:** Clarify error handling and recovery strategy with backend team.

---

### 3.4 Backend Concurrency

**Question:** The backend uses `tokio::spawn` for event processing.

**Details:** Are there any concurrency controls (mutex, semaphore) for events affecting the same protocol?

**Details needed:**
- What prevents race conditions between `ticket_created` and `force_payout` for the same protocol?
- What about concurrent position purchases?

**Impact:** Concurrency test scenarios.

**Recommendation:** Document concurrency model and race condition prevention.

---

## 4. Frontend Questions

---

### 4.1 Wallet Whitelist Management

**Question:** How are new wallets added to `AUTHORIZED_KEYS`?

**Details:**
- Is it a code deployment?
- Is there an admin interface for this?
- How are changes propagated (rebuild, config reload)?

**Impact:** Testing access control changes.

**Recommendation:** Document whitelist management process.

---

### 4.2 Pusher Events — Full List

**Question:** What is the complete list of Pusher events and channels?

**Details:** The code shows `buyout` event on `ticket-specific-*` channel, but are there other events for:
- Position creation?
- Epoch payout?
- Field updates?
- Staking events?

**Impact:** Real-time update test coverage.

**Recommendation:** Document all Pusher events and their payloads.

---

### 4.3 Offline/Error States

**Question:** How does the frontend handle:

**Details needed:**
- Solana RPC downtime
- Signing Service unavailable
- Database unreachable

**Additional questions:**
- Are there error boundaries?
- Is there a retry mechanism?
- Is there a degraded-mode UI?

**Impact:** Resilience testing.

**Recommendation:** Document error handling strategy for all external dependencies.

---

### 4.4 Agent Mode Scope

**Question:** What is the full scope of Agent Mode?

**Details:** Is it only wallet auto-connection, or does it also modify transaction signing behavior?

**Impact:** Automated test configuration.

**Recommendation:** Clarify full Agent Mode capabilities.

---

## 5. Smart Contract Questions

---

### 5.1 Account Size Limits

**Question:** What is the maximum number of participants per chunk?

**Details:**
- When does `create_new_chunk` get triggered?
- What is the max total participants a protocol can handle before running into Solana account size limits?

**Impact:** Scalability and boundary testing.

**Recommendation:** Clarify chunk management and account size limits with smart contract developer.

---

### 5.2 Versioned Transaction Requirement

**Question:** When exactly is a versioned transaction (with ALT) required vs a legacy transaction?

**Details:** The backend handles both, but what are the specific conditions?

**Conditions to clarify:**
- Large number of accounts in transaction?
- Specific instructions that require ALT?
- Account data size thresholds?

**Impact:** Transaction building tests.

**Recommendation:** Document versioned transaction requirements and conditions.

---

### 5.3 Transfer Hook — Exemptions

**Question:** Are there any transfers exempt from the Transfer Hook?

**Details:** For example:
- Program-to-program transfers via PermanentDelegate?
- Mint operations?
- Burn operations?

Or does every single transfer require server_signer?

**Impact:** Transfer authorization test coverage.

**Recommendation:** Clarify Transfer Hook scope and exemptions with smart contract developer.

---

### 5.4 Bonding Curve — Health Ratio Thresholds

**Question:** At what exact health ratio thresholds are sell restrictions applied?

**Details:** The code references `HealthRatioBelowMinimum` and `HealthRatioCritical` errors but threshold values are in the smart contract.

**Impact:** Cannot test sell restriction boundaries without exact values.

**Recommendation:** Document health ratio thresholds (exact values or formula).

---

### 5.5 Multiple Programs on Devnet vs Mainnet

**Question:** Program IDs differ between devnet and mainnet.

**Examples:**
- sol_ticket devnet = `BxNBAX2WN5iGGUfctHhsN9xqyTRvSGFqyBoAetCV94Yy`
- sol_ticket mainnet = `FYaHz8zsZzZJetMmU1uxwfzkU8aryPoWyFsSbm69D44G`

**Questions:**
- Are there any behavioral differences between devnet and mainnet deployments?
- Are there any devnet-specific features or relaxed constraints?

**Impact:** Environment-specific testing.

**Recommendation:** Document any differences between devnet and mainnet behavior.

---

## 6. Database Questions

---

### 6.1 LotteryState Enum — Missing States

**Question:** The `LotteryState` enum only has `ACTIVE` and `LOCKED`.

**Details:** But there are references to "COMPLETED" in orchestrator logic.

**Questions needed:**
- Is `LOCKED` used for both epoch transitions and permanent completion?
- Should there be a `COMPLETED` state?
- What are the transitions: ACTIVE → LOCKED → COMPLETED?

**Impact:** State machine testing.

**Recommendation:** Clarify state machine transitions and add `COMPLETED` state if needed.

---

### 6.2 Legacy Models

**Question:** Several models appear to be legacy.

**Models to review:**
- `TicketTransaction`
- `LotteryTransaction`
- `TicketHistory`
- `TicketFieldHistory`

**Questions:**
- Are they still actively written to?
- Are they being replaced by newer models (ProtocolHistory, FieldPayoutHistory, EpochPayoutHistory)?

**Impact:** Determines which models need test coverage.

**Recommendation:** Audit schema and mark legacy models vs active models.

---

### 6.3 Data Retention

**Question:** Is there any data cleanup/archival policy?

**Details:**
- The cron route `archive-tickets` is commented out
- What is the expected data growth rate?
- What is the retention period for:
  - Transaction history?
  - Event logs?
  - SmartContractEvent records?

**Impact:** Performance and storage testing.

**Recommendation:** Define data retention and archival policies.

---

## 7. DevOps / Environment Questions

---

### 7.1 Environment Parity

**Question:** How closely does devnet environment mirror mainnet?

**Details to verify:**
- Are there any devnet-specific features?
- Are constraints relaxed on devnet?
- Are different RPC endpoints used?
- Are different signing services used?

**Impact:** Test environment fidelity.

**Recommendation:** Document devnet vs mainnet differences clearly.

---

### 7.2 Deployment Process

**Question:** What is the deployment pipeline?

**Details:**
- Docker on Railway for backend/signing service
- How is frontend deployed (Vercel? Railway?)
- What is the rollback procedure?

**Impact:** Deployment verification tests.

**Recommendation:** Document deployment process and rollback strategy.

---

### 7.3 Monitoring & Alerting

**Question:** Is there any monitoring/alerting setup?

**Details to check:**
- Datadog?
- Sentry?
- Custom monitoring?
- What metrics are tracked?
- What triggers alerts?

**Impact:** Determines if we can use monitoring data for test validation.

**Recommendation:** Document monitoring stack and available metrics.

---

### 7.4 Database Migrations

**Question:** How are database schema migrations handled across environments?

**Details:**
- Is Prisma migrate used?
- What is the rollback procedure?
- Are migrations applied to all environments (dev, staging, prod)?

**Impact:** Migration testing strategy.

**Recommendation:** Document migration process and rollback strategy.

---

## 8. Security Questions

---

### 8.1 Rate Limiting

**Question:** Is there any rate limiting on:

**Details to check:**
- Signing Service?
- Frontend API routes?
- Solana RPC?
- Database connections?

**Impact:** Security and load testing.

**Recommendation:** Document rate limits and testing approach.

---

### 8.2 Transaction Replay Protection

**Question:** Beyond Solana's built-in recent blockhash expiry, is there any additional replay protection for signed transactions?

**Details needed:**
- Timestamp-based expiration?
- Nonce in transaction?
- Additional validation?

**Impact:** Security testing.

**Recommendation:** Clarify replay protection mechanisms beyond Solana defaults.

---

### 8.3 Wallet Whitelist Bypass

**Question:** The whitelist is enforced only in the frontend (`AuthGuardProvider`).

**Details to consider:**
- Can a technically savvy user bypass it by calling server actions directly?
- Is there server-side wallet verification?

**Potential bypass paths:**
- Direct HTTP POST to server actions
- Direct Solana transaction without server co-sign
- Wallet not in whitelist but has private key

**Impact:** Authorization bypass testing.

**Recommendation:** Add server-side wallet verification for sensitive operations.

**Note:** Server Actions in Next.js can potentially be called directly via HTTP POST. If wallet verification is only in React component, server actions may be accessible without proper authorization.

---

## 9. Summary Priority

| Priority | Questions Count | Areas |
|----------|----------------|-------|
| **Must clarify before testing** | 6 | Buyout formula, jackpot flow, state machine, event ordering, concurrency, whitelist bypass |
| **Should clarify for thorough coverage** | 8 | Airdrop model, tie-breaking, protocol completion, hold token gating, retry logic, Pusher events, offline states, Agent mode |
| **Nice to know** | 9 | Data retention, monitoring, deployment, environment parity, legacy models, DB migrations, rate limiting, replay protection |

---

## 10. Action Items

### High Priority (Clarify Before Testing)

1. ✅ Document buyout price increase formula
2. ✅ Clarify airdrop distribution model
3. ✅ Document jackpot claim flow (auto-claim vs manual)
4. ✅ Define tie-breaking rules for all pools (points, best field match, token holder)
5. ✅ Clarify protocol completion behavior (remaining funds)
6. ✅ Clarify hold token gating mechanism
7. ✅ Document event ordering and orchestrator handling for out-of-order events
8. ✅ Clarify retry mechanism for failed event processing
9. ✅ Document backend concurrency model and race condition prevention
10. ✅ Document wallet whitelist management process
11. ✅ Document complete Pusher events list
12. ✅ Clarify error handling for all external dependencies
13. ✅ Clarify full Agent Mode scope
14. ✅ Add server-side wallet verification for sensitive operations

### Medium Priority (Clarify for Coverage)

15. Document health ratio thresholds (exact values)
16. Document versioned transaction requirements
17. Document Transfer Hook scope and exemptions
18. Document devnet vs mainnet differences
19. Audit schema and mark legacy vs active models
20. Define data retention and archival policies
21. Document deployment process and rollback strategy
22. Document monitoring stack and available metrics
23. Document database migration process

### Low Priority (Nice to Know)

24. Clarify database connection pool configuration
25. Document rate limits on all services
26. Clarify replay protection beyond Solana defaults
27. Ensure devnet environment mirrors mainnet behavior

---

## 11. Next Steps

1. Schedule meeting with team to review these questions
2. Prioritize high-priority items for clarification
3. Document answers in appropriate files:
   - Update `DOMAIN.md` with clarified business rules
   - Update `ARCHITECTURE.md` (create if needed) with deployment details
   - Create `DEPLOYMENT.md` with environment and monitoring info
4. Create test cases for clarified business logic
5. Update `TESTING.md` with clarified scenarios

---

## 12. Test Coverage Impact

By clarifying these questions, we can:

- **Increase test confidence** — Tests will match actual system behavior
- **Reduce test flakiness** — Less ambiguity means fewer false negatives/positives
- **Improve edge case coverage** — Clarified rules enable more comprehensive testing
- **Enable security testing** — Whitelist bypass paths can be tested once documented

---

## 13. Risk of NOT Clarifying

- **False positives** — Tests fail when system actually works
- **False negatives** — Bugs go undetected in production
- **Wasted test effort** — Tests written for undefined behavior
- **Delayed bug discovery** — Ambiguous rules make debugging harder

**Recommendation:** Prioritize clarification with team before writing comprehensive test suites.
