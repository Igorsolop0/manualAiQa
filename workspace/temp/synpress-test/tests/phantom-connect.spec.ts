import { test, expect } from '@playwright/test';

test.describe('Phantom wallet connection to Lorypten', () => {
  test('should connect Phantom wallet', async ({ page }) => {
    // Navigate to site
    await page.goto('https://www.lorypten.com');
    
    // Wait for page load
    await page.waitForLoadState('networkidle');
    
    // Take screenshot of initial state
    await page.screenshot({ path: 'initial-state.png', fullPage: true });
    
    // Check for wallet connection UI
    const selectWalletButton = page.locator('button:has-text("Select Wallet")').first();
    
    if (await selectWalletButton.count() > 0) {
      console.log('Found Select Wallet button');
      await selectWalletButton.click();
      await page.waitForTimeout(2000);
      
      // Look for Phantom option
      const phantomOption = page.locator('button:has-text("Phantom")').first();
      
      if (await phantomOption.count() > 0) {
        console.log('Found Phantom option, clicking...');
        await phantomOption.click();
        await page.waitForTimeout(5000);
        
        // Check for connection confirmation
        const disconnectButton = page.locator('button:has-text("Disconnect")').first();
        if (await disconnectButton.count() > 0) {
          console.log('✅ Wallet connected successfully!');
          await page.screenshot({ path: 'connected.png', fullPage: true });
        } else {
          console.log('Wallet not connected after clicking Phantom');
          await page.screenshot({ path: 'not-connected.png', fullPage: true });
        }
      } else {
        console.log('Phantom option not found in wallet list');
        await page.screenshot({ path: 'no-phantom-option.png', fullPage: true });
        
        // List all wallet options
        const walletButtons = await page.locator('button').all();
        for (const button of walletButtons) {
          const text = await button.textContent();
          console.log(`Wallet button: "${text}"`);
        }
      }
    } else {
      console.log('Select Wallet button not found');
      await page.screenshot({ path: 'no-select-button.png', fullPage: true });
    }
  });
});