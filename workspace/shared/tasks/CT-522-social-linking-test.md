# CT-522: Social Account Linking via Existing Token — Test Plan

**Jira:** https://next-t-code.atlassian.net/browse/CT-522
**Status:** Ready for testing
**Type:** Backend
**Priority:** High
**Environment:** QA
**Dependencies:** CT-709 (ExternalIdentity refactor)

---

## 📋 Objective

Валідація функціоналу прив'язки соціальних акаунтів (Google, Telegram) до існуючого юзера через OAuth state параметр:
- User може приєднати Google/Telegram до свого акаунту
- Token передається через OAuth `state` параметр
- Backend знаходить існуючого юзера і прив'язує соціальний акаунт
- При невалідному token — помилка, НЕ реєстрація нового юзера
- Множинні соціальні акаунти на одному юзері підтримуються

---

## 🧪 Test Scenarios

### 1. Google Linking — Valid Token (Happy Path)

**Preconditions:**
- User logged in with valid token
- Token: `existing-valid-token-xyz`

**Steps:**
1. Frontend calls `GET /api/v3/GoogleAccount/GetAuthUrl?state={existingValidToken}`
2. User completes Google OAuth flow
3. Backend calls `POST /api/v3/GoogleAccount/Callback`
4. Verify response structure:
   ```json
   {
     "data": {
       "token": "existing-valid-token-xyz",  // Same token, not new
       "refreshToken": "string",
       "clientId": 12345,
       "userName": "string",
       "email": "string",
       "externalId": "user@example.com",
       "linked": true
     },
     "success": true
   }
   ```
5. **Database Check:**
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ClientId = [existing_user_client_id]
   AND RegistrationSourceId = [Google];
   ```

**Expected Result:**
- ✅ Linking successful (200 OK)
- ✅ Same token returned (session continuity)
- ✅ ExternalIdentity row created with ExternalId = email
- ✅ No new user created

---

### 2. Google Linking — Expired Token

**Preconditions:**
- User has expired token
- Token: `expired-token-abc`

**Steps:**
1. Frontend calls `GET /api/v3/GoogleAccount/GetAuthUrl?state={expiredToken}`
2. User completes Google OAuth flow
3. Backend calls `POST /api/v3/GoogleAccount/Callback`
4. Verify error response:
   ```json
   {
     "data": null,
     "success": false,
     "message": "Invalid or expired token",
     "errors": ["Token not found or expired"]
   }
   ```

**Expected Result:**
- ✅ Error response (401 Unauthorized)
- ✅ NO new user created
- ✅ No ExternalIdentity row created

---

### 3. Google Linking — Invalid/Malformed Token

**Preconditions:**
- Invalid token format

**Steps:**
1. Frontend calls `GET /api/v3/GoogleAccount/GetAuthUrl?state={invalidToken}`
2. User completes Google OAuth flow
3. Backend calls `POST /api/v3/GoogleAccount/Callback`
4. Verify error response

**Expected Result:**
- ✅ Error response (401 Unauthorized)
- ✅ NO new user created

---

### 4. Google Linking — Same Account (Idempotent)

**Preconditions:**
- User already has Google linked (user1@gmail.com)

**Steps:**
1. User tries to link same Google account again
2. Verify response behavior

**Expected Result:**
- ✅ Either success (idempotent) or error (already linked)
- ✅ No duplicate ExternalIdentity entries

---

### 5. Google Linking — Different Email Than Profile

**Preconditions:**
- User profile email: `user1@example.com`
- Google email: `user2@gmail.com`

**Steps:**
1. Link Google account to existing user
2. **Database Check:**
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ClientId = [user_client_id];
   ```

**Expected Result:**
- ✅ Linking successful
- ✅ ExternalId = `user2@gmail.com` (Google email)
- ✅ User profile email unchanged

---

### 6. Telegram Linking — Valid Token

**Preconditions:**
- User logged in with valid token
- Token: `existing-valid-token-xyz`

**Steps:**
1. Frontend calls `POST /api/v3/TelegramAccount/HashAuth` with:
   ```json
   {
     "hash": "telegram-hash-data",
     "state": "{existingValidToken}",
     "partnerId": 123,
     "deviceType": "Web",
     "deviceFingerprint": "abc123"
   }
   ```
2. Verify response structure:
   ```json
   {
     "data": {
       "token": "existing-valid-token-xyz",
       "refreshToken": "string",
       "clientId": 12345,
       "userName": "string",
       "email": "string",
       "externalId": "TG123456789",
       "linked": true
     },
     "success": true
   }
   ```
3. **Database Check:**
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ClientId = [existing_user_client_id]
   AND ExternalId = 'TG123456789';
   ```

**Expected Result:**
- ✅ Linking successful
- ✅ ExternalIdentity row created with ExternalId = `TG{id}`
- ✅ Same token returned

---

### 7. Telegram Linking — Expired Token

**Preconditions:**
- User has expired token

**Steps:**
1. Call `POST /api/v3/TelegramAccount/HashAuth` with expired token in `state`
2. Verify error response (401 Unauthorized)

**Expected Result:**
- ✅ Error response (401 Unauthorized)
- ✅ NO new user created

---

### 8. Telegram Linking — Same Account (Idempotent)

**Preconditions:**
- User already has Telegram linked (TG123456789)

**Steps:**
1. User tries to link same Telegram account again
2. Verify response behavior

**Expected Result:**
- ✅ Either success (idempotent) or error (already linked)
- ✅ No duplicate ExternalIdentity entries

---

### 9. Multiple Social Links — One User

**Preconditions:**
- User has existing account (email/password)

**Steps:**
1. Link Google account
   - Verify: ExternalIdentity row created for Google
   - Verify: Login via Google works
2. Link Telegram account
   - Verify: ExternalIdentity row created for Telegram
   - Verify: Login via Telegram works
3. **Database Check:**
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ClientId = [user_client_id];
   ```
   - Expect: 2 rows (Google + Telegram)

**Expected Result:**
- ✅ Both social accounts linked to same user
- ✅ Login via either social works
- ✅ No duplicate ExternalIdentity entries for same social type

---

### 10. Empty State Parameter (Normal Registration Flow)

**Preconditions:**
- No existing user

**Steps:**
1. Call OAuth callback with empty `state` parameter
2. Verify behavior

**Expected Result:**
- ✅ Proceed with normal registration flow
- ✅ New user created if OAuth valid

---

### 11. Malformed State Parameter

**Preconditions:**
- Invalid JSON or malformed `state`

**Steps:**
1. Call OAuth callback with malformed `state`
2. Verify error response

**Expected Result:**
- ✅ Error response
- ✅ No user creation

---

### 12. State Contains Random String

**Preconditions:**
- Random non-token string in `state`

**Steps:**
1. Call OAuth callback with random `state`
2. Verify error response

**Expected Result:**
- ✅ Error response
- ✅ No user creation

---

### 13. Token Not Found

**Preconditions:**
- Valid token format but non-existent user

**Steps:**
1. Call OAuth callback with non-existent token
2. Verify error response

**Expected Result:**
- ✅ Error response
- ✅ No new user created

---

### 14. User Deleted But Token Exists

**Preconditions:**
- User deleted but token format valid

**Steps:**
1. Call OAuth callback with deleted user's token
2. Verify error response

**Expected Result:**
- ✅ Error response
- ✅ No new user creation

---

### 15. Token Continuity After Linking

**Preconditions:**
- User logged in with valid token

**Steps:**
1. Link Google account
2. Verify response contains SAME token (not new)
3. Test: Use token for subsequent API calls

**Expected Result:**
- ✅ Same token returned
- ✅ Session remains active
- ✅ Token still valid for API calls

---

### 16. Refresh Token After Linking

**Preconditions:**
- User linked Google/Telegram

**Steps:**
1. Use refresh token to get new access token
2. Verify refresh token still valid

**Expected Result:**
- ✅ Refresh token works
- ✅ No session interruption

---

### 17. Link Google, Then Link Different Google

**Preconditions:**
- User has Google linked (user1@gmail.com)

**Steps:**
1. User tries to link different Google (user2@gmail.com)
2. Verify response behavior

**Expected Result:**
- ✅ Clarify expected behavior with backend:
  - Option A: Error (only one Google per account)
  - Option B: Replace old Google with new
- ✅ No duplicate ExternalIdentity entries

---

### 18. Unlink and Re-Link

**Preconditions:**
- User has Google linked

**Steps:**
1. Unlink Google (if endpoint exists)
2. Re-link same Google account
3. Verify ExternalId populated correctly

**Expected Result:**
- ✅ Unlink works (if endpoint exists)
- ✅ Re-link works correctly
- ✅ ExternalId = email

---

## 🔧 Testing Approach

### Option 1: API Testing via Swagger (Recommended)
- Use Website API Swagger (QA environment)
- Execute OAuth endpoints directly
- Test linking flow with valid/expired tokens
- Validate responses and DB state

### Option 2: Database Direct Testing
- Query `ExternalIdentity` table directly
- Validate linking results
- Check uniqueness constraints

### Option 3: UI Testing + DB Validation
- Test linking via UI (if frontend implemented)
- Validate DB state after each action

---

## 🗂️ Test Data Requirements

- **Existing user account:** For testing token continuity
- **Google test accounts:**
  - Account 1: user1@gmail.com (for primary linking)
  - Account 2: user2@gmail.com (for testing different Google)
- **Telegram test account:** TG123456789
- **Expired/invalid tokens:** For negative testing
- **Database access:**
  - Read access to `ExternalIdentity` table
  - Read access to `Clients` table

---

## 📊 Evidence

Save evidence to: `shared/test-results/CT-522/`
- API request/response logs
- Database query results (screenshots or CSV)
- Linking flow screenshots

---

## ⚠️ Notes

- **Environment:** QA (as backend is ready for testing)
- **Dependencies:** Requires CT-709 migration to be deployed first
- **Critical:** Backend MUST return error (not registration) when token invalid
- **Uniqueness:** (ExternalId, RegistrationSourceId, PartnerId) enforced
- **Session continuity:** Same token returned, not new one
- **Frontend responsibility:** Must include current user token in OAuth `state` parameter

---

## 📌 Swagger Endpoints to Test

### Google OAuth
- `GET /api/v3/GoogleAccount/GetAuthUrl` — Get auth URL with state
- `POST /api/v3/GoogleAccount/Callback` — OAuth callback

### Telegram OAuth
- `POST /api/v3/TelegramAccount/HashAuth` — Telegram hash auth with state

**Note:** Both endpoints accept `state` parameter with existing user token for linking flow.
