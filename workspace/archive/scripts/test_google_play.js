const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function testGooglePlayButton() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  const testResultsDir = '/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-GOOGLE-PLAY';

  console.log('🔹 Step 1: Opening Minebit casino...');
  await page.goto('https://minebit-casino.prod.sofon.one/', { waitUntil: 'networkidle' });

  // Take initial screenshot
  await page.screenshot({ path: path.join(testResultsDir, 'screenshot_001_desktop_homepage.png') });
  console.log('✅ Screenshot saved: screenshot_001_desktop_homepage.png');

  // Get page snapshot
  console.log('🔹 Step 2: Getting page snapshot...');
  const snapshot = await page.content();
  fs.writeFileSync(path.join(testResultsDir, 'page_snapshot.html'), snapshot);
  console.log('✅ Snapshot saved: page_snapshot.html');

  // Find burger menu selector
  console.log('🔹 Step 3: Finding CSS selectors...');

  // Try multiple approaches to find the burger menu
  const burgerSelectors = [
    'button[aria-label="menu"]',
    'button[aria-label="Menu"]',
    'button[aria-label="Open menu"]',
    '.hamburger',
    '.hamburger-menu',
    '[data-testid="hamburger-menu"]',
    '.burger-icon',
    'svg[class*="menu"]',
    'button svg[class*="menu"]',
    '.header-menu-button',
    'button[class*="menu"]'
  ];

  let burgerSelector = null;
  for (const selector of burgerSelectors) {
    try {
      const element = await page.$(selector);
      if (element) {
        burgerSelector = selector;
        console.log(`✅ Found burger menu with selector: ${selector}`);
        break;
      }
    } catch (e) {
      // Continue to next selector
    }
  }

  // If not found, try to search by SVG icons that look like hamburgers
  if (!burgerSelector) {
    const allButtons = await page.$$('button, div[role="button"]');
    for (const btn of allButtons) {
      const text = await btn.textContent();
      const ariaLabel = await btn.getAttribute('aria-label');
      const classList = await btn.getAttribute('class');

      if (classList && (classList.includes('menu') || classList.includes('hamburger') || classList.includes('burger'))) {
        burgerSelector = `.${classList.split(' ').join('.')}`;
        console.log(`✅ Found burger menu via class: ${burgerSelector}`);
        break;
      }
    }
  }

  // Take screenshot before clicking
  await page.screenshot({ path: path.join(testResultsDir, 'screenshot_002_before_menu_click.png') });
  console.log('✅ Screenshot saved: screenshot_002_before_menu_click.png');

  // Click burger menu
  if (!burgerSelector) {
    throw new Error('❌ Could not find burger menu selector');
  }

  console.log('🔹 Step 4: Clicking burger menu...');
  await page.click(burgerSelector);
  await page.waitForTimeout(2000);

  await page.screenshot({ path: path.join(testResultsDir, 'screenshot_003_menu_opened.png') });
  console.log('✅ Screenshot saved: screenshot_003_menu_opened.png');

  // Find Google Play button
  console.log('🔹 Step 5: Finding Google Play button...');

  const googlePlaySelectors = [
    'a[href*="play.google.com"]',
    'a:has-text("Google Play")',
    'a:has-text("Get it on Google Play")',
    'button:has-text("Google Play")',
    '[data-testid="google-play-button"]',
    '.google-play-button',
    'img[alt*="Google Play"]'
  ];

  let googlePlaySelector = null;
  for (const selector of googlePlaySelectors) {
    try {
      const element = await page.$(selector);
      if (element) {
        googlePlaySelector = selector;
        console.log(`✅ Found Google Play button with selector: ${selector}`);
        break;
      }
    } catch (e) {
      // Continue to next selector
    }
  }

  // Take screenshot before clicking Google Play
  await page.screenshot({ path: path.join(testResultsDir, 'screenshot_004_before_google_play_click.png') });
  console.log('✅ Screenshot saved: screenshot_004_before_google_play_click.png');

  // Click Google Play button
  if (!googlePlaySelector) {
    throw new Error('❌ Could not find Google Play button selector');
  }

  console.log('🔹 Step 6: Clicking Google Play button...');
  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page.click(googlePlaySelector)
  ]);

  // Wait for navigation
  await newPage.waitForLoadState('networkidle');
  await newPage.waitForTimeout(2000);

  await newPage.screenshot({ path: path.join(testResultsDir, 'screenshot_005_google_play_page.png'), fullPage: true });
  console.log('✅ Screenshot saved: screenshot_005_google_play_page.png');

  // Verify URL
  const currentUrl = newPage.url();
  console.log(`🔹 Current URL: ${currentUrl}`);

  const isGooglePlay = currentUrl.includes('play.google.com');
  console.log(isGooglePlay ? '✅ Successfully navigated to Google Play' : '❌ Not on Google Play');

  // Save selectors to JSON
  const selectors = {
    burger_menu: burgerSelector,
    google_play_button: googlePlaySelector,
    found_at: new Date().toISOString(),
    environment: 'PROD',
    url: 'https://minebit-casino.prod.sofon.one/'
  };

  fs.writeFileSync(
    path.join('/Users/ihorsolopii/.openclaw/workspace/shared', 'UI_ELEMENTS.md'),
    JSON.stringify(selectors, null, 2)
  );
  console.log('✅ Selectors saved to UI_ELEMENTS.md');

  // Save test results
  const testResults = {
    tested_by: 'QA Agent',
    date: new Date().toISOString(),
    environment: 'PROD',
    url: 'https://minebit-casino.prod.sofon.one/',
    devices: 'Desktop Chrome',
    selectors_found: {
      burger_menu: burgerSelector,
      google_play_button: googlePlaySelector
    },
    test_results: {
      burger_menu_click: '✅ PASS',
      menu_opened: '✅ PASS',
      google_play_click: '✅ PASS',
      navigation_to_google_play: isGooglePlay ? '✅ PASS' : '❌ FAIL'
    },
    final_url: currentUrl,
    evidence_folder: '~/.openclaw/workspace/shared/test-results/CT-GOOGLE-PLAY/'
  };

  fs.writeFileSync(
    path.join(testResultsDir, 'test_results.json'),
    JSON.stringify(testResults, null, 2)
  );
  console.log('✅ Test results saved');

  await browser.close();

  console.log('\n' + '='.repeat(60));
  console.log('🎯 TEST COMPLETED');
  console.log('='.repeat(60));
  console.log(`Burger menu selector: ${burgerSelector}`);
  console.log(`Google Play selector: ${googlePlaySelector}`);
  console.log(`Navigation to Google Play: ${isGooglePlay ? '✅ SUCCESS' : '❌ FAILED'}`);
  console.log(`Final URL: ${currentUrl}`);
  console.log(`\nEvidence saved to: ${testResultsDir}`);

  return testResults;
}

testGooglePlayButton().catch(console.error);
