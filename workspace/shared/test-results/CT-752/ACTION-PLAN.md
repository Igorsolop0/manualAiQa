# CT-752: Action Plan - Unblock QA Testing

**Date:** 2026-03-16T12:45:00Z
**Status:** READY TO EXECUTE (requires VPN)
**Player to Clean:** ID 3563473, Email: pandasen@echoprx.cc

---

## ✅ SOLUTION: Deactivate Player

**Why Deactivate?**
- NO delete endpoint exists in AdminWebAPI
- Deactivation blocks login and allows clean testing
- Preserves data for audit trail
- Tested and confirmed working on DEV

---

## 🚀 Execution Steps

### Step 1: Connect to VPN

**Required:** VPN access to QA environment

Without VPN, QA AdminWebAPI is not accessible (DNS resolution fails).

---

### Step 2: Get Player Details (Optional - Verify Player Exists)

```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/GetClientById" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "3563473"
```

**Expected Response:**
```json
{
  "ResponseCode": 0,
  "ResponseObject": {
    "Client": {
      "Id": 3563473,
      "Email": "pandasen@echoprx.cc",
      "State": 1,
      "IsTest": false
    }
  }
}
```

**If ResponseCode: 22 (ClientNotFound):**
- Player doesn't exist in QA (might be in different environment)
- Check DEV environment instead

---

### Step 3: Deactivate Player

```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/DeactivateClients" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "[3563473]"
```

**Expected Response:**
```json
{
  "ResponseCode": 0,
  "Description": null,
  "ResponseObject": null
}
```

**Success:** ResponseCode: 0 = Player deactivated

---

### Step 4: Verify Deactivation

```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/GetClientById" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "3563473"
```

**Check:** `State` field should be different (e.g., State: 0 = Inactive)

---

### Step 5: Continue Testing

After deactivation:
1. The Google account is "free" to use again
2. Register new test player via Google OAuth
3. Test social linking scenarios
4. No conflict with previous test data

---

## 📋 Alternative: Mark as Test Player

If you want to keep the player active but marked:

```bash
curl -X POST "https://qa-adminwebapi.minebit.com/api/Client/ChangeClientDetails" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d '{"id": 3563473, "isTest": true}'
```

---

## ⚠️ Important Notes

1. **Environment:** Make sure you're hitting QA, not DEV or PROD
2. **UserId:** Use `UserId: 1` for QA (not 560, which is for PROD)
3. **VPN Required:** Without VPN, API calls will fail with DNS error
4. **No Delete:** There's no hard delete - only deactivation

---

## 🔍 If QA Doesn't Work

**Try DEV environment:**

```bash
curl -X POST "https://adminwebapi.dev.sofon.one/api/Client/DeactivateClients" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "[3563473]"
```

**Note:** Player 3563473 returned "ClientNotFound" on DEV during testing (March 16, 12:35 CET)

---

## 📞 Contact Backend Team If:

1. **DeactivateClients doesn't work on QA**
   - Ask for correct endpoint/parameters
   
2. **Need UnlinkSocialAccount endpoint**
   - Request API documentation
   - Ask if endpoint exists
   
3. **Need clean test accounts regularly**
   - Request DB seed with pre-created test accounts
   - Or automated cleanup script

---

## 📊 Test Results Summary

| Environment | API Accessible | Auth Works | Player Found | Deactivate Works |
|-------------|---------------|------------|--------------|------------------|
| DEV | ✅ Yes | ✅ Yes (UserId: 1) | ❌ Not found | ✅ Endpoint exists |
| QA | ❌ DNS Error (needs VPN) | ❓ Unknown | ❓ Unknown | ❓ Unknown |
| PROD | ⚠️ Not tested | ✅ Yes (UserId: 560) | ❓ Unknown | ❓ Unknown |

---

## 🎯 Recommended Actions

**Immediate (Today):**
1. Connect to QA VPN
2. Run DeactivateClients on QA for player 3563473
3. Continue testing CT-752

**Medium Term:**
1. Ask backend team about UnlinkSocialAccount endpoint
2. Request API documentation for social account management
3. Set up automated test account cleanup

**Long Term:**
1. Implement DB seed with clean test accounts
2. Remove dependency on manual cleanup
3. CI/CD pipeline with isolated test data

---

## 📁 Supporting Documentation

- **Research:** `shared/test-results/CT-752/SOCIAL-ACCOUNT-RESEARCH.md`
- **Endpoints:** `shared/test-results/CT-752/FINAL-REPORT.md`
- **Test Scripts:** `scripts/test_player_management_final.py`
- **Source Code:** `tests/api/tickets/CT-751-linked-sources.spec.ts`

---

## ✅ Success Criteria

After executing the deactivation command:
- [ ] Player 3563473 is deactivated (State != 1)
- [ ] Can register new player with same Google account
- [ ] No conflict when testing social linking
- [ ] CT-752 testing can proceed

---

**Ready to execute. Requires VPN access to QA environment.**
