# Exploratory Charter 1: User Authentication Flow

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing — Single Charter
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)
**Environment:** PROD
**URL:** https://minebit-casino.prod.sofon.one

---

## Test Charter

> **Explore** user registration, login, logout, and profile management
> **Using** Playwright snapshots, CRUD heuristics, state transitions
> **To discover** authentication edge cases, session handling issues, UX inconsistencies

## Scope

**In Scope:**
- Registration form validation (email, password strength, required fields)
- Login with valid/invalid credentials
- Profile page (view, update)
- Logout completeness (session cleared?)
- Session timeout behavior

**Out of Scope:**
- Payments, Deposit, Withdraw
- Other charters (lobby, games, bonuses, help)

## Credentials

Check `workspace/shared/credentials/` for existing test accounts.
If none found, check `minebit-e2e-playwright/src/fixtures/` for test data.
If no credentials available, create a new user via registration flow.

## Execution Steps

1. Navigate to main page → take snapshot → catalog all visible UI elements
2. Find and click Register/Login button
3. Test registration form (if accessible):
   - Valid data → success?
   - Empty fields → validation errors?
   - Weak password → rejected?
   - Already registered email → error message?
4. Test login:
   - Valid credentials → success?
   - Wrong password → error message?
   - Empty fields → validation?
5. Navigate to profile page → snapshot → catalog elements
6. Test logout → verify session cleared
7. Try accessing profile after logout → redirected to login?

## Snapshot Requirements

Save all screenshots to:
```
shared/test-results/exploratory-2026-03-11/charter-1-auth/
```

Naming: `01-main-page.png`, `02-register-form.png`, etc.

## Playwright Rules

Use ONLY `getByRole()` as primary locator:
```typescript
await page.getByRole('button', { name: 'Register' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
```

Fallback to getByText/getByLabel only with explanation in notes.

## Deliverables

1. Screenshots in `charter-1-auth/`
2. `charter-1-auth/notes.md` — session notes with action log
3. `charter-1-auth/elements.md` — functional elements catalog (role, locator, behavior)
4. `charter-1-auth/defects.md` — any defects found (if any)

## When Done

Report to Nexus: "Charter 1 (Auth) завершено. Результати: shared/test-results/exploratory-2026-03-11/charter-1-auth/"
