# CT-752: Google Auth / Google-linked Flow Testing (Registration Modal)

## Ticket
- **ID:** CT-752
- **URL:** https://next-t-code.atlassian.net/browse/CT-752
- **Title:** Handle Linked Registration Sources from GetClientByToken

## Task Type
UI Testing + DevTools Monitoring (Console + Network)

## Environment
- **URL:** https://minebit-casino.qa.sofon.one
- **Environment:** QA
- **Device:** Desktop Chrome
- **Browser Profile:** Profile 3 (Google Chrome)
  - Source: `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`
  - **CRITICAL:** Use existing Google session in Profile 3
  - **DO NOT** re-login to another Google account
  - **DO NOT** create new Google account

## Test Objective
Verify Google auth flow in registration modal and capture:
1. UI behavior (Sign up button → Registration modal → Google/Telegram icons)
2. Console errors/warnings
3. Network activity (OAuth start, redirects, callbacks, status codes)
4. No token leakage in logs

## Stagehand Configuration
- **Stagehand mode:** `auto` (enabled for unstable UI discovery)
- **Browser goals:** Find and interact with Sign up button, wait for registration modal, verify Google/Telegram icons

## Test Flow
1. Open `https://minebit-casino.qa.sofon.one`
2. Click "Sign up" button
3. Wait for registration modal to be visible
4. Verify two registration options are present:
   - Google icon
   - Telegram icon
5. Click Google icon (if present)
6. Monitor and capture:
   - Console errors/warnings
   - Network requests (OAuth start, redirect chain, callback)
   - Status codes, request URLs, response body/error clues
7. **SECURITY:** Do NOT log raw tokens/secrets in report

## Expected Behavior
- Registration modal should appear after clicking "Sign up"
- Two social registration options: Google + Telegram
- Google auth should start OAuth flow
- Network should show OAuth start request, redirect chain, callback

## Evidence Requirements
Save to `shared/test-results/CT-752/`:
- Screenshots at each step
- Network trace (HAR file)
- Console log export
- `results.json` with structured findings

## Output Format
Return in `results.json`:
```json
{
  "status": "completed|failed|partial",
  "reproduced": true|false,
  "breakStep": "step where issue occurs",
  "consoleFindings": {
    "errors": [...],
    "warnings": [...],
    "tokenLeakage": true|false
  },
  "networkFindings": {
    "getClientByTokenCalls": [...],
    "oauthStartRequest": {...},
    "redirectChain": [...],
    "callbackStatus": {...},
    "errors": [...]
  },
  "uiFindings": {
    "signUpButtonFound": true|false,
    "registrationModalVisible": true|false,
    "googleIconPresent": true|false,
    "telegramIconPresent": true|false
  },
  "evidencePaths": {
    "screenshots": [...],
    "networkTrace": "...",
    "consoleLog": "..."
  }
}
```

## Constraints
- Desktop Chrome only
- Use Chrome Profile 3 (existing Google session)
- Capture DevTools data (console + network)
- No raw tokens in output
- Stagehand mode: auto
