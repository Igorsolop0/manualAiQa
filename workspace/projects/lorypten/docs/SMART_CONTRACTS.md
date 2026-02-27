# Smart Contracts Documentation — Lorypten

**Оновлено:** 2026-02-27

---

## 1. Overview

Платформа складається з 6 Solana програм, побудованих з Anchor framework. Вони взаємодіють через CPI (Cross-Program Invocation).

---

## 2. Program Registry

| Program | Program ID (Devnet) | Purpose |
|---------|-------------------|---------|
| `sol_ticket` | `BxNBAX2WN5iGGUfctHhsN9xqyTRvSGFqyBoAetCV94Yy` | Core protocol/lottery logic |
| `sol_bonding_curve` | `CevDPSnS5ygxEjB21Q5zkgxfGWF3ogkkLqdeaowM8zLg` | AMM token trading |
| `sol_token_2022_nft` | `BdzA1gDdNYL3JJ23aFecrdESDuW3bJejFnQXHoYTG8NM` | NFT creation (Token-2022) |
| `sol_transfer_hook_nft` | `ELEodXPrqpMQkpVKgTadEv7dx6k83hsrTLVU6e4HYPF2` | Transfer authorization hook |
| `sol_orao_vrf` | `3B9qwG36WsbFV4MT8XuMi6ccNg2etqDX6bW5wRoMAdbc` | VRF random number generation |
| `sol_treasury` | `4qxyR2KiEN4JDErcaE3GyMcTuHucgzgnYrjuxAYSTECv` | Treasury management |

**`server_signer`** (backend wallet) потрібен для більшості операцій: `E7Vr9kw6qDAAJbEtpxCBocjcomLiKsTw4mFa4hoFdxNz`

---

## 3. sol_ticket — Core Protocol Program

### Purpose
Керує повним життєвим циклом протоколів (лотерей): створення, купівля позицій, оновлення полів, epoch payouts, buyouts, та staking.

### Account Structures

#### `LotteryAccount` (Protocol)

Основний on-chain стан для протоколу.

| Field | Type | Description |
|-------|------|-------------|
| `version` | `u8` | Schema version for migrations |
| `is_active` | `bool` | Whether protocol is active |
| `server_signer` | `Pubkey` | Backend wallet authorized to call restricted instructions |
| `lottery_id` | `[u8; 16]` | UUID of protocol |
| `price` | `u64` | Entry fee in lamports |
| `total_participants` | `u64` | Total number of positions |
| `is_locked` | `bool` | Global lock for epoch transitions |
| `payout_period` | `PayoutPeriod` | Epoch duration enum |
| `current_chunk_index` | `u64` | Current participant chunk |
| `current_chunk_seed` / `chunks_count` | `u32` | Chunk management |
| `token` | `Pubkey` | Ownership NFT (Token-2022) |
| `initial_creator` / `current_owner` | `Pubkey` | Creator and current owner |
| `token_mint` | `Pubkey` | LRPTN or community token mint |
| `bonding_curve` | `Pubkey` | Associated bonding curve PDA |
| `is_official` | `bool` | True for LRPTN protocols, false for community |
| `buyout_enabled` | `bool` | Whether ownership buyout is enabled |
| `current_buyout_price` | `u64` | Current buyout price |
| `hold_token` / `hold_token_amount_per_ticket` | `Pubkey` / `u64` | Token gating |
| Pool percentages | `u8` each | Distribution: points, best_field_match, token_holder, jackpot |
| Top-1 data | Various | Current top-1 PDA and amounts per pool |
| `field_size` | `u8` | 9 (3×3) or 81 (9×9) |
| `next_payout_timestamp` | `u64` | Unix timestamp for next epoch payout |
| `current_payout_epoch` | `u64` | Current epoch number |
| `max_participants` | `Option<u64>` | V2: protocol terminates when reached |
| `max_epochs` | `Option<u64>` | V2: protocol terminates when reached |
| Airdrop seeds and flags | Various | V2: airdrop pool configuration |

#### `ParticipantsChunk`

Linked-list of participant data, stored in chunks.

| Field | Type | Description |
|-------|------|-------------|
| `chunk_index` | `u64` | Index in linked list |
| `current_count` | `u16` | Number of participants in this chunk |
| `prev_chunk` | `Option<Pubkey>` | Previous chunk (linked list) |
| `participants` | `Vec<User>` | List of users in chunk |
| `rounds_history` | `Vec<Round>` | History of game rounds |

#### `PayoutPeriod` Enum

```
MIN1, MIN5, HOUR1, DAY1, WEEK1, MONTH1, MONTH3, MONTH6, YEAR1, YEAR3, YEAR5
```

### Instructions

#### `init_lottery` — Create a new protocol
- **Called by**: Server (be-ticket) after frontend initiates creation
- **Business logic**: Creates `LotteryAccount` and all 4 pool PDAs (jackpot, points, best_field_match, token_holder). Sets up seeds, payout period, pool percentages, field size, buyout config, termination limits.
- **Key accounts**: `server_signer` (signer), `lottery` (PDA), pool accounts, `system_program`

#### `init_lottery_stats_for_user` — Initialize user stats
- **Called by**: Server before a user's first position purchase
- **Business logic**: Creates `UserToLotteryStats` PDA for tracking per-user stats within a protocol.

#### `create_ticket_pda` — Prepare position PDA
- **Called by**: Server before position purchase
- **Business logic**: Creates ticket account PDA. Must be called before `create_ticket`.

#### `create_ticket` — Buy a position
- **Called by**: Server after VRF randomness is ready
- **Business logic**:
  1. Transfers entry fee from user to protocol pools (distributed by percentage)
  2. Generates game field using VRF randomness
  3. CPI to `sol_bonding_curve::mint_tokens_to_vault` — mints protocol tokens
  4. Updates participant chunk (CPI to `create_new_chunk` if full)
  5. Updates protocol statistics (total_participants, pool amounts)
  6. Checks termination conditions (max_participants, max_epochs)
  7. Emits `TicketCreatedEvent`
- **Key constraint**: Protocol must not be locked, must be active

#### `update_ticket_field` — Update position game field
- **Called by**: Server when a new round occurs
- **Business logic**: Applies next game round to position's field. Recalculates points and best_field_match. Emits `TicketFieldUpdatedEvent`.

#### `lock` / `unlock` — Protocol locking
- **Called by**: Server only
- **Business logic**: Locks/unlocks protocol during epoch transitions to prevent race conditions.

#### `create_new_chunk` — Extend participant list
- **Called by**: Via CPI from `create_ticket` when current chunk is full
- **Business logic**: Creates a new `ParticipantsChunk` linked to previous one.

#### `buyout_lottery` / `buyout_lottery1-19` — Protocol buyout
- **Called by**: Any user (if buyout is enabled)
- **Business logic**: Transfers protocol ownership. Multiple versions exist (1-19) to handle different Transfer Hook configurations and remaining account sizes. Uses prepare/finalize split pattern. Increases buyout price after each buyout.
- **Emits**: `LotteryBuyoutEvent`

#### `deposit_token_holder` — Stake tokens on position
- **Called by**: Position owner
- **Business logic**: Deposits tokens onto a position. Tokens become locked for 2 epochs (current + 2), then unlock for Token Holder pool eligibility.
- **Emits**: `TokenHolderDepositEvent`

#### `withdraw_token_holder` — Unstake tokens
- **Called by**: Position owner
- **Business logic**: Withdraws unlocked tokens from a position.
- **Emits**: `TokenHolderWithdrawEvent`

#### `force_payout` — Trigger epoch payout
- **Called by**: Any user (when payout time has passed)
- **Business logic**: Distributes pool rewards to top-1 performers. Resets epoch counters. Increments epoch number.
- **Emits**: `ForcePayoutEvent`

#### `init_airdrop_pools` — Initialize airdrop pools
- **Called by**: Server
- **Business logic**: Creates airdrop pool PDAs for protocol. Sets `awaiting_airdrop_init = false`.
- **Emits**: `AirdropInitializedEvent`

#### `update_lottery_admin` — Admin update
- **Called by**: Server only
- **Business logic**: Updates admin-level settings on protocol.

### Error Codes (83 types)

| Category | Key Errors |
|----------|-----------|
| Access | `UnauthorizedAccess`, `LotteryLocked`, `LotteryNotActive` |
| Pricing | `InvalidPrice`, `InvalidBuyoutPrice` |
| Capacity | `ChunkIsFull`, `InvalidChunkIndex` |
| Payout | `PayoutNotReady`, `NoWinnerFound`, `JackpotAlreadyClaimed` |
| Buyout | `BuyoutNotEnabled`, `InvalidBuyoutPrice` |
| Field | `InvalidFieldSize` |
| Validation | `InvalidPayoutPeriod`, `InvalidChunkAddress` |

---

## 4. sol_bonding_curve — AMM Trading Program

### Purpose
Реалізує автоматизований маркетмейкер (AMM) з використанням формули bonding curve. Кожен протокол має власну bonding curve для торгівлі токенами. Включає treasury та insurance механізми для захисту вартості токенів.

### Account Structures

#### `BondingCurve`

| Field | Type | Description |
|-------|------|-------------|
| `authority` | `Pubkey` | Server signer |
| `token_mint` | `Pubkey` | Token mint address |
| `virtual_sol_reserves` | `u64` | Virtual SOL reserves (constant, for pricing) |
| `virtual_token_reserves` | `u64` | Virtual token reserves (constant, for pricing) |
| `real_sol_reserves` | `u64` | Actual SOL held (87% of purchases) |
| `tokens_in_vault` | `u64` | Tokens in vault |
| `tokens_sold` | `u64` | Total tokens sold |
| `treasury_pda` / `insurance_pda` | `Pubkey` | Treasury (87%) and Insurance (10%) PDAs |
| `sell_spread_bps` | `u16` | Sell spread in basis points (default 500 = 5%) |
| `is_platform` | `bool` | True for LRPTN, false for community tokens |
| `cached_health_ratio` | `u64` | Health ratio × 10000 |
| Statistics fields | Various | Total bought, sold, deposited, withdrawn |

#### `BondingCurveTreasury`

Тримає 87% SOL від купівлі токенів. Використовується для buybacks та підтримки вартості.

#### `BondingCurveInsurance`

Тримає 10% SOL від купівлі токенів. Використовується як safety net для bonding curve.

### Instructions

#### `initialize_platform_token` — Create LRPTN token
- **Called by**: Server (one-time)
- **Business logic**: Creates Token-2022 mint with Transfer Hook extension for platform token (LRPTN).

#### `initialize_bonding_curve` — Create bonding curve
- **Called by**: Server
- **Business logic**: Creates bonding curve PDA with treasury and insurance accounts. Sets virtual reserves and sell spread. `is_platform = true` for LRPTN, `false` for community protocols.

#### `buy_tokens` — Buy tokens with SOL
- **Called by**: Any user
- **Business logic**:
  1. User specifies token amount to buy
  2. SOL cost calculated from bonding curve formula
  3. SOL distributed: 87% → Treasury, 10% → Insurance, 1% → Platform fee, 1% → Protocol owner, 1% → Jackpot
  4. Slippage protection via `max_sol_cost`
  5. Health ratio updated
- **Emits**: `TokensBoughtEvent`

#### `sell_tokens` — Sell tokens for SOL
- **Called by**: Any user
- **Business logic**:
  1. User specifies token amount to sell
  2. SOL payout calculated with 5% sell spread
  3. Health ratio restrictions apply (sell limits at low ratios)
  4. Slippage protection via `min_sol_payout`
  5. SOL transferred from treasury to user
- **Emits**: `TokensSoldEvent`

#### `mint_tokens_to_vault` — Mint tokens via CPI
- **Called by**: Via CPI from `sol_ticket::create_ticket`
- **Business logic**: Mints protocol tokens to vault. Only callable by server_signer.

#### `update_health_ratio` — Refresh health ratio
- **Called by**: Anyone
- **Business logic**: Recalculates `health_ratio = (Treasury + Insurance) / Value of Circulating Tokens`. Cached for performance.

#### `burn_lottery_tokens` — Burn tokens on cleanup
- **Called by**: Via CPI from cleanup operations
- **Business logic**: Burns tokens from vault when a protocol is cleaned up.

#### Close operations (`close_bonding_curve`, `close_treasury`, `close_insurance`, `close_vault_ata`)
- **Called by**: Authority only
- **Precondition**: All balances must be zero
- **Business logic**: Reclaims rent from empty accounts.

### SOL Distribution on Token Purchase

| Destination | Percentage |
|------------|-----------|
| Treasury | 87% |
| Insurance | 10% |
| Platform fee | 1% |
| Protocol owner | 1% |
| Jackpot pool | 1% |

### Error Codes (35 types)

| Category | Key Errors |
|----------|-----------|
| Access | `InvalidServerSigner`, `UnauthorizedAccess` |
| State | `BondingCurveNotActive` |
| Math | `CalculationError`, `SlippageExceeded` |
| Liquidity | `InsufficientSOLReserves`, `InsufficientTokens` |
| Health | `HealthRatioBelowMinimum`, `HealthRatioCritical` |
| Cleanup | `VaultNotEmpty`, `TreasuryNotEmpty`, `InsuranceNotEmpty` |

---

## 5. sol_token_2022_nft — NFT Minting Program

### Purpose
Створює Token-2022 NFTs для протоколів. Кожен протокол отримує ownership NFT та participation tokens (position tickets) з використанням Token-2022 extensions.

### Instructions

#### `init_lottery_token` — Create protocol NFT
- **Business logic**: Creates ownership NFT with extensions: MetadataPointer, GroupPointer, PermanentDelegate, TransferFeeConfig, TokenGroup. Also creates participation mint for positions.

#### `add_participation_mint_to_group` — Link participation mint
- **Business logic**: Associates participation mint with ownership NFT group.

#### `init_ticket_token` — Mint position token
- **Business logic**: Mints a participation token (ticket) to user. Token belongs to NFT group.

### Token-2022 Extensions Used

| Extension | Purpose |
|-----------|---------|
| MetadataPointer | Points to on-chain metadata |
| GroupPointer | Groups ownership NFT with participation tokens |
| PermanentDelegate | Allows burning/transfer by program |
| TransferFeeConfig | Fee configuration on transfers |
| TransferHook | Requires server_signer for all transfers |

---

## 6. sol_transfer_hook_nft — Transfer Authorization

### Purpose
Реалізує Transfer Hook для Token-2022. Кожен трансфер токенів вимагає `server_signer` для ко-підпису, запобігаючи несанкціонованим трансферам.

### Instructions

#### `initialize_transfer_hook`
- **Business logic**: Sets up `ExtraAccountMetaList` for mint, configuring `server_signer` as a required additional signer.

#### `transfer_hook`
- **Business logic**: Executed on every Token-2022 transfer. Validates that `server_signer` has signed the transaction. Rejects transfers without authorization.

### Error Codes
- `PlatformAdminMustSign` — server_signer signature missing
- `TransferNotAuthorized` — transfer rejected
- `InvalidPlatformAdmin` — wrong signer key

---

## 7. sol_orao_vrf — Random Number Generation

### Purpose
Інтегрується з ORAO VRF для генерації верифікованих випадкових чисел для генерації полів позицій.

### Account Structures

#### `RandomState`

| Field | Type | Description |
|-------|------|-------------|
| `lottery_id` | `[u8; 16]` | Protocol UUID |
| `randomness` | `[u8; 64]` | VRF output |
| `generated_count` | `u32` | How many randoms generated |

### Instructions

#### `request_random` — Request VRF randomness
- **Business logic**: Transfers entry fee to temp holder. Calls CPI to ORAO VRF program requesting randomness. Sets up callback to `process_random`.
- **Preconditions**: Protocol must be active and not locked.

#### `process_random` — Receive VRF callback
- **Business logic**: Called by ORAO VRF with random result. Saves to `RandomState`. Emits `RandomResponseEvent`.

#### `initialize_random_state` — Create RandomState PDA
- **Business logic**: Creates PDA for storing randomness.

---

## 8. sol_treasury — Treasury Management

### Purpose
Керує treasury PDAs для ticket purchases та transfer deposits.

### Account Structures

#### `TreasuryTicket`

| Field | Type | Description |
|-------|------|-------------|
| `current_balance` | `u64` | Current SOL balance |
| `total_deposited` / `total_withdrawn` | `u64` | Lifetime totals |
| `deposits_enabled` / `withdrawals_enabled` | `bool` | Feature flags |

#### `TreasuryTransfer`

Similar structure for transfer hook deposits. Tracks `total_transfers_processed`.

### Instructions

- `initialize_treasury_ticket` / `initialize_treasury_transfer` — Create treasury PDAs
- `deposit_to_treasury_ticket_pda` / `deposit_to_treasury_transfer_pda` — Deposit via CPI
- `get_treasury_ticket_info` / `get_treasury_transfer_info` — Read treasury state

---

## 9. Cross-Program Interaction Flow

### Protocol Creation Flow
```
1. Frontend creates transactions
2. sol_token_2022_nft::init_lottery_token → creates ownership NFT
3. sol_ticket::init_lottery → creates protocol state + pool PDAs
4. sol_bonding_curve::initialize_bonding_curve → creates AMM (community protocols)
5. (optional) sol_ticket::init_airdrop_pools → creates airdrop pools
```

### Position Purchase Flow
```
1. sol_ticket::create_ticket_pda → creates position PDA
2. sol_orao_vrf::request_random → requests VRF randomness
3. (async) sol_orao_vrf::process_random → VRF callback with randomness
4. sol_ticket::create_ticket → creates position (uses randomness)
    └── CPI → sol_bonding_curve::mint_tokens_to_vault
5. sol_token_2022_nft::init_ticket_token → mints participation token
```

### Token Trading Flow
```
1. sol_bonding_curve::buy_tokens → user buys tokens with SOL
   - SOL split: 87% treasury, 10% insurance, 1% platform, 1% owner, 1% jackpot
2. sol_bonding_curve::sell_tokens → user sells tokens for SOL
   - 5% sell spread applied
   - Health ratio restrictions at low levels
```

### Buyout Flow
```
1. sol_ticket::prepare_buyout → lock and prepare
2. Token transfer with Transfer Hook verification
3. sol_ticket::finalize_buyout → complete ownership transfer, increase price
```

### Force Payout (Epoch End)
```
1. sol_ticket::force_payout → distribute pools to top-1 winners
   - Points pool → top scorer
   - Best field match pool → best field match holder
   - Token holder pool → largest staker
   - Increment epoch, reset top-1 data
```

---

## 10. Key Constants

| Constant | Value | Usage |
|----------|-------|-------|
| `SERVER_SIGNER_VALIDATOR` | `E7Vr9kw6qDAAJbEtpxCBocjcomLiKsTw4mFa4hoFdxNz` | Server wallet for signing |
| ORAO VRF Program | `VRFCBePmGTpZ234BhbzNNzmyg39Rgdd6VgdfhHwKypU` | VRF provider |

### PDA Seeds

| Seed | Purpose |
|------|---------|
| `"lottery"` + lottery_id | LotteryAccount |
| `"participants"` + lottery_id + chunk_index | ParticipantsChunk |
| `"platform_token_mint"` | LRPTN token mint |
| `"community_token_mint"` + lottery_id | Community token mint |
| `"platform_bonding_curve"` / `"community_bonding_curve"` | Bonding curve PDAs |
| `"treasury_ticket"` / `"treasury_transfer"` | Treasury PDAs |
