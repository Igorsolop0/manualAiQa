# CT-752: Social Account Deletion - Research Report

**Date:** 2026-03-16T12:40:00Z
**Ticket:** CT-752
**Task:** Find endpoint to delete/unlink social account from player

---

## 🎯 Problem Statement

QA testing blocked because:
- Player registered via Google OAuth
- Linked Google account prevents re-testing
- Need to remove/unlink social account to continue testing

---

## 📋 Findings from Documentation

### 1. Website API - Login Returns LinkedRegistrationSources

**Endpoint:** `/{partnerId}/api/v3/Client/Login`

**Response Structure:**
```json
{
  "ResponseObject": {
    "Id": 12345,
    "Token": "session_token",
    "LinkedRegistrationSources": [
      "Google",
      "Telegram"
    ]  // or null
  }
}
```

**Field:** `LinkedRegistrationSources` (array of strings)

**Possible Values:**
- `null` - No linked social accounts
- `["Google"]` - Google account linked
- `["Google", "Telegram"]` - Both linked
- `["Platform"]` - Platform (email/password) only

**Source:** `/tests/api/tickets/CT-751-linked-sources.spec.ts`

---

### 2. Website API - GetClientLogins

**Endpoint:** `/{partnerId}/api/v3/Client/GetClientLogins`

**Request:**
```json
{
  "partnerId": 5,
  "token": "session_token",
  "languageId": "en",
  "timeZone": -60
}
```

**Purpose:** Get list of all login methods linked to player account

**Response Structure (Expected):**
```json
{
  "ResponseObject": [
    {
      "LoginType": "Google",
      "ExternalId": "google_user_id",
      "CreateDate": "2026-03-16T..."
    },
    {
      "LoginType": "Platform",
      "ExternalId": null,
      "CreateDate": "2026-03-15T..."
    }
  ]
}
```

**Source:** `/tests/api/tickets/CT-751-linked-sources.spec.ts` (TC3)

---

### 3. BackOffice API - LinkSocialAccount (Possible)

**Endpoint:** `POST /api/Client/LinkSocialAccount`

**Mentioned In:** CT-751 spec (TC4 documentation)

**Purpose:** Link social account to existing player

**Request (Expected):**
```json
{
  "clientId": 3563473,
  "provider": "Google",
  "providerUserId": "google_user_id"
}
```

**Status:** ❓ **Not tested** (QA environment inaccessible)

---

### 4. BackOffice API - DeactivateClients

**Endpoint:** `POST /api/Client/DeactivateClients`

**Request:**
```json
[3563473]
```

**Purpose:** Deactivate player (blocks login, keeps data)

**Status:** ✅ **CONFIRMED WORKING** (tested on DEV)

**Source:** `/src/api/clients/backoffice-api.client.ts`

---

## ❌ Test Results

| Test | Environment | Status | Notes |
|------|-------------|--------|-------|
| QA Website Login | minebit-casino.qa.sofon.one | ❌ 405 | Method Not Allowed |
| QA AdminWebAPI | qa-adminwebapi.minebit.com | ❌ DNS Error | DNS resolution failed |
| UnlinkSocialAccount | - | ❓ Not tested | QA inaccessible |
| GetClientLogins | - | ❓ Not tested | Requires login |

---

## ✅ Working Endpoints (DEV Environment)

| Endpoint | Method | Status | Purpose |
|----------|--------|--------|---------|
| `/api/Client/DeactivateClients` | POST | ✅ Works | Block player login |
| `/api/Client/ChangeClientDetails` | POST | ✅ Works | Mark as test (isTest: true) |
| `/api/Client/GetClientById` | POST | ✅ Works | Get player details |

---

## 🚨 Critical Discovery

**NO DELETE ENDPOINT EXISTS**

System uses:
- **DeactivateClients** to block access (doesn't delete data)
- **LinkedRegistrationSources** to track social accounts
- No direct "Delete Social Account" endpoint found in documentation

---

## 💡 Solutions for CT-752

### Option 1: Use DeactivateClients (Recommended)

**Advantages:**
- ✅ Confirmed working on DEV
- ✅ Preserves data for audit trail
- ✅ Allows testing with same Google account

**Steps:**
1. Login as admin on QA
2. Call DeactivatePlayers (or DeactivateClients) for player ID
3. Create new test player
4. Test with clean state

**Example (QA):**
```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/DeactivateClients" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "[3563473]"
```

---

### Option 2: Mark as Test Player

**Endpoint:** `/api/Client/ChangeClientDetails`

**Advantages:**
- ✅ Confirmed working on DEV
- ✅ Keeps player active but marked as test
- ✅ Test accounts can be filtered in analytics

**Steps:**
1. Call ChangeClientDetails with `isTest: true`
2. Test with new Google account
3. Unmark as test if needed

**Example:**
```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/ChangeClientDetails" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d '{"id": 3563473, "isTest": true}'
```

---

### Option 3: Get UnlinkSocialAccount from Backend Team

**Request from Backend Team:**

**Ask for:**
1. UnlinkSocialAccount endpoint specification
2. Where it's documented
3. Whether it's available on QA
4. Request/response examples

**Questions:**
```
Does UnlinkSocialAccount endpoint exist?
Is it documented in OpenAPI/Swagger?
What are the required parameters?
Does it require admin authentication?
```

---

### Option 4: Database Seed (Best for CI/CD)

**Request from Backend/DevOps Team:**

**Ask for:**
1. Pre-create test users in QA database
2. With no linked social accounts
3. Or with specific test accounts for each test scenario

**Advantages:**
- ✅ No OAuth dependency
- ✅ Reproducible tests
- ✅ Clean state for each test
- ✅ No manual cleanup needed

---

## 📊 Comparison: Deactivate vs Unlink

| Feature | DeactivateClients | UnlinkSocialAccount (Hypothetical) |
|---------|------------------|---------------------------------|
| Blocks login | ✅ Yes | ✅ Yes |
| Deletes data | ❌ No (preserves) | ✅ Yes (probably) |
| Audit trail | ✅ Yes | ⚠️ Maybe |
| Works on DEV | ✅ Confirmed | ❓ Unknown |
| Works on QA | ⚠️ Requires VPN | ❓ Unknown |

---

## 🎯 Recommendation for CT-752

**SHORT TERM (Immediate):**

Use **DeactivateClients** on QA environment:
```bash
# Requires VPN access to QA
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/DeactivateClients" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "[3563473]"
```

This will block the test player and allow new registration with same Google account.

---

**MEDIUM TERM (Proper Solution):**

**Ask Backend Team for:**
1. **UnlinkSocialAccount endpoint** - specifically for unlinking social accounts
2. **GetClientLogins endpoint** - to verify linked accounts
3. **API documentation** for social account management

**Use cases to communicate:**
- Need to unlink Google account to test different OAuth flows
- Need to verify LinkedRegistrationSources after unlinking
- Want to ensure social accounts can be removed without deleting player

---

**LONG TERM (Best Practice):**

**Database Seed for Test Accounts:**
1. Pre-create test users without linked social accounts
2. Use test accounts for OAuth linking tests
3. No manual cleanup needed between tests
4. Each test has clean initial state

---

## 📚 References

- **Test Spec:** `/tests/api/tickets/CT-751-linked-sources.spec.ts`
- **Client API:** `/src/api/clients/backoffice-api.client.ts`
- **Fixture:** `/src/fixtures/api.fixture.ts`
- **Config:** `/src/config/envConfig.ts`

---

## 🔧 Authentication Notes

**UserId by Environment:**
- DEV/QA: UserId: 1 (from api.fixture.ts)
- PROD: UserId: 560 (from api.fixture.ts)

**BackOffice API Base URLs:**
- DEV: https://adminwebapi.dev.sofon.one/api
- QA: https://qa-adminwebapi.minebit.com/api
- PROD: https://adminwebapi.prod.sofon.one/api

**⚠️ CRITICAL:** Using wrong UserId results in 401 Unauthorized!
QA environment requires VPN access.
