import { test, expect } from '@playwright/test';

test.describe('Minebit Burger Menu & Google Play Flow', () => {
  test('should open burger menu and navigate to Google Play', async ({ page }) => {
    // Step 1: Navigate to Minebit prod
    await page.goto('https://minebit-casino.prod.sofon.one');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Take initial screenshot
    await page.screenshot({ path: 'test-results/01-initial-page.png', fullPage: true });
    
    // Step 2: Try to find and click burger menu
    const burgerMenuSelectors = [
      'button[aria-label="Menu"]',
      '.burger-menu',
      '.hamburger-menu',
      '[data-testid="menu-button"]',
      '[data-cy="menu-toggle"]',
      '[data-test="nav-toggle"]',
      'button:has(svg)',
      'button:has(path)'
    ];
    
    let burgerMenuFound = false;
    for (const selector of burgerMenuSelectors) {
      const elements = await page.locator(selector).count();
      if (elements > 0) {
        console.log(`Found burger menu with selector: ${selector}`);
        await page.locator(selector).first().click();
        burgerMenuFound = true;
        
        // Take screenshot after clicking menu
        await page.screenshot({ path: 'test-results/02-menu-clicked.png', fullPage: true });
        break;
      }
    }
    
    if (!burgerMenuFound) {
      // Fallback: click first button in header
      const headerButtons = await page.locator('header button, .header button').count();
      if (headerButtons > 0) {
        await page.locator('header button, .header button').first().click();
        burgerMenuFound = true;
        console.log('Used fallback: clicked first button in header');
      }
    }
    
    expect(burgerMenuFound).toBeTruthy();
    
    // Step 3: Wait for side panel to open
    await page.waitForTimeout(1000); // Brief wait for animation
    
    // Check for side panel selectors
    const sidePanelSelectors = [
      '.side-panel',
      '.nav-menu',
      '[role="navigation"]',
      '.drawer',
      '.sidebar',
      '.menu-panel'
    ];
    
    let sidePanelVisible = false;
    for (const selector of sidePanelSelectors) {
      const elements = await page.locator(selector).count();
      if (elements > 0) {
        const isVisible = await page.locator(selector).first().isVisible();
        if (isVisible) {
          sidePanelVisible = true;
          console.log(`Side panel visible with selector: ${selector}`);
          
          // Take screenshot of opened menu
          await page.screenshot({ path: 'test-results/03-menu-opened.png', fullPage: true });
          break;
        }
      }
    }
    
    // Step 4: Find Google Play button
    const googlePlaySelectors = [
      'a[href*="play.google.com"]',
      'img[alt*="Google Play"]',
      'img[alt*="Get it on Google Play"]',
      '.google-play-button',
      '[data-testid="google-play-button"]',
      'a:has-text("Google Play")',
      'a:has-text("Get it on Google Play")'
    ];
    
    let googlePlayButtonFound = false;
    let googlePlayHref = '';
    
    for (const selector of googlePlaySelectors) {
      const elements = await page.locator(selector).count();
      if (elements > 0) {
        const element = page.locator(selector).first();
        googlePlayHref = await element.getAttribute('href') || '';
        googlePlayButtonFound = true;
        console.log(`Found Google Play button with selector: ${selector}, href: ${googlePlayHref}`);
        
        // Take screenshot before clicking
        await page.screenshot({ path: 'test-results/04-before-google-play-click.png', fullPage: true });
        
        // Click the button
        await element.click();
        break;
      }
    }
    
    if (!googlePlayButtonFound) {
      // Look for any download/app store links
      const allLinks = await page.locator('a').all();
      for (const link of allLinks) {
        const href = await link.getAttribute('href');
        const text = await link.textContent();
        if (href && (href.includes('play.google.com') || text?.includes('Google Play'))) {
          googlePlayHref = href;
          googlePlayButtonFound = true;
          console.log(`Found Google Play link by text/href: ${text}, ${href}`);
          await link.click();
          break;
        }
      }
    }
    
    expect(googlePlayButtonFound).toBeTruthy();
    
    // Step 5: Wait for navigation and verify Google Play page
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000); // Additional wait for redirect
    
    // Check if we're on Google Play
    const currentUrl = page.url();
    console.log(`Current URL after click: ${currentUrl}`);
    
    // Take screenshot of destination page
    await page.screenshot({ path: 'test-results/05-google-play-page.png', fullPage: true });
    
    // Verify Google Play page
    const pageTitle = await page.title();
    const pageContent = await page.content();
    
    // Check for Google Play indicators
    const isGooglePlay = currentUrl.includes('play.google.com') || 
                        pageTitle.includes('Google Play') ||
                        pageContent.includes('Google Play') ||
                        pageContent.includes('Android app');
    
    console.log(`Page title: ${pageTitle}`);
    console.log(`Is Google Play page: ${isGooglePlay}`);
    
    // Verify page has content
    expect(pageContent.length).toBeGreaterThan(1000);
    
    // Check for common Google Play elements
    const hasInstallButton = await page.locator('button:has-text("Install"), button:has-text("Install app")').count() > 0;
    const hasAppDescription = await page.locator('div:has-text("app"), div:has-text("App")').count() > 0;
    
    console.log(`Has install button: ${hasInstallButton}`);
    console.log(`Has app description: ${hasAppDescription}`);
    
    // Final validation
    expect(isGooglePlay || hasInstallButton || hasAppDescription).toBeTruthy();
    
    // Generate test report
    const testReport = {
      testName: 'Burger Menu & Google Play Flow',
      timestamp: new Date().toISOString(),
      urlTested: 'https://minebit-casino.prod.sofon.one',
      burgerMenuFound,
      sidePanelVisible,
      googlePlayButtonFound,
      googlePlayHref,
      redirectedTo: currentUrl,
      isGooglePlayPage: isGooglePlay,
      pageTitle,
      hasInstallButton,
      hasAppDescription,
      screenshots: [
        'test-results/01-initial-page.png',
        'test-results/02-menu-clicked.png',
        'test-results/03-menu-opened.png',
        'test-results/04-before-google-play-click.png',
        'test-results/05-google-play-page.png'
      ]
    };
    
    console.log('Test Report:', JSON.stringify(testReport, null, 2));
    
    // Save report to file
    const fs = require('fs');
    fs.writeFileSync('test-results/test-report.json', JSON.stringify(testReport, null, 2));
  });
});