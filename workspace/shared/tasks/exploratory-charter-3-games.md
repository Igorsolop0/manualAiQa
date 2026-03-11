# Exploratory Charter 3: Game Launch & Interaction

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing — Single Charter
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)
**Environment:** QA
**URL:** https://minebit-casino.qa.sofon.one

---

## Test Charter

> **Explore** game opening, in-game controls, and return to lobby
> **Using** Playwright snapshots, interaction testing, timing checks
> **To discover** game loading issues, control responsiveness, navigation bugs

## Scope

**In Scope:**
- Game loading (progress indicator, timeout handling)
- In-game controls (spin, stop, auto-play, bet amount, lines)
- Settings panel (sound, speed, quality)
- Return to lobby button
- Game frame resizing

**Out of Scope:**
- Payments, Deposit, Withdraw
- Real money bets (use demo/fun mode only)
- Auth (Charter 1), Lobby nav (Charter 2)

## Prerequisites

- Must be logged in
- Casino lobby accessible

## Execution Steps

1. From lobby, click on a popular slot game → snapshot loading state
2. Wait for game to load → snapshot game screen → catalog all game controls
3. Identify game controls:
   - Spin/Play button
   - Stop button
   - Auto-play toggle
   - Bet amount +/-
   - Lines selector (if available)
   - Settings/Menu button
4. Test basic interactions:
   - Click Spin (demo mode) → animation runs?
   - Change bet amount → UI reflects change?
   - Open settings → sound/speed options?
5. Test return to lobby:
   - Click back/close → lobby loads?
   - Filter state preserved? (note from Charter 2)
6. Try opening a different game type (table game, live casino preview if available)
7. Check game frame on resize (if applicable)

## Snapshot Requirements

Save to: `shared/test-results/exploratory-2026-03-11/charter-3-games/`

## Playwright Rules

Use `getByRole()` as primary. Note: game iframes may need `frame.getByRole()`.

## Deliverables

1. Screenshots in `charter-3-games/`
2. `charter-3-games/notes.md` — session notes
3. `charter-3-games/elements.md` — game control elements catalog
4. `charter-3-games/defects.md` — defects found

## When Done

Report to Nexus: "Charter 3 (Games) завершено. Результати: shared/test-results/exploratory-2026-03-11/charter-3-games/"
