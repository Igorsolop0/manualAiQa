# CT-476 Authentication Status Report

**Generated:** 2026-03-10T14:40:00Z
**Agent:** Cipher (API Docs Agent)

## ✅ Deliverables Complete

### 1. Test Credentials Created
- **Email:** `ct476-test-1773149148460-6177@nextcode.tech`
- **Password:** `TestPass123!`
- **Username:** `iqfr27mWNk`
- **Player ID:** `1184432`
- **Session Token:** `626d4eca402e4f61ae8629889300c03b`

### 2. Scripts Created
- `scripts/prod_auth_graphql.py` - Register new players
- `scripts/test_prod_token_rest.py` - Test token validity

### 3. Documentation
- `workspace/shared/test-auth/prod-player-auth.json` - Credentials JSON
- `workspace/shared/test-auth/token.txt` - Raw token
- `workspace/shared/test-auth/PROD_AUTH_GUIDE.md` - Complete auth guide

## ⚠️ Backend Issues Found

### Critical: REST Login Endpoint Broken
- **Endpoint:** `/{partnerId}/api/v3/Client/Login`
- **Error:** `NullReferenceException`
- **Impact:** Cannot login existing accounts
- **Trace ID:** `306139937cab0d5668a7537bfbfb2eeb`

### Known: GraphQL Token Auth Inconsistent
- **Issue:** Registration tokens don't work for GraphQL queries
- **Workaround:** Use REST API with Authorization header
- **Status:** Works for mutations, fails for queries

## 🚀 Quick Start for Clawver

### Option 1: Playwright with Cookie
```javascript
await context.addCookies([{
  name: 'session_token',
  value: '626d4eca402e4f61ae8629889300c03b',
  domain: 'minebit-casino.prod.sofon.one',
  path: '/'
}]);
```

### Option 2: REST API Call
```bash
curl -H "Authorization: 626d4eca402e4f61ae8629889300c03b" \
  "https://websitewebapi.prod.sofon.one/5/api/v3/Client/GetClientBalance"
```

## 📋 Next Steps

1. **Clawver** uses the generated token for CT-476 testing
2. **Backend Team** fixes Login endpoint bug
3. **Review** PROD_AUTH_GUIDE.md for complete documentation
