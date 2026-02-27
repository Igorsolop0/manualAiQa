# Test Ideas & Coverage Hints

**Оновлено:** 2026-02-27

---

## 1. Testing Strategy Overview

| Test Type | Scope | Tools |
|-----------|-------|-------|
| **Unit** | Individual functions, calculations, utils | Jest (frontend), Rust `#[test]` (backend/contracts) |
| **Integration** | Service interactions, DB operations, CPI | Jest + Anchor localnet, SQLx test transactions |
| **API/Server Action** | Server actions, API routes | Jest + mocking Prisma/Anchor |
| **Smart Contract** | On-chain instructions, state changes | Anchor test framework + Bankrun/Localnet |
| **E2E** | Full user flows via browser | Playwright/Cypress + devnet |

### Priority Order

1. Smart contract tests (highest risk — financial logic on-chain)
2. Backend orchestrator tests (event processing correctness)
3. Server action tests (data access layer)
4. Frontend component tests (UI correctness)
5. E2E flows (full integration)

---

## 2. Smart Contract Tests

---

### 2.1 Existing Tests

**Located in `solana/programs/sol_orao_vrf/test/`:**
- `tests/sol_ticket/init-ticket.test.ts` — protocol initialization
- `tests/sol_ticket/buy-ticket.test.ts` — position purchase
- `tests/sol_orao_vrf/gen-randomness.test.ts` — VRF randomness
- `tests/sol_bonding_curve/init-project.test.ts` — bonding curve setup
- `tests/sol_bonding_curve/cleanup-project.test.ts` — cleanup

Also: `solana/programs/sol_bonding_curve/documentation/test/integration.test.ts` — comprehensive bonding curve scenarios.

---

### 2.2 Critical Paths to Test

#### sol_ticket

| Test Case | Type | Priority |
|-----------|------|----------|
| Create protocol with valid parameters | Integration | P0 |
| Create protocol with invalid pool percentages (sum ≠ 100) | Integration | P0 |
| Buy position in active protocol | Integration | P0 |
| Buy position in locked protocol → should fail | Integration | P0 |
| Buy position in completed protocol → should fail | Integration | P0 |
| Force payout when time is due | Integration | P0 |
| Force payout before time → should fail | Integration | P0 |
| Buyout with correct price | Integration | P1 |
| Buyout with insufficient funds → should fail | Integration | P1 |
| Buyout when disabled → should fail | Integration | P1 |
| Deposit tokens on position | Integration | P1 |
| Withdraw locked tokens → should fail | Integration | P0 |
| Withdraw unlocked tokens | Integration | P1 |
| Protocol termination at max_participants | Integration | P1 |
| Protocol termination at max_epochs | Integration | P1 |
| Lock/unlock by non-server → should fail | Integration | P0 |
| Create ticket without server_signer → should fail | Integration | P0 |
| Chunk creation when current is full | Integration | P2 |
| Airdrop pool initialization | Integration | P2 |

---

#### sol_bonding_curve

| Test Case | Type | Priority |
|-----------|------|----------|
| Buy tokens with sufficient SOL | Integration | P0 |
| Buy tokens — verify 87/10/1/1/1 split | Integration | P0 |
| Sell tokens with valid amount | Integration | P0 |
| Sell tokens — verify 5% spread | Integration | P0 |
| Buy with slippage exceeded → should fail | Integration | P0 |
| Sell with min_sol_payout not met → should fail | Integration | P0 |
| Health ratio calculation accuracy | Unit | P0 |
| Sell restrictions at low health ratio | Integration | P1 |
| Price curve: price increases with supply | Unit | P0 |
| Close curve with non-empty vault → should fail | Integration | P2 |

---

#### sol_transfer_hook_nft

| Test Case | Type | Priority |
|-----------|------|----------|
| Transfer with server_signer → should succeed | Integration | P0 |
| Transfer without server_signer → should fail | Integration | P0 |
| Invalid server_signer key → should fail | Integration | P0 |

---

#### sol_orao_vrf

| Test Case | Type | Priority |
|-----------|------|----------|
| Request randomness for active protocol | Integration | P0 |
| Request randomness for locked protocol → should fail | Integration | P1 |
| VRF callback stores correct randomness | Integration | P0 |

---

### 2.3 Edge Cases Not to Miss

- **Concurrent position purchases** in same block
- **VRF timeout** (randomness never arrives)
- **Chunk overflow** (exact boundary conditions)
- **Epoch transition** during position purchase
- **Buyout during epoch transition**
- **Maximum u64 values** for pool amounts
- **Field size 9 vs 81** behavior differences
- **Empty protocol** (0 positions) force payout

---

## 3. Backend (be-ticket) Tests

---

### 3.1 Orchestrator Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| `ticket_created` — new position, first in protocol | Integration | P0 |
| `ticket_created` — new position with epoch change detected | Integration | P0 |
| `ticket_created` — duplicate event (idempotency) | Integration | P0 |
| `ticket_created` — protocol close condition met | Integration | P1 |
| `ticket_field_updated` — score increase | Integration | P0 |
| `ticket_field_updated` — best_field_match improvement | Integration | P0 |
| `ticket_field_updated` — top-1 change | Integration | P1 |
| `force_payout` — correct epoch history recording | Integration | P0 |
| `force_payout` — points winner reset | Integration | P0 |
| `force_payout` — staking snapshot creation | Integration | P1 |
| `token_holder_deposit` — correct lock epoch calculation | Integration | P0 |
| `token_holder_deposit` — locked/unlocked recalculation | Integration | P0 |
| `lottery_created` — full protocol creation | Integration | P0 |
| `lottery_created` — with bonding curve | Integration | P1 |

---

### 3.2 Service Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| `TicketService.calculate_score_and_create_history` — score calculation | Unit | P0 |
| `TicketService.calculate_potential_points` — potential points | Unit | P1 |
| `LotteryService.create_lottery_in_db` — all fields populated | Integration | P0 |
| `LotteryService.update_pools_and_top1` — pool amount updates | Integration | P0 |
| `SmartContractService.create_ticket_signed_by_service` — 3-tx flow | Integration | P0 |
| `BondingCurveService.process_buy_event` — state update | Integration | P1 |
| `BondingCurveService.update_holder_balance` — percentage calc | Unit | P1 |

---

### 3.3 Game Field Logic Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| `apply_round` — all 4 directions on 3×3 field | Unit | P0 |
| `apply_round` — all 4 directions on 9×9 field | Unit | P0 |
| `is_winning_field` — correct for sorted array | Unit | P0 |
| `is_winning_field` — false for unsorted array | Unit | P0 |
| `apply_round` — boundary diagonals | Unit | P1 |
| Score calculation after multiple rounds | Unit | P0 |

---

### 3.4 Edge Cases Not to Miss

- **Event arrives before DB has related records**
- **Duplicate events** with same `txProof`
- **Concurrent event processing** for same protocol
- **Database connection pool exhaustion**
- **VRF polling timeout**
- **Signing Service unavailable** during ticket creation
- **Account not finalized** when transaction is built

---

## 4. Frontend Tests

---

### 4.1 Server Action Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| `GetListProtocols` — returns protocols with correct filtering | Integration | P0 |
| `GetListProtocols` — empty result | Integration | P1 |
| `GetProtocol` — valid pubkey | Integration | P0 |
| `GetProtocol` — invalid pubkey → null | Integration | P0 |
| `GetOrCreateUser` — new user creation | Integration | P0 |
| `GetOrCreateUser` — existing user return | Integration | P0 |
| `CreateProtocol` — valid form data → transactions built | Integration | P0 |
| `CreatePositionInProtocol` — transaction building | Integration | P0 |
| `BuyTokens` — correct transaction structure | Integration | P1 |
| `SellTokens` — correct transaction structure | Integration | P1 |
| `GetEpochPayoutHistory` — ordered by epoch | Integration | P1 |
| `GetGlobalStatistics` — singleton return | Integration | P1 |

---

### 4.2 Component Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| `AuthGuardProvider` — authorized wallet → render children | Unit | P0 |
| `AuthGuardProvider` — unauthorized wallet → redirect | Unit | P0 |
| `AuthGuardProvider` — no wallet after timeout → redirect | Unit | P0 |
| Protocol card renders correct data | Unit | P1 |
| Protocol filter panel state management | Unit | P1 |
| Trading form validation | Unit | P1 |
| Epoch countdown timer accuracy | Unit | P2 |
| Position field visualization (3×3) | Unit | P2 |
| Position field visualization (9×9) | Unit | P2 |
| Create protocol form validation | Unit | P0 |
| Pool percentages sum validation | Unit | P0 |

---

### 4.3 E2E Tests

| Test Case | Priority |
|-----------|----------|
| Full protocol creation flow (connect wallet → create → verify) | P0 |
| Full position purchase flow (browse → buy → verify field) | P0 |
| Trading flow (buy tokens → verify balance → sell tokens) | P1 |
| Staking flow (deposit → wait epochs → withdraw) | P1 |
| Buyout flow (find protocol → buy → verify ownership change) | P1 |
| Force payout flow (wait for epoch → trigger → verify payouts) | P1 |
| Unauthorized access → redirect to /unauthorized | P0 |
| Protocol list filtering and sorting | P2 |
| History pages display correct data | P2 |

---

## 5. Signing Service Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| Health check returns 200 | API | P0 |
| Get public key with valid HMAC | API | P0 |
| Get public key with invalid HMAC → 401 | API | P0 |
| Get public key with expired timestamp → 401 | API | P0 |
| Sign legacy transaction | API | P0 |
| Sign versioned transaction | API | P0 |
| Sign transaction where keypair is not signer → 400 | API | P0 |
| Sign with treasury keypair | API | P1 |
| HMAC constant-time comparison (no timing attack) | Unit | P1 |
| Per-environment key isolation | Integration | P0 |

---

## 6. Database Tests

| Test Case | Type | Priority |
|-----------|------|----------|
| Unique constraint on `txProof` prevents duplicates | Integration | P0 |
| Cascade behavior on user deletion | Integration | P1 |
| GlobalStatistics singleton (only id=1) | Integration | P0 |
| EpochPayoutHistory `(lotteryPubkey, epochNumber)` uniqueness | Integration | P0 |
| StakingEpochSnapshot uniqueness per protocol+epoch | Integration | P0 |
| TokenDeposit `unlock_epoch = deposit_epoch + 2` | Unit | P0 |
| BondingCurveSnapshot OHLCV data integrity | Integration | P2 |
| Concurrent writes to same lottery (pool amount updates) | Integration | P1 |

---

## 7. Cross-Cutting Test Scenarios

| Scenario | Components Involved | Priority |
|----------|-------------------|----------|
| Full lifecycle: create protocol → buy positions → epoch payout → repeat | All | P0 |
| Protocol termination by max_participants | Contract + Backend + Frontend | P1 |
| Protocol termination by max_epochs | Contract + Backend + Frontend | P1 |
| Bonding curve trading under various health ratios | Contract + Backend | P1 |
| Buyout chain (multiple sequential buyouts) | Contract + Backend + Frontend | P2 |
| Staking across multiple epochs with deposits/withdrawals | Contract + Backend + Frontend | P1 |
| Real-time updates via Pusher after position creation | Backend + Frontend | P2 |
| Error recovery after Signing Service outage | Backend + Signing Service | P2 |
| Data consistency between on-chain state and DB | Contract + Backend | P0 |

---

## 8. Existing Test Infrastructure

### 8.1 Available

- Anchor test framework with Jest configuration (`solana/programs/sol_orao_vrf/test/`)
- Wallet manager for test wallets
- Signing Service integration in tests
- Test helpers and utility functions
- Bonding curve integration test suite

---

### 8.2 Missing / Recommended to Add

- **Unit test setup** for Rust backend (be-ticket)
- **Component testing setup** for Next.js (React Testing Library)
- **E2E test framework** (Playwright recommended for Next.js)
- **CI/CD pipeline** for automated test execution
- **Test database seeding scripts**
- **Mock providers** for Solana RPC in frontend tests
- **Snapshot testing** for UI components

---

## 9. Testing Best Practices

---

### 9.1 Unit Testing

- **Pure functions**: No external dependencies (RPC, DB, etc.)
- **Edge cases**: Test boundary conditions (0, max values, negative numbers)
- **Error paths**: Test all error branches
- **Deterministic**: Use fixed test data, not random values

---

### 9.2 Integration Testing

- **Real components**: Use actual implementations, not mocks (unless necessary)
- **Test data**: Create and clean up test data after each test
- **Isolation**: Tests should not depend on each other
- **Parallel execution**: Tests that don't interfere can run in parallel

---

### 9.3 E2E Testing

- **User perspective**: Test as real user would interact
- **Critical paths**: Focus on happy path + major edge cases
- **Real environment**: Use devnet/localnet, not mocks where possible
- **Clean up**: Ensure test environment is reset after each test

---

### 9.4 Smart Contract Testing

- **Bankrun integration**: Use Bankrun for localnet testing
- **Anchor test framework**: Leverage built-in testing utilities
- **Account management**: Use test accounts with pre-funded balances
- **Instruction testing**: Test each instruction individually before integration

---

## 10. Test Coverage Goals

---

### 10.1 Minimum Coverage Targets

| Component | Target Coverage |
|-----------|----------------|
| Smart Contracts | 90%+ of instruction handlers |
| Backend Orchestrators | 100% of event processing paths |
| Backend Services | 80%+ of methods |
| Server Actions | 100% of public actions |
| Frontend Components | 70%+ of critical components |

---

### 10.2 Critical Path Coverage

**Must cover:**
1. Protocol creation (full flow)
2. Position purchase (VRF + ticket creation)
3. Epoch payout (force_payout + distribution)
4. Staking (deposit + withdraw)
5. Bonding curve trading (buy + sell)
6. Buyout (transfer of ownership)
7. Protocol termination (max participants/epochs)

---

## 11. Mocking Guidelines

---

### 11.1 When to Mock

- **CI/CD**: Unstable external services (Solana RPC, VRF)
- **Unit tests**: External dependencies (Prisma, RPC calls)
- **Component tests**: Child components that require complex setup

---

### 11.2 When NOT to Mock

- **E2E tests**: Use devnet/localnet for realistic testing
- **Integration tests**: Use real implementations where possible
- **Smart contract tests**: Test against actual programs (not mocks)

---

## 12. Test Data Management

---

### 12.1 Seeding Strategy

- **Test accounts**: Pre-funded Solana accounts with SOL
- **Test protocols**: Standard test protocols in devnet
- **Database seeds**: Reproducible test data sets

---

### 12.2 Cleanup Strategy

- **Transactions**: Revert test transactions where possible
- **Database**: Delete test data after each test run
- **Accounts**: Close test accounts and return SOL

---

## 13. CI/CD Recommendations

---

### 13.1 Pipeline Stages

1. **Linting**: ESLint (frontend), Clippy (backend)
2. **Type checking**: TypeScript (frontend), Rust (backend)
3. **Unit tests**: Jest (all packages)
4. **Integration tests**: Anchor (contracts), Jest (services)
5. **E2E tests**: Playwright (frontend)
6. **Build**: Docker images for deployment

---

### 13.2 Fail-Fast Criteria

- Any test failure should fail the entire pipeline
- Flaky tests should be fixed or disabled
- Coverage thresholds must be met before merge
