# PROD Authentication Guide for CT-476 Testing

## Summary

**Status:** ⚠️ PARTIAL SUCCESS - Cannot complete full auth flow due to backend bugs

**Issue:** Both REST Login endpoint and GraphQL token authentication are broken on PROD.

## Working Solution: GraphQL Registration

The only working method to obtain a session token is through **GraphQL Registration**.

### Step 1: Register Player via GraphQL

**Endpoint:** `https://minebit-casino.prod.sofon.one/graphql`

**Method:** POST

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Accept": "*/*",
  "Accept-Language": "en-US,en;q=0.9",
  "Origin": "https://minebit-casino.prod.sofon.one",
  "Referer": "https://minebit-casino.prod.sofon.one/",
  "website-locale": "en",
  "website-origin": "https://minebit-casino.prod.sofon.one",
  "x-time-zone-offset": "-60"
}
```

**Mutation:**
```graphql
mutation PlayerRegisterUniversal(
  $input: PlayerRegisterUniversalInput!
  $bmsPartnerId: Int!
  $locale: Locale!
  $deviceFingerPrint: String
) {
  playerRegisterUniversal(
    input: $input
    bmsPartnerId: $bmsPartnerId
    locale: $locale
    deviceFingerPrint: $deviceFingerPrint
  ) {
    record {
      sessionToken
      userName
      id
      email
    }
    status
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "test-1234567890-1234@nextcode.tech",
    "password": "TestPass123!",
    "currency": "USD",
    "promoCode": null,
    "termsConditionsAccepted": true,
    "affiliateData": "https://minebit-casino.prod.sofon.one"
  },
  "bmsPartnerId": 5,
  "locale": "en",
  "deviceFingerPrint": "01234567890123456789012345678901"
}
```

**Response:**
```json
{
  "data": {
    "playerRegisterUniversal": {
      "record": {
        "sessionToken": "626d4eca402e4f61ae8629889300c03b",
        "userName": "iqfr27mWNk",
        "id": 1184432,
        "email": "ct476-test-1773149148460-6177@nextcode.tech"
      },
      "status": "Success"
    }
  }
}
```

## Step 2: Using the Session Token

### For Playwright (Browser Testing)

**Method 1: Set Cookie**
```javascript
await context.addCookies([{
  name: 'session_token',
  value: '626d4eca402e4f61ae8629889300c03b',
  domain: 'minebit-casino.prod.sofon.one',
  path: '/',
  secure: true,
  httpOnly: true
}]);

await page.goto('https://minebit-casino.prod.sofon.one/quests');
```

**Method 2: Set LocalStorage**
```javascript
await page.goto('https://minebit-casino.prod.sofon.one');
await page.evaluate((token) => {
  localStorage.setItem('session_token', token);
  localStorage.setItem('auth_token', token);
}, '626d4eca402e4f61ae8629889300c03b');
await page.goto('https://minebit-casino.prod.sofon.one/quests');
```

**Method 3: Network Request Interception**
```javascript
await page.route('**/*', async (route) => {
  const headers = route.request().headers();
  if (route.request().url().includes('graphql')) {
    headers['Authorization'] = '626d4eca402e4f61ae8629889300c03b';
  }
  route.continue({ headers });
});
```

### For API Calls (Without Browser)

**REST API (Most Endpoints):**
```bash
curl -X GET "https://websitewebapi.prod.sofon.one/5/api/v3/Client/GetClientBalance" \
  -H "Authorization: 626d4eca402e4f61ae8629889300c03b" \
  -H "website-locale: en" \
  -H "website-origin: https://minebit-casino.prod.sofon.one" \
  -H "x-time-zone-offset: -60"
```

**GraphQL Queries:**
```bash
curl -X POST "https://minebit-casino.prod.sofon.one/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: 626d4eca402e4f61ae8629889300c03b" \
  -H "website-locale: en" \
  -H "website-origin: https://minebit-casino.prod.sofon.one" \
  -d '{
    "operationName": "GetPlayerProfile",
    "query": "query GetPlayerProfile($bmsPartnerId: Int!, $locale: Locale!) { player(bmsPartnerId: $bmsPartnerId, locale: $locale) { id email userName currencyId } }",
    "variables": { "bmsPartnerId": 5, "locale": "en" }
  }'
```

## Known Issues

### ❌ Broken: REST Login Endpoint

**Endpoint:** `/{partnerId}/api/v3/Client/Login`

**Error:** `GeneralException: Object reference not set to an instance of an object.`

**Impact:** Cannot use existing accounts via REST API login

**Trace ID Example:** `306139937cab0d5668a7537bfbfb2eeb`

### ❌ Broken: GraphQL Token Authentication

**Issue:** Session tokens from GraphQL registration don't work for GraphQL queries

**Error:** `SessionNotFound: Session not found for`

**Impact:** Cannot use GraphQL for authenticated queries (only mutations)

**Workaround:** Use REST API endpoints for authenticated requests

## Generated Credentials

Current working test account:
- **Email:** `ct476-test-1773149148460-6177@nextcode.tech`
- **Password:** `TestPass123!`
- **Username:** `iqfr27mWNk`
- **Player ID:** `1184432`
- **Session Token:** `626d4eca402e4f61ae8629889300c03b`
- **Created:** 2026-03-10T14:39:08Z

## Scripts Available

### `scripts/prod_auth_graphql.py`
Registers new player and generates session token.

**Usage:**
```bash
python3 prod_auth_graphql.py
```

**Output:**
- Saves auth data to `workspace/shared/test-auth/prod-player-auth.json`
- Creates token file `workspace/shared/test-auth/token.txt`

### `scripts/test_prod_token_rest.py`
Tests if token works with REST API.

**Usage:**
```bash
python3 test_prod_token_rest.py
```

## Recommendations

### For Clawver Testing

1. **Always use GraphQL registration** to generate new test accounts
2. **Use session token in cookies** for Playwright browser tests
3. **Use Authorization header** for REST API calls
4. **Avoid GraphQL queries** with the token (they don't work)

### For Backend Team

1. **Fix REST Login endpoint** - NullReferenceException blocks all existing accounts
2. **Fix GraphQL session validation** - Tokens from registration should work for queries
3. **Add test mode** to accept mock tokens for automated testing

## Alternative: Manual Browser Auth

If automated auth fails, Clawver can use:

1. Navigate to login page
2. Fill email/password manually
3. Extract session token from localStorage/cookies
4. Use extracted token for subsequent tests

This is slower but more reliable given the backend bugs.
