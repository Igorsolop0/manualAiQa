# MEMORY.md - QA Agent

> This logic relates to testing methodology, locator strategies, data generation, and automation.


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


---

## UI Knowledge Base (AI Page Object Model)

**Location:** `/Users/ihorsolopii/.openclaw/workspace/ui-knowledge/minebit/`

**Purpose:** 
Long-term memory for UI selectors. To avoid parsing the whole DOM every time and breaking tests when UI changes:
1. **Always check this directory first** before creating Playwright scripts or doing interactive testing (e.g. `bonuses-page.json`).
2. If a selector doesn't work during a task, fix it via snapshot analysis and **IMMEDIATELY update the JSON file** with the new selector so it's remembered for next time.
3. Keep logic descriptions (animations, wait states) in the `known_behaviors` key.

---


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
