# API Context: CT-522 - Link Social Account Using Existing Token

## Summary
Allow users already logged in to link a new social account (Telegram, Google) using their existing auth token. The token is passed in the OAuth `state` parameter, and backend extracts it to find and link to the existing user instead of creating a new account.

## Affected Endpoints

### 1. Google OAuth with Linking
`GET /api/v3/GoogleAccount/GetAuthUrl`
`POST /api/v3/GoogleAccount/Callback`

**Auth:** No authentication required (token passed in state).

**Linking Flow:**

**Step 1: Get Auth URL with Token**
```
GET /api/v3/GoogleAccount/GetAuthUrl?PartnerId=123&DeviceType=Web&DeviceFingerprint=abc123&state={existingUserToken}
```

**Step 2: OAuth Callback**
`POST /api/v3/GoogleAccount/Callback`

**Payload:**
```json
{
  "code": "string (OAuth code from Google)",
  "state": "string (existing user token)",
  "partnerId": 123,
  "deviceType": "Web",
  "deviceFingerprint": "string"
}
```

**Backend Logic:**
1. Extract token from `state` parameter
2. Find user by token
3. If found → Link Google account to existing user via `ExternalIdentity` table
4. If not found (token invalid/expired) → Return error (NOT proceed with registration)

**Response (200 OK):**
```json
{
  "data": {
    "token": "string (existing token, not new)",
    "refreshToken": "string",
    "clientId": 12345,
    "userName": "string",
    "email": "string",
    "externalId": "user@example.com",
    "linked": true  // Indicates successful linking
  },
  "success": true,
  "message": "Google account linked successfully",
  "errors": null
}
```

**Error Response (401 Unauthorized):**
```json
{
  "data": null,
  "success": false,
  "message": "Invalid or expired token",
  "errors": ["Token not found or expired"]
}
```

---

### 2. Telegram Hash Auth with Linking
`POST /api/v3/TelegramAccount/HashAuth`

**Auth:** Token passed in hash/state (depends on implementation).

**Payload:**
```json
{
  "hash": "string (Telegram WebApp initData hash)",
  "state": "string (existing user token)",
  "partnerId": 123,
  "deviceType": "Web",
  "deviceFingerprint": "string"
}
```

**Backend Logic:**
1. Extract token from `state` or hash data
2. Find user by token
3. If found → Link Telegram to existing user via `ExternalIdentity` table
4. If not found → Return error

**Response (200 OK):**
```json
{
  "data": {
    "token": "string (existing token, not new)",
    "refreshToken": "string",
    "clientId": 12345,
    "userName": "string",
    "email": "string",
    "externalId": "TG123456789",
    "linked": true
  },
  "success": true,
  "message": "Telegram account linked successfully",
  "errors": null
}
```

**Error Response (401 Unauthorized):**
```json
{
  "data": null,
  "success": false,
  "message": "Invalid or expired token",
  "errors": ["Token not found or expired"]
}
```

---

## Testing Advice

### CT-522 Specific Requirements

#### 1. Google Linking Flow

**Test Case 1: Link Google to Existing Account (Valid Token)**
- User is logged in with valid token
- User initiates "Link Google" flow
- Frontend passes current token in `state` when calling GetAuthUrl
- Complete Google OAuth flow
- Expected: Google account linked to existing user (not new account created)
- Verify DB: `ExternalIdentity` row exists with correct ExternalId = email
- Verify Response: User data matches existing user, not a new user

**Test Case 2: Link Google with Expired Token**
- User has expired token
- User initiates "Link Google" flow
- Frontend passes expired token in `state`
- Complete Google OAuth flow
- Expected: Error response (401 Unauthorized), NO new account created
- Verify DB: No new user created
- Verify Response: "Invalid or expired token" error

**Test Case 3: Link Google with Invalid Token**
- Use completely invalid token (malformed)
- Expected: Error response (401 Unauthorized)
- Verify DB: No new user created

**Test Case 4: Link Same Google to Same Account**
- User already has Google linked
- User tries to link same Google account again
- Expected: Either success (idempotent) or error (already linked)
- Verify DB: No duplicate `ExternalIdentity` entries

**Test Case 5: Link Google to Account with Different Email**
- User's profile email is `user1@example.com`
- User's Google email is `user2@gmail.com`
- Link Google to account
- Expected: Success - Google linked, profile email unchanged
- Verify DB: `ExternalIdentity.ExternalId = user2@gmail.com` for this user

#### 2. Telegram Linking Flow

**Test Case 6: Link Telegram to Existing Account (Valid Token)**
- User is logged in with valid token
- User initiates "Link Telegram" flow
- Frontend passes current token in `state` when calling HashAuth
- Complete Telegram auth flow
- Expected: Telegram account linked to existing user
- Verify DB: `ExternalIdentity` row exists with ExternalId = "TG{id}"
- Verify Response: User data matches existing user

**Test Case 7: Link Telegram with Expired Token**
- User has expired token
- User initiates "Link Telegram" flow
- Expected: Error response (401 Unauthorized), NO new account created
- Verify DB: No new user created

**Test Case 8: Link Same Telegram to Same Account**
- User already has Telegram linked
- User tries to link same Telegram account again
- Expected: Success (idempotent) or error (already linked)
- Verify DB: No duplicate `ExternalIdentity` entries

#### 3. Multiple Social Links

**Test Case 9: Link Google + Telegram to Same Account**
- User has existing account (email/password or other method)
- User links Google
- Verify: Google linked successfully
- User links Telegram
- Verify: Telegram linked to same account
- Verify DB: Two `ExternalIdentity` entries for same ClientId
- Test: Login via Google → works
- Test: Login via Telegram → works (both map to same user)

**Test Case 10: Link Google, Then Link Another Google**
- User links Google account (user1@gmail.com)
- User tries to link different Google account (user2@gmail.com)
- Expected: Either error (only one Google per account) or replace
- Clarify expected behavior with backend team

#### 4. State Parameter Variations

**Test Case 11: Empty State Parameter**
- Call OAuth callback with empty `state`
- Expected: Proceed with normal registration flow (not linking)
- Verify: New user created if OAuth is valid

**Test Case 12: Malformed State Parameter**
- Call OAuth callback with invalid JSON or malformed `state`
- Expected: Error response, no user creation

**Test Case 13: State Contains Non-Token Data**
- Call OAuth callback with random string in `state`
- Expected: Error response, no user creation

#### 5. Integration with CT-709

**Test Case 14: Linking After CT-709 Migration**
- Ensure linking flow works with new `ExternalIdentity.ExternalId` logic
- Link Google → Verify `ExternalId` = email (lowercase)
- Link Telegram → Verify `ExternalId` = "TG{id}"
- Test login via both methods after linking

**Test Case 15: Unlink and Re-Link**
- Link Google to account
- Unlink Google (if endpoint exists)
- Re-link same Google
- Expected: Works correctly, `ExternalId` populated correctly

#### 6. Error Handling

**Test Case 16: Token Not Found**
- Use valid token format but from non-existent user
- Expected: Error response, no user creation

**Test Case 17: User Deleted But Token Exists**
- User is deleted, but token format is valid
- Expected: Error response, no new user creation

**Test Case 18: OAuth Failure After Linking**
- Token is valid, but Google OAuth fails (invalid code, etc.)
- Expected: Error response, no side effects on user account

#### 7. Session Management

**Test Case 19: Token Continuity**
- Link Google using valid token
- Verify: Response contains same/existing token (not new)
- Verify: Session remains active, user stays logged in

**Test Case 20: Refresh Token After Linking**
- Link Google to account
- Use refresh token to get new access token
- Expected: Works correctly, refresh token still valid

---

## Database Changes

### ExternalIdentity Table

**Insertion on Linking:**
- When linking successful, insert new row in `ExternalIdentity`:
  - `ExternalId`: email (Google) or "TG{id}" (Telegram)
  - `RegistrationSourceId`: Google or Telegram
  - `ClientId`: Existing user's ClientId
- Uniqueness constraint on `(ExternalId, RegistrationSourceId, PartnerId)` enforced

**Note:**
- Existing `ExternalIdentity` table is reused (same as CT-709)
- No new tables created

---

## Acceptance Criteria

- ✅ Backend accepts token via `state` parameter during social login
- ✅ Existing user matched correctly and social account linked
- ✅ If user not found (invalid/expired token) → Return error (not registration)
- ✅ Google account linking creates correct `ExternalIdentity` entry
- ✅ Telegram account linking creates correct `ExternalIdentity` entry
- ✅ Multiple social accounts can be linked to same user
- ✅ Existing token remains valid after linking (session continuity)
- ✅ Error handling for expired/invalid tokens
- ✅ No new user creation when linking fails
- ✅ Integration with CT-709's `ExternalIdentity` logic

---

## Related JIRA Info
- **Ticket:** CT-522 - "[BE] Linking Social Account Using Existing User Token"
- **Status:** Ready for testing
- **Priority:** High
- **Dependencies:** CT-709 (ExternalIdentity refactor)

## Notes
- Reuses existing `ExternalIdentity` table from CT-709
- If token is expired or invalid, backend returns error instead of proceeding with registration
- Frontend must include current user token in OAuth `state` parameter
- Response returns existing token (not new) to maintain session continuity
- Linking flow is opt-in via state parameter; normal registration/login flow unchanged
- Uniqueness constraints still apply (same social cannot be linked by different users in same partner)
