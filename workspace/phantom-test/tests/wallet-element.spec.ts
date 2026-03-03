import { test, expect } from '../fixtures/phantom-fixture';

test.describe('Wallet connection element verification', () => {
  test('should display navigation element after wallet connection', async ({ context }) => {
    const page = await context.newPage();
    
    // Відкриваємо Lorypten
    await page.goto('https://www.lorypten.com');
    await page.waitForLoadState('networkidle');
    
    // Перевіряємо, чи є елемент, який показав користувач
    // Шукаємо div з класом bg-[#131726] та текстом LoryptenProtocols
    const navElement = page.locator('div.bg-\\[\\#131726\\]');
    
    // Якщо не знайдено за класом, шукаємо за текстом
    const loryptenText = page.locator('text=LoryptenProtocols');
    
    let foundElement = null;
    if (await navElement.count() > 0) {
      foundElement = navElement.first();
    } else if (await loryptenText.count() > 0) {
      foundElement = loryptenText.first();
    }
    
    // Очікуємо, що хоча б один елемент буде присутній
    expect(foundElement).not.toBeNull();
    
    // Отримуємо HTML елемента
    const elementHTML = await foundElement?.innerHTML();
    console.log('Found element HTML:', elementHTML);
    
    // Перевіряємо наявність кнопки гаманця
    const walletButton = page.locator('button.wallet-adapter-button');
    expect(await walletButton.count()).toBeGreaterThan(0);
    
    // Перевіряємо, що адреса гаманця відображається (скорочена)
    const walletAddress = page.locator('button.wallet-adapter-button >> text=/[A-Za-z0-9]{4}\\.\\.[A-Za-z0-9]{4}/');
    expect(await walletAddress.count()).toBeGreaterThan(0);
    
    const addressText = await walletAddress.first().textContent();
    console.log('Wallet address displayed:', addressText);
    
    // Робимо скріншот
    await page.screenshot({ path: 'wallet-element-check.png' });
  });
});