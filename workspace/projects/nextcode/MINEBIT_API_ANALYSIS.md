# Minebit Casino - Backend API v3 Analysis

## 📋 Swagger Documentation

**Base URLs:**
- **Prod:** `https://websitewebapi.prod.sofon.one`
- **QA:** `https://websitewebapi.qa.sofon.one`
- **Dev:** `https://websitewebapi.dev.sofon.one`

**Swagger UI:**
- Prod: `https://websitewebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3`
- QA: `https://websitewebapi.qa.sofon.one/swagger/index.html?urls.primaryName=API+v3`
- Dev: `https://websitewebapi.dev.sofon.one/swagger/index.html?urls.primaryName=API+v3`

**OpenAPI JSON:**
- `/swagger/v3/swagger.json`

---

## 🎯 API Endpoint Groups (Categories)

### 1. **Auth** - Authentication
**Endpoints:**
- `POST /{partnerId}/api/v3/Auth/otp/request` - Request OTP code
- `POST /{partnerId}/api/v3/Auth/otp/verify` - Verify OTP code

**Status:** Public (no auth required)

**Purpose:** One-time password authentication flow

---

### 2. **Bet** - Betting History
**Endpoints:**
- `POST /{partnerId}/api/v3/Bet/GetCasinoBets` - Get casino bet history
- `POST /{partnerId}/api/v3/Bet/GetSportBookBets` - Get sportsbook bet history

**Status:** Requires authentication

**Purpose:** Retrieve user's betting history for casino games and sports betting

---

### 3. **Bonus** - Bonus System
**Endpoints (16 total):**
- `POST /{partnerId}/api/v3/Bonus/GetPromotions` - Get available promotions
- `POST /{partnerId}/api/v3/Bonus/GetBonusStatusesEnum` - Get bonus status enum
- `POST /{partnerId}/api/v3/Bonus/ActivatePromoCode` - Activate promo code
- `POST /{partnerId}/api/v3/Bonus/SaveSelectedDepositBonus` - Select deposit bonus
- `POST /{partnerId}/api/v3/Bonus/CancelSelectedDepositBonus` - Cancel selected bonus
- `POST /{partnerId}/api/v3/Bonus/GetAvailableForDepositBonuses` - Get bonuses for deposit
- `POST /{partnerId}/api/v3/Bonus/GetBonuses` - Get all bonuses
- `POST /{partnerId}/api/v3/Bonus/GetActiveBonuses` - Get active bonuses
- `POST /{partnerId}/api/v3/Bonus/GetEligibleBonuses` - Get eligible bonuses
- `GET /{partnerId}/api/v3/Bonus/GetAvailableDepositBonuses` - Get available deposit bonuses
- `GET /{partnerId}/api/v3/Bonus/GetBonusDetails/{bonusId}` - Get bonus details
- `POST /{partnerId}/api/v3/Bonus/ActivateEligibleBonus/{bonusId}` - Activate eligible bonus
- `POST /{partnerId}/api/v3/Bonus/ReplaceActiveBonus/{bonusId}` - Replace active bonus
- `POST /{partnerId}/api/v3/Bonus/ClaimBonus/{clientBonusId}` - Claim bonus
- `POST /{partnerId}/api/v3/Bonus/GetSportClientBonuses` - Get sport client bonuses
- `GET /{partnerId}/api/v3/Bonus/GetClientFreeBetBalance/{clientId}/freeBet-balance` - Get free bet balance

**Status:** Requires authentication

**Purpose:** Complete bonus management system - promotions, activation, claiming, wagering

---

### 4. **CalendarBonus** - Daily Bonus Calendar
**Endpoints:**
- `GET /{partnerId}/api/v3/CalendarBonus/GetByClient/{clientId}` - Get calendar bonus by client
- `POST /{partnerId}/api/v3/CalendarBonus/Claim` - Claim calendar bonus

**Status:** Requires authentication

**Purpose:** Daily login bonus calendar system

---

### 5. **Chatwoot** - Customer Support Integration
**Endpoints:**
- `GET /api/v3/Chatwoot/GetHmac` - Get HMAC for Chatwoot authentication

**Status:** Requires authentication

**Purpose:** Customer support chat integration

---

### 6. **Client** - User Management (CRITICAL - 38 endpoints!)
**Endpoints:**
**Authentication:**
- `POST /{partnerId}/api/v3/Client/Login` - Login
- `POST /{partnerId}/api/v3/Client/VerifyTwoFactorLogin` - Verify 2FA
- `POST /{partnerId}/api/v3/Client/VerifyTwoFactorBackupLogin` - Verify 2FA backup
- `POST /{partnerId}/api/v3/Client/Register` - Register new user
- `POST /{partnerId}/api/v3/Client/SignOn` - Sign on
- `POST /{partnerId}/api/v3/Client/LogoutClient` - Logout
- `POST /{partnerId}/api/v3/Client/QuickSmsRegistration` - Quick SMS registration

**Profile Management:**
- `GET /{partnerId}/api/v3/Client/GetClientByToken` - Get client by token
- `POST /{partnerId}/api/v3/Client/ChangeDetails` - Change client details
- `POST /{partnerId}/api/v3/Client/ChangeClientPassword` - Change password
- `POST /{partnerId}/api/v3/Client/UploadImage` - Upload profile image

**Balance:**
- `GET /{partnerId}/api/v3/Client/GetClientBalance` - Get balance
- `POST /{partnerId}/api/v3/Client/GetClientBalance` - Get balance (POST version)

**Password Recovery:**
- `POST /{partnerId}/api/v3/Client/SendRecoveryToken` - Send recovery token
- `POST /{partnerId}/api/v3/Client/RecoverPassword` - Recover password
- `POST /{partnerId}/api/v3/Client/ValidateRecoveryToken` - Validate recovery token
- `POST /{partnerId}/api/v3/Client/SendRecoveryTokenV2` - Send recovery token v2
- `POST /{partnerId}/api/v3/Client/RecoverPasswordV2` - Recover password v2
- `POST /{partnerId}/api/v3/Client/ValidateRecoveryTokenAsyncV2` - Validate recovery token v2

**Verification:**
- `POST /{partnerId}/api/v3/Client/SendVerificationCodeToPhone` - Send SMS verification
- `POST /{partnerId}/api/v3/Client/VerifyClientPhone` - Verify phone
- `POST /{partnerId}/api/v3/Client/SendVerificationCodeToEmail` - Send email verification
- `POST /{partnerId}/api/v3/Client/VerifyClientEmail` - Verify email

**KYC (Know Your Customer):**
- `POST /{partnerId}/api/v3/Client/GetClientIdentityModels` - Get identity models
- `POST /{partnerId}/api/v3/Client/GetKycLevels` - Get KYC levels
- `POST /{partnerId}/api/v3/Client/GetPartnerKycLevels` - Get partner KYC levels
- `POST /{partnerId}/api/v3/Client/SetPoliticallyExposedPerson` - Set PEP status
- `GET /{partnerId}/api/v3/Client/GetKycAidFormUrl` - Get KYC Aid form URL

**Client Info:**
- `POST /{partnerId}/api/v3/Client/GetClientStatuses` - Get client statuses
- `POST /{partnerId}/api/v3/Client/GetClientLimits` - Get client limits
- `POST /{partnerId}/api/v3/Client/GetClientAccounts` - Get client accounts
- `POST /{partnerId}/api/v3/Client/GetClientLogins` - Get client login history

**Validation:**
- `POST /{partnerId}/api/v3/Client/ClientUserNameExists` - Check username exists
- `GET /{partnerId}/api/v3/Client/ClientUserNameExists` - Check username exists (GET)
- `POST /{partnerId}/api/v3/Client/ClientEmailExists` - Check email exists
- `GET /{partnerId}/api/v3/Client/ClientEmailExists` - Check email exists (GET)

**Bonus Management:**
- `PATCH /{partnerId}/api/v3/Client/CancelClientBonus/{clientBonusId}` - Cancel client bonus

**Social:**
- `DELETE /{partnerId}/api/v3/Client/UnlinkSocialAccount` - Unlink social account

**Status:** Mixed - some public (Register, Login, EmailExists, UserNameExists), most require authentication

**Purpose:** Complete user management system - registration, login, profile, KYC, verification

---

### 7. **DepositStreak** - Deposit Streak Bonus
**Endpoints:**
- `GET /{partnerId}/api/v3/DepositStreak/GetDepositStreak` - Get deposit streak status

**Status:** Requires authentication

**Purpose:** Track consecutive deposit bonuses

---

### 8. **DirectPayment** - Direct Payment Processing
**Endpoints:**
- `POST /{partnerId}/api/v3/DirectPayment/CreateWithdrawByCreditCardNumber` - Withdraw to credit card
- `POST /{partnerId}/api/v3/DirectPayment/CreateWithdrawByAccountNumber` - Withdraw to bank account

**Status:** Requires authentication

**Purpose:** Direct withdrawal processing

---

### 9. **GoogleAccount** - Google OAuth
**Endpoints:**
- `GET /api/v3/GoogleAccount/Callback` - OAuth callback
- `POST /api/v3/GoogleAccount/OneTapAuth` - One-tap authentication
- `GET /api/v3/GoogleAccount/GetAuthUrl` - Get Google OAuth URL

**Status:** Public (OAuth flow)

**Purpose:** Google account authentication

---

### 10. **Main** - General Utilities
**Endpoints:**
- `POST /{partnerId}/api/v3/Main/GetRegions` - Get regions list
- `GET /{partnerId}/api/v3/Main/GetBetStates` - Get bet states enum
- `POST /{partnerId}/api/v3/Main/GetKYCDocumentStatesEnum` - Get KYC document states
- `POST /{partnerId}/api/v3/Main/GetOperationTypes` - Get operation types
- `POST /{partnerId}/api/v3/Main/GetKYCDocumentTypesEnum` - Get KYC document types
- `POST /{partnerId}/api/v3/Main/GetKYCFieldTypesEnum` - Get KYC field types
- `POST /{partnerId}/api/v3/Main/GetKycLevelStatesEnum` - Get KYC level states

**Referral System:**
- `POST /{partnerId}/api/v3/Main/GetReferralLink` - Get referral link
- `POST /{partnerId}/api/v3/Main/InviteFriend` - Invite friend
- `POST /{partnerId}/api/v3/Main/GetAffiliateClientsOfManager` - Get affiliate clients

**History:**
- `POST /{partnerId}/api/v3/Main/GetBetsHistory` - Get bets history
- `POST /{partnerId}/api/v3/Main/GetTransactionHistory` - Get transaction history

**Loyalty:**
- `POST /{partnerId}/api/v3/Main/ExchangeComplimentaryPoint` - Exchange loyalty points

**Status:** Mixed - some public (enums), most require authentication

**Purpose:** General utilities, enums, referral system, history, loyalty points

---

### 11. **Payment** - Payment Management
**Endpoints:**
- `GET /{partnerId}/api/v3/Payment/GetPaymentMethodTypesEnum` - Get payment method types
- `GET /{partnerId}/api/v3/Payment/GetPaymentRequestTypes` - Get payment request types
- `GET /{partnerId}/api/v3/Payment/GetPaymentRequests` - Get payment requests
- `GET /{partnerId}/api/v3/Payment/GetAvailablePaymentMethods` - Get available payment methods
- `DELETE /{partnerId}/api/v3/Payment/CancelWithdraw` - Cancel withdrawal
- `GET /{partnerId}/api/v3/Payment/GetClientPaymentStatistics` - Get payment statistics

**Status:** Requires authentication

**Purpose:** Payment method management, withdrawal cancellation, statistics

---

### 12. **PaymentHub** - Payment Hub Integration
**Endpoints:**
- `POST /{partnerId}/api/v3/PaymentHub/Initialize` - Initialize payment hub

**Status:** Requires authentication

**Purpose:** Initialize payment processing system

---

### 13. **Product** - Games & Products (CRITICAL - 18 endpoints!)
**Endpoints:**
**Game Management:**
- `POST /{partnerId}/api/v3/Product/GetGames` - Get games list
- `POST /{partnerId}/api/v3/Product/GetNonAvailableGames` - Get non-available games
- `POST /{partnerId}/api/v3/Product/GetAvailableGamesInCurrentBonus` - Get games available in bonus
- `POST /{partnerId}/api/v3/Product/GetGameCategories` - Get game categories
- `GET /{partnerId}/api/v3/Product/GetGameCategories` - Get game categories (GET)
- `POST /{partnerId}/api/v3/Product/GetCategoryOrder` - Get category order
- `GET /{partnerId}/api/v3/Product/GetCategoryOrder` - Get category order (GET)

**Game Launch:**
- `POST /{partnerId}/api/v3/Product/GetProductUrl` - Get game launch URL
- `POST /{partnerId}/api/v3/Product/CheckProductAvailability` - Check if game is available
- `POST /{partnerId}/api/v3/Product/GetCheckedProductUrl` - Get checked game URL

**Favorites:**
- `POST /{partnerId}/api/v3/Product/AddToFavoriteList` - Add to favorites
- `POST /{partnerId}/api/v3/Product/RemoveClientFavoriteProduct` - Remove from favorites
- `GET /{partnerId}/api/v3/Product/GetClientFavoriteProducts` - Get favorite games

**Jackpots & Winners:**
- `GET /{partnerId}/api/v3/Product/GetJackpotGameData` - Get jackpot data
- `POST /{partnerId}/api/v3/Product/GetJackpotGameData` - Get jackpot data (POST)
- `GET /{partnerId}/api/v3/Product/GetWinners` - Get recent winners
- `POST /{partnerId}/api/v3/Product/GetWinners` - Get recent winners (POST)
- `GET /{partnerId}/api/v3/Product/GetRecentBets` - Get recent bets
- `POST /{partnerId}/api/v3/Product/GetRecentBets` - Get recent bets (POST)

**Utilities:**
- `POST /{partnerId}/api/v3/Product/GetProductTypesEnum` - Get product types

**Status:** Requires authentication

**Purpose:** Complete game lobby system - games list, categories, launch, favorites, jackpots

---

### 14. **Recommendation** - Game Recommendations
**Endpoints:**
- `POST /{partnerId}/api/v3/Recommendation/GetGameRecommendation` - Get game recommendations

**Status:** Requires authentication

**Purpose:** AI-powered game recommendations

---

### 15. **RedirectPayment** - Redirect Payment Flow
**Endpoints:**
- `POST /{partnerId}/api/v3/RedirectPayment/CreateDepositByRedirect` - Create deposit via redirect

**Status:** Requires authentication

**Purpose:** Deposit processing via redirect to payment provider

---

### 16. **TelegramAccount** - Telegram Authentication
**Endpoints:**
- `POST /api/v3/TelegramAccount/HashAuth` - Telegram hash authentication

**Status:** Public (OAuth-like flow)

**Purpose:** Telegram account authentication

---

### 17. **TwoFactorAuth** - Two-Factor Authentication
**Endpoints:** (visible in snapshot but truncated)

**Status:** Requires authentication

**Purpose:** 2FA management

---

## 🔐 Authentication & Headers

### **Authentication Method:**
Based on the user's instructions and Swagger structure:

**Session Token Authentication**
- After registration/login via GraphQL, you receive a `sessionToken`
- This token must be passed in REST API calls

### **Required Headers:**

```http
Authorization: {sessionToken}
Content-Type: application/json
Accept: application/json
website-locale: en
website-origin: https://minebit-casino.prod.sofon.one
x-time-zone-offset: -60
```

**Alternative header names seen in APIs:**
- `Authorization` (most common)
- `X-Session-Token`
- Check Swagger "Authorize" button for exact format

### **Path Parameters:**

All endpoints include `{partnerId}` in the path:
- **Minebit partnerId = 5**
- Example: `/5/api/v3/Client/GetClientBalance`

### **Common Headers for All Requests:**

```http
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Origin: https://minebit-casino.prod.sofon.one
Referer: https://minebit-casino.prod.sofon.one/
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

---

## 🎯 Key Flows for Testing

### **Flow 1: User Registration**
```
1. GraphQL: PlayerRegisterUniversal
   → Returns: sessionToken, userName, id, email
2. REST: Use sessionToken for authenticated requests
```

### **Flow 2: Get User Balance**
```
GET /5/api/v3/Client/GetClientBalance
Headers:
  Authorization: {sessionToken}
  website-locale: en
  website-origin: https://minebit-casino.prod.sofon.one
```

### **Flow 3: Get Games List**
```
POST /5/api/v3/Product/GetGames
Headers:
  Authorization: {sessionToken}
  Content-Type: application/json
Body: {} (or filters)
```

### **Flow 4: Launch a Game**
```
POST /5/api/v3/Product/GetProductUrl
Headers:
  Authorization: {sessionToken}
  Content-Type: application/json
Body: {
  "productId": "game-id",
  "deviceType": "Desktop"
}
```

### **Flow 5: Get Active Bonuses**
```
POST /5/api/v3/Bonus/GetActiveBonuses
Headers:
  Authorization: {sessionToken}
Body: {}
```

### **Flow 6: Create Deposit**
```
POST /5/api/v3/RedirectPayment/CreateDepositByRedirect
Headers:
  Authorization: {sessionToken}
Body: {
  "amount": 100,
  "currency": "USD",
  "paymentMethodId": "method-id"
}
```

### **Flow 7: Get Transaction History**
```
POST /5/api/v3/Main/GetTransactionHistory
Headers:
  Authorization: {sessionToken}
Body: {
  "fromDate": "2026-01-01",
  "toDate": "2026-02-15",
  "pageNumber": 1,
  "pageSize": 20
}
```

---

## 📊 Public vs Authenticated Endpoints

### **Public Endpoints (No Auth Required):**
- Auth: OTP request/verify
- Client: Register, Login, EmailExists, UserNameExists, Password Recovery
- GoogleAccount: All endpoints
- TelegramAccount: HashAuth
- Main: Some enum endpoints

### **Authenticated Endpoints (Require sessionToken):**
- All Bet endpoints
- All Bonus endpoints
- Most Client endpoints (profile, balance, KYC)
- All Payment endpoints
- All Product endpoints
- All Transaction/History endpoints

---

## ⚠️ Important Notes for QA Testing

### **1. Email Generation for Testing:**
```javascript
const timestamp = Date.now();
const jiraTicket = 'CT-728'; // Optional
const email = jiraTicket 
  ? `test-${jiraTicket}${timestamp}@nextcode.tech`
  : `test-${timestamp}@nextcode.tech`;
```

### **2. Default Test Password:**
```
Qweasd123!
```

### **3. Partner ID:**
```
Minebit = 5
```

### **4. Environment Selection:**
- **Dev** - For development testing
- **QA** - For QA testing
- **Prod** - For production smoke tests (CAREFUL!)

### **5. Rate Limiting:**
- Check response headers for rate limits
- Implement delays between test runs

### **6. Test Data Cleanup:**
- Test accounts accumulate
- Consider cleanup strategy for test users

---

## 🔧 Next Steps for Playwright Tests

### **Priority 1 - Smoke Tests:**
1. Registration flow (GraphQL → REST)
2. Login flow
3. Get balance
4. Get games list
5. Launch a game

### **Priority 2 - Core Flows:**
1. Deposit flow
2. Bonus activation
3. Bet history
4. Transaction history

### **Priority 3 - Edge Cases:**
1. Invalid sessionToken
2. Expired sessionToken
3. Invalid partnerId
4. Missing required fields
5. Rate limiting

---

## 📝 Questions for Clarification

1. **Session Token Expiry:** How long does sessionToken remain valid?
2. **Concurrent Sessions:** Can same user have multiple sessions?
3. **Rate Limits:** What are the rate limits per endpoint?
4. **Test Payment Methods:** Are there test payment methods that don't process real money?
5. **Bonus Eligibility:** How to test bonus flows without real deposits?
6. **KYC Testing:** How to test KYC flows in QA/Dev?
7. **Game Availability:** Are all games available in all environments?

---

**Document created:** 2026-02-15
**Author:** BMW M5 (FamAssistant)
**Purpose:** API testing strategy for Minebit casino backend
