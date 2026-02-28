# Minebit (NextCode) — Quick Reference

**Оновлено:** 2026-02-27
**Статус:** Фріланс проєкт — вимагає ініціативи

---

## 🎯 КРИТИЧНИЙ KPI

**Ціль:** 60-65% автономності та якості тестування в NextCode

**Що трекаю:**
- ✅ Прогрес у розумінні процесів NextCode
- ✅ Пам'ятаю сам продукт MineBit
- ✅ Знаю де які елементи знаходяться
- ✅ Знаю стандартний юзер флоу
- ✅ І т.д.

**Як вимірюю:** скільки можу працювати автономно без уточнень

**Коли тікет надходить:**
1. Оцінити скільки я можу зробити самостійно
2. Запитати тільки коли дійсно неясно
3. Проявляти ініціативу — пропонувати рішення

---

## ⚠️ Відомі проблеми

### Документація
- **Великі гепи** — немає повного опису флоувів
- **Jira повільні** — часто нестабільні
- **Складно описати тести** — Ihor іноді не може чітко пояснити як тестувати

### Технічні
- **Багато модалок Smartico** — потрібно хендлити в тестах
- **Повільна Jira** — робота з тікетами займає час
- **Нестабільність** — Jira іноді падає/відповідає помилково

---

## 🎯 Мій підхід в Minebit

### Коли працюю з Minebit
1. **Проявляти ініціативу** — не чекати, пропонувати покращення
2. **Покращувати опис задач** — робити їх зрозумілими та детальними
3. **Exploratory testing** — шукати гепи, порівнювати з TestRail
4. **Запитувати уточнення** — якщо не розумію завдання

### Playwright Best Practices
```typescript
// ✅ DO — Використовувати role-based селектори
await page.getByRole('button', { name: 'Submit' }).click();

// ✅ DO — Використовувати text-based селектори
await page.getByText('Submit').click();

// ❌ DON'T — Уникати довільних CSS селекторів коли можливо
// await page.locator('button.submit-btn').click();
```

### 🎯 Розпізнавання UI елементів (AI Mode)

**Коли використовувати AI Mode для розпізнавання елементів:**
- Videos
- News
- Products
- Books
- Finance

**Три головні підходи:**

#### 1. DOM-based Selectors (Document Object Model)
- **Найнадійніший** метод для веб-додатків
- **ID та Name**: Найшвидші та найстабільніші атрибути (id="login-button")
- **CSS Selectors**: Класи, ієрархія, атрибути (.btn-primary > span)
- **XPath**: Потужна мова для пошуку за текстом (//button[text()='Зберегти'])

#### 2. Visual Recognition (Image-based)
- Використовується, коли немає доступу до коду (Flash-додатки, ігри, remote desktop)
- **Computer Vision**: Пошук елемента за шаблоном зображення (скриншот)
- **OCR**: Розпізнавання тексту в картинках/кнопках (Tesseract)

#### 3. Intelligent Recognition (AI/ML-based)
- **Self-healing**: Якщо розробник змінив ID, система аналізує інші ознаки (розмір, колір, сусідні елементи)
- **Object Detection**: Нейромережі для класифікації елементів

#### Порівняльна таблиця підходів
| Підхід | Надійність | Швидкість | Коли використовувати |
|----------|--------------|------------|-------------------|
| ID / Атрибути | Дуже висока | Дуже швидко | Є доступ до коду та унікальні ID |
| CSS / XPath | Висока | Швидко | Для складних веб-структур |
| Image Recognition | Низька | Повільно | Десктоп-додатки, ігри, Citrix |
| AI / Self-healing | Висока | Повільно | Великі проєкти, що часто змінюються |

### 🎧 iGaming специфіка — Smartico & Strapi
**Проблеми:**
- CMS генерує код, який розробники не контролюють напряму
- Часто генеруються зайві пробіли в контенті (назви акцій, текст кнопок)
- Dynamic контент робить тести "ламкими"

**Рішення:**
1. **XPath з normalize-space()** — ігнорує зайві пробіли
2. **data-testid** — найкраща практика (недоступна? потрібно уточнити)
3. **Стратегія виживання**: якщо немає data-testid — використовувати стабільні ознаки

### 🔧 Hard Skills (Технічні навички)
- ✅ **HTML & CSS** — структура тегів, вкладеність, атрибути, вплив стилів
- ✅ **DevTools** — F12 панель, інспектування елементів, консоль
- ✅ **XPath та CSS Selectors** — критично для автоматизації
- ✅ **DOM-структура** — рендеринг, динамічні зміни, Shadow DOM, iFrames

### 🧠 Soft Skills (Аналітичне мислення)
- ✅ **Увага до деталей** — знайти унікальну ознаку елемента
- ✅ **Критичне мислення** — який селектор буде "стабільним"
- ✅ **Порівняльний аналіз** — оцінити різні варіанти

### 🎯 Просунуті техніки для iGaming

#### 1. Спрощені зв'язки (Axes)
**Коли ID немає — шукайте стабільний "статичний" елемент поруч:**
```xpath
//button[normalize-space()='Прийняти участь']
//div[h2[text()='Вітаємо']]//button (пошук кнопки всередині модалки)
```

#### 2. Регулярні вирази в селекторах
**Strapi може генерувати напівдинамічні класи:**
```xpath
//*[contains(@class, 'Component_button__3aYz1')]
```

#### 3. Index-based Recognition (Останній шанс)
**Якщо модалка багато і однакові — звертатися за індексом:**
```xpath
//div[@class='modal'])[last()]  // але це шлях до нестабільних тестів!
```

#### 4. Просунутий XPath (Axes & Logic)
**Ви повинні вміти "бігати" по дереву DOM вгору-вниз:**
```xpath
//parent::div    // батьківський елемент
//following::button  // наступний елемент того ж рівня
//preceding::input   // попередній елемент
```

#### 5. Робота з iFrames
**Smartico часто вбудовується через iframe:**
```typescript
// Перемикнути контекст драйвера
await page.frameLocator('#smartico-iframe').getByText('Claim').click();

// Якщо не знаєте індекс iframe — переключитись
const frames = page.frames();
const targetFrame = frames.find(f => f.url().includes('smartico'));
```

#### 6. Shadow DOM
**Звичайний XPath там не працює — використовуйте JS executor:**
```typescript
const element = await page.evaluate(() => {
  const shadowRoot = document.querySelector('#component').shadowRoot;
  return shadowRoot.querySelector('.button');
});
```

#### 7. Wait Strategies (Очікування клікабельності)
**Модалки Smartico завантажуються із затримкою:**
```typescript
// ❌ DON'T — чекати просто присутність
await expect(locator).toBeVisible();

// ✅ DO — чекати клікабельність
await expect(locator).toBeEnabled();  // або toHaveAttribute('ready', 'true')
```

#### 8. DevTools Protocol
**Аналізуйте Network tab, щоб зрозуміти звідки контент:**
- Strapi чи Smartico?
- Це допоможе писати логічніші селектори

### 🤖 Скілт-архітектура для "майстра селекторів"

#### 1. Скіл "DOM Crawler & Tree Flattener"
- Фокус на **інтерактивних атрибутах**: button, input, a, role="button"
- **Спрощене дерево**: без скритих елементів
- **Текстовий mapper**: мапити видимий текст на конкретні вузли DOM

#### 2. Скіл "Visual Grounding" (Візуальна прив'язка)
- **Set-of-Mark (SoM) Prompting**:
  - Агент отримує скріншот
  - Всі клікабельні елементи пронумеровані візуальними мітками
  - Агент каже: "Клікай на елемент №14"
- **Ідеально для Smartico**, де DOM заплутана, але візуальна кнопка "X" завжди однакова

#### 3. Скіл "Heuristic Selector Generator"
- Агент генерує каскад селекторів за пріоритетністю:
  ```typescript
  1. Semantic: [aria-label="Close"]
  2. Text-based: //span[contains(text(), 'Бонус')]
  3. Proximity: //div[h2[text()='Вітаємо']]//button
  4. Relative path: //button[following::h2[text()='Назва слоту']]
  ```

#### 4. Скіл "Contextual Anchoring"
- Якщо структура стабільна, але класи динамічні:
```xpath
// Індекси відносно стабільних батьківських елементів
//div[@class='game-container'][1]//button[contains(text(), 'Spin')]
```

#### 5. Скіл "Shadow DOM & Iframe Specialist"
- Автоматично перевіряти наявність `#shadow-root`
- Вміти виконувати JS-скрипти через Playwright/Selenium для "пробиття" фреймів Smartico

### 🎨 Приклад модалки Smartico

**Що важко "спіймати":**
```html
<div class="smartico-modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <h2>Вітання бонус</h2>
      <button class="close-btn">×</button>
    </div>
    <div class="modal-body">
      <p>Ви отримали бонус $10!</p>
      <button class="claim-btn">Забрати</button>
    </div>
  </div>
</div>
```

**Проблеми:**
- Класи напівдинамічні (`modal__3xYz1`)
- Без `data-testid`
- Кнопка закриття може бути просто `×`

**Рішення:**
```typescript
// 1. Знайти стабільний батьківський елемент
const modal = page.getByRole('dialog').getByText('Вітання бонус');

// 2. Пошук кнопки через текст
const claimBtn = modal.getByRole('button', { name: /забрати/i });
const closeBtn = modal.getByRole('button', { name: 'Закрити' });

// 3. Чекати клікабельність
await expect(claimBtn).toBeEnabled();
```

### 💡 Порада щодо розробників
**Якщо вони не хочуть ставити ID, пропонуйте:**
- ✅ **Accessibility** — aria-label або role (стандарт індустрії)
- ✅ **data-testid** — найкраща практика для тестування
- ✅ **Stable structure** — уникати напівдинамічні класи

### 🎯 Реалізація через CDP (Chrome DevTools Protocol)
**Найкращий спосіб навчити агента — надати доступ до CDP:**
- ✅ Використовуйте бібліотеки на кшталт Playwright
- ✅ Вбудовані механізми очікування та краща робота з фреймворками
- ✅ Не потрібен чистий Selenium

### 🤖 Системний промпт: "Senior Automation Engineer"
**Роль:** Експерт з автоматизації Playwright (TypeScript), що спеціалізується на складних iGaming платформах

**Алгоритм розпізнавання (Level-by-Level):**

**Рівень 1: Бізнес-контекст та роль (Reasoning)**
- Де знаходимся? (Головна сторінка, лобі слотів чи активна модалка Smartico?)
- Яка мета цього елемента? (Це закриття вікна, запуск гри чи перехід до умов бонусу?)
- Чи є він частиною динамічного контенту? (Якщо текст виглядає як назва акції зі Strapi, він може змінитися)

**Рівень 2: User-Facing Locators (Найстабільніше!)**
- **Пріоритет:** Ігнорувати класи (які в Strapi часто динамічні)
- **Шукати за тим, що бачить гравець:**
  ```typescript
  // ✅ DO — User-facing locators
  page.getByRole('button', { name: 'Join now' });
  page.getByText('Bonus Terms');
  page.getByPlaceholder('Search slots...');
  ```
- **Тільки потім:** якщо не знайдено — використовувати складніші підходи

**Рівень 3: Стабільність аналізу**
- Якщо це "Play Now" — це стабільний маркер
- Якщо текст виглядає як назва акції зі Strapi — може змінитися

### 🧹 Skill #1: "Smart Filtering" (Робота з вкладеністю)
**В iGaming багато однакових кнопок "Play" — агент має локалізувати пошук:**
```typescript
// Знайти кнопку "Play" саме в контейнері конкретного слота
await page.locator('.slot-card')
  .filter({ hasText: 'Gonzo’s Quest' })
  .getByRole('button', { name: 'Play' })
  .click();
```

### 🪟 Skill #2: "Automatic Frame Handling"
**Для віджетів Smartico, які часто "ховаються" — використовуйте frameLocator:**
```typescript
// ✅ DO — Playwright за замовчуванням "пробиває" Shadow DOM
const smarticoPopup = page.frameLocator('#smartico-iframe-id');
await smarticoPopup.getByLabel('Close modal').click();

// ❌ DON'T — Перемикати контекст вручну як у Selenium
```

### 🎨 Skill #3: "Visual Comparisons" (Snapshot Testing)
**Для слотів, де елементи малюються на Canvas і DOM-дерева немає:**
```typescript
// Порівнювати скріншоти
await expect(page.locator('.slot-machine-canvas'))
  .toHaveScreenshot('spin-button-active.png');

// ⚠️ Use code with caution — порівнювальні скріншоти можуть бути flaky
```

### 🏗 SmarticoHandler — Шаблон класу
**Практична рекомендація:** Створіть базовий клас для взаємодії з модалками Smartico:**
```typescript
class SmarticoHandler {
  constructor(private page: Page) {}

  async waitForModal() {
    await this.page.getByRole('dialog', { name: /bonus|welcome/i }).toBeVisible();
  }

  async close() {
    const modal = this.page.getByRole('dialog', { name: /bonus|welcome/i });
    const closeBtn = modal.getByRole('button', { name: /close|cancel/i });
    await closeBtn.click();
    await expect(modal).toBeHidden();
  }

  async claimBonus(amount: string) {
    const modal = await this.waitForModal();
    const claimBtn = modal.getByRole('button', { name: /claim/i });
    await expect(claimBtn).toBeEnabled();
    await claimBtn.click();
  }
}
```

### 🎯 Priority: User-Facing Locators
**Навчіть агента ігнорувати класи (які в Strapi часто динамічні):**
- ❌ DON'T: `page.locator('.Component_button__3aYz1')`
- ✅ DO: `page.getByRole('button', { name: 'Claim' })`
- ✅ DO: `page.getByText('Bonus Terms')`
- ✅ DO: `page.getByPlaceholder('Search...')`

**Це найстабільніший підхід у Playwright!**

### ♿ Accessibility як порятунок
**Якщо розробники не дають ID, вони часто генерують aria-label або role через CMS:**
- ✅ Навчіть агента використовувати Accessibility Tree через Playwright Codegen
- ✅ Це стандарт індустрії — найбільш надійний "порятунок" відсутності ID

### 🔧 DevTools Protocol
**Network tab analysis:**
1. Відкрити F12
2. Перейти на Network tab
3. Відфільтрувати по "strapi" та "smartico"
4. Зрозуміти звідки контент — допоможе писати логічніші селектори

### 🔑 Swagger First — Не йди в лоб з UI!
**Важливо:** Перед тестуванням UI — дивись в Swagger документацію!

**Коли працюєш з:** реєстрація, поповнення балансу, KYC, email verification

**Правильний процес:**
1. **Знайти ендпоїнт в Swagger:**
   - Website API: `https://websitewebapi.prod.sofon.one/swagger/`
   - BackOffice API: `https://adminwebapi.prod.sofon.one/swagger/`

2. **Розуміти структуру запиту:**
   - Параметри (body, headers, query)
   - Типи даних (required/optional)
   - Формат відповіді

3. **Можливо протестувати API напряму:**
   - Виверифікувати що ендпоїнт працює
   - Перевірити відповідь, статус коди

4. **Тільки потім UI тестування:**
   - Тепер ти знаєш що саме відбувається
   - Знаєш які дані мають бути в формах
   - Знаєш які відповіді очікувати

**Що це дає:**
- ✅ Швидше тестування (знаєш структуру заздалегідь)
- ✅ Менше сліпого пошуку елементів на UI
- ✅ Краще розуміння системи
- ✅ Можна протестувати API напряму перед UI

### Smartico Modals — Need to Handle
- Багато модалок від Smartico:
  - Бонуси
  - Вітальні екрани
  - Налаштування
  - Promotions
- **Тестовий паттерн:**
  1. Перевірити чи модалка відкрита: `toBeVisible()`
  2. Підтвердити/закрити модалку
  3. Чекати поки вона зникне: `toBeHidden()`
  4. Продовжити тест

---

## 🔍 Exploratory Testing Process

### Коли Ihor просить exploratory testing:
1. **Знайти тікет в Jira** — отримати контекст
2. **Перевірити TestRail** — чи є існуючі тести
3. **Запустити тести** — подивитись що працює, що ні
4. **Знайти гепи** — що не покрито існуючими тестами
5. **Запропонувати нові тести** — заповнити гепи

### Коли не розумію завдання:
1. **Запитати уточнення** — "Чи можеш дати приклад кроків?"
2. **Запитати скріншоти** — показати що саме потрібно протестувати
3. **Перевірити схожі тікети** — знайти паттерни
4. **Робити допущення** — але явно сказати що це допущення

---

## 🧪 Playwright — Smartico Modal Handling

### Pattern для модалок
```typescript
// Приклад: Бонус модалка
async function handleBonusModal(page: Page) {
  // 1. Чекати модалку
  const modal = page.getByRole('dialog', { name: /bonus/i });
  await expect(modal).toBeVisible();

  // 2. Якщо треба — заповнити форму
  await modal.getByRole('textbox', { name: 'Code' }).fill('BONUS123');

  // 3. Підтвердити/закрити
  await modal.getByRole('button', { name: 'Claim' }).click();

  // 4. Чекати поки закриється
  await expect(modal).toBeHidden();
}
```

### Відомі Smartico модалки
- Bonus claim
- Welcome bonus
- Loyalty program
- Achievements
- Tournaments

---

## 📋 Тестовий чекліст перед початком

### Перед написанням тесту:
- [ ] Читаю тікет в Jira (отримую контекст)
- [ ] Перевіряю TestRail (чи є існуючі тести)
- [ ] Розумію кроки (питаю якщо ні)
- [ ] Знаю які Smartico модалки можуть з'явитись

### Після написання тесту:
- [ ] Використовую `getByRole` та `getByText`
- [ ] Хендлю всі можливі модалки
- [ ] Тест стабільний (не flaky)
- [ ] Додаю коментарі для інших QA

---

## 🎯 Цілі в Minebit

### Короткострокові:
- ✅ Покращити якість описів тікетів
- ✅ Зменшити flaky тести
- ✅ Покрити гепи в тестовому покритті

### Довгострокові:
- ✅ Створити стабільну базу тести
- ✅ Документація Smartico модалок
- ✅ Інтеграція TestRail + Playwright

---

## 📞 Коли я не розумію

### Мої запитання:
- "Можеш надати приклад кроків?"
- "Що саме я бачу на екрані?"
- "Які дані мають бути в формі?"
- "Це критичний чи nice-to-have баг?"

### Якщо все ще неясно:
- Пропоную: "Давай я запущу тест і ми подивимось разом що він робить"
- Не припускаю — явно кажу що це допущення

---

## 🔗 Корисні посилання

### Swagger Документація (Важливо!)
- **Website API:** https://websitewebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3
  - Ендпоїнти для клієнта
  - Реєстрація, поповнення балансу, KYC, email verification
- **BackOffice API:** https://adminwebapi.prod.sofon.one/swagger/index.html?urls.primaryName=API+v3
  - Ендпоїнти для адміна
  - Управління бонусами, гравцями, транзакціями

### Інші посилання
- Jira: https://next-t-code.atlassian.net/browse/
- TestRail: (URL — потрібно уточнити)
- Playwright Docs: https://playwright.dev/docs/api/class-page
- UI Knowledge Base: `/Users/ihorsolopii/.openclaw/workspace/ui-knowledge/minebit/`

### Ключові ендпоїнти для швидкого доступу
**Website API:**
- POST `/api/v3/player/login` — авторизація
- POST `/api/v3/player/register` — реєстрація
- POST `/api/v3/payment/deposit` — поповнення балансу
- POST `/api/v3/player/verify-email` — email verification
- POST `/api/v3/kyc/submit` — KYC

**BackOffice API:**
- GET `/api/v1/client/{id}` — пошук клієнта
- POST `/api/v1/payment/make-payment` — створення депозиту
- PATCH `/api/v1/payment/change-status` — зміна статусу платежу
- POST `/api/v1/wallet/credit` — поповнення балансу (CreateDebitCorrection)
- POST `/api/v1/wallet/debit` — зняття балансу (CreateCreditCorrection)

---

**Пам'ятай:** Minebit потребує більше ініціативи та пропонувань, ніж Lorypten! 🎯

---

## 📌 OUTPUT FORMAT — Standard для кожного елемента

**Для кожного елемента надавай:**

### 1. Аналіз (Коротке пояснення)
```
Аналіз: Це модалка Smartico. Він завантажується в iframe. Кнопка закриття зазвичай не має тексту, але має aria-label="Close" або іконку "X".
```

### 2. Локатор (Готовий код на Playwright + TS)
```typescript
const modal = page.frameLocator('iframe[src*="smartico"]').locator('.modal-content');
const closeBtn = modal.getByRole('button', { name: /close|закрити/i });
await closeBtn.click();
```

### 3. Альтернатива (На випадок, якщо не працює)
```typescript
// Якщо aria-label відсутній — використовувати координати або пошук по SVG іконці всередині модалки
const closeButton = modal.locator('svg').locator({ hasText: '×' });
await closeButton.click();
```

---

## 🔮 Приклад повного сценарію

**Запит користувача:** "Знайди кнопку закриття в модалці Smartico"

### Моє міркування:
```
Аналіз: Це сторонній віджет Smartico. Він завантажується в iframe. Кнопка закриття зазвичай не має тексту, але має aria-label="Close" або іконку "×".

Локатор: 
const modal = page.frameLocator('iframe[src*="smartico"]').locator('.modal-content');
const closeBtn = modal.getByRole('button', { name: /close|закрити/i });
await closeBtn.click();

Альтернатива: Якщо aria-label відсутній — використовувати координати або пошук по SVG іконці всередині модалки
const closeButton = modal.locator('svg').locator({ hasText: '×' });
await closeButton.click();
```

**Use code with caution.**

---

## ✅ CHECKLIST: Переконуйся перед написанням тесту

- [ ] Перевіряю, чи елемент в iframe
- [ ] Знаю стабільний батьківський елемент (якір)
- [ ] Перевіряю Accessibility Tree (F12 → Accessibility)
- [ ] Перевіряю Network tab (звідки контент?)
- [ ] Використовує getByRole() першочергово
- [ ] Перевіряю, чи текст статичний (назва акції Strapi)
- [ ] Маю альтернативний локатор на випадок failure
- [ ] Додав коментарі для інших QA
