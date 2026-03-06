import { test, expect } from '@playwright/test';

test.describe('Burger Menu and Google Play Button Test', () => {
  test('should open burger menu and click Google Play button', async ({ page }) => {
    // 1. Navigate to Minebit casino
    await page.goto('https://minebit-casino.prod.sofon.one/');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // 2. Find and click burger menu icon
    // Try different selectors for burger menu
    const burgerMenuSelectors = [
      'button[aria-label*="menu"]',
      'button.menu-toggle',
      '.burger-menu',
      '.hamburger-icon',
      'button:has(svg)',
      '[data-testid="menu-button"]',
      'button:has-text("Menu")'
    ];
    
    let burgerMenuClicked = false;
    for (const selector of burgerMenuSelectors) {
      try {
        const element = page.locator(selector).first();
        if (await element.count() > 0) {
          await element.click();
          console.log(`Clicked burger menu with selector: ${selector}`);
          burgerMenuClicked = true;
          
          // Wait for side panel to open
          await page.waitForTimeout(1000);
          break;
        }
      } catch (error) {
        console.log(`Selector ${selector} not found or not clickable`);
      }
    }
    
    if (!burgerMenuClicked) {
      // Try to find any button that might be the menu
      const allButtons = await page.locator('button').all();
      for (const button of allButtons) {
        const boundingBox = await button.boundingBox();
        if (boundingBox && boundingBox.width < 50 && boundingBox.height < 50) {
          // Small button, likely a menu icon
          await button.click();
          console.log('Clicked small button (potential menu)');
          burgerMenuClicked = true;
          await page.waitForTimeout(1000);
          break;
        }
      }
    }
    
    expect(burgerMenuClicked).toBeTruthy();
    
    // 3. Find and click "Get it on Google Play" button
    const googlePlaySelectors = [
      'a[href*="play.google.com"]',
      '.google-play-button',
      'button:has-text("Get it on Google Play")',
      'a:has-text("Get it on Google Play")',
      '[data-testid="google-play-button"]'
    ];
    
    let googlePlayClicked = false;
    for (const selector of googlePlaySelectors) {
      try {
        const element = page.locator(selector).first();
        if (await element.count() > 0) {
          await element.click();
          console.log(`Clicked Google Play button with selector: ${selector}`);
          googlePlayClicked = true;
          break;
        }
      } catch (error) {
        console.log(`Selector ${selector} not found`);
      }
    }
    
    if (!googlePlayClicked) {
      // Try to find any link with Google Play text
      const allLinks = await page.locator('a').all();
      for (const link of allLinks) {
        const text = await link.textContent();
        if (text && text.includes('Google Play')) {
          await link.click();
          console.log('Clicked link with "Google Play" text');
          googlePlayClicked = true;
          break;
        }
      }
    }
    
    expect(googlePlayClicked).toBeTruthy();
    
    // 4. Verify we landed on Google Play page
    await page.waitForLoadState('networkidle');
    
    // Check URL contains play.google.com
    const currentUrl = page.url();
    expect(currentUrl).toContain('play.google.com');
    
    // Check page has content
    const pageTitle = await page.title();
    expect(pageTitle).toBeTruthy();
    
    // Check for Minebit content on Google Play page
    const pageContent = await page.textContent('body');
    expect(pageContent).toContainMatch(/minebit|casino|game/i);
    
    console.log(`Successfully navigated to: ${currentUrl}`);
    console.log(`Page title: ${pageTitle}`);
    
    // Take screenshot for evidence
    await page.screenshot({ path: 'google-play-result.png', fullPage: true });
  });
});