# Bonus Creation Analysis

## AdminWebApi Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/Bonus/CreateBonus` | Create new bonus |
| POST | `/api/Bonus/GetBonusById` | Get bonus details |
| PUT | `/api/Bonus/AddTriggerToBonus` | Add trigger to bonus |
| POST | `/api/Bonus/CloneBonus` | Clone existing bonus |
| POST | `/api/Bonus/BulkUpdateBonuses` | Bulk update |
| POST | `/api/Bonus/ClaimBonusForClients` | Claim for player |

## CreateBonus Flow (Hypothesis)

### Step 1: Create Bonus
```
POST /api/Bonus/CreateBonus
Header: UserId: 560
Body: {
  "Name": "Test Manual Claim Bonus",
  "PartnerId": 5,
  "BonusTypeId": 10,  // 10=Wager, 14=FS, 16=Split
  "MinAmount": 0.01,
  "MaxAmount": 100.00,
  "CurrencyMode": 0,  // 0=Single currency
  "Status": true,
  "StartTime": "2026-02-19T00:00:00Z",
  "FinishTime": "2027-02-19T23:59:59Z",
  
  // CT-753 specific
  "RequiresManualClaim": true,
  "TurnoverCount": 1,  // Wager multiplier
  "ValidForAwarding": 99999,  // Hours to activate
  "ValidForSpending": 99999,  // Hours to wager
  
  // Optional
  "Languages": { "Type": 65, "Ids": ["en"] },
  "Products": [],  // Games for FS
  ...
}
```

### Step 2: Add Trigger
```
PUT /api/Bonus/AddTriggerToBonus
Body: {
  "BonusId": <new_bonus_id>,
  "TriggerType": "Deposit",  // or "PromoCode", "Registration"
  "MinDeposit": 10.00,
  "Currencies": ["USD", "EUR"],
  ...
}
```

## Required Fields (Based on PROD data)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Name | string | Bonus name | "Test Manual Claim" |
| PartnerId | int | Brand ID | 5 (Minebit) |
| BonusTypeId | int | Bonus type | 10, 14, 16 |
| MinAmount | decimal | Min bonus amount | 0.01 |
| Status | bool | Active/Inactive | true |
| StartTime | datetime | Active from | "2026-02-19T00:00:00Z" |
| FinishTime | datetime | Active until | "2027-02-19T23:59:59Z" |

## CT-753 Fields (RequiresManualClaim)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| RequiresManualClaim | bool | Manual claim required | true |
| TurnoverCount | int? | Wager multiplier | 1, 5, 10 |
| ValidForAwarding | int | Hours to activate | 99999 |
| ValidForSpending | int | Hours to wager | 99999 |

## Bonus Types

| ID | Name | RequiresManualClaim? |
|----|------|---------------------|
| 1 | Welcome | Possible |
| 10 | Wager | ✅ Yes (CT-753) |
| 11 | No Deposit | Possible |
| 14 | Free Spins | Possible |
| 15 | FS Registration | Possible |
| 16 | Split Match | Possible |

## Trigger Types

1. **Deposit** - First deposit, any deposit
2. **Registration** - New user signup
3. **PromoCode** - User enters code
4. **Smartico** - External system trigger

## Questions for Tomorrow

1. What is the exact CreateBonus request body?
2. How to configure Products for Free Spins?
3. How to set ResetScheduleCron for recurring bonuses?
4. Strapi role in bonus configuration?
5. How triggers are configured in detail?

