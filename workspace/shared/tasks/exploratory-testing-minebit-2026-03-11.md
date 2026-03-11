# Exploratory Testing Plan — Minebit iGaming

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)

---

## 1. Мета та підхід

**Exploratory Testing** — одночасне вивчення продукту, проєктування тестів і їх виконання під час сесії.

**Ключові принципи:**
- Не виконуєш наперед написані кейси
- Сам ставиш гіпотези, шукаєш ризики
- Варіюєш сценарії за результатами попередніх
- Працюєш за коротким test charter

---

## 2. Scope / Out of Scope

### ✅ In Scope
- Реєстрація, логін, лог-аут, профіль
- Лобі казино: список ігор, фільтри, пошук, категорії
- Відкриття ігор, базові інтеракції (без реальних фінансових операцій)
- Бонуси, промо, туторіали, help/FAQ, навігація, меню, хедер/футер

### ❌ Out of Scope
- Payments
- Deposit
- Withdraw

---

## 3. Test Charters (3-5 сесій)

### Charter 1: User Authentication Flow

> **Explore** user registration, login, logout, and profile management
> **Using** Playwright snapshots, CRUD heuristics, state transitions
> **To discover** authentication edge cases, session handling issues, UX inconsistencies

**Test object:** Auth flow (registration → login → profile → logout)

**Focus areas:**
- Registration form validation (email, password strength, required fields)
- Login with valid/invalid credentials
- Password reset flow
- Profile update functionality
- Session timeout behavior
- Logout completeness (session cleared?)

**Risks to find:**
- SQL injection attempts in input fields
- Session hijacking vulnerabilities
- Incomplete logout (tokens not cleared)
- Profile data not persisting
- UX: confusing error messages

**Heuristics:**
- CRUD (Create/Read/Update/Delete user)
- Error guessing (invalid inputs)
- Boundaries (password length limits)
- State transitions (logged in → logged out)

---

### Charter 2: Casino Lobby Navigation

> **Explore** casino lobby filters, game search, categories, and navigation
> **Using** Playwright getByRole, snapshots, navigation heuristics
> **To discover** filtering bugs, navigation issues, performance problems, UX gaps

**Test object:** Casino lobby (home page, game list, filters)

**Focus areas:**
- Game filters (provider, category, type, popularity)
- Search functionality (partial matches, no results)
- Category tabs (Slots, Live Casino, Table Games)
- Sorting options (A-Z, Popular, New)
- Pagination / infinite scroll
- Game cards display (thumbnails, titles, provider badges)
- Quick vs. Full game launch

**Risks to find:**
- Filters not applying correctly
- Search returning wrong results
- Category mismatch (game in wrong category)
- Performance: slow loading on large lists
- UX: filter state not persisting after game open/close

**Heuristics:**
- CRUD (filter selections)
- Boundaries (empty results, max results)
- State transitions (filter apply → clear → reapply)
- Error guessing (special characters in search)

---

### Charter 3: Game Launch & Interaction

> **Explore** game opening, in-game controls, and return to lobby
> **Using** Playwright snapshots, interaction testing, timing checks
> **To discover** game loading issues, control responsiveness, navigation bugs

**Test object:** Game page (game frame, controls, UI)

**Focus areas:**
- Game loading (progress indicator, timeout handling)
- In-game controls (spin, stop, auto-play, bet amount, lines)
- Settings panel (sound, speed, quality)
- Balance display (if visible)
- Return to lobby button
- Game crash / error handling
- Multiple games in tabs (if supported)

**Risks to find:**
- Game not loading (stuck at 0%)
- Controls unresponsive during animation
- Bet amount changing unexpectedly
- Return to lobby losing session state
- Game frame not resizing properly

**Heuristics:**
- State transitions (idle → spinning → result)
- Boundaries (min/max bet, max lines)
- Timing (rapid clicks, slow network)
- Error guessing (bet with 0 balance)

---

### Charter 4: Bonuses & Promotions UI

> **Explore** bonuses list, promo pages, and bonus activation UI
> **Using** Playwright snapshots, navigation, UI validation
> **To discover** display issues, broken links, missing info, UX confusion

**Test object:** Bonuses page, promo banners, bonus activation modals

**Focus areas:**
- Bonus list display (thumbnails, titles, terms)
- Promo banners in lobby
- Bonus terms & conditions readability
- Bonus activation button (UI only, no real activation)
- Expired bonuses display
- Bonus categories / filters

**Risks to find:**
- Broken images or links
- Terms not accessible
- Expired bonuses still shown
- Bonus UI inconsistent across pages
- Mobile vs. desktop layout issues

**Heuristics:**
- CRUD (view bonus list)
- State transitions (active → expired)
- Boundaries (many bonuses in list)
- Consistency (same bonus shown differently)

---

### Charter 5: Help/FAQ & Navigation

> **Explore** help pages, FAQ, footer links, and overall navigation
> **Using** Playwright snapshots, link validation, accessibility checks
> **To discover** broken links, outdated content, missing help topics

**Test object:** Help/FAQ, footer, navigation menu

**Focus areas:**
- FAQ search functionality
- Help categories navigation
- Footer links (Terms, Privacy, Responsible Gaming)
- Header navigation (home, lobby, profile, logout)
- Breadcrumbs (if present)
- External links (open in new tab?)

**Risks to find:**
- 404 errors on help pages
- Outdated FAQ content
- Links opening in same tab (losing game session)
- Missing critical help topics (payments, limits)
- Accessibility issues (no alt text, poor contrast)

---

## 4. Snapshot Requirements

**Для кожної суттєвої сторінки:**

1. **Зроби скріншот** сторінки:
   ```bash
   # Playwright example
   await page.screenshot({ path: 'screenshots/<charter>_<page>_<timestamp>.png', fullPage: true });
   ```

2. **Збережи в структуру:**
   ```
   shared/test-results/exploratory-2026-03-11/
   ├── charter-1-auth/
   │   ├── 01-registration-form.png
   │   ├── 02-login-page.png
   │   ├── 03-profile-page.png
   │   └── notes.md
   ├── charter-2-lobby/
   │   ├── 01-lobby-filters.png
   │   ├── 02-game-search.png
   │   └── notes.md
   └── ...
   ```

3. **Визнач функціональні елементи** для кожного snapshot:
   - Основні кнопки (Play, Register, Login, Logout, Spin, etc.)
   - Поля вводу (email, password, search, filters)
   - Навігаційні елементи (меню, вкладки, категорії)
   - Елементи управління грою (spin, stop, auto-play, bet amount)

4. **Зафіксуй для кожного елемента:**
   - Роль (button, link, textbox, combobox, menuitem)
   - Очікувану поведінку
   - Playwright локатор

---

## 5. Playwright Locator Rules (CRITICAL)

**Пріоритет локаторів:**

1. **getByRole()** — головний метод
   ```typescript
   await page.getByRole('button', { name: 'Register' }).click();
   await page.getByRole('link', { name: 'Casino' }).click();
   await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
   await page.getByRole('tab', { name: 'Slots' }).click();
   await page.getByRole('button', { name: 'Spin' }).click();
   ```

2. **Fallback (тільки якщо getByRole не підходить):**
   - `getByText()` — коли потрібно знайти текст
   - `getByLabel()` — для полів з label
   - `getByPlaceholder()` — для полів з placeholder
   - `getByTestId()` — якщо є data-testid

3. **Заборонено:**
   - Довільні CSS селектори (`page.locator('.btn-primary')`)
   - XPath (`page.locator('//button')`)
   - Використання fallback без пояснення в нотатках

**Приклад логування fallback:**
```
Element: Game filter dropdown
Role: Not accessible via getByRole (custom dropdown)
Fallback: page.getByLabel('Filter by provider')
Reason: Dropdown uses custom implementation without proper ARIA role
```

---

## 6. Logging Format

**Для кожної дії під час сесії:**

```markdown
### Test Action Log

| Time | Action | Input | Expected | Actual | Status | Screenshot |
|------|--------|-------|----------|--------|--------|------------|
| 14:32 | Click Register button | - | Registration form opens | Form opened | ✅ PASS | 01-registration-form.png |
| 14:33 | Fill email field | "test@example.com" | Field filled | Field filled | ✅ PASS | 02-registration-filled.png |
| 14:34 | Submit with weak password | "123" | Error message shown | No error, form submitted | ❌ FAIL | 03-weak-password-bug.png |
```

**Спостереження / дефекти:**
```markdown
### Defects Found

**DEF-001: Weak password accepted**
- Location: Registration form
- Steps: Enter password "123" → Submit
- Expected: Error message "Password must be 8+ characters"
- Actual: Form submitted successfully
- Severity: High
- Screenshot: 03-weak-password-bug.png
- Playwright locator: `page.getByRole('textbox', { name: 'Password' })`

**DEF-002: Filter state not persisting**
- Location: Casino lobby
- Steps: Apply filter "Provider: NetEnt" → Open game → Return to lobby
- Expected: Filter still applied
- Actual: Filter cleared, showing all games
- Severity: Medium
- Screenshot: 05-filter-state-bug.png
```

---

## 7. Deliverables

Після завершення сесій:

1. **Screenshots** → `shared/test-results/exploratory-2026-03-11/screenshots/`
2. **Session notes** → `shared/test-results/exploratory-2026-03-11/notes.md`
3. **Defects list** → `shared/test-results/exploratory-2026-03-11/defects.md`
4. **Functional elements catalog** → `shared/test-results/exploratory-2026-03-11/ui-elements.md`
5. **TestRail candidates** (optional) → potential test cases from findings

---

## 8. Execution Commands

### Start exploratory session:
```bash
cd /Users/ihorsolopii/Documents/minebit-e2e-playwright
npx playwright test tests/exploratory/exploratory-charter-1.spec.ts --headed
```

### Snapshot script template:
```typescript
// tests/exploratory/helpers/snapshot-helper.ts
import { Page } from '@playwright/test';

export async function captureSnapshot(
  page: Page, 
  charter: string, 
  pageName: string
): Promise<string> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `${charter}_${pageName}_${timestamp}.png`;
  const filepath = `shared/test-results/exploratory-2026-03-11/screenshots/${filename}`;
  
  await page.screenshot({ path: filepath, fullPage: true });
  
  return filepath;
}
```

---

## 9. Questions for Ihor (Before Starting)

1. **Environment:** QA or Dev?
2. **Test account:** Should I use existing test credentials or create new?
3. **VPN required?** If yes, which country?
4. **Device priority:** Desktop Chrome first, then mobile?
5. **Timebox per charter:** 30-45 minutes recommended. Agreed?
6. **Game providers:** Any specific providers to test? (NetEnt, Evolution, Pragmatic Play, etc.)

---

**Created by:** Nexus (Orchestrator)
**For:** Clawver (QA Agent)
**Status:** Ready for approval
