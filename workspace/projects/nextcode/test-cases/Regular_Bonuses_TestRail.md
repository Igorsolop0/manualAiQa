# Regular Bonuses — Manual Test Cases (TestRail Format)

**Project:** Minebit
**Section:** Regular Bonuses (Daily, Cashback, Weekly, Monthly)
**Related Tickets:** CT-45, CT-44, CT-558, CT-559, CT-61, CRYPTO-459
**Created:** 2026-02-23
**Author:** Panda Sensei

---

## Section 1: Bonus States & Transitions

### TC-RB-001: New Player — All Regular Bonuses Visible

**Priority:** High
**Type:** Manual
**Estimate:** 10 min
**Preconditions:**
- New player registered (no deposits, no bonuses claimed)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as new player | Player logged in successfully |
| 2 | Navigate to Bonuses page | Bonuses page loads |
| 3 | Scroll to Regular Bonuses section | Section visible with 4 bonus cards: Daily, Cashback, Weekly, Monthly |
| 4 | Check each bonus card | Each card shows "AwaitingForActivation" state with "Play game" button disabled |
| 5 | Check timer on each card | Timer shows NextAvailableAt date (tomorrow for Daily, next Sunday for Weekly, etc.) |

**Notes:** All bonuses should be in AwaitingForActivation state for new players.

---

### TC-RB-002: State Transition — AwaitingForActivation → ReadyForActivation

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Preconditions:**
- Player has inactive Regular Bonus (e.g., Cashback)
- NextAvailableAt time has passed

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Wait until NextAvailableAt time | Timer expires |
| 2 | Refresh Bonuses page | Page reloads |
| 3 | Check bonus card state | State changes to "ReadyForActivation" |
| 4 | Check button | "Activate" button appears and is enabled |
| 5 | Check bonus amount | Amount field shows value (calculated by Smartico) |

**Notes:** May need to trigger Smartico calculation manually or wait for cron job.

---

### TC-RB-005: State Transition — ReadyForClaiming → Closed

**Priority:** High
**Type:** Manual
**Estimate:** 10 min
**Preconditions:**
- Player has bonus in ReadyForClaiming state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click "Claim $X" button | Claim process starts |
| 2 | Check balance | Bonus amount credited to real balance |
| 3 | Check bonus card | Bonus card disappears from Regular Bonuses section |
| 4 | Check Active Bonuses | Bonus status = "Closed" |
| 5 | Check transaction history | Transaction shows bonus claim with correct amount |

**Notes:** Bonus amount should match the claimed amount.

---

## Section 2: Parallel Claim (CT-45 Critical)

### TC-RB-006: Cashback — Can Claim with Active Bonus

**Priority:** Critical
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-45
**Preconditions:**
- Player has active bonus (e.g., Welcome Pack)
- Player has Cashback in ReadyForActivation state
- Player has net loss in the period

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify active bonus exists | Active bonus shows in Active Bonuses list |
| 2 | Navigate to Regular Bonuses | Cashback card visible |
| 3 | Check Cashback availability | "Activate" button enabled |
| 4 | Click "Activate" on Cashback | Cashback activates successfully |
| 5 | Check Active Bonuses | BOTH bonuses appear (original + Cashback) |

**Notes:** This is the CRITICAL test for CT-45. Cashback MUST be claimable with other active bonus.

---

### TC-RB-007: Rakeback — Can Claim with Active Bonus

**Priority:** Critical
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-45
**Preconditions:**
- Player has active bonus
- Player has Rakeback in ReadyForActivation state
- Player has wagered amount

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify active bonus exists | Active bonus shows in Active Bonuses list |
| 2 | Navigate to Regular Bonuses | Rakeback card visible |
| 3 | Check Rakeback availability | "Activate" button enabled |
| 4 | Click "Activate" on Rakeback | Rakeback activates successfully |
| 5 | Check Active Bonuses | BOTH bonuses appear |

**Notes:** Rakeback can be claimed parallel with other bonuses (CT-45).

---

### TC-RB-008: Monthly Bonus (No Wager) — Can Claim with Active Bonus

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-45
**Preconditions:**
- Player has active bonus
- Player has Monthly bonus (CampaignCash without wager) in ReadyForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify active bonus exists | Active bonus shows in Active Bonuses list |
| 2 | Navigate to Regular Bonuses | Monthly card visible |
| 3 | Check Monthly availability | "Activate" button enabled |
| 4 | Click "Activate" on Monthly | Monthly activates successfully |
| 5 | Check Active Bonuses | BOTH bonuses appear |

**Notes:** Monthly bonus without wager can be claimed parallel (CT-45).

---

### TC-RB-009: Weekly Bonus (With Wager) — Cannot Claim with Active Bonus

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-45
**Preconditions:**
- Player has active bonus
- Player has Weekly bonus (with wagering requirement) in ReadyForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify active bonus exists | Active bonus shows in Active Bonuses list |
| 2 | Navigate to Regular Bonuses | Weekly card visible |
| 3 | Check Weekly availability | "Activate" button DISABLED or bonus card shows "locked" state |
| 4 | Try to click "Activate" | Cannot activate |
| 5 | Check error message (if any) | Message: "Cannot activate while another bonus is active" |

**Notes:** Weekly with wagering requirement CANNOT be claimed parallel with other active bonus.

---

### TC-RB-010: CashBackBonus Type — Parallel Claim Verification

**Priority:** High
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-45
**Preconditions:**
- BackOffice access
- Bonus with Type = "CashBackBonus" configured

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login to BO | BO dashboard loads |
| 2 | Navigate to Bonuses → Find CashBackBonus | Bonus found |
| 3 | Check bonus Type field | Type = "CashBackBonus" |
| 4 | Create test player | Player created |
| 5 | Activate any other bonus | Bonus active |
| 6 | Try to activate CashBackBonus | Activation successful (parallel claim allowed) |

**Notes:** CT-45 specifically mentions "CashBackBonus" type as parallel-claimable.

---

### TC-RB-011: CampaignCash (No Wager) — Parallel Claim Verification

**Priority:** High
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-45
**Preconditions:**
- BackOffice access
- Bonus with Type = "CampaignCash" without wagering configured

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login to BO | BO dashboard loads |
| 2 | Navigate to Bonuses → Find CampaignCash | Bonus found |
| 3 | Check bonus Type = "CampaignCash" | Confirmed |
| 4 | Check wagering configuration | HasWagering = false or TurnoverCount = 0 |
| 5 | Create test player with active bonus | Active bonus exists |
| 6 | Try to activate CampaignCash | Activation successful |

**Notes:** CampaignCash WITHOUT wager can be claimed parallel.

---

## Section 3: Timer Logic (CT-558)

### TC-RB-012: Daily Bonus — Timer Shows Next Day 00:00 UTC

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-558
**Preconditions:**
- Player with Daily bonus (e.g., Daily Login Bonus)
- Bonus in AwaitingForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Note current date/time | Current time recorded |
| 2 | Navigate to Regular Bonuses | Daily bonus card visible |
| 3 | Check NextAvailableAt timer | Timer shows tomorrow 00:00 UTC |
| 4 | Calculate expected date | Expected: current date + 1 day, 00:00 UTC |
| 5 | Compare timer with expected | Timer matches expected date |

**Notes:** Timer should reset to next day at midnight UTC.

---

### TC-RB-013: Weekly Bonus — Timer Shows Next Sunday 00:00 UTC

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-558
**Preconditions:**
- Player with Weekly bonus
- Bonus in AwaitingForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Note current day of week | Current day recorded (e.g., Tuesday) |
| 2 | Navigate to Regular Bonuses | Weekly bonus card visible |
| 3 | Check NextAvailableAt timer | Timer shows next Sunday 00:00 UTC |
| 4 | Calculate expected date | Expected: next Sunday 00:00 UTC |
| 5 | Compare timer with expected | Timer matches expected date |

**Notes:** Weekly timer always points to next Sunday.

---

### TC-RB-014: Monthly Bonus — Timer Shows 1st of Next Month 00:00 UTC

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-558
**Preconditions:**
- Player with Monthly bonus
- Bonus in AwaitingForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Note current month | Current month recorded (e.g., February) |
| 2 | Navigate to Regular Bonuses | Monthly bonus card visible |
| 3 | Check NextAvailableAt timer | Timer shows 1st of next month 00:00 UTC |
| 4 | Calculate expected date | Expected: March 1st 00:00 UTC (if current is February) |
| 5 | Compare timer with expected | Timer matches expected date |

**Notes:** Monthly timer always points to 1st day of next month.

---

### TC-RB-015: Custom CRON — Timer Follows BO Configuration

**Priority:** Medium
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-558
**Preconditions:**
- BackOffice access
- Bonus with custom CRON schedule configured (e.g., "Every Tuesday and Friday at 15:00 UTC")

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login to BO | BO dashboard loads |
| 2 | Navigate to Bonuses → Find bonus with CRON | Bonus found |
| 3 | Check CRON configuration | CRON: "0 15 * * 2,5" (Tue, Fri 15:00 UTC) |
| 4 | Navigate to Regular Bonuses (as player) | Bonus card visible |
| 5 | Check NextAvailableAt timer | Timer shows next Tue/Fri 15:00 UTC |
| 6 | Verify timer matches CRON | Timer correct |

**Notes:** Custom CRON overrides default daily/weekly/monthly logic.

---

### TC-RB-016: IsPendingCalculation Flag — Smartico Pending State

**Priority:** High
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-558
**Preconditions:**
- Player with Cashback/Rakeback
- Timer just expired (NextAvailableAt passed)
- Smartico calculation not yet complete

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Wait for NextAvailableAt to pass | Timer expires |
| 2 | Refresh Bonuses page | Page reloads |
| 3 | Check bonus card state | State may still be "AwaitingForActivation" |
| 4 | Check IsPendingCalculation flag | IsPendingCalculation = true |
| 5 | Check Amount field | Amount = null or 0 |
| 6 | Wait for Smartico calculation | Calculation completes |
| 7 | Refresh page again | State changes to "ReadyForActivation" |
| 8 | Check IsPendingCalculation | IsPendingCalculation = false |
| 9 | Check Amount | Amount shows calculated value |

**Notes:** There may be a timing mismatch between timer (00:00) and Smartico calculation (e.g., 00:15).

---

## Section 4: Smartico Integration

### TC-RB-017: Cashback — Net Loss Calculation

**Priority:** High
**Type:** Manual
**Estimate:** 30 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with deposits and bets
- Player has net loss in the period (deposits - withdrawals - balance < 0)
- Cashback configured (e.g., 10% of net loss)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as test player | Player logged in |
| 2 | Deposit $100 | Balance = $100 |
| 3 | Play games and lose $80 | Balance = $20 |
| 4 | Check net loss | Net loss = $80 ($100 deposit - $20 balance) |
| 5 | Wait for Cashback trigger (Tue/Fri) | Trigger time arrives |
| 6 | Navigate to Regular Bonuses | Cashback card shows calculated amount |
| 7 | Verify Cashback amount | Amount ≈ $8 (10% of $80) |

**Notes:** Cashback is based on net loss formula in Smartico.

---

### TC-RB-018: Cashback — No Net Loss = No Bonus

**Priority:** High
**Type:** Manual
**Estimate:** 20 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with no net loss (won more than lost)
- Cashback period (Tue/Fri)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as test player | Player logged in |
| 2 | Deposit $100 | Balance = $100 |
| 3 | Play games and WIN $50 | Balance = $150 |
| 4 | Check net loss | Net loss = -$50 (negative = profit) |
| 5 | Wait for Cashback trigger (Tue/Fri) | Trigger time arrives |
| 6 | Navigate to Regular Bonuses | Cashback card shows "No cashback available" or Amount = $0 |
| 7 | Check bonus state | State remains "AwaitingForActivation" |

**Notes:** If no net loss, cashback is not awarded.

---

### TC-RB-019: Rakeback — Total Wagered Calculation

**Priority:** High
**Type:** Manual
**Estimate:** 30 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with bets placed
- Rakeback configured (e.g., 5% of total wagered)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as test player | Player logged in |
| 2 | Deposit $100 | Balance = $100 |
| 3 | Place bets totaling $500 | Total wagered = $500 |
| 4 | Wait for Rakeback calculation (daily) | Calculation time arrives |
| 5 | Navigate to Regular Bonuses | Rakeback card shows calculated amount |
| 6 | Verify Rakeback amount | Amount ≈ $25 (5% of $500) |

**Notes:** Rakeback is based on total wagered, not wins/losses.

---

### TC-RB-020: Rakeback — Bonus Bets May Not Contribute

**Priority:** Medium
**Type:** Manual
**Estimate:** 30 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with active bonus
- Bonus bets placed

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Activate bonus | Bonus active |
| 2 | Place bets using bonus funds | Bets placed |
| 3 | Check total wagered in BO | Wagered amount recorded |
| 4 | Check Rakeback calculation | Bonus bets may NOT contribute to rake |
| 5 | Verify Rakeback amount | Amount calculated only from real money bets |

**Notes:** Depends on configuration — bonus bets may not count toward rake.

---

## Section 5: Auto-Crediting (CT-44)

### TC-RB-021: Finished Bonus — Auto-Credit on Cancel

**Priority:** Critical
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-44
**Preconditions:**
- Player with active bonus
- Wagering requirement completed (status = Finished)
- Bonus has winnings > $0

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Complete wagering requirement | Status = Finished |
| 2 | Note current balance | Balance recorded (e.g., $50) |
| 3 | Note bonus winnings | Winnings = $30 (example) |
| 4 | Cancel bonus | Bonus cancelled |
| 5 | Check balance | Balance increased by $30 → $80 |
| 6 | Check bonus status | Status = Closed |
| 7 | Check FinalAmount field | FinalAmount = $30 |

**Notes:** CRITICAL — Winnings must be auto-credited when cancelling Finished bonus.

---

### TC-RB-022: Active Bonus — No Auto-Credit on Cancel

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-44
**Preconditions:**
- Player with active bonus
- Wagering requirement NOT completed (status = Active)
- Bonus has winnings > $0

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify bonus status = Active | Wagering not complete |
| 2 | Note current balance | Balance recorded (e.g., $50) |
| 3 | Note bonus winnings | Winnings = $30 (example) |
| 4 | Cancel bonus | Bonus cancelled |
| 5 | Check balance | Balance unchanged = $50 |
| 6 | Check bonus status | Status = Closed |
| 7 | Check FinalAmount field | FinalAmount = $0 |

**Notes:** Active (not Finished) bonuses do NOT credit winnings on cancel.

---

### TC-RB-023: Cash Bonus (No Wager) — Auto-Credit on Cancel

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-44
**Preconditions:**
- Player with CampaignCash bonus (no wagering)
- Bonus has amount > $0

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Activate CampaignCash bonus | Bonus active |
| 2 | Note current balance | Balance recorded (e.g., $50) |
| 3 | Note bonus amount | Amount = $20 (example) |
| 4 | Cancel bonus | Bonus cancelled |
| 5 | Check balance | Balance increased by $20 → $70 |
| 6 | Check bonus status | Status = Closed |

**Notes:** Cash bonuses without wager auto-credit on cancel.

---

## Section 6: E2E UI Tests

### TC-RB-024: UI — Bonus Card Displays Correct State

**Priority:** High
**Type:** Manual
**Estimate:** 10 min
**Related:** CT-61
**Preconditions:**
- Player with bonus in each state:
  - AwaitingForActivation
  - ReadyForActivation
  - CurrentlyWagering
  - ReadyForClaiming

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to Bonuses page | Page loads |
| 2 | Check AwaitingForActivation card | Button: "Play game" (disabled or no action) |
| 3 | Check ReadyForActivation card | Button: "Activate" (enabled) |
| 4 | Check CurrentlyWagering card | Button: "Play game" (enabled), Progress bar visible |
| 5 | Check ReadyForClaiming card | Button: "Claim $X" (enabled with amount) |

**Notes:** Each state must render correct button and UI elements.

---

### TC-RB-025: UI — Timer Countdown Display

**Priority:** Medium
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-559
**Preconditions:**
- Player with bonus in AwaitingForActivation state
- NextAvailableAt > 24 hours away

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to Bonuses page | Page loads |
| 2 | Find bonus card with timer | Timer visible |
| 3 | Check countdown format | Format: "X days Y hours Z minutes" |
| 4 | Wait 1 minute | Timer decrements by 1 minute |
| 5 | Check timer updates | Timer shows updated countdown |

**Notes:** Timer should countdown in real-time.

---

### TC-RB-026: UI — Progress Bar for Wagering Bonus

**Priority:** Medium
**Type:** Manual
**Estimate:** 20 min
**Related:** CT-61
**Preconditions:**
- Player with active bonus in CurrentlyWagering state
- Wagering requirement = $100

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to Bonuses page | Page loads |
| 2 | Find bonus card | Progress bar visible |
| 3 | Check initial progress | Progress = 0% |
| 4 | Place bets totaling $50 | Wagering = $50 |
| 5 | Refresh page | Progress bar updates to 50% |
| 6 | Place bets totaling $50 more | Wagering = $100 |
| 7 | Refresh page | Progress bar shows 100% |

**Notes:** Progress bar should reflect real-time wagering progress.

---

### TC-RB-027: UI — Regular Bonuses Section Layout

**Priority:** Low
**Type:** Manual
**Estimate:** 10 min
**Related:** CT-61
**Preconditions:**
- Player logged in
- Regular Bonuses configured

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to Bonuses page | Page loads |
| 2 | Scroll to Regular Bonuses section | Section visible |
| 3 | Check bonus cards layout | Cards arranged in grid/row |
| 4 | Verify 4 bonus types present | Rakeback, Cashback, Weekly, Monthly visible |
| 5 | Check card design | Each card shows: icon, title, amount/timer, button |

**Notes:** Visual layout verification.

---

## Section 7: Negative Tests

### TC-RB-028: Cannot Activate Two Wagering Bonuses Simultaneously

**Priority:** High
**Type:** Manual
**Estimate:** 15 min
**Related:** CT-45
**Preconditions:**
- Player with active bonus (with wagering)
- Player has another bonus (with wagering) in ReadyForActivation state

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify active bonus exists | Active bonus with wagering |
| 2 | Navigate to Regular Bonuses | Second bonus visible |
| 3 | Try to activate second bonus | Activation blocked |
| 4 | Check error message | "Cannot activate: active bonus exists" |

**Notes:** Only ONE wagering bonus can be active at a time.

---

### TC-RB-029: Cannot Claim Cashback Without Net Loss

**Priority:** High
**Type:** Manual
**Estimate:** 20 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with no net loss
- Cashback period (Tue/Fri)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as player with profit | Player logged in |
| 2 | Navigate to Regular Bonuses | Cashback card visible |
| 3 | Check Cashback amount | Amount = $0 or "Not available" |
| 4 | Try to activate | Cannot activate (no amount) |

**Notes:** Cashback requires net loss.

---

### TC-RB-030: Cannot Claim Rakeback Without Wagering

**Priority:** Medium
**Type:** Manual
**Estimate:** 15 min
**Related:** CRYPTO-459
**Preconditions:**
- Player with no bets placed
- Rakeback calculation period

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as new player | Player logged in |
| 2 | Navigate to Regular Bonuses | Rakeback card visible |
| 3 | Check Rakeback amount | Amount = $0 or "Not available" |
| 4 | Try to activate | Cannot activate (no amount) |

**Notes:** Rakeback requires total wagered > $0.

---

## Summary

**Total Test Cases:** 30

**Priority Distribution:**
- Critical: 2 (TC-RB-006, TC-RB-021)
- High: 20
- Medium: 6
- Low: 2

**Coverage:**
- Bonus States: 5 tests
- Parallel Claim: 6 tests
- Timer Logic: 5 tests
- Smartico Integration: 4 tests
- Auto-Crediting: 3 tests
- E2E UI: 4 tests
- Negative: 3 tests

**Related Tickets:**
- CT-45 (Parallel Claim) — 6 tests
- CT-44 (Auto-Crediting) — 3 tests
- CT-558 (Timer Logic) — 5 tests
- CT-559 (Timer UI) — 1 test
- CT-61 (UI) — 3 tests
- CRYPTO-459 (Regular Bonuses) — 4 tests
