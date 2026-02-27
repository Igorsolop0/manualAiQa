# QA Testing Notes

## Utilities & Helpers

### Smartico Promotional Overlay Handler

**File:** `src/utils/smartico-handler.ts`

**Purpose:** Handle Smartico promotional iframes that appear after login and block UI interactions.

**Usage:**
```typescript
import { 
  dismissSmarticoOverlays, 
  safeClick, 
  waitForInteractive,
  preparePageForTesting 
} from '../utils/smartico-handler';

// Before interacting with elements
await dismissSmarticoOverlays(page);
await element.click();

// Or use safe click (handles overlays automatically)
await safeClick(page, '[data-testid="wallet-button"]');

// Wait for page to be interactive
await waitForInteractive(page);

// Prepare page before testing
await preparePageForTesting(page);
```

**Smartico Iframe Types:**
- `__smarticoPrizeDrop###` - Prize drop notifications
- `__btgPromoHolder` - Bonus/promo notifications
- `__btgPromo###` - Promotional content

**Note:** These overlays are NOT part of regression/feature testing and should always be dismissed.

---

## Selectors Reference

### Login Modal (Fixed)
```typescript
// CORRECT selectors (role-based):
await page.getByRole('textbox', { name: /email/i }).fill(email);
await page.getByRole('textbox', { name: /password/i }).fill(password);
await page.getByRole('button', { name: /start playing/i }).click();

// WRONG selectors (don't use):
// input[type="email"]  ❌
// input[name="email"]  ❌
// button:has-text("Log In") for submit  ❌ (it's "Start Playing")
```

### User Menu
```typescript
const userMenu = page.getByTestId('PlayerAccountMenuButton-menu-toggle');
await safeClick(page, '[data-testid="PlayerAccountMenuButton-menu-toggle"]');
```

### Wallet Button
```typescript
const walletBtn = page.getByTestId('ActionButton-openLink').filter({ hasText: /wallet/i });
// Or navigate directly: /?modal=wallet
```

---

## Page URLs Reference

### Guest Pages
| Page | URL |
|------|-----|
| Homepage | `/` |
| Games | `/games` |
| Slots | `/games/slots` |
| Live Casino | `/games/live-casino` |
| VIP (info) | `/vip-club-unauthenticated` |
| Loyalty (info) | `/loyalty-guest` |
| Quests (info) | `/quests` |
| Promos | `/promo-list` |
| Help | `/help-center-account` |

### Authenticated Pages
| Page | URL |
|------|-----|
| Wallet | `/?modal=wallet` |
| Favorites | `/games/favorites` |
| Profile | `/profile` |
| Security | `/profile/security` |
| Transactions | `/profile/transactions` |
| Bets History | `/profile/bets-history` |
| Bonus History | `/profile/bonus-history` |
| Verification | `/profile/verification` |

---

## Test Execution Commands

### Run Exploratory Tests
```bash
cd /Users/ihorsolopii/Documents/minebit-e2e-playwright

# Guest pages exploration
ENV=prod npx playwright test quick-exploration --project=e2e-chromium

# Authenticated exploration
ENV=prod npx playwright test authenticated --project=e2e-chromium

# Wallet exploration
ENV=prod npx playwright test exploratory-wallet --project=e2e-chromium
```

---

## Known Issues & Solutions

### Smartico Overlays Blocking Clicks
**Issue:** After login, Smartico promotional iframes block all UI interactions.
**Solution:** Use `dismissSmarticoOverlays(page)` before any click operation.

### Login Modal Selectors
**Issue:** `input[type="email"]` selector doesn't work.
**Solution:** Use role-based selectors: `getByRole('textbox', { name: /email/i })`.

### New User Has Empty Favorites
**Expected:** Favorites page shows 0 games for new users.
**Not a bug:** Users need to add games to favorites first.
