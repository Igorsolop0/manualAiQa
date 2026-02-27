# Exploratory Testing Plan - Minebit Casino

## Role: Senior QA Automation Engineer (iGaming/Casino)

## Scope

| Area | Status | Notes |
|------|--------|-------|
| `/bonuses` | ❌ SKIP | Redesign in progress (1-2 days) |
| Wallet Modal | ✅ FOCUS | UI/UX only — NO payment transactions |
| Other pages | ✅ FOCUS | Platform exploration |

---

## Task Breakdown

### 1. Wallet Modal (UI/UX Audit)

**Focus:** DOM structure, elements, text, buttons

**Test Scenarios:**
| # | Scenario | Data to Capture |
|---|----------|-----------------|
| 1.1 | Open Wallet modal (unauthenticated) | Elements visible, CTA buttons |
| 1.2 | Open Wallet modal (authenticated) | Balance display, action buttons |
| 1.3 | Document DOM structure | All elements, locators, attributes |
| 1.4 | Document button states | Enabled/Disabled, labels |
| 1.5 | Document text content | Labels, descriptions, amounts |

**Deliverables:**
- Screenshot (unauthenticated)
- Screenshot (authenticated)
- DOM structure
- Element map with locators

---

### 2. Platform Exploration (Other Pages)

**Pages to explore:**

| Page | Auth Status | Focus |
|------|-------------|-------|
| Homepage (`/`) | Unauthenticated | Hero, navigation, game cards |
| Homepage (`/`) | Authenticated | User menu, balance, favorites |
| Games Lobby (`/games`) | Both | Categories, filters, game cards |
| Game Categories | Both | Slots, Live Casino, Table Games |
| Game Launch | Both | Demo vs Real Money, iframe |
| Sidebar | Both | Navigation structure |
| Footer | Both | Links, legal, social |
| Profile/Settings | Authenticated only | Menu structure |
| Quests | Authenticated only | Tabs, cards |

---

## Technical Tasks

For each explored page/element:

### Screenshot
```typescript
await page.screenshot({ path: 'screenshots/page-name.png', fullPage: true });
```

### DOM Structure
```typescript
const html = await page.content();
// Extract key elements
```

### Element Properties
```typescript
// Locator
const button = page.getByRole('button', { name: 'Play' });

// Attributes
const attributes = await button.evaluate(el => ({
  class: el.className,
  disabled: el.disabled,
  testId: el.getAttribute('data-testid'),
  // ... more attributes
}));
```

### State Analysis
- Button states (enabled/disabled/hovered)
- Form states (empty/filled/error)
- Loading states

---

## Expected Output

### 1. Page Structure Report
For each page:
- URL variations (auth vs unauth)
- Main sections
- Key components

### 2. Element Map (DOM)
For key elements:
- Locators (role, testId, text, class)
- Attributes
- States

### 3. Technical Description
- Component names
- Interaction patterns
- State transitions

---

## Tools

- Playwright CLI: `npx playwright codegen`
- Playwright MCP: Browser automation
- Screenshot capture
- DOM extraction

---

## Run Commands

### Homepage (Unauthenticated)
```bash
cd /Users/ihorsolopii/Documents/minebit-e2e-playwright
ENV=prod npx playwright codegen https://minebit-casino.prod.sofon.one
```

### Homepage (Authenticated)
```bash
# Create test user first via GraphQL, then login
```

---

## Notes

- PaymentHub team handles payment logic — DO NOT test transactions
- Focus on UI/UX identification only
- Document findings for automation planning
