# Task: PROD Bonus Stagehand Smoke Test

**Ticket:** PROD-BONUS-STAGEHAND-SMOKE
**Environment:** PROD
**URL:** https://minebit-casino.prod.sofon.one/
**Created:** 2026-03-13

---

## Stagehand Configuration

**Stagehand mode:** REQUIRED

This is an exploratory/discovery test. Stagehand MUST be used to find the correct path to Bonus section dynamically.

---

## Browser Goal (SINGLE GOAL)

**Goal:** "Open Minebit PROD homepage, find the Bonus button/section, navigate there, read the Bonuses page, find the 'Join now' action button, click it and observe what happens next."

---

## Test Flow

### Phase 1: Discovery
1. Navigate to https://minebit-casino.prod.sofon.one/
2. Use Stagehand to understand page structure
3. Find Bonus entry point (button/link/section)
4. Take screenshot + DOM snapshot

### Phase 2: Navigation
1. Navigate to Bonuses page
2. Read and document available bonuses
3. Find "Join now" or "Play Now" action button
4. Take screenshot + DOM snapshot

### Phase 3: Action
1. Click the "Join now" button
2. Observe what happens:
   - Redirect to registration?
   - Modal popup?
   - Login wall?
   - Error state?
3. Take screenshot of final state

---

## PROD Safety Rules (CRITICAL)

🚨 **DO NOT:**
- Make deposits
- Create new user accounts
- Execute risky or irreversible actions
- Fill in real personal data

✅ **ALLOWED:**
- Navigate and observe
- Click "Join now" to see where it leads
- Document login walls / auth requirements
- Take screenshots

---

## Evidence Output

**Save to:** `shared/test-results/PROD-BONUS-STAGEHAND-SMOKE/`

**Required artifacts:**
```
PROD-BONUS-STAGEHAND-SMOKE/
├── stagehand-output.json     # Full Stagehand log
├── screenshots/
│   ├── 01_homepage.png
│   ├── 02_bonus_entry.png
│   ├── 03_bonuses_page.png
│   ├── 04_join_now_button.png
│   └── 05_after_click.png
├── dom-snapshots/             # HTML state per phase
└── summary.json               # Final report
```

**summary.json must include:**
```json
{
  "success": true/false,
  "browser_goal_achieved": true/false,
  "bonus_entry_found": true/false,
  "join_now_clicked": true/false,
  "what_happened_after_click": "description",
  "redirect_url": "url or null",
  "login_wall_detected": true/false,
  "modal_detected": true/false,
  "error_state": "description or null",
  "key_findings": ["finding1", "finding2"],
  "screenshots_count": 5
}
```

---

## Success Criteria

✅ **Test passes if:**
1. Homepage loaded successfully
2. Bonus entry point found (button/link/section)
3. Navigated to Bonuses page
4. "Join now" button found and clicked
5. Final state documented (redirect/modal/login-wall/error)

❌ **Test fails if:**
1. URL not accessible
2. No Bonus entry found after reasonable discovery
3. Stagehand crashes or times out
4. Critical error prevents completion

---

## Execution Command

```bash
openclaw agent --id qa-agent --message "Execute PROD exploratory smoke test: workspace/shared/tasks/PROD-BONUS-STAGEHAND-SMOKE.md"
```

---

**Status:** READY FOR EXECUTION
