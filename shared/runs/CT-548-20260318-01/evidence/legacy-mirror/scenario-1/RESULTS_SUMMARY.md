# CT-548 Scenario 1: Stagehand Testing Results

## Статус: PARTIAL — Login blocker

## Виконано
- **Stagehand runs:** 3 спроби
- **Runner:** /Users/ihorsolopii/Documents/stagehand-runner
- **Chrome Profile:** Profile 3 (specified but not effectively used)

## Запуски

### Запуск 1 (19:11) — Login via email/password
- **Steps:** 8 кроків
- **Progress:**
  1. ariaTree
  2. Click Log In
  3. wait
  4. ariaTree
  5. fillForm (спроба)
  6. Click Start Playing
  7. wait
  8. screenshot
- **Problem:** timeout на login modal — credentials не заповнені коректно
- **Artifacts:** `CT-548/stagehand/20260315-191118-login-as-test-user-via-email-password-navigate/`
- **Screenshots:** 9 скріншотів (initial + 8 steps)

### Запуск 2 (19:16) — Login retry
- **Steps:** 20 кроків
- **Progress:**
  - Login modal відкритий
  - Email textbox clicked, keys typed
  - Password textbox clicked, keys typed
  - Start Playing clicked (3x)
- **Problem:** timeout — login не завершився, залишається на modal
- **Artifacts:** `CT-548/stagehand/20260315-191612-login-as-test-user-via-email-password-navigate/`
- **Screenshots:** 21 скріншот
- **Root cause:** Stagehand не може коректно заповнити login form

### Запуск 3 (19:20) — Direct to test-social-linking (skip login)
- **Steps:** 6 кроків
- **Progress:**
  1. ariaTree
  2. screenshot
  3. scroll
  4. screenshot
  5. scroll
  6. screenshot
- **Problem:** test-social-linking сторінка порожня для не залогінених користувачів
- **Artifacts:** `CT-548/stagehand/20260315-192015-navigate-to-test-social-linking-page-find-and-c/`
- **Screenshots:** 7 скріншотів
- **Root cause:** Social linking UI доступна тільки для logged-in users

## Key Findings

1. **Stagehand cannot handle login form reliably**
   - fillForm action не працює коректно з Minebit login modal
   - Manual typing (keys) спрацював але login не завершився

2. **test-social-linking requires auth**
   - URL `https://minebit-casino.qa.sofon.one/test-social-linking` показує UI тільки для залогінених користувачів
   - Без auth сторінка порожня або redirect

3. **Chrome Profile 3 integration unclear**
   - Profile path specified but Stagehand не використовує існуючу Google session
   - OAuth popup requires active Google session

## Recommendations

### Option 1: Manual login + Stagehand
1. User logs in manually in Chrome Profile 3:
   ```
   open -na "Google Chrome" --args --profile-directory="Profile 3" "https://minebit-casino.qa.sofon.one"
   ```
2. Login with test-ihorsolop0@nextcode.tech / Qweasd123!
3. Navigate to test-social-linking
4. Run Stagehand with goal "Link Google account, complete OAuth, verify linked"

### Option 2: Playwright with CDP connection
1. Launch Chrome Profile 3 with CDP port
2. Connect Playwright to CDP session
3. Execute linking flow in existing context

### Option 3: API-first approach
1. Use API to get auth token
2. Use token to navigate directly to test-social-linking
3. Handle Google linking separately

## Next Steps
- Confirm which option Ihor prefers
- If Option 1: provide manual login instructions
- If Option 2: set up CDP connection
- If Option 3: get API endpoint info

## Evidence Paths
- Run 1: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/stagehand/20260315-191118-login-as-test-user-via-email-password-navigate/`
- Run 2: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/stagehand/20260315-191612-login-as-test-user-via-email-password-navigate/`
- Run 3: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/stagehand/20260315-192015-navigate-to-test-social-linking-page-find-and-c/`
