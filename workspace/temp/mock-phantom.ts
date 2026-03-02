import { chromium, type BrowserContext, type Page } from 'playwright';

(async () => {
  const userDataDir = '/Users/ihorsolopii/Library/Application Support/Google/Chrome/Default';
  const browser: BrowserContext = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    viewport: { width: 1280, height: 720 },
  });

  const page: Page = await browser.newPage();
  
  // Inject mock solana object before page loads
  await page.addInitScript(() => {
    // Create mock Phantom wallet
    const mockSolana = {
      isPhantom: true,
      isConnected: false,
      publicKey: null,
      connect: async () => {
        console.log('Mock Phantom: connect called');
        // Simulate successful connection
        mockSolana.isConnected = true;
        mockSolana.publicKey = {
          toBase58: () => 'MockPublicKey11111111111111111111111111111111'
        };
        return { publicKey: mockSolana.publicKey };
      },
      disconnect: async () => {
        console.log('Mock Phantom: disconnect called');
        mockSolana.isConnected = false;
        mockSolana.publicKey = null;
      },
      signMessage: async (message: Uint8Array) => {
        console.log('Mock Phantom: signMessage called');
        return { signature: new Uint8Array(64).fill(1) };
      },
      signTransaction: async (transaction: any) => {
        console.log('Mock Phantom: signTransaction called');
        return transaction;
      },
      signAllTransactions: async (transactions: any[]) => {
        console.log('Mock Phantom: signAllTransactions called');
        return transactions;
      },
      on: (event: string, callback: Function) => {
        console.log(`Mock Phantom: event listener added for ${event}`);
      },
      off: (event: string, callback: Function) => {
        console.log(`Mock Phantom: event listener removed for ${event}`);
      }
    };
    
    // Inject into window
    (window as any).solana = mockSolana;
    console.log('Mock Phantom wallet injected');
  });
  
  try {
    console.log('Navigating to https://www.lorypten.com...');
    await page.goto('https://www.lorypten.com', { waitUntil: 'networkidle' });
    
    // Wait for page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Take initial screenshot
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/mock-initial.png' });
    
    // Check if mock is present
    const mockExists = await page.evaluate(() => {
      return typeof (window as any).solana !== 'undefined' && (window as any).solana.isPhantom;
    });
    console.log(`Mock wallet injected and detected: ${mockExists}`);
    
    // Check for Select Wallet button
    const selectButton = await page.locator('button:has-text("Select Wallet")').first();
    if (await selectButton.count() === 0) {
      console.log('Select Wallet button not found, looking for other buttons...');
      const allButtons = await page.locator('button').all();
      for (const btn of allButtons) {
        const text = await btn.textContent();
        console.log(`Button text: "${text}"`);
      }
    } else {
      console.log('Clicking Select Wallet button...');
      await selectButton.click();
      await page.waitForTimeout(2000);
      
      // Check if Phantom appears in list
      const phantomOption = await page.locator('button:has-text("Phantom")').first();
      if (await phantomOption.count() > 0) {
        console.log('✅ Phantom option found! Mock injection worked.');
        await phantomOption.click();
        await page.waitForTimeout(3000);
        
        // Check connection status
        const connectedButton = await page.locator('button:has-text("Disconnect"), button:has-text("Connected")').first();
        if (await connectedButton.count() > 0) {
          const text = await connectedButton.textContent();
          console.log(`✅ Wallet connected! Button text: "${text}"`);
        } else {
          console.log('Wallet not connected after clicking Phantom');
        }
      } else {
        console.log('Phantom option still not found, taking screenshot of modal...');
        await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/mock-modal.png', fullPage: true });
        
        // List all options in modal
        const modalButtons = await page.locator('button').all();
        for (const btn of modalButtons) {
          const text = await btn.textContent();
          console.log(`Modal button: "${text}"`);
        }
      }
    }
    
    // Final screenshot
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/mock-final.png', fullPage: true });
    
    console.log('Test completed. Keeping browser open for inspection...');
    await page.waitForTimeout(10000);
    
  } catch (error) {
    console.error('Error:', error);
    await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/mock-error.png', fullPage: true });
  } finally {
    await browser.close();
  }
})();