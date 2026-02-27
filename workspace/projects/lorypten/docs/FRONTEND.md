# Frontend Documentation — Next.js App

**Оновлено:** 2026-02-27

---

## 1. Overview

Frontend — це Next.js 15 application з використанням App Router, React 19, та TypeScript. Використовує Server Actions для доступу до даних (Prisma) та Anchor для blockchain interactions в server scope.

---

## 2. Application Structure

```
frontend/next/src/
├── app/                              # Pages and routes (App Router)
│   ├── page.tsx                       # Home — protocol list
│   ├── layout.tsx                       # Root layout with providers
│   ├── protocol/                       # Protocol pages
│   ├── createProtocol/                  # Protocol creation form
│   ├── buyouts/                        # Buyout-enabled protocols
│   ├── tokens/                          # User's NFT tokens
│   ├── about/                           # About page
│   ├── unauthorized/                     # Access denied
│   ├── (marketing)/                     # Marketing pages
│   └── api/                             # API routes
├── requests/                          # Server Actions (Prisma + Anchor)
├── customComponents/                   # Reusable UI components
├── components/                        # shadcn/ui base components
├── providers/                          # React context providers
├── utils/                             # Utility functions
├── constants/                         # App constants
├── types/                             # TypeScript types
├── hooks/                             # Custom hooks
├── store/                             # Jotai atoms
└── services/                          # External service clients
```

---

## 3. Pages & Routes

| Route | Type | Description |
|-------|------|-------------|
| `/` | Server | Home page — list of all protocols with global statistics |
| `/protocol/[pubkey]` | Server | Protocol detail page with tabs |
| `/protocol/[pubkey]/position/[positionPubkey]` | Server | Position detail page |
| `/createProtocol` | Server | Create new protocol form |
| `/buyouts` | Server | List of buyout-enabled protocols |
| `/tokens` | Client | User's Token-2022 NFTs list |
| `/tokens/[address]` | Client | Token detail view |
| `/about` | Client | Platform information page |
| `/unauthorized` | Client | Access denied page for non-whitelisted wallets |
| `/(marketing)/trading-info` | Client | Trading fees and math explanation |

### Protocol Detail Page Tabs

Protocol page (`/protocol/[pubkey]`) має sub-navigation з цими секціями:

| Tab | Component | Description |
|-----|-----------|-------------|
| Details | `protocolDetails.view.tsx` | Protocol configuration, pools, stats |
| Description | `protocolDescription.view.tsx` | Protocol description text |
| My Positions | `protocolMyPositionsContainer.tsx` | User's positions in this protocol |
| History | `protocolHistory.container.tsx` | Charts and tables: epoch payouts, staking, positions |
| Top-1 | `protocolTopOne.view.tsx` | Current top-1 winners per pool |
| Trading | `poolTrading.container.tsx` | Bonding curve trading (buy/sell tokens) |
| Buyout | `protocolBuyout.container.tsx` | Protocol buyout interface |

### History Sub-sections

| Component | Data Source |
|-----------|------------|
| `EpochPayoutsChart.tsx` | Epoch payout amounts over time |
| `PositionsByEpochChart.tsx` | Number of positions per epoch |
| `StakingByEpochChart.tsx` | Staking amounts per epoch |
| `EpochPayoutHistoryTable.tsx` | Detailed epoch payout records |
| `FieldPayoutHistoryTable.tsx` | Field (jackpot) payout records |
| `PositionPurchaseHistoryTable.tsx` | Purchase transaction records |
| `TokenStakingStatsTable.tsx` | Staking statistics table |

---

## 4. User Flows

### Flow 1: Connect Wallet & Access Platform

**Preconditions**: User has a Solana wallet (Phantom, Solflare, etc.)

**Steps**:
1. User opens the site
2. `AuthGuardProvider` checks if wallet is connected
3. If connected → verify wallet pubkey is in `AUTHORIZED_KEYS` whitelist
4. If authorized → show platform content
5. If not authorized → redirect to `/unauthorized`
6. If not connected within 2.5s timeout → redirect to `/unauthorized`

**Edge cases**:
- Wallet disconnects mid-session → next navigation triggers re-check
- Multiple wallets → first connected wallet is used

### Flow 2: Browse Protocols (Home Page)

**Steps**:
1. Server Action `GetListProtocols()` fetches protocols from Prisma
2. Server Action `GetGlobalStatistics()` fetches global stats
3. Protocols displayed as cards (`protocolCartView.tsx`) with filtering
4. Global statistics displayed in `GlobalStatisticsSection`

**Filters** (`ShadcnProtocolFiltersPanel.tsx`):
- Sort by: total users, jackpot amount, entry fee, creation date
- Filter by: duration, field size, active/completed status

### Flow 3: Create Protocol

**Preconditions**: Connected and authorized wallet

**Steps**:
1. User navigates to `/createProtocol`
2. Fills form with:
   - Entry fee (in SOL)
   - Payout duration (MIN_1 through YEAR_5)
   - Field size (3×3 or 9×9)
   - Pool distribution percentages (must sum to 100%)
   - Buyout enabled/disabled + initial price
   - Max participants / max epochs (optional)
   - Airdrop configuration (4 optional pools)
   - Protocol image
3. Form validated via Yup schema (`createProtocol/schema.ts`)
4. On submit:
   a. Image uploaded to ImageKit
   b. Token metadata uploaded to Supabase
   c. Multiple Solana transactions built and signed:
      - Create ALT (Address Lookup Table)
      - Create protocol (init_lottery_token + init_lottery + init_bonding_curve)
      - (Optional) Initialize airdrop pools
   d. Transactions sent sequentially via Signing Service
5. Backend picks up `LotteryInitializedEvent` and creates DB records

**Validation rules**:
- Entry fee: minimum amount enforced
- Percentages: points + best_field + token_holder + jackpot = 100
- Duration: must be valid `PayoutPeriod`
- Buyout price: must be > 0 if enabled

### Flow 4: Buy Position (Ticket)

**Preconditions**: Connected wallet, protocol is ACTIVE, not locked

**Steps**:
1. User views protocol detail page
2. Clicks "Create Position" button
3. Frontend calls `createPositionInProtocol()` server action
4. Server action:
   a. Builds `request_random` + `create_ticket_pda` transactions
   b. Signs via Signing Service
   c. User signs with wallet
   d. Sends to Solana
5. VRF generates randomness → `RandomResponseEvent`
6. Backend processes event → calls `create_ticket_signed_by_service()`
   - Tx1: Create ATA
   - Tx2: Create ticket
   - Tx3: Mint participation token
7. `TicketCreatedEvent` emitted → backend updates DB
8. Frontend reads updated data via Prisma

**Edge cases**:
- VRF callback delayed → backend polls with timeout
- Protocol locked during epoch transition → purchase rejected
- Max participants reached → protocol closes

### Flow 5: View & Update Position

**Steps**:
1. User navigates to `/protocol/[pubkey]/position/[positionPubkey]`
2. Server fetches position data + field + scores + ranks
3. Position page shows:
   - Game field visualization (current field vs winning field)
   - Score and ranking
   - Staking info (locked/unlocked tokens)
   - Field update history

**Field update** (triggered by backend when rounds occur):
1. Backend receives `TicketFieldUpdatedEvent`
2. Updates field in DB
3. Recalculates points and best_field_match
4. Frontend shows updated field on next load/refresh

### Flow 6: Stake Tokens (Token Holder Deposit)

**Preconditions**: User owns position, has tokens to stake

**Steps**:
1. User views their position page
2. Enters amount to stake
3. Calls `depositTokenHolder()` server action
4. Transaction built and signed
5. Tokens transferred to position PDA
6. `TokenHolderDepositEvent` → backend creates `TokenDeposit` record
7. Tokens locked for 2 epochs, then unlock for Token Holder pool rewards

**Business rules**:
- Deposit lock: tokens locked for `current_epoch + 2` epochs
- Only unlocked tokens count toward Token Holder pool ranking
- Multiple deposits create separate `TokenDeposit` records

### Flow 7: Withdraw Staked Tokens

**Preconditions**: User has unlocked tokens (past lock period)

**Steps**:
1. User views position with unlocked tokens
2. Clicks "Withdraw"
3. Calls `withdrawTokenHolder()` server action
4. Only unlocked tokens can be withdrawn
5. `TokenHolderWithdrawEvent` → backend marks deposits as withdrawn

### Flow 8: Force Payout (Epoch End)

**Preconditions**: `next_payout_timestamp` has passed

**Steps**:
1. User sees "Force Payout" button on protocol page (visible when payout is due)
2. Calls `forcePayoutProtocol()` server action
3. Transaction triggers `force_payout` instruction
4. `ForcePayoutEvent` → backend:
   - Records epoch payout history
   - Distributes pool rewards to top-1 winners
   - Resets epoch counters
   - Increments epoch number

### Flow 9: Buy/Sell Tokens (Trading)

**Steps (Buy)**:
1. User navigates to protocol's Trading tab
2. Enters SOL amount
3. Frontend calculates expected tokens via bonding curve formula
4. User submits → `buyTokens()` server action
5. Transaction built with `sol_bonding_curve::buy_tokens`
6. `TokensBoughtEvent` → backend records trade

**Steps (Sell)**:
1. User enters token amount to sell
2. Frontend calculates expected SOL (minus 5% spread)
3. User submits → `sellTokens()` server action
4. Transaction built with `sol_bonding_curve::sell_tokens`
5. `TokensSoldEvent` → backend records trade

**Trading page components**:
- `TradingForm.tsx` — Buy/sell form with slippage settings
- `TradingChart.tsx` / `BondingCurveChart.tsx` — Price charts (Recharts)
- `TopHolders.tsx` — Top token holders table
- `TransactionHistory.tsx` — Recent trades

### Flow 10: Protocol Buyout

**Preconditions**: Protocol has `buyout_enabled = true`

**Steps**:
1. User views Buyout tab on protocol page
2. Sees current buyout price
3. Clicks "Buyout" → calls buyout server action
4. Transaction includes multiple versions (buyoutLottery1-19) for Transfer Hook
5. `LotteryBuyoutEvent` → backend transfers ownership, increases price

**Business rules**:
- Buyout price increases after each buyout
- New owner receives 1% of bonding curve trading fees
- Any user can buyout if they can pay the price

---

## 5. Key Components

### Layout Components

| Component | Purpose |
|-----------|---------|
| `ui-layout.tsx` | Main layout: header, navigation, footer, wallet button |
| `burgerMenu.tsx` | Mobile navigation menu |
| `subHeader.tsx` | Sub-header with context info |

### Protocol Components

| Component | Purpose |
|-----------|---------|
| `protocolCartView.tsx` | Protocol card for list views |
| `protocolBuyoutCard.tsx` | Buyout-specific card |
| `protocolExampleField.tsx` | Visual example of game field |
| `protocolTableInfo.tsx` | Protocol details table |
| `protocolTokenTableInfo.tsx` | Token information table |
| `ProtocolAirdropInfo.tsx` | Airdrop pool configuration display |
| `EpochCountdownBlock.tsx` | Countdown timer to next epoch |
| `ProtocolImage.tsx` | Protocol image with ImageKit |

### Position Components

| Component | Purpose |
|-----------|---------|
| `positionField.tsx` | Game field visualization for a position |
| `availableField.tsx` | Available field display (ex-tickets) |
| `historyField.tsx` | Historical field display |

### Trading Components

| Component | Purpose |
|-----------|---------|
| `TradingForm.tsx` | Buy/sell token form |
| `TradingChart.tsx` | Price chart (candlestick/line) |
| `BondingCurveChart.tsx` | Bonding curve visualization |
| `TopHolders.tsx` | Token holder ranking |
| `TransactionHistory.tsx` | Trade history list |

### Token Components

| Component | Purpose |
|-----------|---------|
| `tokens-list-feature.tsx` | List of user's Token-2022 NFTs |
| `token-card.tsx` | Individual token card |
| `WalletTokenPicker.tsx` | Token selector from wallet |

### Statistics

| Component | Purpose |
|-----------|---------|
| `GlobalStatisticsSection.tsx` | Platform-wide statistics display |

---

## 6. Forms & Validation

### Create Protocol Form

| Field | Type | Validation |
|-------|------|-----------|
| `entryFee` | number | Required, minimum enforced |
| `duration` | select | Required, one of PayoutPeriod values |
| `fieldSize` | select | Required, 9 or 81 |
| `pointsPoolPercentage` | number | Required, 0-100 |
| `bestFieldMatchPoolPercentage` | number | Required, 0-100 |
| `tokenHolderPoolPercentage` | number | Required, 0-100 |
| `jackpotPoolPercentage` | number | Required, 0-100 |
| `buyoutEnabled` | boolean | Optional |
| `initialBuyoutPrice` | number | Required if buyout enabled |
| `maxParticipants` | number | Optional (null = unlimited) |
| `maxEpochs` | number | Optional (null = unlimited) |
| `hasPointsAirdrop` | boolean | Optional |
| `hasBestFieldAirdrop` | boolean | Optional |
| `hasTokenHolderAirdrop` | boolean | Optional |
| `hasJackpotAirdrop` | boolean | Optional |
| `image` | file | Optional |

**Cross-field validation**: All 4 pool percentages must sum to 100%.

### Trading Form

| Field | Type | Validation |
|-------|------|-----------|
| `amount` | number | Required, positive |
| `type` | "BUY" \| "SELL" | Required |
| `slippage` | number | Optional, default varies |

---

## 7. Real-Time Updates

Frontend використовує **Pusher** для real-time event notifications.

| Channel Pattern | Events | Usage |
|----------------|--------|-------|
| `ticket-specific-${lotteryPubkey}` | `buyout`, updates | Protocol-specific real-time updates |

Pusher client ініціалізується в components, що потребують real-time data (наприклад, protocol detail page). Updates тригерять data refetch через Prisma.

---

## 8. State Management

| Technology | Usage |
|-----------|-------|
| **Jotai** | Global atoms for cluster selection, wallet state |
| **React Hook Form** | Form state in Create Protocol |
| **Server Components** | Data fetching via Prisma (no client state needed) |
| **URL state** | Protocol pubkey and position pubkey in URL params |

---

## 9. Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Next.js 15 (App Router) |
| **UI** | React 19, TypeScript |
| **Styling** | Tailwind CSS 4 |
| **Components** | Radix UI (shadcn/ui) |
| **Animations** | Framer Motion |
| **Forms** | React Hook Form, Yup |
| **Charts** | Recharts |
| **State** | Jotai (atoms) |
| **Data Access** | Prisma ORM (Server Actions) |
| **Blockchain** | Anchor (server-side), @solana/wallet-adapter-react (client) |
| **Real-time** | Pusher (WebSocket) |
| **Images** | ImageKit |
| **Metadata Storage** | Supabase S3 |
| **Validation** | Yup |

---

## 10. Security & Access Control

### Wallet Authorization Flow

1. User connects wallet
2. Frontend checks pubkey against `AUTHORIZED_KEYS` whitelist
3. If not in whitelist → redirect to `/unauthorized`
4. Timeout: 2.5s → auto-redirect if not authorized

### AuthGuardProvider

- Checks wallet connection on every route change
- Handles wallet disconnect/reconnect
- Manages authorization state

---

## 11. Key Features

### Protocol Management
- Create protocols with custom parameters
- View protocol details (pools, stats, history)
- Protocol filtering and sorting
- Real-time updates via Pusher

### Position Management
- Buy positions (tickets) with VRF randomness
- View game field visualization
- Track scores and rankings
- Field update history

### Trading
- Bonding curve price charts
- Buy/sell tokens with slippage protection
- Top token holders ranking
- Trade history

### Staking
- Deposit tokens on positions
- 2-epoch lock period
- Withdraw unlocked tokens
- Token holder pool rewards

### Buyout
- View buyout-enabled protocols
- Buyout at current price
- Price increases after each buyout
- Transfer Hook verification
