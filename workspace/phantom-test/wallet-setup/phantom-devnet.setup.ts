import { BrowserContext, Page } from '@playwright/test';
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.join(__dirname, '..', '.env') });

/**
 * Перевіряє, чи гаманець вже налаштований у Phantom.
 * Якщо ні — намагається налаштувати (але може зазнати невдачі через закриття сторінки).
 */
export async function setupPhantomWallet(context: BrowserContext, extensionId: string): Promise<boolean> {
  const page = await context.newPage();
  
  // Спробуємо відкрити popup сторінку (якщо гаманець налаштований, вона покаже баланс)
  const popupUrl = `chrome-extension://${extensionId}/popup.html`;
  await page.goto(popupUrl);
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);
  
  // Робимо скріншот для налагодження
  await page.screenshot({ path: 'phantom-popup-initial.png' });
  
  // Перевіряємо, чи є ознаки налаштованого гаманця:
  // - кнопка "Receive" або "Send"
  // - адреса гаманця
  // - баланс
  
  const receiveButton = page.locator('button:has-text("Receive"), button:has-text("Deposit")');
  const sendButton = page.locator('button:has-text("Send"), button:has-text("Withdraw")');
  const walletAddress = page.locator('text=/[1-9A-HJ-NP-Za-km-z]{32,44}/');
  
  if (await receiveButton.count() > 0 || await sendButton.count() > 0 || await walletAddress.count() > 0) {
    console.log('✅ Phantom wallet already configured!');
    
    // Тепер перемикаємо на Devnet через налаштування
    await switchToDevnet(page);
    await page.close();
    return true;
  }
  
  // Якщо гаманець не налаштований, відкриваємо onboarding
  console.log('⚠️ Phantom wallet not configured. Attempting onboarding...');
  
  const onboardingUrl = `chrome-extension://${extensionId}/onboarding.html`;
  await page.goto(onboardingUrl);
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
  
  await page.screenshot({ path: 'phantom-onboarding.png' });
  
  // Клікаємо "I already have a wallet"
  const importButton = page.locator('button:has-text("I already have a wallet"), button:has-text("Import")').first();
  if (await importButton.count() > 0) {
    await importButton.click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'phantom-import-step.png' });
    
    // Далі потрібно ввести seed-фразу
    // Спробуємо знайти textarea для введення всієї фрази
    const seedPhrase = process.env.TEST_WALLET_SEED;
    if (!seedPhrase) {
      throw new Error('TEST_WALLET_SEED не знайдено у .env');
    }
    
    const seedTextarea = page.locator('textarea').first();
    if (await seedTextarea.count() > 0) {
      await seedTextarea.fill(seedPhrase);
      await page.waitForTimeout(500);
      await page.screenshot({ path: 'phantom-seed-entered.png' });
      
      // Шукаємо кнопку "Continue" або "Import"
      const continueBtn = page.locator('button:has-text("Continue"), button:has-text("Import"), button:has-text("Next")').first();
      if (await continueBtn.count() > 0) {
        await continueBtn.click();
        await page.waitForTimeout(2000);
        
        // Може з'явитися поле для пароля
        const passwordInput = page.locator('input[type="password"]').first();
        if (await passwordInput.count() > 0) {
          const password = process.env.TEST_WALLET_PASSWORD;
          if (!password) {
            throw new Error('TEST_WALLET_PASSWORD не знайдено у .env');
          }
          await passwordInput.fill(password);
          
          const confirmPassword = page.locator('input[type="password"]').nth(1);
          if (await confirmPassword.count() > 0) {
            await confirmPassword.fill(password);
          }
          
          const createBtn = page.locator('button:has-text("Create"), button:has-text("Continue"), button:has-text("Next")').first();
          if (await createBtn.count() > 0) {
            await createBtn.click();
            await page.waitForTimeout(2000);
          }
        }
      }
    }
  }
  
  // Спробуємо знову відкрити popup
  await page.goto(popupUrl);
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
  
  // Перемикаємо на Devnet
  await switchToDevnet(page);
  
  await page.close();
  return true;
}

/**
 * Перемикає Phantom на Devnet
 */
async function switchToDevnet(page: Page): Promise<void> {
  // Шукаємо кнопку налаштувань
  const settingsButton = page.locator('button[aria-label="Settings"], button:has-text("Settings"), [data-testid="settings-button"], button:has(img)').first();
  
  // Спробуємо знайти будь-яку кнопку з іконкою шестірні
  const allButtons = await page.locator('button').all();
  for (const btn of allButtons) {
    const innerHtml = await btn.innerHTML();
    if (innerHtml.includes('svg') && (innerHtml.includes('settings') || innerHtml.includes('gear') || innerHtml.includes('cog'))) {
      await btn.click();
      await page.waitForTimeout(500);
      break;
    }
  }
  
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'phantom-settings.png' });
  
  // Шукаємо "Developer Settings" або "Testnet"
  const developerBtn = page.locator('button:has-text("Developer"), button:has-text("Testnet"), button:has-text("Devnet")').first();
  if (await developerBtn.count() > 0) {
    await developerBtn.click();
    await page.waitForTimeout(500);
    
    // Вмикаємо Testnet mode
    const testnetToggle = page.locator('button:has-text("Testnet"), button:has-text("Devnet"), [role="switch"]').first();
    if (await testnetToggle.count() > 0) {
      await testnetToggle.click();
      await page.waitForTimeout(1000);
      console.log('✅ Switched to Devnet');
    }
  }
}