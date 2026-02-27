# Backend Documentation — be-ticket

**Оновлено:** 2026-02-27

---

## 1. Overview

Backend — це Rust сервіс, побудований з Actix Web. Основна відповідальність — слухати події Solana блокчейну, обробляти їх через orchestrators, та синхронізувати стан в PostgreSQL базу даних.

---

## 2. Architecture Overview

```
main.rs
├── AppContext (central state holder)
│   ├── Services (business logic)
│   ├── Repositories (DB access)
│   └── Providers (external integrations)
├── Event Listener (PubSub subscriptions)
│   └── Orchestrators (event handlers)
└── HTTP Server (Actix Web)
    └── Routes (health check only)
```

### Entry Point (`main.rs`)

- Завантажує `.env` конфігурацію
- Ініціалізує tracing/logging
- Створює `AppContext` з усіма services, repositories, та providers
- Запускає дві паралельні задачі:
  1. **Event listener** — підписується на blockchain events
  2. **HTTP server** — один Actix Web worker з Railway-optimized timeouts

---

## 3. Application Context (`app/app_context.rs`)

`AppContext` структура тримає всі ініціалізовані services та надає їх до handlers.

### Initialized Services

| Service | Responsibility |
|---------|---------------|
| `ApiService` | HTTP notifications to frontend API routes |
| `TicketService` | Position/ticket business logic |
| `LotteryService` | Protocol/lottery business logic |
| `SmartContractService` | Building and sending on-chain transactions |
| `RandomService` | VRF randomness handling |
| `UserService` | User creation and lookup |
| `BondingCurveService` | Token trading event processing |

### Initialized Repositories

Всі repositories діляться PostgreSQL connection pool (`PgPoolOptions`).

| Repository | Table |
|-----------|-------|
| `TicketRepository` | Tickets + TicketField |
| `LotteryRepository` | Lotteries |
| `UserRepository` | Users |
| `UserTicketScoreRepository` | Scores |
| `TicketHistoryRepository` | Ticket action history |
| `TicketFieldHistoryRepository` | Field change history |
| `TicketPositionInChunkRepository` | Chunk positions |
| `TicketTransactionRepository` | Ticket transactions |
| `LotteryTransactionRepository` | Lottery transactions |
| `RandomnessRepository` | VRF randomness records |
| `BondingCurveRepository` | Bonding curve state |
| `BondingCurveTransactionRepository` | Trade history |
| `SmartContractEventRepository` | Event tracking |
| `EpochPayoutHistoryRepository` | Epoch payout records |
| `FieldPayoutHistoryRepository` | Field payout records |
| `TokenDepositRepository` | Token staking deposits |
| `StakingEpochSnapshotRepository` | Staking snapshots |
| `GlobalStatisticsRepository` | Global stats (singleton) |
| `ProtocolHistoryRepository` | Protocol purchase history |

### Providers

| Provider | Purpose |
|----------|---------|
| `OnchainProvider` (ticket) | Solana RPC for ticket program |
| `OnchainProvider` (vrf) | Solana RPC for VRF program |
| `OnchainProvider` (token_2022) | Solana RPC for NFT program |
| `PubSubProvider` | Event subscription via WebSocket |
| `KurrentDbProvider` | Event streaming from KurrentDB |

---

## 4. Event System

### Subscribed Events

| Event | Source Program | Trigger |
|-------|---------------|---------|
| `LotteryInitializedEvent` | sol_ticket | Protocol created |
| `TicketCreatedEvent` | sol_ticket | Position purchased |
| `TicketFieldUpdatedEvent` | sol_ticket | Field updated (new round) |
| `LotteryBuyoutEvent` | sol_ticket | Protocol bought out |
| `RandomResponseEvent` | sol_orao_vrf | VRF randomness ready |
| `TokenHolderDepositEvent` | sol_ticket | Token staked on position |
| `TokenHolderWithdrawEvent` | sol_ticket | Token unstaked from position |
| `ForcePayoutEvent` | sol_ticket | Epoch payout triggered (V2) |
| `AirdropInitializedEvent` | sol_ticket | Airdrop pools created (V2) |
| `BondingCurveInitializedEvent` | sol_bonding_curve | Curve created |
| `TokensBoughtEvent` | sol_bonding_curve | Tokens purchased |
| `TokensSoldEvent` | sol_bonding_curve | Tokens sold |

### Event Processing

Events десеріалізуються з Borsh формату. Кожен тип event маршрутизується до відповідного orchestrator. Events обробляються в окремих `tokio::spawn` tasks.

---

## 5. Orchestrators

Orchestrators містять core business logic для обробки blockchain events.

### `ticket_created` — Position Purchase Handler

**Triggered by**: `TicketCreatedEvent`

**Processing steps:**
1. Determine if this is a new position or field update
2. Detect epoch payout (compare `event.epoch_number` with last recorded epoch)
3. If new epoch detected:
   - Create `EpochPayoutHistory` record with top-1 payouts
   - Create `StakingEpochSnapshot` with staking stats
   - Reset points score for points pool winner
4. Create or update ticket and its game field in DB
5. Create transaction records (`TicketTransaction`, `LotteryTransaction`)
6. Create history records (`TicketHistory`, `TicketFieldHistory`)
7. Calculate score points and update `UserTicketScore`
8. Save player position in chunk (`TicketPositionInChunk`)
9. Update protocol statistics (total users, pool amounts, top-1 data)
10. Update `GlobalStatistics`
11. If `is_active == false` in event → close protocol (update state to LOCKED/COMPLETED)

### `ticket_field_updated` — Field Update Handler

**Triggered by**: `TicketFieldUpdatedEvent`

Similar to `ticket_created` but for field updates on existing positions:
1. Detect epoch changes
2. Update ticket field with new round data
3. Recalculate points and best_field_match
4. Update top-1 data from event
5. Update pool amounts

### `lottery_created` — Protocol Creation Handler

**Triggered by**: `LotteryInitializedEvent`

**Processing steps:**
1. Create user in DB if not exists
2. Fetch bonding curve data from blockchain
3. Create `BondingCurve` record in DB (if new)
4. Create `Lottery` record with all protocol data
5. Create `LotteryTransaction` record
6. Increment `GlobalStatistics.totalProtocols`

### `force_payout` — Epoch Payout Handler

**Triggered by**: `ForcePayoutEvent`

**Processing steps:**
1. Record `EpochPayoutHistory` with top-1 payout details
2. Create `StakingEpochSnapshot`
3. Reset points score for points pool winner
4. Update protocol's pool amounts and `payout_next_time`
5. Reset top-1 data after payout
6. Check protocol termination conditions

### `token_holder_deposit` — Staking Handler

**Triggered by**: `TokenHolderDepositEvent`

**Processing steps:**
1. Create `TokenDeposit` record with `deposit_epoch` and `unlock_epoch` (current + 2)
2. Calculate total locked/unlocked amounts for position
3. Update ticket staking statistics (`total_tokens_staked`, `locked_tokens`, `unlocked_tokens`)

### `token_holder_withdraw` — Unstaking Handler

**Triggered by**: `TokenHolderWithdrawEvent`

Similar to deposit but marks deposits as withdrawn and updates staking stats.

### `airdrop_initialized` — Airdrop Setup Handler

**Triggered by**: `AirdropInitializedEvent`

Updates protocol flags: sets `awaiting_airdrop_init = false` and enables appropriate airdrop pool flags.

### `lottery_buyout` — Buyout Handler

**Triggered by**: `LotteryBuyoutEvent`

Updates protocol ownership, buyout price, and buyout count.

---

## 6. Services

### `SmartContractService`

Відповідає за побудову та відправку Solana транзакцій.

**Key method: `create_ticket_signed_by_service()`**

Будує та відправляє 3 послідовні транзакції для створення позиції:

| Step | Transaction | Content |
|------|------------|---------|
| Tx1 | Create ATA | Creates Associated Token Account if needed |
| Tx2 | Create Ticket | `create_ticket` instruction (versioned with ALT or legacy) |
| Tx3 | Mint Token | `init_ticket_token` instruction (Token-2022) |

**Features:**
- Address Lookup Table (ALT) support для великих транзакцій (versioned transactions)
- Airdrop remaining accounts handling (22-35 additional accounts)
- VRF request polling з configurable interval
- Account finalization waiting перед продовженням
- Signing via Signing Service API

### `TicketService`

Position/ticket business logic.

| Method | Purpose |
|--------|---------|
| `create_with_field()` | Create ticket + field in DB (single transaction) |
| `update_with_field()` | Update ticket + field data |
| `calculate_score_and_create_history()` | Calculate points, update score, create history records |
| `save_player_position()` | Save chunk position for verification |
| `create_purchase_transaction()` | Create purchase-related transaction records |
| `calculate_potential_points()` | Calculate points a position could earn |

### `LotteryService`

Protocol/lottery business logic.

| Method | Purpose |
|--------|---------|
| `create_lottery_in_db()` | Create protocol with all V2 fields (airdrop, limits) |
| `process_lottery_buyout()` | Handle ownership transfer |
| `update_pools_and_top1_from_field_update()` | Update pool amounts and top-1 |
| `update_airdrop_status()` | Mark airdrop as initialized |
| `close_lottery()` | Set protocol state to completed |
| `update_pools_from_force_payout()` | Update after epoch payout |

### `ApiService`

HTTP client для сповіщення frontend.

| Method | Purpose |
|--------|---------|
| `notify_create_ticket()` | Notify about position creation |
| `purchase_ticket()` | Notify about purchase |
| `notify_jackpot_claim()` | Notify about jackpot |
| `notify_random_created()` | Notify about VRF result |

**Authentication:** Bearer token from `NOTIFY_SECRET` env var.

### `BondingCurveService`

| Method | Purpose |
|--------|---------|
| `process_buy_event()` | Record buy transaction, update holder balance |
| `process_sell_event()` | Record sell transaction, update holder balance |
| `update_holder_balance()` | Recalculate token holder balance and supply percentage |
| `try_create_snapshot()` | Create price/volume snapshot for charts |

---

## 7. Providers

### `OnchainProvider`

Solana blockchain interaction layer.

| Method | Purpose |
|--------|---------|
| `build_instruction_with_args()` | Build instruction from IDL definition |
| `fetch_account_data<T>()` | Deserialize account data (Borsh) |
| `wait_for_all_accounts_exist_finalized()` | Poll until accounts exist with Finalized commitment |
| `wait_for_vrf_request_fulfilled_finalized()` | Poll until VRF request has randomness |
| `send_signed_transaction()` | Send legacy transaction |
| `send_signed_versioned_transaction()` | Send versioned transaction |
| `create_unsigned_b64_versioned_transaction()` | Create versioned tx with ALT |
| `fetch_address_lookup_table()` | Load ALT for versioned transactions |

### `PubSubProvider`

WebSocket event subscription.

- Type-safe subscriptions via `TypeId`
- Borsh deserialization of events
- Async handlers via `tokio::spawn`

### `KurrentDbProvider`

Event streaming integration.

- Connects to KurrentDB stream `webhook-full-transactions`
- Processes `WebhookEvent` with revision tracking
- Handles reconnection and retry logic

---

## 8. Game Field Logic (`utils/game_field.rs`)

### Field Representation

- **3×3 field**: array of 9 values (0-8)
- **9×9 field**: array of 81 values (0-80)
- **Winning field**: `[1, 2, 3, 4, 5, 6, 7, 8, 9]` (sorted sequence)

### Round Application

Кожен round має:
- **Direction**: UpLeft, UpRight, DownLeft, DownRight
- **Diagonal index**: which diagonal to shift

`apply_round()` shifts values along specified diagonal in given direction.

### Scoring

- Points increase when values move closer to winning position
- `is_winning_field()` checks if field matches `[1, 2, 3, ..., N]`
- `best_field_match_count` tracks how many values are in their correct position

---

## 9. HTTP Endpoints

Backend надає мінімальні HTTP endpoints (більшість комунікації event-driven):

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | None | Health check |
| `GET` | `/ip` | None | Server IP information |

---

## 10. Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SOLANA_RPC_URL` | Solana RPC endpoint |
| `SOLANA_WS_URL` | Solana WebSocket endpoint |
| `SIGNING_SERVICE_URL` | Signing Service base URL |
| `SIGNING_SERVICE_SECRET` | HMAC secret for Signing Service |
| `NOTIFY_SECRET` | Bearer token for frontend API notifications |
| `KURRENT_DB_URL` | KurrentDB connection string |
| `SUPABASE_URL` / `SUPABASE_KEY` | Supabase for IDL storage |

---

## 11. Dependencies

| Crate | Version | Purpose |
|-------|---------|---------|
| `actix-web` | 4.0 | HTTP server |
| `tokio` | — | Async runtime |
| `sqlx` | — | PostgreSQL driver |
| `solana-sdk` / `solana-client` | — | Solana interaction |
| `anchor-lang` / `anchor-client` | — | Anchor framework |
| `borsh` | — | Binary serialization |
| `kurrentdb` | — | Event streaming |
| `reqwest` | — | HTTP client |
| `chrono` | — | Date/time |
| `uuid` | — | UUID handling |
| `tracing` | — | Structured logging |

---

## 12. Transaction Flows

### Position Creation Flow (3 transactions)

```
Tx1: Create ATA (if needed)
    ↓
Tx2: create_ticket instruction (sol_ticket)
    ↓
Tx3: init_ticket_token instruction (sol_token_2022_nft)
```

**Features:**
- ALT (Address Lookup Table) для оптимізації
- VRF polling з retry logic
- Account finalization перевірка
- Signing via Signing Service (HMAC auth)

### Epoch Detection

Backend автоматично детектує нові епохи при обробці `TicketCreatedEvent` та `TicketFieldUpdatedEvent`:

1. Порівнює `event.epoch_number` з останнім записом в DB
2. Якщо новий epoch → створює `EpochPayoutHistory` та `StakingEpochSnapshot`
3. Reset points та оновлює pool amounts
