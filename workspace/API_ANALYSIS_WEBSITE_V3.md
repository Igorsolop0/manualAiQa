# Website API v3 - Swagger Analysis

**Base URL (Prod):** `https://websitewebapi.prod.sofon.one`

**Swagger:** `https://websitewebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3`

---

## 📊 Overview

- **Total Endpoints:** 125
- **Groups:** 19
- **Auth Method:** `token` (sessionToken) in request body

---

## 🔑 Authentication

**Token Location:** Request body field `token`

**Base Request Structure:**
```json
{
  "partnerId": 5,
  "languageId": "en",
  "timeZone": -60,
  "countryCode": "AT",
  "domain": "https://minebit-casino.prod.sofon.one",
  "method": "...",
  "token": "<sessionToken>",
  "productId": null,
  "requestData": { ... }
}
```

**Key Headers (from GraphQL registration):**
- `website-locale: en`
- `website-origin: https://minebit-casino.prod.sofon.one`
- `x-time-zone-offset: -60`

---

## 📁 Endpoint Groups

### 1. Client (38 endpoints) 👤
**Purpose:** User management, authentication, profile

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Client/Register` | New user registration | ❌ |
| POST | `/{partnerId}/api/v3/Client/Login` | User login | ❌ |
| GET | `/{partnerId}/api/v3/Client/GetClientByToken` | Get user by token | ✅ |
| GET/POST | `/{partnerId}/api/v3/Client/GetClientBalance` | Get balance | ✅ |
| POST | `/{partnerId}/api/v3/Client/ChangeDetails` | Update profile | ✅ |
| POST | `/{partnerId}/api/v3/Client/LogoutClient` | Logout | ✅ |
| POST | `/{partnerId}/api/v3/Client/ChangeClientPassword` | Change password | ✅ |
| POST | `/{partnerId}/api/v3/Client/SendRecoveryToken` | Password reset email | ❌ |
| POST | `/{partnerId}/api/v3/Client/RecoverPassword` | Reset password | ❌ |
| GET | `/{partnerId}/api/v3/Client/ClientEmailExists` | Check email exists | ❌ |
| GET | `/{partnerId}/api/v3/Client/ClientUserNameExists` | Check username exists | ❌ |
| POST | `/{partnerId}/api/v3/Client/GetClientAccounts` | Get user accounts | ✅ |
| POST | `/{partnerId}/api/v3/Client/GetClientLimits` | Get user limits | ✅ |
| POST | `/{partnerId}/api/v3/Client/GetClientLogins` | Get login history | ✅ |

---

### 2. Product (20 endpoints) 🎮
**Purpose:** Games, game launch, winners, jackpots

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Product/GetProductUrl` | Get game launch URL | ✅ |
| POST | `/{partnerId}/api/v3/Product/CheckProductAvailability` | Check game available | ✅ |
| GET/POST | `/{partnerId}/api/v3/Product/GetWinners` | Recent winners | ❌ |
| GET/POST | `/{partnerId}/api/v3/Product/GetRecentBets` | Recent bets | ❌ |
| GET/POST | `/{partnerId}/api/v3/Product/GetJackpotGameData` | Jackpot info | ❌ |
| POST | `/{partnerId}/api/v3/Product/GetProductTypesEnum` | Game types list | ❌ |

---

### 3. Bonus (16 endpoints) 🎁
**Purpose:** Bonuses, promotions, promo codes

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Bonus/GetPromotions` | Get promotions list | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/GetBonuses` | Get available bonuses | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/GetActiveBonuses` | Get active bonuses | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/GetEligibleBonuses` | Get eligible bonuses | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/ActivatePromoCode` | Activate promo code | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/SaveSelectedDepositBonus` | Select deposit bonus | ✅ |
| POST | `/{partnerId}/api/v3/Bonus/CancelSelectedDepositBonus` | Cancel selected bonus | ✅ |
| GET | `/{partnerId}/api/v3/Bonus/GetAvailableDepositBonuses` | Available deposit bonuses | ✅ |

---

### 4. Payment (6 endpoints) 💳
**Purpose:** Deposits, withdrawals, payment methods

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/{partnerId}/api/v3/Payment/GetAvailablePaymentMethods` | Payment methods | ✅ |
| GET | `/{partnerId}/api/v3/Payment/GetPaymentRequests` | Transaction history | ✅ |
| DELETE | `/{partnerId}/api/v3/Payment/CancelWithdraw` | Cancel withdrawal | ✅ |
| GET | `/{partnerId}/api/v3/Payment/GetClientPaymentStatistics` | Payment stats | ✅ |

---

### 5. Bet (2 endpoints) 🎲
**Purpose:** Bet history

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Bet/GetCasinoBets` | Casino bet history | ✅ |
| POST | `/{partnerId}/api/v3/Bet/GetSportBookBets` | Sports bet history | ✅ |

---

### 6. TwoFactorAuth (7 endpoints) 🔐
**Purpose:** 2FA setup and management

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/2fa/setup` | Setup 2FA | ✅ |
| POST | `/{partnerId}/api/v3/2fa/enable` | Enable 2FA | ✅ |
| DELETE | `/{partnerId}/api/v3/2fa/disable` | Disable 2FA | ✅ |
| GET | `/{partnerId}/api/v3/2fa/status` | 2FA status | ✅ |
| POST | `/{partnerId}/api/v3/2fa/verify` | Verify 2FA code | ✅ |

---

### 7. Main (13 endpoints) ℹ️
**Purpose:** Enums, reference data, utilities

**Key Endpoints:**
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Main/GetRegions` | Regions list | ❌ |
| POST | `/{partnerId}/api/v3/Main/GetReferralLink` | Referral link | ✅ |
| POST | `/{partnerId}/api/v3/Main/InviteFriend` | Invite friend | ✅ |
| GET | `/{partnerId}/api/v3/Main/GetBetStates` | Bet states enum | ❌ |

---

### 8. CalendarBonus (2 endpoints) 📅
**Purpose:** Daily/weekly calendar bonuses

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/{partnerId}/api/v3/CalendarBonus/GetByClient/{clientId}` | Calendar bonuses | ✅ |
| POST | `/{partnerId}/api/v3/CalendarBonus/Claim` | Claim calendar bonus | ✅ |

---

### 9. DepositStreak (1 endpoint) 🔥
**Purpose:** Deposit streak bonus

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/{partnerId}/api/v3/DepositStreak/GetDepositStreak` | Get deposit streak | ✅ |

---

### 10. PaymentHub (1 endpoint) 🏦
**Purpose:** Payment initialization

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/PaymentHub/Initialize` | Initialize payment | ✅ |

---

### 11. DirectPayment (2 endpoints) 💰
**Purpose:** Direct withdrawals

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/DirectPayment/CreateWithdrawByCreditCardNumber` | Withdraw to card | ✅ |
| POST | `/{partnerId}/api/v3/DirectPayment/CreateWithdrawByAccountNumber` | Withdraw to account | ✅ |

---

### 12. RedirectPayment (1 endpoint) 🔗
**Purpose:** Redirect deposits

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/RedirectPayment/CreateDepositByRedirect` | Redirect deposit | ✅ |

---

### 13. Recommendation (1 endpoint) 🎯
**Purpose:** Game recommendations

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Recommendation/GetGameRecommendation` | Game recommendations | ✅ |

---

### 14. Auth (2 endpoints) 📱
**Purpose:** OTP authentication

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/{partnerId}/api/v3/Auth/otp/request` | Request OTP | ❌ |
| POST | `/{partnerId}/api/v3/Auth/otp/verify` | Verify OTP | ❌ |

---

### 15. GoogleAccount (3 endpoints) 🔑
**Purpose:** Google OAuth

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/v3/GoogleAccount/GetAuthUrl` | Get Google OAuth URL | ❌ |
| GET | `/api/v3/GoogleAccount/Callback` | OAuth callback | ❌ |
| POST | `/api/v3/GoogleAccount/OneTapAuth` | One-tap auth | ❌ |

---

### 16. TelegramAccount (1 endpoint) ✈️
**Purpose:** Telegram auth

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/v3/TelegramAccount/HashAuth` | Telegram auth | ❌ |

---

### 17. VkAccount (2 endpoints) 🇷🇺
**Purpose:** VK OAuth

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/v3/VkAccount/GetAuthUrl` | Get VK OAuth URL | ❌ |
| GET | `/api/v3/VkAccount/Callback` | OAuth callback | ❌ |

---

### 18. Chatwoot (1 endpoint) 💬
**Purpose:** Chat support integration

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/v3/Chatwoot/GetHmac` | Get Chatwoot HMAC | ✅ |

---

### 19. Version (6 endpoints) 📌
**Purpose:** Health check, version info

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/build` | Build info | ❌ |
| GET | `/ping` | Ping | ❌ |

---

## 🔐 Auth Summary

**Public (no token required):**
- Client: Register, Login, SendRecoveryToken, RecoverPassword, ClientEmailExists, ClientUserNameExists
- Main: GetRegions, GetBetStates, all enums
- Product: GetWinners, GetRecentBets, GetJackpotGameData (public game info)
- Auth: OTP request/verify
- Google/Telegram/Vk: OAuth endpoints
- Version: build, ping

**Authenticated (token required):**
- Client: GetClientByToken, GetClientBalance, ChangeDetails, Logout, etc.
- Product: GetProductUrl (game launch)
- Bonus: All bonus endpoints
- Payment: All payment endpoints
- Bet: All bet history
- 2FA: All 2FA endpoints
- CalendarBonus, DepositStreak, etc.

---

## 🧪 Test Flow Examples

### 1. Registration + Login (GraphQL)
```bash
# Register via GraphQL
curl 'https://minebit-casino.prod.sofon.one/graphql' \
  -H 'content-type: application/json' \
  -H 'website-locale: en' \
  -H 'website-origin: https://minebit-casino.prod.sofon.one' \
  -H 'x-time-zone-offset: -60' \
  --data-raw '{
    "operationName": "PlayerRegisterUniversal",
    "variables": {
      "input": {
        "email": "test-CT728-1708012345@nextcode.tech",
        "password": "Qweasd123!",
        "currency": "USD",
        "promoCode": null,
        "termsConditionsAccepted": true,
        "affiliateData": "https://minebit-casino.prod.sofon.one/lobby-ct-728"
      },
      "bmsPartnerId": 5,
      "locale": "en",
      "deviceFingerPrint": "0606669b5eb21bbef203d7b1103343a7"
    },
    "query": "mutation PlayerRegisterUniversal(...) { ... }"
  }'

# Response contains sessionToken
```

### 2. Get Balance (authenticated)
```bash
curl -X GET "https://websitewebapi.prod.sofon.one/5/api/v3/Client/GetClientBalance?token=YOUR_SESSION_TOKEN" \
  -H 'website-locale: en' \
  -H 'website-origin: https://minebit-casino.prod.sofon.one'
```

### 3. Get Available Bonuses
```bash
curl -X POST "https://websitewebapi.prod.sofon.one/5/api/v3/Bonus/GetBonuses" \
  -H 'Content-Type: application/json' \
  --data '{
    "partnerId": 5,
    "languageId": "en",
    "timeZone": -60,
    "domain": "https://minebit-casino.prod.sofon.one",
    "token": "YOUR_SESSION_TOKEN"
  }'
```

### 4. Get Game Launch URL
```bash
curl -X POST "https://websitewebapi.prod.sofon.one/5/api/v3/Product/GetProductUrl" \
  -H 'Content-Type: application/json' \
  --data '{
    "partnerId": 5,
    "languageId": "en",
    "timeZone": -60,
    "domain": "https://minebit-casino.prod.sofon.one",
    "token": "YOUR_SESSION_TOKEN",
    "position": "main",
    "isForDemo": false,
    "isForMobile": false
  }'
```

---

## 📋 Key Fields for QA

| Field | Description | Example |
|-------|-------------|---------|
| `partnerId` | Brand ID (path param) | 5 (Minebit) |
| `token` | Session token from GraphQL | `606d62e2e6114e86adf8aeff8e95b58e` |
| `languageId` | Locale code | `en`, `de`, `uk` |
| `timeZone` | Timezone offset | `-60` (CET) |
| `domain` | Website origin | `https://minebit-casino.prod.sofon.one` |
| `countryCode` | ISO country code | `AT`, `DE`, `UA` |

---

## 📁 Files

- **Swagger JSON:** `/Users/ihorsolopii/.openclaw/workspace/swagger_website_prod_v3.json`
