# Exploratory Charter 2: Casino Lobby Navigation

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing — Single Charter
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)
**Environment:** QA
**URL:** https://minebit-casino.qa.sofon.one

---

## Test Charter

> **Explore** casino lobby filters, game search, categories, and navigation
> **Using** Playwright getByRole, snapshots, navigation heuristics
> **To discover** filtering bugs, navigation issues, performance problems, UX gaps

## Scope

**In Scope:**
- Game filters (provider, category, type, popularity)
- Search functionality (partial matches, no results, special chars)
- Category tabs (Slots, Live Casino, Table Games, etc.)
- Sorting options (A-Z, Popular, New)
- Pagination / infinite scroll
- Game cards display (thumbnails, titles, provider badges)

**Out of Scope:**
- Payments, Deposit, Withdraw
- Actually playing games (covered in Charter 3)
- Auth flow (covered in Charter 1)

## Prerequisites

- Must be logged in (use credentials from Charter 1 or `workspace/shared/credentials/`)

## Execution Steps

1. Navigate to casino lobby → full page snapshot → catalog all UI elements
2. Test category tabs — click each, verify game list changes
3. Test filters:
   - Apply single filter → games filtered correctly?
   - Apply multiple filters → combination works?
   - Clear filters → all games shown?
   - Filter state after page refresh?
4. Test search:
   - Search known game name → found?
   - Partial name → suggestions?
   - No results → empty state UX?
   - Special characters → no crash?
5. Test sorting (if available)
6. Scroll/pagination — more games load?
7. Game card elements — snapshot one card, catalog elements

## Snapshot Requirements

Save to: `shared/test-results/exploratory-2026-03-11/charter-2-lobby/`

## Playwright Rules

Use ONLY `getByRole()` as primary:
```typescript
await page.getByRole('tab', { name: 'Slots' }).click();
await page.getByRole('searchbox', { name: 'Search' }).fill('blackjack');
```

## Deliverables

1. Screenshots in `charter-2-lobby/`
2. `charter-2-lobby/notes.md` — session notes
3. `charter-2-lobby/elements.md` — functional elements catalog
4. `charter-2-lobby/defects.md` — defects found

## When Done

Report to Nexus: "Charter 2 (Lobby) завершено. Результати: shared/test-results/exploratory-2026-03-11/charter-2-lobby/"
