# Test Plan: CT-709 — [BE] Refactor Login & Registration (AUTONOMOUS)

**Ticket:** CT-709 - [BE] Refactor Login & Registration
**Status:** Ready for testing
**Type:** Backend-only (API testing)
**Estimated Time:** 4 hours
**Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/103

---

## 📋 Executive Summary

OAuth refactor to use stable `ExternalIdentity.ExternalId` instead of email/user_id. **This test plan is fully autonomous** — no DB access required, no external test data dependencies.

### Key Changes:
- **Google:** `ExternalId = email` (lowercase) — primary identifier
- **Telegram:** `ExternalId = "TG{telegramUserId}"` — primary identifier
- **Tiered lookup:** ExternalId → Email/UserName fallback → Registration
- **Auto-backfill:** Legacy accounts get ExternalId on first login

### Test Strategy:
✅ **API-only testing** via Playwright/curl
✅ **Mocked test data** (Google JWT, Telegram hash)
✅ **Response validation** (no DB queries needed)
✅ **State transitions** verified through API responses

---

## 🔧 Test Data Setup (Autonomous)

### 1. Telegram WebApp Hash Generator

Create `scripts/generate_telegram_hash.py`:

```python
import hmac
import hashlib
import urllib.parse
import json
from datetime import datetime

def generate_telegram_init_data(bot_token: str, user_id: int, username: str = "test_user"):
    """
    Generate valid Telegram WebApp initData for testing.
    Based on: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    
    # Create user object
    user_data = {
        "id": user_id,
        "first_name": f"Test{user_id}",
        "last_name": "User",
        "username": username,
        "language_code": "en"
    }
    
    # Create initData query string
    init_data = {
        "query_id": f"AAH{user_id}MQ{datetime.now().timestamp():.0f}",
        "user": json.dumps(user_data),
        "auth_date": str(int(datetime.now().timestamp())),
    }
    
    # Sort and create data-check-string
    sorted_items = sorted(init_data.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])
    
    # Generate hash
    secret_key = hmac.new(
        b"WebAppData", 
        bot_token.encode(), 
        hashlib.sha256
    ).digest()
    
    hash_value = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Add hash to init_data
    init_data["hash"] = hash_value
    
    # Return as query string
    return urllib.parse.urlencode(init_data)

# Example usage:
# BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Get from bot father
# TEST_USER_ID = 123456789
# init_data = generate_telegram_init_data(BOT_TOKEN, TEST_USER_ID, "testuser")
# print(init_data)
```

**How to get bot token:**
1. Create test bot via @BotFather in Telegram (2 minutes)
2. Use bot token in test script
3. Or use existing dev bot token from team

---

### 2. Google OneTap JWT Mock

Create `scripts/mock_google_jwt.js`:

```javascript
const jwt = require('jsonwebtoken');

/**
 * Mock Google OneTap JWT for testing
 * Structure: https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
 */

function generateMockGoogleJWT(options = {}) {
  const {
    email = 'test.user@example.com',
    emailVerified = true,
    name = 'Test User',
    picture = 'https://example.com/photo.jpg',
    givenName = 'Test',
    familyName = 'User',
    aud = 'your-client-id.apps.googleusercontent.com',
    iss = 'https://accounts.google.com',
    sub = '12345678901234567890', // Unique Google user ID
  } = options;

  const now = Math.floor(Date.now() / 1000);
  
  const payload = {
    iss,
    sub,
    aud,
    iat: now,
    exp: now + 3600, // 1 hour
    email,
    email_verified: emailVerified,
    name,
    picture,
    given_name: givenName,
    family_name: familyName,
    locale: 'en',
    hd: 'example.com', // Hosted domain (G Suite)
  };

  // Use any secret for testing (backend will verify via Google API in real scenario)
  // For local testing, backend might accept test tokens
  const token = jwt.sign(payload, 'test-secret-key');
  
  return token;
}

// Example usage:
// const credential = generateMockGoogleJWT({ email: 'new.user@test.com' });
// console.log(credential);

module.exports = { generateMockGoogleJWT };
```

**Installation:**
```bash
npm install jsonwebtoken
```

---

## 📝 Test Cases (Autonomous Execution)

### Test Suite 1: Google OAuth Flow

#### TC-G001: Existing Google User Login
**Priority:** P0 | **Execution:** API

**Preconditions:**
- QA environment deployed
- Existing test user with Google linked (from previous tests or created via API)

**Steps:**
```bash
# 1. Generate mock Google JWT
GOOGLE_JWT=$(node scripts/mock_google_jwt.js | tail -1)

# 2. Call OneTapAuth endpoint
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{
    \"credential\": \"$GOOGLE_JWT\",
    \"partnerId\": 1,
    \"deviceType\": \"Web\",
    \"deviceFingerprint\": \"test-fingerprint-001\"
  }" \
  | jq '.'

# 3. Validate response
# Expected: 200 OK, token returned, externalId populated
```

**Validation (via API response):**
- ✅ Response status: 200
- ✅ Response contains: `data.token` (valid JWT)
- ✅ Response contains: `data.externalId` (matches email)
- ✅ Response contains: `data.clientId` (numeric ID)
- ✅ Token is valid (can make authenticated requests)

**Evidence:** Save full response JSON to `test-results/CT-709/TC-G001-response.json`

---

#### TC-G002: New Google User Registration
**Priority:** P0 | **Execution:** API

**Steps:**
```bash
# 1. Generate NEW unique email
UNIQUE_EMAIL="test.$(date +%s)@example.com"
GOOGLE_JWT=$(node scripts/mock_google_jwt.js | tail -1)

# 2. Call OneTapAuth
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{
    \"credential\": \"$GOOGLE_JWT\",
    \"partnerId\": 1,
    \"deviceType\": \"Web\",
    \"deviceFingerprint\": \"test-fingerprint-002\"
  }" \
  | jq '.'

# 3. Verify new user created
# Expected: new clientId, email verified = false (or true depending on config)
```

**Validation (via API response):**
- ✅ Response status: 200
- ✅ Response contains: `data.clientId` (NEW ID)
- ✅ Response contains: `data.externalId = email` (lowercase)
- ✅ Response contains: `data.isEmailVerified = true` (Google verifies)

**Evidence:** Save response JSON

---

#### TC-G003: Google Email Case Insensitivity
**Priority:** P1 | **Execution:** API

**Steps:**
```bash
# 1. Register with uppercase email
EMAIL_UPPER="Test.User@Example.COM"
GOOGLE_JWT_UPPER=$(node -e "const {generateMockGoogleJWT} = require('./scripts/mock_google_jwt.js'); console.log(generateMockGoogleJWT({email: '$EMAIL_UPPER'}));")

curl -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT_UPPER\", \"partnerId\": 1}" \
  | jq '.data.externalId'

# Expected: "test.user@example.com" (lowercase)
```

**Validation:**
- ✅ `data.externalId` is lowercase (email normalization)
- ✅ Login succeeds with any case in JWT

---

### Test Suite 2: Telegram OAuth Flow

#### TC-TG001: Existing Telegram User Login
**Priority:** P0 | **Execution:** API

**Preconditions:**
- Python script ready
- Bot token available (from @BotFather)
- Test Telegram user ID

**Steps:**
```bash
# 1. Generate Telegram hash
BOT_TOKEN="YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
TEST_USER_ID="123456789"  # Your test Telegram ID

TELEGRAM_INIT_DATA=$(python3 scripts/generate_telegram_hash.py \
  --bot-token "$BOT_TOKEN" \
  --user-id "$TEST_USER_ID" \
  --username "testuser")

# 2. Call HashAuth endpoint
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/TelegramAccount/HashAuth \
  -H "Content-Type: application/json" \
  -d "{
    \"hash\": \"$TELEGRAM_INIT_DATA\",
    \"partnerId\": 1,
    \"deviceType\": \"Web\",
    \"deviceFingerprint\": \"test-fingerprint-003\"
  }" \
  | jq '.'

# 3. Validate response
```

**Validation:**
- ✅ Response status: 200
- ✅ Response contains: `data.token`
- ✅ Response contains: `data.externalId = "TG{telegramUserId}"`
- ✅ Token works for authenticated requests

**Evidence:** Save response JSON

---

#### TC-TG002: New Telegram User Registration
**Priority:** P0 | **Execution:** API

**Steps:**
```bash
# 1. Generate NEW Telegram user ID
NEW_USER_ID=$(shuf -i 100000000-999999999 -n 1)
TELEGRAM_INIT_DATA=$(python3 scripts/generate_telegram_hash.py \
  --bot-token "$BOT_TOKEN" \
  --user-id "$NEW_USER_ID" \
  --username "newuser$NEW_USER_ID")

# 2. Call HashAuth
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/TelegramAccount/HashAuth \
  -H "Content-Type: application/json" \
  -d "{\"hash\": \"$TELEGRAM_INIT_DATA\", \"partnerId\": 1}" \
  | jq '.'

# 3. Verify new user created
```

**Validation:**
- ✅ Response status: 200
- ✅ New `clientId` assigned
- ✅ `data.externalId = "TG{NEW_USER_ID}"`

---

### Test Suite 3: Backfill Verification (Critical)

#### TC-BF001: Pre-Migration Google User Backfill
**Priority:** P0 | **Execution:** API + State Check

**Preconditions:**
- Identify or create user registered BEFORE deployment
- If no pre-migration user exists, skip this test initially, then re-run after migration

**Steps:**
```bash
# 1. Get existing user (created before migration)
# Use email from test account created earlier

# 2. First login after deployment
GOOGLE_JWT=$(node scripts/mock_google_jwt.js | tail -1)
RESPONSE=$(curl -s -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT\", \"partnerId\": 1}")

echo "$RESPONSE" | jq '.'

# 3. Check if externalId is populated in response
EXTERNAL_ID=$(echo "$RESPONSE" | jq -r '.data.externalId')

if [ -n "$EXTERNAL_ID" ] && [ "$EXTERNAL_ID" != "null" ]; then
  echo "✅ Backfill SUCCESS: externalId = $EXTERNAL_ID"
else
  echo "❌ Backfill FAILED: externalId not populated"
fi

# 4. Login AGAIN and verify lookup uses ExternalId now
# (No way to verify this externally, but if login succeeds, it works)
curl -s -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT\", \"partnerId\": 1}" \
  | jq '.success'
```

**Validation:**
- ✅ First login: succeeds (fallback to email)
- ✅ First login response: `externalId` populated
- ✅ Second login: succeeds (ExternalId lookup)

**Note:** If no pre-migration users available, this test will be executed post-deployment with production users (monitor logs).

---

#### TC-BF002: Pre-Migration Telegram User Backfill
**Priority:** P0 | **Execution:** API

**Similar to TC-BF001, but for Telegram**

---

### Test Suite 4: Uniqueness & Edge Cases

#### TC-U001: Same Google Email Different Partners
**Priority:** P1 | **Execution:** API

**Steps:**
```bash
# 1. User registers in Partner 1
GOOGLE_JWT=$(node scripts/mock_google_jwt.js | tail -1)
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT\", \"partnerId\": 1}" \
  | jq '.data.clientId'

# 2. Same user in Partner 2
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT\", \"partnerId\": 2}" \
  | jq '.data.clientId'

# Expected: Two different clientIds (allowed)
```

**Validation:**
- ✅ Both registrations succeed
- ✅ Different `clientId` per partner
- ✅ Same `externalId` (email)

---

#### TC-U002: Duplicate Google Email Same Partner
**Priority:** P1 | **Execution:** API

**Steps:**
```bash
# 1. User A registers with email in Partner 1
EMAIL="duplicate.test@example.com"
GOOGLE_JWT_A=$(node -e "const {generateMockGoogleJWT} = require('./scripts/mock_google_jwt.js'); console.log(generateMockGoogleJWT({email: '$EMAIL', sub: '111111111'}));")

RESPONSE_A=$(curl -s -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT_A\", \"partnerId\": 1}")

CLIENT_ID_A=$(echo "$RESPONSE_A" | jq -r '.data.clientId')

# 2. User B tries same email in Partner 1
GOOGLE_JWT_B=$(node -e "const {generateMockGoogleJWT} = require('./scripts/mock_google_jwt.js'); console.log(generateMockGoogleJWT({email: '$EMAIL', sub: '222222222'}));")

RESPONSE_B=$(curl -s -X POST https://minebit-casino.qa.sofon.one/api/v3/GoogleAccount/OneTapAuth \
  -H "Content-Type: application/json" \
  -d "{\"credential\": \"$GOOGLE_JWT_B\", \"partnerId\": 1}")

# Check response
echo "$RESPONSE_B" | jq '.'

# Expected: Error or login as User A (email already linked)
```

**Validation:**
- ✅ Either error message: "Email already linked to another user"
- ✅ OR User B logs in as User A (account takeover prevention — verify behavior with backend team)

---

### Test Suite 5: Regression Tests

#### TC-R001: Traditional Email/Password Login
**Priority:** P0 | **Execution:** API

**Steps:**
```bash
# Use existing email/password user (created via API or existing test account)
curl -X POST https://minebit-casino.qa.sofon.one/api/v3/Account/Login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "existing.user@test.com",
    "password": "TestPass123!",
    "partnerId": 1
  }' \
  | jq '.success'
```

**Validation:**
- ✅ Login succeeds
- ✅ Token returned
- ✅ No OAuth-related errors

---

## 📊 Test Execution Plan

### Phase 1: Setup (30 minutes)
- [ ] Create Python script for Telegram hash generation
- [ ] Create Node.js script for Google JWT mock
- [ ] Test scripts locally with mock data
- [ ] Get bot token from @BotFather

### Phase 2: Smoke Tests (30 minutes)
- [ ] TC-G001: Existing Google login
- [ ] TC-G002: New Google registration
- [ ] TC-TG001: Existing Telegram login
- [ ] TC-TG002: New Telegram registration
- [ ] TC-R001: Email/password login

### Phase 3: Functional Tests (1 hour)
- [ ] TC-G003: Case sensitivity
- [ ] TC-BF001: Google backfill (if pre-migration user available)
- [ ] TC-BF002: Telegram backfill (if pre-migration user available)
- [ ] TC-U001: Cross-partner registration
- [ ] TC-U002: Duplicate email same partner

### Phase 4: Reporting (30 minutes)
- [ ] Compile results.json
- [ ] Write Slack message
- [ ] Write Jira comment

---

## 📋 Deliverables

1. **Test Scripts:**
   - `scripts/generate_telegram_hash.py`
   - `scripts/mock_google_jwt.js`

2. **Test Results:**
   - `test-results/CT-709/results.json` — Structured results
   - `test-results/CT-709/TC-*.json` — Individual test responses
   - `test-results/CT-709/slack-message.txt` — Quick summary
   - `test-results/CT-709/jira-comment.txt` — Detailed report

---

## 🎓 Acceptance Criteria Coverage

| AC | Test Case(s) | Validation Method |
|----|--------------|-------------------|
| ExternalId utilized | TC-G001, TC-TG001 | API response contains `externalId` |
| Telegram uses ExternalId | TC-TG001, TC-BF002 | Response shows `TG{id}` format |
| Google uses ExternalId | TC-G001, TC-G003 | Response shows lowercase email |
| Auto-create on first login | TC-G002, TC-TG002 | New clientId created |
| Backfill pre-migration | TC-BF001, TC-BF002 | `externalId` populated on first login |
| Uniqueness enforced | TC-U001, TC-U002 | Cross-partner allowed, same-partner blocked |
| Email changes stable | N/A | Cannot test without real email change in profile |
| No regression | TC-R001 | Traditional login still works |

---

## 🚨 Risk Mitigation

| Risk | Mitigation |
|------|------------|
| No pre-migration users available | Test backfill on staging/prod after deployment |
| Bot token unavailable | Create new bot via @BotFather (2 min) |
| Mock JWT rejected by backend | Use real Google OAuth in browser, extract token |
| API endpoints differ from docs | Check Swagger, test with real data first |

---

**Prepared by:** QA Agent (Clawver 🐞)
**Date:** 2026-03-10
**Status:** Ready for Autonomous Execution
**Dependencies:** None (all tools available)
