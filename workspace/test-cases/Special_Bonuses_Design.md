# Special Bonuses Section — Test Case Design

**Project:** Minebit
**Related Ticket:** CRYPTO-461 (Testing)
**Created:** 2026-02-23
**Author:** Panda Sensei

---

## 📊 Source of Truth — BO Prod Data

### Special Bonuses on Prod (Minebit, Active):

| Type ID | Count | Type Name | Example |
|---------|-------|-----------|---------|
| **10** | 191 | CampaignWager/Unknown | $150,000 Cash Drop, Low Balance Cash Bonus |
| **11** | 45 | CampaignCash | Giveaway winner |
| **14** | 55 | FreeSpin-related | 30 FS Giveaway Winner, Prize Drop FS |
| **16** | 50 | Deposit+FS Combination | 150% + 50 FS bonuses |

**Key Categories:**
- **Welcome Pack:** 3 bonuses (TurnoverCount: 35-40)
- **Deposit Bonuses:** 18 bonuses (Ultimate Rush series, TurnoverCount: 15)
- **FreeSpin Bonuses:** 139 bonuses
- **Promo Code Bonuses:** Hidden until code entered

**Common Characteristics:**
- Most have `TurnoverCount` > 0 (WAGERING REQUIRED)
- Some have `TurnoverCount: None` (NO WAGERING)
- `IsSmartico: false` for most (BO-managed, not Smartico)

---

## 🔄 Special Bonuses States (from CRYPTO-461)

| State | Button | Endpoint | Description |
|-------|--------|----------|-------------|
| **ReadyForActivation** | "Activate" | GetEligibleBonuses | Bonus can be activated |
| **AwaitingForDeposit** | "Deposit" | GetActiveBonus | Waiting for deposit |
| **PlayingFreespins** | "Choose game" | GetActiveBonus | (FS only) Play FS |
| **CurrentlyWagering** | "Play game" | GetActiveBonus | Wagering in progress |
| **ReadyForClaiming** | "Claim $X" | GetActiveBonus | Ready to claim |

---

## 🎯 Test Case Categories

### Category 1: UI & Visibility (2 tests)
- Guest user cannot see Special Bonuses
- Authorized user sees Special Bonuses section

### Category 2: States & Transitions (8 tests)
- ReadyForActivation → Activate
- AwaitingForDeposit → Make deposit → PlayingFreespins/CurrentlyWagering
- PlayingFreespins → Complete FS → CurrentlyWagering
- CurrentlyWagering → Complete wagering → ReadyForClaiming
- ReadyForClaiming → Claim → Closed

### Category 3: Bonus Types (4 tests)
- Deposit Bonus with wagering
- FreeSpin Bonus
- Cash Bonus (no deposit required)
- Mixed Bonus (Deposit + FS)

### Category 4: Welcome Pack (3 tests)
- Progressive unlocking (Bonus 1 → 2 → 3 → 4)
- Only 1 active at a time
- Deposit tiers

### Category 5: Promo Code Bonuses (3 tests)
- Hidden until code entered
- Activate after code input
- Cannot reuse code

### Category 6: Parallel Claim (2 tests)
- CANNOT claim with active Special Bonus (monobonus)
- CAN claim Regular Bonus with active Special Bonus

### Category 7: Negative Scenarios (3 tests)
- Cannot activate with active bonus
- Wagering expiration
- Bonus cancellation (lose winnings)

---

## 📋 Proposed Test Cases (25 total)

### Category 1: UI & Visibility

#### TC-SB-001: Guest User — Cannot See Special Bonuses
**Priority:** High
**Preconditions:** User not logged in
**Steps:**
1. Navigate to Bonuses page as guest
2. Check for Special Bonuses section
**Expected:** Special Bonuses section NOT visible (only login prompt or regular content)

#### TC-SB-002: Authorized User — Special Bonuses Section Visible
**Priority:** High
**Preconditions:** User logged in
**Steps:**
1. Navigate to Bonuses page
2. Check Special Bonuses section
**Expected:** Special Bonuses section visible with available bonuses

---

### Category 2: States & Transitions

#### TC-SB-003: ReadyForActivation — Activate Bonus
**Priority:** Critical
**Preconditions:**
- Player has no active bonus
- Player has bonus in ReadyForActivation state
- Bonus has wagering requirement
**Steps:**
1. Navigate to Special Bonuses
2. Check bonus card shows "Activate" button
3. Click "Activate"
4. Check Active Bonuses page
**Expected:**
- Bonus activated successfully
- Appears in Active Bonuses
- State = CurrentlyWagering (if deposit already made)

#### TC-SB-004: AwaitingForDeposit — Deposit Required
**Priority:** Critical
**Preconditions:**
- Player has no active bonus
- Player activated deposit bonus
- No deposit made yet
**Steps:**
1. Activate deposit bonus
2. Check bonus card shows "Deposit" button
3. Click "Deposit" → navigate to payment
4. Make deposit
5. Return to Bonuses page
**Expected:**
- After deposit, bonus state changes
- State = CurrentlyWagering or PlayingFreespins

#### TC-SB-005: PlayingFreespins — Complete FS Phase
**Priority:** Critical
**Preconditions:**
- Player has FreeSpin bonus activated
- FS not yet played
**Steps:**
1. Navigate to Special Bonuses
2. Check bonus shows "Choose game" button
3. Click "Choose game" → game opens
4. Play all FS
5. Return to Bonuses page
**Expected:**
- After FS completed, state = CurrentlyWagering
- Progress bar shows wagering progress

#### TC-SB-006: CurrentlyWagering — Complete Wagering
**Priority:** Critical
**Preconditions:**
- Player has active bonus in CurrentlyWagering state
- Wagering requirement > $0
**Steps:**
1. Navigate to Special Bonuses
2. Check bonus shows "Play game" button
3. Note wagering progress bar
4. Play games to complete wagering
5. Return to Bonuses page
**Expected:**
- Progress bar reaches 100%
- State = ReadyForClaiming
- Button changes to "Claim $X"

#### TC-SB-007: ReadyForClaiming — Claim Bonus
**Priority:** Critical
**Preconditions:**
- Player has bonus in ReadyForClaiming state
- Amount > $0
**Steps:**
1. Navigate to Special Bonuses
2. Check bonus shows "Claim $X" button
3. Click "Claim"
**Expected:**
- Amount credited to real balance
- Bonus disappears from Active Bonuses
- Bonus moves to History

#### TC-SB-008: State Transition — Full Flow (Deposit Bonus)
**Priority:** High
**Preconditions:**
- Player has deposit bonus available
- No active bonus
**Steps:**
1. Activate deposit bonus
2. Make deposit
3. Complete wagering
4. Claim bonus
**Expected:**
- All states transition correctly
- Amount credited at the end

#### TC-SB-009: State Transition — Full Flow (FS Bonus)
**Priority:** High
**Preconditions:**
- Player has FS bonus available
- No active bonus
**Steps:**
1. Activate FS bonus
2. Play FS in specific game
3. Complete wagering on FS winnings
4. Claim bonus
**Expected:**
- All states: ReadyForActivation → PlayingFreespins → CurrentlyWagering → ReadyForClaiming

#### TC-SB-010: Active Bonus — Always First in Section
**Priority:** High
**Preconditions:**
- Player has active Special Bonus
- Multiple Special Bonuses available
**Steps:**
1. Navigate to Special Bonuses
2. Check bonus order
**Expected:**
- Active bonus appears FIRST in the section
- Other bonuses appear after

---

### Category 3: Bonus Types

#### TC-SB-011: Deposit Bonus — Wagering Required
**Priority:** High
**Preconditions:**
- Player has deposit bonus (e.g., Ultimate Rush)
- TurnoverCount > 0
**Steps:**
1. Activate deposit bonus
2. Make qualifying deposit
3. Check wagering requirement
4. Complete wagering
5. Claim
**Expected:**
- Wagering required (e.g., x15 or x40)
- Progress bar visible
- Amount credited after claim

#### TC-SB-012: FreeSpin Bonus — No Wagering on FS
**Priority:** High
**Preconditions:**
- Player has FS bonus with TurnoverCount = None
**Steps:**
1. Activate FS bonus
2. Play FS in specific game
3. Check bonus state after FS
**Expected:**
- No wagering on FS winnings
- Amount available to claim immediately

#### TC-SB-013: Cash Bonus — No Deposit Required
**Priority:** High
**Preconditions:**
- Player has cash bonus (no deposit required)
- TurnoverCount = None
**Steps:**
1. Activate cash bonus
2. Check bonus state
3. Claim immediately
**Expected:**
- No deposit required
- No wagering
- Amount credited directly to balance

#### TC-SB-014: Mixed Bonus — Deposit + FS
**Priority:** High
**Preconditions:**
- Player has mixed bonus (e.g., 150% + 50 FS)
**Steps:**
1. Activate bonus
2. Make deposit
3. Play FS
4. Complete wagering
5. Claim
**Expected:**
- Both components (deposit bonus + FS) processed
- Wagering on both parts

---

### Category 4: Welcome Pack

#### TC-SB-015: Welcome Pack — Progressive Unlocking
**Priority:** Critical
**Preconditions:**
- New player registered
- Welcome Pack configured (4 bonuses)
**Steps:**
1. Check Bonuses page after registration
2. Verify Bonus 1 available
3. Activate and complete Bonus 1
4. Check Bonus 2 unlocks
5. Complete Bonus 2, check Bonus 3 unlocks
**Expected:**
- Bonuses unlock sequentially
- Cannot skip bonuses

#### TC-SB-016: Welcome Pack — Only 1 Active at Time
**Priority:** Critical
**Preconditions:**
- Player has active Welcome Pack bonus
**Steps:**
1. Check Welcome Pack Bonus 1 active
2. Try to activate Bonus 2
**Expected:**
- Cannot activate Bonus 2 while Bonus 1 active
- Must complete Bonus 1 first

#### TC-SB-017: Welcome Pack — Deposit Tiers
**Priority:** High
**Preconditions:**
- Welcome Pack with tiers configured
**Steps:**
1. Deposit minimum amount → Tier 1
2. Check bonus amount
3. Complete and claim
4. Deposit medium amount → Tier 2
5. Check increased bonus amount
**Expected:**
- Different deposit amounts → different bonus tiers
- Higher deposit = higher bonus percentage

---

### Category 5: Promo Code Bonuses

#### TC-SB-018: Promo Code — Hidden Until Entered
**Priority:** High
**Preconditions:**
- Promo code bonus configured
- Player not entered code yet
**Steps:**
1. Navigate to Bonuses page
2. Check for promo code bonus
3. Enter promo code in input field
4. Check bonus appears
**Expected:**
- Bonus NOT visible before code entry
- Appears in Available Bonuses after code entry

#### TC-SB-019: Promo Code — Activate After Entry
**Priority:** High
**Preconditions:**
- Player entered valid promo code
**Steps:**
1. After code entry, check bonus in Available
2. Activate bonus
3. Complete requirements
4. Claim
**Expected:**
- Normal activation flow after code entry

#### TC-SB-020: Promo Code — Cannot Reuse
**Priority:** High
**Preconditions:**
- Player already used promo code
**Steps:**
1. Try to enter same promo code again
**Expected:**
- Code rejected
- Error message: "Code already used" or similar

---

### Category 6: Parallel Claim

#### TC-SB-021: Special Bonus — Cannot Activate with Active Bonus
**Priority:** Critical
**Preconditions:**
- Player has active Special Bonus
- Another Special Bonus available
**Steps:**
1. Check active Special Bonus
2. Try to activate another Special Bonus
**Expected:**
- Cannot activate
- Message: "Active bonus exists" or similar

#### TC-SB-022: Regular Bonus — Can Claim with Active Special Bonus
**Priority:** Critical
**Related:** CT-45
**Preconditions:**
- Player has active Special Bonus
- Regular Bonus in ReadyForClaiming state
**Steps:**
1. Check active Special Bonus
2. Navigate to Regular Bonuses
3. Claim Regular Bonus
**Expected:**
- Regular Bonus can be claimed (CT-45)
- Special Bonus remains active

---

### Category 7: Negative Scenarios

#### TC-SB-023: Wagering Expiration — Bonus Lost
**Priority:** High
**Preconditions:**
- Player has active bonus with wagering
- Wagering time limit expires
**Steps:**
1. Activate bonus
2. Wait for expiration time (or manipulate time)
3. Check bonus status
**Expected:**
- Bonus status = Expired or Lost
- Winnings lost
- Bonus removed from Active Bonuses

#### TC-SB-024: Bonus Cancellation — Lose Winnings
**Priority:** High
**Preconditions:**
- Player has active bonus (NOT finished)
- Wagering incomplete
**Steps:**
1. Activate bonus
2. Play partially (wagering incomplete)
3. Cancel bonus
4. Check balance
**Expected:**
- Bonus cancelled
- Winnings LOST (not credited)
- Balance unchanged

#### TC-SB-025: Minimum Amount Not Met — Bonus Lost
**Priority:** Medium
**Preconditions:**
- Bonus requires minimum deposit
- Player deposits less than minimum
**Steps:**
1. Activate deposit bonus
2. Deposit amount < minimum required
3. Check bonus status
**Expected:**
- Bonus not activated
- Error message about minimum deposit

---

## 📊 Summary

**Total Test Cases:** 25

**Priority Distribution:**
- Critical: 7
- High: 16
- Medium: 2

**Coverage by Category:**
| Category | Tests | Focus |
|----------|-------|-------|
| UI & Visibility | 2 | Guest vs authorized user |
| States & Transitions | 8 | All 5 states + transitions |
| Bonus Types | 4 | Deposit, FS, Cash, Mixed |
| Welcome Pack | 3 | Progressive, mono-bonus, tiers |
| Promo Code | 3 | Hidden, activate, no reuse |
| Parallel Claim | 2 | Mono-bonus vs Regular parallel |
| Negative | 3 | Expiration, cancellation, minimum |

---

## 🔑 Key Differences from Regular Bonuses:

| Parameter | Regular Bonuses | Special Bonuses |
|-----------|----------------|-----------------|
| **Wagering** | ❌ None (TurnoverCount: null) | ✅ Most have wagering |
| **States** | 3 (Waiting, Ready, Claimed) | 5 (Ready, Deposit, FS, Wagering, Claim) |
| **Parallel Claim** | ✅ Yes (CT-45) | ❌ Mono-bonus |
| **Active Bonus Position** | In list | Always FIRST in section |
| **Promo Code** | N/A | ✅ Hidden until code entered |
| **Welcome Pack** | N/A | ✅ Progressive unlocking |

---

## ⚠️ Questions for Clarification:

1. **What is BonusTypeId 10, 14, 16?** (Need BO documentation)
2. **How does progress bar work for Special Bonuses?** (Wagering progress, not time)
3. **What happens to FS winnings if bonus cancelled during wagering?**
4. **Can Welcome Pack be skipped?** (Documentation says no, but need to verify)
5. **Where is promo code input field located?** (On Bonus Page? Separate section?)

---

**Next Steps:**
1. Clarify questions above
2. Review existing TestRail cases for Special Bonuses
3. Add missing test cases to TestRail
4. Execute test cases for CRYPTO-461
