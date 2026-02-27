# Database Schema

**Оновлено:** 2026-02-27

---

## 1. Overview

PostgreSQL database managed by Prisma ORM. Schema file: `shared/prisma/schema.prisma`.

---

## 2. Entity Relationship Overview

```
User ─────────────────── 1:N ──── Ticket (positions)
│                                │
│                                ├── 1:1 ── TicketField
│                                ├── 1:1 ── UserTicketScore
│                                ├── 1:N ── TicketHistory
│                                ├── 1:N ── TicketFieldHistory
│                                ├── 1:N ── TicketPositionInChunk
│                                ├── 1:N ── TicketTransaction
│                                ├── 1:N ── TokenDeposit
│                                └── 1:N ── Randomness
│
│                                ├── 1:N ── Lottery (as creator)
│                                │   │
│                                │   ├── 1:N ── Ticket
│                                │   ├── 1:1 ── BondingCurve
│                                │   ├── 1:N ── ProtocolHistory
│                                │   ├── 1:N ── FieldPayoutHistory
│                                │   ├── 1:N ── EpochPayoutHistory
│                                │   ├── 1:N ── TokenDeposit
│                                │   ├── 1:N ── StakingEpochSnapshot
│                                │   └── 1:N ── LotteryTransaction
│                                │       ├── 1:N ── TicketTransaction (as buyer/seller)
│                                │       └── 1:N ── LotteryTransaction (as buyer/seller)
│
│                                └── 1:N ── GlobalStatistics (singleton, id=1)
│
SmartContractEvent (event tracking)
```

---

## 3. Core Models

---

### 3.1 User

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `pubkey` | String | PK | Solana wallet public key |
| `username` | String | Unique | Auto-generated username |
| `email` | String? | Optional | Email (unused currently) |
| `totalEarnings` | Float | Default 0.0 | Lifetime earnings |
| `withdrawnEarnings` | Float | Default 0.0 | Total withdrawn |
| `perfectCombinationsWon` | Int | Default 0 | Jackpots won |
| `createdAt` | DateTime | Auto | Creation timestamp |
| `updatedAt` | DateTime | Auto | Last update |

**Indexes**: `createdAt`, `totalEarnings`, `withdrawnEarnings`, `perfectCombinationsWon`, `email`

---

### 3.2 Lottery (Protocol)

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `pubkey` | String | PK | On-chain PDA address |
| `id` | String | Unique | UUID |
| `entryFee` | Float | Required | Position purchase price (SOL) |
| `duration` | String? | Optional | Payout period label |
| `payoutNextTime` | DateTime? | Optional | Next epoch payout timestamp |
| `jackpotPoolAmount` | Float | Default 0.0 | Current jackpot pool |
| `pointsPoolAmount` | Float | Default 0.0 | Current points pool |
| `bestFieldMatchPoolAmount` | Float | Default 0.0 | Current best field pool |
| `tokenHolderPoolAmount` | Float | Default 0.0 | Current token holder pool |
| `totalUsers` | Int | Default 0 | Unique users count |
| `totalPositions` | Int | Default 0 | Total positions |
| `currentState` | LotteryState | Default ACTIVE | Protocol state |
| `lotterySeed` | Int | Required | PDA seed |
| `pointsPoolSeed` | Int | Required | Points pool PDA seed |
| `bestFieldMatchPoolSeed` | Int | Required | Best field match pool PDA seed |
| `tokenHolderPoolSeed` | Int | Required | Token holder pool PDA seed |
| `jackpotTokenHolderPoolSeed` | Int | Required | Jackpot token holder pool PDA seed |
| `firstChunkSeed` | Int | Required | First chunk seed |
| `currentChunkSeed` | Int | Required | Current chunk seed |
| `ownerPubKey` | String? | FK → User | Current owner |
| `tokenPubKey` | String | Required | Ownership NFT address |
| `bondingCurvePubkey` | String | FK → BondingCurve | Associated bonding curve |
| `topOnePointsPDA` | String? | Optional | Current points leader |
| `topOnePointsAmount` | Float | Default 0.0 | Points leader's amount |
| `topOneBestMatchFieldPDA` | String? | Optional | Best match leader |
| `topOneBestMatchFieldAmount` | Float | Default 0.0 | Best match amount |
| `topOneTokenHolderPDA` | String? | Optional | Token holder leader |
| `topOneTokenHolderAmount` | Float | Default 0.0 | Token holder amount |
| `accumulateTokenHolderToJackpotAmount` | Float | Default 0.0 | Accumulated to jackpot |
| `totalPaidPointsPool` | Float | Default 0.0 | Lifetime paid to points pool |
| `totalPaidBestFieldMatchPool` | Float | Default 0.0 | Lifetime paid to best field match pool |
| `totalPaidTokenHolderPool` | Float | Default 0.0 | Lifetime paid to token holder pool |
| `totalPaidJackpotTokenHolderPool` | Float | Default 0.0 | Lifetime paid to jackpot token holder pool |
| `pointsPoolPercentage` | Int | Required | Points pool distribution % |
| `bestFieldMatchPoolPercentage` | Int | Required | Best field match pool distribution % |
| `tokenHolderPoolPercentage` | Int | Required | Token holder pool distribution % |
| `jackpotTokenHolderPoolPercentage` | Int | Required | Jackpot token holder pool distribution % |
| `fieldSize` | Int | Required | 9 (3×3) or 81 (9×9) |
| `tokenMint` | String | Required | Token mint address |
| `holdToken` | String? | Optional | Token gating address |
| `holdTokenAmountPerTicket` | BigInt? | Optional | Required token amount |
| `buyoutEnabled` | Boolean | Default false | Buyout feature flag |
| `initialBuyoutPrice` | BigInt | Default 0 | Initial buyout price |
| `currentBuyoutPrice` | BigInt | Default 0 | Current buyout price |
| `buyoutCount` | Int | Default 0 | Number of buyouts |
| `lastBuyoutAt` | DateTime? | Optional | Last buyout timestamp |
| `altAddress` | String? | Optional | Address Lookup Table |
| `maxParticipants` | BigInt? | Optional | V2: max positions (null = no limit) |
| `maxEpochs` | BigInt? | Optional | V2: max epochs (null = no limit) |
| `awaitingAirdropInit` | Boolean | Default false | V2: airdrop init pending |
| `hasPointsAirdrop` | Boolean | Default false | V2: points airdrop flag |
| `hasBestFieldAirdrop` | Boolean | Default false | V2: best field airdrop flag |
| `hasTokenHolderAirdrop` | Boolean | Default false | V2: token holder airdrop flag |
| `hasJackpotAirdrop` | Boolean | Default false | V2: jackpot airdrop flag |
| `pointsAirdropSeed` | Int? | Optional | V2: points airdrop PDA seed |
| `bestFieldAirdropSeed` | Int? | Optional | V2: best field airdrop PDA seed |
| `tokenHolderAirdropSeed` | Int? | Optional | V2: token holder airdrop PDA seed |
| `jackpotAirdropSeed` | Int? | Optional | V2: jackpot airdrop PDA seed |
| `createdAt` | DateTime | Auto | Creation timestamp |

**Indexes**: `currentState`, `totalUsers`, `totalPositions`, `jackpotPoolAmount`, `createdAt`, `duration`, `entryFee`, `tokenPubKey`, `bondingCurvePubkey`, `tokenMint`, `buyoutEnabled`, `(buyoutEnabled, currentState)`, `currentBuyoutPrice`

---

### 3.3 Ticket (Position)

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `pubkey` | String | PK, Unique | On-chain PDA |
| `ticketId` | String | Unique | UUID |
| `txProof` | String | Unique | Creation transaction signature |
| `userPubkey` | String | FK → User | Owner wallet |
| `ticketFieldId` | Int | FK → TicketField, Unique | Game field reference |
| `lotteryPubkey` | String | FK → Lottery | Parent protocol |
| `tokenPubKey` | String | Required | Participation token |
| `epochNumber` | Int? | Optional | Current epoch at creation/update |
| `bestFieldMatchCount` | Int | Default 0 | Correct positions count |
| `totalTokensStaked` | BigInt | Default 0 | Total staked tokens |
| `lockedTokens` | BigInt | Default 0 | Currently locked tokens |
| `unlockedTokens` | BigInt | Default 0 | Currently unlocked tokens |
| `fieldUpdateCount` | Int | Default 0 | Number of field updates |
| `potentialPoints` | Int | Default 0 | Max achievable points |

**Indexes**: `createdAt`, `tokenPubKey`, `(lotteryPubkey, epochNumber)`, `(lotteryPubkey, bestFieldMatchCount DESC)`, `(lotteryPubkey, totalTokensStaked DESC)`

---

## 4. Score & Earnings Models

---

### 4.1 UserTicketScore

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `id` | Int | PK, Auto | Sequential ID |
| `ticketPubkey` | String | Unique, FK → Ticket | Position reference |
| `userPubkey` | String | FK → User | User reference |
| `lotteryPubkey` | String | FK → Lottery | Protocol reference |
| `score` | Int | Default 0 | Current score |

**Unique**: `(userPubkey, ticketPubkey, lotteryPubkey)`, `(ticketPubkey, lotteryPubkey)`, `(userPubkey, ticketPubkey)`

---

### 4.2 UserTicketScoreHistory

Tracks every score change for audit trail.

| Column | Type | Description |
|--------|------|-------------|
| `previousScore` | Int | Score before change |
| `currentScore` | Int | Score after change |
| `pointsAdded` | Int | Delta for this transaction |

---

## 5. Field Models

---

### 5.1 TicketField

| Column | Type | Description |
|--------|------|-------------|
| `id` | Int | PK, Auto |
| `ticketPubkey` | String | Position reference |
| `lotteryPubkey` | String | Protocol reference |
| `initialField` | Json | Original field (array of ints) |
| `currentField` | Json | Current field state (array of ints) |

---

### 5.2 TicketFieldHistory

Records every field change with the move that caused it.

| Column | Type | Description |
|--------|------|-------------|
| `fieldValues` | Json | Field state at this point |
| `moveObject` | Json | The round/move that was applied |

---

## 6. History Models

---

### 6.1 ProtocolHistory

Simple log of position purchases in a protocol.

| Column | Type | Description |
|--------|------|-------------|
| `lotteryPubkey` | String | FK → Lottery |
| `txProof` | String | Unique transaction signature |

---

### 6.2 FieldPayoutHistory

Records jackpot (field) payouts.

| Column | Type | Description |
|--------|------|-------------|
| `lotteryPubkey` | String | FK → Lottery |
| `amount` | Float | Payout amount (SOL) |
| `txProof` | String | Unique transaction |

---

### 6.3 EpochPayoutHistory

Records epoch-end payouts with top-1 details.

| Column | Type | Description |
|--------|------|-------------|
| `lotteryPubkey` | String | FK → Lottery |
| `epochNumber` | Int | Epoch number |
| `startDate` / `endDate` | DateTime | Epoch time range |
| `topOnePointsPDA` | String? | Points winner |
| `topOnePointsAmount` | Float | Points payout amount |
| `topOneBestMatchFieldPDA` | String? | Best match winner |
| `topOneBestMatchFieldAmount` | Float | Best match payout amount |
| `topOneTokenHolderPDA` | String? | Token holder winner |
| `topOneTokenHolderAmount` | Float | Token holder payout amount |
| `txProof` | String | Unique transaction |

---

## 7. Token Staking Models

---

### 7.1 TokenDeposit

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `ticketPubkey` | String | FK → Ticket |
| `lotteryPubkey` | String | FK → Lottery |
| `amount` | BigInt | Deposited amount (lamports) |
| `depositEpoch` | Int | Epoch when deposited |
| `unlockEpoch` | Int | `depositEpoch + 2` |
| `isWithdrawn` | Boolean | Default false |
| `txProof` | String | Unique transaction |

**Indexes**: `(lotteryPubkey, depositEpoch)`, `(lotteryPubkey, unlockEpoch)`, `ticketPubkey`, `isWithdrawn`

---

### 7.2 StakingEpochSnapshot

| Column | Type | Description |
|--------|------|-------------|
| `lotteryPubkey` | String | FK → Lottery |
| `epochNumber` | Int | Epoch number |
| `totalStaked` | BigInt | Total staked at epoch end |
| `totalLocked` | BigInt | Locked tokens |
| `totalUnlocked` | BigInt | Unlocked tokens |
| `depositsInEpoch` | BigInt | New deposits this epoch |
| `withdrawalsInEpoch` | BigInt | Withdrawals this epoch |
| `tokenHolderPoolAmount` | Float | Pool amount at epoch end |

**Unique**: `(lotteryPubkey, epochNumber)`

---

## 8. Bonding Curve Models

---

### 8.1 BondingCurve

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `id` | String | UUID, PK |
| `pubkey` | String | Unique, on-chain address |
| `tokenMint` | String | Token mint address |
| `isPlatform` | Boolean | True for LRPTN |
| `virtualSolReserves` | BigInt | Virtual SOL (constant) |
| `virtualTokenReserves` | BigInt | Virtual tokens (constant) |
| `realSolReserves` | BigInt | Actual SOL held |
| `tokensInVault` | BigInt | Tokens in vault |
| `tokensSold` | BigInt | Total sold |
| `sellSpreadBps` | Int | Sell spread (500 = 5%) |
| `cachedHealthRatio` | BigInt | Health ratio × 10000 |
| `isActive` | Boolean | Active flag |

---

### 8.2 BondingCurveTransaction

| Column | Type | Description |
|--------|------|-------------|
| `signature` | String | Unique, tx signature |
| `type` | String | "BUY" or "SELL" |
| `userWallet` | String | Trader wallet |
| `tokenAmount` | BigInt | Token amount traded |
| `solAmount` | BigInt | SOL amount traded |
| `pricePerToken` | Decimal(30,15) | Price at execution |
| `virtualSolAfter` | BigInt | Reserves after trade |
| `virtualTokenAfter` | BigInt | Reserves after trade |
| `healthRatioAfter` | BigInt | Health ratio after trade |
| `slot` | BigInt | Solana slot |
| `timestamp` | DateTime | Trade timestamp |

---

### 8.3 TokenHolder

| Column | Type | Description |
|--------|------|-------------|
| `walletAddress` | String | Holder's wallet |
| `tokenBalance` | BigInt | Current balance |
| `percentageOfSupply` | Decimal(10,4) | % of total supply |

**Unique**: `(bondingCurvePubkey, walletAddress)`

---

### 8.4 BondingCurveSnapshot

OHLCV candle data for charts.

| Column | Type | Description |
|--------|------|-------------|
| `interval` | String | "1hour" or "1day" |
| `timestamp` | DateTime | Candle timestamp |
| `openPrice` / `highPrice` / `lowPrice` / `closePrice` | Decimal(30,15) | OHLC prices |
| `volume` | BigInt | Trading volume |
| `txCount` | Int | Number of trades |

**Unique**: `(bondingCurvePubkey, interval, timestamp)`

---

## 9. Utility Models

---

### 9.1 SmartContractEvent

| Column | Type | Description |
|--------|------|-------------|
| `revision` | BigInt | Event revision number |
| `streamName` | String | Unique, KurrentDB stream |

Used for tracking which events have been processed (cursor management).

---

### 9.2 GlobalStatistics (Singleton)

| Column | Type | Description |
|--------|------|-------------|
| `id` | Int | Always 1 |
| `totalProtocols` | Int | Platform-wide protocol count |
| `totalPositions` | Int | Platform-wide position count |
| `currentPointsPool` | Float | Sum of current points pool amounts across all protocols |
| `currentBestFieldMatchPool` | Float | Sum of current best field match pool amounts |
| `currentTokenHolderPool` | Float | Sum of current token holder pool amounts |
| `currentJackpotTokenHolderPool` | Float | Sum of current jackpot token holder pool amounts |
| `totalPaidPointsPool` | Float | Lifetime payouts to points pool across all protocols |
| `totalPaidBestFieldMatchPool` | Float | Lifetime payouts to best field match pool |
| `totalPaidTokenHolderPool` | Float | Lifetime payouts to token holder pool |
| `totalPaidJackpotTokenHolderPool` | Float | Lifetime payouts to jackpot token holder pool |
| `maxPointsPayout` | Float | Largest single points payout |
| `maxBestFieldMatchPayout` | Float | Largest single best field match payout |
| `maxTokenHolderPayout` | Float | Largest single token holder payout |
| `maxJackpotTokenHolderPayout` | Float | Largest single jackpot token holder payout |
| `maxPointsPayoutProtocol` | String? | Protocol with largest points payout |
| `maxBestFieldMatchPayoutProtocol` | String? | Protocol with largest best field match payout |
| `maxTokenHolderPayoutProtocol` | String? | Protocol with largest token holder payout |
| `maxJackpotTokenHolderPayoutProtocol` | String? | Protocol with largest jackpot token holder payout |
| `topTotalPayoutProtocol` | String? | Protocol with highest total across 4 pools |
| `topTotalPayoutAmount` | Float? | That protocol's total amount |

---

## 10. Enums

---

### 10.1 LotteryState

```
ACTIVE    — protocol is running normally
LOCKED    — protocol is locked (epoch transition or completed)
```

---

### 10.2 TicketTransactionType

```
CREATE           — initial position creation
JACKPOT_PAYOUT   — jackpot claimed
PURCHASE          — position purchase
OPENED            — position opened
CLOSED            — position closed
DELETED            — position deleted
```

---

### 10.3 LotteryTransactionType

```
CREATE    — protocol creation
PURCHASE  — position purchase in protocol
OPENED    — protocol opened
CLOSED    — protocol closed
PAUSED    — protocol paused
DELETED   — protocol deleted
```

---

### 10.4 TicketHistoryActionType

```
CREATE           — position created
CHANGE_OWNER     — ownership changed
SELL_TOKEN       — token sold
BUY_TOKEN        — token bought
COMPLETION       — field completed (jackpot)
OPENED           — position opened
CLOSED           — position closed
PAUSED           — position paused
DELETED          — position deleted
```

---

## 11. Schema Design Principles

---

### 11.1 Write Separation

**Key rule**: Frontend ONLY READS from the database. All WRITES are performed by the Rust backend after processing blockchain events.

**Rationale:**
- Ensures data consistency with on-chain state
- Prevents race conditions
- Single source of truth (backend orchestrators)

---

### 11.2 Idempotency

Transaction signatures serve as idempotency keys:

- `Ticket.txProof` — prevents duplicate position creation
- `TicketFieldHistory.fieldValues` — prevents duplicate field updates
- `EpochPayoutHistory.txProof` — prevents duplicate payouts
- `BondingCurveTransaction.signature` — prevents duplicate trades

---

### 11.3 Event Tracking

`SmartContractEvent.revision` tracks which events from KurrentDB have been processed:

- Acts as cursor for stream resumption
- Prevents duplicate processing
- Enables fault-tolerant event handling

---

### 11.4 Unique Constraints

Tables use `@@unique` constraints for:
- Preventing duplicate users (email, username)
- Preventing duplicate tickets (txProof)
- Preventing duplicate deposits (ticketPubkey, depositEpoch)
- Preventing duplicate snapshots (bondingCurvePubkey, interval, timestamp)

---

## 12. Index Strategy

---

### 12.1 Read Optimization

**Frequently queried columns are indexed:**

| Table | Indexed Columns | Query Pattern |
|--------|----------------|---------------|
| `User` | `createdAt`, `totalEarnings`, `withdrawnEarnings` | Leaderboards |
| `Lottery` | `currentState`, `totalUsers`, `totalPositions`, `createdAt` | Protocol lists, filtering |
| `Ticket` | `createdAt`, `tokenPubKey`, `(lotteryPubkey, epochNumber)` | Position history, rankings |
| `TokenDeposit` | `(lotteryPubkey, depositEpoch)`, `(lotteryPubkey, unlockEpoch)` | Staking queries |

---

### 12.2 Write Optimization

**Indexes for upsert operations:**

| Table | Unique Constraint | Pattern |
|--------|----------------|----------|
| `User` | `pubkey` (PK) | Single record per wallet |
| `UserTicketScore` | `(userPubkey, ticketPubkey, lotteryPubkey)` | One score per user per protocol |
| `TokenDeposit` | `(lotteryPubkey, depositEpoch)` | One deposit per position per epoch |

---

## 13. Data Consistency Rules

---

### 13.1 Pool Amount Integrity

All pool amounts in `Lottery` must satisfy:

```
jackpotPoolAmount + pointsPoolAmount + bestFieldMatchPoolAmount + tokenHolderPoolAmount =
  totalPaidJackpotTokenHolderPool + totalPaidPointsPool + totalPaidBestFieldMatchPool + totalPaidTokenHolderPool + currentAccumulatedRewards
```

Where `currentAccumulatedRewards` = entryFee × totalPositions

---

### 13.2 Staking Consistency

For each ticket:

```
totalTokensStaked = lockedTokens + unlockedTokens
```

For each epoch:

```
totalStaked = totalLocked + totalUnlocked
```

---

### 13.3 Bonding Curve Consistency

```
virtualSolReserves × virtualTokenReserves = k (constant)
```

```
realSolReserves = tokensSold × entryFee × 0.87 (87% to treasury)
```

```
tokensInVault = tokensSold - (tokensSold via exit)
```

---

### 13.4 Token Supply Consistency

For each bonding curve:

```
SUM(TokenHolder.tokenBalance) = tokensInVault + tokensSold
```

---

## 14. Migration Strategy

---

### 14.1 Schema Evolution

**Prisma migrations:**
- Located in `shared/prisma/migrations/`
- Applied via `prisma migrate dev`
- Auto-generated SQL with rollback support

**Versioning:**
- Migration files are timestamped
- Each migration includes `up` and `down` SQL
- Prisma schema file updated after each migration

---

### 14.2 Zero-Downtime Deployments

**Migration approach:**
1. Deploy new backend version with updated Prisma schema
2. Run migrations in-place
3. New backend version compatible with old schema
4. Gradual rollout to new backend
5. Old backend version deprecated after migration completes

---

## 15. Backup & Recovery

---

### 15.1 Database Backup

**Backup strategy:**
- Daily full backups via PostgreSQL `pg_dump`
- Incremental WAL archiving (continuous archiving)
- Retention: 30 days of backups

**Restore procedure:**
1. Stop application (backend)
2. Drop current database
3. Restore from backup file
4. Verify data integrity
5. Restart application

---

### 15.2 Disaster Recovery

**Recovery scenarios:**

| Scenario | Recovery Steps |
|----------|----------------|
| **Corrupted table** | Restore from latest backup, replay missed events |
| **Lost events** | Replay KurrentDB stream from last revision |
| **Missing data** | Manually fix via Prisma scripts, restore from backup |

---

## 16. Performance Considerations

---

### 16.1 Connection Pooling

**Prisma pool configuration:**
- Max connections: Configurable via `DATABASE_URL` connection params
- Connection timeout: 10 seconds
- Idle timeout: 30 seconds
- Max lifetime: 1 hour

---

### 16.2 Query Optimization

**Index usage patterns:**
- Always filter by indexed columns
- Use `select` for partial column retrieval
- Use `include` for relations (avoid N+1 queries)

---

### 16.3 Write Throughput

**Write patterns:**
- Backend writes in batches (up to 100 records per transaction)
- Use `upsert` for idempotent operations
- Defer non-critical updates to background jobs

---

## 17. Security Considerations

---

### 17.1 Data Privacy

**Sensitive data protection:**
- Wallet public keys are stored (not private keys)
- User emails are optional and encrypted at rest
- No personal identifying information stored beyond wallet

---

### 17.2 Access Control

**Database access:**
- Frontend: Read-only via Prisma
- Backend: Full access via SQLx
- Admin: Read-only via Prisma (different schema context)

---

### 17.3 SQL Injection Protection

**Protection layers:**
- Prisma ORM (parameterized queries)
- No raw SQL in frontend
- Raw SQL in backend is carefully validated

---

### 17.4 Data Retention

**Retention policies:**
- Transaction history: Retained indefinitely (audit trail)
- Event logs: Retained for 90 days
- Backup retention: 30 days
