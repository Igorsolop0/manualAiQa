# Task: Stagehand Smoke Test - Auth Flow

**Task ID:** CT-STAGEHAND-SMOKE
**Проєкт:** Minebit (NextCode)
**Тип:** Stagehand Exploratory Smoke
**Дата:** 2026-03-12
**Агент:** Clawver (QA Agent)
**Environment:** PROD
**URL:** https://minebit-casino.prod.sofon.one

---

## Stagehand Configuration

**Stagehand Mode:** REQUIRED

**Browser Goal:**
```
Відкрити minebit PROD, знайти та відкрити Login/Register entrypoint, увійти існуючим тест-акаунтом, дійти до стану 'користувач авторизований і доступний профіль/меню'.
```

**Parameters:**
- maxSteps: 25
- timeoutMs: 90000
- screenshots: true
- domSnapshots: true

---

## PROD Safety Rules

**🚨 CRITICAL: DO NOT CREATE NEW USERS ON PROD!**

Use ONLY existing test account:
```
Email: test-ihorsolop0@nextcode.tech
Password: Qweasd123!
```

---

## Execution Steps

### Phase 1: Stagehand Discovery (REQUIRED MODE)

1. Navigate to PROD URL
2. Let Stagehand discover login/register entry point
3. Fill login form with existing credentials
4. Submit and wait for authenticated state
5. Verify profile/menu is accessible

**Stagehand should autonomously:**
- Find the login button (could be "Login", "Sign In", "Account" icon, etc.)
- Locate email/password fields
- Fill credentials
- Submit form
- Confirm authentication success

### Phase 2: Playwright Validation (Deterministic)

After Stagehand completes, validate with Playwright:

1. **Logout test:**
   - Find logout button
   - Click logout
   - Verify redirected to main page or login

2. **Post-logout verification:**
   - Try accessing profile URL directly
   - Should redirect to login or show "not authenticated"

---

## Output Requirements

Save all results to:
```
shared/test-results/CT-STAGEHAND-SMOKE/
```

**Required files:**
1. `stagehand-output.json` — Full Stagehand output
2. `stagehand-screenshots/` — Screenshots from Stagehand
3. `playwright-validation/` — Playwright validation results
4. `summary.md` — Final report with:
   - Success/Fail status
   - Steps taken by Stagehand
   - Any errors encountered
   - Playwright validation results

---

## Success Criteria

✅ **Stagehand:**
- Successfully logged in with existing credentials
- Reached authenticated state
- Profile/menu accessible

✅ **Playwright:**
- Logout works correctly
- Session cleared after logout
- Cannot access profile without authentication

❌ **Failure scenarios:**
- Stagehand couldn't find login entry point
- Credentials rejected
- Stagehand exceeded maxSteps
- Playwright validation failed

---

## When Done

Report to Nexus with:
1. `stagehand-output.json` path
2. `meta.artifactDir` path
3. Short conclusion (success/fail + reason)

<!-- PHASE2_DISPATCH_BLOCK_START -->
## Phase 2 Pilot Dispatch Hooks (Auto-generated)

- **run_id:** `CT-STAGEHAND-SMOKE-20260313-01`
- **agent:** `qa-agent`
- **mode:** `dual-write` (legacy + run mirror)

After execution, run mirror sync:
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --ticket CT-STAGEHAND-SMOKE
```

Fail-fast runtime guard (required before normal emit-result in Stagehand ONLY tasks):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py stagehand-guard --ticket CT-STAGEHAND-SMOKE --phase post --agent qa-agent --on-violation blocked --next-owner nexus --emit-result --write-results-stub
```

If auth/session was used in this run, register session-record (reference-only handoff):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py register-session --ticket CT-STAGEHAND-SMOKE --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login
```

Emit result packet for Nexus review:
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-result --ticket CT-STAGEHAND-SMOKE --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-STAGEHAND-SMOKE/results.json
```

Emit learning candidate (if run produced reusable insight):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-learning --ticket CT-STAGEHAND-SMOKE --owner qa-agent --status completed --observed "<observed>" --impact "<impact>" --applies-to "<applies-to>" --promote-to run-only --evidence-ref workspace/shared/test-results/CT-STAGEHAND-SMOKE/results.json
```

Nexus pre-summary gate (wait for stable results + validate contracts):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py pre-summary-gate --ticket CT-STAGEHAND-SMOKE
```
<!-- PHASE2_DISPATCH_BLOCK_END -->
