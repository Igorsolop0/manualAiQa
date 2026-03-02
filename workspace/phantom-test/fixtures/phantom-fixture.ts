import { test as base, chromium, BrowserContext } from '@playwright/test';
import path from 'path';
import * as dotenv from 'dotenv';
import * as fs from 'fs';

dotenv.config({ path: path.join(__dirname, '..', '.env') });

// Шлях до розширення Phantom
const PHANTOM_EXTENSION_PATH = '/Users/ihorsolopii/Library/Application Support/Google/Chrome/Profile 1/Extensions/bfnaelmomeimhlpmgjnjophhpkkoljpa/26.7.0_0';

// Директорія для даних браузера (persistent context)
const USER_DATA_DIR = path.join(__dirname, '..', '.browser-data');

export const test = base.extend<{
  context: BrowserContext;
  extensionId: string;
}>({
  context: async ({ }, use) => {
    // Створюємо директорію для даних, якщо не існує
    if (!fs.existsSync(USER_DATA_DIR)) {
      fs.mkdirSync(USER_DATA_DIR, { recursive: true });
    }
    
    // Запускаємо persistent context з розширенням Phantom
    const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
      headless: false, // Розширення не працюють у headless режимі
      args: [
        `--disable-extensions-except=${PHANTOM_EXTENSION_PATH}`,
        `--load-extension=${PHANTOM_EXTENSION_PATH}`,
        '--no-sandbox',
      ],
    });
    await use(context);
    await context.close();
  },

  extensionId: async ({ context }, use) => {
    // ID розширення — це папка (bfnaelmomeimhlpmgjnjophhpkkoljpa)
    const extensionId = 'bfnaelmomeimhlpmgjnjophhpkkoljpa';
    await use(extensionId);
  },
});

export const { expect } = test;