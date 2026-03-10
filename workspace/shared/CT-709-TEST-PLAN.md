# Test Plan: CT-709 — [BE] Refactor Login & Registration

**Ticket:** CT-709 - [BE] Refactor Login & Registration
**Status:** Ready for testing
**Type:** Backend-only (API testing)
**Estimated Time:** 6 hours
**Backend MR:** https://git.dolore.cc/platform/platform-be/-/merge_requests/103

---

## 📋 Executive Summary (TL;DR)

**What Changed:** OAuth login now uses `ExternalIdentity.ExternalId` instead of email/user_id for stable authentication.

**Key Flows:**
- Google login via OneTapAuth → ExternalId = email (lowercase)
- Telegram login via HashAuth → ExternalId = "TG{telegramUserId}"
- Auto-backfill for pre-migration users on first login
- Cross-partner support (same social can be used across different partners)

**Critical Edge Cases:**
- Email change scenario: Login still works even if email changes (ExternalId is stable)
- Case-insensitive Google lookup: USER@EXAMPLE.COM = user@example.com
- Uniqueness per partner: Same Google can be used in Partner 1 AND Partner 2
- Duplicate prevention: Same Google cannot be used by two users in same partner

**Migration Validation:**
- All existing Google/Telegram users get `ExternalId` auto-populated on first login
- No DB access needed — verify via API responses (`data.externalId` field)

---

## 🎯 Test Strategy

### Black-Box Techniques Applied:
- **Equivalence Partitioning:** User states (pre/post-migration, existing/new, same/different partners)
- **Boundary Value Analysis:** Edge cases around uniqueness, case sensitivity, email changes
- **State Transition Testing:** Pre-migration → First login (backfill) → Post-migration state
- **Error Guessing:** Duplicate links, orphaned records, data inconsistencies

### Test Types:
- **Smoke Tests:** Verify critical login flows work immediately after deployment
- **Functional Tests:** Detailed validation of all OAuth scenarios
- **Migration Tests:** Verify backfill happens via API responses (no DB access)
- **Regression Tests:** Ensure no impact on other login methods

### Tool Availability Validation:
- ✅ API calls via curl/Playwright APIRequestContext
- ✅ Response validation (JSON structure, fields, values)
- ✅ Web search for data generation strategies
- ✅ Helper script creation for test data
- ❌ Database access (not available) → Migration verified via API responses only

---

## 📝 Test Cases

### Category 1: Google Login Flow

#### TC-G001: Existing Google User (Post-Migration)
**Priority:** P0 (Critical)
**Preconditions:** User registered via Google with ExternalId populated

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` with valid Google JWT | Returns 200 OK |
| 2 | Verify response structure | `data.token` exists, `data.externalId` exists |
| 3 | Verify `data.externalId` format | Format: email (lowercase) |
| 4 | Verify authentication | Login successful, token valid |

**Evidence:** Save full JSON response showing `data.externalId` populated

---

#### TC-G002: Existing Google User (Pre-Migration) - Backfill Verification
**Priority:** P0 (Critical)
**Preconditions:** User registered via Google BEFORE deployment (no ExternalId in DB)
**Note:** Cannot verify pre-state via DB, but can verify POST-response backfill

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` | Returns 200 OK (fallback via email) |
| 2 | Verify response contains `data.externalId` | `externalId` now present (was not present before) |
| 3 | Verify `data.externalId` format | Format: email (lowercase) |
| 4 | Login again with same credentials | Returns 200 OK (now uses ExternalId lookup) |

**Evidence:** First response showing `data.externalId` populated (backfill occurred)

---

#### TC-G003: New Google Registration
**Priority:** P0 (Critical)
**Preconditions:** New Google account (never used before)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` with new Google JWT | Returns 200 OK |
| 2 | Verify response contains new user data | `data.clientId` present, `data.token` valid |
| 3 | Verify `data.externalId` | `externalId` = email (lowercase) |
| 4 | Verify uniqueness via error handling | Second registration with same Google email in same partner should fail |

**Evidence:** Response JSON showing new user with `externalId` populated

---

#### TC-G004: Google Email Change Scenario (Critical Edge Case)
**Priority:** P0 (Critical)
**Preconditions:** User has Google linked, email = old@example.com

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login via Google OneTapAuth | Returns 200 OK, `data.externalId` = old@example.com |
| 2 | User changes email in profile to new@example.com | Email updated (via profile API) |
| 3 | Login again via Google OneTapAuth (still using old@example.com JWT) | Returns 200 OK! **Key: Login still works** |
| 4 | Verify `data.externalId` in response | Still shows old@example.com (unchanged) |
| 5 | Verify profile email vs externalId | Profile email = new@example.com, ExternalId = old@example.com |

**Rationale:** Proves that ExternalId provides stability even when user changes email elsewhere.

**Evidence:** Responses showing `data.externalId` unchanged despite email change

---

#### TC-G005: Google Email Case-Insensitive Lookup
**Priority:** P1 (High)
**Preconditions:** User registered with Google email = User@Example.COM

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` with JWT for User@Example.COM (uppercase) | Returns 200 OK |
| 2 | Verify `data.externalId` | Shows "user@example.com" (lowercase) |
| 3 | Login again with JWT for user@example.com (lowercase) | Returns 200 OK |
| 4 | Verify same user (clientId) | `data.clientId` identical in both logins |

**Rationale:** Proves case-insensitive lookup but lowercase storage.

**Evidence:** Two responses showing same user, lowercase ExternalId

---

### Category 2: Telegram Login Flow

#### TC-TG001: Existing Telegram User (Post-Migration)
**Priority:** P0 (Critical)
**Preconditions:** User registered via Telegram with ExternalId = "TG123456789"

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/TelegramAccount/HashAuth` with valid Telegram hash | Returns 200 OK |
| 2 | Verify response structure | `data.token` exists, `data.externalId` exists |
| 3 | Verify `data.externalId` format | Format: "TG{telegramUserId}" |
| 4 | Verify authentication | Login successful |

**Evidence:** Save full JSON response showing `data.externalId` populated

---

#### TC-TG002: Existing Telegram User (Pre-Migration) - Backfill Verification
**Priority:** P0 (Critical)
**Preconditions:** User registered via Telegram BEFORE deployment (UserName = "TG123456789", no ExternalId)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/TelegramAccount/HashAuth` | Returns 200 OK (fallback via UserName) |
| 2 | Verify response contains `data.externalId` | `externalId` now present |
| 3 | Verify `data.externalId` format | Format: "TG123456789" |
| 4 | Login again with same credentials | Returns 200 OK (now uses ExternalId lookup) |

**Evidence:** First response showing `data.externalId` populated (backfill occurred)

---

#### TC-TG003: New Telegram Registration
**Priority:** P0 (Critical)
**Preconditions:** New Telegram account (ID = 999999999)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/TelegramAccount/HashAuth` | Returns 200 OK |
| 2 | Verify response contains new user data | `data.clientId` present, `data.token` valid |
| 3 | Verify `data.externalId` | `externalId` = "TG999999999" |
| 4 | Verify uniqueness via error handling | Second registration with same TG ID in same partner should fail |

**Evidence:** Response JSON showing new user with `externalId` populated

---

### Category 3: Linking Social to Existing Account

#### TC-L001: Link Google to Existing Account
**Priority:** P1 (High)
**Preconditions:** User has existing email/password account

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login with email/password | Returns 200 OK |
| 2 | Link Google account via API | Link successful |
| 3 | Login via Google OneTapAuth | Returns 200 OK |
| 4 | Verify `data.externalId` | `externalId` = google@email.com (NOT username) |

**Evidence:** Response showing `data.externalId` = email format

---

#### TC-L002: Link Telegram to Existing Account
**Priority:** P1 (High)
**Preconditions:** User has existing email/password account

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login with email/password | Returns 200 OK |
| 2 | Link Telegram account via API | Link successful |
| 3 | Login via Telegram HashAuth | Returns 200 OK |
| 4 | Verify `data.externalId` | `externalId` = "TG123456789" |

**Evidence:** Response showing `data.externalId` = TG format

---

### Category 4: Uniqueness & Edge Cases

#### TC-U001: Same Google Email Across Different Partners
**Priority:** P1 (High)
**Preconditions:** PartnerId = 1, PartnerId = 2

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` with PartnerId=1 | Returns 200 OK, `data.clientId` = 111 |
| 2 | `POST /api/v3/GoogleAccount/OneTapAuth` with same Google email, PartnerId=2 | Returns 200 OK, `data.clientId` = 222 (different user) |
| 3 | Verify `data.externalId` in both | Same `externalId` in both responses (email) |

**Rationale:** Proves uniqueness is per Partner, not global.

**Evidence:** Two responses with same `externalId` but different `clientId`

---

#### TC-U002: Prevent Duplicate Google Link in Same Partner
**Priority:** P1 (High)
**Preconditions:** User A already linked Google in Partner 1 (clientId = 111)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | User B tries to link same Google in Partner 1 | Returns 4xx error (email already linked) |
| 2 | Verify error message | Contains "already linked" or similar |

**Rationale:** Proves uniqueness enforced within same partner.

**Evidence:** Error response, no new user created

---

#### TC-U003: Same Telegram ID Across Different Partners
**Priority:** P1 (High)
**Preconditions:** PartnerId = 1, PartnerId = 2

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/TelegramAccount/HashAuth` with PartnerId=1 | Returns 200 OK, `data.clientId` = 111 |
| 2 | `POST /api/v3/TelegramAccount/HashAuth` with same TG ID, PartnerId=2 | Returns 200 OK, `data.clientId` = 222 (different user) |
| 3 | Verify `data.externalId` in both | Same `externalId` in both responses (TG format) |

**Evidence:** Two responses with same `externalId` but different `clientId`

---

#### TC-U004: Prevent Duplicate Telegram Link in Same Partner
**Priority:** P1 (High)
**Preconditions:** User A already linked Telegram in Partner 1 (clientId = 111)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | User B tries to link same Telegram in Partner 1 | Returns 4xx error (TG ID already linked) |
| 2 | Verify error message | Contains "already linked" or similar |

**Evidence:** Error response, no new user created

---

### Category 5: Migration Verification (Via API Responses Only)

#### TC-M001: Verify Backfill Happens on First Login (Google)
**Priority:** P0 (Critical)
**Preconditions:** Identify pre-migration Google user (no ExternalId previously)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/GoogleAccount/OneTapAuth` with pre-migration user | Returns 200 OK |
| 2 | Verify `data.externalId` present | `externalId` populated with email |
| 3 | Login again with same credentials | Returns 200 OK |
| 4 | Verify `data.externalId` unchanged | Same `externalId` as before |

**Evidence:** First response shows `data.externalId` now present (proves backfill)

---

#### TC-M002: Verify Backfill Happens on First Login (Telegram)
**Priority:** P0 (Critical)
**Preconditions:** Identify pre-migration Telegram user

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/TelegramAccount/HashAuth` with pre-migration user | Returns 200 OK |
| 2 | Verify `data.externalId` present | `externalId` populated with "TG{id}" |
| 3 | Login again with same credentials | Returns 200 OK |
| 4 | Verify `data.externalId` unchanged | Same `externalId` as before |

**Evidence:** First response shows `data.externalId` now present (proves backfill)

---

### Category 6: Regression Tests

#### TC-R001: Traditional Email/Password Login Unaffected
**Priority:** P0 (Critical)
**Preconditions:** User with email/password credentials

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/Account/Login` with email/password | Returns 200 OK |
| 2 | Verify response contains token | Token valid, user authenticated |
| 3 | Compare with pre-deployment behavior | No difference |

**Rationale:** Ensures OAuth changes don't break traditional login.

**Evidence:** Login response

---

#### TC-R002: OTP Login Unaffected (If Exists)
**Priority:** P1 (High)
**Preconditions:** User with OTP enabled

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/OTP/Request` | OTP sent successfully |
| 2 | `POST /api/v3/OTP/Verify` | Returns 200 OK |
| 3 | Verify session created | Session valid |

**Evidence:** OTP flow responses

---

#### TC-R003: Token Refresh Flow Unaffected
**Priority:** P1 (High)
**Preconditions:** Valid refresh token from Google/Telegram login

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | `POST /api/v3/Account/RefreshToken` | Returns 200 OK |
| 2 | Verify new access token | Token valid, different from previous |
| 3 | Verify session extends | Session still valid |

**Evidence:** Refresh token response

---

#### TC-R004: Session Persistence After OAuth Login
**Priority:** P1 (High)
**Preconditions:** User logged in via Google/Telegram

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login via Google/Telegram OAuth | Returns 200 OK |
| 2 | Make authenticated API call (e.g., `/api/v3/Account/Profile`) | Call succeeds |
| 3 | Wait 10 minutes, make another call | Call succeeds (session persisted) |
| 4 | Verify token not expired | Token valid |

**Evidence:** API call responses showing successful authentication

---

## 🛠️ Test Data Generation Strategy

### Autonomous Data Generation (No Dependencies)

**Telegram WebApp Hash Generation:**
```bash
# Research shows we can generate valid test hashes using:
# - HMAC-SHA256 with bot token
# - Telegram WebApp init data structure

# Helper script will be created:
~/.openclaw/workspace-qa-agent/scripts/telegram-hash-generator.py
```

**Google OAuth JWT Mocking:**
```bash
# Research shows multiple approaches:
# - Use jwt.io to create test JWT tokens
# - Use Node.js jwt library to generate test tokens
# - Mock the endpoint responses directly

# Helper script will be created:
~/.openclaw/workspace-qa-agent/scripts/google-jwt-generator.js
```

### Test Account Strategy:
1. Use existing pre-migration users (identify via Backend team)
2. Generate new test users via OAuth flows (registration)
3. Create mock JWT tokens for Google using jwt.io or library
4. Generate Telegram test hashes using HMAC-SHA256 script

---

## 🚀 Test Execution Approach

### Phase 1: Pre-Deployment Preparation (1 hour)
- [ ] Create helper scripts for test data generation
- [ ] Identify 2-3 pre-migration users (Google + Telegram)
- [ ] Prepare mock JWT tokens for Google
- [ ] Generate Telegram test hashes
- [ ] Document current API response structure (baseline)

### Phase 2: Smoke Tests (30 minutes) - Immediately After Deployment
- [ ] TC-G001: Existing Google login (quick validation)
- [ ] TC-TG001: Existing Telegram login (quick validation)
- [ ] TC-G003: New Google registration
- [ ] TC-TG003: New Telegram registration
- [ ] TC-R001: Email/password login (regression check)

### Phase 3: Functional Tests (2 hours)
- [ ] Run all Google flow tests (TC-G002, TC-G004, TC-G005)
- [ ] Run all Telegram flow tests (TC-TG002)
- [ ] Run linking tests (TC-L001, TC-L002)
- [ ] Run uniqueness tests (TC-U001 to TC-U004)

### Phase 4: Migration Verification (1 hour)
- [ ] TC-M001: Google backfill on first login (via API response)
- [ ] TC-M002: Telegram backfill on first login (via API response)
- [ ] Document backfill behavior (before/after response comparison)

### Phase 5: Regression Tests (1 hour)
- [ ] TC-R002: OTP login (if applicable)
- [ ] TC-R003: Token refresh
- [ ] TC-R004: Session persistence
- [ ] Verify no performance degradation (check response times)

### Phase 6: Edge Case Validation (30 minutes)
- [ ] TC-G004: Email change scenario (stability test)
- [ ] TC-G005: Case-insensitive lookup
- [ ] Cross-partner uniqueness tests

---

## 📊 Expected Test Results Summary

| Category | Total Tests | Expected Pass | Expected Fail | Notes |
|----------|-------------|---------------|---------------|-------|
| Google Login | 5 | 5 | 0 | |
| Telegram Login | 3 | 3 | 0 | |
| Linking | 2 | 2 | 0 | |
| Uniqueness | 4 | 4 | 0 | |
| Migration | 2 | 2 | 0 | Verified via API only |
| Regression | 4 | 4 | 0 | |
| **Total** | **20** | **20** | **0** | Reduced from 22 (merged DB checks) |

---

## 📋 Deliverables

### After Testing:
1. **Test Report** (`results.json`) — Structured JSON with all test results
2. **Slack Message** (`slack-message.txt`) — Concise Pass/Fail summary
3. **Jira Comment** (`jira-comment.txt`) — ISTQB-format detailed report
4. **Evidence Files** — All API responses (JSON), screenshots, helper scripts
5. **Helper Scripts** — Telegram hash generator, Google JWT generator

### Output Location:
```
~/.openclaw/workspace/shared/test-results/CT-709/
├── slack-message.txt
├── jira-comment.txt
├── results.json
├── evidence/
│   ├── google-login-response-001.json
│   ├── telegram-login-response-001.json
│   └── ...
└── scripts/
    ├── telegram-hash-generator.py
    └── google-jwt-generator.js
```

---

## 🚨 Potential Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Backfill logic fails silently | Medium | High | Verify via API responses (externalId presence) |
| Uniqueness constraint blocks legitimate cross-partner logins | Low | Medium | Test cross-partner scenario thoroughly (TC-U001, TC-U003) |
| Email change scenario breaks login | Low | High | Test TC-G004 explicitly (critical edge case) |
| Performance degradation due to new lookup logic | Low | Medium | Monitor API response times, log >1s responses |
| Migration not applied correctly | Low | High | Verify with pre-migration users immediately after deploy |

---

## 🎓 Acceptance Criteria Verification

| AC | Status | Test Case(s) |
|----|--------|--------------|
| `ExternalIdentity.ExternalId` utilized correctly | ✅ TC-G003, TC-TG003, TC-M001, TC-M002 |
| Telegram login uses `ExternalId` as primary lookup | ✅ TC-TG001, TC-TG002 |
| Google login uses `ExternalId` (email) as primary lookup | ✅ TC-G001, TC-G002 |
| First login creates `ExternalIdentity` entry automatically | ✅ TC-G003, TC-TG003 |
| Pre-migration users get `ExternalId` backfilled | ✅ TC-G002, TC-TG002, TC-M001, TC-M002 |
| DB migration populates `ExternalId` (verified via API) | ✅ TC-M001, TC-M002 |
| Uniqueness enforced per (ExternalId, RegistrationSource, PartnerId) | ✅ TC-U001, TC-U002, TC-U003, TC-U004 |
| Same user can link same socials in different partners | ✅ TC-U001, TC-U003 |
| Different users cannot use same social in same partner | ✅ TC-U002, TC-U004 |
| Old login-by-email-for-socials removed as primary | ✅ TC-G001, TC-TG001 (prove ExternalId used) |
| Email changes don't break OAuth login | ✅ TC-G004 (Critical!) |
| No regression on other login methods | ✅ TC-R001, TC-R002, TC-R003, TC-R004 |

---

## 📝 Notes

- **No UI tests required** — This is Backend-only testing
- **All tests executed via API** — curl or Playwright APIRequestContext
- **No DB access needed** — Migration verified via `data.externalId` in responses
- **Helper scripts to be created** — For test data generation
- **Coordinate with Backend team** — Identify 2-3 pre-migration users
- **Monitor production logs** — After deployment, watch for OAuth-related errors

---

**Prepared by:** QA Agent (Clawver 🐞)
**Date:** 2026-03-10 (Updated after self-review)
**Ticket:** CT-709
**Status:** Ready for Execution
