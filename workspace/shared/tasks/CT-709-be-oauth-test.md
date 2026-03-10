# CT-709: Backend OAuth Refactor — Test Plan (Dev Environment)

**Jira:** https://next-t-code.atlassian.net/browse/CT-709
**Status:** Testing
**Type:** Backend
**Environment:** Dev
**PR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/103

---

## 📋 Objective

Валідація рефакторингу OAuth авторизації:
- ExternalIdentity таблиця створена та працює
- Telegram login використовує ExternalId = `TG{telegramUserId}`
- Google login використовує ExternalId = `email`
- Fallback механізм для pre-migration users працює
- Migration коректно заповнює ExternalId для існуючих юзерів

---

## 🧪 Test Scenarios

### 1. Google OAuth — Existing User (Backfill)

**Preconditions:**
- Existing Google user в DB (created before migration)
- Email: `test-google@example.com`

**Steps:**
1. Login via Google OAuth API endpoint
2. Verify login succeeds (200 response)
3. **Database Check:** Query `ExternalIdentity` table
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ExternalId = 'test-google@example.com'
   AND RegistrationSourceId = [Google];
   ```
4. Verify ExternalId populated correctly

**Expected Result:**
- ✅ Login successful
- ✅ ExternalIdentity row created/updated
- ✅ ExternalId = email (lowercased)

---

### 2. Google OAuth — New User Registration

**Preconditions:**
- New Google account (not in DB)
- Email: `new-google-test@example.com`

**Steps:**
1. Register via Google OAuth API endpoint
2. **Database Check:** Query `ExternalIdentity` table
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ExternalId = 'new-google-test@example.com';
   ```
3. Verify ClientId created
4. Verify ExternalId = email

**Expected Result:**
- ✅ Registration successful
- ✅ New Client record created
- ✅ ExternalIdentity.ExternalId = email (lowercased)

---

### 3. Google OAuth — Email Change Scenario

**Preconditions:**
- Existing Google user with ExternalId populated
- User changed email in Google account

**Steps:**
1. User changes email in Google: `old-email@example.com` → `new-email@example.com`
2. Login via Google OAuth
3. **Database Check:** Verify ExternalId still = `old-email@example.com`
4. Verify login still works (resolves by ExternalId, not email)

**Expected Result:**
- ✅ Login successful despite email change
- ✅ ExternalId unchanged (stable identifier)
- ✅ No duplicate ExternalIdentity rows

---

### 4. Telegram OAuth — Existing User

**Preconditions:**
- Existing Telegram user (TG-prefixed user_id)
- Telegram ID: `123456789`

**Steps:**
1. Login via Telegram OAuth API endpoint
2. **Database Check:** Query `ExternalIdentity` table
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ExternalId = 'TG123456789'
   AND RegistrationSourceId = [Telegram];
   ```
3. Verify ExternalId = `TG{telegramUserId}`

**Expected Result:**
- ✅ Login successful
- ✅ ExternalIdentity lookup via ExternalId
- ✅ No fallback to UserName needed

---

### 5. Telegram OAuth — New User Registration

**Preconditions:**
- New Telegram account (not in DB)
- Telegram ID: `987654321`

**Steps:**
1. Register via Telegram OAuth API endpoint
2. **Database Check:** Query `ExternalIdentity` table
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ExternalId = 'TG987654321';
   ```
3. Verify ClientId created

**Expected Result:**
- ✅ Registration successful
- ✅ New Client record created
- ✅ ExternalIdentity.ExternalId = `TG987654321`

---

### 6. Social Account Linking

**Preconditions:**
- Existing user with email/password login
- User links Google account

**Steps:**
1. Link Google account to existing user
2. **Database Check:** Query `ExternalIdentity` table
   ```sql
   SELECT * FROM ExternalIdentity
   WHERE ClientId = [existing_user_client_id];
   ```
3. Verify ExternalId stored correctly (not email for Google)

**Expected Result:**
- ✅ Linking successful
- ✅ ExternalIdentity row created with correct ExternalId

---

### 7. Migration Verification (Database Spot-Check)

**Steps:**
1. Query existing Google users before migration:
   ```sql
   SELECT COUNT(*) FROM Clients
   WHERE RegistrationSourceId = [Google]
   AND Email IS NOT NULL;
   ```
2. After deployment, verify ExternalId populated:
   ```sql
   SELECT COUNT(*) FROM ExternalIdentity
   WHERE RegistrationSourceId = [Google];
   ```
3. Repeat for Telegram users:
   ```sql
   SELECT COUNT(*) FROM ExternalIdentity
   WHERE RegistrationSourceId = [Telegram]
   AND ExternalId LIKE 'TG%';
   ```

**Expected Result:**
- ✅ ExternalId count matches Clients count
- ✅ All Telegram ExternalIds start with 'TG'
- ✅ All Google ExternalIds = lowercased email

---

## 🔧 Testing Approach

### Option 1: API Testing via Swagger (Recommended)
- Use Website API Swagger (dev environment)
- Execute OAuth endpoints directly
- Validate responses (200, tokens, etc.)

### Option 2: Database Direct Testing
- Query `ExternalIdentity` table directly
- Validate migration results
- Check constraints and indexes

### Option 3: UI Testing + DB Validation
- Login via UI (Telegram/Google buttons)
- Validate DB state after each action

---

## 🗂️ Test Data Requirements

- **Google test accounts:**
  - Existing user (pre-migration)
  - New user (for registration test)

- **Telegram test accounts:**
  - Existing user (TG-prefixed user_id)
  - New user (for registration test)

- **Database access:**
  - Read access to `ExternalIdentity` table
  - Read access to `Clients` table

---

## 📊 Evidence

Save evidence to: `shared/test-results/CT-709/`
- API request/response logs
- Database query results (screenshots or CSV)
- Migration validation reports

---

## ⚠️ Notes

- **Environment:** Dev only (as specified by developer)
- **Fallback:** Pre-migration users should still login via UserName fallback
- **Backwards compatibility:** Old login-by-email/prefixed-id removed
- **Migration:** One-time migration populates ExternalId for existing users

---

## 📌 Swagger Endpoints to Test (TBD)

**TODO:** Check Swagger for:
- `/api/auth/google` — Google OAuth
- `/api/auth/telegram` — Telegram OAuth
- `/api/auth/link` — Account linking

Update with actual endpoint paths from Swagger.
