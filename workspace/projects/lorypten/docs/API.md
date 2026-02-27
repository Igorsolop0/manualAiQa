# API Documentation — QA Focused

**Оновлено:** 2026-02-27

---

## 1. Overview

The platform does **not** have a traditional REST API. Instead, it uses four communication patterns:

1. **Server Actions** (Next.js) — frontend reads/writes via Prisma and Anchor
2. **Backend HTTP** (be-ticket) — minimal endpoints (health check)
3. **Signing Service API** — transaction signing endpoints
4. **Frontend API Routes** — notification webhooks from backend

---

## 2. Server Actions (Frontend → Database)

All server actions are in `frontend/next/src/requests/` and use `"use server"` directive. They execute on the server side and access PostgreSQL via Prisma.

---

### 2.1 Protocol Domain

#### `GetListProtocols()`

- **File**: `requests/protocol/getListProtocols.ts`
- **Description**: Fetch paginated list of protocols with optional filters
- **Request**: Filter params (state, duration, fieldSize, sort)
- **Response**: `Lottery[]` with related `BondingCurve`
- **DB Query**: `prisma.lottery.findMany()` with dynamic where/orderBy

#### `GetProtocol(pubkey: string)`

- **File**: `requests/protocol/getProtocol.ts`
- **Description**: Fetch single protocol by its on-chain pubkey
- **Response**: `Lottery` with `BondingCurve`, `Ticket[]`, stats
- **DB Query**: `prisma.lottery.findUnique()` with includes

#### `GetBuyoutProtocols()`

- **File**: `requests/protocol/getBuyoutProtocols.ts`
- **Description**: Fetch protocols that have buyout enabled
- **Response**: `Lottery[]` where `buyoutEnabled = true`

#### `GetBuyoutStats(lotteryPubkey: string)`

- **File**: `requests/protocol/getBuyoutStats.ts`
- **Description**: Fetch buyout statistics for a protocol
- **Response**: Buyout count, prices, last buyout date

#### `GetProtocolStats(lotteryPubkey: string)`

- **File**: `requests/protocol/getProtocolStats.ts`
- **Description**: Fetch detailed protocol statistics
- **Response**: Pool amounts, top-1 data, user counts

#### `GetProtocolFromChain(pubkey: string)`

- **File**: `requests/protocol/getProtocolFromChain.ts`
- **Description**: Fetch protocol data directly from Solana blockchain (not DB)
- **Response**: On-chain `LotteryAccount` data
- **Usage**: Verification and cross-checking

#### `CreateProtocol(formData)`

- **File**: `requests/protocol/createProtocol.ts`
- **Description**: Build and sign protocol creation transactions
- **Request**: Form data (entry fee, duration, pools, buyout config, airdrop config)
- **Response**: Transaction signatures
- **Side effects**: Creates on-chain accounts (does NOT write to DB — backend handles that via events)

---

### 2.2 Position Domain

#### `GetPositionFromPDA(positionPubkey: string)`

- **File**: `requests/position/getPositionFromPDA.ts`
- **Description**: Fetch position details from DB
- **Response**: `Ticket` with `TicketField`, `UserTicketScore`

#### `GetPositionsByProtocol(lotteryPubkey: string)`

- **File**: `requests/position/getPositionsByProtocol.ts`
- **Description**: Fetch all positions for a protocol
- **Response**: `Ticket[]` with fields and scores

#### `GetPositionRanks(ticketPubkey: string, lotteryPubkey: string)`

- **File**: `requests/position/getPositionRanks.ts`
- **Description**: Fetch ranking data for a position (points rank, staking rank, best match rank)
- **Response**: Position rankings across different pools

#### `CreatePositionInProtocol(lotteryPubkey, userPubkey)`

- **File**: `requests/position/createPositionInProtocol.ts`
- **Description**: Build VRF request and ticket PDA creation transactions
- **Response**: Partially signed transactions for user to sign
- **Side effects**: Initiates on-chain position creation flow

#### `UpdatePositionField(ticketPubkey, userPubkey)`

- **File**: `requests/position/updatePositionField.ts`
- **Description**: Build field update transaction
- **Response**: Transaction for user to sign

#### `DepositTokenHolder(ticketPubkey, amount)`

- **File**: `requests/position/depositTokenHolder.ts`
- **Description**: Build token staking transaction
- **Response**: Transaction for user to sign

#### `WithdrawTokenHolder(ticketPubkey, amount)`

- **File**: `requests/position/withdrawTokenHolder.ts`
- **Description**: Build token unstaking transaction
- **Response**: Transaction for user to sign

#### `ForcePayoutProtocol(lotteryPubkey)`

- **File**: `requests/position/forcePayoutProtocol.ts`
- **Description**: Build force payout transaction
- **Response**: Transaction for user to sign

---

### 2.3 History Domain

#### `GetEpochPayoutHistory(lotteryPubkey: string)`

- **File**: `requests/history/getEpochPayoutHistory.ts`
- **Description**: Fetch epoch payout history for a protocol
- **Response**: `EpochPayoutHistory[]` with top-1 PDAs and amounts

#### `GetFieldPayoutHistory(lotteryPubkey: string)`

- **File**: `requests/history/getFieldPayoutHistory.ts`
- **Description**: Fetch field (jackpot) payout history
- **Response**: `FieldPayoutHistory[]` with amounts and dates

#### `GetPositionPurchaseHistory(lotteryPubkey: string)`

- **File**: `requests/history/getPositionPurchaseHistory.ts`
- **Description**: Fetch position purchase records
- **Response**: `ProtocolHistory[]` with transaction proofs

#### `GetStakingByEpoch(lotteryPubkey: string)`

- **File**: `requests/history/getStakingByEpoch.ts`
- **Description**: Fetch staking snapshots per epoch
- **Response**: `StakingEpochSnapshot[]` (totalStaked, locked, unlocked per epoch)

#### `GetPositionsByEpoch(lotteryPubkey: string)`

- **File**: `requests/history/getPositionsByEpoch.ts`
- **Description**: Fetch position count per epoch
- **Response**: Aggregated position counts by epoch

#### `GetEpochPayoutsChart(lotteryPubkey: string)`

- **File**: `requests/history/getEpochPayoutsChart.ts`
- **Description**: Fetch data for epoch payouts chart
- **Response**: Chart-ready data points

#### `GetStakingStats(lotteryPubkey: string)`

- **File**: `requests/history/getStakingStats.ts`
- **Description**: Fetch aggregated staking statistics
- **Response**: Total staked, average stake, distribution

---

### 2.4 Bonding Curve Domain

#### `GetBondingCurveState(pubkey: string)`

- **File**: `requests/bonding/getBondingCurveState.ts`
- **Description**: Fetch bonding curve state from DB
- **Response**: `BondingCurve` model data

#### `GetBondingCurveFromChain(pubkey: string)`

- **File**: `requests/bonding/getBondingCurveFromChain.ts`
- **Description**: Fetch bonding curve data directly from blockchain
- **Response**: On-chain `BondingCurveAccount`

#### `GetBondingCurveData(pubkey: string)`

- **File**: `requests/bonding/getBondingCurveData.ts`
- **Description**: Fetch combined bonding curve data (DB + calculations)
- **Response**: Price, reserves, health ratio, supply info

#### `GetBondingCurveHistory(bondingCurvePubkey: string)`

- **File**: `requests/bonding/getBondingCurveHistory.ts`
- **Description**: Fetch trade transaction history
- **Response**: `BondingCurveTransaction[]`

#### `GetBondingCurveSnapshots(bondingCurvePubkey: string, interval: string)`

- **File**: `requests/bonding/getBondingCurveSnapshots.ts`
- **Description**: Fetch OHLCV snapshots for charts
- **Response**: `BondingCurveSnapshot[]` (open, high, low, close, volume)

#### `GetTopHolders(bondingCurvePubkey: string)`

- **File**: `requests/bonding/getTopHolders.ts`
- **Description**: Fetch top token holders
- **Response**: `TokenHolder[]` (wallet, balance, percentage)

#### `BuyTokens(bondingCurvePubkey, amount, maxSolCost)`

- **File**: `requests/bonding/buyTokens.ts`
- **Description**: Build token purchase transaction
- **Response**: Transaction for user to sign

#### `SellTokens(bondingCurvePubkey, amount, minSolPayout)`

- **File**: `requests/bonding/sellTokens.ts`
- **Description**: Build token sale transaction
- **Response**: Transaction for user to sign

---

### 2.5 User Domain

#### `GetUser(pubkey: string)`

- **File**: `requests/user/getUser.ts`
- **Description**: Fetch user by wallet pubkey
- **Response**: `User` model or null

#### `GetOrCreateUser(pubkey: string)`

- **File**: `requests/user/getOrCreateUser.ts`
- **Description**: Get existing user or create new one
- **Response**: `User` model (created with auto-generated username)

#### `GetUserTokens(pubkey: string)`

- **File**: `requests/user/getUserTokens.ts`
- **Description**: Fetch Token-2022 tokens owned by user
- **Response**: Token account data from Solana

#### `GetTokenMetadata(mintAddress: string)`

- **File**: `requests/user/getTokenMetadata.ts`
- **Description**: Fetch token metadata from Supabase
- **Response**: Token name, symbol, image URL

#### `GetOnChainTokenData(mintAddress: string)`

- **File**: `requests/user/getOnChainTokenData.ts`
- **Description**: Fetch token data from blockchain
- **Response**: Mint info, supply, extensions

---

### 2.6 Statistics Domain

#### `GetGlobalStatistics()`

- **File**: `requests/statistics/getGlobalStatistics.ts`
- **Description**: Fetch platform-wide statistics (singleton)
- **Response**: `GlobalStatistics` (total protocols, positions, pool amounts, max payouts)

---

### 2.7 Legacy (Ex-Lottery) Domain

#### `BuyoutLottery / BuyoutLottery1-19`

- **Files**: `requests/ex-lottery/buyoutLottery*.ts`
- **Description**: 19+ versions of buyout transactions for different Transfer Hook configurations
- **Response**: Signed transactions

---

### 2.8 Supabase Domain

#### `UploadProtocolTokenMetadata(data)`

- **File**: `requests/supabase/protocol/uploadProtocolTokenMetadata.ts`
- **Description**: Upload token metadata JSON to Supabase S3 bucket
- **Response**: Upload confirmation

---

## 3. Signing Service API

**Base URL**: Deployed on Railway (production)

---

### 3.1 Authentication

All endpoints (except `/health`) require **HMAC-SHA256 authentication**.

| Header | Description |
|--------|-------------|
| `x-signature` | HMAC-SHA256(secret, timestamp + body) |
| `x-timestamp` | Current Unix timestamp (seconds) |
| `Content-Type` | `application/json` |

**Timestamp window**: 300 seconds (5 minutes).

---

### 3.2 Endpoints

#### `GET /health`

- **Auth**: None
- **Response**: `200 OK` — service is healthy

---

#### `POST /get-public-key`

- **Auth**: HMAC
- **Request body**: `{ "environment": "local" | "dev" | "main" }`
- **Response**: `{ "publicKey": "Base58EncodedPublicKey" }`
- **Business rules**: Returns server keypair's public key for the specified environment

---

#### `POST /get-treasury-public-key`

- **Auth**: HMAC
- **Request body**: `{ "environment": "local" | "dev" | "main" }`
- **Response**: `{ "publicKey": "Base58EncodedPublicKey" }`
- **Business rules**: Returns treasury keypair's public key

---

#### `POST /sign-transaction`

- **Auth**: HMAC
- **Request body**:
  ```json
  {
    "environment": "local" | "dev" | "main",
    "transaction": "Base64EncodedTransaction"
  }
  ```
- **Response**:
  ```json
  {
    "signedTransaction": "Base64EncodedSignedTransaction",
    "isFullySigned": boolean,
    "remainingSigners": number
  }
  ```
- **Business rules**:
  - Accepts both legacy and versioned (v0) transactions
  - Performs partial signing (only adds server signature)
  - Validates that the keypair is a required signer
  - Returns remaining signer count

---

#### `POST /sign-treasury-transaction`

- **Auth**: HMAC
- **Request body**: Same as `/sign-transaction`
- **Response**: Same structure
- **Business rules**: Signs with treasury keypair instead of server keypair

---

### 3.3 Error Responses

| Status | Body | Reason |
|--------|------|--------|
| 401 | `"Invalid signature"` | HMAC verification failed |
| 401 | `"Timestamp expired"` | Timestamp outside 5-minute window |
| 400 | `"Invalid transaction format"` | Cannot deserialize transaction |
| 400 | `"Keypair is not a required signer"` | Transaction doesn't require this key |
| 500 | `"Internal server error"` | Unexpected failure |

---

## 4. Frontend API Routes

---

### 4.1 `POST /api/notify/createdPosition`

- **File**: `src/app/api/notify/createdPosition/route.ts`
- **Auth**: Bearer token (`NOTIFY_SECRET`)
- **Description**: Backend notifies frontend that a position was created
- **Usage**: Triggers Pusher event for real-time UI update

---

### 4.2 `POST /api/notify/createPosition`

- **File**: `src/app/api/notify/createPosition/route.ts`
- **Auth**: Bearer token (`NOTIFY_SECRET`)
- **Description**: Backend notifies frontend about position creation in progress

---

### 4.3 `GET /api/test-metadata`

- **File**: `src/app/api/test-metadata/route.ts`
- **Auth**: None
- **Query params**: `?mint=<address>`
- **Description**: Test endpoint for fetching token metadata from Supabase

---

### 4.4 `GET /api/test-onchain`

- **File**: `src/app/api/test-onchain/route.ts`
- **Auth**: None
- **Query params**: `?mint=<address>`
- **Description**: Test endpoint for fetching on-chain token data

---

### 4.5 `POST /api/cron/archive-tickets`

- **File**: `src/app/api/cron/archive-tickets/route.ts`
- **Auth**: Bearer token (`CRON_SECRET`)
- **Description**: Cron job for archiving old tickets (currently disabled/commented out)

---

## 5. Backend HTTP Endpoints (be-ticket)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | None | Health check — returns 200 if service is running |
| `GET` | `/ip` | None | Returns public and local IP addresses of server |

> **Open question for PO/Dev**: Are there any additional backend API endpoints planned? The current backend is almost entirely event-driven with no user-facing REST API.

---

## 6. Testing Guidelines

### 6.1 Server Actions Testing

Server actions are not directly accessible via HTTP. To test them:

1. **Integration tests**: Use Playwright to interact with the frontend UI
2. **Direct testing**: Import server action in test file and call directly (requires server environment)
3. **Database verification**: Query PostgreSQL directly after action execution

### 6.2 Signing Service Testing

**Test scenarios:**
- Valid transaction signing (legacy and versioned)
- Invalid HMAC signature
- Expired timestamp
- Invalid transaction format
- Missing required signer
- Treasury vs server keypair signing

**Example test request:**
```bash
curl -X POST https://signing-service.example.com/sign-transaction \
  -H "Content-Type: application/json" \
  -H "x-timestamp: $(date +%s)" \
  -H "x-signature: $(calculate_hmac)" \
  -d '{
    "environment": "dev",
    "transaction": "<base64_tx>"
  }'
```

### 6.3 Frontend API Routes Testing

**Test scenarios:**
- `/api/notify/*` endpoints with valid `NOTIFY_SECRET`
- `/api/cron/*` endpoints with valid `CRON_SECRET`
- `/api/test-*` endpoints (no auth required)

### 6.4 Event-Driven Flow Testing

Most backend logic is triggered by blockchain events. Test flows:

1. **Position creation**:
   - Build and send VRF request
   - Wait for `RandomResponseEvent`
   - Verify backend creates ticket records

2. **Epoch payout**:
   - Trigger `ForcePayoutEvent`
   - Verify `EpochPayoutHistory` created
   - Verify pool amounts updated

3. **Staking**:
   - Trigger `TokenHolderDepositEvent`
   - Verify `TokenDeposit` record created
   - Verify lock period enforced

### 6.5 Mock Blockchain Calls

For UI testing, mock blockchain calls to:
- Avoid CI/CD instability
- Test edge cases without on-chain transactions
- Test error conditions

Use:
- Playwright `page.route()` to intercept RPC calls
- Mock data responses for known scenarios

---

## 7. Security Considerations

### 7.1 Signing Service Security

- **HMAC-SHA256** ensures request integrity
- **5-minute timestamp window** prevents replay attacks
- **Environment separation** (local/dev/main) prevents cross-env key leaks
- **Partial signing only** — service never has full control over transactions

### 7.2 Frontend API Routes Security

- **Bearer token authentication** for all notification endpoints
- **CRON_SECRET** for scheduled jobs
- **Public test endpoints** should be disabled in production

### 7.3 Wallet Authorization

- **Whitelist check** (`AUTHORIZED_KEYS`) before allowing platform access
- **2.5s timeout** to force wallet connection
- **Re-check on navigation** prevents session hijacking

---

## 8. Common Issues & Debugging

### 8.1 Server Actions Fail Silently

**Symptom**: UI doesn't update, no error visible

**Debugging**:
- Check server logs in Railway/Vercel
- Verify database connection
- Check Prisma query syntax
- Use `console.log` in server action (appears in server logs)

### 8.2 Signing Service Returns 401

**Symptom**: Invalid signature or timestamp expired

**Debugging**:
- Verify HMAC calculation matches server implementation
- Check system clock synchronization
- Ensure timestamp is in seconds (not milliseconds)

### 8.3 Events Not Processed by Backend

**Symptom**: On-chain transaction succeeds but DB not updated

**Debugging**:
- Check backend logs for event subscription errors
- Verify `PubSubProvider` WebSocket connection
- Check Borsh deserialization
- Verify orchestrator logic

### 8.4 Pusher Not Updating UI

**Symptom**: Real-time updates not appearing

**Debugging**:
- Verify Pusher channel subscription
- Check `NOTIFY_SECRET` matches between backend and frontend
- Verify API route is being called
- Check browser console for Pusher errors

---

## 9. Environment Variables Reference

### 9.1 Frontend (Next.js)

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection |
| `SUPABASE_URL` / `SUPABASE_KEY` | Supabase S3 for metadata |
| `SIGNING_SERVICE_URL` | Signing Service base URL |
| `SIGNING_SERVICE_SECRET` | HMAC secret for signing requests |
| `PUSHER_APP_ID` / `PUSHER_KEY` / `PUSHER_SECRET` / `PUSHER_CLUSTER` | Pusher WebSocket |
| `AUTHORIZED_KEYS` | Comma-separated wallet pubkeys |
| `NOTIFY_SECRET` | Bearer token for notification endpoints |
| `CRON_SECRET` | Bearer token for cron jobs |
| `SOLANA_RPC_URL` | Solana RPC endpoint |
| `SOLANA_NETWORK` | "devnet" or "mainnet-beta" |

### 9.2 Signing Service

| Variable | Purpose |
|----------|---------|
| `SIGNING_SERVICE_SECRET` | HMAC secret |
| `SERVER_KEYPAIR_*` | Server keypair for transactions |
| `TREASURY_KEYPAIR_*` | Treasury keypair for special operations |
| `RPC_URL_LOCAL` / `RPC_URL_DEV` / `RPC_URL_MAIN` | Environment-specific RPC URLs |

### 9.3 Backend (be-ticket)

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection |
| `SOLANA_RPC_URL` / `SOLANA_WS_URL` | Solana RPC/WebSocket |
| `SIGNING_SERVICE_URL` / `SIGNING_SERVICE_SECRET` | Signing Service |
| `NOTIFY_SECRET` | Bearer token for notifications |
| `KURRENT_DB_URL` | KurrentDB connection |
| `SUPABASE_URL` / `SUPABASE_KEY` | Supabase IDL storage |
