# Deposit Streak — Manual Test Cases (TestRail Format)

**Project:** Minebit
**Section:** Bonuses → Deposit Streak
**Related Tickets:** CT-??? (Deposit Streak feature)
**Created:** 2026-03-03
**Author:** Panda Sensei
**Status:** Draft

---

## Section: Deposit Streak — Basic Flow

### Basic Flow — 2 Deposits → Bonus → Claim

**Priority:** High
**Type:** Manual (E2E)
**Estimate:** 15 min
**Preconditions:**
- New player registered with non‑test email (e.g., `john.doe123@nextcode.tech`)
- Player has at least $60 USD balance (or payment method ready for two $30 deposits)
- Deposit Streak campaign is active on the environment

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as the new player | Player logged in successfully |
| 2 | Navigate to Bonuses page | Bonuses page loads |
| 3 | Make first deposit of $30 USD through the payment UI | Deposit succeeds, balance updates |
| 4 | Refresh Bonuses page | No Deposit Streak bonus card appears |
| 5 | Make second deposit of $30 USD through the payment UI | Deposit succeeds, balance updates |
| 6 | Refresh Bonuses page | Deposit Streak bonus card appears with status "Ready to claim" |
| 7 | Click the "Claim" button on the bonus card | Toast notification "Bonus claimed successfully" appears |
| 8 | Verify player balance | Balance increases by the bonus amount |
| 9 | Return to Bonuses page | Deposit Streak card is no longer visible |

**Notes:**
- Bonus should appear only after the second deposit.
- Bonus amount depends on campaign configuration (e.g., $5, $10).
- If bonus does not appear, check player segmentation (should not be in test segments like "All users Test OQ").

---

### Deposit Below Minimum Amount — No Bonus

**Priority:** Medium
**Type:** Manual (E2E)
**Estimate:** 10 min
**Preconditions:**
- New player registered with non‑test email
- Player has at least $58 USD balance
- Minimum deposit for Deposit Streak is $30 (confirm with campaign settings)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as the new player | Player logged in successfully |
| 2 | Make first deposit of $29 USD (below minimum) | Deposit succeeds, balance updates |
| 3 | Make second deposit of $29 USD | Deposit succeeds, balance updates |
| 4 | Navigate to Bonuses page | No Deposit Streak bonus card appears |
| 5 | (Optional) Make a third deposit of $30 USD | Bonus still does not appear (only consecutive deposits ≥ $30 count) |

**Notes:**
- Deposits below the minimum amount should not increment the deposit streak counter.
- If bonus appears, campaign minimum‑amount logic is broken.

---

### Full Cycle — 10 Deposits (4 Bonuses)

**Priority:** Medium
**Type:** Manual (E2E)
**Estimate:** 30 min
**Preconditions:**
- New player registered with non‑test email
- Player has at least $300 USD balance (or payment method for 10 deposits)
- Deposit Streak campaign active

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as the new player | Player logged in successfully |
| 2 | Make 10 consecutive deposits of $30 USD each | All deposits succeed |
| 3 | After each deposit, refresh Bonuses page | Track when bonus cards appear |
| 4 | Verify bonus appearance pattern | Bonuses appear **only** after deposits 2, 4, 8, 10 |
| 5 | Claim each bonus as it appears | Each bonus is claimed successfully, balance increases accordingly |
| 6 | After 10 deposits, count total bonuses claimed | Exactly 4 bonuses have been claimed |

**Notes:**
- The streak resets after each bonus? (Check campaign rules – may continue counting.)
- If bonuses appear on wrong deposits, streak‑counting logic is broken.

---

## Section: Deposit Streak — Edge Cases

### Different Currencies (If Supported)

**Priority:** Low
**Type:** Manual (E2E)
**Estimate:** 15 min
**Preconditions:**
- Deposit Streak campaign supports multiple currencies (USD, EUR, CAD)
- Player registered with supported non‑USD currency
- Player has sufficient balance in that currency

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as the player | Player logged in successfully |
| 2 | Make two deposits in the non‑USD currency (≥ minimum equivalent) | Deposits succeed |
| 3 | Navigate to Bonuses page | Deposit Streak bonus card appears with correct currency symbol |
| 4 | Claim the bonus | Bonus amount is credited in the player’s currency |

**Notes:**
- Bonus amount may be fixed in USD and converted, or be currency‑specific.
- If bonus does not appear, campaign may not be configured for that currency.

---

### Wallet Correction Does Not Trigger Bonus

**Priority:** Low
**Type:** Manual (API‑assisted)
**Estimate:** 10 min
**Preconditions:**
- New player registered with non‑test email
- Access to BackOffice/Wallet API for balance corrections

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as the player | Player logged in successfully |
| 2 | Via Wallet API, credit $30 to player’s balance (CreateDebitCorrection) | Balance increases |
| 3 | Repeat with another $30 credit | Balance increases again |
| 4 | Navigate to Bonuses page | **No** Deposit Streak bonus card appears |

**Notes:**
- Only real payment‑flow deposits (MakeManualRedirectPayment → MarkAsPaid) should trigger the streak.
- If bonus appears after Wallet corrections, trigger logic is wrong.

---

## Section: Deposit Streak — UI Validation

### Bonus Card Elements & States

**Priority:** Low
**Type:** Manual (UI)
**Estimate:** 5 min
**Preconditions:**
- Player has triggered a Deposit Streak bonus (after 2 deposits)

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to Bonuses page | Deposit Streak card is visible |
| 2 | Check card title | Shows "Deposit Streak" (or campaign‑specific name) |
| 3 | Check bonus amount | Displays correct amount (e.g., "$5") |
| 4 | Check claim button | Button is enabled, reads "Claim" |
| 5 | Check any progress indicator | If present, shows correct progress (e.g., "2/2 deposits") |
| 6 | Click "Claim" | Button becomes disabled, toast "Bonus claimed successfully" appears |
| 7 | Refresh page | Card disappears |

**Notes:**
- UI should match the design spec.
- If progress indicator is missing or incorrect, frontend logic may be broken.

---

## Appendix: Test Data & Automation Notes

**Test Player Creation:**
- Use non‑test email pattern: `[random-string]@nextcode.tech`
- Avoid `test-*`, `demo-*`, `user-*` prefixes to bypass test segmentation.
- For manual testing, can use real payment methods (stripe, etc.) or BackOffice manual deposits (MakeManualRedirectPayment → MarkAsPaid).

**Automation Scripts Available:**
- `deposit_streak_auto.py` – Automates deposit creation via BackOffice UI API (Bearer token).
- Requires valid Bearer token (expires every ~3 hours) and player ID.

**Known Issues (as of 2026‑03‑03):**
- Players with `@nextcode.tech` emails may still be placed into test segments; verify segmentation in BackOffice.
- Deposit Streak campaign may be inactive on PROD for new players – confirm with devs.
- Payment method ID 19 (test method) may not trigger bonuses even after MarkAsPaid.

**References:**
- BackOffice UI API: `https://backoffice.prod.sofon.one/mgw/admin/`
- Wallet API: `https://wallet.prod.sofon.one`
- Campaign configuration in BackOffice → Campaigns → Deposit Streak

---

*Document generated by OpenClaw Assistant based on Deposit Streak testing session 2026‑03‑03.*