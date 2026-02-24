# BackOffice API v1 - Swagger Analysis

**Base URL (Prod):** `https://adminwebapi.prod.sofon.one`

**Swagger:** `https://adminwebapi.prod.sofon.one/swagger/index.html`

**Auth:** Header `UserId: <adminUserId>`
- Prod: `UserId: 560`
- QA/Dev: `UserId: 1`

---

## 📊 Overview

- **Total Endpoints:** 368
- **Groups:** 35
- **Auth Method:** Header `UserId`

---

## 📁 Key Endpoint Groups for QA

### 1. Client (55 endpoints) 👤
**Purpose:** Player management, balance operations

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/Client/GetClients` | Search players |
| POST | `/api/Client/GetClientById` | Get player details |
| POST | `/api/Client/CreateCreditCorrection` | **Add balance (credit)** |
| POST | `/api/Client/CreateDebitCorrection` | **Remove balance (debit)** |
| POST | `/api/Client/GetClientCorrections` | Balance change history |
| POST | `/api/Client/ChangeClientDetails` | Update player info |
| POST | `/api/Client/ChangeClientPassword` | Change password |
| POST | `/api/Client/DeactivateClients` | Deactivate player |
| POST | `/api/Client/ActivateClientPromocode` | Activate promo code |
| POST | `/api/Client/CancelClientBonus` | Cancel player bonus |
| POST | `/api/Client/ExportClients` | Export players list |

---

### 2. Bonus (27 endpoints) 🎁
**Purpose:** Bonus management

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/Bonus/GetBonuses` | Get bonuses list |
| POST | `/api/Bonus/GetBonusById` | Get bonus details |
| POST | `/api/Bonus/CreateBonus` | **Create new bonus** |
| PUT | `/api/Bonus/AddTriggerToBonus` | Add trigger to bonus |
| POST | `/api/Bonus/CloneBonus` | Clone bonus |
| POST | `/api/Bonus/BulkUpdateBonuses` | Bulk update bonuses |
| POST | `/api/Bonus/ClaimBonusForClients` | Claim bonus for player |
| POST | `/api/Bonus/GetBonusInfo` | Get bonus info |

---

### 3. Product (30 endpoints) 🎮
**Purpose:** Game management

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/Product/GetGameProviders/{partnerId}` | Get game providers |
| POST | `/api/Product/AddProduct/{partnerId}` | Add game |
| POST | `/api/Product/EditProduct/{partnerId}` | Edit game |
| POST | `/api/Product/ChangePartnerProductState` | Enable/disable game |
| POST | `/api/Product/GetCategoriesProductsOrder/{partnerId}` | Get game categories |

---

### 4. Partner (23 endpoints) 🏢
**Purpose:** Brand/partner management

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/Partner/GetPartners` | Get partners list |
| POST | `/api/Partner/CreatePartner` | Create partner |
| GET | `/api/Partner/GetPartnerProperties/partnerId` | Get partner settings |
| POST | `/api/Partner/GetPartnerKeys` | Get partner API keys |

---

### 5. Report (43 endpoints) 📊
**Purpose:** Reports and analytics

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/Report/GetReportByCorrections` | Balance corrections report |
| POST | `/api/Report/GetSummaryCorrectionChargebackReport` | Chargeback report |
| POST | `/api/Report/GetSummaryCorrectionRefundReport` | Refund report |

---

## 🔧 Key Schemas for QA

### ClientCorrectionInput (Credit/Debit)
```json
{
  "amount": 100.00,
  "accountId": 12345,
  "accountTypeId": 1,
  "currencyId": "USD",
  "clientId": 1147217,
  "info": "Test balance correction for CT-728",
  "productId": null,
  "bonusTurnoverAmount": 0,
  "unusedTurnoverAmount": 0
}
```

| Field | Type | Description |
|-------|------|-------------|
| `amount` | number | Amount to credit/debit |
| `clientId` | integer | Player ID |
| `currencyId` | string | Currency code (USD, EUR, etc.) |
| `accountId` | integer | Account ID (from GetClientAccounts) |
| `accountTypeId` | enum | Account type (1=Real, 2=Bonus, etc.) |
| `info` | string | Comment/reason |

---

### ApiFilterBonus (Search Bonuses)
```json
{
  "partnerId": 5,
  "takeCount": 50,
  "skipCount": 0,
  "isActive": true,
  "type": 1
}
```

---

## 🧪 Test Flow Examples

### 1. Search Player
```bash
curl -X POST "https://adminwebapi.prod.sofon.one/api/Client/GetClients" \
  -H "UserId: 560" \
  -H "Content-Type: application/json" \
  -d '{
    "takeCount": 10,
    "skipCount": 0,
    "email": "test-CT728@nextcode.tech"
  }'
```

### 2. Credit Balance (Add Money)
```bash
curl -X POST "https://adminwebapi.prod.sofon.one/api/Client/CreateCreditCorrection" \
  -H "UserId: 560" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00,
    "clientId": 1147217,
    "currencyId": "USD",
    "accountId": 12345,
    "accountTypeId": 1,
    "info": "Test deposit for CT-728"
  }'
```

### 3. Debit Balance (Remove Money)
```bash
curl -X POST "https://adminwebapi.prod.sofon.one/api/Client/CreateDebitCorrection" \
  -H "UserId: 560" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "clientId": 1147217,
    "currencyId": "USD",
    "accountId": 12345,
    "accountTypeId": 1,
    "info": "Test withdrawal for CT-728"
  }'
```

### 4. Get Bonuses List
```bash
curl -X POST "https://adminwebapi.prod.sofon.one/api/Bonus/GetBonuses" \
  -H "UserId: 560" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerId": 5,
    "takeCount": 50,
    "skipCount": 0,
    "isActive": true
  }'
```

### 5. Get Bonus Details
```bash
curl -X POST "https://adminwebapi.prod.sofon.one/api/Bonus/GetBonusById" \
  -H "UserId: 560" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123
  }'
```

---

## 📋 Environment Reference

| Env | Base URL | UserId |
|-----|----------|--------|
| Prod | `https://adminwebapi.prod.sofon.one` | 560 |
| QA | `https://adminwebapi.qa.sofon.one` | 1 |
| Dev | `https://adminwebapi.dev.sofon.one` | 1 |

---

## 📁 Files

- **Swagger JSON:** `/Users/ihorsolopii/.openclaw/workspace/swagger_backoffice_prod_v1.json` (1.3MB)
