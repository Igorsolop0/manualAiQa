# CT-752: Registration Modal - Google & Telegram Icons (Focused Test)

## Ticket
- **ID:** CT-752
- **URL:** https://next-t-code.atlassian.net/browse/CT-752
- **Objective:** Verify Google & Telegram auth options in registration modal

## Environment
- **URL:** https://minebit-casino.qa.sofon.one
- **Device:** Desktop Chrome only
- **Chrome Profile:** Profile 3 (existing Google session)
  - Path: `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`
  - **DO NOT** re-login or create new Google account

## CRITICAL: Test Flow (Execute EXACTLY)

### Step 1: Open Browser
- Launch Chrome with Profile 3
- Navigate to `https://minebit-casino.qa.sofon.one`

### Step 2: Find and Click Sign Up
- Locate the "Sign up" button
- Click it
- Screenshot: `01_before_signup.png`

### Step 3: Wait for Registration Modal
- Wait until registration modal is visible
- Confirm modal appears
- Screenshot: `02_registration_modal.png`

### Step 4: Verify Social Auth Options
Check if the modal contains TWO registration methods:
- ✅ Google icon/button present? (yes/no)
- ✅ Telegram icon/button present? (yes/no)
- Screenshot: `03_social_options_closeup.png` (zoomed if needed)

### Step 5: Optional - Monitor Auth Flow (if icons present)
- If Google icon exists: click it (do NOT complete auth, just monitor)
- Capture:
  - Console errors/warnings
  - Network requests (OAuth start, redirect, callback)
  - Status codes, request URLs
- Screenshot: `04_console_errors.png`
- Screenshot: `05_network_requests.png`

### Step 6: Evidence Collection
- Save all screenshots to `shared/test-results/CT-752/`
- Export console log (if errors found)
- Save network trace (HAR) if auth flow triggered

## Stagehand Configuration
- **Mode:** `auto` (enable for UI discovery)
- **Goals:**
  1. Find "Sign up" button
  2. Verify registration modal contains Google & Telegram icons

## Security Requirements
- **DO NOT** log raw tokens or secrets in report
- **DO NOT** complete auth flow (just monitor network requests)
- **DO NOT** create new accounts

## Output Requirements

### Short Summary
- Sign up button found? (yes/no)
- Registration modal appeared? (yes/no)
- Google icon present? (yes/no)
- Telegram icon present? (yes/no)

### Detailed Findings
**Console:**
- Number of errors
- Top 3 errors (descriptions, NO tokens)

**Network:**
- OAuth start request found? (yes/no)
- Redirect chain observed? (yes/no)
- Callback request found? (yes/no)
- Status codes (list)

**Break Point:**
- If failed to find: exact step where it stopped

### Evidence Paths
- List all screenshot files
- Console log file (if saved)
- Network trace file (if saved)

## DO NOT (Focus Guardrails)
- ❌ Do NOT test login flow
- ❌ Do NOT test timer badges
- ❌ Do NOT test bonuses
- ❌ Do NOT test other features
- ❌ Do NOT create new accounts
- ❌ Do NOT complete Google auth (just monitor)

## FOCUS
**ONLY TEST:** Sign up button → Registration modal → Google/Telegram icons presence
