# NextCode API Testing - Архітектура та Swagger

## 🏗️ Архітектура NextCode (Online Casino)

### Компоненти системи:
1. **Frontend** — Web/Mobile UI
2. **Backend** — API server
3. **Strapi** — Headless CMS (content management)
4. **Smartico** — Bonus/Promo system

---

## 🔍 Swagger/OpenAPI Documentation

### Пошук Swagger документації:

**Типові URL для Swagger:**
```
https://api.nextcode.tech/swagger
https://api.nextcode.tech/api-docs
https://api.nextcode.tech/docs
https://backend.nextcode.tech/swagger
https://strapi.nextcode.tech/documentation
```

**Для Strapi:**
```
https://strapi.nextcode.tech/admin
https://strapi.nextcode.tech/documentation
```

**Для Smartico:**
- Smartico usually provides API docs separately
- Check: Smartico dashboard → API Documentation

---

## 📋 Що потрібно зібрати:

### 1. Backend API
- [ ] Swagger URL
- [ ] Base URL (production/staging)
- [ ] Authentication method (JWT, API key, etc.)
- [ ] Key endpoints:
  - User management
  - Games
  - Payments
  - Bonuses
  - Transactions

### 2. Strapi CMS
- [ ] API documentation URL
- [ ] Content types (bonuses, promotions, games)
- [ ] Authentication
- [ ] Webhooks

### 3. Smartico
- [ ] API documentation
- [ ] Bonus system endpoints
- [ ] Webhook endpoints
- [ ] Integration with Backend

---

## 🎯 API Testing з Playwright

### Чому Playwright для API testing:
✅ Вже встановлено
✅ Можна комбінувати UI + API тести
✅ Підтримка authentication
✅ Request/response validation
✅ Mocking responses

### Приклад API тесту з Playwright:

```javascript
import { test, expect } from '@playwright/test';

test.describe('NextCode Backend API', () => {
  let apiContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: 'https://api.nextcode.tech',
      extraHTTPHeaders: {
        'Authorization': `Bearer ${process.env.API_TOKEN}`,
      },
    });
  });

  test('Get user profile', async () => {
    const response = await apiContext.get('/api/v1/user/profile');
    expect(response.ok()).toBeTruthy();

    const user = await response.json();
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('email');
  });

  test('Get available games', async () => {
    const response = await apiContext.get('/api/v1/games');
    expect(response.ok()).toBeTruthy();

    const games = await response.json();
    expect(Array.isArray(games)).toBeTruthy();
    expect(games.length).toBeGreaterThan(0);
  });

  test('Strapi - Get bonuses', async () => {
    const response = await apiContext.get('https://strapi.nextcode.tech/api/bonuses');
    expect(response.ok()).toBeTruthy();

    const bonuses = await response.json();
    expect(bonuses.data).toBeDefined();
  });
});
```

---

## 🔧 Setup для API Testing

### 1. Створити конфігурацію:

```javascript
// playwright.config.js
export default {
  use: {
    baseURL: process.env.API_BASE_URL || 'https://api.nextcode.tech',
    extraHTTPHeaders: {
      'Authorization': `Bearer ${process.env.API_TOKEN}`,
      'Content-Type': 'application/json',
    },
  },
};
```

### 2. Environment variables:

```bash
# .env
API_BASE_URL=https://api.nextcode.tech
API_TOKEN=your-token-here
STRAPI_URL=https://strapi.nextcode.tech
SMARTICO_URL=https://smartico.nextcode.tech
```

---

## 📊 Потенційні API тести для NextCode:

### Backend API:
- User authentication (login/register/logout)
- User profile (get/update)
- Games list (filtered by provider/category)
- Game launch (get URL/session)
- Payments (deposit/withdraw)
- Transactions history
- Bonuses (list/claim/activate)

### Strapi API:
- Content: Bonuses
- Content: Promotions
- Content: Game categories
- Content: Static pages
- Media files

### Smartico API:
- Bonus eligibility
- Bonus activation
- Wagering progress
- Bonus claim

---

## 🎯 Наступні кроки:

### 1. Зібрати інформацію:
```
? Swagger URL для Backend
? Strapi API documentation URL
? Smartico API documentation
? API tokens для тестування
? Test accounts (users)
```

### 2. Створити структуру тестів:
```
tests/
├── api/
│   ├── backend/
│   │   ├── auth.spec.js
│   │   ├── user.spec.js
│   │   ├── games.spec.js
│   │   └── payments.spec.js
│   ├── strapi/
│   │   ├── bonuses.spec.js
│   │   └── promotions.spec.js
│   └── smartico/
│       └── bonus-system.spec.js
```

### 3. Написати helper functions:
```javascript
// helpers/api.js
export async function authenticate(apiContext, email, password) {
  const response = await apiContext.post('/api/v1/auth/login', {
    data: { email, password }
  });
  const { token } = await response.json();
  return token;
}

export async function getActiveBonus(apiContext, userId) {
  const response = await apiContext.get(`/api/v1/user/${userId}/bonuses/active`);
  return response.json();
}
```

---

## 💡 Автоматизація задач:

### Можна автоматизувати:
1. **Перевірка стану бонусів** — API call раз на N хвилин
2. **Валідація нових ігор** — при додаванні гри в Strapi
3. **Моніторинг API health** — endpoint availability
4. **Smoke tests** — критичні endpoints після деплою
5. **Data validation** — консистентність даних між системами

---

## 🔗 Інтеграції:

### CI/CD Pipeline:
```yaml
# .github/workflows/api-tests.yml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright test --project=api
```

### Cron Jobs (через OpenClaw):
- Щохвилини: API health check
- Щогодини: Critical endpoints validation
- Щодня: Full API test suite
- При деплої: Smoke tests

---

## 📝 Потрібно від тебе:

1. **Swagger/OpenAPI URLs:**
   - Backend: `?`
   - Strapi: `?`
   - Smartico: `?`

2. **API Tokens:**
   - Backend API token
   - Strapi API token
   - Smartico API key

3. **Test Accounts:**
   - Test user credentials
   - Test game IDs
   - Test bonus IDs

4. **Priority endpoints:**
   - Які endpoints найважливіші для тестування?
   - Які частіше всього ламаються?

---

**Дай мені URL для Swagger документації, і я створю повний набір API тестів! 🚀**
