# MEMORY.md - Jira Watcher

> This logic relates to Slack threading, Gmail checking, Standup analysis, and Jira API queries.


---

## Gmail Integration (ihor.so@nextcode.tech)

**Status:** ✅ Active

**Setup Date:** 2026-02-14

**How it works:**
- IMAP connection to Gmail via App Password
- Automatic checks every 30 minutes during work hours (9:00-18:00 CET, Mon-Fri)
- Jira tickets detected and summarized automatically
- Notifications sent to Telegram

**✅ Vacation Mode завершено:**
- NextCode vacation: 2026-02-25 to 2026-03-02 (completed)
- Jira ticket notifications відновлено з 2026-03-02
- Нормальний режим роботи активовано

**Credentials Location:**
- App Password: `/Users/ihorsolopii/.openclaw/workspace/.gmail_config`
- Seen IDs: `/Users/ihorsolopii/.openclaw/workspace/.gmail_seen_ids.json`

**Cron Job:** `40d004fa-6219-438a-bf2e-a0dad924a18f` (Gmail Check - NextCode)

**Scripts:**
- Checker: `/Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py`
- Notifier: `/Users/ihorsolopii/.openclaw/workspace/scripts/gmail_notify.py`

**Manual Check:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py
```

**Reinitialize (mark all as seen):**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/gmail_checker.py --init
```

---


---

## Jira API Integration

**Status:** ✅ Active

**Setup Date:** 2026-02-14

**How it works:**
- `go-jira` CLI installed
- API Token configured for authentication
- Full access to ticket details, comments, status

**Credentials:**
- API Token: `/Users/ihorsolopii/.openclaw/workspace/.jira_token`
- Config: `~/.jira.yml`
- Domain: `https://next-t-code.atlassian.net`
- User: `ihor.so@nextcode.tech`

**Fetch Ticket:**
```bash
python3 /Users/ihorsolopii/.openclaw/workspace/scripts/jira_fetch.py CT-722
```

**Direct CLI:**
```bash
export JIRA_API_TOKEN=$(cat ~/.openclaw/workspace/.jira_token)
jira view CT-722 -e https://next-t-code.atlassian.net -u ihor.so@nextcode.tech
```

---


---

## NextCode Jira Tickets Status (as of 2026-02-14)

**Open/Needs Attention:**
- CT-722 - Deposit streak bonus bug (DiaOl waiting for status update ⚠️)

**Recently Completed:**
- CT-727 - Recent wins widget ✅ Done
- CT-736 - Regular Bonuses prod config ✅ Done
- CT-560 - Special bonuses redesign ✅ Done

---


---

## 🧵 Slack Threading System for Jira Tickets

**Status:** ✅ Active

**Setup Date:** 2026-02-26

**How it works:**
- When a new Jira ticket arrives in `#qa-testing` channel, system automatically saves its `thread_ts` (Timestamp) to `/Users/ihorsolopii/.openclaw/workspace/jira_threads.json`
- This enables threaded conversations where all ticket-related updates stay in one place

**🔴 IRON RULE — Mandatory Threading:**

When Ihor asks you to analyze or test a specific ticket (e.g., CT-757), you MUST:

1. **Read the threads file:**
   ```bash
   cat /Users/ihorsolopii/.openclaw/workspace/jira_threads.json
   ```

2. **Find the `ts` for the requested ticket** (e.g., `"CT-757": "1772119587.021079"`)

3. **Send ALL communications in the thread:**
   - Test reports
   - Analysis results
   - Screenshots
   - Suggestions

4. **Use the Slack wrapper script:**
   ```bash
   python3 /Users/ihorsolopii/.openclaw/workspace/scripts/slack_message_helper.py \
     --channel C0AH10XDKM2 \
     --text "Your message here" \
     --thread_ts "TICKET_TS_FROM_JSON"
   ```

**Why this matters:**
- Keeps the `#qa-testing` channel clean
- All ticket history in one continuous thread
- Easy to track conversation per ticket
- Follows the USER.md Rule #8

**Example workflow:**
```
Ihor: "Analyze CT-757"
→ You: Read jira_threads.json → find CT-757 ts → "1772119587.021079"
→ You: Send analysis via slack_message_helper.py with --thread_ts "1772119587.021079"
→ Result: All CT-757 discussion in one thread
```

---


---

## Daily Standup Monitoring

**Правило:** Щодня перевіряти транскрипти дейлі-мітингів за сьогодні та попередні два дні. Вилучати ключову інформацію щодо готовності тікетів до тестування або нюансів у тестуванні. Зберігати цю інформацію для майбутнього дизайну тест-кейсів або тестування тікетів.

**Процес:**
1. **Отримання транскрипту:** Користувач надає транскрипт дейлі (текст).
2. **Аналіз:** Визначити ключові теми, статуси тікетів, проблеми, плани.
3. **Збереження:**
   - Зберегти самарі у файл `projects/nextcode/meeting-notes/YYYY-MM-DD-daily-summary.md`
   - Опублікувати самарі у Slack канал `#general`
   - Оновити MEMORY.md з важливою довгостроковою інформацією (наприклад, блокуючі проблеми, зміни в процесах)
4. **Оновлення статусів тікетів:** Витягнути інформацію про тікети, які будуть готові до тестування, та додати їх до списку моніторингу.

**Важливі елементи для вилучення:**
- Тікети, які розробники закінчили або готові до тестування
- Проблеми, що виникають під час тестування (наприклад, сегментація гравців, конфігурація бонусів)
- Плани на спринт (хто що робить, оцінки)
- Технічні нюанси (наприклад, Bearer токен протухає через 3 години)

**Частота:** Щодня (під час робочих годин) або при отриманні транскрипту.

**Посилання:**
- Папка з щоденними нотатками: `projects/nextcode/meeting-notes/`
- Slack канал: `#general` (C0AHRLH1Y3S)

---
