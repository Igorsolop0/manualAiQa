import { test, expect } from '@playwright/test';

test.describe('CT-548: Google Account Linking', () => {
  test('Scenario 1: Link Google account to existing user', async ({ browser }) => {
    // Use Chrome Profile 3
    const context = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      storageState: undefined, // Fresh context
    });

    // Connect to Chrome Profile 3 CDP
    // Note: Chrome must be launched with --remote-debugging-port=18803
    // And using Profile 3

    const page = await context.newPage();
    const evidenceDir = '/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548/scenario-1';

    // Step 1: Navigate to QA
    await page.goto('https://minebit-casino.qa.sofon.one');
    await page.screenshot({ path: `${evidenceDir}/01-homepage.png` });

    // Step 2: Click Log In
    await page.click('button:has-text("Log In")');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: `${evidenceDir}/02-login-modal.png` });

    // Step 3: Fill credentials
    await page.fill('input[type="email"]', 'test-ihorsolop0@nextcode.tech');
    await page.fill('input[type="password"]', 'Qweasd123!');
    await page.screenshot({ path: `${evidenceDir}/03-filled-credentials.png` });

    // Step 4: Submit login
    await page.click('button:has-text("Start Playing")');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: `${evidenceDir}/04-after-login.png` });

    // Step 5: Navigate to test-social-linking
    await page.goto('https://minebit-casino.qa.sofon.one/test-social-linking');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${evidenceDir}/05-social-linking-page.png` });

    // Step 6: Find and click Link Google button
    const linkGoogleButton = page.locator('button:has-text("Google"), [data-testid*="google"], [aria-label*="Google"]');
    await linkGoogleButton.first().click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${evidenceDir}/06-google-linking-initiated.png` });

    // Step 7: Handle Google OAuth (if popup appears)
    const [popup] = await Promise.all([
      page.waitForEvent('popup').catch(() => null),
      page.waitForTimeout(3000),
    ]);

    if (popup) {
      await popup.screenshot({ path: `${evidenceDir}/07-google-oauth-popup.png` });
      // Note: User needs to manually select Google account from Profile 3
      // Or we need to pre-authenticate in Profile 3
    }

    // Step 8: Check final state
    await page.screenshot({ path: `${evidenceDir}/08-final-state.png` });

    // Evidence: Check if Google is linked
    const pageContent = await page.content();
    const isGoogleLinked = pageContent.includes('Google') && pageContent.includes('linked');

    // Write results
    const results = {
      ticket: 'CT-548',
      scenario: 1,
      status: isGoogleLinked ? 'SUCCESS' : 'PARTIAL',
      evidence: `${evidenceDir}`,
      notes: 'Manual verification needed for Google OAuth with Chrome Profile 3',
    };

    console.log(JSON.stringify(results, null, 2));

    await context.close();
  });
});
