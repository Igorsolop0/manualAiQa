# MEMORY.md - Long-Term Memory


---

## Notes
- All emails from jira@next-t-code.atlassian.net are Jira notifications
- Ticket format: CT-XXX or PR-XXXX
- Jira base URL: https://next-t-code.atlassian.net/browse/

---


---

## Installed Skills (Use When Needed)

### prompt-engineering-expert
**Use when Ihor has problems writing prompts**

Location: `/Users/ihorsolopii/.openclaw/workspace/skills/prompt-engineering-expert`

**Capabilities:**
- Prompt analysis & optimization
- Custom instructions design for AI agents
- Chain-of-thought, few-shot, XML techniques
- Troubleshooting prompt issues
- Best practices for Gemini/Cline/OpenClaw prompts

**When to suggest:**
- "Як написати промпт для..."
- "Чи хороший цей промпт?"
- "Чому цей промпт не працює?"
- "Оптимізуй інструкції для агента"

---

### Notion API
**Status:** ✅ Configured

**API Key:** `~/.config/notion/api_key`

**Workspace pages:**
- Need to do - TODO Tracker
- FamAssistant
- US vs Europe AI Market Analysis
- Prospects Database
- AI Dev Tools Consulting Marketplace

**Use for:** Creating notes, managing TODOs, database queries

---

### clawddocs
**Use for OpenClaw documentation questions**

- Setup providers (Discord, Telegram, WhatsApp)
- Cron jobs, webhooks, automation
- Troubleshooting gateway/browser issues
- Config snippets

---

### playwright-mcp
**Status:** ✅ Installed

**Use for:** MCP-based browser automation (alternative to playwright-cli)

---

### reflect-learn
**Status:** ✅ Auto-reflection ENABLED

**Location:** `~/.reflect/`

**What it does:**
- Analyzes conversations for learnings from corrections
- Proposes updates to agent files, MEMORY.md, or new skills
- "Correct once, never again" philosophy

**Commands:**
- `/reflect` — Run reflection now
- `/reflect status` — Show state & metrics
- `/reflect review` — Review low-confidence learnings

**Auto-triggers:** PreCompact hook (before context compaction)

---


---

## Pending Tasks

**Tomorrow 13:30:** Remind about balance API issue
- `CreateDebitCorrection` not adding balance
- Need to investigate why

---


---

## Austria Information Hub (Notion)

**Status:** ✅ Active

**Created:** 2026-02-24

**Notion Page:** https://www.notion.so/Austria-31121ca6a7778147af0fdd5b73a52d64

**Location:** Ihor - Profile → Austria - Інформаційний хаб

**What's inside:**
- Ключові дати та дедлайни (тимчасовий захист, пенсії, RWR+)
- Гарячі лінії (BBU, ПФУ)
- Корисні посилання (категоризовані):
  - 🇺🇦 Міграція/Українці (BBU, Familienbeihilfe, Aufenthaltsrecht, пенсії)
  - 💼 Податки/Працівники (BMF, FinanzOnline)
  - 👶 Сім'я/Діти (MeineSV, Wien.gv.at)
  - 📰 Новини/Уряд (Bundeskanzleramt, BFA, Oesterreich.gv.at)
  - 🌐 Міжнародні організації (UNHCR)

**How to update:**
- Користувач пише "/austria" або "перевір Австрію"
- Я роблю пошук по офіційних джерелах
- Нові посилання додаю в Notion

**Last Check:** 2026-02-24

**Cron Job:** `be670aac-f0af-462d-bc09-56cfc12ca0e4` (Austria Weekly Check — понеділок о 9:00)

---


---

## 🎯 Фінансова Ціль: Квартира

**Мета:** Накопичити ~50,000 € на квартиру (Відень або Дюссельдорф)

**Статус:** Активна

**Дата постановки:** 2026-02-19

**Контекст:**
- Власник Seeker phone on Solana
- Інтерес до крипти
- Сім'я (дружина + син)
- Працює на двох роботах (Sdui + NextCode)

**Що я можу робити:**
- Моніторинг крипто ринків (Solana, DeFi протоколи)
- Аналіз пасивного доходу (staking, yield farming, dividend stocks)
- Розрахунки та планування
- Пошук можливостей
- Регулярні нагадування та перевірка прогресу

**Профіль:**
- IT-спеціалісти (без підприємницького досвіду)
- Стратегія: заробіток + пасивні інвестиції (не створення бізнесу)
- Класичний шлях накопичення

**Фінансові дані (2026-02-19):**
- Поточні заощадження: ~15-17,000 €
- Сімейний дохід: ~7,500-7,800 €/міс
- Витрати: ~6,000-6,500 €/міс
- Потенціал заощаджень: 1,000-1,800 €/міс (очікується деталізація витрат)
- Горизонт: 5 років
- Ризик-профіль: Збалансований
- Віра в crypto game-changer

---


---

## 🍔 Структурована методологія тест-дизайну (Burger Approach)

**Додано:** 2026-02-28  
**Джерело:** Ihor's structured QA approach  
**Файл:** `QA_TEST_DESIGN_APPROACH.md`

### Основна ідея
Методологія "бургер" — це структурований підхід до тест-дизайну, де кожен шар відповідає за певний аспект:

0. **Memory Check (перед будь-яким аналізом)** — пошук релевантного контексту в пам'яті
1. **Feature container (котлета/судок)** — контекст фічі, вимоги, обмеження
2. **Testing types (салат)** — види тестування (functional, security, usability...)
3. **Test design techniques (помідор)** — техніки (EP, BVA, Decision Tables...)
4. **Principles & risk-based approach (булочка)** — принципи, ризики, пріоритезація
5. **Test scenarios (готовий бургер)** — сценарії тестування

### Memory Check (деталі)
**Перед початком будь-якого аналізу завжди шукай релевантний контекст у пам'яті:**

**MEMORY CHECK — виконуй перед кожним тікетом:**

1. **Доменні патерни**
   - Чи тестував я схожі фічі раніше? (наприклад, призначення бонусів, ліміти депозитів, KYC флоу, теги, операції з гаманцями)
   - Які edge cases або баги знаходили в схожих тікетах?
   - Які інтеграції були задіяні і що зламалося минулого разу?

2. **Відомі ризики з пам'яті**
   - Чи є відомі нестабільні області в цьому домені? (наприклад, затримки синхронізації Smartico, race conditions Wallet Service, розбіжності статусів Provider Manager)
   - Чи є відомі проблеми зворотної сумісності?
   - Чи є повторювані патерни дефектів для цього типу змін?

3. **Наявне тестове покриття**
   - Чи є вже Playwright тести (API або UI) для цієї області?
   - Які тестові файли / хелпери вже існують, які можна повторно використати?
   - Які патерни тестових даних вже працюють в цьому середовищі?

4. **Знання про середовище та конфігурацію**
   - Чи є відомі проблеми, специфічні для середовища, для цієї області функціоналу?
   - Чи є специфічні тестові акаунти, токени або сиди, які варто використовувати?

**Виводи це коротким блоком:**
```
Memory relevant to this ticket:
- Similar tickets tested: ...
- Known risks/patterns: ...
- Existing test coverage: ...
- Reusable helpers/accounts: ...
- Nothing relevant found (if memory is empty for this area)
```

**Тільки після Memory Check → переходь до layered analysis (Simple або Full режим залежно від складності тікету).**

### Коли застосовувати
- **Завжди** при отриманні задач на тестування нової фічі
- **Завжди** при аналізі тікетів Jira для Minebit/NextCode
- **Завжди** при проектуванні тестів для Lorypten
- **Особливо важливо** коли вимоги нечіткі — методика допомагає виявити гепи

### Ключові правила
- **Завжди починати з Memory Check** — перевіряти наявний контекст перед аналізом
- Не пропускати шари — проходити послідовно 0-5
- Якщо вимоги незрозумілі — явно вказувати, задавати питання
- Прив'язувати кожен сценарій до вимоги, виду тестування та техніки
- Застосовувати домен-специфічні адаптації (казино, платежі, Web3)
- **CRITICAL GUARDRAIL (TEST TYPES):** Ніколи не генерувати Security/Performance/Load/Usability тести для функціональних тікетів, якщо користувач явно цього не попросив.
- **CRITICAL GUARDRAIL (TESTRAIL):** Перед відправкою або генерацією тест-кейсів для TestRail, **ЗАВЖДИ валідувати** їх за правилами з файлу `TESTRAIL_STANDARDS.md` (Language = English, no Jira IDs in titles, auto-learning dictionary).

### Адаптації для наших проєктів
**Minebit/NextCode (казино):**
- Завжди враховувати платежі, бонусні системи, KYC
- Використовувати Swagger First підхід (API перед UI)
- Пам'ятати про Smartico модалки
- Тестувати на рівні API (Website API, BackOffice API, Wallet API)

**Playwright automation:**
- Оцінювати, які сценарії можна автоматизувати
- Використовувати `getByRole()`, `getByText()` замість CSS селекторів
- Налаштовувати тестові дані через API перед UI тестами

**Lorypten (Solana Web3):**
- Тестувати транзакції блокчейну, підключення гаманців
- Перевіряти gas fees, network conditions
- Тестувати smart contract interactions

---


---

## 🎯 Мій підхід до роботи з проєктами

**🎯 КРИТИЧНИЙ KPI (60-65% автономності):**
- **Ціль:** 60-65% автономності та якості тестування в NextCode
- **Що трекаю:**
  - Прогрес у розумінні процесів NextCode
  - Пам'ятаю сам продукт MineBit
  - Знаю де які елементи знаходяться
  - Знаю стандартний юзер флоу
  - І т.д.
- **Як вимірюю:** скільки можу працювати автономно без уточнень

---

**Два проєкти з різними рівнями документації:**

### Lorypten (Solana Web3)
- ✅ **Повна документація** (~200KB) — готовий QA-пакет
- ✅ Структура, архітектура, API, домен, тестова стратегія
- ✅ Коли працюю з Lorypten — маю повний контекст

### Minebit (NextCode) — фріланс проєкт
- ⚠️ **Проблеми з документацією** — великі гепи
- ⚠️ Jira повільні та нестабільні
- ⚠️ Складно пояснити як тестувати той чи інший тікет
- ⚠️ Багато модалок від Smartico — потрібно хендлити

**Моє завдання в Minebit:**
- ✅ **Проявляти ініціативу** — не чекати, а пропонувати покращення процесів
- ✅ **Покращувати опис задач** — робити їх зрозумілими та детальними
- ✅ **Exploratory testing** — порівнювати з TestRail, заповнювати гепи
- ✅ **Playwright best practices** — використовувати `getByRole`, `getByText` замість довільних селекторів
- ✅ **Розуміти Smartico модалки** — знати які модалки існують та як їх хендлити

**Коли Ihor запитує про Minebit:**
1. Автоматично переключаюсь в режим "Minebit — потребує більше контексту та ініціативи"
2. Не чекаю на детальні інструкції — пропоную варіанти
3. Якщо не розумію завдання — запитую уточнення, але не пасивний
4. Пам'ятаю про Smartico модалки — згадую про них в тестах

**Playwright підхід для Minebit:**
- Використовувати `getByRole()` — найнадійніший та доступний метод
- Використовувати `getByText()` — коли потрібно знайти текст
- Уникати довільних селекторів (`css selectors`) коли це можливо
- Для модалок Smartico — перевіряти чи відкрити, чекати `toBeVisible()`, закривати після тесту

**Minebit Cheat Sheet:**
- **`projects/nextcode/MINEBIT_CHEAT_SHEET.md`** — Швидкий довідник для роботи з Minebit:
  - Відомі проблеми (документація, повільна Jira, модалки Smartico)
  - Мій підхід в Minebit (ініціатива, покращення описів)
  - Playwright best practices (getByRole, getByText)
  - Exploratory testing процес
  - Smartico modal handling pattern
  - Тестовий чекліст
  - Коли я не розумію (мої запитання)
  - **🔑 Swagger First — не йди в лоб з UI!**

**Важлива порада від Ihor:**
> "Є доступ до Swagger документації NextCode. Використовуй її якщо потрібно щось протестувати на UI: реєстрація, поповнення балансу, KYC, email verification. Не йди прямо в лоб з пошуком елементів на UI — оптимізовуй процеси."

**Що це означає:**
1. Перед UI тестуванням — дивись в Swagger (Website API / BackOffice API)
2. Розумій структуру запиту (параметри, типи даних)
3. Можливо протестувати API напряму
4. Тільки потім переходити до UI — тепер ти знаєш що саме відбувається

---
