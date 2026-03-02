import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // Один worker, оскільки працюємо з розширеннями
  reporter: 'list',
  use: {
    headless: false, // Розширення не працюють у headless режимі
    actionTimeout: 10000,
    navigationTimeout: 30000,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'phantom',
      testMatch: /.*\.spec\.ts/,
    },
  ],
});