import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function checkDepositStreakUI() {
  console.log('🚀 Starting Deposit Streak UI Check...');

  const browser = await chromium.launch({
    headless: false,
    args: ['--start-maximized']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    locale: 'en-US'
  });

  const page = await context.newPage();

  const email = 'demo1772643519424@nextcode.tech';
  const password = 'Qweasd123!';
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const screenshotDir = path.join(__dirname, '..', 'screenshots', 'deposit-streak-check');

  console.log(`📸 Screenshots will be saved to: ${screenshotDir}`);

  // Navigate to Minebit PROD
  console.log('🌐 Navigating to Minebit PROD...');
  await page.goto('https://minebit-casino.prod.sofon.one', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(screenshotDir, `01-home-${timestamp}.png`), fullPage: true });
  console.log('✅ Screenshot: Homepage saved');

  // Find and click login button
  console.log('🔍 Looking for login button...');
  try {
    // Try multiple possible login button selectors
    const loginSelectors = [
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'a[href*="login"]',
      '[data-testid*="login"]',
      '.login-button',
      '.btn-login'
    ];

    let loginButton = null;
    for (const selector of loginSelectors) {
      try {
        loginButton = await page.waitForSelector(selector, { timeout: 2000 });
        if (loginButton) {
          console.log(`✅ Found login button with selector: ${selector}`);
          await loginButton.click();
          break;
        }
      } catch (e) {
        continue;
      }
    }

    if (!loginButton) {
      console.log('⚠️ Could not find login button with standard selectors');
      console.log('🔍 Page title:', await page.title());
      throw new Error('Login button not found');
    }

    await page.waitForLoadState('networkidle');
    console.log('✅ Login button clicked');

  } catch (e) {
    console.log('❌ Error clicking login button:', e.message);
    await page.screenshot({ path: path.join(screenshotDir, `error-login-${timestamp}.png`), fullPage: true });
    await browser.close();
    return;
  }

  // Fill login form
  console.log('📝 Filling login form...');
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
    await page.screenshot({ path: path.join(screenshotDir, `error-form-${timestamp}.png`), fullPage: true });
    await browser.close();
    return;
  }

  // Wait for login to complete
  console.log('⏳ Waiting for login to complete...');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000);

  // Screenshot after login
  await page.screenshot({ path: path.join(screenshotDir, `02-logged-in-${timestamp}.png`), fullPage: true });
  console.log('📸 Screenshot: Logged in (full page)');

  // Navigate to bonuses page
  console.log('🎁 Navigating to bonuses page...');
  try {
    await page.goto('https://minebit-casino.prod.sofon.one/bonuses', { waitUntil: 'networkidle' });
    console.log('✅ Navigated to bonuses page');
  } catch (e) {
    console.log('⚠️ Could not navigate to bonuses page:', e.message);
  }

  // Wait for bonuses to load
  await page.waitForTimeout(2000);

  // Screenshot bonuses page
  await page.screenshot({ path: path.join(screenshotDir, `03-bonuses-${timestamp}.png`), fullPage: true });
  console.log('📸 Screenshot: Bonuses page (full page)');

  // Check for Deposit Streak bonus
  console.log('\n🔍 Checking for Deposit Streak bonus...');
  try {
    const depositStreakExists = await page.locator(':has-text("Deposit Streak")').count() > 0 ||
                                await page.locator(':has-text("deposit streak")').count() > 0 ||
                                await page.locator(':has-text("Streak")').count() > 0;

    if (depositStreakExists) {
      console.log('✅ DEPOSIT STREAK BONUS FOUND!');

      const streakElement = page.locator(':has-text("Streak")').first();
      await streakElement.screenshot({ path: path.join(screenshotDir, `04-deposit-streak-card-${timestamp}.png`) });
      console.log('📸 Screenshot: Deposit Streak bonus element saved');
    } else {
      console.log('❌ DEPOSIT STREAK BONUS NOT FOUND');
    }
  } catch (e) {
    console.log('⚠️ Error checking for Deposit Streak:', e.message);
  }

  // Check for any active bonuses
  console.log('\n🔍 Checking for active bonuses...');
  try {
    const claimButtons = await page.locator('button:has-text("Claim")').count();
    console.log(`🎁 Found ${claimButtons} "Claim" buttons`);

    const activeTexts = await page.locator(':has-text("Active"), :has-text("Available")').count();
    console.log(`🎁 Found ${activeTexts} elements with "Active" or "Available" text`);

    // Count all bonus cards
    const bonusCards = await page.locator('[class*="bonus"], [data-testid*="bonus"], .bonus-card').count();
    console.log(`🎁 Total bonus-related elements: ${bonusCards}`);

  } catch (e) {
    console.log('⚠️ Error checking for bonuses:', e.message);
  }

  // Output summary
  console.log('\n📊 SUMMARY:');
  console.log('   - Screenshots saved to:', screenshotDir);
  console.log('   - Test user:', email);
  console.log('   - Client ID: 1181008');
  console.log('   - Deposits made: 10 × $30 USD = $300');

  // Keep browser open for manual inspection
  console.log('\n⏸️ Browser will stay open for 60 seconds for manual inspection...');
  await page.waitForTimeout(60000);

  await browser.close();
  console.log('\n✅ Done! Browser closed.');
}

checkDepositStreakUI().catch(console.error);
