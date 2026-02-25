# MEMORY.md - Long-Term Memory

## Gmail Integration (ihor.so@nextcode.tech)

**Status:** ✅ Active

**Setup Date:** 2026-02-14

**How it works:**
- IMAP connection to Gmail via App Password
- Automatic checks every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri)
- Jira tickets detected and summarized automatically
- Notifications sent to Telegram

**⚠️ Vacation Mode:**
- NextCode vacation: 2026-02-25 to 2026-03-02 (return Monday 2026-03-03)
- Do NOT send Jira ticket notifications during vacation
- Resume normal checks on 2026-03-03

**Credentials Location:**
- App Password: `/Users/ihorsolopii/.openclaw/workspace/.gmail_config`
- Seen IDs: `/Users/ihorsolopii/.openclaw/workspace/.gmail_seen_ids.json`

**Cron Job:** `40d004fa-6219-438a-bf2e-a0dad924a18f` (Gmail Check - NextCode)

**Scripts:**
- Checker: `/Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py`
- Notifier: `/Users/ihorsolopii/.openclaw/workspace/scripts/gmail_notify.py`

**Manual Check:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py
```

**Reinitialize (mark all as seen):**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py --init
```

---

## Jira API Integration

**Status:** ✅ Active

**Setup Date:** 2026-02-14

**How it works:**
- `go-jira` CLI installed
- API Token configured for authentication
- Full access to ticket details, comments, status

**Credentials:**
- API Token: `/Users/ihorsolopii/.openclaw/workspace/.jira_token`
- Config: `~/.jira.yml`
- Domain: `https://next-t-code.atlassian.net`
- User: `ihor.so@nextcode.tech`

**Fetch Ticket:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/jira_fetch.py CT-722
```

**Direct CLI:**
```bash
export JIRA_API_TOKEN=$(cat ~/.openclaw/workspace/.jira_token)
jira view CT-722 -e https://next-t-code.atlassian.net -u ihor.so@nextcode.tech
```

---

## NextCode Jira Tickets Status (as of 2026-02-14)

**Open/Needs Attention:**
- CT-722 - Deposit streak bonus bug (DiaOl waiting for status update ⚠️)

**Recently Completed:**
- CT-727 - Recent wins widget ✅ Done
- CT-736 - Regular Bonuses prod config ✅ Done
- CT-560 - Special bonuses redesign ✅ Done

---

## Website API (Client Frontend)

**REST API** — ендпоїнти, які викликає фронтенд-клієнт

**Environments:**
- **Prod:** https://websitewebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3
- **QA:** https://websitewebapi.qa.sofon.one/swagger/index.html?urls.primaryName=API+v3
- **Dev:** https://websitewebapi.dev.sofon.one/swagger/index.html?urls.primaryName=API+v3

**Auth:** Session token у хедерах

**GraphQL Registration (Minebit, partnerId = 5):**
```
URL: https://minebit-casino.prod.sofon.one/graphql
Mutation: PlayerRegisterUniversal
Email format: test-{jiraticketIfExist}timetoday@nextcode.tech
Password: Qweasd123!
```

**Key Headers:**
- `website-locale: en`
- `website-origin: https://minebit-casino.prod.sofon.one`
- `x-time-zone-offset: -60`

---

## BackOffice API (Admin)

**Адмінський API** — створення бонусів, управління балансом, інформація про гравців

**Environments:**
- **Prod:** https://adminwebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3 (UserId: 560)
- **QA:** https://adminwebapi.qa.sofon.one/swagger/index.html?urls.primaryName=API+v3 (UserId: 1)
- **Dev:** https://adminwebapi.dev.sofon.one/swagger/index.html?urls.primaryName=API+v3 (UserId: 1)

**Auth:** Header `UserId: <adminUserId>`

**Приклад запиту:**
```bash
curl 'https://adminwebapi.prod.sofon.one/.../some-endpoint' \
  -H 'UserId: 560' \
  -H 'Content-Type: application/json'
```

**Можливості:**
- Створення/зміна бонусів
- Отримання інформації про бонуси, тригери, промо
- Поповнення/зміна балансу гравця (credit/debit)
- Детальна інформація про гравців, транзакції, ставки

---

## API Documentation

**Website API v3 Analysis:** `/Users/ihorsolopii/.openclaw/workspace/API_ANALYSIS_WEBSITE_V3.md`
- 125 endpoints, 19 groups
- Client, Product, Bonus, Payment, Bet, 2FA, etc.

**BackOffice API v1 Analysis:** `/Users/ihorsolopii/.openclaw/workspace/API_ANALYSIS_BACKOFFICE_V1.md`
- 368 endpoints, 35 groups
- Client, Bonus, Product, Partner, Report, etc.

**Swagger JSON Files:**
- Website v3: `swagger_website_prod_v3.json` (424KB)
- BackOffice v1: `swagger_backoffice_prod_v1.json` (1.3MB)

---

## Wallet Service API

**Wallet Operations** — баланс, транзакції, корекції

**Swagger:** https://wallet.dev.sofon.one/swagger/index.html

**Environments:**
- **Dev:** https://wallet.dev.sofon.one
- **QA:** https://wallet.qa.sofon.one
- **Prod:** https://wallet.prod.sofon.one

**Auth:** Немає авторизації (відкритий API)

**Key Endpoints:**
- **GET** `/{partnerId}/api/v1/balance/{clientId}/{currency}` — Перевірити баланс
- **GET** `/{partnerId}/api/v1/transaction/list/client/{clientId}` — Список транзакцій
- **POST** `/{partnerId}/api/v1/transaction/correction/debit` — Додати гроші ✅
- **POST** `/{partnerId}/api/v1/transaction/correction/credit` — Зняти гроші ❌

**Приклад запиту:**
```bash
curl 'https://wallet.dev.sofon.one/5/api/v1/balance/59107/USD'
```

**Відповідь:**
```json
{
  "Balances": { "Unused": 30.91 },
  "AvailableMain": 30.91,
  "AvailableBonus": 0.0,
  "Currency": "USD"
}
```

---

## Bonus Configuration

### Confluence Bonuses Setup

**Source:** https://next-t-code.atlassian.net/wiki/spaces/QS/pages/204111989/Bonuses+setup

**Campaign (Bonus)** — промо, яке гравці бачать на брендах і можуть активувати.

### Етапи налаштування промо:
1. Створити промо в BackOffice
2. Налаштувати UI конфігурацію в Strapi
3. Мати тестового гравця, який відповідає критеріям (segment)

### Типи бонусів:
- **Wager Casino** — бонусні гроші + turnover balance (треба проставити)
- **Freespins** — безкоштовні спіни в іграх
- **Split Match + Freespins** — спіни + вейджер на виграш
- **Cashback** — інтеграція з Smartico

### Сегментація:
- Гравець з 0 депозитів = сегмент "non-depositors" → бачить бонуси для 1-го депозиту
- Після 1-го депозиту сегмент змінюється → бонуси для 1-го депозиту недоступні

### 📘 Complete Bonus System Documentation

**File:** `bonus-analysis/BONUS_SYSTEM_DOCUMENTATION.md` (14.8KB)

**Source:** Confluence QA Space + Google Docs Bonus Tech Dock (via Comet browser)

**Added:** 2026-02-23

**Contents:**
- Архітектура (BO, Strapi, Smartico, Kafka)
- Всі типи бонусів (Welcome Pack, Signup Code, Promo Code, Regular Bonuses)
- General Setup поля (Active, Name, Turnover Count, Min/Max CO, Is Smartico...)
- Trigger Settings (Any Deposit, Specific Deposit, PromoCode, Campaign Link)
- Max Cashout Multiplier формули
- Gap Analysis тест-кейсів
- Критичні моменти для тестування

### ⚠️ Regular Bonuses — Real Data (BO Prod)

**Updated:** 2026-02-23

**Source of Truth:** BO Prod data (Confluence docs may be outdated)

**Regular Bonuses (BO Prod):**
| Bonus | ID | BonusTypeId | TurnoverCount | IsSmartico | CRON |
|-------|----|----|--------------|------------|------|
| Monthly | 8301 | 11 | **null** | true | `0 0 1 * *` |
| Weekly | 8299 | 11 | **null** | true | `0 0 * * 6` |
| Cashback | 7207 | 11 | **null** | true | `0 0 * * 2,5` |

**Key Facts:**
- **TurnoverCount: null** = NO WAGERING for Regular Bonuses
- **BonusTypeId: 11** = CampaignCash
- **IsSmartico: true** = Calculated by Smartico
- **CT-45 applies to ALL** = All Regular Bonuses can be claimed parallel

**States:**
1. **Waiting for reward** — Timer visible, waiting for calculation
2. **Ready for claim** — Amount calculated, button: "Claim ${amount}"
3. **Claimed** — Amount credited to real balance (NO Active Bonuses entry)

**UI:**
- Amount shown on card when "Ready for claim"
- Button: "Claim ${amount}"
- Progress bar: TIME progress (NOT wagering)
- Minimum amount: $0.3

---

## BO-Асистент Minebit (Флоу депозиту)

**Джерело правди:** Swagger BO (`adminwebapi`)

**Env UserId:**
- Prod: 560
- QA: 1
- Dev: 1

### Стандартний флоу:

**1. Реєстрація/Пошук клієнта**
- `apiClientRegisterClient` — створити нового
- `apiClientGetClientById` — отримати за ID

**2. Перевірка IsTest**
- Якщо `IsTest != true` → питаю підтвердження
- `apiClientChangeClientDetails` з `IsTest = true`

**3. Створення депозиту**
```json
{
  "amount": 30,
  "clientId": 1147383,
  "currencyId": "USD",
  "externalTransactionId": "<random 15-20 chars>",
  "partnerPaymentMethodId": 19,
  "paymentRequestType": "Deposit"
}
```
- Ендпоїнт: `MakeManualRedirectPayment` або аналог з Payment tag

**4. MarkAsPaid (обов'язково!)**
```json
{
  "Comment": "test",
  "PaymentRequestId": 12345,
  "ChangeStatusTo": "MarkAsPaid",
  "ProcessingType": 0,
  "Type": "Deposit"
}
```
- Ендпоїнт: PATCH `Payment/ChangeStatus`

### Правила безпеки:
- Завжди питаю підтвердження перед змінами
- Депозити тільки для `IsTest = true`
- Не показую реальні токени/секрети

### ⚠️ Важливо — інвертована логіка:
```
CreateCreditCorrection → DEBITS (знімає гроші) ❌
CreateDebitCorrection  → CREDITS (додає гроші) ✅
```

### Ключові operationId:
- `apiClientGetClientById`
- `apiClientChangeClientDetails`
- `apiClientRegisterClient`
- `MakeManualRedirectPayment`
- `Payment/ChangeStatus`

---

## Playwright Framework Architecture

**File:** `/Users/ihorsolopii/.openclaw/workspace/MINEBIT_PLAYWRIGHT_ARCHITECTURE.md`

**Test Distribution:**
- API Tests: 60% (fast, reliable)
- E2E Tests: 25% (critical flows)
- Mobile Tests: 10% (mobile UI)
- Mocked Tests: 5% (edge cases)

**Key Features:**
- Multi-project config (API, E2E, Mobile, Mocked)
- Page Object Model
- API Client Layer (Website + BackOffice + GraphQL)
- Test Fixtures (auth, player creation)
- Mock handlers for UI states

---

## Notes
- All emails from jira@next-t-code.atlassian.net are Jira notifications
- Ticket format: CT-XXX or PR-XXXX
- Jira base URL: https://next-t-code.atlassian.net/browse/

---

## Playwright Automation Project

**Location:** `/Users/ihorsolopii/Documents/minebit-e2e-playwright`

**Important:** When asked to add E2E/API tests → work in this project, NOT in workspace.

**Structure (reorganized 2026-02-16):**
```
tests/
├── api/
│   ├── smoke/          # 6 tests, ~5 min (critical path)
│   ├── regression/     # 9 tests, ~15 min (full coverage)
│   └── tickets/        # 17 tests (CT-751, CT-754...)
├── e2e/
│   └── smoke/          # E2E smoke tests (auth, games, wallet...)
└── regression/         # E2E regression (deposit, games)
```

**Run commands:**
```bash
cd /Users/ihorsolopii/Documents/minebit-e2e-playwright

# API tests
npx playwright test --project=api-smoke      # 6 tests, critical
npx playwright test --project=api-regression # 9 tests, detailed
npx playwright test --project=api-tickets    # 17 tests, ticket-specific
npx playwright test CT-754                   # Specific ticket tests

# E2E tests
npx playwright test --project=e2e-chromium   # Desktop Chrome
npx playwright test --project=e2e-mobile-safari  # iPhone
```

**Adding ticket tests:**
1. Create `tests/api/tickets/CT-XXX-description.spec.ts`
2. Add tags: `@api`, `@ticket`, `@CT-XXX`
3. Run: `npx playwright test --project=api-tickets CT-XXX`

---

## API Testing Strategy (2026-02-15)

**Approach:** API Tests + API for E2E setup

| Test Type | Purpose | When |
|-----------|---------|------|
| **API Tests** | Test API directly | New/changed endpoints |
| **API in E2E** | Setup test data | Always for E2E tests |

**Player Fixtures:**
- `testPlayer` — creates player via API (no balance)
- `testPlayerWithBalance` — creates player + 100 USD balance

**Files:**
- `src/fixtures/player.fixture.ts` — E2E player fixtures
- `src/fixtures/api.fixture.ts` — API test fixtures
- `src/api/clients/` — GraphQL, Website API, BackOffice API clients

**Current Status:**
- API tests: 11 passed, 4 failed (balance issue)
- E2E tests: ready to run
- TypeScript: 14 warnings (unused vars, non-blocking)

---

## Project Configuration (2026-02-15)

**ESLint:** `eslint.config.mjs` (flat config)
- TypeScript support
- Playwright plugin
- Prettier integration

**Prettier:** `.prettierrc`
- Single quotes, trailing comma es5, print width 100

**Scripts:**
```bash
npm run type-check  # TypeScript check
npm run lint        # ESLint
npm run format      # Prettier
npm run check       # Both
```

**Installed Browsers:**
- Chromium 1200/1208 ✅
- WebKit 2248 ✅
- Firefox ❌ (not installed)

**Mobile Devices:**
- Pixel 7, iPhone 13/14, iPad Pro ✅

---

## Installed Skills (Use When Needed)

### prompt-engineering-expert
**Use when Ihor has problems writing prompts**

Location: `/Users/ihorsolopii/.openclaw/workspace/skills/prompt-engineering-expert`

**Capabilities:**
- Prompt analysis & optimization
- Custom instructions design for AI agents
- Chain-of-thought, few-shot, XML techniques
- Troubleshooting prompt issues
- Best practices for Gemini/Cline/OpenClaw prompts

**When to suggest:**
- "Як написати промпт для..."
- "Чи хороший цей промпт?"
- "Чому цей промпт не працює?"
- "Оптимізуй інструкції для агента"

---

### Notion API
**Status:** ✅ Configured

**API Key:** `~/.config/notion/api_key`

**Workspace pages:**
- Need to do - TODO Tracker
- FamAssistant
- US vs Europe AI Market Analysis
- Prospects Database
- AI Dev Tools Consulting Marketplace

**Use for:** Creating notes, managing TODOs, database queries

---

### clawddocs
**Use for OpenClaw documentation questions**

- Setup providers (Discord, Telegram, WhatsApp)
- Cron jobs, webhooks, automation
- Troubleshooting gateway/browser issues
- Config snippets

---

### playwright-mcp
**Status:** ✅ Installed

**Use for:** MCP-based browser automation (alternative to playwright-cli)

---

### reflect-learn
**Status:** ✅ Auto-reflection ENABLED

**Location:** `~/.reflect/`

**What it does:**
- Analyzes conversations for learnings from corrections
- Proposes updates to agent files, MEMORY.md, or new skills
- "Correct once, never again" philosophy

**Commands:**
- `/reflect` — Run reflection now
- `/reflect status` — Show state & metrics
- `/reflect review` — Review low-confidence learnings

**Auto-triggers:** PreCompact hook (before context compaction)

---

## Pending Tasks

**Tomorrow 13:30:** Remind about balance API issue
- `CreateDebitCorrection` not adding balance
- Need to investigate why

---

## Austria Information Hub (Notion)

**Status:** ✅ Active

**Created:** 2026-02-24

**Notion Page:** https://www.notion.so/Austria-31121ca6a7778147af0fdd5b73a52d64

**Location:** Ihor - Profile → Austria - Інформаційний хаб

**What's inside:**
- Ключові дати та дедлайни (тимчасовий захист, пенсії, RWR+)
- Гарячі лінії (BBU, ПФУ)
- Корисні посилання (категоризовані):
  - 🇺🇦 Міграція/Українці (BBU, Familienbeihilfe, Aufenthaltsrecht, пенсії)
  - 💼 Податки/Працівники (BMF, FinanzOnline)
  - 👶 Сім'я/Діти (MeineSV, Wien.gv.at)
  - 📰 Новини/Уряд (Bundeskanzleramt, BFA, Oesterreich.gv.at)
  - 🌐 Міжнародні організації (UNHCR)

**How to update:**
- Користувач пише "/austria" або "перевір Австрію"
- Я роблю пошук по офіційних джерелах
- Нові посилання додаю в Notion

**Last Check:** 2026-02-24

**Cron Job:** `be670aac-f0af-462d-bc09-56cfc12ca0e4` (Austria Weekly Check — понеділок о 9:00)

---

## 🎯 Фінансова Ціль: Квартира

**Мета:** Накопичити ~50,000 € на квартиру (Відень або Дюссельдорф)

**Статус:** Активна

**Дата постановки:** 2026-02-19

**Контекст:**
- Власник Seeker phone on Solana
- Інтерес до крипти
- Сім'я (дружина + син)
- Працює на двох роботах (Sdui + NextCode)

**Що я можу робити:**
- Моніторинг крипто ринків (Solana, DeFi протоколи)
- Аналіз пасивного доходу (staking, yield farming, dividend stocks)
- Розрахунки та планування
- Пошук можливостей
- Регулярні нагадування та перевірка прогресу

**Профіль:**
- IT-спеціалісти (без підприємницького досвіду)
- Стратегія: заробіток + пасивні інвестиції (не створення бізнесу)
- Класичний шлях накопичення

**Фінансові дані (2026-02-19):**
- Поточні заощадження: ~15-17,000 €
- Сімейний дохід: ~7,500-7,800 €/міс
- Витрати: ~6,000-6,500 €/міс
- Потенціал заощаджень: 1,000-1,800 €/міс (очікується деталізація витрат)
- Горизонт: 5 років
- Ризик-профіль: Збалансований
- Віра в crypto game-changer
