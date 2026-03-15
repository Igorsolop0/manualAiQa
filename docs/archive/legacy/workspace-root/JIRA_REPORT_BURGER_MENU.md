# Jira Test Report: Burger Menu & Google Play Button Functionality

## Тестований функціонал
- Бургер-меню (іконка для відкриття бокової панелі)
- Кнопка "Get it on Google Play" всередині меню

## Тестове середовище
- **URL:** https://minebit-casino.prod.sofon.one/
- **Браузер:** Chrome (Playwright)
- **Дата тестування:** 2026-03-06

## Тест-кейси

### 1. Відкриття бургер-меню
**Очікуваний результат:** Клік на іконку бургер-меню відкриває бокову панель
**Фактичний результат:** Потрібно виконати тестування для визначення точного селектора

### 2. Клік на "Get it on Google Play"
**Очікуваний результат:** Користувач переходить на сторінку додатка в Google Play
**Фактичний результат:** Потрібно виконати тестування для підтвердження

### 3. Перевірка сторінки Google Play
**Очікуваний результат:** Сторінка містить контент про додаток Minebit
**Фактичний результат:** Потрібно виконати тестування

## Знайдені селектори (попередні)

### Бургер-меню:
- `button[aria-label*="menu"]`
- `button.menu-toggle`
- `.burger-menu`
- `.hamburger-icon`
- `button:has(svg)`
- `[data-testid="menu-button"]`
- `button:has-text("Menu")`

### Кнопка "Get it on Google Play":
- `a[href*="play.google.com"]`
- `.google-play-button`
- `button:has-text("Get it on Google Play")`
- `a:has-text("Get it on Google Play")`
- `[data-testid="google-play-button"]`

## Наступні кроки

1. **Запустити Playwright тест** для автоматизації перевірки:
   ```bash
   cd /Users/ihorsolopii/Documents/minebit-e2e-playwright
   npx playwright test /Users/ihorsolopii/.openclaw/workspace/test-burger-menu.spec.ts
   ```

2. **Уточнити селектори** на основі результатів тестування

3. **Оновити UI_ELEMENTS.md** з точними селекторами

4. **Додати тест до регрессійного набору** Minebit

## Рекомендації
- Додати data-testid атрибути для ключових елементів UI для стабільного тестування
- Перевірити функціонал на мобільних пристроях (responsive design)
- Перевірити альтернативні шляхи доступу до меню (клавіатура, screen readers)

## Докази
- Тестовий скрипт: `test-burger-menu.spec.ts`
- UI Elements документація: `UI_ELEMENTS.md`
- Скріншоти результату будуть збережені після виконання тесту

---

**Статус:** Очікує виконання тестування
**Пріоритет:** Середній
**Призначено:** QA Team