# Minebit Platform - Exploratory Testing Report

## Executive Summary

**Date:** 2026-02-18
**Environment:** Production (https://minebit-casino.prod.sofon.one)
**Scope:** UI/UX exploration, platform capabilities

---

## Platform Overview

**Minebit** is a crypto-friendly online casino platform offering:
- 4789+ Slots games
- Live Casino
- Sports-related games
- VIP/Loyalty program
- Multiple promotions

---

## Pages Explored

### Guest User Pages (Accessible without login)

| Page | URL | Status | Key Features |
|------|-----|--------|--------------|
| Homepage | `/` | ✅ | Hero, Categories, Recent Wins, Game Cards |
| Games Lobby | `/games` | ✅ | All games, filters |
| Slots | `/games/slots` | ✅ | 4789+ games, Play + Demo |
| Live Casino | `/games/live-casino` | ✅ | Live dealer games |
| Instant Games | `/games/instant` | ✅ | 56 games visible |
| New Games | `/games/new-games` | ✅ | Latest releases |
| Jackpots | `/games/jackpots` | ✅ | Jackpot games |
| Drops & Wins | `/games/drops-wins` | ✅ | Tournament games |
| Providers | `/games/providers` | ✅ | Provider list |
| VIP Club | `/vip-club-unauthenticated` | ✅ | VIP benefits info |
| Loyalty | `/loyalty-guest` | ✅ | Loyalty program info |
| Quests | `/quests` | ✅ | Quest types info |
| Promo List | `/promo-list` | ✅ | All promotions |
| Help Center | `/help-center-account` | ✅ | FAQ |

---

### Authenticated User Pages (Tested)

| Page | URL | Status | Key Features |
|------|-----|--------|--------------|
| User Menu | Header dropdown | ✅ | Profile, Transactions, Bets History, Bonus History, Verification, Security, Our Community |
| Wallet Modal | `/?modal=wallet` | ✅ | Balance, Deposit, Withdrawal |
| Favorites | `/games/favorites` | ✅ | Saved games |
| Profile | `/profile` | ✅ | Account settings |
| Security | `/profile/security` | ✅ | Password change, 2FA |
| Transactions | `/profile/transactions` | ✅ | Transaction history |
| Bets History | `/profile/bets-history` | ⏳ Pending | Bet history |
| Bonus History | `/profile/bonus-history` | ⏳ Pending | Bonus claims |
| Verification | `/profile/verification` | ⏳ Pending | KYC |

---

## Game Categories

| Category | Games Count | Demo Mode | Real Money |
|----------|-------------|-----------|------------|
| Slots | 4789+ | ✅ | ✅ |
| Hot Games | 186+ | ✅ | ✅ |
| Live Casino | Multiple | ✅ | ✅ |
| Instant | 56+ | ✅ | ✅ |
| Blackjack | Multiple | ✅ | ✅ |
| Roulette | Multiple | ✅ | ✅ |
| Game Shows | Multiple | ✅ | ✅ |
| Jackpots | Multiple | ✅ | ✅ |
| Drops & Wins | Multiple | ✅ | ✅ |
| New Games | Multiple | ✅ | ✅ |

---

## Game Providers (48+)

- PragmaticPlay
- Hacksaw Gaming
- Evolution Gaming
- BGaming
- Nolimit City
- PGSoft
- ... and more

---

## Promotions Available

1. **Wheels of Fortune** - Spin to win
2. **Drops & Wins - Winter Edition** - Tournament
3. **Cashback** - Regular cashback
4. **Personal quests** - Complete tasks
5. **Spinoleague** - Competition
6. **Daily bonus** - Daily rewards
7. **Reload bonus** - Deposit bonus
8. **Valentine's Day Tournament** - Seasonal

---

## VIP Program

### VIP Benefits:
- Special Bonuses
- VIP Welcome Bonuses
- Birthday Rewards
- Personal VIP Bonuses
- Secret Rewards
- Higher Reload Bonuses

### VIP Privileges:
- Huge Payouts
- Withdrawal Priority
- Profile Customization
- VIP Quests & Challenges
- Exclusive Games & Releases
- VIP Support
- Personal Manager
- VIP Transfer Program
- SUPER PRIZE

---

## Loyalty Program

### How it works:
1. **Create Your Account**
2. **Play and Earn EXP**
3. **Unlock Bigger Rewards**

### Rewards:
- Bigger Reload Bonuses
- Weekly Cashback Up to 20%
- Level-Up Bonuses
- Personal Quests
- Wheel of Fortune
- Exclusive VIP Access

---

## Quests System

### Quest Types:
- **VIP Quests** - For VIP members
- **Promo Quests** - Event-based
- **Daily Quests** - Complete daily
- **Weekly Quests** - Weekly challenges

---

## Authentication

### Login Modal:
- Social Login: **Google**, **Telegram**
- Email/Password login
- "Forgot password?" link
- "Register" link

### Sign Up Modal:
- 6 Input fields
- 10 Form elements
- Social registration available

---

## Game Launch Flow

### Demo Mode:
```
1. Browse games
2. Click "Demo" button
3. Game loads in iframe
4. URL: /game/{game-name}-{id}?isForDemo=true
```

### Real Money:
```
1. Login required
2. Click "Play" button
3. Game loads in iframe
4. Balance deducted on bet
```

---

## UI Components Identified

### Header:
- Logo
- Navigation links (22)
- Game categories (4)
- CTA buttons (22)

### Footer:
- Payment methods icons
- Social links
- Download app
- Legal information
- Support contact

### Game Card:
- Game thumbnail
- Provider name
- Game name
- "Play" button
- "Demo" button (if available)
- Favorite button

### Recent Top Wins Widget:
- Visible on homepage
- Shows recent wins
- Provider, game, player, amount

---

## Technical Observations

### URL Patterns:
```
/games/{category}
/game/{game-name}-{id}?isForDemo=true
/vip-club-{auth-status}
/loyalty-{auth-status}
```

### Role-based Selectors (for automation):
```
button:has-text("Play")
button:has-text("Demo")
button:has-text("Log In")
button:has-text("Sign Up")
textbox "Email"
textbox "Password"
```

### Data Attributes:
```
data-testid="ActionButton-openLink"
data-testid="PlayerAccountMenuButton-menu-toggle"
```

---

## Screenshots Captured

### Guest User:
```
test-results/exploratory/quick/
├── 01-homepage.png
├── 02-games.png
├── 03-slots.png
├── 04-live-casino.png
├── 05-recent-wins-widget.png
├── 09-signup-modal.png
├── 10-vip.png
├── 11-promo-list.png
├── 12-quests-guest.png
├── 13-loyalty-guest.png
├── 14-help-center.png
├── 15-game-demo.png
├── 16-providers.png
├── 17-jackpots.png
├── 18-drops-wins.png
├── 19-new-games.png
└── 20-instant.png
```

### Authenticated User:
```
test-results/exploratory/auth/
├── 01-logged-in.png
├── 02-wallet-modal.png
├── 03-favorites.png
├── 04-profile.png
├── 05-security.png
└── 06-transactions.png
```

---

## Next Steps

### Pending Exploration:
1. **Wallet Modal** (authenticated)
2. **Deposit flow** (UI only)
3. **Withdrawal flow** (UI only)
4. **Active bonuses page**
5. **Favorites page**
6. **Profile/Settings**

### Automation Recommendations:

1. Create Page Objects for each page
2. Use role-based selectors
3. Handle iframe for game launch
4. Test authenticated vs unauthenticated states
5. **Use Smartico overlay handler** for all authenticated tests

---

## Smartico Overlay Handling

**Problem:** After login, Smartico promotional iframes block all UI interactions.

**Solution:** Use the `smartico-handler.ts` utility:

```typescript
import { dismissSmarticoOverlays, safeClick, waitForInteractive } from '../utils/smartico-handler';

// Before interacting with elements
await dismissSmarticoOverlays(page);
await element.click();

// Or use safe click (auto-handles overlays)
await safeClick(page, '[data-testid="wallet-button"]');
```

**Smartico iframe types to handle:**
- `__smarticoPrizeDrop###` - Prize drop notifications
- `__btgPromoHolder` - Bonus/promo notifications
- `__btgPromo###` - Promotional content

**Note:** These overlays are NOT part of regression/feature testing and should always be dismissed.

---

## Conclusion

Minebit is a fully-featured crypto casino with:
- Extensive game library (4789+ slots, live casino, etc.)
- Multiple promotions and tournaments
- VIP and Loyalty programs
- Quests system
- Demo mode for all games

Platform is well-structured for automation with clear UI patterns and role-based elements.
