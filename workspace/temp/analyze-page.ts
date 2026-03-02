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
    
    // Check if window.solana exists
    const solanaExists = await page.evaluate(() => {
      return typeof (window as any).solana !== 'undefined';
    });
    console.log(`window.solana exists: ${solanaExists}`);
    
    // Check for wallet adapter
    const walletAdapterExists = await page.evaluate(() => {
      return typeof (window as any).phantom?.solana !== 'undefined';
    });
    console.log(`window.phantom.solana exists: ${walletAdapterExists}`);
    
    // List all global objects with "solana" or "phantom"
    const globalObjects = await page.evaluate(() => {
      const objects = [];
      for (const key in window) {
        if (key.toLowerCase().includes('solana') || key.toLowerCase().includes('phantom')) {
          objects.push(key);
        }
      }
      return objects;
    });
    console.log('Global objects with solana/phantom:', globalObjects);
    
    // Check for wallet adapter library
    const scripts = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('script')).map(script => script.src || script.textContent?.substring(0, 100));
    });
    
    const walletAdapterScripts = scripts.filter(src => 
      src && (src.includes('wallet-adapter') || src.includes('solana') || src.includes('phantom'))
    );
    console.log('Wallet adapter scripts found:', walletAdapterScripts.length);
    
    // Take screenshot
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/analysis.png', fullPage: true });
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();