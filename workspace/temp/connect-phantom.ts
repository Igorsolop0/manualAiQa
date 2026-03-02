import { chromium, type BrowserContext, type Page } from 'playwright';

(async () => {
  const userDataDir = '/Users/ihorsolopii/Library/Application Support/Google/Chrome/Default';
  const browser: BrowserContext = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    viewport: { width: 1280, height: 720 },
  });

  const page: Page = await browser.newPage();
  
  try {
    console.log('Navigating to https://www.lorypten.com...');
    await page.goto('https://www.lorypten.com', { waitUntil: 'networkidle' });
    
    await page.waitForLoadState('domcontentloaded');
    
    // Take initial screenshot
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/initial.png' });
    
    // Find and click Select Wallet button
    const selectButton = await page.locator('button:has-text("Select Wallet")').first();
    if (await selectButton.count() === 0) {
      throw new Error('Select Wallet button not found');
    }
    
    console.log('Clicking Select Wallet button...');
    await selectButton.click();
    
    // Wait for wallet selection modal
    await page.waitForTimeout(2000);
    
    // Take screenshot of modal
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/wallet-modal.png' });
    
    // Look for Phantom wallet option
    const phantomOption = await page.locator('button:has-text("Phantom")').first();
    if (await phantomOption.count() === 0) {
      console.log('Phantom option not found in modal. Listing all wallet buttons:');
      const allButtons = await page.locator('button').all();
      for (const btn of allButtons) {
        const text = await btn.textContent();
        console.log(`Button text: "${text}"`);
      }
      throw new Error('Phantom wallet option not found');
    }
    
    console.log('Clicking Phantom wallet option...');
    await phantomOption.click();
    
    // Wait for connection - may open Phantom popup
    await page.waitForTimeout(5000);
    
    // Check if new popup opened
    const pages = browser.pages();
    if (pages.length > 1) {
      console.log('Popup window detected, taking screenshot...');
      const popup = pages[1];
      await popup.waitForLoadState();
      await popup.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/phantom-popup.png' });
      // Check if popup has connect/approve button
      const approveButton = await popup.locator('button:has-text("Connect"), button:has-text("Approve"), button:has-text("Sign")').first();
      if (await approveButton.count() > 0) {
        console.log('Found approve button in popup, clicking...');
        await approveButton.click();
        await page.waitForTimeout(3000);
      }
    }
    
    // Check connection status on main page
    await page.waitForTimeout(3000);
    const connectedButton = await page.locator('button:has-text("Disconnect"), button:has-text("Connected"), button:has-text("0x")').first();
    if (await connectedButton.count() > 0) {
      const text = await connectedButton.textContent();
      console.log(`✅ Wallet connected! Button text: "${text}"`);
      await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/connected.png', fullPage: true });
    } else {
      console.log('Wallet not connected yet');
      await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/not-connected.png', fullPage: true });
    }
    
    // Final screenshot
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/final.png', fullPage: true });
    
    console.log('Test completed. Check screenshots in workspace/temp/');
    
  } catch (error) {
    console.error('Error:', error);
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/connect-error.png', fullPage: true });
  } finally {
    // Keep browser open for 10 seconds for inspection
    console.log('Keeping browser open for 10 seconds...');
    await page.waitForTimeout(10000);
    await browser.close();
  }
})();