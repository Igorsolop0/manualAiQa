# CT-772: Bonuses Page UI Smoke Test (Production)

## Context
Ticket CT-772 introduces UI changes to the Bonuses page:
1. **Regular Bonuses** — New timer badge (circular, top-right, format: `13H:50M`)
2. **Special Bonuses** — Empty state banner ("Bonuses Coming Soon")

## Environment
- **URL:** https://minebit-casino.prod.sofon.one/
- **Credentials:**
  - Email: `democt7721773158046436@nextcode.tech`
  - Password: `Qweasd123!`
  - Client ID: 1184509
  - Balance: $100.00 USD

## Test Scenarios

### Scenario 1: Login & Navigation
1. Open https://minebit-casino.prod.sofon.one/
2. Click "Login" button
3. Enter credentials:
   - Email: `democt7721773158046436@nextcode.tech`
   - Password: `Qweasd123!`
4. Submit login form
5. Wait for successful login (user dashboard visible)
6. Navigate to Bonuses page (URL: `/bonuses` or `/bonuses-new`)

### Scenario 2: Regular Bonuses — Timer Badge UI
**Precondition:** Player has active bonuses (balance = $100)

**Test Steps:**
1. On Bonuses page, locate "Regular Bonuses" section
2. Verify timer badge appears:
   - Position: top-right of bonus card
   - Shape: circular
   - Label: "Ends in"
   - Format: `XXH:XXM` (NOT `XXh:XXm:XXs`)
3. Take screenshot
4. **Expected:** Timer badge matches design specs above

### Scenario 3: Special Bonuses — Empty State
**Test Steps:**
1. On Bonuses page, locate "Special Bonuses" section
2. If no special bonuses available, verify empty state:
   - Banner text: "Bonuses Coming Soon"
   - Description: "No special bonuses available right now. Stay tuned exciting rewards are on the way!"
3. Take screenshot
4. **Expected:** Empty state displays correctly

### Scenario 4: Locale Switching
**Test Steps:**
For each locale: **ru, de, es, fr, pt**

1. Switch language/locale to target locale
2. Refresh Bonuses page
3. Verify:
   - Timer badge format remains correct (`XXH:XXM`)
   - Empty state text is translated
   - No UI layout issues
4. Take screenshot for each locale

### Scenario 5: Responsive Check (Desktop + Mobile)
**Devices:**
- Desktop: MacBook Air (Chromium)
- Mobile: iPhone 14 viewport

**Test Steps:**
1. Test all above scenarios on Desktop
2. Switch to Mobile viewport (iPhone 14)
3. Re-test Scenarios 2-4
4. Take screenshots for both viewports
5. **Expected:** UI looks correct on both form factors

## Success Criteria
- ✅ Login successful
- ✅ Timer badge displays in correct format (`XXH:XXM`)
- ✅ Empty state displays for special bonuses (if applicable)
- ✅ All 5 locales render correctly
- ✅ UI responsive on Desktop + Mobile
- ✅ No console errors or layout issues

## Evidence Required
- Screenshots of:
  - Regular bonuses with timer badge
  - Special bonuses empty state (if applicable)
  - Each locale version
  - Desktop + Mobile viewports
- Video recording (optional but recommended)

## Notes
- **CRITICAL:** Use `getByRole()` and `getByText()` locators (Playwright best practices)
- Handle Smartico modals if they appear
- Use **ONLY Chromium browser** to save memory
- **Mobile viewport is MANDATORY** (not optional)

## Estimated Time
20-30 minutes

## Execution Command
```bash
openclaw agent --id qa-agent --message "Виконай цю таску: /Users/ihorsolopii/.openclaw/workspace/shared/tasks/CT-772_smoke_test.md"
```
