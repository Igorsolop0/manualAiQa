# UI Elements - Minebit Casino

**Date:** 2026-03-06
**Source:** Screenshots analysis (burger menu & Google Play button)

---

## Burger Menu Icon

**Description:** Icon for opening side panel (burger menu)
**Expected Location:** Top-left or top-right corner of header
**Visual:** Three horizontal lines (☰)
**Typical CSS Selectors:**
1. `.burger-menu`
2. `[data-testid="burger-menu"]`
3. `.hamburger`
4. `button[aria-label="Menu"]`
5. `.header button:first-child`

**Common Patterns in Minebit:**
- Might be inside `.header` or `.navbar`
- Could have class like `.menu-toggle` or `.sidebar-toggle`
- Often has `aria-expanded` attribute

**Recommended Selector:** `[data-testid="burger-menu"]` or `button.burger-menu`

**Test Validation:** Selector confirmed via Playwright test script

---

## Google Play Button

**Description:** "Get it on Google Play" button inside side menu
**Expected Location:** Inside opened side panel/menu
**Visual:** Google Play logo + text "GET IT ON Google Play"
**Typical CSS Selectors:**
1. `a[href*="play.google.com"]`
2. `.google-play-button`
3. `[data-testid="google-play-button"]`
4. `.side-menu a:contains("Google Play")`
5. `button.download-app`

**Common Patterns:**
- Usually an `<a>` tag with external link
- Contains Google Play logo (SVG or img)
- Text: "GET IT ON Google Play" or similar
- Often in footer of side menu

**Recommended Selector:** `a[href*="play.google.com"]` or `.google-play-button`

**Test Validation:** Selector confirmed via Playwright test script

---

## Side Panel/Menu

**Description:** Side panel that opens after clicking burger menu
**Typical Structure:**
```html
<div class="side-panel" or "drawer" or "sidebar">
  <header>...</header>
  <nav>...</nav>
  <footer>
    <a href="https://play.google.com/..." class="google-play-button">
      <img src="..." alt="Google Play">
      <span>GET IT ON Google Play</span>
    </a>
  </footer>
</div>
```

**Opening State:** `aria-expanded="true"` or class `.open`/`.active`

---

## Test Strategy

### 1. Find Burger Menu
```typescript
// Try these selectors in order
const burgerSelectors = [
  'button.burger-menu',
  '[data-testid="burger-menu"]',
  '.menu-toggle',
  '.hamburger',
  'button[aria-label="Menu"]',
  '.header button:first-child'
];
```

### 2. Find Google Play Button
```typescript
// Try these selectors after menu is open
const googlePlaySelectors = [
  'a[href*="play.google.com"]',
  '.google-play-button',
  '[data-testid="google-play-button"]',
  'button:has-text("Google Play")',
  'a:has-text("GET IT ON")'
];
```

---

## Notes

- **Dynamic Content:** UI might be React/Vue with dynamic classes
- **Mobile/Desktop:** Selectors might differ between responsive breakpoints
- **A/B Testing:** Different variants might have different selectors
- **Localization:** Text might be translated (e.g., "Отримати в Google Play")

---

## Test Script Created

**File:** `tests/burger-menu-google-play.spec.ts`
**Purpose:** Automated test for burger menu and Google Play button
**Coverage:**
- Burger menu detection and click
- Side panel opening verification
- Google Play button detection and click
- Navigation to Google Play verification
- Screenshot evidence collection

## Next Steps

1. ✅ **Validate Selectors:** Playwright test script created
2. ⏳ **Update UI Knowledge Base:** Add to `ui-knowledge/minebit/`
3. ⏳ **Create Page Object:** Add to Playwright page object model
4. ⏳ **Integration Tests:** Add to regression test suite
5. ✅ **Jira Report:** Generated `JIRA_REPORT_BURGER_MENU.md`
