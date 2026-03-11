# Exploratory Charter 4: Bonuses & Promotions UI

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing — Single Charter
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)
**Environment:** QA
**URL:** https://minebit-casino.qa.sofon.one

---

## Test Charter

> **Explore** bonuses list, promo pages, and bonus activation UI
> **Using** Playwright snapshots, navigation, UI validation
> **To discover** display issues, broken links, missing info, UX confusion

## Scope

**In Scope:**
- Bonus list display (thumbnails, titles, terms)
- Promo banners in lobby
- Bonus terms & conditions readability
- Bonus activation button (UI only, do NOT actually activate)
- Expired bonuses display
- Bonus categories / filters
- Smartico modals (if they appear — handle them!)

**Out of Scope:**
- Payments, Deposit, Withdraw
- Actually claiming/activating bonuses with real money
- Auth, Lobby, Games (other charters)

## Prerequisites

- Must be logged in

## Execution Steps

1. Navigate to Bonuses/Promotions page → full snapshot → catalog elements
2. List all visible bonuses — types, thumbnails, CTAs
3. Check bonus card elements:
   - Title visible?
   - Image loading?
   - "Terms & Conditions" link working?
   - CTA button text meaningful?
4. Click on a bonus → detail page opens? → snapshot
5. Check T&C page — content loaded? Readable?
6. Look for promo banners on home/lobby page → snapshot
7. Check if expired bonuses are visible (they shouldn't be)
8. Handle Smartico modals if they pop up (close, then continue)

## Snapshot Requirements

Save to: `shared/test-results/exploratory-2026-03-11/charter-4-bonuses/`

## Deliverables

1. Screenshots in `charter-4-bonuses/`
2. `charter-4-bonuses/notes.md` — session notes
3. `charter-4-bonuses/elements.md` — bonus UI elements catalog
4. `charter-4-bonuses/defects.md` — defects found

## When Done

Report to Nexus: "Charter 4 (Bonuses) завершено. Результати: shared/test-results/exploratory-2026-03-11/charter-4-bonuses/"
