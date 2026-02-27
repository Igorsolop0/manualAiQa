# Integrations & External Dependencies

**Оновлено:** 2026-02-27

---

## 1. Overview

The Lorypten platform integrates with multiple external services to provide blockchain, real-time, storage, and communication capabilities.

---

## 2. Solana Blockchain

---

### 2.1 Connection

| Service | RPC | WebSocket |
|---------|-----|-----------|
| Backend (be-ticket) | `SOLANA_RPC_URL` | `SOLANA_WS_URL` |
| Frontend (Next.js) | Configured per cluster in `cluster.provider.tsx` | Same |
| Signing Service | No direct connection (signs transactions only) | — |

---

### 2.2 Cluster Support

The frontend supports multiple Solana clusters:

- **Devnet** — development and testing
- **Mainnet** — production
- **Custom** — user-defined RPC endpoints

Cluster selection is managed via Jotai atoms in `cluster.provider.tsx`.

---

### 2.3 Error Handling

- **RPC errors**: Retried with exponential backoff in `OnchainProvider`
- **Transaction confirmation**: Polls with `Finalized` commitment level
- **Account not found**: Handled gracefully with retry logic
- **VRF timeout**: Backend polls up to configurable timeout before giving up

---

### 2.4 Idempotency

- Transaction signatures serve as idempotency keys (stored as `txProof` in DB)
- Event processing checks `SmartContractEvent.revision` to avoid duplicate processing
- Database operations use `@@unique` constraints to prevent duplicates

---

## 3. ORAO VRF

---

### 3.1 Purpose

Provides verifiable random numbers for game field generation.

---

### 3.2 Integration

| Aspect | Detail |
|--------|--------|
| Program ID | `VRFCBePmGTpZ234BhbzNNzmyg39Rgdd6VgdfhHwKypU` |
| Integration | CPI from `sol_orao_vrf` program |
| Flow | `request_random` → ORAO generates → `process_random` callback |
| Randomness | 64 bytes stored in `RandomState` PDA |

---

### 3.3 Error Handling

- VRF request may fail if ORAO network is congested
- Backend polls for VRF fulfillment with configurable interval and timeout
- If VRF fails, position creation is aborted

---

## 4. KurrentDB (Event Streaming)

---

### 4.1 Purpose

Persistent event stream for webhook events from Solana.

---

### 4.2 Integration

| Aspect | Detail |
|--------|--------|
| Stream | `webhook-full-transactions` |
| Events | `WebhookEvent` with transaction data |
| Tracking | `SmartContractEvent.revision` for cursor management |
| Connection | `KURRENT_DB_URL` env var |

---

### 4.3 Error Handling

- Connection retry with configurable delays
- Event revision tracking ensures exactly-once processing
- Failed event processing is logged but doesn't block stream

---

## 5. Supabase

---

### 5.1 Purpose

Object storage for token metadata JSON files and IDL files.

---

### 5.2 Integration

| Aspect | Detail |
|--------|--------|
| Usage | Upload/download token metadata JSON |
| Bucket | Configured via constants |
| Auth | `SUPABASE_URL` + `SUPABASE_KEY` env vars |
| Frontend | `uploadProtocolTokenMetadata()` server action |
| Backend | IDL loading on startup |

---

### 5.3 Stored Data

- **Token metadata JSON**: `{ name, symbol, description, image }` per mint
- **IDL files**: Anchor IDL for all programs (used by backend for instruction building)

---

### 5.4 Error Handling

- Upload failures: Surfaced to frontend as form error
- IDL load failures: Backend fails to start (critical dependency)

---

## 6. ImageKit (CDN)

---

### 6.1 Purpose

Image CDN for protocol images and avatars.

---

### 6.2 Integration

| Aspect | Detail |
|--------|--------|
| Provider | `ImageKitProvider` React component |
| Domain | `ik.imagekit.io` |
| Upload | During protocol creation |
| Display | `ProtocolImage.tsx` component |

---

### 6.3 Error Handling

- Fallback placeholder image if upload/load fails
- Image URL patterns in `protocolImageUrl.ts`

---

## 7. Pusher (Real-Time)

---

### 7.1 Purpose

WebSocket-based real-time notifications for UI updates.

---

### 7.2 Integration

| Aspect | Detail |
|--------|--------|
| Library | `pusher-js` (frontend client) |
| Trigger | Backend sends notifications via API routes |
| Channel | `ticket-specific-${lotteryPubkey}` |
| Events | `buyout`, position updates |

---

### 7.3 Flow

1. Backend processes blockchain event
2. Backend calls frontend API route (`/api/notify/...`) with Bearer auth
3. API route triggers Pusher event
4. Frontend Pusher client receives event
5. UI component refetches data

---

### 7.4 Error Handling

- Pusher connection failures: Client auto-reconnects
- Missed events: Frontend relies on polling/page refresh as fallback

---

## 8. PostgreSQL Database

---

### 8.1 Connection

| Service | Method | Connection |
|---------|--------|-----------|
| Frontend | Prisma Client | `POSTGRES_PRISMA_URL` (pooled) |
| Backend | SQLx (raw SQL) | `DATABASE_URL` (direct) |
| Migrations | Prisma CLI | `POSTGRES_URL_NON_POOLING` (direct) |

---

### 8.2 Shared Schema

The schema is maintained in `shared/prisma/schema.prisma` and published as `@lorypten/prisma-schema` npm package.

**Key rule**: Frontend ONLY READS from the database. All WRITES are performed by the Rust backend after processing blockchain events.

---

### 8.3 Error Handling

- Connection pool management: `PgPoolOptions` with configurable max connections
- Transaction support: Atomic operations in repositories
- Unique constraint violations: Handled gracefully (upsert patterns)

---

## 9. Signing Service

---

### 9.1 Purpose

Isolated microservice for managing Solana keypairs and co-signing transactions.

---

### 9.2 Integration

| Consumer | Usage |
|----------|-------|
| Frontend (Next.js) | `SigningService` class in `services/signingService/` |
| Backend (be-ticket) | Direct HTTP calls via `reqwest` |
| Admin panel | Same `SigningService` class |
| Test suite | `SigningService` in test utils |

---

### 9.3 Deployment

- **Platform**: Railway
- **Dockerfile**: Multi-stage Rust build with `cargo-chef`
- **Port**: 3001 (or `PORT` from environment)
- **Runs as**: Non-root user (`app`)

---

### 9.4 Error Handling

- HMAC auth failures: 401 response
- Invalid transactions: 400 response with detail
- Keypair not a signer: 400 response
- Service unavailable: Callers must handle connection errors

---

## 10. Token-2022 Program

---

### 10.1 Purpose

Solana Token-2022 program with extensions for advanced token functionality.

---

### 10.2 Extensions Used

| Extension | Purpose |
|-----------|---------|
| Transfer Hook | Requires server authorization for transfers |
| Metadata Pointer | On-chain metadata reference |
| Group Pointer | NFT grouping (ownership + participation) |
| Permanent Delegate | Program can manage tokens |
| Transfer Fee Config | Fee on transfers |
| Token Group / Group Member | NFT hierarchy |

---

### 10.3 Integration

- **Ownership NFT**: Represents protocol ownership
- **Participation tokens**: Represent positions (tickets)
- **Transfer Hook**: Every transfer validated by `sol_transfer_hook_nft`

---

## 11. External Service Summary

| Service | Purpose | Failure Impact |
|---------|---------|---------------|
| **Solana RPC** | Blockchain reads/writes | Platform fully non-functional |
| **ORAO VRF** | Random number generation | Position creation blocked |
| **KurrentDB** | Event streaming | Backend event processing stops |
| **Supabase** | Metadata storage + IDL | Protocol creation fails, backend may fail to start |
| **ImageKit** | Image CDN | Missing protocol images |
| **Pusher** | Real-time updates | No live UI updates, polling fallback |
| **PostgreSQL** | Data persistence | Platform fully non-functional |
| **Signing Service** | Transaction co-signing | All on-chain operations blocked |
| **Railway** | Deployment | Services unavailable |

---

## 12. Testing Guidelines for Integrations

---

### 12.1 Solana RPC Testing

**Test cases:**
- RPC endpoint connectivity
- Transaction confirmation polling
- Account fetching with different commitment levels
- RPC error handling (rate limits, timeouts)
- Idempotency (duplicate transaction detection)

---

### 12.2 VRF Testing

**Test cases:**
- VRF request → randomness generation flow
- VRF timeout handling
- VRF failure scenarios (ORAO network congestion)
- Randomness uniqueness (non-deterministic)
- Position creation with VRF failure

---

### 12.3 KurrentDB Testing

**Test cases:**
- Event stream connection
- Event revision tracking (exactly-once processing)
- Reconnection after connection loss
- Failed event handling (non-blocking)

---

### 12.4 Supabase Testing

**Test cases:**
- Token metadata upload/download
- IDL file loading on backend startup
- Upload error handling
- Invalid metadata format

---

### 12.5 ImageKit Testing

**Test cases:**
- Image upload during protocol creation
- Image URL generation
- Fallback to placeholder on failure
- Invalid image format handling

---

### 12.6 Pusher Testing

**Test cases:**
- WebSocket connection/subscription
- Event trigger → receive flow
- Auto-reconnection after disconnect
- Missed event handling (polling fallback)

---

### 12.7 PostgreSQL Testing

**Test cases:**
- Connection pool management
- Transaction atomicity
- Unique constraint handling (upsert)
- Schema migrations
- Read-only vs write separation (frontend vs backend)

---

### 12.8 Signing Service Testing

**Test cases:**
- HMAC authentication
- Transaction signing (legacy + versioned)
- Error responses (401, 400)
- Service unavailable handling
- Keypair rotation scenarios

---

### 12.9 Token-2022 Testing

**Test cases:**
- Transfer Hook authorization (server co-sign)
- Transfer without server sign (should fail)
- Metadata pointer resolution
- Group member validation
- NFT ownership transfer

---

## 13. Edge Cases & Failure Modes

---

### 13.1 Solana RPC Failure

**Symptom**: All blockchain operations fail

**Mitigation**:
- Exponential backoff for retries
- Circuit breaker pattern after repeated failures
- Fallback RPC endpoints (if configured)

---

### 13.2 VRF Timeout

**Symptom**: Position creation hangs indefinitely

**Mitigation**:
- Configurable timeout (default: 5 minutes)
- Abort position creation if timeout exceeded
- Notify user of VRF failure

---

### 13.3 KurrentDB Connection Loss

**Symptom**: Backend stops processing blockchain events

**Mitigation**:
- Reconnection with backoff
- Buffer events in memory during outage
- Resume processing after reconnection

---

### 13.4 Supabase Upload Failure

**Symptom**: Protocol creation fails at image/metadata upload

**Mitigation**:
- Surface error to user with clear message
- Allow retry without re-entering all data
- Fallback to default metadata if critical

---

### 13.5 ImageKit Unavailable

**Symptom**: Protocol images don't load

**Mitigation**:
- Fallback placeholder image
- Retry with backoff
- Cache successful uploads

---

### 13.6 Pusher Connection Issues

**Symptom**: Real-time updates don't appear

**Mitigation**:
- Auto-reconnect with backoff
- Polling fallback for critical data
- User notification of connection issues

---

### 13.7 PostgreSQL Connection Pool Exhaustion

**Symptom**: Database queries fail or slow

**Mitigation**:
- Configurable max connections
- Connection timeout and cleanup
- Circuit breaker for repeated failures

---

### 13.8 Signing Service Unavailable

**Symptom**: All on-chain operations fail

**Mitigation**:
- Circuit breaker pattern
- Clear error messages to users
- Health monitoring with alerts

---

### 13.9 Token-2022 Transfer Hook Failure

**Symptom**: Token transfers rejected

**Mitigation**:
- Verify server signer availability
- Check Transfer Hook configuration
- Fallback to legacy transfers if needed

---

## 14. Monitoring & Observability

---

### 14.1 Solana RPC Monitoring

- **Metrics**: Response time, error rate, success rate
- **Alerts**: High error rate, slow responses (>5s)
- **Tools**: Custom logging in `OnchainProvider`

---

### 14.2 VRF Monitoring

- **Metrics**: Request latency, fulfillment time, failure rate
- **Alerts**: High failure rate (>10%), timeout rate
- **Tools**: Backend polling logs

---

### 14.3 Database Monitoring

- **Metrics**: Connection pool usage, query time, error rate
- **Alerts**: Pool exhaustion (>90%), slow queries (>1s)
- **Tools**: PostgreSQL stats, Prisma logs

---

### 14.4 Signing Service Monitoring

- **Metrics**: Request rate, response time, HMAC failures
- **Alerts**: High failure rate (>5%), high latency (>2s)
- **Tools**: Railway logs, custom metrics

---

### 14.5 Pusher Monitoring

- **Metrics**: Connection health, event delivery rate
- **Alerts**: Connection drops, high missed event rate
- **Tools**: Pusher dashboard, client-side logs

---

## 15. Environment Variables Reference

### 15.1 Solana

| Variable | Service | Purpose |
|----------|---------|---------|
| `SOLANA_RPC_URL` | Backend | Solana RPC endpoint |
| `SOLANA_WS_URL` | Backend | Solana WebSocket endpoint |
| `NEXT_PUBLIC_SOLANA_RPC_URL` | Frontend | RPC URL (exposed to client) |
| `NEXT_PUBLIC_SOLANA_NETWORK` | Frontend | Cluster selection (devnet/mainnet-beta) |

### 15.2 KurrentDB

| Variable | Service | Purpose |
|----------|---------|---------|
| `KURRENT_DB_URL` | Backend | KurrentDB connection string |

### 15.3 Supabase

| Variable | Service | Purpose |
|----------|---------|---------|
| `SUPABASE_URL` | Frontend, Backend | Supabase base URL |
| `SUPABASE_KEY` | Frontend, Backend | Supabase API key |
| `NEXT_PUBLIC_SUPABASE_URL` | Frontend | Supabase URL (exposed to client) |
| `NEXT_PUBLIC_SUPABASE_KEY` | Frontend | Supabase key (exposed to client) |

### 15.4 ImageKit

| Variable | Service | Purpose |
|----------|---------|---------|
| `NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT` | Frontend | ImageKit upload endpoint |
| `NEXT_PUBLIC_IMAGEKIT_PUBLIC_KEY` | Frontend | ImageKit public key |
| `NEXT_PUBLIC_IMAGEKIT_AUTH_ENDPOINT` | Frontend | ImageKit auth endpoint |

### 15.5 Pusher

| Variable | Service | Purpose |
|----------|---------|---------|
| `NEXT_PUBLIC_PUSHER_APP_ID` | Frontend | Pusher application ID |
| `NEXT_PUBLIC_PUSHER_KEY` | Frontend | Pusher key |
| `NEXT_PUBLIC_PUSHER_SECRET` | Frontend | Pusher secret (server-side) |
| `NEXT_PUBLIC_PUSHER_CLUSTER` | Frontend | Pusher cluster |

### 15.6 PostgreSQL

| Variable | Service | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | Backend | PostgreSQL connection (direct) |
| `POSTGRES_PRISMA_URL` | Frontend | PostgreSQL connection (pooled) |
| `POSTGRES_URL_NON_POOLING` | Migrations | PostgreSQL connection (direct) |

### 15.7 Signing Service

| Variable | Service | Purpose |
|----------|---------|---------|
| `SIGNING_SERVICE_URL` | Frontend, Backend | Signing Service base URL |
| `SIGNING_SERVICE_SECRET` | Frontend, Backend | HMAC secret for auth |

---

## 16. Common Issues & Debugging

---

### 16.1 Solana RPC Errors

**Symptom**: "RPC error: timeout" or "RPC error: too many requests"

**Debugging**:
- Check RPC endpoint is accessible
- Verify rate limits are not exceeded
- Check network connectivity
- Try alternative RPC endpoint if configured

---

### 16.2 VRF Timeouts

**Symptom**: Position creation fails with "VRF timeout"

**Debugging**:
- Check VRF timeout configuration
- Verify ORAO network status
- Check backend logs for VRF polling
- Increase timeout if needed

---

### 16.3 Database Connection Errors

**Symptom**: "Connection pool exhausted" or "Unable to connect"

**Debugging**:
- Check database is running
- Verify connection string is correct
- Check max connections in pool config
- Review PostgreSQL logs

---

### 16.4 ImageKit Upload Failures

**Symptom**: Protocol creation fails at image upload

**Debugging**:
- Check ImageKit API key is valid
- Verify network connectivity to ImageKit
- Check image size/format constraints
- Review ImageKit dashboard for errors

---

### 16.5 Pusher Connection Issues

**Symptom**: Real-time updates not working

**Debugging**:
- Check Pusher app ID/key/cluster are correct
- Verify network allows WebSocket connections
- Check browser console for Pusher errors
- Verify Pusher subscription channel is correct

---

### 16.6 Signing Service Failures

**Symptom**: All on-chain operations fail

**Debugging**:
- Check Signing Service is running
- Verify HMAC secret is correct
- Check network connectivity to service
- Review Signing Service logs

---

### 16.7 Supabase Upload Failures

**Symptom**: Token metadata upload fails

**Debugging**:
- Check Supabase URL/key are correct
- Verify bucket exists and has write permissions
- Check file size/format constraints
- Review Supabase dashboard for errors

---

### 16.8 Token-2022 Transfer Hook Errors

**Symptom**: Transfer fails with "PlatformAdminMustSign"

**Debugging**:
- Verify server signer is available
- Check Transfer Hook is configured on token mint
- Ensure transaction includes server signer account
- Check Signing Service is reachable

---

### 16.9 KurrentDB Connection Loss

**Symptom**: Backend stops processing events

**Debugging**:
- Check KurrentDB is running
- Verify connection string is correct
- Check network connectivity
- Review backend logs for connection errors

---

## 17. Deployment Considerations

---

### 17.1 Service Dependencies

**Critical path** (must be available for platform to work):
1. Solana RPC
2. PostgreSQL
3. Signing Service
4. Backend (be-ticket)

**Optional but recommended:**
5. Pusher (real-time updates)
6. ImageKit (protocol images)
7. Supabase (metadata storage)

---

### 17.2 Health Checks

**Service health endpoints:**

| Service | Endpoint | Status |
|----------|-----------|--------|
| Frontend | `/` | 200 if page loads |
| Backend | `/health` | 200 if service running |
| Signing Service | `/health` | 200 if service running |
| PostgreSQL | Connection test | Success if connected |

---

### 17.3 Redundancy & Failover

**Current setup:**
- Single RPC endpoint per cluster
- Single database instance
- Single Signing Service instance

**Future improvements:**
- Multiple RPC endpoints with failover
- Database read replicas
- Multiple Signing Service instances with load balancing

---

### 17.4 Scalability

**Horizontal scaling:**
- Frontend: Stateless → can scale horizontally
- Backend: Stateful (database connection) → need connection pooling
- Signing Service: Stateless → can scale horizontally

**Vertical scaling:**
- Increase database resources (CPU, RAM)
- Increase RPC rate limits
- Increase connection pool sizes
