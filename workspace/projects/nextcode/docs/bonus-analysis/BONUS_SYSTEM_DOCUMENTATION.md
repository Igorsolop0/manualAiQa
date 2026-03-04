# Bonus System Documentation

**Source:** Confluence QA Space + Google Docs Bonus Tech Dock
**Compiled by:** Comet browser + reviewed by OpenClaw
**Date:** 2026-02-23

---

## РОЗДІЛ 1: АРХІТЕКТУРА БОНУСНОЇ СИСТЕМИ

### 1.1 Компоненти системи

| Компонент | Роль |
|-----------|------|
| BackOffice (BO) | Створення, конфігурація бонусів та тригерів |
| Strapi | UI відображення бонусів на фронтенді, картки, slug, зображення |
| Smartico | CRM-движок: розрахунок cashback/rakeback, тригери бонусів через API |
| Kafka Topic | `Smartico.ClientBonusUpdateEvent` — lifecycle events бонусів |
| Swagger (CRM Gateway) | Ендпоїнт для ручної активації бонусів: https://crmgateway.qa.cp.nextcode.tech/swagger/index.html |
| DBeaver / DB | Отримання Security Code API-юзера |

### 1.2 Де налаштовується бонус в BO

```
Bonuses → Common → General Setup
```

---

## РОЗДІЛ 2: ТИПИ БОНУСІВ

### 2.1 Загальна класифікація (BO Types)

| Тип | Опис |
|-----|------|
| Campaign Wager Casino | Бонусні гроші + wager, треба прокрутити щоб вивести |
| Campaign FreeSpin | Безкоштовні спіни на ігри |
| Split Match + FreeSpin | ФС + вейджер на виграш з ФС |
| CashBack Bonus | Кешбек через Smartico |
| Campaign Cash | Кеш без вейджеру або з вейджером |
| Match | Відповідний бонус до депозиту |

---

### 2.2 Welcome Pack (Progressive Deposit Bonus)

**Концепція:** Прогресивна серія з 4 бонусів для нових юзерів.

**Логіка розблокування:**
- Bonus 1 — доступний одразу після реєстрації (auto або manual claim)
- Bonus 2 — тільки після завершення Bonus 1 + 1-й депозит
- Bonus 3 — після завершення Bonus 2 + 2-й депозит
- Bonus 4 — після завершення Bonus 3 + 3-й депозит

**Депозитні тири:**

| Тір | Депозит | Бонус |
|-----|---------|-------|
| Tier 1 | Мінімальний | Base % + FS |
| Tier 2 | Середній | Increased % + more FS |
| Tier 3 | Максимальний | Max % + max FS |

**Стани бонусу:**

| Стан | Поведінка системи |
|------|-------------------|
| Registration | Всі 4 бонуси видно на сторінці бонусів |
| Activation | Активований бонус → Active Bonuses |
| FS Completed | Перехід у Wager Phase (той самий bonus ID!) |
| Wager Completed | Бонус зникає з активних, наступний розблоковується |

**⚠️ Обмеження:**
- Одночасно тільки 1 активний Welcome Pack бонус
- Строго по черзі — Bonus 2 без закриття Bonus 1 неможливий
- FS кредитуються в одну конкретну слот-гру (вказана в картці)

**Welcome Pack у BO:**
- `Bonuses → Bonus Package` — там додаються бонуси один за одним
- Бонуси в welcome pack повинні мати deposit trigger

---

### 2.3 Signup Code Bonus (Registration Promo Code Bonus)

**Концепція:** Бонус активується під час реєстрації через промокод.

**🔴 HIDDEN PLACE:** Бонус НЕ видно в жодній секції бонусів до введення промокоду під час реєстрації!

**Flow активації:**
1. Юзер відмічає "Use promo code" під час signup
2. Вводить валідний промокод → BE валідує
3. Після реєстрації → бонус з'являється в Available Bonuses
4. Юзер активує вручну → переходить у Active Bonuses
5. Після завершення/скасування → зникає назавжди

**⚠️ Критичні правила:**
- Промокод можна використати тільки 1 раз при реєстрації
- Якщо Welcome Pack автоактивувався → Signup Code Bonus НЕ замінює його, а чекає в Available
- Пост-реєстраційне введення коду — неможливе
- Скасування спалює всі FS та бонусні кошти — відновлення неможливе

---

### 2.4 Promo Code Bonus (Non-signup, на сторінці бонусів)

**Концепція:** Промокод вводиться в спеціальне поле на Bonus Page (не при реєстрації).

**🔴 HIDDEN PLACE:** Бонус прихований до введення коду. Поле введення промокоду знаходиться безпосередньо на Bonus Page.

**Flow:**
1. Юзер переходить на Bonuses Page
2. Вводить промокод у dedicated input field
3. Бонус з'являється в Available Bonuses
4. Активує вручну → Active Bonuses
5. Після завершення/скасування → зникає назавжди

**Контент бонусу (видно в info card ℹ):**
- Bonus %, Max Bonus, Min Deposit
- FS Count, FS Game, Max Win
- Wager Multiplier, Expiry, Bet Limits

**⚠️ Обмеження:**
- 1 промокод = 1 бонус, 1 раз на юзера
- Не можна стекати з вже активним promo-бонусом
- Не замінює Welcome Pack

---

### 2.5 Regular Bonuses (Cashback, Rakeback, Reload)

Конфігуруються в BO, тригеруються та розраховуються через Smartico, відображаються в Strapi.

#### Cashback
- **Тригер:** двічі на тиждень (вівторок і п'ятниця)
- **Розрахунок:** net loss formula в Smartico
- Якщо немає net loss → бонус не видається
- Відображається як info card (завжди) + окрема claim card (коли тригернуто)
- **Crediting:** bonus funds / real funds / site token (залежить від конфігу)

#### Rakeback
- Розраховується щодня в Smartico (на основі total wagered)
- Видно завжди на Bonus Page
- Бони з бонусних коштів можуть не зараховуватись в rake
- Не можна клеймити поки активний інший бонус

#### Weekly Reload
- **Тригер:** кожну п'ятницю (активність попереднього тижня)
- Claim вручну

#### Monthly Reload
- **Тригер:** 1-й день місяця (активність попереднього місяця)
- Tiered rewards залежно від суми вейджеру
- Claim вручну

#### Weekend Reload
- Розблоковується 1 раз на тиждень
- **Вимоги:** Loyalty Level 2 + вейджер мінімум $500
- Після розблокування стає deposit bonus (пропорційно до депозиту)

---

## РОЗДІЛ 3: НАЛАШТУВАННЯ БОНУСУ В BO — ПОВНІ ПОЛЯ

### 3.1 General Setup (Загальні поля)

| Поле | Опис | Важливо |
|------|------|---------|
| Active (checkbox) | Робить бонус активним | ⚠️ ОБОВ'ЯЗКОВО проставити! |
| Name | Назва для клієнта на порталі | Required |
| Description | Опис бонусу | Required |
| Partner | Портал/бренд де бонус доступний | Required |
| Type | Тип бонусу (Campaign/Wager/FS/etc.) | Required |
| Player ID | Бонус тільки для конкретного гравця | Optional / Hidden |
| Bonus Category | Категорія бонусу | Optional |
| Start Time / Finish Time | Дата/час активації та закриття | Required |
| Affiliate | Лінк афіліата | Optional |
| Max Receivers Count | Скільки разів бонус може бути використаний | Optional |
| Max Granted | Максимальна сума до видачі | Optional |
| Turnover Count | Кількість оборотів (x) для вейджеру | Важливо |
| Valid for awarding (hours) | Коли бонус може бути виданий | Optional |
| Valid for spending (hours) | Коли бонус може бути використаний до скасування | Optional |
| Reusing max Count | Загальна кількість повторних видач | Optional |
| Reusing max Count per Day/Week/Month | Ліміти повторних видач | Optional |
| Contribution Template | Шаблон внеску ігор у вейджер | Optional |
| Min CO | Мінімальна сума для cashout (якщо < → бонус закривається) | ⚠️ Критично |
| Max CO | Максимальна сума переведення з бонус-балансу на реал | Optional |
| Max CO Multiplier | Множник для макс. кешауту | Optional |
| Real Bets Only for Wagering | Тільки реальні ставки зараховуються у вейджер | Optional |
| Hidden / Edge Wager Bet Restriction | Правила які ставки зараховуються у вейджер | Optional |
| Bet Account Percent | % ставки що зараховується у вейджер | Optional |
| Is Smartico (checkbox) | Для Smartico-managed бонусів | ⚠️ Обов'язково для Smartico |
| Multicurrency mode | Розширений режим мульти-валют | Hidden feature |

---

### 3.2 Trigger Settings

**Шлях:** `Bonuses → Triggers → Create Trigger Settings`

**Типи тригерів:**

| Тип | Умова |
|-----|-------|
| Any Deposit | Після будь-якого депозиту |
| Specific Deposit | Депозит конкретної суми |
| PromoCode | Юзер вводить промокод |
| Campaign Link Code | Реферальне посилання |
| Sign In / Sign Up | Логін або реєстрація |

**Поля тригера Any Deposit:**

| Поле | Опис |
|------|------|
| Calculation Type: Fixed | Фіксована сума до bonus account |
| Calculation Type: Percent of Source | % від депозиту до bonus account |
| Min Amount | Мінімальна сума депозиту |
| Max Amount | Максимальна сума депозиту |
| Up To Amount | Ліміт суми яку можна отримати на бонусний рахунок |
| Week Days | Дні тижня коли тригер активний |

**Поля тригера PromoCode:**

| Поле | Опис |
|------|------|
| Bonus Setting Codes | Сам промокод |
| Min Amount | Мінімальна сума для бонусного балансу |
| Week Days | Дні тижня |

**Прив'язка тригера до бонусу:**
- 1 тригер → Order = 0
- Кілька тригерів (наприклад промокод + депозит) → Order 0, 1, ... (0 = перший)

---

## РОЗДІЛ 4: MAX CASHOUT MULTIPLIER — ДЕТАЛЬНИЙ ОПИС

Поле `Max CO Multiplier` визначає максимальну суму виводу з бонусних виграшів.

| Опція | Розрахунок |
|-------|------------|
| Not Selected | Без обмежень |
| Bonus Balance | Max CO = (Bonus Balance + FS Winnings) × Multiplier |
| Deposit Balance | Max CO = Deposit Amount × Multiplier |

**⚠️ КРИТИЧНО:** Якщо обрано Deposit Balance для no-deposit бонусу → система автоматично fallback до Bonus Balance логіки!

**Формули:**
- Deposit bonus + Deposit Balance mode: `$100 deposit × 5x = $500 max cashout`
- Deposit bonus + Bonus Balance mode: `($75 bonus + $30 FS winnings) × 2x = $210`
- No-deposit + Bonus Balance: `($20 initial + $15 FS) × 3x = $105`

**🔴 HIDDEN PLACE:** Перевірка Max Win Amount:
```
Clients & Segments → [Client] → Dashboard → Account Info → Max Win Amount
```

---

## Тестові кейси — Gap Analysis

### ✅ Існуючі тести (8 шт)
- `bonuses-unauth-sign-up-flow.md` — Unauth bonuses page → Sign Up modal
- `eligible-bonuses.spec.ts` (smoke) — Eligible bonuses for player
- `eligible-bonuses.spec.ts` (regression) — Bonus structure validation
- `bonuses.spec.ts` (E2E) — Unauth bonuses page UI
- `bonuses-authenticated.spec.ts` (exploratory) — Auth bonuses page

### ❌ Відсутні тести (пріоритет)

| Пріоритет | Тип | Причина |
|-----------|-----|---------|
| **P0** | Welcome Pack | Ключовий флоу для нових гравців |
| **P0** | Signup Code | Приховані бонуси — критичний edge case |
| **P1** | Promo Code | Основна функція бонусної сторінки |
| **P1** | Max Cashout | Фінансові розрахунки |
| **P2** | Regular Bonuses | Cashback/Rakeback — Smartico залежність |
| **P2** | Bonus States | Lifecycle тестування |

---

## Ключові ендпоїнти API

### Website API (Client)
- `GET /api/v3/Bonuses/Eligible` — доступні бонуси
- `GET /api/v3/Bonuses/Active` — активні бонуси
- `POST /api/v3/Bonuses/Claim` — активувати бонус
- `POST /api/v3/Bonuses/ClaimPromoCode` — застосувати промокод

### BackOffice API (Admin)
- `GET /api/v3/Bonus` — список бонусів
- `POST /api/v3/Bonus` — створити бонус
- `GET /api/v3/BonusTrigger` — тригери
- `POST /api/v3/BonusTrigger` — створити тригер

---

## Сегменти, що впливають на активацію бонусів (Minebit)

**Джерело:** Повідомлення від проджект менеджера Danylo (бренд Minebit), 2026-03-04.

**Важливо:** Ця інформація критична для створення користувачів на продакшн-енвайронменті, щоб бонуси працювали правильно.

### 4 сегменти, які Вадим встановлює як тригер для активації:

| Сегмент | Тип | Призначення |
|---------|-----|-------------|
| Multiaccount | Комплексний | Автоматично присвоюється системою |
| Bonus Hunter | Статичний | Виставляється вручну |
| Mult | Статичний | Виставляється вручну |
| Fraud_reg_pass | Комплексний | Автоматично присвоюється системою |

**Правило:** Якщо гравцю присвоєно хоча б один із цих сегментів, активація бонусів для нього **недоступна**.

### Сегмент MULTI_BONUS_ALLOWED

- **Призначення:** Повертає можливість отримувати бонуси (якщо гравець раніше потрапив у блокуючі сегменти).
- **Оновлення:** Сегменти оновлюються через певний час автоматично. Для термінового оновлення потрібно звернутися до Danylo (тригернути вручну).

### Сегменти, які НЕ присвоюються автоматично

Ці сегменти **не присвоюються** гравцям, тому не блокують бонуси:
- ВІП (VIP)
- ПреВІП (Pre-VIP)
- Потенційний ВІП (Potential VIP)

---

## Корисні посилання

- Confluence Bonuses Setup: https://next-t-code.atlassian.net/wiki/spaces/QS/pages/204111989/Bonuses+setup
- CRM Gateway Swagger: https://crmgateway.qa.cp.nextcode.tech/swagger/index.html
- Website API v3: https://websitewebapi.prod.sofon.one/swagger/index.html
- BackOffice API v3: https://adminwebapi.prod.sofon.one/swagger/index.html
