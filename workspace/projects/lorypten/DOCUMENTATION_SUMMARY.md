# Lorypten Documentation Summary

**Дата завершення:** 2026-02-27  
**Загальний обсяг:** ~200KB (10 файлів документації)

---

## 📁 Структура документації

```
projects/lorypten/
├── PROJECT.md                    (26.9KB) — Основний індекс проєкту
└── docs/
    ├── SMART_CONTRACTS.md        (18.5KB) — 6 Solana programs, account structures, instructions
    ├── BACKEND.md                (14.3KB) — be-ticket Rust/Actix backend, event-driven architecture
    ├── FRONTEND.md               (16.1KB) — Next.js 15 frontend structure, pages/routes, user flows
    ├── API.md                    (18.7KB) — QA-focused API documentation, Server Actions, Signing Service
    ├── DOMAIN.md                 (18.4KB) — Domain concepts, business rules, invariants, calculations
    ├── AUTH.md                   (13.0KB) — Authentication & authorization, wallet-based auth, HMAC-SHA256
    ├── INTEGRATIONS.md           (18.4KB) — Integrations & external dependencies (10 services)
    ├── DATABASE.md               (23.5KB) — PostgreSQL schema with Prisma ORM, entity relationships
    ├── TESTING.md                (15.7KB) — Test ideas & coverage hints, testing strategy
    └── OPEN_QUESTIONS.md         (16.3KB) — 23 open questions & gaps, priorities, action items
```

**Разом:** ~200KB технічної документації

---

## 🎯 Що ми маємо зараз (10 файлів документації)

### 1. **Smart Contracts** (6 programs)
- `sol_ticket` — core lottery/tickets program
- `sol_bonding_curve` — AMM/trading program
- `sol_token_2022_nft` — NFT minting program
- `sol_transfer_hook_nft` — transfer authorization program
- `sol_orao_vrf` — randomness program
- `sol_treasury` — treasury management program

### 2. **Backend Architecture** (be-ticket — Rust/Actix Web)
- Event-driven architecture (14 subscribed events)
- 7 orchestrators for event processing
- Services (SmartContract, Ticket, Lottery, API, BondingCurve)
- Providers (Onchain, PubSub, KurrentDB)
- Game field logic (rounds, scoring)

### 3. **Frontend Structure** (Next.js 15 — React 19)
- App Router structure
- 11 routes with detail tabs
- 10 critical user flows
- Key components (Layout, Protocol, Position, Trading, Token, Statistics)
- Real-time updates via Pusher
- State management (Jotai, React Hook Form, Prisma)

### 4. **API Documentation** (QA Focused)
- Server Actions (8 domains: Protocol, Position, History, Bonding Curve, User, Statistics, Legacy, Supabase)
- Signing Service API (HMAC-SHA256 auth, 5 endpoints)
- Frontend API Routes (5 endpoints)
- Backend HTTP Endpoints (be-ticket)
- Testing guidelines & security considerations

### 5. **Domain & Business Rules**
- Core domain concepts (Protocol, Position, Epoch, Pools, Bonding Curve, User)
- Invariants & constraints (6 sets)
- Calculations & formulas (bonding curve price, SOL distribution, health ratio, score calculation)
- State machines & lifecycles (4 diagrams)
- Pool distribution rules
- Game field rules (3×3, 9×9)
- Protocol termination conditions
- Airdrop system

### 6. **Authentication & Authorization**
- Wallet-based authentication (no passwords/sessions/JWTs)
- Whitelist access control (AuthGuardProvider, Authorized Keys)
- Signing Service HMAC-SHA256 authentication
- On-chain access control (Server Signer validation)
- Backend notification auth (Bearer token)
- Access control matrix (10+ actions)

### 7. **Integrations & External Dependencies** (10 services)
- Solana Blockchain (RPC/WebSocket)
- ORAO VRF (random number generation)
- KurrentDB (event streaming)
- Supabase (object storage)
- ImageKit (CDN)
- Pusher (real-time WebSocket)
- PostgreSQL (database)
- Signing Service (isolated microservice)
- Token-2022 Program (extensions)

### 8. **Database Schema** (PostgreSQL + Prisma ORM)
- Entity relationships (User → Ticket → Lottery → GlobalStatistics)
- Core models (User, Lottery/Protocol, Ticket/Position)
- Score & earnings models
- Field models
- History models
- Token staking models
- Bonding curve models
- Utility models
- Enums & schema design principles

### 9. **Test Ideas & Coverage Hints**
- Testing strategy overview (Unit, Integration, API/Server Action, Smart Contract, E2E)
- Priority order (Smart contracts highest risk → backend → server actions → frontend → E2E)
- Smart contract tests (existing tests, critical paths, edge cases)
- Backend tests (orchestrators, services, game field logic)
- Frontend tests (server actions, components, E2E flows)
- Signing service tests
- Database tests
- Cross-cutting test scenarios

### 10. **Open Questions & Gaps** (23 questions)
- **Business Logic** (7): Buyout price formula, airdrop distribution, jackpot claim flow, tie-breaking, protocol completion, hold token gating
- **Architecture** (4): KurrentDB vs PubSub, event ordering, retry/dead letter queue, backend concurrency
- **Frontend** (4): Wallet whitelist management, Pusher events, offline/error states, Agent Mode scope
- **Smart Contract** (5): Account size limits, versioned transactions, Transfer Hook exemptions, health ratio thresholds, devnet vs mainnet
- **Database** (3): LotteryState enum, legacy models, data retention
- **DevOps/Environment** (4): Environment parity, deployment process, monitoring & alerting, database migrations
- **Security** (3): Rate limiting, transaction replay protection, wallet whitelist bypass

---

## 🚀 Повний QA-пакет для Lorypten

**Це повна документація для QA, що включає:**

- ✅ Technical architecture
- ✅ API endpoints & Server Actions
- ✅ Business rules & invariants
- ✅ Test cases & edge cases
- ✅ QA checklist
- ✅ Security considerations
- ✅ Auth & access control
- ✅ External integrations & dependencies
- ✅ Database schema & design principles
- ✅ Testing strategy & coverage goals
- ✅ CI/CD recommendations
- ✅ Deployment considerations
- ✅ Open questions & action items

**Наступні кроки:**
1. Заповнити placeholder URLs в PROJECT.md (staging/prod URLs, repo, Jira, RPC endpoint)
2. Створити `scripts/` директорію з прикладами скриптів
3. Створити `test-cases/` директорію з тест-кейсами
4. Провести meeting з командою для уточнення open questions
5. Почати писати тести для critical flows

**Документація готова для початку тестування!** 🎯