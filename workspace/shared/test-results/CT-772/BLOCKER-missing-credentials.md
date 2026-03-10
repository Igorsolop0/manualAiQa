# CT-772 Smoke Test Status Report

**Date:** 2026-03-10 17:54 GMT+1
**Ticket:** CT-772
**Environment:** Production (https://minebit.com)

## ❌ BLOCKER: Missing Credentials

**Issue:** 
Credentials file `workspace/shared/credentials/minebit-prod.json` does not exist.

**Required:**
- Production test account email
- Production test account password
- Confirmed test account with bonuses enabled

## 📋 Test Plan Ready

**Scope:**
1. ✅ Regular Bonuses — Timer Badge UI (6 locales: EN, RU, DE, ES, FR, PT)
2. ✅ Special Bonuses — Empty State Banner
3. ✅ Responsive Check (Desktop + Mobile)
4. ✅ Regression Check (CTAs, Timer countdown)

**Test Environment:**
- URL: https://minebit.com/bonuses
- Auth: Required (authorized user)
- Device: Desktop Chrome (MacBook Air)
- Mobile: Pixel 7 (if available)

## 🎯 Next Steps

**Waiting for Ihor to provide:**
1. Production test account credentials
2. Account should have:
   - Active bonuses (for timer badge verification)
   - Access to bonuses page
   - Valid balance

**Once credentials provided, I will:**
1. Login to production
2. Test all 6 locales
3. Verify timer badge format (XXH:YYM)
4. Verify empty state banner
5. Take screenshots for each locale
6. Test responsive design
7. Generate final report

## Estimated Time
20-30 minutes after credentials provided

---

**Action Required:** 
👉 Ihor, please provide production credentials or create new test file at:
`workspace/shared/credentials/minebit-prod.json`

Format:
```json
{
  "email": "test-account@example.com",
  "password": "test-password",
  "notes": "Account has active bonuses for testing"
}
```
