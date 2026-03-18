# Master Project Knowledge & Abstracted Learnings

_This document is maintained autonomously by Nexus Orchestrator. It contains the abstracted rules, architectural facts, and recurring patterns discovered by QA Agent and API Agent over time. Nexus uses this to ensure mistakes are never repeated._

## 1. API & Backend Rules

### 1.1 Critical Flow Testing
- **Registration → Login**: Always test together. Broken login after registration = P0 blocker
- **OAuth Tokens**: Verify backend accepts mock tokens on dev/stage BEFORE designing OAuth tests
- **If mock tokens rejected**: Request real credentials or test mode flag from backend team

### 1.2 API Test Data Generation
- **Telegram WebApp hash**: Can generate using HMAC-SHA256 with bot token (Python libraries available)
- **Google OneTap JWT**: Can mock for testing with Playwright
- **Rule**: Always research solutions (web search, mocks, local generators) for at least 10 minutes before reporting blockers

---

## 2. UI & Playwright Patterns

### 2.1 Test Plan Design Rules
- **Tool Reality Check**: Test plans must use ONLY available tools (API, curl, Playwright, read, write, exec, web_search)
- **NO assumptions about**: DB access, admin APIs, external systems without verification
- **Alternative to DB queries**: Use API responses to validate state instead

### 2.2 Slack Communication Rules
- **Self-contained reports**: Every Slack report must include TL;DR with key flows/edge cases
- **Actionable without attachments**: Message should be enough to make decisions
- **Always include**: 3-5 key flows being tested + critical edge cases

### 2.3 Smoke Test Rules
- **Internal domains priority**: NEVER propose public domains (e.g., minebit.com) for backend smoke tests
- **Always prioritize**: Internal portals (e.g., minebit-casino.prod.sofon.one)
- **VPN check**: Verify VPN status before writing test plan
- **Auth required**: Guest checks rarely have value for casino/finance — always include authorized checks

### 2.4 Credentials Hunting (QA Agent)
- **Mandatory first step**: Search local E2E repository (`fixtures`, `locators`, `env`) for test credentials
- **Alternative**: Create new user via API before halting at login screen
- **FORBIDDEN**: Stop at login window and report error without attempting to find/create credentials

---

---

## 3. Existing Test Infrastructure — minebit-e2e-playwright

**Location:** `/Users/ihorsolopii/Documents/minebit-e2e-playwright`

This is the existing Playwright E2E project for Minebit. Agents MUST check it before creating anything from scratch.

### 3.1 Page Objects & Components (ready to reference)

| Component | Path | What it does |
|-----------|------|-------------|
| `SignUpModal` | `src/gui/minebit/modals/auth/SignUpModal.ts` | Registration modal — fields, validation, submit |
| `LogInModal` | `src/gui/minebit/modals/auth/LogInModal.ts` | Login modal — email/password flow |
| `AuthModal` | `src/gui/minebit/modals/auth/AuthModal.ts` | Auth modal base (shared logic) |
| `WalletModal` | `src/gui/minebit/modals/WalletModal.ts` | Wallet/cashier modal |
| `HomePage` | `src/gui/minebit/pages/home/HomePage.ts` | Homepage selectors and actions |
| `BonusesPage` | `src/gui/minebit/pages/bonuses/BonusesPage.ts` | Bonuses page |
| `QuestsPage` | `src/gui/minebit/pages/quests/QuestsPage.ts` | Quests/missions page |
| `GamesLobbyPage` | `src/gui/minebit/pages/games/GamesLobbyPage.ts` | Game lobby |
| `DepositPage` | `src/gui/minebit/cashier/DepositPage.ts` | Deposit flow |
| `WithdrawalPage` | `src/gui/minebit/cashier/WithdrawalPage.ts` | Withdrawal flow |
| `HeaderComponent` | `src/gui/minebit/components/header/HeaderComponent.ts` | Header navigation |
| `SidebarComponent` | `src/gui/minebit/components/sidebar/SidebarComponent.ts` | Sidebar navigation |
| `RecentTopWinsWidget` | `src/gui/minebit/components/widgets/RecentTopWinsWidget.ts` | Recent Winners slider |

### 3.2 Fixtures (ready to use)

| Fixture | Path | What it does |
|---------|------|-------------|
| `player.fixture.ts` | `src/fixtures/player.fixture.ts` | Create test player via API |
| `api.fixture.ts` | `src/fixtures/api.fixture.ts` | API helpers for tests |
| `test-data.fixture.ts` | `src/fixtures/test-data.fixture.ts` | Test data setup (balance, deposits, bonuses) |
| `core-ui-fixture.ts` | `src/fixtures/core-ui-fixture.ts` | Base UI test fixture |
| `minebit-ui-fixture.ts` | `src/fixtures/brands/minebit-ui-fixture.ts` | Minebit-specific UI fixture |

### 3.3 Utilities

| Utility | Path | What it does |
|---------|------|-------------|
| `ApiClient.ts` | `src/utils/api/ApiClient.ts` | HTTP client for platform API |
| `DataGenerator.ts` | `src/utils/DataGenerator.ts` | Generate test emails, passwords, names |
| `GlobalUsers.ts` | `src/constants/GlobalUsers.ts` | Pre-configured test accounts |
| `uiHelpers.ts` | `src/utils/uiHelpers.ts` | Common UI action helpers |

### 3.4 Rules for Agents

1. **Before creating a new selector** — check if a Page Object already has it
2. **Before writing registration logic** — use `player.fixture.ts` or `SignUpModal.ts`
3. **Before writing login logic** — use `LogInModal.ts` or API-based auth from `api.fixture.ts`
4. **Before creating test data** — use `test-data.fixture.ts` or `DataGenerator.ts`
5. **Before inventing UI navigation** — check `HomePage.ts`, `HeaderComponent.ts`, `SidebarComponent.ts`
6. **When testing Recent Winners** — reference `RecentTopWinsWidget.ts` for selectors and structure

### 3.5 Existing Test Specs (reference for patterns)

- `tests/api/smoke/auth/registration.spec.ts` — API registration flow
- `tests/api/smoke/bonus/eligible-bonuses.spec.ts` — Bonus eligibility
- `tests/api/smoke/player/balance.spec.ts` — Player balance
- `tests/e2e/smoke/quests/quests.spec.ts` — Quests E2E
- `tests/regression/payments/deposit.spec.ts` — Deposit regression
- `tests/regression/games/games.spec.ts` — Games regression

---

## 4. General Business Logic
*(Will be populated by Nexus)*
