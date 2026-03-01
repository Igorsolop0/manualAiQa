# QA Automation Workflow v2 (Jira → TestRail)
**Version:** 2.1  
**Created:** 2026-03-01  
**Updated:** 2026-03-01  
**Status:** Active  

## Trigger
Automatically run this workflow when:
- A Jira ticket appears with status "Ready for Testing"
- OR ticket changes status to "In Testing"  
- OR assignee = Ihor Solopii

**Current Implementation:** Check Jira during each heartbeat and whenever Ihor messages me.

## Workflow — execute strictly in order

### STEP 1 — Memory Check
Before any ticket analysis, perform Memory Check:
- Have I tested similar features before?
- What are known risks in this area (bonuses, payments, KYC, Smartico, Wallet Service)?
- What test cases already exist in TestRail for this module?
- What Playwright helpers/fixtures already exist in the repo?
- Check `MEMORY.md` and `memory/YYYY-MM-DD.md` for recent context

### STEP 2 — Layered Analysis
Apply QA Layered Test Design Methodology (from memory):
- Determine complexity: simple / medium / complex
- Determine testing levels: UI / API / integration / edge cases
- Determine priorities: critical path → happy path → negative → edge cases

### STEP 3 — senior-qa: Test Generation
Use senior-qa skill to generate:
- Playwright spec files (.spec.ts) with Page Object if needed
- API test files if ticket involves backend
- Name files by pattern: `[ticket-id]-[feature-name].spec.ts`
- Example: `CT-699-bonus-assignment.spec.ts`

**Note:** senior-qa focuses on React/Next.js but can be adapted for Minebit.

### STEP 3.5 — Human Review Gate (MANDATORY — DO NOT SKIP)
After generating spec files, send me this message:

```
🧪 QA Agent — Test Review Required
📋 Ticket: [TICKET-ID] — [ticket name]
📁 Generated files:
- [filename].spec.ts (X test cases)
- [filename].api.spec.ts (X test cases) — if any
🔍 Coverage:
- Critical path: X tests
- Happy path: X tests
- Negative: X tests
- Edge cases: X tests
⚠️ Questions / doubts:
- [unclear requirements, ambiguous behavior, gaps in specification]

Reply:
✅ "ok" / "ок" / "го" / "+" → run tests
✏️ "changes: [comment]" → rework and send again
```

WAIT for response. Do NOT proceed to STEP 4 without my confirmation.

**Response logic:**
- "ok" / "ок" / "го" / "+" → proceed to STEP 4
- "changes: [comment]" → return to STEP 3, incorporate comment, regenerate and resend for review
- No response > 2 hours → send reminder and continue waiting

### STEP 4 — Запуск тестів з обов'язковим збором evidence
Запускай тести завжди з такою командою:
```bash
npx playwright test [ticket-id]-[feature].spec.ts \
  --reporter=html \
  --output=./test-results/[ticket-id]/
```

**Конфіг playwright.config.ts має містити:**
```typescript
use: {
  trace: 'on',          // завжди, не тільки при failure
  video: 'on',          // завжди
  screenshot: 'on',     // завжди
  outputDir: './test-results'
}
```

**Якщо конфіг ще не має цих налаштувань — додай їх зараз.**

Після запуску зафіксуй:
- Загальний результат: X passed / X failed / X skipped
- Час виконання
- Шлях до HTML report: `./test-results/[ticket-id]/index.html`

### STEP 5 — Evidence collection (обов'язково для КОЖНОГО тесту)
Для КОЖНОГО тесту (не тільки failed) зібрати:

**PASSED тест:**
✅ Screenshot фінального стану → `[ticket-id]-[test-name]-PASSED.png`  
✅ Відео виконання → `[ticket-id]-[test-name].webm`

**FAILED тест:**
❌ Screenshot моменту падіння → `[ticket-id]-[test-name]-FAILED.png`  
❌ Відео виконання → `[ticket-id]-[test-name].webm`  
❌ Trace файл → `[ticket-id]-[test-name]-trace.zip`  
❌ Console errors із логу

**Структура артефактів:**
```
./test-results/
  [ticket-id]/
    screenshots/
    videos/
    traces/
    report/           ← HTML Playwright report
```

### STEP 6 — Підготовка evidence для мого ревю (НЕ завантажувати самостійно)
Агент НЕ додає коментар до Jira самостійно і НЕ завантажує attachments. Замість цього:

1. **Зібрати всі артефакти** у `./test-results/[ticket-id]/`
   - screenshots/
   - videos/
   - traces/
   - report/ (HTML)

2. **Сформувати драфт Jira коментаря** і показати мені в чаті:
   ```
   📋 DRAFT Jira Comment для [TICKET-ID]
   
   🤖 QA Agent Report — [TICKET-ID]
   ✅ Passed: X | ❌ Failed: X | ⏭️ Skipped: X
   ⏱️ Duration: Xs
   
   Evidence:
   📸 Screenshots: [список файлів які треба прикріпити]
   🎥 Video: [список файлів які треба прикріпити]
   📊 Full HTML Report: ./test-results/[ticket-id]/report/index.html
   
   Failed tests:
   - [test name] → Причина: [error message] → Screenshot: [filename]
   
   Висновок: Ready to merge / Needs fixes / Blocked
   ```

3. **Після показу драфту написати мені:**
   "📎 Evidence готові у `./test-results/[ticket-id]/`  
   Скопіюй коментар вище і прикріпи файли до тікету вручну.  
   Коли додаси — напиши 'done' щоб я оновив статус у TestRail."

4. **Чекати на моє "done"** перед переходом до STEP 6.5.

### STEP 6.5 — Final Summary Ping
Send me final message:

```
✅ QA Workflow complete — [TICKET-ID]
Result: Passed X / Failed X / Skipped X
TestRail Run: [link]
Evidence prepared: ✅ (awaiting your manual upload to Jira)

[If any Failed:]
❌ X tests failed — artifacts: ./test-results/[ticket-id]/
Need your attention before changing ticket status.

[If all Passed:]
🟢 All green — change ticket status to "Done / Passed QA"?
Reply "yes" for me to update status.
```

Wait for my response before changing ticket status in Jira.

## Implementation Notes

### Skills Status
- ✅ senior-qa: installed
- ⚠️ playwright-cli: not found; using playwright-mcp + exec commands
- ⚠️ vibetesting: not found; using Playwright's built-in trace/video

### Jira Integration
Currently relies on Gmail notifications. Need to implement direct Jira API check for:
- Status = "Ready for Testing"
- Assignee = Ihor Solopii

### TestRail Integration
API key needed. Pending configuration.

### Playwright Project Structure
Tests location: `/Users/ihorsolopii/Documents/minebit-e2e-playwright/tests/`
- API tests: `tests/api/tickets/`
- E2E tests: `tests/e2e/smoke/`

### Evidence Collection Configuration
**Playwright config updates required:**
- `trace: 'on'` (always, not just on failure)
- `video: 'on'` (always)
- `screenshot: 'on'` (always)
- `outputDir: 'test-results'` (already set)

**Current config status:** Needs update (trace/video/screenshot currently set to 'retain-on-failure'/'only-on-failure')

**Artifact structure:**
```
test-results/[ticket-id]/
├── screenshots/      # PNG files for every test (PASSED/FAILED)
├── videos/          # WEBM files for every test
├── traces/          # ZIP trace files for failed tests
└── report/          # HTML Playwright report
```

### Human-in-the-loop Gates
1. Test review (STEP 3.5) – approve generated tests
2. Evidence review (STEP 6) – manual Jira attachment by Ihor
3. Status update confirmation (STEP 6.5) – final approval

## Monitoring
- Check for new tickets during each heartbeat
- If workflow stuck > 10 min on any step: alert Ihor
- If at Review Gate > 2h: send reminder