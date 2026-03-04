import { test, expect } from '../fixtures/phantom-fixture';

test.describe('Exploratory testing: Create Protocol feature', () => {
  test.beforeEach(async ({ context }) => {
    // Налаштування перед кожним тестом
    console.log('Starting exploratory testing of Create Protocol feature');
  });

  test('should navigate to community page and find Create Protocol button', async ({ context }) => {
    const page = await context.newPage();
    
    // Крок 1: Відкрити головну сторінку
    await page.goto('https://www.lorypten.com');
    await page.waitForLoadState('networkidle');
    
    // Перевірити, чи гаманець підключено
    const walletButton = page.locator('button.wallet-adapter-button');
    if (await walletButton.count() === 0) {
      console.log('Wallet button not found. Page may be in restricted state.');
      const html = await page.locator('body').innerHTML();
      console.log('Page content snippet:', html.substring(0, 2000));
      // Робимо скріншот для налагодження
      await page.screenshot({ path: 'exploratory-step1-home.png' });
      
      // Перевіримо, чи є повідомлення про обмежений доступ
      const restrictedMessage = page.locator('text=Access Restricted');
      if (await restrictedMessage.count() > 0) {
        console.log('Access Restricted page shown - wallet not authorized');
        // Можливо, потрібно підключити інший гаманець
        return;
      }
    } else {
      const walletText = await walletButton.first().textContent();
      console.log('Wallet button text:', walletText);
      await page.screenshot({ path: 'exploratory-step1-wallet-connected.png' });
    }
    
    // Крок 2: Перейти на сторінку Community Protocols
    // У HTML з повідомлення є посилання з класом text-[#14F195] та текстом Community Protocols
    const communityLink = page.locator('a:has-text("Community Protocols")');
    
    if (await communityLink.count() === 0) {
      // Спробуємо знайти будь-яке посилання на /community
      const allLinks = await page.locator('a').all();
      for (const link of allLinks) {
        const href = await link.getAttribute('href');
        if (href && href.includes('community')) {
          console.log('Found community link with href:', href);
          await link.click();
          await page.waitForLoadState('networkidle');
          break;
        }
      }
    } else {
      await communityLink.click();
      await page.waitForLoadState('networkidle');
    }
    
    // Перевіримо URL
    const currentUrl = page.url();
    console.log('Current URL after navigation:', currentUrl);
    expect(currentUrl).toContain('/community');
    await page.screenshot({ path: 'exploratory-step2-community.png' });
    
    // Крок 3: Знайти кнопку Create Protocol
    // У HTML з повідомлення є кнопка з текстом "Create Protocol"
    const createProtocolButton = page.locator('button:has-text("Create Protocol"), a:has-text("Create Protocol")');
    
    if (await createProtocolButton.count() === 0) {
      console.log('Create Protocol button not found on community page');
      // Виведемо всі кнопки для налагодження
      const allButtons = await page.locator('button').all();
      for (const btn of allButtons) {
        const text = await btn.textContent();
        console.log('Button text:', text);
      }
      await page.screenshot({ path: 'exploratory-step2-no-button.png' });
    } else {
      console.log('Found Create Protocol button');
      await createProtocolButton.click();
      await page.waitForLoadState('networkidle');
      
      // Перевіримо, чи перейшли на сторінку створення протоколу
      const createUrl = page.url();
      console.log('URL after clicking Create Protocol:', createUrl);
      expect(createUrl).toContain('/createProtocol');
      
      await page.screenshot({ path: 'exploratory-step3-create-page.png' });
      
      // Крок 4: Перевірити форму
      const formTitle = page.locator('h1:has-text("Create New Lorypten Protocol")');
      expect(await formTitle.count()).toBeGreaterThan(0);
      
      // Виведемо структуру форми для налагодження
      const formElements = await page.locator('form input, form select, form textarea').all();
      console.log('Form elements found:', formElements.length);
      
      // Робимо детальний скріншот форми
      await page.screenshot({ path: 'exploratory-step4-form.png', fullPage: true });
    }
  });

  test('should fill create protocol form with valid data', async ({ context }) => {
    const page = await context.newPage();
    
    // Переходимо прямо на сторінку створення протоколу
    await page.goto('https://www.lorypten.com/createProtocol');
    await page.waitForLoadState('networkidle');
    
    // Перевіримо, чи ми на сторінці створення
    const formTitle = page.locator('h1:has-text("Create New Lorypten Protocol")');
    if (await formTitle.count() === 0) {
      console.log('Not on create protocol page. Current page:');
      await page.screenshot({ path: 'exploratory-not-on-create-page.png' });
      return;
    }
    
    // Заповнимо форму згідно з документацією
    // Примітка: це exploratory testing, тому ми використовуємо тестові дані
    
    // 1. Entry Fee (в SOL)
    const entryFeeInput = page.locator('input[name*="entryFee"], input[placeholder*="Entry Fee"]').first();
    if (await entryFeeInput.count() > 0) {
      await entryFeeInput.fill('0.1');
    }
    
    // 2. Payout Duration (випадаючий список)
    // Можливі значення: MIN_1, HOUR_1, DAY_1, WEEK_1, MONTH_1, MONTH_3, MONTH_6, YEAR_1, YEAR_5
    const durationSelect = page.locator('select').first();
    if (await durationSelect.count() > 0) {
      await durationSelect.selectOption({ value: 'DAY_1' }); // 1 день
    }
    
    // 3. Field Size (3×3 або 9×9)
    // Можуть бути радіо-кнопки або випадаючий список
    const fieldSize3x3 = page.locator('input[value*="3x3"], input[name*="fieldSize"][value*="3"]').first();
    if (await fieldSize3x3.count() > 0) {
      await fieldSize3x3.click();
    }
    
    // 4. Pool Distribution Percentages
    // Потрібно заповнити 4 поля: points, best_field, token_holder, jackpot
    // Сума має бути 100%
    const pointsInput = page.locator('input[name*="points"], input[placeholder*="points"]').first();
    if (await pointsInput.count() > 0) {
      await pointsInput.fill('40');
    }
    
    const bestFieldInput = page.locator('input[name*="best_field"], input[placeholder*="best field"]').first();
    if (await bestFieldInput.count() > 0) {
      await bestFieldInput.fill('30');
    }
    
    const tokenHolderInput = page.locator('input[name*="token_holder"], input[placeholder*="token holder"]').first();
    if (await tokenHolderInput.count() > 0) {
      await tokenHolderInput.fill('20');
    }
    
    const jackpotInput = page.locator('input[name*="jackpot"], input[placeholder*="jackpot"]').first();
    if (await jackpotInput.count() > 0) {
      await jackpotInput.fill('10');
    }
    
    // 5. Buyout (опціонально)
    // Можливо, checkbox для включення buyout
    const buyoutCheckbox = page.locator('input[type="checkbox"][name*="buyout"]').first();
    if (await buyoutCheckbox.count() > 0) {
      await buyoutCheckbox.click();
      
      // Якщо buyout увімкнено, заповнити ціну
      const buyoutPriceInput = page.locator('input[name*="buyoutPrice"]').first();
      if (await buyoutPriceInput.count() > 0) {
        await buyoutPriceInput.fill('10'); // 10 SOL
      }
    }
    
    // 6. Завантаження зображення
    // Playwright може завантажувати файли через input[type="file"]
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0) {
      // Створюємо тестовий файл або використовуємо існуючий
      const testImagePath = 'test-image.jpg';
      await fileInput.setInputFiles(testImagePath);
      console.log('File uploaded (or attempted)');
    }
    
    // 7. Max Participants / Max Epochs (опціонально)
    const maxParticipantsInput = page.locator('input[name*="maxParticipants"]').first();
    if (await maxParticipantsInput.count() > 0) {
      await maxParticipantsInput.fill('100');
    }
    
    // 8. Airdrop configuration (4 optional pools)
    // Можливо, додаткові поля
    
    // Робимо скріншот заповненої форми
    await page.screenshot({ path: 'exploratory-filled-form.png', fullPage: true });
    
    // 9. Перевіримо валідацію перед відправкою
    const submitButton = page.locator('button[type="submit"]:has-text("Create"), button:has-text("Create Protocol")');
    if (await submitButton.count() > 0) {
      const isDisabled = await submitButton.isDisabled();
      console.log('Submit button disabled?', isDisabled);
      
      if (!isDisabled) {
        console.log('Form appears to be valid. Ready to submit.');
        // У реальному тесті ми могли б натиснути, але для exploratory
        // можливо, краще не відправляти без дозволу
        // await submitButton.click();
      } else {
        console.log('Form has validation errors');
        // Пошукаємо повідомлення про помилки
        const errorMessages = page.locator('.text-red-500, .error-message');
        const errorCount = await errorMessages.count();
        console.log('Validation errors found:', errorCount);
        for (let i = 0; i < errorCount; i++) {
          const errorText = await errorMessages.nth(i).textContent();
          console.log(`Error ${i+1}:`, errorText);
        }
      }
    }
    
    // Виведемо HTML форми для налагодження
    const formHtml = await page.locator('form').first().innerHTML();
    console.log('Form HTML snippet:', formHtml.substring(0, 3000));
  });
});