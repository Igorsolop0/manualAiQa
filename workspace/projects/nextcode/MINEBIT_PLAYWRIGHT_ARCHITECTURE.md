# Minebit Playwright Framework Architecture

**Project:** Minebit Casino (NextCode)  
**Type:** API + E2E + Mobile Testing  
**Tech Stack:** Playwright, TypeScript/JavaScript

---

## 📁 Project Structure

```
minebit-automation/
├── playwright.config.ts              # Main config with multi-project setup
├── playwright.config.api.ts          # API-only config
├── playwright.config.e2e.ts          # E2E-only config
├── package.json
├── tsconfig.json
│
├── src/
│   ├── api/                          # API Testing Layer
│   │   ├── clients/
│   │   │   ├── website-api.client.ts     # Website API v3 client
│   │   │   ├── backoffice-api.client.ts  # BackOffice API v1 client
│   │   │   └── graphql.client.ts         # GraphQL client (registration)
│   │   │
│   │   ├── models/
│   │   │   ├── requests/                 # Request DTOs
│   │   │   └── responses/                # Response DTOs
│   │   │
│   │   └── services/
│   │       ├── auth.service.ts           # Auth operations
│   │       ├── bonus.service.ts          # Bonus operations
│   │       ├── payment.service.ts        # Payment operations
│   │       └── player.service.ts         # Player CRUD
│   │
│   ├── e2e/                          # E2E Testing Layer
│   │   ├── pages/
│   │   │   ├── base.page.ts             # Base Page Object
│   │   │   ├── login.page.ts
│   │   │   ├── lobby.page.ts
│   │   │   ├── game.page.ts
│   │   │   ├── bonus.page.ts
│   │   │   ├── profile.page.ts
│   │   │   └── payment.page.ts
│   │   │
│   │   ├── components/
│   │   │   ├── header.component.ts
│   │   │   ├── footer.component.ts
│   │   │   ├── modal.component.ts
│   │   │   └── bonus-card.component.ts
│   │   │
│   │   └── fixtures/
│   │       └── e2e.fixture.ts            # E2E-specific fixtures
│   │
│   ├── mobile/                       # Mobile Testing Layer
│   │   ├── devices/
│   │   │   ├── iphone-14.ts
│   │   │   ├── pixel-7.ts
│   │   │   └── galaxy-s23.ts
│   │   │
│   │   └── pages/
│   │       └── mobile-*.page.ts          # Mobile-specific pages
│   │
│   ├── mocks/                        # Mock Backend Layer
│   │   ├── handlers/
│   │   │   ├── auth.handler.ts           # Auth mock handlers
│   │   │   ├── bonus.handler.ts          # Bonus mock handlers
│   │   │   └── payment.handler.ts        # Payment mock handlers
│   │   │
│   │   ├── data/
│   │   │   ├── bonuses.mock.json
│   │   │   ├── games.mock.json
│   │   │   └── players.mock.json
│   │   │
│   │   └── server.ts                     # Mock server setup
│   │
│   ├── fixtures/                     # Test Fixtures
│   │   ├── api.fixture.ts                # API context fixtures
│   │   ├── auth.fixture.ts               # Auth fixtures
│   │   ├── player.fixture.ts             # Player creation/cleanup
│   │   └── index.ts                      # Combined fixtures
│   │
│   ├── utils/                        # Utilities
│   │   ├── env.ts                        # Environment config
│   │   ├── logger.ts                     # Logging
│   │   ├── helpers.ts                    # Common helpers
│   │   ├── waiters.ts                    # Custom waiters
│   │   └── assertions.ts                 # Custom assertions
│   │
│   └── config/
│       ├── environments.ts               # Env configurations
│       └── test-data.ts                  # Test data factories
│
├── tests/
│   ├── api/                          # API Tests
│   │   ├── auth/
│   │   │   ├── login.spec.ts
│   │   │   ├── register.spec.ts
│   │   │   └── logout.spec.ts
│   │   │
│   │   ├── bonus/
│   │   │   ├── eligible-bonuses.spec.ts
│   │   │   ├── activate-bonus.spec.ts
│   │   │   └── promo-code.spec.ts
│   │   │
│   │   ├── payment/
│   │   │   ├── deposit.spec.ts
│   │   │   └── withdraw.spec.ts
│   │   │
│   │   └── player/
│   │       ├── profile.spec.ts
│   │       └── balance.spec.ts
│   │
│   ├── e2e/                          # E2E Tests
│   │   ├── auth/
│   │   │   ├── login.flow.spec.ts
│   │   │   └── registration.flow.spec.ts
│   │   │
│   │   ├── bonus/
│   │   │   ├── claim-bonus.flow.spec.ts
│   │   │   └── wagering.flow.spec.ts
│   │   │
│   │   └── game/
│   │       └── play-game.flow.spec.ts
│   │
│   ├── mobile/                       # Mobile Tests
│   │   ├── login.mobile.spec.ts
│   │   └── game.mobile.spec.ts
│   │
│   └── mocked/                       # Mocked Backend Tests
│       ├── ui-states.mocked.spec.ts
│       └── error-handling.mocked.spec.ts
│
├── test-results/                     # Test artifacts
│   ├── screenshots/
│   ├── videos/
│   └── traces/
│
└── reports/                          # Test reports
    └── html/
```

---

## ⚙️ Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';
import { ENV } from './src/config/environments';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
  ],
  
  use: {
    baseURL: ENV.websiteUrl,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // API Tests
    {
      name: 'api',
      testDir: './tests/api',
      use: { 
        baseURL: ENV.apiUrl,
      },
    },

    // E2E - Desktop Chrome
    {
      name: 'e2e-chrome',
      testDir: './tests/e2e',
      use: { 
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    // E2E - Desktop Firefox
    {
      name: 'e2e-firefox',
      testDir: './tests/e2e',
      use: { 
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    // E2E - Desktop Safari (WebKit)
    {
      name: 'e2e-webkit',
      testDir: './tests/e2e',
      use: { 
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    // Mobile - iPhone 14
    {
      name: 'mobile-iphone',
      testDir: './tests/mobile',
      use: {
        ...devices['iPhone 14'],
        baseURL: ENV.websiteUrl,
      },
    },

    // Mobile - Pixel 7
    {
      name: 'mobile-pixel',
      testDir: './tests/mobile',
      use: {
        ...devices['Pixel 7'],
        baseURL: ENV.websiteUrl,
      },
    },

    // Mocked Backend Tests
    {
      name: 'mocked',
      testDir: './tests/mocked',
      use: {
        baseURL: 'http://localhost:3000', // Mock server
      },
    },
  ],

  webServer: {
    command: 'npm run mock-server',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### src/config/environments.ts

```typescript
type Environment = 'prod' | 'qa' | 'dev';

interface EnvironmentConfig {
  name: Environment;
  apiUrl: string;
  websiteUrl: string;
  backofficeUrl: string;
  graphqlUrl: string;
  partnerId: number;
  boUserId: number;
}

const environments: Record<Environment, EnvironmentConfig> = {
  prod: {
    name: 'prod',
    apiUrl: 'https://websitewebapi.prod.sofon.one',
    websiteUrl: 'https://minebit-casino.prod.sofon.one',
    backofficeUrl: 'https://adminwebapi.prod.sofon.one',
    graphqlUrl: 'https://minebit-casino.prod.sofon.one/graphql',
    partnerId: 5,
    boUserId: 560,
  },
  qa: {
    name: 'qa',
    apiUrl: 'https://websitewebapi.qa.sofon.one',
    websiteUrl: 'https://minebit-casino.qa.sofon.one',
    backofficeUrl: 'https://adminwebapi.qa.sofon.one',
    graphqlUrl: 'https://minebit-casino.qa.sofon.one/graphql',
    partnerId: 5,
    boUserId: 1,
  },
  dev: {
    name: 'dev',
    apiUrl: 'https://websitewebapi.dev.sofon.one',
    websiteUrl: 'https://minebit-casino.dev.sofon.one',
    backofficeUrl: 'https://adminwebapi.dev.sofon.one',
    graphqlUrl: 'https://minebit-casino.dev.sofon.one/graphql',
    partnerId: 5,
    boUserId: 1,
  },
};

export const ENV = environments[process.env.ENV as Environment || 'qa'];
```

---

## 🔧 API Client Layer

### src/api/clients/website-api.client.ts

```typescript
import { APIRequestContext, APIResponse } from '@playwright/test';
import { ENV } from '../../config/environments';

export class WebsiteApiClient {
  private request: APIRequestContext;
  private baseUrl: string;
  private partnerId: number;

  constructor(request: APIRequestContext) {
    this.request = request;
    this.baseUrl = ENV.apiUrl;
    this.partnerId = ENV.partnerId;
  }

  private get defaultHeaders() {
    return {
      'Content-Type': 'application/json',
      'website-locale': 'en',
      'website-origin': ENV.websiteUrl,
      'x-time-zone-offset': '-60',
    };
  }

  async getBonus<T = any>(
    endpoint: string, 
    token?: string, 
    data?: Record<string, any>
  ): Promise<{ response: APIResponse; body: T }> {
    const url = `${this.baseUrl}/${this.partnerId}/api/v3/Bonus/${endpoint}`;
    
    const body = {
      partnerId: this.partnerId,
      languageId: 'en',
      timeZone: -60,
      countryCode: 'AT',
      domain: ENV.websiteUrl,
      token: token || undefined,
      ...data,
    };

    const response = await this.request.post(url, {
      headers: this.defaultHeaders,
      data: body,
    });

    const responseBody = await response.json() as T;
    return { response, body: responseBody };
  }

  async getClient<T = any>(
    endpoint: string, 
    token: string, 
    data?: Record<string, any>
  ): Promise<{ response: APIResponse; body: T }> {
    const url = `${this.baseUrl}/${this.partnerId}/api/v3/Client/${endpoint}`;
    
    const body = {
      partnerId: this.partnerId,
      languageId: 'en',
      timeZone: -60,
      countryCode: 'AT',
      domain: ENV.websiteUrl,
      token,
      ...data,
    };

    const response = await this.request.post(url, {
      headers: this.defaultHeaders,
      data: body,
    });

    const responseBody = await response.json() as T;
    return { response, body: responseBody };
  }
}
```

### src/api/clients/backoffice-api.client.ts

```typescript
import { APIRequestContext, APIResponse } from '@playwright/test';
import { ENV } from '../../config/environments';

export class BackOfficeApiClient {
  private request: APIRequestContext;
  private baseUrl: string;
  private userId: number;

  constructor(request: APIRequestContext) {
    this.request = request;
    this.baseUrl = ENV.backofficeUrl;
    this.userId = ENV.boUserId;
  }

  private get defaultHeaders() {
    return {
      'Content-Type': 'application/json',
      'UserId': this.userId.toString(),
    };
  }

  async getClientById(clientId: number): Promise<APIResponse> {
    return this.request.post(`${this.baseUrl}/api/Client/GetClientById`, {
      headers: this.defaultHeaders,
      data: clientId,
    });
  }

  async changeClientDetails(data: {
    id: number;
    isTest?: boolean;
    [key: string]: any;
  }): Promise<APIResponse> {
    return this.request.post(`${this.baseUrl}/api/Client/ChangeClientDetails`, {
      headers: this.defaultHeaders,
      data,
    });
  }

  async createDebitCorrection(data: {
    amount: number;
    clientId: number;
    currencyId: string;
    accountId: number;
    accountTypeId: number;
    info: string;
  }): Promise<APIResponse> {
    return this.request.post(`${this.baseUrl}/api/Client/CreateDebitCorrection`, {
      headers: this.defaultHeaders,
      data,
    });
  }

  async getBonuses(data: {
    partnerId: number;
    takeCount: number;
    skipCount?: number;
    isActive?: boolean;
  }): Promise<APIResponse> {
    return this.request.post(`${this.baseUrl}/api/Bonus/GetBonuses`, {
      headers: this.defaultHeaders,
      data,
    });
  }
}
```

---

## 🧪 Test Fixtures

### src/fixtures/api.fixture.ts

```typescript
import { test as base, APIRequestContext } from '@playwright/test';
import { WebsiteApiClient } from '../api/clients/website-api.client';
import { BackOfficeApiClient } from '../api/clients/backoffice-api.client';
import { GraphQLClient } from '../api/clients/graphql.client';

export const test = base.extend<{
  apiContext: APIRequestContext;
  websiteApi: WebsiteApiClient;
  backofficeApi: BackOfficeApiClient;
  graphql: GraphQLClient;
}>({
  apiContext: async ({ playwright }, use) => {
    const context = await playwright.request.newContext({
      baseURL: process.env.API_URL,
    });
    await use(context);
    await context.dispose();
  },

  websiteApi: async ({ apiContext }, use) => {
    await use(new WebsiteApiClient(apiContext));
  },

  backofficeApi: async ({ apiContext }, use) => {
    await use(new BackOfficeApiClient(apiContext));
  },

  graphql: async ({ apiContext }, use) => {
    await use(new GraphQLClient(apiContext));
  },
});

export { expect } from '@playwright/test';
```

### src/fixtures/player.fixture.ts

```typescript
import { test as base } from '@playwright/test';
import { GraphQLClient } from '../api/clients/graphql.client';
import { BackOfficeApiClient } from '../api/clients/backoffice-api.client';
import { generateTestEmail } from '../utils/helpers';

interface TestPlayer {
  id: number;
  email: string;
  password: string;
  username: string;
  token: string;
  accountId: number;
}

export const test = base.extend<{
  testPlayer: TestPlayer;
}>({
  testPlayer: async ({ graphql, backofficeApi }, use) => {
    // Create player
    const email = generateTestEmail();
    const password = 'Qweasd123!';
    
    const { player } = await graphql.registerPlayer({
      email,
      password,
      currency: 'USD',
      partnerId: 5,
    });

    // Set IsTest = true
    await backofficeApi.changeClientDetails({
      id: player.id,
      isTest: true,
    });

    // Get account ID
    const accounts = await backofficeApi.getClientAccounts(player.id);
    const accountId = accounts[0].Id;

    const testPlayer: TestPlayer = {
      id: player.id,
      email,
      password,
      username: player.username,
      token: player.token,
      accountId,
    };

    await use(testPlayer);

    // Cleanup (optional)
    // await backofficeApi.deactivateClient(player.id);
  },
});

export { expect } from '@playwright/test';
```

---

## 📝 Example Tests

### tests/api/bonus/eligible-bonuses.spec.ts

```typescript
import { test, expect } from '../../src/fixtures';

test.describe('Eligible Bonuses API', () => {
  test('should return eligible bonuses for new player', async ({ 
    testPlayer, 
    websiteApi 
  }) => {
    const { body } = await websiteApi.getBonus(
      'GetEligibleBonuses',
      testPlayer.token
    );

    expect(body.ResponseCode).toBe('Success');
    expect(Array.isArray(body.ResponseObject)).toBe(true);
    expect(body.ResponseObject.length).toBeGreaterThan(0);
  });

  test('should show only available bonuses', async ({ 
    testPlayer, 
    websiteApi 
  }) => {
    const { body } = await websiteApi.getBonus(
      'GetEligibleBonuses',
      testPlayer.token
    );

    const availableBonuses = body.ResponseObject.filter(
      (b: any) => b.IsAvailable === true
    );

    expect(availableBonuses.length).toBeGreaterThan(0);
  });
});
```

### tests/api/payment/deposit.spec.ts

```typescript
import { test, expect } from '../../src/fixtures';

test.describe('Deposit Operations', () => {
  test('should add balance via BackOffice', async ({ 
    testPlayer, 
    backofficeApi 
  }) => {
    // Add 10 USD
    const response = await backofficeApi.createDebitCorrection({
      amount: 10,
      clientId: testPlayer.id,
      currencyId: 'USD',
      accountId: testPlayer.accountId,
      accountTypeId: 1,
      info: 'Test deposit via automated test',
    });

    expect(response.ok()).toBe(true);

    // Verify balance
    const accounts = await backofficeApi.getClientAccounts(testPlayer.id);
    const balance = accounts[0].Balance;
    
    expect(balance).toBe(10);
  });
});
```

### tests/e2e/auth/login.flow.spec.ts

```typescript
import { test, expect } from '../../src/fixtures';
import { LoginPage } from '../../src/e2e/pages/login.page';
import { LobbyPage } from '../../src/e2e/pages/lobby.page';

test.describe('Login Flow', () => {
  test('should login successfully', async ({ page, testPlayer }) => {
    const loginPage = new LoginPage(page);
    const lobbyPage = new LobbyPage(page);

    await loginPage.goto();
    await loginPage.login(testPlayer.email, testPlayer.password);

    await expect(lobbyPage.welcomeMessage).toBeVisible();
    await expect(lobbyPage.balance).toContainText('10.00');
  });
});
```

---

## 🎭 Mocked Backend Tests

### src/mocks/handlers/bonus.handler.ts

```typescript
import { Route, Request } from '@playwright/test';

export async function handleGetEligibleBonuses(route: Route) {
  const request = route.request();
  
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      ResponseCode: 'Success',
      ResponseObject: [
        {
          Id: 100,
          IsAvailable: true,
          HasDepositTrigger: true,
          HasFreeSpins: false,
          HasWagering: true,
          CampaignFinishTime: '2030-01-01T00:00:00Z',
        },
      ],
    }),
  });
}

export async function setupBonusMocks(page: Page) {
  await page.route('**/api/v3/Bonus/GetEligibleBonuses', handleGetEligibleBonuses);
  await page.route('**/api/v3/Bonus/GetBonuses', handleGetEligibleBonuses);
}
```

### tests/mocked/ui-states.mocked.spec.ts

```typescript
import { test, expect } from '@playwright/test';
import { setupBonusMocks } from '../../src/mocks/handlers/bonus.handler';

test.describe('UI States (Mocked Backend)', () => {
  test.beforeEach(async ({ page }) => {
    await setupBonusMocks(page);
  });

  test('should display bonus card correctly', async ({ page }) => {
    await page.goto('/bonuses');
    
    const bonusCard = page.locator('[data-testid="bonus-card"]').first();
    await expect(bonusCard).toBeVisible();
    await expect(bonusCard.locator('.bonus-status')).toHaveText('Available');
  });
});
```

---

## 📱 Mobile Testing

### tests/mobile/login.mobile.spec.ts

```typescript
import { test, expect, devices } from '@playwright/test';
import { MobileLoginPage } from '../../src/mobile/pages/mobile-login.page';

test.use(devices['iPhone 14']);

test.describe('Mobile Login', () => {
  test('should show mobile-specific login UI', async ({ page, testPlayer }) => {
    const loginPage = new MobileLoginPage(page);
    
    await loginPage.goto();
    
    // Mobile-specific assertions
    await expect(loginPage.mobileMenuButton).toBeVisible();
    await expect(loginPage.fingerprintLogin).toBeVisible();
  });

  test('should handle touch events correctly', async ({ page }) => {
    const loginPage = new MobileLoginPage(page);
    
    await loginPage.goto();
    await loginPage.tapEmailField();
    await loginPage.typeEmail('test@example.com');
    
    await expect(loginPage.emailField).toHaveValue('test@example.com');
  });
});
```

---

## 🏆 Best Practices

### 1. **Test Data Management**
- Use factories for test data generation
- Clean up test data after tests
- Use fixtures for common setup/teardown

### 2. **API Testing**
- Test all API endpoints systematically
- Validate response schemas
- Test error handling and edge cases
- Use API tests for smoke tests (fast, reliable)

### 3. **E2E Testing**
- Use Page Object Model
- Focus on critical user flows
- Avoid testing every edge case in E2E
- Use API for setup, E2E for UI validation

### 4. **Mobile Testing**
- Use Playwright device emulators
- Test responsive breakpoints
- Test touch interactions
- Test orientation changes

### 5. **Mocked Backend**
- Test UI states that are hard to reproduce
- Test error handling UI
- Test loading states
- Test edge cases (empty states, max values)

### 6. **Test Parallelization**
- Run API tests in parallel (fast)
- Run E2E tests per browser
- Run mobile tests in parallel
- Use sharding for CI

### 7. **Reporting**
- Use HTML reporter for debugging
- Use JSON reporter for CI integration
- Attach screenshots/videos on failure
- Use trace viewer for debugging

---

## 📊 Test Distribution Recommendation

| Type | Percentage | Purpose |
|------|------------|---------|
| **API Tests** | 60% | Fast, reliable, comprehensive |
| **E2E Tests** | 25% | Critical user flows |
| **Mobile Tests** | 10% | Mobile-specific UI |
| **Mocked Tests** | 5% | Edge cases, error states |

---

## 🚀 Running Tests

```bash
# All tests
npx playwright test

# API tests only
npx playwright test --project=api

# E2E Chrome only
npx playwright test --project=e2e-chrome

# Mobile tests
npx playwright test --project=mobile-iphone

# Specific test file
npx playwright test tests/api/bonus/eligible-bonuses.spec.ts

# With specific environment
ENV=prod npx playwright test

# Debug mode
npx playwright test --debug

# UI mode
npx playwright test --ui
```

---

## 📋 Next Steps

1. **Setup project** - Initialize npm project with Playwright
2. **Create API clients** - Website + BackOffice + GraphQL
3. **Write API tests** - Start with auth and bonus endpoints
4. **Create Page Objects** - Login, Lobby, Bonus pages
5. **Write E2E tests** - Critical flows (login, deposit, bonus claim)
6. **Add mobile tests** - Key flows on mobile devices
7. **Add mocked tests** - Edge cases and error handling
8. **CI/CD integration** - GitHub Actions or similar

---

**Готовий почати імплементацію?** 🚀
