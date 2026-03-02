import { test, expect } from '../fixtures/phantom-fixture';
import { setupPhantomWallet } from '../wallet-setup/phantom-devnet.setup';

test.describe('Phantom Wallet Connection to Lorypten', () => {
  test.beforeEach(async ({ context, extensionId }) => {
    // Налаштовуємо гаманець перед кожним тестом (якщо потрібно)
    console.log('Setting up Phantom wallet...');
    try {
      await setupPhantomWallet(context, extensionId);
    } catch (error) {
      console.log('Wallet setup error (may already be configured):', error);
    }
  });

  test('should connect Phantom wallet to Lorypten', async ({ context, extensionId }) => {
    const page = await context.newPage();
    
    // Відкриваємо Lorypten
    await page.goto('https://www.lorypten.com');
    await page.waitForLoadState('networkidle');
    
    // Робимо скріншот початкового стану
    await page.screenshot({ path: 'lorypten-initial.png' });
    
    // Перевіряємо, чи є кнопка "Select Wallet" або "Disconnect Wallet"
    const selectWalletButton = page.locator('button:has-text("Select Wallet")');
    const disconnectButton = page.locator('button:has-text("Disconnect Wallet")');
    
    // Якщо вже є "Disconnect Wallet" — гаманець уже підключено
    if (await disconnectButton.count() > 0) {
      console.log('Wallet already connected!');
      await page.screenshot({ path: 'lorypten-already-connected.png' });
      return;
    }
    
    // Перевіряємо кнопку "Select Wallet"
    await expect(selectWalletButton).toBeVisible({ timeout: 10000 });
    
    // Клікаємо "Select Wallet"
    await selectWalletButton.click();
    
    // Чекаємо модальне вікно з вибором гаманця
    await page.waitForTimeout(1500);
    
    // Робимо скріншот модального вікна
    await page.screenshot({ path: 'lorypten-wallet-modal.png' });
    
    // Шукаємо кнопку Phantom у модальному вікні
    // Можливі селектори: кнопка з текстом "Phantom", img з alt="Phantom", div з class="phantom"
    const phantomOption = page.locator('button:has-text("Phantom"), button:has(img[alt*="Phantom"]), [data-testid="phantom-wallet-option"]').first();
    
    if (await phantomOption.count() === 0) {
      // Виводимо HTML для налагодження
      const modalHtml = await page.locator('body').innerHTML();
      console.log('Modal HTML snippet:', modalHtml.substring(0, 2000));
      throw new Error('Phantom wallet option not found in modal');
    }
    
    // Клікаємо на Phantom
    await phantomOption.click();
    
    // Чекаємо появи popup від Phantom для підтвердження підключення
    console.log('Waiting for Phantom popup...');
    const popupPromise = context.waitForEvent('page', { timeout: 15000 });
    const popup = await popupPromise;
    await popup.waitForLoadState('domcontentloaded');
    
    // Робимо скріншот popup
    await popup.screenshot({ path: 'phantom-popup.png' });
    
    // У popup шукаємо кнопку підтвердження (Connect / Approve)
    const connectButton = popup.locator('button:has-text("Connect"), button:has-text("Approve"), button:has-text("Confirm")').first();
    
    if (await connectButton.count() > 0) {
      await connectButton.click();
      console.log('Clicked Connect in Phantom popup');
    } else {
      // Можливо, потрібно прокрутити або шукати інший елемент
      console.log('Connect button not found. Popup HTML:', await popup.locator('body').innerHTML().then(h => h.substring(0, 1000)));
    }
    
    // Чекаємо, поки popup закриється
    try {
      await popup.waitForEvent('close', { timeout: 10000 });
      console.log('Phantom popup closed');
    } catch (e) {
      console.log('Popup did not close, may need manual interaction');
    }
    
    // Перевіряємо, що гаманець підключено на сторінці Lorypten
    // Чекаємо трохи для оновлення UI
    await page.waitForTimeout(2000);
    
    // Знову перевіряємо кнопку
    const disconnectButtonAfter = page.locator('button:has-text("Disconnect Wallet")');
    const walletAddress = page.locator('text=/[A-Za-z0-9]{4,10}\.\.\.[A-Za-z0-9]{4,10}/');
    
    // Робимо фінальний скріншот
    await page.screenshot({ path: 'lorypten-final-state.png' });
    
    // Перевіряємо успішне підключення
    if (await disconnectButtonAfter.count() > 0) {
      console.log('✅ Wallet successfully connected! Disconnect button visible.');
    } else if (await walletAddress.count() > 0) {
      console.log('✅ Wallet address visible:', await walletAddress.first().textContent());
    } else {
      console.log('⚠️ Could not confirm wallet connection');
    }
    
    expect(await disconnectButtonAfter.count() > 0 || await walletAddress.count() > 0).toBeTruthy();
  });
});