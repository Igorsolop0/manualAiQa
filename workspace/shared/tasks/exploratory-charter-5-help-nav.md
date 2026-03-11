# Exploratory Charter 5: Help/FAQ & Navigation

**Проєкт:** Minebit (NextCode)
**Тип:** Exploratory Testing — Single Charter
**Дата:** 2026-03-11
**Агент:** Clawver (QA Agent)
**Environment:** QA
**URL:** https://minebit-casino.qa.sofon.one

---

## Test Charter

> **Explore** help pages, FAQ, footer links, and overall site navigation
> **Using** Playwright snapshots, link validation, accessibility checks
> **To discover** broken links, outdated content, missing help topics, navigation bugs

## Scope

**In Scope:**
- FAQ page and search
- Help categories navigation
- Footer links (Terms, Privacy, Responsible Gaming, About)
- Header navigation (home, lobby, profile, logout)
- Breadcrumbs (if present)
- External links behavior (open in new tab?)
- Overall navigation consistency

**Out of Scope:**
- Payments, Deposit, Withdraw
- Auth, Lobby, Games, Bonuses (other charters)

## Prerequisites

- Must be logged in

## Execution Steps

1. Navigate to Help/FAQ page → full snapshot → catalog elements
2. Test FAQ search (if available):
   - Search known topic → results?
   - Search unknown → empty state?
3. Browse FAQ categories → content loads?
4. Scroll to footer → snapshot → catalog all links
5. Click each footer link:
   - Terms of Service → loads? Content?
   - Privacy Policy → loads?
   - Responsible Gaming → loads?
   - Contact/Support → loads?
6. Check external links → open in new tab? (should not lose game session)
7. Test header navigation:
   - Home link → goes to main page?
   - Profile → goes to profile?
   - Each nav item accessible via getByRole?
8. Check for 404 errors on any page
9. Note any accessibility issues (missing alt text, poor contrast)

## Snapshot Requirements

Save to: `shared/test-results/exploratory-2026-03-11/charter-5-help/`

## Deliverables

1. Screenshots in `charter-5-help/`
2. `charter-5-help/notes.md` — session notes
3. `charter-5-help/elements.md` — navigation/help elements catalog
4. `charter-5-help/defects.md` — defects found

## When Done

Report to Nexus: "Charter 5 (Help/Nav) завершено. Результати: shared/test-results/exploratory-2026-03-11/charter-5-help/"

---

**This is the FINAL charter. After completing this, compile a summary of all 5 charters into:**
`shared/test-results/exploratory-2026-03-11/SUMMARY.md`
