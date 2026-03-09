# API Context: CT-709 - OAuth Login Refactor (External Identity)

## Summary
Backend refactor to use external provider identifiers (`ExternalIdentity.ExternalId`) instead of email/user_id for social login (Google, Telegram). Existing OAuth endpoints remain unchanged, but the backend lookup logic now prioritizes ExternalId with fallback to pre-migration accounts.

## Affected Endpoints

### 1. Google OneTap Authentication
`POST /api/v3/GoogleAccount/OneTapAuth`

**Auth:** No authentication required (this is the login endpoint).

**Payload:**
```json
{
  "credential": "string (JWT from Google OneTap)",
  "partnerId": 123,
  "deviceType": "Web",
  "deviceFingerprint": "string"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "token": "string",
    "refreshToken": "string",
    "clientId": 12345,
    "userName": "string",
    "email": "string",
    "isEmailVerified": true,
    "currencyId": "USD",
    "balance": 1000.00,
    "externalId": "user@example.com"  // NEW: ExternalId now populated
  },
  "success": true,
  "message": null,
  "errors": null
}
```

**Backend Changes:**
- Primary lookup: `ExternalIdentity.ExternalId == email` (case-insensitive)
- Fallback for pre-migration: Email/UserName lookup
- Backfill: On successful login, `ExternalId` is populated if missing
- Uniqueness: (ExternalId, RegistrationSource, PartnerId) must be unique

---

### 2. Google Get Auth URL
`GET /api/v3/GoogleAccount/GetAuthUrl`

**Auth:** No authentication required.

**Query Parameters:**
- `PartnerId` (optional, int32): Partner ID
- `DeviceType` (optional, enum): Device type (Web, Mobile, etc.)
- `DeviceFingerprint` (optional, string): Device fingerprint

**Response (200 OK):**
```json
{
  "data": "https://accounts.google.com/...",
  "success": true
}
```

---

### 3. Google OAuth Callback
`POST /api/v3/GoogleAccount/Callback`

**Auth:** No authentication required.

**Payload:** Google OAuth callback data (code, state, etc.)

**Response (200 OK):**
```json
{
  "data": {
    "token": "string",
    "refreshToken": "string",
    "clientId": 12345,
    "userName": "string",
    "email": "string",
    "isEmailVerified": true,
    "currencyId": "USD",
    "balance": 1000.00,
    "externalId": "user@example.com"
  },
  "success": true
}
```

**Backend Changes:**
Same lookup logic as OneTapAuth (ExternalId first, then email fallback).

---

### 4. Telegram Hash Authentication
`POST /api/v3/TelegramAccount/HashAuth`

**Auth:** No authentication required.

**Payload:**
```json
{
  "hash": "string (Telegram WebApp initData hash)",
  "partnerId": 123,
  "deviceType": "Web",
  "deviceFingerprint": "string"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "token": "string",
    "refreshToken": "string",
    "clientId": 12345,
    "userName": "string",
    "email": "string",
    "isEmailVerified": true,
    "currencyId": "USD",
    "balance": 1000.00,
    "externalId": "TG123456789"  // NEW: ExternalId now populated
  },
  "success": true,
  "message": null,
  "errors": null
}
```

**Backend Changes:**
- Primary lookup: `ExternalIdentity.ExternalId == "TG{telegramUserId}"`
- Fallback for pre-migration: UserName lookup (TG-prefixed)
- Backfill: On successful login, `ExternalId` is populated if missing

---

## Testing Advice

### CT-709 Specific Requirements

#### 1. Google Login Flow

**Test Case 1: Existing Google User (Post-Migration)**
- User already has Google linked with `ExternalId = email` in `ExternalIdentity` table
- Login via OneTapAuth
- Expected: Login succeeds, user authenticated correctly

**Test Case 2: Existing Google User (Pre-Migration)**
- User linked Google before this change (no `ExternalId` populated)
- Login via OneTapAuth
- Expected: Login succeeds via email fallback, AND `ExternalId` is backfilled automatically
- Verify DB: Check that `ExternalIdentity.ExternalId` now contains the email

**Test Case 3: New Google Registration**
- New user registers via Google
- Expected: Registration succeeds, `ExternalIdentity.ExternalId = email` (lowercase)
- Verify DB: Check that new `ExternalIdentity` row exists with correct `ExternalId`

**Test Case 4: Email Change Scenario**
- User has Google linked, then changes their email in their profile
- Login again via Google with new email
- Expected: Login still works because lookup is by `ExternalId` (old email), not current profile email
- This ensures stability even if user changes email elsewhere

#### 2. Telegram Login Flow

**Test Case 5: Existing Telegram User (Post-Migration)**
- User already has Telegram linked with `ExternalId = "TG{id}"`
- Login via HashAuth
- Expected: Login succeeds

**Test Case 6: Existing Telegram User (Pre-Migration)**
- User linked Telegram before (no `ExternalId`, only `UserName = "TG{id}"`)
- Login via HashAuth
- Expected: Login succeeds via UserName fallback, AND `ExternalId` is backfilled
- Verify DB: `ExternalIdentity.ExternalId` now contains "TG{telegramUserId}"

**Test Case 7: New Telegram Registration**
- New user registers via Telegram
- Expected: Registration succeeds, `ExternalIdentity.ExternalId = "TG{telegramUserId}"`
- Verify DB: New `ExternalIdentity` row with correct format

#### 3. Linking Social to Existing Account

**Test Case 8: Link Google to Existing Account**
- User has existing account (email/password)
- User links Google to their account
- Expected: `ExternalIdentity.ExternalId` set to Google email (NOT username)
- Verify DB: `ExternalIdentity` row exists with correct values

**Test Case 9: Link Telegram to Existing Account**
- User has existing account
- User links Telegram to their account
- Expected: `ExternalIdentity.ExternalId` set to "TG{telegramUserId}"
- Verify DB: `ExternalIdentity` row exists with correct format

#### 4. Uniqueness & Edge Cases

**Test Case 10: Same Google Email Across Partners**
- User A links Google (user@example.com) in Partner 1
- User A can link same Google email in Partner 2
- Expected: Both succeed (uniqueness is per Partner)

**Test Case 11: Prevent Duplicate Google Links in Same Partner**
- User A links Google (user@example.com) in Partner 1
- User B tries to link same Google (user@example.com) in Partner 1
- Expected: Fails - email already linked to another user in same partner

**Test Case 12: Case-Insensitive Google Email**
- User registers with Google as User@Example.COM
- Expected: `ExternalId` stored as lowercase: "user@example.com"
- Subsequent logins work with any case

#### 5. Migration Verification (Post-Deployment)

**Test Case 13: DB Check - Google Users**
- After deployment, query DB for existing Google users
- Verify: `ExternalIdentity.ExternalId` is populated with lowercased email
- Expected: All pre-migration Google users have backfilled `ExternalId`

**Test Case 14: DB Check - Telegram Users**
- After deployment, query DB for existing Telegram users
- Verify: `ExternalIdentity.ExternalId` is populated with "TG{id}" format
- Expected: All pre-migration Telegram users have backfilled `ExternalId`

#### 6. Regression Testing

**Test Case 15: Traditional Email/Password Login**
- Ensure regular email/password login still works
- Verify no side effects from OAuth changes

**Test Case 16: OTP Login**
- If OTP login exists, verify it still works
- No impact expected (different flow)

**Test Case 17: Session/Token Management**
- After OAuth login, verify tokens work correctly
- Test refresh token flow
- Verify session persistence

---

## Database Changes

### New/Modified Tables

**ExternalIdentity Table** (existing, now with populated ExternalId)
- `ExternalId` (string): The stable external identifier
  - Google: email (lowercase)
  - Telegram: "TG{telegramUserId}"
- `RegistrationSourceId` (int): Source type (Google, Telegram, etc.)
- `ClientId` (int): FK to Client
- Index: Composite on `(ExternalId, RegistrationSourceId)`

**Migration:**
- Existing Telegram users: Copy `UserName` (TG-prefixed) to `ExternalId`
- Existing Google users: Copy lowercased `Email` to `ExternalId`
- Orphan clients: Insert missing `ExternalIdentity` rows

---

## Acceptance Criteria

- ✅ New `ExternalIdentity.ExternalId` table column utilized correctly
- ✅ Telegram login uses `ExternalId` as primary lookup
- ✅ Google login uses `ExternalId` (email) as primary lookup
- ✅ First login creates `ExternalIdentity` entry automatically
- ✅ Pre-migration users get `ExternalId` backfilled on next login
- ✅ DB migration populates `ExternalId` for existing users
- ✅ Uniqueness enforced per (ExternalId, RegistrationSource, PartnerId)
- ✅ Same user can link same socials in different partners
- ✅ Different users cannot use same social in same partner
- ✅ Old login-by-email-for-socials and login-by-prefixed-Telegram-id removed (as primary)
- ✅ Email changes don't break OAuth login (stable `ExternalId`)
- ✅ No regression on other login methods

---

## Related JIRA Info
- **Ticket:** CT-709 - "[BE] Refactor Login & Registration"
- **Status:** Ready for testing
- **Priority:** Normal
- **Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/103
- **Blocked:** CT-656
- **Linked Issues:** CRYPTO-450 (implements)

## Notes
- Change is purely backend; no API contract changes
- Response structure remains the same
- `externalId` field in response was already present, now reliably populated
- Migration runs on deployment; no downtime expected
- Tiered lookup ensures backward compatibility:
  1. Primary: `ExternalIdentity.ExternalId` lookup
  2. Fallback: Email/UserName (pre-migration)
  3. Register: New user registration
