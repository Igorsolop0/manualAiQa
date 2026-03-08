# MEMORY.md - API Docs Agent

> This logic details endpoint mappings, Swagger references, and specific BackOffice/Website/Wallet flows.


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
