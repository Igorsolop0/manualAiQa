# Authentication & Authorization

**Оновлено:** 2026-02-27

---

## 1. Overview

The platform uses **wallet-based authentication** (no passwords, no sessions, no JWTs). All identity is derived from Solana wallet public keys.

---

## 2. Authentication Model

---

### 2.1 Wallet Connection (Frontend)

- Users authenticate by connecting their Solana wallet (Phantom, Solflare, Backpack, etc.)
- The `@solana/wallet-adapter-react` library handles connection
- Connection state is managed by `SolanaProvider` in `layout.tsx`
- **No server-side session** — wallet connection is entirely client-side

---

### 2.2 User Creation

- Users are created in the database on first meaningful interaction
- `GetOrCreateUser(pubkey)` server action handles upsert
- Username is auto-generated (no registration form)
- **User identity = wallet public key** (primary key in `User` table)

---

### 2.3 No Traditional Auth

- No login/logout flow
- No passwords or email verification
- No refresh tokens or session management
- No OAuth or social login
- **Identity is wallet itself**

---

## 3. Whitelist Access Control (Frontend)

---

### 3.1 `AuthGuardProvider`

**File**: `frontend/next/src/providers/AuthGuardProvider.tsx`

The platform restricts access to a predefined list of wallet addresses.

**Behavior**:
1. On page load, provider checks if wallet is connected
2. Waits up to **2.5 seconds** for auto-connection (some wallets auto-reconnect)
3. If connected → checks if `wallet.publicKey` is in `AUTHORIZED_KEYS`
4. If authorized → renders children (platform content)
5. If not authorized OR not connected after timeout → redirects to `/unauthorized`

---

### 3.2 Authorized Keys

**File**: `frontend/next/src/constants/lib/constants.ts`

```typescript
AUTHORIZED_KEYS = BASE_AUTHORIZED_KEYS + (AGENT_MODE && devnet ? AGENT_WALLET_KEY : [])
```

- `BASE_AUTHORIZED_KEYS`: hardcoded list of authorized wallet public keys
- `AGENT_WALLET_KEY`: additional key for automated testing (devnet only)
- `AGENT_MODE`: enabled via `NEXT_PUBLIC_AGENT_MODE=true` env var

---

### 3.3 Agent Mode (Devnet Only)

When `NEXT_PUBLIC_AGENT_MODE=true`:

- An additional wallet key (`AGENT_WALLET_KEY`) is added to `AUTHORIZED_KEYS`
- `AgentWalletAdapter` allows automatic connection without user interaction
- Used for **automated testing and CI**

---

### 3.4 Admin Panel Access

**File**: `frontend/next_admin/src/lib/constants.ts`

The admin panel has a separate `AUTHORIZED_KEYS` list. Only wallets in this list can access the admin interface. Same `AuthGuardProvider` pattern.

---

## 4. Signing Service Authentication

---

### 4.1 HMAC-SHA256 Protocol

All Signing Service API calls are authenticated with HMAC-SHA256.

**Request headers**:

| Header | Value |
|--------|-------|
| `x-signature` | HMAC-SHA256(`API_SECRET`, `timestamp` + `requestBody`) |
| `x-timestamp` | Current Unix timestamp in seconds |

**Validation**:
1. Server receives request
2. Extracts `x-timestamp` and `x-signature` headers
3. Checks if timestamp is within **300-second (5-minute) window**
4. Computes expected HMAC: `HMAC-SHA256(secret, timestamp + body)`
5. Constant-time comparison of expected vs received signature
6. Rejects if mismatch or expired

---

### 4.2 Environment-Specific Secrets

| Environment | Secret Variable |
|------------|-----------------|
| Local | `API_SECRET_LOCAL` |
| Dev | `API_SECRET_DEV` |
| Main | `API_SECRET_MAIN` |
| Fallback | `API_SECRET` |

---

### 4.3 Per-Environment Keypairs

The Signing Service maintains separate keypairs per environment:

| Purpose | Local | Dev | Main |
|---------|-------|-----|------|
| Server key | `keys/server-key/local.json` | `keys/server-key/dev.json` | `keys/server-key/main.json` |
| Treasury key | `keys/treasury-key/local.json` | `keys/treasury-key/dev.json` | `keys/treasury-key/main.json` |

**Keys can also be provided via environment variables as base64-encoded keypairs:**

- `KEYPAIR_LOCAL_BASE64`, `KEYPAIR_DEV_BASE64`, `KEYPAIR_MAIN_BASE64`
- `TREASURY_KEYPAIR_LOCAL_BASE64`, `TREASURY_KEYPAIR_DEV_BASE64`, `TREASURY_KEYPAIR_MAIN_BASE64`

---

## 5. On-Chain Access Control

---

### 5.1 Server Signer Validation

Most smart contract instructions require `server_signer` to be a signer. The expected address is hardcoded:

```typescript
SERVER_SIGNER_VALIDATOR = E7Vr9kw6qDAAJbEtpxCBocjcomLiKsTw4mFa4hoFdxNz
```

**Instructions that require server_signer:**
- `init_lottery`, `create_ticket_pda`, `create_ticket`
- `lock`, `unlock`
- `init_airdrop_pools`, `update_lottery_admin`
- `mint_tokens_to_vault`, `burn_lottery_tokens`
- `initialize_platform_token`, `initialize_bonding_curve`
- All Transfer Hook validations

---

### 5.2 Transfer Hook Authorization

Every Token-2022 transfer requires `server_signer` to co-sign:

- Prevents unauthorized token transfers
- Backend must participate in every buyout, token transfer
- **Without server signature** → `PlatformAdminMustSign` error

---

### 5.3 Open Instructions (no server_signer required)

- `buy_tokens` / `sell_tokens` (bonding curve trading)
- `force_payout` (anyone can trigger when time is due)
- `deposit_token_holder` / `withdraw_token_holder` (position owner)
- `update_health_ratio` (anyone can refresh)
- `buyout_lottery` (anyone with sufficient funds)

---

## 6. Backend Notification Auth

Backend → Frontend notification API calls use Bearer token:

- Header: `Authorization: Bearer <NOTIFY_SECRET>`
- Secret stored in `NOTIFY_SECRET` env var
- Validated in API route handlers

---

## 7. Access Control Matrix

| Action | Who | Auth Method |
|--------|-----|-------------|
| View protocols | Anyone with whitelisted wallet | Wallet connection + whitelist |
| Create protocol | Whitelisted wallet | Wallet + server co-sign |
| Buy position | Whitelisted wallet | Wallet + server co-sign |
| Stake tokens | Position owner | Wallet (on-chain owner check) |
| Withdraw tokens | Position owner | Wallet (on-chain owner check) |
| Force payout | Any whitelisted wallet | Wallet only (no server needed) |
| Buy/sell tokens | Any whitelisted wallet | Wallet only |
| Buyout protocol | Any whitelisted wallet with funds | Wallet + server co-sign (Transfer Hook) |
| Admin panel | Admin-whitelisted wallet | Wallet connection + admin whitelist |
| Signing Service calls | Services with HMAC secret | HMAC-SHA256 |
| Backend notifications | Backend with NOTIFY_SECRET | Bearer token |

---

## 8. Security Considerations

---

### 8.1 Wallet-Based Security

**Pros:**
- No password management
- No session hijacking risk
- Private keys never leave device
- Non-custodial (users control funds)

**Cons:**
- Wallet loss = total loss (no recovery)
- Key compromise = unauthorized access
- No 2FA/MFA support

---

### 8.2 Whitelist Protection

- Only authorized wallets can access platform
- Whitelist is enforced at **multiple layers**:
  1. Frontend (`AuthGuardProvider`)
  2. Server Actions (check before DB operations)
  3. Smart contracts (server_signer validation)

---

### 8.3 HMAC Security

- **Constant-time comparison** prevents timing attacks
- **5-minute timestamp window** prevents replay attacks
- **Environment separation** prevents cross-env key leaks
- **Base64 encoding** for keypair storage avoids filesystem permissions issues

---

### 8.4 Server Signer Protection

- Server keypair is required for critical operations
- **Transfer Hook** ensures all token transfers are authorized
- Keypairs stored securely (env vars or encrypted files)
- Never exposed to client-side

---

### 8.5 Admin Access

- Separate whitelist for admin panel
- No shared credentials
- Admin actions are logged (audit trail via on-chain transactions)

---

## 9. Testing Guidelines for Auth

---

### 9.1 Whitelist Testing

**Test cases:**
- Authorized wallet → can access platform
- Unauthorized wallet → redirected to `/unauthorized`
- Empty whitelist → no one can access
- Admin whitelist → separate from platform whitelist

---

### 9.2 Agent Mode Testing

**Test cases:**
- `AGENT_MODE=true` + devnet → `AGENT_WALLET_KEY` added
- `AGENT_MODE=false` → key not added
- Agent wallet → can auto-connect
- Non-agent wallet → needs manual connection

---

### 9.3 Signing Service Testing

**Test cases:**
- Valid HMAC → request accepted
- Invalid HMAC → 401 Invalid signature
- Expired timestamp → 401 Timestamp expired
- Missing headers → 400 Bad Request
- Different environments → separate secrets

---

### 9.4 On-Chain Access Testing

**Test cases:**
- Instruction without server_signer → should fail
- Instruction with server_signer → should succeed
- Transfer without server co-sign → `PlatformAdminMustSign` error
- Open instructions (buy/sell tokens) → should work without server

---

### 9.5 Backend Notification Testing

**Test cases:**
- Valid `NOTIFY_SECRET` → notification accepted
- Invalid secret → 401 Unauthorized
- Missing header → 400 Bad Request

---

## 10. Edge Cases & Security Risks

---

### 10.1 Wallet Disconnection

**Risk**: User disconnects wallet mid-session

**Mitigation**:
- `AuthGuardProvider` checks on every navigation
- Redirect to `/unauthorized` if not connected

---

### 10.2 Keypair Exposure

**Risk**: Server keypair leaked via environment variables

**Mitigation**:
- Use `.env` files (not committed to git)
- Rotate keys regularly
- Use encrypted storage in production

---

### 10.3 Replay Attacks

**Risk**: Intercepted HMAC request resent

**Mitigation**:
- 5-minute timestamp window
- Timestamp must be monotonically increasing
- Server logs all requests for audit

---

### 10.4 Whitelist Bypass

**Risk**: Direct API call without going through frontend

**Mitigation**:
- Server Actions check whitelist before DB operations
- Smart contracts enforce server_signer validation
- No public REST API for sensitive operations

---

### 10.5 Admin Privilege Escalation

**Risk**: Admin whitelist compromised

**Mitigation**:
- Separate admin panel with own whitelist
- Admin actions require server co-sign
- Audit trail via on-chain transactions

---

## 11. Environment Variables Reference

### 11.1 Frontend (Platform)

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_AGENT_MODE` | Enable Agent Mode (devnet only) |
| `NEXT_PUBLIC_SOLANA_NETWORK` | Solana network (devnet/mainnet-beta) |
| `AUTHORIZED_KEYS` | Comma-separated wallet pubkeys |
| `AGENT_WALLET_KEY` | Additional wallet for automated testing |

### 11.2 Frontend (Admin Panel)

| Variable | Purpose |
|----------|---------|
| `ADMIN_AUTHORIZED_KEYS` | Admin panel wallet whitelist |

### 11.3 Signing Service

| Variable | Purpose |
|----------|---------|
| `API_SECRET` | Fallback HMAC secret |
| `API_SECRET_LOCAL` | HMAC secret for local env |
| `API_SECRET_DEV` | HMAC secret for dev env |
| `API_SECRET_MAIN` | HMAC secret for main env |
| `KEYPAIR_LOCAL_BASE64` | Server keypair (local) |
| `KEYPAIR_DEV_BASE64` | Server keypair (dev) |
| `KEYPAIR_MAIN_BASE64` | Server keypair (main) |
| `TREASURY_KEYPAIR_LOCAL_BASE64` | Treasury keypair (local) |
| `TREASURY_KEYPAIR_DEV_BASE64` | Treasury keypair (dev) |
| `TREASURY_KEYPAIR_MAIN_BASE64` | Treasury keypair (main) |

### 11.4 Backend (be-ticket)

| Variable | Purpose |
|----------|---------|
| `SIGNING_SERVICE_SECRET` | HMAC secret for Signing Service |
| `NOTIFY_SECRET` | Bearer token for frontend notifications |

---

## 12. Common Issues & Debugging

---

### 12.1 "Unauthorized" Redirect

**Symptom**: User redirected to `/unauthorized` despite having wallet

**Debugging**:
- Check if wallet pubkey is in `AUTHORIZED_KEYS`
- Verify wallet is connected (check browser console)
- Check `NEXT_PUBLIC_AGENT_MODE` setting
- Verify `AuthGuardProvider` is mounted correctly

---

### 12.2 HMAC 401 Errors

**Symptom**: Signing Service returns 401 Invalid signature

**Debugging**:
- Verify HMAC calculation matches server implementation
- Check timestamp format (seconds, not milliseconds)
- Ensure `API_SECRET_*` env vars are set correctly
- Check environment (local/dev/main) matches secret used

---

### 12.3 Server Signer Mismatch

**Symptom**: Transaction fails with "server_signer mismatch"

**Debugging**:
- Verify server keypair is correct for environment
- Check `SERVER_SIGNER_VALIDATOR` constant
- Ensure Signing Service is using correct keypair
- Verify instruction includes server signer account

---

### 12.4 Transfer Hook Failures

**Symptom**: Token transfer fails with `PlatformAdminMustSign`

**Debugging**:
- Ensure Signing Service is called for all transfers
- Verify Transfer Hook is configured on token mint
- Check server_signer is included in transaction
- Verify transaction includes correct Transfer Hook accounts

---

### 12.5 Agent Mode Not Working

**Symptom**: Agent wallet not auto-connecting

**Debugging**:
- Check `NEXT_PUBLIC_AGENT_MODE=true` is set
- Verify network is devnet (Agent Mode devnet-only)
- Check `AGENT_WALLET_KEY` is valid base58 pubkey
- Verify `AgentWalletAdapter` is mounted
