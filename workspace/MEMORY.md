# MEMORY.md - Long-Term Memory

## Gmail Integration (ihor.so@nextcode.tech)

**Status:** ✅ Active

**Setup Date:** 2026-02-14

**How it works:**
- IMAP connection to Gmail via App Password
- Automatic checks every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri)
- Jira tickets detected and summarized automatically
- Notifications sent to Telegram

**✅ Vacation Mode завершено:**
- NextCode vacation: 2026-02-25 to 2026-03-02 (completed)
- Jira ticket notifications відновлено з 2026-03-02
- Нормальний режим роботи активовано

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

### ⚠️ Дві системи авторизації (критично!)

**Відкрито:** 2026-03-03 — Для автоматизації депозитів потрібно розрізняти дві системи:

| Система | URL | Авторизація | Повертає PaymentRequestId? |
|---------|-----|-------------|----------------------------|
| **AdminWeb API** | `https://adminwebapi.prod.sofon.one/api/` | `UserId: 560` (заголовок) | ❌ Ні (`{"PaymentUrl": null}`) |
| **BackOffice UI API** | `https://backoffice.prod.sofon.one/mgw/admin/` | `Bearer` токен (JWT) | ✅ Так (можна викликати `MarkAsPaid`) |

**Ключова відмінність:**
- `MakeManualRedirectPayment` через **AdminWeb API** створює депозит, але не повертає `PaymentRequestId` → неможливо викликати `MarkAsPaid` → депозит залишається в `InProgress` → **подія депозиту не тригериться** → бонуси не нараховуються.
- Той самий ендпоїнт через **BackOffice UI API** з Bearer токеном повертає `PaymentRequestId` → можна викликати `MarkAsPaid` → депозит завершується → подія тригериться → **бонуси нараховуються**.

**Повний автоматизований флоу (працює):**
1. `POST /mgw/admin/api/Client/MakeManualRedirectPayment` (Bearer токен)
2. `POST /mgw/admin/api/v2/Payment/GetAllWithTotal` (пошук за `clientId`)
3. `PATCH /mgw/admin/api/v2/Payment/ChangeStatus` (`MarkAsPaid`)

**Скрипт автоматизації:** `deposit_streak_auto.py` (див. дневник 2026-03-03)

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

**⚠️ Увага:** Цей флоу використовує AdminWeb API (`UserId: 560`). Для тригеру бонусів потрібен **BackOffice UI API** з Bearer токеном (див. розділ "Дві системи авторизації" вище).

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

**Для BackOffice UI API (Bearer токен):**
- `POST /mgw/admin/api/Client/MakeManualRedirectPayment`
- `POST /mgw/admin/api/v2/Payment/GetAllWithTotal`
- `PATCH /mgw/admin/api/v2/Payment/ChangeStatus`
- `GET /mgw/admin/api/v2/Payment/GetById/{id}`

---

## UI Knowledge Base (AI Page Object Model)

**Location:** `/Users/ihorsolopii/.openclaw/workspace/ui-knowledge/minebit/`

**Purpose:** 
Long-term memory for UI selectors. To avoid parsing the whole DOM every time and breaking tests when UI changes:
1. **Always check this directory first** before creating Playwright scripts or doing interactive testing (e.g. `bonuses-page.json`).
2. If a selector doesn't work during a task, fix it via snapshot analysis and **IMMEDIATELY update the JSON file** with the new selector so it's remembered for next time.
3. Keep logic descriptions (animations, wait states) in the `known_behaviors` key.

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

## 🧵 Slack Threading System for Jira Tickets

**Status:** ✅ Active

**Setup Date:** 2026-02-26

**How it works:**
- When a new Jira ticket arrives in `#qa-testing` channel, system automatically saves its `thread_ts` (Timestamp) to `/Users/ihorsolopii/.openclaw/workspace/jira_threads.json`
- This enables threaded conversations where all ticket-related updates stay in one place

**🔴 IRON RULE — Mandatory Threading:**

When Ihor asks you to analyze or test a specific ticket (e.g., CT-757), you MUST:

1. **Read the threads file:**
   ```bash
   cat /Users/ihorsolopii/.openclaw/workspace/jira_threads.json
   ```

2. **Find the `ts` for the requested ticket** (e.g., `"CT-757": "1772119587.021079"`)

3. **Send ALL communications in the thread:**
   - Test reports
   - Analysis results
   - Screenshots
   - Suggestions

4. **Use the Slack wrapper script:**
   ```bash
   python3 /Users/ihorsolopii/.openclaw/workspace/scripts/slack_message_helper.py \
     --channel C0AH10XDKM2 \
     --text "Your message here" \
     --thread_ts "TICKET_TS_FROM_JSON"
   ```

**Why this matters:**
- Keeps the `#qa-testing` channel clean
- All ticket history in one continuous thread
- Easy to track conversation per ticket
- Follows the USER.md Rule #8

**Example workflow:**
```
Ihor: "Analyze CT-757"
→ You: Read jira_threads.json → find CT-757 ts → "1772119587.021079"
→ You: Send analysis via slack_message_helper.py with --thread_ts "1772119587.021079"
→ Result: All CT-757 discussion in one thread
```

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

---

## 🍔 Структурована методологія тест-дизайну (Burger Approach)

**Додано:** 2026-02-28  
**Джерело:** Ihor's structured QA approach  
**Файл:** `QA_TEST_DESIGN_APPROACH.md`

### Основна ідея
Методологія "бургер" — це структурований підхід до тест-дизайну, де кожен шар відповідає за певний аспект:

0. **Memory Check (перед будь-яким аналізом)** — пошук релевантного контексту в пам'яті
1. **Feature container (котлета/судок)** — контекст фічі, вимоги, обмеження
2. **Testing types (салат)** — види тестування (functional, security, usability...)
3. **Test design techniques (помідор)** — техніки (EP, BVA, Decision Tables...)
4. **Principles & risk-based approach (булочка)** — принципи, ризики, пріоритезація
5. **Test scenarios (готовий бургер)** — сценарії тестування

### Memory Check (деталі)
**Перед початком будь-якого аналізу завжди шукай релевантний контекст у пам'яті:**

**MEMORY CHECK — виконуй перед кожним тікетом:**

1. **Доменні патерни**
   - Чи тестував я схожі фічі раніше? (наприклад, призначення бонусів, ліміти депозитів, KYC флоу, теги, операції з гаманцями)
   - Які edge cases або баги знаходили в схожих тікетах?
   - Які інтеграції були задіяні і що зламалося минулого разу?

2. **Відомі ризики з пам'яті**
   - Чи є відомі нестабільні області в цьому домені? (наприклад, затримки синхронізації Smartico, race conditions Wallet Service, розбіжності статусів Provider Manager)
   - Чи є відомі проблеми зворотної сумісності?
   - Чи є повторювані патерни дефектів для цього типу змін?

3. **Наявне тестове покриття**
   - Чи є вже Playwright тести (API або UI) для цієї області?
   - Які тестові файли / хелпери вже існують, які можна повторно використати?
   - Які патерни тестових даних вже працюють в цьому середовищі?

4. **Знання про середовище та конфігурацію**
   - Чи є відомі проблеми, специфічні для середовища, для цієї області функціоналу?
   - Чи є специфічні тестові акаунти, токени або сиди, які варто використовувати?

**Виводи це коротким блоком:**
```
Memory relevant to this ticket:
- Similar tickets tested: ...
- Known risks/patterns: ...
- Existing test coverage: ...
- Reusable helpers/accounts: ...
- Nothing relevant found (if memory is empty for this area)
```

**Тільки після Memory Check → переходь до layered analysis (Simple або Full режим залежно від складності тікету).**

### Коли застосовувати
- **Завжди** при отриманні задач на тестування нової фічі
- **Завжди** при аналізі тікетів Jira для Minebit/NextCode
- **Завжди** при проектуванні тестів для Lorypten
- **Особливо важливо** коли вимоги нечіткі — методика допомагає виявити гепи

### Ключові правила
- **Завжди починати з Memory Check** — перевіряти наявний контекст перед аналізом
- Не пропускати шари — проходити послідовно 0-5
- Якщо вимоги незрозумілі — явно вказувати, задавати питання
- Прив'язувати кожен сценарій до вимоги, виду тестування та техніки
- Застосовувати домен-специфічні адаптації (казино, платежі, Web3)
- **CRITICAL GUARDRAIL (TEST TYPES):** Ніколи не генерувати Security/Performance/Load/Usability тести для функціональних тікетів, якщо користувач явно цього не попросив.
- **CRITICAL GUARDRAIL (TESTRAIL):** Перед відправкою або генерацією тест-кейсів для TestRail, **ЗАВЖДИ валідувати** їх за правилами з файлу `TESTRAIL_STANDARDS.md` (Language = English, no Jira IDs in titles, auto-learning dictionary).

### Адаптації для наших проєктів
**Minebit/NextCode (казино):**
- Завжди враховувати платежі, бонусні системи, KYC
- Використовувати Swagger First підхід (API перед UI)
- Пам'ятати про Smartico модалки
- Тестувати на рівні API (Website API, BackOffice API, Wallet API)

**Playwright automation:**
- Оцінювати, які сценарії можна автоматизувати
- Використовувати `getByRole()`, `getByText()` замість CSS селекторів
- Налаштовувати тестові дані через API перед UI тестами

**Lorypten (Solana Web3):**
- Тестувати транзакції блокчейну, підключення гаманців
- Перевіряти gas fees, network conditions
- Тестувати smart contract interactions

---

## 🎯 Мій підхід до роботи з проєктами

**🎯 КРИТИЧНИЙ KPI (60-65% автономності):**
- **Ціль:** 60-65% автономності та якості тестування в NextCode
- **Що трекаю:**
  - Прогрес у розумінні процесів NextCode
  - Пам'ятаю сам продукт MineBit
  - Знаю де які елементи знаходяться
  - Знаю стандартний юзер флоу
  - І т.д.
- **Як вимірюю:** скільки можу працювати автономно без уточнень

---

**Два проєкти з різними рівнями документації:**

### Lorypten (Solana Web3)
- ✅ **Повна документація** (~200KB) — готовий QA-пакет
- ✅ Структура, архітектура, API, домен, тестова стратегія
- ✅ Коли працюю з Lorypten — маю повний контекст

### Minebit (NextCode) — фріланс проєкт
- ⚠️ **Проблеми з документацією** — великі гепи
- ⚠️ Jira повільні та нестабільні
- ⚠️ Складно пояснити як тестувати той чи інший тікет
- ⚠️ Багато модалок від Smartico — потрібно хендлити

**Моє завдання в Minebit:**
- ✅ **Проявляти ініціативу** — не чекати, а пропонувати покращення процесів
- ✅ **Покращувати опис задач** — робити їх зрозумілими та детальними
- ✅ **Exploratory testing** — порівнювати з TestRail, заповнювати гепи
- ✅ **Playwright best practices** — використовувати `getByRole`, `getByText` замість довільних селекторів
- ✅ **Розуміти Smartico модалки** — знати які модалки існують та як їх хендлити

**Коли Ihor запитує про Minebit:**
1. Автоматично переключаюсь в режим "Minebit — потребує більше контексту та ініціативи"
2. Не чекаю на детальні інструкції — пропоную варіанти
3. Якщо не розумію завдання — запитую уточнення, але не пасивний
4. Пам'ятаю про Smartico модалки — згадую про них в тестах

**Playwright підхід для Minebit:**
- Використовувати `getByRole()` — найнадійніший та доступний метод
- Використовувати `getByText()` — коли потрібно знайти текст
- Уникати довільних селекторів (`css selectors`) коли це можливо
- Для модалок Smartico — перевіряти чи відкрити, чекати `toBeVisible()`, закривати після тесту

**Minebit Cheat Sheet:**
- **`projects/nextcode/MINEBIT_CHEAT_SHEET.md`** — Швидкий довідник для роботи з Minebit:
  - Відомі проблеми (документація, повільна Jira, модалки Smartico)
  - Мій підхід в Minebit (ініціатива, покращення описів)
  - Playwright best practices (getByRole, getByText)
  - Exploratory testing процес
  - Smartico modal handling pattern
  - Тестовий чекліст
  - Коли я не розумію (мої запитання)
  - **🔑 Swagger First — не йди в лоб з UI!**

**Важлива порада від Ihor:**
> "Є доступ до Swagger документації NextCode. Використовуй її якщо потрібно щось протестувати на UI: реєстрація, поповнення балансу, KYC, email verification. Не йди прямо в лоб з пошуком елементів на UI — оптимізовуй процеси."

**Що це означає:**
1. Перед UI тестуванням — дивись в Swagger (Website API / BackOffice API)
2. Розумій структуру запиту (параметри, типи даних)
3. Можливо протестувати API напряму
4. Тільки потім переходити до UI — тепер ти знаєш що саме відбувається

---

## 🛠️ Test Data Scripts (Автоматизація підготовки даних)

**Створено:** 2026-03-03

**Локація:** `/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/test-data-scripts/`

**Призначення:** Автоматизована підготовка тестових даних для Minebit/NextCode через API.

### Доступні скрипти

| Скрипт | Функція |
|--------|---------|
| `01_create_test_player.py` | Створення тестового гравця (GraphQL/Website API) |
| `02_set_test_player_balance.py` | Встановлення балансу (Wallet/BackOffice API) |
| `03_create_deposit_flow.py` | Повний флоу депозиту через BackOffice (**AdminWeb API**, `UserId` auth) |
| `deposit_streak_auto.py` | Автоматизація Deposit Streak тесту (**BackOffice UI API**, `Bearer` токен) |
| `04_get_player_info.py` | Отримання інформації про гравця |
| `05_create_bonus.py` | Створення тестового бонусу |
| `07_test_data_orchestrator.py` | Оркестратор сценаріїв |

### Сценарії оркестратора

- `player_with_balance` — Гравець з балансом
- `player_with_bonus` — Гравець з бонусом
- `deposit_streak` — Гравець з 3 депозитами
- `high_roller` — Гравець з великим балансом ($1000)
- `full_setup` — Повне налаштування (balance + deposit + bonus)

### Швидке використання

```bash
cd /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/test-data-scripts

# Створити гравця з балансом
python3 scripts/01_create_test_player.py --env qa --balance 100

# Додати баланс
python3 scripts/02_set_test_player_balance.py 123456 --amount 50 --env qa

# Виконати сценарій
python3 scripts/07_test_data_orchestrator.py --scenario player_with_balance --env qa
```

### API Клієнти

- **WebsiteApiClient** — `https://websitewebapi.{env}.sofon.one`
- **AdminWebApiClient** — `https://adminwebapi.{env}.sofon.one` (`UserId` auth)
- **BackOfficeUiApiClient** — `https://backoffice.{env}.sofon.one/mgw/admin/` (`Bearer` токен)
- **WalletApiClient** — `https://wallet.{env}.sofon.one`
- **GraphQLClient** — `https://minebit-casino.{env}.sofon.one/graphql`

**Примітка:** Для депозитів, що тригерять бонуси, використовуйте **BackOfficeUiApiClient** (Bearer токен). AdminWebApiClient не повертає `PaymentRequestId` для `MarkAsPaid`.

### Важливі правила

1. **Безпека:** Всі скрипти автоматично встановлюють `IsTest = true`
2. **Wallet API логіка:** `create_debit_correction` → додає гроші ✅
3. **Deposit flow:** Створити депозит → MarkAsPaid (обов'язково!)
4. **Prod:** Вимагає підтвердження для всіх дій
5. **Бонуси:** Wallet corrections **не тригерять** бонуси Deposit Streak. Для тестування бонусів використовуйте BackOffice UI API (`Bearer` токен) з повним флоу (`MakeManualRedirectPayment` → `MarkAsPaid`).

### Інтеграція з Playwright

Скрипти можна використовувати як модулі у Playwright fixtures:

```python
from create_test_player import create_test_player

@pytest.fixture
def test_player():
    return create_test_player(env="qa", setup_balance=True)
```

**Детальна документація:** `test-data-scripts/README.md`

---

## ⚠️ Проблема сегментації гравців (критично для тестування бонусів)

**Відкрито:** 2026-03-03

**Проблема:** Гравці з тестовими email потрапляють у тестові сегменти, які можуть блокувати бонуси Deposit Streak.

**Тестові сегменти (виявлено користувачем):**
- `Segments Static: Icon-edit Dynamic: BP-bonusId-1222-WhenToHide-05/09/2025`
- `All users Test OQ`
- `BP-bonusId-1525-WhenToHide-05/09/2025`
- `BP-bonusId-1223-WhenToHide-05/09/2025`
- `BP-bonusId-1224-WhenToHide-05/09/2025`
- `Smartico Segments: Pawn Pioneer`
- `Complex Segments: Active_user, Multiaccount`

### Блокуючі сегменти (Minebit)
**Джерело:** Повідомлення від проджект менеджера Danylo (бренд Minebit), 2026-03-04.

Вадим (з команди Minebit) встановлює наступні 4 сегменти як тригери для активації бонусів. Якщо гравець має хоча б один із цих сегментів, активація будь-яких бонусів для нього **блокована**.

| Сегмент | Тип | Призначення |
|---------|-----|-------------|
| Multiaccount | Комплексний | Автоматично присвоюється системою |
| Bonus Hunter | Статичний | Виставляється вручну |
| Mult | Статичний | Виставляється вручну |
| Fraud_reg_pass | Комплексний | Автоматично присвоюється системою |

**Сегмент MULTI_BONUS_ALLOWED** — повертає можливість отримувати бонуси (якщо гравець раніше потрапив у блокуючі сегменти). Оновлюється автоматично через час; для термінового оновлення потрібно звернутися до Danylo.

**Сегменти, які НЕ присвоюються автоматично** (не блокують бонуси): ВІП, ПреВІП, Потенційний ВІП.

*Ця інформація критична для створення користувачів на PROD, щоб бонуси працювали правильно.*

### 🛠️ Рішення: менш тестові дані

1. **Оновлено `generate_test_data.py`**:
   - Email: `demo1772565196491@nextcode.tech` (замість `test-...`)
   - Username: `demo1772565196719` (замість `user...`)
   - Пароль: `Qweasd123!` (без змін)

2. **Новий гравець 1179951** (створено 2026-03-03):
   - Email: `demo1772565196491@nextcode.tech`
   - Client ID: 1179951
   - Session token: `ef6140930984437293552d19fae1106f`
   - **Не позначений як тестовий** (помилка 400 при спробі встановити `IsTest = true`)
   - Можливо, уникає тестових сегментів

### ⚠️ Поточна блокуюча проблема: Bearer токен протух
- Bearer токен для BackOffice UI API має термін дії ~3 години
- Поточний токен (дійсний до 22:46 UTC 2026-03-03) повертає **401 Unauthorized**
- Без нового Bearer токена неможливо створювати депозити через BackOffice UI API

### 📋 Висновки для тестування Deposit Streak:
1. **Використовуйте гравців з "demo" email** замість "test-" щоб уникнути тестової сегментації
2. **Bearer токен потребує оновлення** кожні ~3 години (отримувати через логін BackOffice)
3. **Перевіряйте сегментацію гравця** перед тестуванням бонусів
4. **Wallet corrections не тригерять бонуси** — використовуйте лише BackOffice UI API з повним флоу (`MakeManualRedirectPayment` → `MarkAsPaid`)

---

## 🔍 Результати повного тестування Deposit Streak (2026-03-03)

### Автоматизований флоу працює ідеально
**Скрипт:** `deposit_streak_auto.py` (розташування: `projects/nextcode/test-data-scripts/scripts/`)

**Флоу:**
1. `POST /mgw/admin/api/Client/MakeManualRedirectPayment` (Bearer токен)
2. `POST /mgw/admin/api/v2/Payment/GetAllWithTotal` (пошук за `clientId`)
3. `PATCH /mgw/admin/api/v2/Payment/ChangeStatus` (`MarkAsPaid`)

**Результат:** 10/10 депозитів успішно створено та позначено як оплачені. Технічно флоу працює бездоганно.

### Бонуси не з'являються навіть після успішних депозитів
**Тестовий гравець:** 1179951 (demo1772565196491@nextcode.tech)
- **10 депозитів по $30 кожен:** усі успішні
- **Очікувані бонуси:** 4 (після депозитів 2, 4, 8, 10)
- **Фактичні бонуси:** 0 (жодного бонусу не з'явилося)

### Можливі причини відсутності бонусів
1. **Сегментація:** Гравець все ще може потрапляти в тестові сегменти
2. **Кампанія неактивна:** Deposit Streak може бути неактивований на PROD для нових гравців
3. **Payment method 19:** Тестовий метод може не тригерити бонуси навіть після `MarkAsPaid`
4. **Конфігурація бонусу:** Додаткові критерії (мінімальна сума, інтервал тощо)

### Критичні відкриття
1. **Гравець не позначений як тестовий:** При спробі встановити `IsTest = true` для гравця 1179951 отримано помилку 400. Це може бути **добре** — гравець не потрапляє в тестові сегменти.
2. **Bearer токен має обмежений термін дії:** ~3 години, потрібно оновлювати через логін BackOffice.
3. **Технічна автоматизація готова:** Скрипт `deposit_streak_auto.py` може використовуватися для майбутніх тестувань після вирішення проблеми з бонусами.

### Наступні кроки
1. **Ручна перевірка бонусів** для гравця 1179951 через UI
2. **Перевірка сегментації** через BackOffice
3. **Перевірка активності кампанії Deposit Streak** на PROD
4. **Пошук реального payment method** для USD (не тестового)

### Запропоновані тест-кейси для TestRail
Підготовлено 10 детальних тест-кейсів, що охоплюють:
- Основний флоу (2 депозити → бонус → клейм)
- Регресивний тест (10 депозитів)
- Негативні тести (Wallet corrections, тестові сегменти)
- UI validation, API validation, edge cases

**Критичні моменти для тестування:**
- Авторизація: BackOffice UI API vs AdminWeb API
- Сегментація гравців
- Payment method вплив на тригер бонусів
- Wallet corrections не тригерять бонуси

---

## QA Testing Learnings - Minebit (2026‑03‑04)

### 🧪 CT‑824 Realtime Rakeback – Comprehensive Test Analysis

**Context:** Full smoke‑test and E2E test case design for new Realtime Rakeback feature (epic CRYPTO‑463).

**What We Tested:**
1. **Player creation & deposit** via BackOffice API (Bearer token flow).
2. **Real‑money wager** ($100) in game `trade‑smarter‑1000x`.
3. **30‑minute accrual wait** (cron `*/30 * * * *`).
4. **Bonus appearance** on `/bonuses` page.
5. **Claim flow** and balance verification.
6. **House Edge calculation** validation.

**Key Discoveries:**
1. **Formula works correctly** – `Rakeback = wager × 0.0025 (0.25% house edge) × 0.1 (10% coefficient)`.
2. **House Edge configuration error** – Game `trade‑smarter‑1000x` uses 0.278% instead of required 0.25%.
3. **Funds go to real balance** (Unused balance) – consistent with Regular Bonuses (BonusTypeId: 11).
4. **No Active Bonuses entry** – claimed amounts credited directly to balance (no wagering).
5. **Smartico involvement** (IsSmartico: true) – calculation may have slight delays.
6. **Bearer token expiration** – BackOffice UI API token lasts ~3 hours, requires login refresh.

**Critical Testing Patterns Established:**
- **API‑first setup** – Create player/deposit via API (minutes) before UI testing.
- **Burger Methodology** – Structured test design: Memory Check → Feature Container → Testing Types → Techniques → Risk‑Based Approach → Scenarios.
- **TestRail integration** – Automated case addition via Python script (`testrail_add_realtime_rakeback.py`).
- **E2E test case structure** – Clear preconditions, steps, expected results, prioritization.

**Scripts & Tools Developed:**
1. `testrail_add_realtime_rakeback.py` – Add 5 E2E cases to TestRail (Section ID 7091).
2. `deposit_streak_auto.py` – Automated deposit flow with Bearer token (usable for rakeback).
3. **Player creation pattern** – GraphQL registration + BackOffice deposit + MarkAsPaid.

**Lessons for Future Minebit Testing:**
- **Always verify House Edge per game category** – Configuration can differ and cause financial discrepancies.
- **Bearer token management** – Refresh before automated test suites.
- **Test player segmentation** – Avoid `demo*`/`test*` emails to prevent test‑segment exclusion.
- **30‑minute wait problem** – Need test‑only cron (1‑5 min) or mock API endpoint for CI.
- **BackOffice UI API vs AdminWeb API** – Use UI API (`Bearer` token) for deposits that trigger bonuses (returns `PaymentRequestId`).
- **Wallet corrections don't trigger bonuses** – Only proper deposit flow (`MakeManualRedirectPayment` → `MarkAsPaid`) works.

**Test Coverage Created:**
- 5 E2E test cases in TestRail (IDs 30630‑30634).
- Burger‑based test scenarios for House Edge, VIP split, timers, negative cases.
- API validation steps for balance, bonus eligibility, accrual timing.

**Next Time Similar Task:**
1. Ask developer about test‑only cron interval or mock endpoint.
2. Verify House Edge configuration for target game before testing.
3. Use fresh Bearer token (login via BackOffice).
4. Create player with non‑test email pattern.
5. Run basic happy‑path, then expand to edge cases.

---

## Daily Standup Monitoring

**Правило:** Щодня перевіряти транскрипти дейлі-мітингів за сьогодні та попередні два дні. Вилучати ключову інформацію щодо готовності тікетів до тестування або нюансів у тестуванні. Зберігати цю інформацію для майбутнього дизайну тест-кейсів або тестування тікетів.

**Процес:**
1. **Отримання транскрипту:** Користувач надає транскрипт дейлі (текст).
2. **Аналіз:** Визначити ключові теми, статуси тікетів, проблеми, плани.
3. **Збереження:**
   - Зберегти самарі у файл `projects/nextcode/meeting-notes/YYYY-MM-DD-daily-summary.md`
   - Опублікувати самарі у Slack канал `#general`
   - Оновити MEMORY.md з важливою довгостроковою інформацією (наприклад, блокуючі проблеми, зміни в процесах)
4. **Оновлення статусів тікетів:** Витягнути інформацію про тікети, які будуть готові до тестування, та додати їх до списку моніторингу.

**Важливі елементи для вилучення:**
- Тікети, які розробники закінчили або готові до тестування
- Проблеми, що виникають під час тестування (наприклад, сегментація гравців, конфігурація бонусів)
- Плани на спринт (хто що робить, оцінки)
- Технічні нюанси (наприклад, Bearer токен протухає через 3 години)

**Частота:** Щодня (під час робочих годин) або при отриманні транскрипту.

**Посилання:**
- Папка з щоденними нотатками: `projects/nextcode/meeting-notes/`
- Slack канал: `#general` (C0AHRLH1Y3S)

---

## CT-622 Metamask FE Integration (Crypto Wallet Auth)

**Status:** Testing (as of 2026-03-04)
**Assignee:** Panda Sensei (Ihor)
**Blockers:** CRYPTO-485 (BE) in Development, PR‑2870 (Tested)
**Depends:** CT‑621 (Ready for Release)

**Description:** Add Metamask as registration & login method on desktop + mobile. Frontend SDK (wagmi+viem or ethers), UI button in Strapi, conditional popup for missing extension, loader during auth, follow BC Games flow.

**Key Requirements:**
- Desktop with extension installed → click opens extension
- Desktop without extension → popup with download link / QR code for mobile
- Mobile with app installed → prompt to open app
- Loader on button during auth process
- Integration with BE API (SIWE flow)

**Testing Results (2026-03-04):**
- ✅ **Desktop + extension:** Works – click opens extension, sign message, successful login, loader shows
- ❌ **Desktop − extension:** Errors – popup appears with download link & QR code, but backend API calls fail:
  - GET 502 (Bad Gateway)
  - GET 500 (Internal Server Error)  
  - POST 500 (Internal Server Error)
  - TypeError: Cannot read properties of null (reading '0')
- **Error context:** Zone.js Angular errors in `XMLHttpRequest.addEventListener:load getClient@ ngOnInit@`

**Root Cause Hypothesis:** Backend endpoints for Metamask auth (SIWE flow) not fully deployed to DEV yet (CRYPTO‑485 still in Development). Frontend calls failing due to missing/unavailable API routes.

**Next Steps:**
1. Confirm CRYPTO‑485 deployment status
2. Inspect network requests to identify failing endpoints
3. Verify CORS configuration
4. Check backend logs for 502/500 errors
5. Mark CT‑622 as **Blocked by CRYPTO‑485** until BE endpoints return 200

**Test Coverage Needed:**
- Extension detection logic
- Popup UI & QR code generation
- Mobile deep‑link flow
- Error handling for missing backend
- Cross‑browser compatibility (Chrome, Firefox, Safari)
- Security validation (SIWE signature, nonce, replay attack prevention)

**Burger Methodology Analysis:** Completed – see Slack thread for full structured test design.

**BackOffice User Details Issue (2026‑03‑04):**
- **Problem:** After successful Metamask registration, tester cannot view user details in BackOffice UI – receives an error.
- **Possible causes:** Missing fields for crypto‑wallet users (email, phone), UI not handling new registration type, expired Bearer token, backend API issue.
- **Diagnostic steps:** Check API endpoint `GetClientById` via AdminWeb API (UserId auth) and BackOffice UI API (Bearer token). Compare response structure with traditional email‑registered users.
- **Status:** Awaiting details (error message, client ID) from tester.

**Password/Email & Segmentation Questions (2026‑03‑04):**
- **Tester questions:** Can Metamask‑registered users set password? Add email? Will segmentation work?
- **Analysis from ticket:** No explicit requirements for password/email in CT‑622; SIWE auth uses wallet address identification.
- **Likely behavior:** Crypto‑wallet users may have **no password/email** in current implementation; segmentation based on email may not work.
- **Segmentation alternatives:** May need to use wallet address or registration type for segmentation.
- **Testing focus:** Primary goal is Metamask auth flow (extension, popup, mobile deep‑link). Password/email/segmentation may be out of scope for this ticket.
- **Next steps:** Check personal cabinet for email/password addition; fetch user data via API; consult tech research doc or developer for clarification.

**API Analysis for Client 59153 (2026‑03‑04):**
- **Client ID:** 59153 (Metamask‑registered user on DEV)
- **Session token:** `ed31ecae754546bfb0707565fb2f03f2` (provided by tester)
- **Findings:**
  1. AdminWeb API → 404 Not Found (endpoint may be wrong or user doesn't exist in AdminWeb system).
  2. Wallet API → 503 Service Temporarily Unavailable (Wallet service on DEV appears down).
  3. BackOffice API via script → `'NoneType' object has no attribute 'get'` (likely expired Bearer token or authentication issue).
  4. Website API → 401 Unauthorized (session token not valid for this endpoint).
  5. GraphQL → `Cannot return null for non‑nullable field Query.player` (user not found with given parameters).
- **Observations:** DEV environment has API availability issues. Session token works for site authentication but not for all API endpoints.
- **Recommendation:** Tester should check **WebsiteWeb API Swagger (DEV)** → endpoint `GET /api/v3/Client/GetClientById` with `id=59153` and appropriate headers to see if email/phone fields are present.

**TestRail E2E Test Cases for CT‑622 (2026‑03‑04):**
- **Status:** ✅ Added 12 test cases via script `testrail_add_metamask_integration.py`
- **Section:** "Metamask Integration" (ID 7213) under "Authentication" (ID 6839)
- **TestRail URL:** https://nexttcode.testrail.io/index.php?/suites/view/631&group_by=cases:section_id&group_id=7213
- **Cases:** Desktop+extension, Desktop−extension, Mobile+app, Mobile−app, Signature rejection, Multiple accounts, Network switching, Session persistence, Cross‑browser, Responsive UI, Loader states, BE integration
- **Security test case:** Not added due to priority_id error (low priority)
- **Next:** Tester can execute tests; mark CT‑622 as Blocked by CRYPTO‑485 for missing‑extension flow
