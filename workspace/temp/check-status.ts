import { chromium, type BrowserContext, type Page } from 'playwright';

(async () => {
  const userDataDir = '/Users/ihorsolopii/Library/Application Support/Google/Chrome/Default';
  const browser: BrowserContext = await chromium.launchPersistentContext(userDataDir, {
    headless: true,
    viewport: { width: 1280, height: 720 },
  });

  const page: Page = await browser.newPage();
  
  try {
    console.log('Navigating to https://www.lorypten.com...');
    await page.goto('https://www.lorypten.com', { waitUntil: 'networkidle' });
    
    // Wait for page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Take screenshot of current state
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/current-state.png', fullPage: true });
    
    // Check for wallet connection indicators
    const walletButton = await page.locator('button.wallet-adapter-button').first();
    if (await walletButton.count() > 0) {
      const buttonText = await walletButton.textContent();
      const isDisabled = await walletButton.isDisabled();
      console.log(`Wallet button text: "${buttonText}"`);
      console.log(`Wallet button disabled: ${isDisabled}`);
      
      // If button says "Disconnect Wallet" - wallet is connected
      if (buttonText?.includes('Disconnect')) {
        console.log('✅ Wallet appears to be connected!');
        
        // Look for wallet address
        const addressElement = await page.locator('[data-testid="wallet-address"], .wallet-address, button:has-text("0x")').first();
        if (await addressElement.count() > 0) {
          const address = await addressElement.textContent();
          console.log(`Wallet address: ${address}`);
        }
      } else if (buttonText?.includes('Connect')) {
        console.log('⚠️ Wallet connect button found but not connected');
      }
    } else {
      console.log('No wallet button found');
    }
    
    // Also check for any other indicators
    const bodyText = await page.textContent('body');
    if (bodyText?.includes('Connected') || bodyText?.includes('0x')) {
      console.log('Found "Connected" or "0x" in page text');
    }
    
    console.log('Screenshot saved to current-state.png');
    
  } catch (error) {
    console.error('Error:', error);
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/check-error.png' });
  } finally {
    await browser.close();
  }
})();