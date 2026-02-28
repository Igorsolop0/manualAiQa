# Проєкт: Lorypten (Solana Web3 App)

**Домен:** Blockchain, Web3, Solana, Lottery Protocol
**Стек тестування:** Playwright, API (REST/RPC), Mock Data

---

## 📋 System Overview

Lorypten — **децентралізований протокол платформа** на блокчейні Solana. Користувачі створюють та беруть участь у лотерейних "протоколах", де купують "позиції" (білети) з ігровими полями. Кожна позиція має випадково згенероване поле, що еволюціонує з часом.

**Основні функції:**
- **Protocol creation** — створення протоколів з налаштуваними періодами виплат, entry fees та пулами
- **Position purchasing** — купівля позицій в протоколах, кожна з унікальним ігровим полем
- **Epoch-based payouts** — винагороди розподіляються серед найкращих наприкінці кожної епохи
- **Token trading** — кожен протокол має власну bonding curve для торгівлі токенами (buy/sell)
- **Staking** — стейкінг токенів на позиціях для заробітку з пулу Token Holder
- **Buyout mechanism** — передача власності протоколу через buyout
- **Airdrop system** — протоколи можуть мати airdrop пули для додаткових винагород

---

## 👥 Main User Roles

| Role | Description |
|------|-------------|
| **Regular User** | Підключає Solana гаманець, купує позиції в протоколах, стейкає токени, отримує виплати |
| **Protocol Creator** | Створює нові протоколи з кастомними параметрами (entry fee, duration, field size, pools, buyout, airdrop) |
| **Protocol Owner** | Поточний власник протоколу (може змінюватись через buyout). Отримує 1% з bonding curve trades |
| **Admin** | Використовує адмін панель для управління гаманцями, деплоїв, PDAs. Whitelist-based доступ |
| **Server (be-ticket)** | Backend сервіс, який слухає блокчейн події та синхронізує стан DB |
| **Signing Service** | Microservice, що зберігає keypairs та ко-підписує транзакції |

---

## 🏗️ High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│ SOLANA BLOCKCHAIN                                                       │
│                                                                        │
│  Smart Contracts (6 programs)                                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ sol_ticket    │ │sol_bonding   │ │sol_token_2022│ │sol_transfer   │ │
│  │ (lottery/     │ │_curve        │ │_nft          │ │_hook_nft     │ │
│  │ tickets)      │ │(AMM/trading) │ │(NFT minting) │ │(transfer auth)│ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│  ┌──────────────┐ ┌──────────────┐                            │
│  │ sol_orao_vrf │ │ sol_treasury │                            │
│  │ (randomness) │ │ (treasury     │                            │
│  │              │ │  mgmt)       │                            │
│  └──────────────┘ └──────────────┘                            │
└──────────────────────────────────────────────────────────────────────────┘
                │ Events (via webhook / PubSub)
                ▲ Transactions
                ▼
┌──────────────────────┐ ┌──────────────────────┐
│ Backend (be-ticket)  │ │ Signing Service      │
│ Rust / Actix Web    │ │ Rust / Axum         │
│                     │ │                     │
│ - Event listener     │ │ - Transaction signing│
│ - Orchestrators     │ │ - Keypair isolation │
│ - DB sync           │ │ - HMAC auth         │
│ - Smart contract    │───────────────────────│
│   interactions      │ HTTP/HMAC            │
└──────────┬───────────┘ └──────────────────────┘
           │ Write
           ▲
           │ Sign requests
    Read   ▼
┌──────────────────────┐ ┌──────────────────────┐
│ PostgreSQL DB        │◀───┐                │
│ (via Prisma)        │     │ Server Actions    │
│                     │     │                  │
│ - Protocols         │─────│ Frontend (Next.js)│
│ - Tickets           │     │ App Router        │
│ - BondingCurves     │     │                  │
│ - History           │     │ - Prisma reads    │
│ - Statistics        │     │ - Solana wallet    │
│                     │     │ - Anchor (server) │
└──────────────────────┘     │ - Pusher real-time │
                            └──────────────────────┘
                                   ▲
                          ┌────────┴────────┐
                          │ Pusher WS       │
                          └─────────────────┘
                                   ▲
                          ┌──────────┴──────────┐
                          │ Admin Frontend       │
                          │ (Next.js)           │
                          │ - Wallet mgmt       │
                          │ - Deploy mgmt       │
                          │ - PDA mgmt          │
                          └───────────────────────┘
```

---

## 🎯 Services & Responsibilities

### Smart Contracts (6 programs)

| Program | Responsibility |
|---------|---------------|
| `sol_ticket` | Core protocol/lottery logic: create protocols, buy positions, payouts, buyout, staking |
| `sol_bonding_curve` | AMM для торгівлі токенами: buy/sell tokens, health ratio, treasury/insurance management |
| `sol_token_2022_nft` | NFT створення з використанням Token-2022 extensions: ownership NFT, participation tokens |
| `sol_transfer_hook_nft` | Transfer Hook, що вимагає server_signer авторизації для всіх токенів трансферів |
| `sol_orao_vrf` | VRF інтеграція з ORAO для генерації випадкових чисел |
| `sol_treasury` | Treasury PDA management для ticket та transfer депозитів |

### Backend Services

| Service | Responsibility |
|---------|---------------|
| `be-ticket` | Головний backend. Слухає блокчейн події, обробляє через orchestrators, пише в DB |
| `signing_service` | Ізольоване зберігання keypairs та ко-підписання транзакцій через HMAC-authenticated API |

### Frontend Applications

| App | Responsibility |
|-----|---------------|
| `frontend/next` | Основний користувацький додаток. Перегляд протоколів, управління позиціями, торгівля, buyout |
| `frontend/next_admin` | Адмін панель. Управління гаманцями, деплої, PDA |

### Shared Resources

| Resource | Purpose |
|----------|---------|
| `shared/prisma` | Prisma schema, спільна між frontend та backend (публікується як `@lorypten/prisma-schema` npm package) |
| `solana/programs/sol_orao_vrf/idl/` | IDL файли для всіх програм (публікується як `@lorypten/solana-idl` npm package) |

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Blockchain** | Solana (Devnet / Mainnet), Anchor Framework |
| **Smart Contracts** | Rust, Anchor, Token-2022, ORAO VRF |
| **Backend** | Rust, Actix Web 4, Tokio, SQLx, Borsh |
| **Signing Service** | Rust, Axum, HMAC-SHA256 |
| **Database** | PostgreSQL (via Prisma ORM / SQLx) |
| **Frontend** | Next.js 15 (App Router), React 19, TypeScript |
| **UI** | Tailwind CSS 4, Radix UI (shadcn/ui), Framer Motion |
| **State Management** | Jotai (atoms), React Hook Form |
| **Wallet** | @solana/wallet-adapter-react (Phantom, Solflare, etc.) |
| **Real-time** | Pusher (WebSocket) |
| **Image CDN** | ImageKit |
| **Metadata Storage** | Supabase S3 (token metadata JSON) |
| **Event Streaming** | KurrentDB (webhook events) |
| **Deployment** | Railway (backend, signing service) |
| **Charts** | Recharts |

---

## 🌍 Середовища (Environments)

- **Staging URL:** `[ЗДОБУТИ LNK]`
- **Production URL:** `[ЗДОБУТИ LNK]`
- **Локація Кредосів (Credentials/Configs):** `projects/lorypten/.env` або `projects/lorypten/.config` *(додай потрібні файли сюди)*

## 🛠 Інфраструктура

- **Repo Url:** `[ЗДОБУТИ LNK]`
- **Jira / Task Board:** `[ЗДОБУТИ LNK]`
- **API Docs / Swagger:** `[ЗДОБУТИ LNK]`
- **RPC Endpoint (Solana):** `[ВКАЖИ DEVNET АБО MAINNET RPC URL]`
- **IDL Package:** `@lorypten/solana-idl` (npm)
- **Prisma Schema Package:** `@lorypten/prisma-schema` (npm)

---

## 🌊 Ключові Флоу (Critical Flows)

### 1. Protocol Creation
1. Protocol Creator відкриває "Create Protocol" форму
2. Налаштовує параметри: entry fee, duration, field size, pools (Treasury, Protocol Owner, Buyout), buyout price, airdrop pools
3. Frontend будує транзакцію → Signing Service → Solana
4. `sol_ticket` створює Protocol PDA
5. be-ticket слухає подію та синхронізує в DB

### 2. Position Purchase
1. User вибирає протокол та натискає "Buy Position"
2. Frontend будує транзакцію → Signing Service → Solana
3. `sol_ticket` minting ticket position з випадковим полем
4. `sol_token_2022_nft` створює ownership NFT
5. User сплачує entry fee (SOL або token протоколу)
6. be-ticket синхронізує нову позицію в DB

### 3. Token Trading (Bonding Curve)
1. User хоче buy/sell токени протоколу
2. Frontend показує bonding curve графік (Recharts)
3. User вводить кількість → Frontend будує транзакцію
4. `sol_bonding_curve` розраховує ціну та виконує trade
5. Protocol Owner отримує 1% комісію
6. Treasury та Insurance пули оновлюються

### 4. Epoch Payouts
1. Epoch закінчується (наприклад, 7 днів)
2. `sol_ticket` автоматично розподіляє винагороди:
   - Treasury Pool → переможцям
   - Protocol Owner Pool → власнику протоколу
   - Token Holder Pool → стейкерам токенів
   - Buyout Pool → в резерв
3. be-ticket слухає подію payout та оновлює статистику
4. Frontend показує leaderboard та виплати

### 5. Wallet Connection
1. User натискає "Connect Wallet"
2. @solana/wallet-adapter-react відкриває вибір гаманця
3. Phantom / Solflare / інші гаманці
4. Wallet підписує повідомлення для автентифікації
5. Frontend зберігає wallet public key в Jotai state

### 6. Staking
1. User має токени протоколу на позиції
2. Натискає "Stake Tokens" → вводить кількість
3. Frontend будує транзакцію staking → Signing Service → Solana
4. Staked токени отримують винагороду з Token Holder Pool
5. Real-time оновлення через Pusher WebSocket

### 7. Buyout
1. Protocol Owner хоче продати протокол
2. Встановлює buyout ціну
3. Інший користувач хоче купити (buyout)
4. Frontend будує транзакцію buyout → Signing Service → Solana
5. `sol_ticket` передає власність новому власнику
6. Old Owner отримує buyout кошти

### 8. Airdrop
1. Protocol має airdrop пул
2. Airdrop тригериться (автоматично або вручну)
3. Eligible користувачі отримують токени
4. be-ticket синхронізує airdrop розподіл в DB
5. Frontend показує airdrop історію

---

## 📊 Data Flow Summary

1. **User action** (наприклад, buy position) → Frontend будує Solana транзакцію.
2. Frontend відправляє транзакцію в **Signing Service** для server co-signature.
3. User підписує з гаманця → транзакція відправляється в **Solana**.
4. Solana програма виконується, емітить **events**.
5. **be-ticket** backend підбирає події через PubSub/webhook.
6. Backend **orchestrators** обробляють події та пишуть в **PostgreSQL**.
7. Frontend читає оновлені дані з DB через **Prisma** (Server Actions).
8. Real-time оновлення через **Pusher** для UI refresh.

---

## 📜 Правила тестування (Working Agreements)

- Використовувати **Playwright** для E2E-тестування.
- Всі тестові скрипти повинні розміщуватися в `projects/lorypten/scripts/` або окремому git-репозиторії.
- Максимально мокати (mock) блокчейн-виклики для стабільності на CI/CD (якщо ми тестуємо UI).
- Будь-яка проектна документація пишеться в `projects/lorypten/docs/`.

### Mock Strategy для CI/CD

- **Smart Contract Calls:** Mock `@solana/web3.js` calls → повертає фіктивні дані
- **Signing Service:** Mock HTTP endpoints → повертає pre-signed transactions
- **Blockchain Events:** Mock webhook/websocket events для be-ticket
- **Solana Wallet:** Mock wallet adapter для тестів без реального гаманця
- **Pusher:** Mock WebSocket для real-time оновлень

### Test Data

- Використовувати фіксовані test accounts з devnet
- Seed data для PostgreSQL (test protocols, tickets, positions)
- Test tokens для bonding curve тестів

---

## 🔑 Токени та Доступи

### Required для локальної розробки:
- `SOLANA_PRIVATE_KEY` — для local testing (тільки devnet!)
- `SIGNING_SERVICE_HMAC_KEY` — для Signing Service auth
- `PUSHER_APP_ID`, `PUSHER_KEY`, `PUSHER_SECRET` — для real-time
- `DATABASE_URL` — PostgreSQL connection string
- `NEXT_PUBLIC_RPC_URL` — Solana RPC endpoint

### Файли конфігурації:
- `projects/lorypten/.env` — environment variables (не в git!)
- `projects/lorypten/.env.example` — template з коментарями

---

## 📚 Документація

### Smart Contracts
- **`docs/SMART_CONTRACTS.md`** — Детальна документація всіх 6 Solana програм:
  - Program registry з Devnet IDs
  - Account structures (LotteryAccount, BondingCurve, etc.)
  - Всі інструкції (instructions) з business logic
  - Error codes
  - Cross-program interaction flows
  - PDA seeds та key constants

### Backend (be-ticket)
- **`docs/BACKEND.md`** — Детальна документація backend сервісу:
  - Architecture overview (AppContext, Services, Repositories, Providers)
  - Event system (14 subscribed events)
  - Orchestrators (7 core handlers)
  - Services (SmartContract, Ticket, Lottery, API, BondingCurve)
  - Providers (Onchain, PubSub, KurrentDB)
  - Game field logic (rounds, scoring)
  - HTTP endpoints
  - Environment variables
  - Dependencies

### Frontend (Next.js App)
- **`docs/FRONTEND.md`** — Детальна документація frontend додатку:
  - Application structure (App Router, Server Actions, components)
  - Pages & routes (11 routes)
  - Protocol detail page tabs (7 sections)
  - User flows (10 critical flows)
  - Key components (Layout, Protocol, Position, Trading, Token, Statistics)
  - Forms & validation (Create Protocol, Trading)
  - Real-time updates (Pusher channels)
  - State management (Jotai, React Hook Form, Prisma)
  - Technology stack (Next.js 15, React 19, Tailwind 4, shadcn/ui, Recharts)
  - Security & access control (wallet authorization)

### API Documentation (QA Focused)
- **`docs/API.md`** — Повна документація API та систем комунікації:
  - Server Actions (8 domains: Protocol, Position, History, Bonding Curve, User, Statistics, Legacy, Supabase)
  - Signing Service API (HMAC auth, 5 endpoints, error responses)
  - Frontend API Routes (5 notification and test endpoints)
  - Backend HTTP Endpoints (be-ticket: /health, /ip)
  - Testing guidelines (Server Actions, Signing Service, Event-Driven flows, Mock blockchain)
  - Security considerations (HMAC, Bearer tokens, Wallet authorization)
  - Common issues & debugging
  - Environment variables reference (Frontend, Signing Service, Backend)

### Domain & Business Rules
- **`docs/DOMAIN.md`** — Бізнес-правила та доменна модель:
  - Core Domain Concepts (Protocol, Position, Epoch, Pools, Bonding Curve, User)
  - Invariants & Constraints (Protocol, Position, Epoch, Staking, Bonding Curve, Buyout)
  - Calculations & Formulas (Bonding curve price, SOL distribution, Health ratio, Score calculation)
  - State Machines & Lifecycles (Protocol, Epoch, Token Staking, Position Field)
  - Pool Distribution Rules (Entry fee, Token purchase)
  - Game Field Rules (3×3, 9×9, Round mechanics, Scoring)
  - Protocol Termination Conditions (V2)
  - Airdrop System (V2)
  - Testing Guidelines (8 domain test suites)
  - Edge Cases to Test (Concurrency, Boundary, Invalid states)
  - QA Checklist (Protocol setup, Position management, Epoch & payout, Staking, Trading, Termination)

### Authentication & Authorization
- **`docs/AUTH.md`** — Система аутентифікації та авторизації:
  - Authentication Model (Wallet-based, no passwords/sessions/JWTs)
  - Whitelist Access Control (AuthGuardProvider, Authorized Keys, Agent Mode)
  - Signing Service Authentication (HMAC-SHA256, environment-specific secrets, per-env keypairs)
  - On-Chain Access Control (Server Signer validation, Transfer Hook authorization, open instructions)
  - Backend Notification Auth (Bearer token)
  - Access Control Matrix (10+ actions with auth methods)
  - Security Considerations (Wallet-based, whitelist, HMAC, server signer, admin access)
  - Testing Guidelines (Whitelist, Agent Mode, Signing Service, On-Chain, Backend Notification)
  - Edge Cases & Security Risks (Wallet disconnection, keypair exposure, replay, whitelist bypass, admin escalation)
  - Environment Variables Reference (Frontend, Admin Panel, Signing Service, Backend)
  - Common Issues & Debugging (Unauthorized redirect, HMAC 401, server signer mismatch, Transfer Hook failures, Agent Mode)

### Integrations & External Dependencies
- **`docs/INTEGRATIONS.md`** — Інтеграції та зовнішні залежності:
  - Solana Blockchain (RPC/WebSocket connection, cluster support, error handling, idempotency)
  - ORAO VRF (random number generation, integration details, error handling)
  - KurrentDB (event streaming, revision tracking, connection retry)
  - Supabase (object storage, token metadata, IDL files)
  - ImageKit (CDN, protocol images, avatars, fallback)
  - Pusher (real-time WebSocket notifications, channel patterns, flow)
  - PostgreSQL (connection methods, shared schema, error handling)
  - Signing Service (isolated microservice, integration, deployment, error handling)
  - Token-2022 Program (extensions: Transfer Hook, Metadata, Group Pointer, Permanent Delegate)
  - External Service Summary (10 services with failure impact)
  - Testing Guidelines (9 integration test suites)
  - Edge Cases & Failure Modes (9 failure scenarios with mitigation)
  - Monitoring & Observability (5 service monitoring areas)
  - Environment Variables Reference (Solana, KurrentDB, Supabase, ImageKit, Pusher, PostgreSQL, Signing Service)
  - Common Issues & Debugging (9 troubleshooting scenarios)
  - Deployment Considerations (service dependencies, health checks, redundancy, scalability)

### Database Schema
- **`docs/DATABASE.md`** — PostgreSQL база даних (Prisma ORM):
  - Entity Relationship Overview (User → Ticket → Lottery → GlobalStatistics)
  - Core Models (User, Lottery/Protocol, Ticket/Position)
  - Score & Earnings Models (UserTicketScore, UserTicketScoreHistory)
  - Field Models (TicketField, TicketFieldHistory)
  - History Models (ProtocolHistory, FieldPayoutHistory, EpochPayoutHistory)
  - Token Staking Models (TokenDeposit, StakingEpochSnapshot)
  - Bonding Curve Models (BondingCurve, BondingCurveTransaction, TokenHolder, BondingCurveSnapshot)
  - Utility Models (SmartContractEvent, GlobalStatistics)
  - Enums (LotteryState, TicketTransactionType, LotteryTransactionType, TicketHistoryActionType)
  - Schema Design Principles (Write Separation, Idempotency, Event Tracking, Unique Constraints)
  - Index Strategy (Read Optimization, Write Optimization)
  - Data Consistency Rules (Pool Amount Integrity, Staking Consistency, Bonding Curve Consistency, Token Supply Consistency)
  - Migration Strategy (Schema Evolution, Zero-Downtime Deployments)
  - Backup & Recovery (Database Backup, Disaster Recovery)
  - Performance Considerations (Connection Pooling, Query Optimization, Write Throughput)
  - Security Considerations (Data Privacy, Access Control, SQL Injection Protection, Data Retention)

### Testing & Coverage
- **`docs/TESTING.md`** — Test Ideas & Coverage Hints:
  - Testing Strategy Overview (Unit, Integration, API/Server Action, Smart Contract, E2E)
  - Priority Order (Smart contracts highest risk, then backend, server actions, frontend, E2E)
  - Smart Contract Tests (Existing tests, Critical Paths, Edge Cases)
  - Backend (be-ticket) Tests (Orchestrators, Services, Game Field Logic)
  - Frontend Tests (Server Actions, Components, E2E flows)
  - Signing Service Tests (Health check, HMAC auth, Transaction signing, Error handling)
  - Database Tests (Unique constraints, Cascade behavior, Singleton uniqueness)
  - Cross-Cutting Test Scenarios (Full lifecycle, Protocol termination, Trading, Buyout, Staking, Real-time updates, Error recovery, Data consistency)
  - Existing Test Infrastructure (Available, Missing/Recommended to Add)
  - Testing Best Practices (Unit, Integration, E2E, Smart Contract)
  - Test Coverage Goals (Minimum targets, Critical path coverage)
  - Mocking Guidelines (When to mock vs NOT to mock)
  - Test Data Management (Seeding strategy, Cleanup strategy)
  - CI/CD Recommendations (Pipeline stages, Fail-fast criteria)

### Open Questions & Gaps
- **`docs/OPEN_QUESTIONS.md`** — Питання та прогалини, що потребують уточнення з командою:
  - Business Logic Questions (7): Buyout price formula, airdrop distribution model, jackpot claim flow, tie-breaking for pools, protocol completion, hold token gating
  - Architecture Questions (4): KurrentDB vs PubSub, event ordering guarantees, retry/dead letter queue, backend concurrency
  - Frontend Questions (4): Wallet whitelist management, Pusher events full list, offline/error states, Agent Mode scope
  - Smart Contract Questions (5): Account size limits, versioned transaction requirements, Transfer Hook exemptions, health ratio thresholds, devnet vs mainnet differences
  - Database Questions (3): LotteryState enum missing states, legacy models, data retention
  - DevOps/Environment Questions (4): Environment parity, deployment process, monitoring & alerting, database migrations
  - Security Questions (3): Rate limiting, transaction replay protection, wallet whitelist bypass
  - Summary (6+8+9=23 questions), Priorities (Must clarify/Should clarify/Nice to know)
  - Action Items (14 high/23 medium/27 low priority)
  - Next Steps (meeting with team, document answers, create test cases)
  - Test Coverage Impact (increased confidence, reduced flakiness, improved edge case coverage)
  - Risk of NOT clarifying

### Додаткова документація
Додаткові документи будуть розміщені в `projects/lorypten/docs/`:
- API documentation (якщо є Swagger/OpenAPI)
- Test plans та test cases
- Deployment guides
- Troubleshooting notes

### 📊 Documentation Summary
- **`DOCUMENTATION_SUMMARY.md`** — Зведений звіт про документацію Lorypten:
  - Структура документації (10 файлів, ~200KB)
  - Огляд кожного документа (Smart Contracts, Backend, Frontend, API, Domain, Auth, Integrations, Database, Testing, Open Questions)
  - Повний QA-пакет для Lorypten
  - Наступні кроки для тестування

---

## 📝 TODO для заповнення

- [ ] Додати Staging та Production URLs
- [ ] Додати Repo URL
- [ ] Додати Jira / Task Board URL
- [ ] Вказати RPC Endpoint (devnet/mainnet)
- [ ] Створити `scripts/` директорію з прикладами скриптів
- [ ] Створити `docs/` для додаткової документації
- [ ] Написати test cases для critical flows
