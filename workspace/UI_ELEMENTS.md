# UI Elements - Minebit Burger Menu & Google Play Button

## Based on Screenshot Analysis (2026-03-06)

### 1. Burger Menu Icon
**Purpose:** Opens the side panel/navigation menu
**Expected Location:** Top-left corner of the page
**Typical Selectors:**
- CSS: `button[aria-label="Menu"]`, `.burger-menu`, `.hamburger-menu`, `[data-testid="menu-button"]`
- XPath: `//button[@aria-label="Menu"]`, `//button[contains(@class, 'burger')]`, `//button[contains(@class, 'hamburger')]`
- Data attributes: `[data-cy="menu-toggle"]`, `[data-test="nav-toggle"]`

**Visual Description:** Three horizontal lines (hamburger icon)

### 2. Google Play Button (Inside Menu)
**Purpose:** Redirects to Google Play Store for app download
**Expected Location:** Inside the opened side panel, likely in a "Download App" section
**Typical Selectors:**
- CSS: `a[href*="play.google.com"]`, `.google-play-button`, `[alt="Get it on Google Play"]`
- XPath: `//a[contains(@href, 'play.google.com')]`, `//img[@alt="Get it on Google Play"]/parent::a`
- Button text: Could be `Get it on Google Play` or similar

**Visual Description:** Google Play badge with robot logo and text "Get it on Google Play"

### 3. Side Panel/Navigation Menu
**Purpose:** Contains navigation links and app download options
**Expected Selectors:**
- CSS: `.side-panel`, `.nav-menu`, `[role="navigation"]`, `.drawer`
- XPath: `//div[contains(@class, 'side-panel')]`, `//nav[contains(@class, 'menu')]`

### 4. Expected Test Flow:
1. Navigate to `https://minebit-casino.prod.sofon.one`
2. Wait for page load
3. Click burger menu icon
4. Wait for side panel to open (visibility check)
5. Find Google Play button inside panel
6. Click Google Play button
7. Verify redirect to `play.google.com`
8. Verify Google Play page has content (title, description, install button)

### 5. Fallback Strategies:
- If standard selectors don't work, use:
  - `document.querySelectorAll('button')` and filter by position/size
  - Screenshot comparison for visual testing
  - Network monitoring for Google Play redirect

### 6. Environment Notes:
- **Prod URL:** `https://minebit-casino.prod.sofon.one`
- **Mobile responsive:** Check both desktop and mobile views
- **Authentication:** May need to handle login state

---

## Next Steps:
1. Execute Playwright test to validate selectors
2. Update this file with actual working selectors
3. Create comprehensive test report for Jira
4. Add screenshots as evidence