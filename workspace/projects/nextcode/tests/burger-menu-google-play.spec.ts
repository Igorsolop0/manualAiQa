import { test, expect } from '@playwright/test';

test.describe('Burger Menu and Google Play Button Test', () => {
  test('should open burger menu and click Google Play button', async ({ page }) => {
    // Step 1: Navigate to Minebit Casino
    await page.goto('https://minebit-casino.prod.sofon.one/');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Step 2: Find and click burger menu
    const burgerSelectors = [
      'button.burger-menu',
      '[data-testid="burger-menu"]',
      '.menu-toggle',
      '.hamburger',
      'button[aria-label="Menu"]',
      '.header button:first-child',
      'button:has(svg)',
      'button:has(path)'
    ];
    
    let burgerFound = false;
    for (const selector of burgerSelectors) {
      const burgerButton = page.locator(selector).first();
      if (await burgerButton.count() > 0) {
        console.log(`Found burger menu with selector: ${selector}`);
        await burgerButton.click();
        burgerFound = true;
        break;
      }
    }
    
    if (!burgerFound) {
      // Fallback: click on any button that looks like menu
      const allButtons = page.locator('button');
      const buttonCount = await allButtons.count();
      for (let i = 0; i < buttonCount; i++) {
        const button = allButtons.nth(i);
        const text = await button.textContent();
        if (!text || text.trim() === '') {
          // Empty button might be icon button
          await button.click();
          await page.waitForTimeout(1000);
          // Check if side panel opened
          const sidePanel = page.locator('.side-panel, .drawer, .sidebar, [aria-expanded="true"]').first();
          if (await sidePanel.count() > 0) {
            burgerFound = true;
            break;
          }
        }
      }
    }
    
    expect(burgerFound).toBeTruthy();
    
    // Step 3: Wait for side panel to open
    await page.waitForTimeout(2000);
    
    // Check for side panel
    const sidePanelSelectors = [
      '.side-panel',
      '.drawer',
      '.sidebar',
      '[aria-expanded="true"]',
      '.menu-open',
      '.nav-open'
    ];
    
    let sidePanelVisible = false;
    for (const selector of sidePanelSelectors) {
      const panel = page.locator(selector).first();
      if (await panel.count() > 0) {
        sidePanelVisible = true;
        console.log(`Side panel found with selector: ${selector}`);
        break;
      }
    }
    
    expect(sidePanelVisible).toBeTruthy();
    
    // Step 4: Find and click Google Play button
    const googlePlaySelectors = [
      'a[href*="play.google.com"]',
      '.google-play-button',
      '[data-testid="google-play-button"]',
      'button:has-text("Google Play")',
      'a:has-text("GET IT ON")',
      'a:has-text("Google Play")',
      'a:has-text("Get it on")'
    ];
    
    let googlePlayFound = false;
    let googlePlayUrl = '';
    
    for (const selector of googlePlaySelectors) {
      const googlePlayButton = page.locator(selector).first();
      if (await googlePlayButton.count() > 0) {
        console.log(`Found Google Play button with selector: ${selector}`);
        googlePlayUrl = await googlePlayButton.getAttribute('href') || '';
        await googlePlayButton.click();
        googlePlayFound = true;
        break;
      }
    }
    
    if (!googlePlayFound) {
      // Look for any link containing play.google.com
      const allLinks = page.locator('a');
      const linkCount = await allLinks.count();
      for (let i = 0; i < linkCount; i++) {
        const link = allLinks.nth(i);
        const href = await link.getAttribute('href');
        if (href && href.includes('play.google.com')) {
          googlePlayUrl = href;
          await link.click();
          googlePlayFound = true;
          break;
        }
      }
    }
    
    expect(googlePlayFound).toBeTruthy();
    expect(googlePlayUrl).toContain('play.google.com');
    
    // Step 5: Wait for navigation and verify Google Play page
    await page.waitForLoadState('networkidle');
    
    // Check if we're on Google Play
    const currentUrl = page.url();
    console.log(`Navigated to: ${currentUrl}`);
    
    // Verify it's Google Play
    expect(currentUrl).toContain('play.google.com');
    
    // Check for Google Play content
    const pageTitle = await page.title();
    const pageContent = await page.textContent('body');
    
    expect(pageTitle).toBeTruthy();
    expect(pageContent).toBeTruthy();
    
    // Take screenshot for evidence
    const screenshotPath = `test-results/burger-menu-google-play-${Date.now()}.png`;
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`Screenshot saved: ${screenshotPath}`);
    
    // Step 6: Generate Jira report
    const testResults = {
      testName: 'Burger Menu and Google Play Button Test',
      timestamp: new Date().toISOString(),
      url: 'https://minebit-casino.prod.sofon.one/',
      burgerMenuFound: burgerFound,
      sidePanelOpened: sidePanelVisible,
      googlePlayButtonFound: googlePlayFound,
      googlePlayUrl: googlePlayUrl,
      navigatedToGooglePlay: currentUrl.includes('play.google.com'),
      screenshot: screenshotPath,
      status: 'PASSED'
    };
    
    console.log('Test Results:', JSON.stringify(testResults, null, 2));
    
    // Save results to file
    const fs = require('fs');
    fs.writeFileSync(
      `test-results/burger-menu-results-${Date.now()}.json`,
      JSON.stringify(testResults, null, 2)
    );
  });
});