"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const playwright_1 = require("playwright");
(async () => {
    const userDataDir = '/Users/ihorsolopii/Library/Application Support/Google/Chrome/Default';
    const browser = await playwright_1.chromium.launchPersistentContext(userDataDir, {
        headless: false,
        viewport: { width: 1280, height: 720 },
        args: [
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
        ],
    });
    const page = await browser.newPage();
    try {
        console.log('Navigating to https://www.lorypten.com...');
        await page.goto('https://www.lorypten.com', { waitUntil: 'networkidle' });
        // Wait for page to load
        await page.waitForLoadState('domcontentloaded');
        // Look for Connect button - common selectors for Web3 connect buttons
        const connectSelectors = [
            'button:has-text("Connect")',
            'button:has-text("Connect Wallet")',
            '[data-testid="connect-button"]',
            '.connect-button',
            'button:has-text("Sign in")',
            'button:has-text("Login")',
        ];
        let connectButton = null;
        for (const selector of connectSelectors) {
            connectButton = await page.locator(selector).first();
            if (await connectButton.count() > 0) {
                console.log(`Found connect button with selector: ${selector}`);
                break;
            }
        }
        if (!connectButton || await connectButton.count() === 0) {
            // Take screenshot for debugging
            await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/no-connect-button.png' });
            throw new Error('Connect button not found');
        }
        console.log('Clicking connect button...');
        await connectButton.click();
        // Wait for Phantom popup - it might open a new window
        // Or wait for wallet address to appear on page
        const walletAddressSelectors = [
            'button:has-text("0x")',
            'button:has-text("Disconnect")',
            '[data-testid="wallet-address"]',
            '.wallet-address',
            'button:has-text("Connected")',
        ];
        // Wait for any of these selectors for up to 30 seconds
        let walletElement = null;
        for (const selector of walletAddressSelectors) {
            try {
                walletElement = page.locator(selector).first();
                await walletElement.waitFor({ state: 'visible', timeout: 30000 });
                console.log(`Wallet connected! Found element: ${selector}`);
                break;
            }
            catch (e) {
                // continue
            }
        }
        if (!walletElement) {
            // Check if there's a Phantom popup window
            const pages = browser.pages();
            if (pages.length > 1) {
                console.log('Found multiple pages, maybe Phantom popup opened');
                const popup = pages[1];
                await popup.waitForLoadState();
                // Take screenshot of popup
                await popup.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/phantom-popup.png' });
                console.log('Popup screenshot saved');
            }
        }
        // Take screenshot of main page after connection attempt
        await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/after-connect.png' });
        // Also take full page screenshot
        await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/full-page.png', fullPage: true });
        console.log('Test completed. Screenshots saved to workspace/temp/');
    }
    catch (error) {
        console.error('Error during test:', error);
        await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/temp/error.png' });
        throw error;
    }
    finally {
        // Close browser after 5 seconds to allow manual inspection
        console.log('Closing browser in 5 seconds...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        await browser.close();
    }
})();
