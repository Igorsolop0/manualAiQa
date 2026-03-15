# CT-548: Google Account Linking — Scenario 1 (Exploratory)

## Ticket
- **ID:** CT-548
- **URL:** https://next-t-code.atlassian.net/browse/CT-548
- **Status:** Ready for Testing

## Task Scope
**One scenario only:** Link Google account to existing user

## Execution Policy
- **Tool:** Stagehand REQUIRED (exploratory, OAuth flow)
- **Stagehand ONLY** — do NOT create Playwright tests
- **Chrome Profile:** `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`
- **Environment:** QA
- **Test URL:** `https://minebit-casino.qa.sofon.one/test-social-linking`

**CRITICAL:**
1. Use `stagehand` CLI/tool for UI discovery
2. Do NOT generate Playwright test files
3. Stagehand should navigate and interact with the browser
4. Capture evidence via Stagehand output

## Pre-conditions
1. User logged in via email/password (create account if needed)
2. Google NOT yet linked to this account
3. Google Profile 3 available for OAuth

## Stagehand Payload (USE THIS)

**Runner:** `/Users/ihorsolopii/Documents/stagehand-runner`

**Goal:** "Login as test user via email/password, navigate to test-social-linking page, click Link Google button, complete Google OAuth using Chrome Profile 3, verify Google account is linked"

**Initial URL:** `https://minebit-casino.qa.sofon.one`

**Command:**
```bash
RUNNER_DIR="/Users/ihorsolopii/Documents/stagehand-runner"
TASK_OUT_DIR="/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/scenario-1"
mkdir -p "$TASK_OUT_DIR"

PAYLOAD_FILE="$TASK_OUT_DIR/stagehand-payload.json"

cat > "$PAYLOAD_FILE" <<'JSON'
{
  "goal": "Login as test user, navigate to test-social-linking page, click Link Google button, complete Google OAuth using Chrome Profile 3, verify Google account is linked",
  "initialUrl": "https://minebit-casino.qa.sofon.one",
  "ticketId": "CT-548",
  "maxSteps": 40,
  "timeoutMs": 120000,
  "needScreenshots": true,
  "needDomSnapshots": true,
  "chromeProfile": "/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3"
}
JSON

cd "$RUNNER_DIR"
npm run run -- --input "$PAYLOAD_FILE" --pretty
```

**Test Account:**
- Email: `test-ihorsolop0@nextcode.tech`
- Password: `Qweasd123!`

## Expected Evidence
1. **Screenshots:**
   - Login/registration page
   - test-social-linking page (before linking)
   - Google OAuth popup (if captured)
   - Success state (after linking)
   - Profile showing linked Google account

2. **Network requests:**
   - Auth token in linking request payload
   - `/GoogleAccount/GetAuthUrl` response
   - Player object with `linkedRegistrationSources`

3. **Artifacts folder:**
   - `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/scenario-1/`

## Success Criteria
- [ ] User authenticated via email/password
- [ ] test-social-linking page accessible
- [ ] Google OAuth completed successfully
- [ ] `linkedRegistrationSources` includes "Google"
- [ ] Evidence captured for each step

## Known Issues
- QA env may not return `linkedRegistrationSources` — check if fixed

## Output
After completion, report:
- What happened at each step
- Any blockers or unexpected behavior
- Evidence paths
- Recommendation for next scenario
