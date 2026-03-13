# CT-752: Registration Modal - Google & Telegram Icons

## Ticket
- **ID:** CT-752
- **URL:** https://next-t-code.atlassian.net/browse/CT-752

## CRITICAL TASK (Follow EXACTLY)

### Step-by-Step Instructions:
1. Navigate to: `https://minebit-casino.qa.sofon.one`
2. Find and click the "Sign up" button
3. Wait for the registration modal to appear
4. Verify that the registration modal contains TWO social registration options:
   - Google icon/button
   - Telegram icon/button
5. Take screenshots of:
   - The page before clicking Sign up
   - The registration modal with Google and Telegram icons
6. Capture console errors and network requests
7. Report findings

## Stagehand Mode
- **ENABLED** (use Stagehand for UI discovery)

## Browser Configuration
- Desktop Chrome
- Use Chrome Profile 3 (existing Google session)
- Profile path: `/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 3`

## Output Required
Report:
- Was "Sign up" button found? (yes/no)
- Was registration modal visible after clicking? (yes/no)
- Were Google and Telegram icons present in modal? (yes/no)
- Any console errors?
- Any network errors?
- Screenshots saved to `shared/test-results/CT-752/`

## Security
- Do NOT log raw tokens or secrets
- Do NOT create new accounts
- Do NOT re-login to different Google account

## DO NOT
- Do NOT test login flow (unless requested)
- Do NOT test timer badges
- Do NOT test bonuses
- Do NOT test other features

## FOCUS
Only test: Sign up button → Registration modal → Google/Telegram icons
