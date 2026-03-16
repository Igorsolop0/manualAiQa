# CT-548: Scenario 2 — Sign Up → Google Linking

## Ticket
- **ID:** CT-548
- **URL:** https://next-t-code.atlassian.net/browse/CT-548
- **Status:** Ready for Testing

## Execution Policy
- **Tool:** Stagehand REQUIRED
- **Chrome Profile:** `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`
- **Environment:** QA
- **Test URL:** `https://minebit-casino.qa.sofon.one`

## Stagehand Payload

```json
{
  "goal": "Click Sign Up, create new account via email/password, navigate to test-social-linking page, find Link Google button, complete Google OAuth using Chrome Profile 3, verify Google account is linked",
  "initialUrl": "https://minebit-casino.qa.sofon.one",
  "ticketId": "CT-548",
  "maxSteps": 35,
  "timeoutMs": 120000,
  "needScreenshots": true,
  "needDomSnapshots": true,
  "chromeProfile": "/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3",
  "testCredentials": {
    "email": "test-ct548-<timestamp>@nextcode.tech",
    "password": "TestPass123!"
  }
}
```

## Flow
1. Navigate to QA
2. Click "Sign Up"
3. Fill registration form:
   - Email: test-ct548-<timestamp>@nextcode.tech
   - Password: TestPass123!
4. Complete registration
5. Navigate to test-social-linking
6. Click "Link Google"
7. Complete Google OAuth (Profile 3)
8. Verify Google linked

## Evidence Path
- `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/stagehand/<timestamp>-<run>/`

## Success Criteria
- [ ] New account created
- [ ] test-social-linking accessible
- [ ] Google OAuth completed
- [ ] Google appears in linked providers
- [ ] Evidence captured
