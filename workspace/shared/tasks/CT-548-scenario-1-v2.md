# CT-548: Google Linking — Stagehand Scenario 1

## Ticket
- **ID:** CT-548
- **URL:** https://next-t-code.atlassian.net/browse/CT-548
- **Status:** Ready for Testing

## Execution Policy
- **Tool:** Stagehand REQUIRED — use ONLY Stagehand, no Playwright test generation
- **Chrome Profile:** `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`
- **Environment:** QA
- **Test URL:** `https://minebit-casino.qa.sofon.one/test-social-linking`

## Stagehand Runner
- **Location:** `/Users/ihorsolopii/Documents/stagehand-runner`
- **Command:** `npm run run -- --input <payload.json> --pretty`

## Scenario 1: Google Linking Flow

### Test Credentials
- **Email:** `test-ihorsolop0@nextcode.tech`
- **Password:** `Qweasd123!`

### Steps
1. **Navigate to QA:** `https://minebit-casino.qa.sofon.one`
2. **Login via email/password:**
   - Click "Log In" button
   - Fill email: `test-ihorsolop0@nextcode.tech`
   - Fill password: `Qweasd123!`
   - Click "Start Playing"
   - Wait for login to complete
3. **Navigate to test-social-linking:**
   - Go to `https://minebit-casino.qa.sofon.one/test-social-linking`
4. **Link Google account:**
   - Find "Link Google" button
   - Click it
   - Google OAuth should use Chrome Profile 3 session
   - Select Google account from Profile 3
   - Complete authorization
5. **Verify:**
   - Check success message
   - Check Google appears in linked providers

### Stagehand Payload
```json
{
  "goal": "Login with test-ihorsolop0@nextcode.tech / Qweasd123!, navigate to test-social-linking, click Link Google button, complete Google OAuth using Chrome Profile 3, verify Google account is linked",
  "initialUrl": "https://minebit-casino.qa.sofon.one",
  "ticketId": "CT-548",
  "maxSteps": 30,
  "timeoutMs": 90000,
  "needScreenshots": true,
  "needDomSnapshots": true,
  "chromeProfile": "/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3"
}
```

## Evidence Path
- **Artifacts:** `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/stagehand/<timestamp>-<run>/`
- **Screenshots:** Each step
- **DOM Snapshots:** Each step
- **Output JSON:** Stagehand steps, artifacts, meta

## Success Criteria
- [ ] User logged in via email/password
- [ ] test-social-linking page accessible
- [ ] Google OAuth completed successfully
- [ ] Google appears in linked providers
- [ ] Evidence captured

## Known Issues
- QA env may not return `linkedRegistrationSources` — verify if present
- Stagehand may timeout on form fill — try again if partial success

## Output
After execution, report:
- Success/Failure status
- Steps completed (from Stagehand output)
- Evidence paths
- Any blockers or unexpected behavior
- Recommendation for next scenario
