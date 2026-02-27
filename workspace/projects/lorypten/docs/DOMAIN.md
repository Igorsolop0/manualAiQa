# Domain & Business Rules

**Оновлено:** 2026-02-27

---

## 1. Core Domain Concepts

---

### 1.1 Protocol (Lottery)

A protocol is the central entity. It represents a game instance where users buy positions and compete for rewards.

| Property | Description |
|----------|-------------|
| **Identity** | On-chain PDA with UUID (`lottery_id`) |
| **Ownership** | Has `initial_creator` and `current_owner` (transferable via buyout) |
| **Token** | Each protocol has an associated token traded on a bonding curve |
| **NFT** | Ownership NFT (Token-2022) represents protocol ownership |
| **State** | `ACTIVE` or `LOCKED` (during epoch transitions) |
| **Lifecycle** | Runs indefinitely unless `maxParticipants` or `maxEpochs` is reached |

---

### 1.2 Position (Ticket)

A position represents a user's participation in a protocol. Each position has a game field.

| Property | Description |
|----------|-------------|
| **Identity** | On-chain PDA, linked to user and protocol |
| **Game field** | Array of values (9 for 3×3, 81 for 9×9) |
| **Scoring** | Points calculated from field proximity to winning state |
| **Staking** | Tokens can be staked on position for Token Holder pool |
| **Token** | Participation token (Token-2022, member of protocol's NFT group) |

---

### 1.3 Epoch

Time period after which rewards are distributed to top-1 performers.

| Property | Description |
|----------|-------------|
| **Duration** | Configurable: MIN_1 to YEAR_5 |
| **Trigger** | `force_payout` instruction when `next_payout_timestamp` passed |
| **Payout** | Top-1 in each pool receives that pool's accumulated funds |
| **Reset** | After payout, pool accumulations and top-1 data reset |
| **Counter** | `current_payout_epoch` increments each cycle |

---

### 1.4 Pools

Each protocol has 4 reward pools. Entry fees are distributed by percentage.

| Pool | Competition | Winner |
|------|------------|--------|
| **Points Pool** | Field matching score | Highest scorer this epoch |
| **Best Field Match Pool** | Number of correct positions | Most values in correct place |
| **Token Holder Pool** | Staked (unlocked) token amount | Largest staker |
| **Jackpot Pool** | Game field completion | First to achieve winning field `[1,2,3,...,N]` |

---

### 1.5 Bonding Curve (AMM)

Automated market maker for protocol tokens.

| Property | Description |
|----------|-------------|
| **Formula** | Constant product: `virtual_sol × virtual_token = k` |
| **Spread** | 5% sell spread (500 bps) |
| **Health Ratio** | `(Treasury + Insurance) / Circulating Token Value` |
| **Revenue split** | 87% treasury, 10% insurance, 1% platform, 1% owner, 1% jackpot |

---

### 1.6 User

A wallet address that has interacted with the platform.

| Property | Description |
|----------|-------------|
| **Identity** | Solana wallet public key |
| **Username** | Auto-generated on first interaction |
| **Tracking** | Total earnings, withdrawn earnings, perfect combinations won |

---

## 2. Invariants & Constraints

---

### 2.1 Protocol Invariants

1. **Pool percentages MUST sum to 100%**: `points + best_field_match + token_holder + jackpot = 100`
2. Protocol MUST have exactly 4 pools created on-chain
3. Protocol MUST be ACTIVE and not LOCKED for position purchases
4. `field_size` MUST be 9 (3×3) or 81 (9×9) — cannot change after creation
5. `payout_period` cannot change after creation
6. `entry_fee` cannot change after creation
7. `server_signer` must match known server wallet for restricted operations

---

### 2.2 Position Invariants

1. One position per user per `create_ticket` transaction
2. Position's initial field is generated from VRF randomness — non-deterministic
3. Points can only increase or reset (reset only at epoch boundary for pool winner)
4. `best_field_match_count` represents current number of correctly placed values
5. A position belongs to exactly one protocol

---

### 2.3 Epoch Invariants

1. Epoch number monotonically increases
2. `next_payout_timestamp = current_time + payout_period` after each payout
3. Force payout can only be called when `current_time >= next_payout_timestamp`
4. Protocol is LOCKED during payout processing (prevents race conditions)
5. Top-1 data resets after each payout

---

### 2.4 Staking Invariants

1. Deposited tokens are locked for 2 epochs: `unlock_epoch = deposit_epoch + 2`
2. Only unlocked tokens count toward Token Holder pool ranking
3. Withdrawal only allowed for unlocked tokens (`current_epoch >= unlock_epoch`)
4. Multiple deposits per position allowed, each tracked separately

---

### 2.5 Bonding Curve Invariants

1. `virtual_sol_reserves` and `virtual_token_reserves` are constants (never change)
2. `real_sol_reserves` = actual SOL held (87% from purchases minus withdrawals)
3. Health Ratio ≥ 1.0 for normal operation; selling restricted below certain thresholds
4. Sell spread (5%) is always applied to sell transactions
5. Token price increases as supply increases (bonding curve property)

---

### 2.6 Buyout Invariants

1. Buyout price increases after each buyout
2. New owner receives ownership NFT
3. Previous owner receives buyout payment
4. Protocol continues operating with new owner

---

## 3. Calculations & Formulas

---

### 3.1 Bonding Curve Price Calculation

```
Token Price = virtual_sol_reserves / virtual_token_reserves

Buy Cost = (tokens_requested × virtual_sol_reserves) / (virtual_token_reserves - tokens_requested)

Sell Payout = (tokens_sold × real_sol_reserves) / (virtual_token_reserves + tokens_sold) × (1 - sell_spread)
```

Where `sell_spread = 5% (500 bps)`

---

### 3.2 SOL Distribution on Token Purchase

| Destination | Amount |
|------------|--------|
| Treasury PDA | 87% of SOL paid |
| Insurance PDA | 10% of SOL paid |
| Platform fee wallet | 1% of SOL paid |
| Protocol owner | 1% of SOL paid |
| Jackpot pool | 1% of SOL paid |

---

### 3.3 Health Ratio

```
Health Ratio = (Treasury Balance + Insurance Balance) / Value of Circulating Tokens

Value of Circulating Tokens = tokens_sold × current_price
```

The ratio is cached and updated periodically. Stored as `cached_health_ratio × 10000` (for integer precision).

---

### 3.4 Score Calculation

Points are calculated based on how close the position's field values are to their correct positions.

**The exact formula:**
- Each value in the field has a "correct position" (value N should be at index N-1)
- Points increase when a round moves values closer to their correct positions
- `potential_points` represents the maximum points achievable from current field state

---

### 3.5 Buyout Price Progression

> **Open question for PO/Dev**: What is the exact formula for buyout price increase after each buyout? The code shows `current_buyout_price` is updated but the multiplication factor is in the smart contract.

---

## 4. State Machines & Lifecycles

---

### 4.1 Protocol Lifecycle

```
┌──────────────────────────┐
│     CREATION            │
│ (init_lottery_token +   │
│  init_lottery +         │
│  init_bonding_curve)    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐     ┌──▶│     ACTIVE              │◀──┐
│ - Positions can be bought│     │
│ - Trading active        │     │
│ - Staking active       │     │
└─────┬──────────┬──────────┘
      │          │
      │ Lock     │ Buyout
      ▼          │
┌─────────────┐   │
│    LOCKED   │   │
│ (epoch      │   │
│  transition)│   │
└──────┬──────┘   │
       │          │
       │ Unlock   │
       │          │
       └──────────┘
                  │
                  │ (max_participants reached OR
                  │  max_epochs reached OR
                  │  is_active = false)
                  │
                  ▼
┌──────────────────────────┐
│     COMPLETED          │
│ - No new positions     │
│ - Trading may continue │
│ - State = LOCKED      │─────┘
└──────────────────────────┘
    (buyout still possible)
```

---

### 4.2 Epoch Lifecycle

```
┌─────────────────────┐
│   EPOCH N STARTS   │
│ (after payout or    │
│  protocol creation)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   ACCUMULATING     │
│ - Positions bought  │
│ - Fees → pools     │
│ - Scores tracked   │
│ - Top-1 updated    │
│ - Staking active   │
└──────────┬──────────┘
           │
           │ next_payout_timestamp reached
           ▼
┌─────────────────────┐
│   PAYOUT PENDING  │
│ - Any user can    │
│   call force_payout│
└──────────┬──────────┘
           │
           │ force_payout called
           ▼
┌─────────────────────┐
│ PAYOUT PROCESSING  │
│ - Protocol locked  │
│ - Pool → top-1    │
│ - Epoch recorded   │
│ - Staking snapshot │
│ - Counters reset   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ EPOCH N+1 STARTS   │
│ - Protocol unlocked │
│ - New accumulation │
└─────────────────────┘
```

---

### 4.3 Token Staking Lifecycle

```
     DEPOSIT (epoch E)
           │
           │ Token locked
           ▼
     EPOCH E: locked
           │
           │ (next epoch)
           ▼
  EPOCH E+1: locked
           │
           │ (next epoch)
           ▼
  EPOCH E+2: UNLOCKED ← counts toward Token Holder ranking
           │
           │ User calls withdraw
           ▼
      WITHDRAWN
```

---

### 4.4 Position Field Evolution

```
    VRF Randomness
           │
           ▼
   INITIAL FIELD
   (random arrangement of values)
           │
           │ Round 1 (direction + diagonal)
           ▼
   FIELD STATE 1
   → score calculated
           │
           │ Round 2
           ▼
   FIELD STATE 2
   → score recalculated
           │
           │ ...
           ▼
   WINNING FIELD [1,2,3,...,N]
   → JACKPOT!
   (or protocol ends by epoch/participant limit)
```

---

## 5. Pool Distribution Rules

---

### 5.1 On Position Purchase (Entry Fee Distribution)

The entry fee is split across 4 pools based on protocol-configured percentages:

| Pool | Payout trigger | Winner criteria |
|------|---------------|-----------------|
| Points | End of epoch | Highest cumulative score |
| Best Field Match | End of epoch | Most values in correct positions |
| Token Holder | End of epoch | Most unlocked staked tokens |
| Jackpot | Achieving winning field | First player to get `[1,2,...,N]` |

---

### 5.2 On Token Purchase (Bonding Curve)

| Destination | % | Description |
|------------|---|-------------|
| Treasury | 87% | Backs token value, used for buybacks |
| Insurance | 10% | Safety net for health ratio |
| Platform | 1% | Platform revenue |
| Owner | 1% | Protocol owner revenue |
| Jackpot | 1% | Additional jackpot funding |

---

## 6. Game Field Rules

---

### 6.1 3×3 Field (field_size = 9)

- 9 cells, values 1-9
- Winning state: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`
- 4 diagonals possible

---

### 6.2 9×9 Field (field_size = 81)

- 81 cells, values 1-81
- Winning state: `[1, 2, 3, ..., 81]`
- More diagonals, longer games

---

### 6.3 Round Mechanics

Each round specifies:
- **Direction**: UpLeft, UpRight, DownLeft, DownRight
- **Diagonal index**: which diagonal line to shift

Values along the selected diagonal shift one position in the given direction. This creates a sliding puzzle mechanic.

---

### 6.4 Scoring Rules

- Points increase when a round moves values closer to their target positions
- `best_field_match_count`: number of values currently at their correct index
- Jackpot: awarded when ALL values are at their correct positions

---

## 7. Protocol Termination Conditions (V2)

A protocol terminates (becomes COMPLETED) when any of these conditions is met:

| Condition | Source |
|-----------|--------|
| `max_participants` reached | `total_participants >= max_participants` |
| `max_epochs` reached | `current_payout_epoch >= max_epochs` |
| Jackpot won | Winning field achieved (game field = sorted sequence) |
| Admin closure | `is_active = false` set by admin |

**When terminated:**
- No new positions can be purchased
- Existing positions retain their data
- Trading on bonding curve may continue
- Buyout may still be possible

---

## 8. Airdrop System (V2)

Protocols can optionally enable 4 types of airdrop pools:

| Airdrop Pool | Mirrors |
|-------------|---------|
| Points Airdrop | Points Pool |
| Best Field Airdrop | Best Field Match Pool |
| Token Holder Airdrop | Token Holder Pool |
| Jackpot Airdrop | Jackpot Pool |

Airdrop pools are initialized via a separate instruction (`init_airdrop_pools`) after protocol creation. The `awaiting_airdrop_init` flag tracks initialization status.

> **Open question for PO/Dev**: How exactly are airdrop pool rewards distributed? Is it the same as regular pools (top-1 per epoch) or a different distribution model?

---

## 9. Testing Guidelines for Business Rules

### 9.1 Protocol Creation

**Test cases:**
- Verify pool percentages sum to exactly 100%
- Test with invalid percentage combinations (> 100%, < 100%)
- Verify protocol is created with correct state (ACTIVE)
- Test with both field_size options (9, 81)
- Test with all payout period options (MIN_1 to YEAR_5)

---

### 9.2 Position Purchase

**Test cases:**
- Verify VRF randomness produces different initial fields
- Verify only one position per transaction
- Verify points calculation is correct
- Verify `best_field_match_count` is accurate
- Test purchase when protocol is LOCKED (should fail)
- Test purchase after protocol is COMPLETED (should fail)

---

### 9.3 Epoch Payout

**Test cases:**
- Verify force_payout fails before `next_payout_timestamp`
- Verify force_payout succeeds after `next_payout_timestamp`
- Verify protocol is LOCKED during payout processing
- Verify top-1 winners receive correct amounts
- Verify pool accumulations reset after payout
- Verify epoch number increments

---

### 9.4 Staking

**Test cases:**
- Verify tokens are locked for 2 epochs after deposit
- Verify unlocked tokens count toward Token Holder ranking
- Verify locked tokens do NOT count toward ranking
- Verify withdrawal fails during lock period
- Verify withdrawal succeeds after unlock epoch
- Test multiple deposits on same position

---

### 9.5 Bonding Curve Trading

**Test cases:**
- Verify buy price calculation matches formula
- Verify sell payout includes 5% spread
- Verify SOL distribution (87/10/1/1/1 split)
- Verify health ratio calculation is correct
- Test trading when health ratio < 1.0 (should restrict sells)
- Verify token price increases as supply increases

---

### 9.6 Game Field & Scoring

**Test cases:**
- Verify initial field is random and non-deterministic
- Verify round application shifts values correctly
- Verify points increase when values move closer to correct positions
- Verify `best_field_match_count` is accurate
- Test winning field detection (jackpot award)
- Verify 3×3 vs 9×9 field differences

---

### 9.7 Protocol Termination

**Test cases:**
- Verify no new positions after `max_participants` reached
- Verify no new positions after `max_epochs` reached
- Verify protocol becomes COMPLETED when jackpot won
- Verify trading continues after termination
- Verify buyout still possible after termination

---

### 9.8 Buyout

**Test cases:**
- Verify buyout price increases after each transaction
- Verify new owner receives ownership NFT
- Verify previous owner receives payment
- Verify protocol continues operating with new owner
- Test buyout on COMPLETED protocol (should work)

---

## 10. Edge Cases to Test

### 10.1 Concurrency

- Multiple users buying positions simultaneously
- Force payout called during position purchase
- Staking and unstaking during epoch transition

### 10.2 Boundary Conditions

- Exactly 100% pool distribution
- Pool distribution at 99.99% or 100.01%
- Zero tokens staked at epoch end
- Single position in protocol
- Empty protocol (no positions yet)

### 10.3 Invalid States

- Attempt to buy position on COMPLETED protocol
- Attempt to withdraw before unlock epoch
- Attempt to force payout before timestamp
- Attempt to sell tokens when health ratio < threshold

---

## 11. QA Checklist

### Protocol Setup
- [ ] Pool percentages sum to 100%
- [ ] Field size is 9 or 81
- [ ] Payout period is valid
- [ ] Entry fee is positive
- [ ] Server signer is correct
- [ ] Airdrop pools initialized (if enabled)

### Position Management
- [ ] VRF randomness is non-deterministic
- [ ] Points calculated correctly
- [ ] Best field match count accurate
- [ ] One position per transaction
- [ ] Field updates work correctly

### Epoch & Payout
- [ ] Force payout only after timestamp
- [ ] Protocol locks during payout
- [ ] Top-1 receives correct amount
- [ ] Pool accumulations reset
- [ ] Epoch counter increments

### Staking
- [ ] 2-epoch lock enforced
- [ ] Only unlocked tokens count
- [ ] Withdrawal works after unlock
- [ ] Multiple deposits tracked separately

### Trading
- [ ] Buy price matches formula
- [ ] Sell includes 5% spread
- [ ] SOL split is 87/10/1/1/1
- [ ] Health ratio calculated correctly
- [ ] Price increases with supply

### Termination
- [ ] Max participants stops purchases
- [ ] Max epochs stops purchases
- [ ] Jackpot triggers COMPLETED state
- [ ] Trading continues after termination
- [ ] Buyout works after termination
