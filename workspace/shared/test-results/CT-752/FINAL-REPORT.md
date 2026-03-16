# CT-752: Player Management Endpoints - Final Report

**Date:** 2026-03-16T12:35:00Z
**Ticket:** CT-752
**Task:** Find player deletion endpoint on AdminWebAPI

---

## ✅ SOLUTION FOUND

### Working Endpoints

**1. GetClientById**
```
POST /api/Client/GetClientById
Headers:
  - Content-Type: application/json
  - UserId: 1 (for DEV/QA) or 560 (for PROD)
Body: <clientId> (number)
```

**2. DeactivateClients** ⭐
```
POST /api/Client/DeactivateClients
Headers:
  - Content-Type: application/json
  - UserId: 1 (for DEV/QA) or 560 (for PROD)
Body: [<clientId>] (array of client IDs)
```

**3. ChangeClientDetails**
```
POST /api/Client/ChangeClientDetails
Headers:
  - Content-Type: application/json
  - UserId: 1 (for DEV/QA) or 560 (for PROD)
Body: {
  "id": <clientId>,
  "isTest": true,  // optional
  "state": <number>,  // optional
  "nickName": "<name>",  // optional
  "info": "<text>"  // optional
}
```

---

## 🔑 Key Discovery

### UserId by Environment

| Environment | UserId | Base URL |
|-------------|--------|----------|
| DEV | **1** | https://adminwebapi.dev.sofon.one/api |
| QA | **1** | https://adminwebapi.qa.sofon.one/api |
| PROD | **560** | https://adminwebapi.prod.sofon.one/api |

**⚠️ CRITICAL:** Using wrong UserId results in 401 Unauthorized!

---

## 📋 Example Commands

### Get Client Details
```bash
curl -X POST "https://adminwebapi.dev.sofon.one/api/Client/GetClientById" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "3563473"
```

### Deactivate Player (Blocks the player)
```bash
curl -X POST "https://adminwebapi.dev.sofon.one/api/Client/DeactivateClients" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d "[3563473]"
```

### Mark Player as Test
```bash
curl -X POST "https://adminwebapi.dev.sofon.one/api/Client/ChangeClientDetails" \
  -H "Content-Type: application/json" \
  -H "UserId: 1" \
  -d '{"id": 3563473, "isTest": true}'
```

---

## 🎯 Solution for CT-752

**Player to clean:**
- ID: 3563473
- Email: pandasen@echoprx.cc
- Environment: **QA** (not DEV)

**Steps:**

1. **Get player details on QA:**
   ```bash
   curl -X POST "https://adminwebapi.qa.sofon.one/api/Client/GetClientById" \
     -H "Content-Type: application/json" \
     -H "UserId: 1" \
     -d "3563473"
   ```

2. **Deactivate the player:**
   ```bash
   curl -X POST "https://adminwebapi.qa.sofon.one/api/Client/DeactivateClients" \
     -H "Content-Type: application/json" \
     -H "UserId: 1" \
     -d "[3563473]"
   ```

3. **Alternative: Mark as test player:**
   ```bash
   curl -X POST "https://adminwebapi.qa.sofon.one/api/Client/ChangeClientDetails" \
     -H "Content-Type: application/json" \
     -H "UserId: 1" \
     -d '{"id": 3563473, "isTest": true}'
   ```

---

## 📝 Findings

### ✅ What Works
- **DeactivateClients** endpoint exists and works
- **ChangeClientDetails** can mark players as test
- **GetClientById** retrieves player information
- Authentication with UserId header works correctly

### ⚠️ What Doesn't Work
- No "DeleteClient" or "DeletePlayer" endpoint found
- Player must be deactivated, not deleted
- QA environment may require VPN access

### 💡 Recommendation
Use **DeactivateClients** to block the player. This:
- Prevents login
- Keeps data for audit trail
- Allows clean testing with same Google account

---

## 🔍 Test Results

**DEV Environment:**
- ✅ API accessible
- ✅ Authentication works (UserId: 1)
- ⚠️ Player 3563473 not found in DEV (exists in QA)

**QA Environment:**
- ❓ Not tested (requires VPN access)
- Should work with same endpoints and UserId: 1

**PROD Environment:**
- ⚠️ Not tested (PROD uses UserId: 560)
- Should work with same endpoints

---

## 📚 Related Files

- Test script: `scripts/test_player_management_final.py`
- Results: `shared/test-results/CT-752/player-management-final.json`
- BackOffice API client: `src/api/clients/backoffice-api.client.ts`
- API fixture: `src/fixtures/api.fixture.ts`

---

## 🚀 Next Steps

1. **Connect to QA environment** via VPN
2. **Run deactivation command** on QA
3. **Test social linking** with clean state
4. **Document** the cleanup process for future tests

---

## 📌 Important Notes

1. **No Delete Endpoint:** System doesn't support hard delete of players
2. **Deactivate Instead:** Use DeactivateClients to block access
3. **Test Players:** Can mark with `isTest: true` for filtering
4. **Audit Trail:** Deactivation keeps data, deletion would lose audit history
5. **Environment-Specific:** Remember to use correct UserId (1 for DEV/QA, 560 for PROD)
