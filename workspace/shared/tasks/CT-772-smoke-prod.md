# CT-772: Bonuses Page UI — Smoke Test (Production)

**Jira:** https://next-t-code.atlassian.net/browse/CT-772
**Status:** On Production
**Priority:** Normal

## Опис фічі
Оновлення UI сторінки бонусів:
1. **Regular bonuses** — Новий timer badge (circular, top-right, формат `XXH:YYM`, лейбл "Ends in")
2. **Special bonuses** — Empty state banner "Bonuses Coming Soon" (коли немає бонусів)

## Environment
- **URL:** https://minebit-casino.prod.sofon.one/bonuses (Internal Portal)
- **Auth:** REQUIRED (authorized user)
- **Credentials:** Use test account from `workspace/shared/credentials/minebit-prod.json`

## Test Scenarios

### 1. Regular Bonuses — Timer Badge (All Locales)

**Що перевіряти:**
- Timer badge у top-right corner (circular)
- Лейбл "Ends in" (або переклад)
- Формат часу: `XXH:YYM` (не `XXh:YYm:ZZs`)
- Текст не обрізається, layout не ламається

| Locale | URL Path |
|--------|----------|
| EN | `/bonuses` |
| RU | `/ru/bonuses` |
| DE | `/de/bonuses` |
| ES | `/es/bonuses` |
| FR | `/fr/bonuses` |
| PT | `/pt/bonuses` |

**Steps:**
1. Login to Minebit production
2. Navigate to bonuses page
3. Switch locale to RU → verify timer badge
4. Switch locale to DE → verify timer badge
5. Switch locale to ES → verify timer badge
6. Switch locale to FR → verify timer badge
7. Switch locale to PT → verify timer badge
8. Take screenshots for each locale

### 2. Special Bonuses — Empty State

**Якщо у користувача немає special bonuses:**
- Banner "Bonuses Coming Soon" відображається
- Текст: "No special bonuses available right now. Stay tuned exciting rewards are on the way!"
- Переклад коректний для кожної локалі

### 3. Responsive Check

**Devices:**
- Desktop Chrome (MacBook Air)
- Mobile Chrome (Pixel 7) — if available

**Resolutions:**
- 1920x1080 (desktop)
- 390x844 (mobile)

### 4. Regression Check

- Bonus CTAs працюють: "Play game", "Activate", "Deposit", "Choose game", "Claim"
- Timer countdown оновлюється (не замерзлий)

## Expected Results

✅ Timer badge у всіх локалях відображається коректно
✅ Текст не обрізається на довгих перекладах (DE, FR)
✅ Empty state banner показується якщо немає special bonuses
✅ Layout не ломиться на mobile
✅ Bonus actions працюють

## Evidence
Save screenshots to: `shared/test-results/CT-772/`
- `bonuses-timer-en.png`
- `bonuses-timer-ru.png`
- `bonuses-timer-de.png`
- `bonuses-timer-es.png`
- `bonuses-timer-fr.png`
- `bonuses-timer-pt.png`
- `bonuses-empty-state.png` (if applicable)

## Notes
- На QA тестувалось 3 дні тому — все працювало
- Timer компонент має бути reusable для Bonuses Widget
