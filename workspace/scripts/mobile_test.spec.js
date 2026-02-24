// Playwright Test - Mobile Device Emulation
// Run with: npx playwright test mobile_test.spec.js

import { test, expect, devices } from '@playwright/test';

// Pixel 7 configuration
test.use({
  ...devices['Pixel 7'],
});

test('Pixel 7 - Chrome browser test', async ({ page }) => {
  await page.goto('https://www.google.com');
  
  // Verify mobile viewport
  const viewport = page.viewportSize();
  console.log(`Pixel 7 Viewport: ${viewport.width}x${viewport.height}`);
  
  // Check if search box is visible
  const searchBox = await page.locator('textarea[name="q"], input[name="q"]');
  await expect(searchBox).toBeVisible();
  
  // Take screenshot
  await page.screenshot({ path: 'pixel7-google.png', fullPage: true });
  console.log('✅ Pixel 7 test passed');
});

// iPhone 14 configuration (separate test)
test.describe('iPhone 14 - Safari browser', () => {
  test.use({
    ...devices['iPhone 14'],
  });

  test('iPhone 14 - Safari browser test', async ({ page }) => {
    await page.goto('https://www.apple.com');
    
    // Verify mobile viewport
    const viewport = page.viewportSize();
    console.log(`iPhone 14 Viewport: ${viewport.width}x${viewport.height}`);
    
    // Check page title
    await expect(page).toHaveTitle(/Apple/);
    
    // Take screenshot
    await page.screenshot({ path: 'iphone14-apple.png', fullPage: true });
    console.log('✅ iPhone 14 test passed');
  });
});
