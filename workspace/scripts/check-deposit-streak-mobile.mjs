import { chromium, devices } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function checkDepositStreakMobile() {
  console.log('🚀 Starting Deposit Streak UI Check (Mobile - iPhone 14)...');

  const browser = await chromium.launch({
    headless: false,
    args: ['--start-maximized']
  });

  // Use iPhone 14 device emulation
  const context = await browser.newContext({
    ...devices['iPhone 14'],
    locale: 'en-US'
  });

  const page = await context.newPage();

  const email = 'demo1772643519424@nextcode.tech';
  const password = 'Qweasd123!';
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const screenshotDir = path.join(__dirname, '..', 'screenshots', 'deposit-streak-mobile');

  console.log(`📸 Screenshots will be saved to: ${screenshotDir}`);
  console.log(`📱 Device: iPhone 14 (Mobile)`);

  // Navigate to Minebit PROD
  console.log('🌐 Navigating to Minebit PROD...');
  await page.goto('https://minebit-casino.prod.sofon.one', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(screenshotDir, `01-home-mobile-${timestamp}.png`), fullPage: true });
  console.log('✅ Screenshot: Homepage (mobile) saved');

  // Find and click login button (mobile version)
  console.log('🔍 Looking for login button (mobile)...');
  try {
    // Try multiple possible login button selectors (mobile may use hamburger menu)
    const loginSelectors = [
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'a[href*="login"]',
      '[data-testid*="login"]',
      // Mobile menu button
      'button[aria-label*="menu"]',
      'button:has-text("Menu")',
      '.menu-button',
      '.hamburger'
    ];

    let loginButton = null;
    for (const selector of loginSelectors) {
      try {
        loginButton = await page.waitForSelector(selector, { timeout: 2000 });
        if (loginButton) {
          console.log(`✅ Found login/menu button with selector: ${selector}`);
          await loginButton.click();

          // Wait a bit for menu to open if it's a hamburger
          await page.waitForTimeout(1000);

          // Try to find login button in menu if this was a hamburger
          try {
            const loginInMenu = await page.waitForSelector('a:has-text("Log in"), button:has-text("Log in"), a:has-text("Login"), button:has-text("Login")', { timeout: 2000 });
            if (loginInMenu) {
              console.log('✅ Found login in menu');
              await loginInMenu.click();
            }
          } catch (e) {
            // This was already a direct login button, not hamburger
            console.log('✅ Direct login button clicked');
          }
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!loginButton) {
      console.log('⚠️ Could not find login button with standard selectors');
      throw new Error('Login button not found');
    }

    await page.waitForLoadState('networkidle');
    console.log('✅ Login button clicked');

  } catch (e) {
    console.log('❌ Error clicking login button:', e.message);
    await page.screenshot({ path: path.join(screenshotDir, `error-login-mobile-${timestamp}.png`), fullPage: true });
    await browser.close();
    return;
  }

  // Fill login form (mobile)
  console.log('📝 Filling login form (mobile)...');
  try {
    // Find email input
    const emailSelectors = [
      'input[type="email"]',
      'input[name*="email"]',
      'input[placeholder*="email" i]',
      'input[placeholder*="Email" i]'
    ];

    let emailInput = null;
    for (const selector of emailSelectors) {
      try {
        emailInput = await page.waitForSelector(selector, { timeout: 2000 });
        if (emailInput) {
          console.log(`✅ Found email input with selector: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!emailInput) {
      throw new Error('Email input not found');
    }

    await emailInput.fill(email);
    console.log(`✅ Email filled: ${email}`);

    // Find password input
    const passwordSelectors = [
      'input[type="password"]',
      'input[name*="password"]',
      'input[placeholder*="password" i]',
      'input[placeholder*="Password" i]'
    ];

    let passwordInput = null;
    for (const selector of passwordSelectors) {
      try {
        passwordInput = await page.waitForSelector(selector, { timeout: 2000 });
        if (passwordInput) {
          console.log(`✅ Found password input with selector: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!passwordInput) {
      throw new Error('Password input not found');
    }

    await passwordInput.fill(password);
    console.log('✅ Password filled');

    // Find and click submit button
    const submitSelectors = [
      'button[type="submit"]',
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'button:has-text("Sign in")',
      '[type="submit"]'
    ];

    let submitButton = null;
    for (const selector of submitSelectors) {
      try {
        submitButton = await page.waitForSelector(selector, { timeout: 2000 });
        if (submitButton) {
          console.log(`✅ Found submit button with selector: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!submitButton) {
      throw new Error('Submit button not found');
    }

    await submitButton.click();
    console.log('✅ Login form submitted');

  } catch (e) {
    console.log('❌ Error filling login form:', e.message);
    await page.screenshot({ path: path.join(screenshotDir, `error-form-mobile-${timestamp}.png`), fullPage: true });
    await browser.close();
    return;
  }

  // Wait for login to complete
  console.log('⏳ Waiting for login to complete...');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000);

  // Screenshot after login (mobile)
  await page.screenshot({ path: path.join(screenshotDir, `02-logged-in-mobile-${timestamp}.png`), fullPage: true });
  console.log('📸 Screenshot: Logged in (mobile, full page)');

  // Navigate to bonuses page (mobile - may use bottom navigation)
  console.log('🎁 Navigating to bonuses page (mobile)...');
  try {
    // Try to find bonuses link/button in mobile navigation
    const bonusesSelectors = [
      'a:has-text("Bonus")',
      'a:has-text("Bonuses")',
      'nav a[href*="bonus"]',
      // Bottom navigation
      'nav:has-text("Bonuses")',
      // Mobile bottom bar
      '[role="navigation"] a:has-text("Bonuses")'
    ];

    for (const selector of bonusesSelectors) {
      try {
        const bonusesLink = await page.waitForSelector(selector, { timeout: 2000 });
        if (bonusesLink) {
          console.log(`✅ Found bonuses link with selector: ${selector}`);
          await bonusesLink.click();
          break;
        }
      } catch (e) {
        continue;
      }
    }

    await page.waitForLoadState('networkidle');
    console.log('✅ Navigated to bonuses page');

  } catch (e) {
    console.log('⚠️ Could not find bonuses link via mobile nav, trying direct URL:', e.message);
    await page.goto('https://minebit-casino.prod.sofon.one/bonuses', { waitUntil: 'networkidle' });
  }

  // Wait for bonuses to load
  await page.waitForTimeout(2000);

  // Screenshot bonuses page (mobile)
  await page.screenshot({ path: path.join(screenshotDir, `03-bonuses-mobile-${timestamp}.png`), fullPage: true });
  console.log('📸 Screenshot: Bonuses page (mobile, full page)');

  // Check for Deposit Streak bonus (mobile)
  console.log('\n🔍 Checking for Deposit Streak bonus (mobile)...');
  try {
    const depositStreakExists = await page.locator(':has-text("Deposit Streak")').count() > 0 ||
                                await page.locator(':has-text("deposit streak")').count() > 0 ||
                                await page.locator(':has-text("Streak")').count() > 0;

    if (depositStreakExists) {
      console.log('✅ DEPOSIT STREAK BONUS FOUND (MOBILE)!');

      const streakElement = page.locator(':has-text("Streak")').first();
      await streakElement.screenshot({ path: path.join(screenshotDir, `04-deposit-streak-card-mobile-${timestamp}.png`) });
      console.log('📸 Screenshot: Deposit Streak bonus element (mobile) saved');
    } else {
      console.log('❌ DEPOSIT STREAK BONUS NOT FOUND (MOBILE)');
    }
  } catch (e) {
    console.log('⚠️ Error checking for Deposit Streak (mobile):', e.message);
  }

  // Check for any active bonuses (mobile)
  console.log('\n🔍 Checking for active bonuses (mobile)...');
  try {
    const claimButtons = await page.locator('button:has-text("Claim")').count();
    console.log(`🎁 Found ${claimButtons} "Claim" buttons`);

    const activeTexts = await page.locator(':has-text("Active"), :has-text("Available")').count();
    console.log(`🎁 Found ${activeTexts} elements with "Active" or "Available" text`);

    // Count all bonus cards
    const bonusCards = await page.locator('[class*="bonus"], [data-testid*="bonus"], .bonus-card').count();
    console.log(`🎁 Total bonus-related elements: ${bonusCards}`);

  } catch (e) {
    console.log('⚠️ Error checking for bonuses (mobile):', e.message);
  }

  // Output summary
  console.log('\n📊 SUMMARY (MOBILE):');
  console.log('   - Screenshots saved to:', screenshotDir);
  console.log('   - Device: iPhone 14 (Mobile)');
  console.log('   - Test user:', email);
  console.log('   - Client ID: 1181008');
  console.log('   - Deposits made: 10 × $30 USD = $300');

  // Keep browser open for manual inspection
  console.log('\n⏸️ Browser will stay open for 60 seconds for manual inspection...');
  await page.waitForTimeout(60000);

  await browser.close();
  console.log('\n✅ Done! Browser closed.');
}

checkDepositStreakMobile().catch(console.error);
