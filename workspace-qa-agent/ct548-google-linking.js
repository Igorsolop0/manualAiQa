// CT-548: Google Linking & Unlinking — UI Test
// Uses Playwright network mocking (no real Google accounts)
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const RESULTS_DIR = '/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-548';
const SCREENSHOTS_DIR = path.join(RESULTS_DIR, 'screenshots');
const NETWORK_DIR = path.join(RESULTS_DIR, 'network-logs');
const CONSOLE_DIR = path.join(RESULTS_DIR, 'console-logs');
const TEST_URL = 'https://minebit-casino.qa.sofon.one/test-social-linking';
const TIMESTAMP = Date.now();
const EMAIL = `ct548_test_${TIMESTAMP}@nextcode.tech`;
const PASSWORD = 'Qweasd123!';

// Ensure dirs
[SCREENSHOTS_DIR, NETWORK_DIR, CONSOLE_DIR].forEach(d => fs.mkdirSync(d, { recursive: true }));

const allResults = [];
const networkLog = [];
const consoleLog = [];

function addResult(tc, scenario, status, evidence, notes = '') {
  allResults.push({ tc, scenario, status, evidence, notes, timestamp: new Date().toISOString() });
}

async function screenshot(page, name) {
  const filePath = path.join(SCREENSHOTS_DIR, name);
  await page.screenshot({ path: filePath, timeout: 5000 }).catch(() => {});
  return filePath;
}

(async () => {
  console.log('=== CT-548: Google Linking & Unlinking ===\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // ---- Collect console & network ----
  page.on('console', msg => {
    const entry = { type: msg.type(), text: msg.text() };
    consoleLog.push(entry);
    if (msg.type() === 'error') console.log(`  [CONSOLE] ${msg.text().substring(0, 150)}`);
  });
  page.on('pageerror', err => {
    consoleLog.push({ type: 'pageerror', text: err.message });
  });

  page.on('request', req => {
    networkLog.push({ url: req.url(), method: req.method(), type: req.resourceType() });
    // Log API calls
    if (req.url().includes('GoogleAccount') || req.url().includes('GetAuthUrl') || 
        req.url().includes('LinkGoogle') || req.url().includes('UnlinkGoogle') ||
        req.url().includes('linkToken')) {
      console.log(`  [REQ] ${req.method()} ${req.url()}`);
      if (req.postData()) console.log(`        Body: ${req.postData().substring(0, 200)}`);
    }
  });

  page.on('response', async res => {
    const url = res.url();
    if (url.includes('GoogleAccount') || url.includes('GetAuthUrl') ||
        url.includes('GetClientByToken') || url.includes('GetClientLogins')) {
      try {
        const body = await res.json();
        console.log(`  [RES] ${res.status()} ${url.split('/').pop()}`);
        console.log(`        Body: ${JSON.stringify(body).substring(0, 300)}`);
      } catch {}
    }
  });

  // ===================================================================
  // PHASE 1: Page Discovery — What does test-social-linking look like?
  // ===================================================================
  console.log('[Phase 1] Page Discovery');
  
  await page.goto(TEST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  
  const pageTitle = await page.title();
  const pageUrl = page.url();
  console.log(`  Title: ${pageTitle}`);
  console.log(`  URL: ${pageUrl}`);
  
  await screenshot(page, '01_page_load.png');
  
  // Get full page text for discovery
  const bodyText = await page.evaluate(() => document.body.innerText);
  console.log(`  Page text (first 500 chars):\n${bodyText.substring(0, 500)}\n`);
  
  // Look for key elements
  const elementsFound = await page.evaluate(() => {
    const checks = {
      hasLinkGoogleButton: !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => b.textContent.includes('Link') && b.textContent.includes('Google')),
      hasUnlinkGoogleButton: !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => b.textContent.includes('Unlink') && b.textContent.includes('Google')),
      hasGoogleText: !!document.querySelector('body') && document.querySelector('body').innerText.includes('Google'),
      hasTelegramText: !!document.querySelector('body') && document.querySelector('body').innerText.includes('Telegram'),
      hasConnectButton: !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => b.textContent.trim() === 'Connect'),
      hasLinkButton: !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => b.textContent.includes('Link')),
      hasUnlinkButton: !!document.querySelector('button') && [...document.querySelectorAll('button')].some(b => b.textContent.includes('Unlink')),
      buttonCount: document.querySelectorAll('button').length,
      linkCount: document.querySelectorAll('a').length,
      inputCount: document.querySelectorAll('input').length,
      formCount: document.querySelectorAll('form').length,
    };
    // Get all button texts
    checks.buttonTexts = [...document.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean);
    checks.linkTexts = [...document.querySelectorAll('a')].map(a => a.textContent.trim()).filter(Boolean);
    return checks;
  });
  
  console.log(`  Elements found:`);
  console.log(`    Buttons: ${elementsFound.buttonCount}`);
  console.log(`    Links: ${elementsFound.linkCount}`);
  console.log(`    Inputs: ${elementsFound.inputCount}`);
  console.log(`    Forms: ${elementsFound.formCount}`);
  console.log(`    Has Google text: ${elementsFound.hasGoogleText}`);
  console.log(`    Has Telegram text: ${elementsFound.hasTelegramText}`);
  console.log(`    Has Link Google: ${elementsFound.hasLinkGoogleButton}`);
  console.log(`    Has Unlink Google: ${elementsFound.hasUnlinkGoogleButton}`);
  console.log(`    Button texts: ${elementsFound.buttonTexts.join(', ')}`);
  console.log(`    Link texts: ${elementsFound.linkTexts.join(', ')}`);
  
  addResult('TC4', 'Page loads & displays content', 
    elementsFound.hasGoogleText ? 'PASS' : 'PARTIAL',
    '01_page_load.png',
    `Google text: ${elementsFound.hasGoogleText}, Telegram: ${elementsFound.hasTelegramText}, Buttons: [${elementsFound.buttonTexts.join(', ')}]`
  );
  
  // ===================================================================
  // PHASE 2: Login — Need auth session for linking/unlinking
  // ===================================================================
  console.log('\n[Phase 2] Authentication');
  
  // Navigate to homepage first, then open sign-in modal
  await page.goto('https://minebit-casino.qa.sofon.one', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Click Sign Up to open the registration/login modal
  const signUpBtn = page.locator('button:has-text("Sign Up")').first();
  if (await signUpBtn.isVisible()) {
    await signUpBtn.click();
    console.log('  Clicked Sign Up button');
    await page.waitForTimeout(2000);
  }
  
  // Check if we need to switch to Sign In tab inside the modal
  const signInTab = page.locator('text=Sign In').first();
  if (await signInTab.isVisible()) {
    await signInTab.click();
    console.log('  Clicked Sign In tab');
    await page.waitForTimeout(1000);
  }
  
  const loginFormVisible = await page.getByPlaceholder('Email').first().isVisible().catch(() => false);
  console.log(`  Login form visible: ${loginFormVisible}`);
  
  if (loginFormVisible) {
    await page.getByPlaceholder('Email').fill(EMAIL);
    await page.getByPlaceholder('Password').first().fill(PASSWORD);
    console.log(`  Filled: ${EMAIL} / ********`);
    
    await screenshot(page, '02_login_filled.png');
    
    // Submit — use force:true because MuiBackdrop intercepts pointer events
    // The submit button is inside the modal, need to find it there
    const submitBtn = page.locator('button[type="submit"]').first();
    const startPlayingBtn = page.getByRole('button', { name: 'Start Playing' });
    
    if (await startPlayingBtn.count() > 0) {
      await startPlayingBtn.click({ force: true });
      console.log('  Start Playing clicked (force)');
    } else if (await submitBtn.count() > 0) {
      await submitBtn.click({ force: true });
      console.log('  Submit clicked (force)');
    } else {
      console.log('  No submit button found in modal');
    }
    await page.waitForTimeout(5000);
    
    // Check auth state
    const afterLoginUrl = page.url();
    const hasBalance = await page.getByRole('button', { name: /\$/ }).count() > 0;
    console.log(`  After login URL: ${afterLoginUrl}`);
    console.log(`  Has balance button: ${hasBalance}`);
    
    await screenshot(page, '03_after_login.png');
    
    // Navigate back to test page
    await page.goto(TEST_URL, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(3000);
    await screenshot(page, '04_test_page_authenticated.png');
    
    // Re-check elements after auth
    const authElements = await page.evaluate(() => {
      const body = document.querySelector('body').innerText;
      return {
        bodyText: body.substring(0, 1000),
        hasLinkGoogle: [...document.querySelectorAll('button, a')].some(el => el.textContent.includes('Connect')),
        hasUnlinkGoogle: [...document.querySelectorAll('button, a')].some(el => el.textContent.includes('Unlink')),
        hasGoogleText: body.includes('Google'),
        hasTelegramText: body.includes('Telegram'),
        hasConnectButton: [...document.querySelectorAll('button')].some(el => el.textContent.trim() === 'Connect'),
        buttonTexts: [...document.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean),
        linkTexts: [...document.querySelectorAll('a')].map(a => a.textContent.trim()).filter(Boolean),
      };
    });
    
    console.log(`  Auth body text: ${authElements.bodyText.substring(0, 500)}`);
    console.log(`  Auth buttons: [${authElements.buttonTexts.join(', ')}]`);
    console.log(`  Auth links: [${authElements.linkTexts.join(', ')}]`);
    console.log(`  Has Link Google: ${authElements.hasLinkGoogle}`);
    console.log(`  Has Unlink Google: ${authElements.hasUnlinkGoogle}`);
    
    addResult('TC5', '"Connect" button visible for Google (authenticated user)',
      authElements.hasLinkGoogle ? 'PASS' : 'FAIL',
      '04_test_page_authenticated.png',
      `Authenticated buttons: [${authElements.buttonTexts.join(', ')}], Google text: ${authElements.hasGoogleText}`
    );
  } else {
    console.log('  ⚠️ Login form not available — continuing without auth');
    addResult('TC5', '"Link Google" button visible', 'BLOCKED', '01_page_load.png', 'Login form not available');
    await screenshot(page, '02_no_login_form.png');
  }
  
  // ===================================================================
  // PHASE 3: Test Linking Flow (with network mock)
  // ===================================================================
  console.log('\n[Phase 3] Link Google Flow (Mocked)');
  
  // Re-navigate to test page
  await page.goto(TEST_URL, { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(2000);
  
  // Look for Google-related buttons/links
  // The page uses "Connect" buttons, not "Link Google"
  const googleConnectElements = await page.locator('button:has-text("Connect")').all();
  const googleTextElements = await page.locator('text=Google').all();
  
  console.log(`  Connect elements found: ${googleConnectElements.length}`);
  console.log(`  Google text elements: ${googleTextElements.length}`);
  
  // Find the Connect button NEXT to "Google" text
  let targetConnectBtn = null;
  for (let i = 0; i < googleConnectElements.length; i++) {
    const text = await googleConnectElements[i].textContent();
    // Skip if this Connect button is next to Telegram
    const parentText = await googleConnectElements[i].evaluate(el => {
      return el.closest('div')?.parentElement?.innerText?.substring(0, 50) || '';
    });
    console.log(`    Connect ${i+1}: parent context "${parentText}"`);
    
    if (parentText.includes('Google') && !parentText.includes('Telegram')) {
      targetConnectBtn = googleConnectElements[i];
      console.log(`    → This is the Google Connect button`);
      break;
    }
  }
  
  if (!targetConnectBtn && googleConnectElements.length >= 1) {
    // Assume first Connect is for Google (based on page layout: Google first, then Telegram)
    targetConnectBtn = googleConnectElements[0];
    console.log(`    → Using first Connect button as Google Connect`);
  }
  
  if (targetConnectBtn) {
    // Set up network mocks BEFORE clicking
    // Mock Google OAuth redirect
    await page.route('**/accounts.google.com/**', route => {
      console.log('  [MOCK] Intercepted Google OAuth redirect');
      route.fulfill({
        status: 200,
        contentType: 'text/html',
        body: '<html><body><h1>MOCK Google OAuth</h1><p>This is a mocked Google OAuth page.</p></body></html>'
      });
    });
    
    // Mock the callback endpoint
    await page.route('**/callback/google**', route => {
      console.log('  [MOCK] Intercepted Google callback');
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ success: true, linked: true })
      });
    });
    
    // Mock token exchange
    await page.route('**/oauth2/v4/token**', route => {
      console.log('  [MOCK] Intercepted token exchange');
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          access_token: 'mock-access-token',
          id_token: 'mock-id-token',
          token_type: 'Bearer',
          expires_in: 3600
        })
      });
    });
    
    // Mock GetAuthUrl endpoint
    await page.route('**/GoogleAccount/GetAuthUrl**', route => {
      const linkToken = route.request().url().includes('linkToken') ? 'TOKEN_FOUND' : 'NO_TOKEN';
      console.log(`  [MOCK] GetAuthUrl intercepted — linkToken: ${linkToken}`);
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          authUrl: 'https://accounts.google.com/o/oauth2/v2/auth?mock=redirect',
          linkToken: linkToken
        })
      });
    });
    
    await screenshot(page, '05_before_link_click.png');
    
    // Try clicking the Connect button
    try {
      const [newPage] = await Promise.all([
        context.waitForEvent('page', { timeout: 10000 }).catch(() => null),
        targetConnectBtn.click()
      ]);
      
      console.log(`  Clicked Google element`);
      
      if (newPage) {
        await newPage.waitForLoadState('domcontentloaded').catch(() => {});
        console.log(`  New page opened: ${newPage.url()}`);
        await newPage.screenshot({ path: path.join(SCREENSHOTS_DIR, '06_oauth_redirect.png'), timeout: 5000 }).catch(() => {});
      }
      
      await page.waitForTimeout(3000);
      await screenshot(page, '07_after_link_click.png');
      
      // Check for network calls to GetAuthUrl
      const getAuthUrlCalls = networkLog.filter(n => n.url.includes('GetAuthUrl'));
      console.log(`  GetAuthUrl calls: ${getAuthUrlCalls.length}`);
      if (getAuthUrlCalls.length > 0) {
        getAuthUrlCalls.forEach((c, i) => console.log(`    ${i+1}. ${c.method} ${c.url}`));
        addResult('TC6', 'GetAuthUrl called with linkToken',
          getAuthUrlCalls.some(c => c.url.includes('linkToken')) ? 'PASS' : 'FAIL',
          '07_after_link_click.png',
          `GetAuthUrl calls: ${getAuthUrlCalls.length}`
        );
      }
    } catch (err) {
      console.log(`  Click error: ${err.message.substring(0, 100)}`);
      addResult('TC6', 'OAuth redirect after clicking Link Google', 'FAIL', '05_before_link_click.png', err.message.substring(0, 200));
    }
    
    // Unmock for remaining tests
    await page.unroute('**/accounts.google.com/**');
    await page.unroute('**/callback/google**');
    await page.unroute('**/oauth2/v4/token**');
    await page.unroute('**/GoogleAccount/GetAuthUrl**');
  } else {
    addResult('TC5', 'Link Google button visible', 'FAIL', '04_test_page_authenticated.png',
      'No Google-related elements found on page');
    console.log('  No Google elements found — skipping linking flow');
  }
  
  // ===================================================================
  // PHASE 4: Test Unlinking Flow
  // ===================================================================
  console.log('\n[Phase 4] Unlink Google Flow');
  
  const unlinkElements = await page.locator('button:has-text("Unlink"), a:has-text("Unlink")').all();
  const unlinkGoogleElements = await page.locator('button:has-text("Unlink")').all();
  
  console.log(`  Unlink elements: ${unlinkElements.length}`);
  console.log(`  Unlink Google elements: ${unlinkGoogleElements.length}`);
  
  if (unlinkGoogleElements.length > 0) {
    await screenshot(page, '08_before_unlink.png');
    
    try {
      await unlinkGoogleElements[0].click();
      await page.waitForTimeout(2000);
      await screenshot(page, '09_after_unlink_click.png');
      console.log('  Unlink clicked');
      addResult('TC9', 'Unlink Google button click', 'PASS', '09_after_unlink_click.png');
    } catch (err) {
      console.log(`  Unlink error: ${err.message.substring(0, 100)}`);
      addResult('TC9', 'Unlink Google button click', 'FAIL', '08_before_unlink.png', err.message.substring(0, 200));
    }
  } else {
    addResult('TC9', 'Unlink Google available (requires linked state)', 'SKIP', '', 'No unlink elements — Google not linked');
    console.log('  No unlink elements — skipping (expected if Google not linked)');
  }
  
  // ===================================================================
  // PHASE 5: Error Cases
  // ===================================================================
  console.log('\n[Phase 5] Error Cases');
  
  // TC12: Link without auth (navigate without session)
  console.log('  [TC12] Link without auth session');
  
  // Clear cookies
  await context.clearCookies();
  await page.goto(TEST_URL, { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(3000);
  await screenshot(page, '10_no_auth_state.png');
  
  const noAuthElements = await page.evaluate(() => {
    const body = document.querySelector('body').innerText;
    return {
      hasLinkGoogle: [...document.querySelectorAll('button, a')].some(el => el.textContent.includes('Link Google')),
      hasError: body.includes('error') || body.includes('Error') || body.includes('unauthorized'),
      bodySnippet: body.substring(0, 300),
      buttonTexts: [...document.querySelectorAll('button')].map(b => b.textContent.trim()).filter(Boolean),
    };
  });
  
  console.log(`    Has Link Google (no auth): ${noAuthElements.hasLinkGoogle}`);
  console.log(`    Has error text: ${noAuthElements.hasError}`);
  console.log(`    Body: ${noAuthElements.bodySnippet}`);
  console.log(`    Buttons: [${noAuthElements.buttonTexts.join(', ')}]`);
  
  addResult('TC12', 'Link without auth — error handling',
    noAuthElements.hasError ? 'PASS' : (noAuthElements.hasLinkGoogle ? 'FAIL' : 'PARTIAL'),
    '10_no_auth_state.png',
    `Link Google visible without auth: ${noAuthElements.hasLinkGoogle}, Error text: ${noAuthElements.hasError}`
  );
  
  // ===================================================================
  // PHASE 6: Full Page Snapshot
  // ===================================================================
  console.log('\n[Phase 6] Final Evidence');
  
  // Take final full-page snapshot
  const finalBodyText = await page.evaluate(() => document.body.innerText);
  console.log(`  Final page text length: ${finalBodyText.length} chars`);
  
  // Save full body text
  fs.writeFileSync(path.join(RESULTS_DIR, 'page-content.txt'), finalBodyText);
  
  // Save console log
  fs.writeFileSync(path.join(CONSOLE_DIR, 'errors.log'), 
    consoleLog.map(e => `[${e.type}] ${e.text}`).join('\n'));
  
  // Save network log
  const apiCalls = networkLog.filter(n => 
    n.url.includes('GoogleAccount') || n.url.includes('GetAuthUrl') || 
    n.url.includes('linkToken') || n.url.includes('google') ||
    n.url.includes('GetClientByToken')
  );
  fs.writeFileSync(path.join(NETWORK_DIR, 'api-calls.json'), JSON.stringify({
    totalRequests: networkLog.length,
    apiCalls: apiCalls,
    timestamps: new Date().toISOString()
  }, null, 2));
  
  // ===================================================================
  // GENERATE REPORT
  // ===================================================================
  console.log('\n=== GENERATING REPORT ===\n');
  
  const passed = allResults.filter(r => r.status === 'PASS').length;
  const failed = allResults.filter(r => r.status === 'FAIL').length;
  const partial = allResults.filter(r => r.status === 'PARTIAL').length;
  const blocked = allResults.filter(r => r.status === 'BLOCKED').length;
  const skipped = allResults.filter(r => r.status === 'SKIP').length;
  
  const report = {
    ticket: 'CT-548',
    test: 'Google Linking & Unlinking — UI Test',
    environment: 'QA',
    url: TEST_URL,
    timestamp: new Date().toISOString(),
    runId: 'CT-548-20260318-01',
    strategy: 'Playwright Network Mocking (Option B)',
    registeredEmail: EMAIL,
    results: {
      total: allResults.length,
      passed, failed, partial, blocked, skipped,
      details: allResults
    },
    pageDiscovery: elementsFound,
    network: {
      totalRequests: networkLog.length,
      apiCalls: apiCalls.length,
      consoleErrors: consoleLog.filter(e => e.type === 'error').length,
    },
    evidence: {
      screenshots: fs.readdirSync(SCREENSHOTS_DIR).map(f => `screenshots/${f}`),
      networkLogs: fs.readdirSync(NETWORK_DIR).map(f => `network-logs/${f}`),
      consoleLogs: fs.readdirSync(CONSOLE_DIR).map(f => `console-logs/${f}`),
    }
  };
  
  fs.writeFileSync(path.join(RESULTS_DIR, 'results.json'), JSON.stringify(report, null, 2));
  
  // Markdown result file
  let md = `# CT-548 Test Results\n\n**Date:** ${new Date().toISOString()}\n**Environment:** QA\n**URL:** ${TEST_URL}\n**Tester:** Clawver\n**Strategy:** Playwright Network Mocking (Option B)\n\n## Summary\n- Total scenarios: ${allResults.length}\n- Passed: ${passed}\n- Failed: ${failed}\n- Partial: ${partial}\n- Blocked: ${blocked}\n- Skipped: ${skipped}\n\n## Detailed Results\n\n`;
  
  // Group by phase
  const phases = {
    'Page Discovery': allResults.filter(r => ['TC4'].includes(r.tc)),
    'Happy Path — Linking': allResults.filter(r => ['TC5', 'TC6', 'TC7', 'TC8'].includes(r.tc)),
    'Happy Path — Unlinking': allResults.filter(r => ['TC9', 'TC10', 'TC11'].includes(r.tc)),
    'Error Cases': allResults.filter(r => ['TC12', 'TC13', 'TC14', 'TC15'].includes(r.tc)),
    'Edge Cases': allResults.filter(r => ['TC16', 'TC17', 'TC18'].includes(r.tc)),
  };
  
  for (const [phase, items] of Object.entries(phases)) {
    if (items.length === 0) continue;
    md += `### ${phase}\n\n| # | Scenario | Status | Evidence | Notes |\n|---|----------|--------|----------|-------|\n`;
    for (const r of items) {
      md += `| ${r.tc} | ${r.scenario} | ${r.status} | ${r.evidence} | ${r.notes} |\n`;
    }
    md += '\n';
  }
  
  md += `## Page Discovery\n\n`;
  md += `- Buttons: ${elementsFound.buttonCount}\n`;
  md += `- Links: ${elementsFound.linkCount}\n`;
  md += `- Inputs: ${elementsFound.inputCount}\n`;
  md += `- Has Google text: ${elementsFound.hasGoogleText}\n`;
  md += `- Has Telegram text: ${elementsFound.hasTelegramText}\n`;
  md += `- Has Link Google button: ${elementsFound.hasLinkGoogleButton}\n`;
  md += `- Has Unlink Google button: ${elementsFound.hasUnlinkGoogleButton}\n`;
  md += `- Button texts: ${elementsFound.buttonTexts.join(', ')}\n`;
  md += `- Link texts: ${elementsFound.linkTexts.join(', ')}\n\n`;
  
  md += `## Issues Found\n\n`;
  if (failed > 0) {
    allResults.filter(r => r.status === 'FAIL').forEach(r => {
      md += `1. **${r.tc}: ${r.scenario}** — ${r.notes}\n`;
    });
  } else {
    md += 'No critical issues found.\n';
  }
  
  md += `\n## Evidence Files\n\n`;
  md += `### Screenshots\n`;
  fs.readdirSync(SCREENSHOTS_DIR).forEach(f => md += `- screenshots/${f}\n`);
  md += `\n### Network Logs\n`;
  fs.readdirSync(NETWORK_DIR).forEach(f => md += `- network-logs/${f}\n`);
  md += `\n### Console Logs\n`;
  fs.readdirSync(CONSOLE_DIR).forEach(f => md += `- console-logs/${f}\n`);
  
  fs.writeFileSync(path.join(RESULTS_DIR, 'CT-548-result.md'), md);
  
  // Console summary
  console.log('============================');
  console.log(`  Total: ${allResults.length}`);
  console.log(`  Passed: ${passed}`);
  console.log(`  Failed: ${failed}`);
  console.log(`  Partial: ${partial}`);
  console.log(`  Blocked: ${blocked}`);
  console.log(`  Skipped: ${skipped}`);
  console.log(`  Console errors: ${consoleLog.filter(e => e.type === 'error').length}`);
  console.log(`  Network requests: ${networkLog.length}`);
  console.log(`  API calls: ${apiCalls.length}`);
  console.log('============================\n');
  
  allResults.forEach(r => console.log(`  ${r.tc}: ${r.status} — ${r.scenario}`));
  
  await browser.close();
  console.log('\nDone.');
})().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
