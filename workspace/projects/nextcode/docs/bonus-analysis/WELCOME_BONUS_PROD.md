# Welcome Bonus (PROD) — Quick Reference

**Last Updated:** 2026-03-12  
**Bonus ID:** 11380  
**Name:** ROCKTUBER 150% + 50 FS  
**Template:** Welcome Bonus Wagering (ID: 30)  
**Category:** Affiliate

---

## 🎁 Bonus Structure

| Parameter | Value |
|-----------|-------|
| **Deposit Match** | 150% |
| **Free Spins** | 50 FS × 7 games = 350 FS total |
| **Min Deposit** | $0.10 |
| **Max Bonus** | $500 |
| **Wagering** | x40 (TurnoverCount: 40) |
| **Valid For Spending** | 120 days |
| **Valid For Awarding** | ~3 years (until 2029-02-27) |

---

## 🎮 Free Spins Games (50 FS each)

| # | Game | ProductStructureId |
|---|------|-------------------|
| 1 | Gates of Olympus | 76807 |
| 2 | Sweet Bonanza | 58105 |
| 3 | Sugar Rush | 56261 |
| 4 | Starlight Princess | 55330 |
| 5 | Big Bass Bonanza | 43147 |
| 6 | The Dog House | 42429 |
| 7 | Wolf Gold | 40964 |

---

## 🎯 Eligibility Rules

| Rule | Value |
|------|-------|
| **Usage Limit** | 1 per player (ReusingMaxCount: 1) |
| **Email Verification** | NOT required |
| **Segments Excluded** | 1437, 1151, 487, 484 |
| **Total Claimed** | 4 players (as of 2026-03-12) |

---

## 💰 Wagering Conditions

| Parameter | Value |
|-----------|-------|
| **BetRealPercent** | 100% (real money wagering only) |
| **Min Wager Bet** | $0.10 |
| **Max Wager Bet** | $5.00 |
| **Max Cashout Multiplier** | x3 |
| **IsWagerOnlyReal** | true (WinRealPercentSameAsBet: true) |
| **IsStrictBetDistribution** | false |

---

## ⚙️ Technical Details

| Parameter | Value |
|-----------|-------|
| **BonusTypeId** | 16 |
| **IsSmartico** | false |
| **RequiresManualClaim** | false |
| **IsDepositStreak** | false |
| **IsAlwaysEligible** | false |
| **Status** | Active (true) |
| **PartnerId** | 5 |

---

## 📋 API Endpoints for Testing

### Get Bonus Details
```
GET /api/admin/bonuses/{id}
```

### Get Eligible Bonuses for Player
```
GET /api/player/bonuses/eligible
Authorization: Bearer {player_token}
```

### Claim Bonus (if RequiresManualClaim = true)
```
POST /api/player/bonuses/{id}/claim
```

---

## 🔍 Quick Queries

**Find this bonus on PROD:**
```bash
curl -X GET "https://api.minebit.com/api/admin/bonuses/11380" \
  -H "Authorization: Bearer {admin_token}"
```

**Check if player is eligible:**
- Player must NOT be in segments: 1437, 1151, 487, 484
- Player must NOT have claimed this bonus before (ReusingMaxCount: 1)

---

## 📝 Notes

- **Long-term campaign** — valid until February 2029
- **No Smartico integration** — handled directly by bonus system
- **Auto-awarded** — no manual claim required
- **Affiliate-driven** — likely tied to ROCKTUBER affiliate code

---

## 🔗 Related Files

- Full JSON response: `shared/test-results/CT-603/welcome-bonus-11380.json`
- Bonus system docs: `BONUS_SYSTEM_DOCUMENTATION.md`
