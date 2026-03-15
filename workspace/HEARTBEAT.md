# HEARTBEAT.md - Nexus Recurring Checks

This file is allowed to contain recurring operational checks because Nexus is the orchestrator.

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## ✅ Vacation Mode завершено (2026-02-25 to 2026-03-02)
**Нормальний режим роботи відновлено** — Jira ticket notifications активовано.

Gmail checks + Jira processing працюють повноцінно.

---

## Gmail Check (NextCode)
Check for new emails and notify if important:

```bash
python3 /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/gmail_checker.py
```

**NORMAL MODE: Jira processing активовано**

If output contains `NEW_EMAILS_COUNT:`, parse emails and process:

**For Jira tickets:**
1. Extract ticket ID (e.g., CT-727)
2. Fetch ticket details using Jira API:
   ```bash
   python3 /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/jira_fetch.py CT-727
   ```
3. Summarize: status, priority, last comment, action needed
4. Send notification to Telegram (action=send, to=282986529, channel=telegram)

**For non-Jira emails:**
1. Show sender, subject, preview
2. Assess urgency
3. Send notification

## Frequency
Check every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri).

---

## ConfAdapt Technology Monitor (Weekly)
Monitor developments in multi-token prediction / ConfAdapt research.

**Schedule:** Every Monday at 10:00 AM (or during Monday heartbeat)

**Check if:** Today is Monday AND last check was >6 days ago

**Script:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/confadapt_monitor.py
```

**State file:** `memory/confadapt_state.json`
**Log file:** `memory/confadapt_log.md`

**When changes detected:**
1. Read the report from script output
2. Send summary to Telegram (to=282986529, channel=telegram)
3. Update state file automatically

**Manual check anytime:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/confadapt_monitor.py
```

---

## QA Workflow Check (Jira → TestRail)
**Trigger:** Check Jira for tickets: status = "Ready for Testing" AND assignee = Ihor Solopii (Panda Sensei)

**Script:** Use Jira API via jira_poller.py
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/jira_poller.py
```

**NORMAL MODE:** Workflow triggering активовано.

**If new ticket found:** Trigger QA Automation Workflow v2

**Workflow Gates Monitoring:**
- If workflow is at Review Gate (STEP 3.5): remind Ihor if no response > 2h
- If workflow stuck > 10 min on any step: alert Ihor

**Frequency:** Check every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri)

**Workflow Location:** `/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/workflows/QA_AUTOMATION_WORKFLOW_V2.md`

---

## ✅ Завершено: Test Data Scripts (2026-03-04)

**Виконано:**

1. **Скрипти 04‑05** ✅ (існують):
   - `04_get_player_info.py` — отримання інформації про гравця
   - `05_create_bonus.py` — створення тестових бонусів

2. **Оркестратор сценаріїв** ✅ (`07_test_data_orchestrator.py`):
   - `player_with_balance` — гравець з балансом
   - `deposit_streak` — гравець з 3 депозитами (20, 30, 50 USD)
   - `high_roller` — гравець з великим балансом ($1000+)
   - `player_with_bonus` — гравець з бонусом
   - `full_setup` — повний налаштування (баланс + депозити + бонус)

3. **Інтеграція в реальні тести Minebit** ✅:
   - Фікстура `test-data.fixture.ts` створена
   - 6 тестів використовують автоматичну підготовку даних:
     * `bonus/eligible-bonuses.spec.ts`
     * `fixture-test.spec.ts`
     * `player/balance.spec.ts`
     * `deposit-streak.spec.ts`

4. **Автоматичний пошук payment method** ✅ (`06_payment_methods.py`):
   - Скрипт для переліку доступних payment methods для кожної валюти

**Використання:**
```bash
# Оркестратор — створення сценаріїв
cd /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/test-data-scripts
python3 scripts/07_test_data_orchestrator.py --scenario deposit_streak --env qa

# Список сценаріїв
python3 scripts/07_test_data_orchestrator.py --list
```

**У Playwright тестах:**
```typescript
import { test } from '../../src/fixtures/test-data.fixture';

test('my test', async ({ createTestPlayer, depositToPlayer }) => {
  const player = await createTestPlayer({ env: 'qa', balance: 100 });
  await depositToPlayer(player.clientId, 30);
});
```
