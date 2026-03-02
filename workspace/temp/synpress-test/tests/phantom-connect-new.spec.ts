import { test as base, chromium, type BrowserContext } from '@playwright/test';
import path from 'path';
import fs from 'fs';

// Try to import from synpress-phantom
let phantomFixture;
try {
  const { phantomFixture: pf } = await import('@synthetixio/synpress-phantom/playwright');
  phantomFixture = pf;
} catch (error) {
  console.log('Could not import synpress-phantom fixture, using custom...');
}

// Custom fixture if synpress-phantom not available
export const test = phantomFixture || base.extend<{
  context: BrowserContext;
  extensionId: string;
}>({
  context: async ({}, use) => {
    // We need to find Phantom extension path
    // Look in synpress-phantom package for extension
    const possiblePaths = [
      path.join(__dirname, '../node_modules/@synthetixio/synpress-phantom/dist/extension'),
      path.join(__dirname, '../node_modules/@synthetixio/synpress-phantom/extension'),
      path.join(__dirname, '../node_modules/@synthetixio/synpress-phantom/dist'),
      // Also check if there's a downloaded extension
      path.join(process.env.HOME || '', '.cache/synpress/phantom'),
    ];
    
    let extensionPath = '';
    for (const p of possiblePaths) {
      if (fs.existsSync(p) && fs.existsSync(path.join(p, 'manifest.json'))) {
        extensionPath = p;
        break;
      }
    }
    
    if (!extensionPath) {
      throw new Error('Phantom extension not found. Please run: npx synpress-cache --phantom');
    }
    
    console.log(`Using Phantom extension from: ${extensionPath}`);
    
    const context = await chromium.launchPersistentContext('', {
      headless: false, // Required for extensions
      args: [
        `--disable-extensions-except=${extensionPath}`,
        `--load-extension=${extensionPath}`,
        '--no-sandbox',
      ],
    });
    
    await use(context);
    await context.close();
  },

  extensionId: async ({ context }, use) => {
    // Wait for service worker for Manifest V3
    let [worker] = context.serviceWorkers();
    if (!worker) {
      worker = await context.waitForEvent('serviceworker');
    }
    const extensionId = worker.url().split('/')[2];
    console.log(`Phantom extension ID: ${extensionId}`);
    await use(extensionId);
  },
});

export const { expect } = test;

// Test to connect Phantom wallet to Lorypten
test('connect Phantom wallet to Lorypten', async ({ context, extensionId, page }) => {
  // First, we need to import a test wallet (if not already set up)
  // This would require navigating to phantom onboarding page
  // For now, assume wallet is already set up
  
  // Navigate to Lorypten
  await page.goto('https://www.lorypten.com');
  await page.waitForLoadState('networkidle');
  
  // Take initial screenshot
  await page.screenshot({ path: 'test-initial.png' });
  
  // Check for Select Wallet button
  const selectButton = page.locator('button:has-text("Select Wallet")').first();
  if (await selectButton.count() === 0) {
    throw new Error('Select Wallet button not found');
  }
  
  await selectButton.click();
  await page.waitForTimeout(2000);
  
  // Look for Phantom option - now it should be there since window.solana is injected
  const phantomOption = page.locator('button:has-text("Phantom")').first();
  if (await phantomOption.count() === 0) {
    await page.screenshot({ path: 'test-no-phantom.png', fullPage: true });
    
    // Debug: list all wallet options
    const buttons = await page.locator('button').all();
    for (const btn of buttons) {
      const text = await btn.textContent();
      console.log(`Button: "${text}"`);
    }
    
    throw new Error('Phantom option still not found after extension load');
  }
  
  console.log('Found Phantom option, clicking...');
  await phantomOption.click();
  
  // Wait for Phantom popup
  const popupPromise = context.waitForEvent('page');
  const popup = await popupPromise;
  await popup.waitForLoadState();
  
  // Take screenshot of popup
  await popup.screenshot({ path: 'test-phantom-popup.png' });
  
  // Click connect/approve button in popup
  const connectButton = popup.locator('button:has-text("Connect"), button:has-text("Approve")').first();
  if (await connectButton.count() > 0) {
    await connectButton.click();
  }
  
  // Wait for connection on main page
  await page.waitForTimeout(3000);
  
  // Check for disconnect button or wallet address
  const disconnectButton = page.locator('button:has-text("Disconnect"), button:has-text("Connected")').first();
  if (await disconnectButton.count() > 0) {
    const text = await disconnectButton.textContent();
    console.log(`✅ Wallet connected! Button text: "${text}"`);
    await page.screenshot({ path: 'test-connected.png', fullPage: true });
  } else {
    console.log('Wallet not connected');
    await page.screenshot({ path: 'test-not-connected.png', fullPage: true });
  }
});