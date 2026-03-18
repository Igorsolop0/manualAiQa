// CT-798: WebSocket Connection Validation
// Standalone script - uses raw playwright (not @playwright/test)
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const RESULTS_DIR = '/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-798';
const QA_URL = 'https://minebit-casino.qa.sofon.one';

(async () => {
  console.log('=== CT-798: WebSocket Connection Validation ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Collect all console messages
  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push({ type: msg.type(), text: msg.text() }));
  page.on('pageerror', err => consoleLogs.push({ type: 'error', text: err.message }));
  
  // Collect WebSocket connections via CDP
  let wsConnections = [];
  let wsMessages = [];
  
  const cdpSession = await context.newCDPSession(page);
  
  // Enable Network domain to capture WebSocket frames
  await cdpSession.send('Network.enable');
  
  cdpSession.on('Network.webSocketCreated', (params) => {
    wsConnections.push({
      requestId: params.requestId,
      url: params.url,
      time: new Date().toISOString()
    });
    console.log(`  [WS] Connection created: ${params.url}`);
  });
  
  cdpSession.on('Network.webSocketFrameReceived', (params) => {
    wsMessages.push({
      requestId: params.requestId,
      timestamp: params.timestamp,
      opcode: params.response.opcode,
      mask: params.response.mask,
      payloadLength: params.response.payloadData?.length || 0,
      payloadData: params.response.payloadData?.substring(0, 200),
      direction: 'received'
    });
  });
  
  cdpSession.on('Network.webSocketFrameSent', (params) => {
    wsMessages.push({
      requestId: params.requestId,
      timestamp: params.timestamp,
      opcode: params.response.opcode,
      payloadLength: params.response.payloadData?.length || 0,
      payloadData: params.response.payloadData?.substring(0, 200),
      direction: 'sent'
    });
  });
  
  cdpSession.on('Network.webSocketClosed', (params) => {
    console.log(`  [WS] Connection closed: ${params.requestId}`);
    const conn = wsConnections.find(c => c.requestId === params.requestId);
    if (conn) conn.closed = true;
  });
  
  // Track all network requests for filtering
  const allRequests = [];
  page.on('request', req => allRequests.push({ url: req.url(), method: req.method(), resourceType: req.resourceType() }));
  page.on('response', res => {
    const req = allRequests.find(r => r.url === res.url());
    if (req) req.status = res.status();
  });

  // ===== STEP 1: Navigate to homepage =====
  console.log('[Step 1] Navigate to homepage...');
  await page.goto(QA_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.join(RESULTS_DIR, '01_homepage.png'), timeout: 5000 });
  console.log('  Screenshot: 01_homepage.png');
  console.log('  WS connections after initial load:', wsConnections.length);

  // ===== STEP 2: Register Player =====
  console.log('\n[Step 2] Register new player...');
  const timestamp = Date.now();
  const email = `test_ws_${timestamp}@test.tech`;
  const password = 'TestPassword123!';
  
  try {
    // Click Sign Up button
    await page.locator('button:has-text("Sign Up")').first().click({ timeout: 5000 });
    await page.waitForTimeout(2000);
    
    // Take screenshot of Sign Up modal
    await page.screenshot({ path: path.join(RESULTS_DIR, '02_sign_up_modal.png'), timeout: 5000 });
    console.log('  Screenshot: 02_sign_up_modal.png');
    
    // Fill registration form - use the known selectors from E2E project
    const emailInput = page.getByPlaceholder('Email');
    const passwordInput = page.getByPlaceholder('Password');
    
    await emailInput.waitFor({ state: 'visible', timeout: 10000 });
    await emailInput.fill(email);
    console.log(`  Filled email: ${email}`);
    
    await passwordInput.first().fill(password);
    console.log('  Filled password');
    
    // Check if there's a confirm password field
    const confirmInput = page.locator('input[placeholder*="confirm" i], input[name="confirmPassword"]');
    if (await confirmInput.count() > 0) {
      await confirmInput.first().fill(password);
      console.log('  Filled confirm password');
    }
    
    // Check terms checkbox if present
    const termsCheckbox = page.locator('input[type="checkbox"]').first();
    if (await termsCheckbox.count() > 0) {
      const isChecked = await termsCheckbox.isChecked();
      if (!isChecked) {
        await termsCheckbox.check();
        console.log('  Checked terms checkbox');
      }
    }
    
    await page.screenshot({ path: path.join(RESULTS_DIR, '03_form_filled.png'), timeout: 5000 });
    console.log('  Screenshot: 03_form_filled.png');
    
    // Submit registration
    const submitBtn = page.locator('button[type="submit"], button:has-text("Sign Up"), button:has-text("Create Account"), button:has-text("Start Playing")').first();
    await submitBtn.click({ timeout: 5000 });
    console.log('  Submit clicked');
    
    // Wait for response
    await page.waitForLoadState('domcontentloaded', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: path.join(RESULTS_DIR, '04_after_registration.png'), timeout: 5000 });
    console.log('  Screenshot: 04_after_registration.png');
    console.log(`  Current URL: ${page.url()}`);
    
  } catch (err) {
    console.log(`  Registration error: ${err.message.substring(0, 100)}`);
    await page.screenshot({ path: path.join(RESULTS_DIR, '04_registration_error.png'), timeout: 5000 }).catch(() => {});
    
    // Fallback: try via API registration
    console.log('  Trying API registration as fallback...');
    try {
      const registerResponse = await page.evaluate(async ({ email, password }) => {
        const res = await fetch('/graphql', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: `mutation Register($input: RegisterInput!) {
              registerPlayer(input: $input) {
                id
                email
                token
              }
            }`,
            variables: {
              input: { email, password, currency: 'USD' }
            }
          })
        });
        return await res.json();
      }, { email, password });
      
      console.log('  API registration result:', JSON.stringify(registerResponse).substring(0, 200));
      
      if (registerResponse?.data?.registerPlayer?.token) {
        console.log('  Player registered via API, setting cookie...');
        const token = registerResponse.data.registerPlayer.token;
        await context.addCookies([{
          name: 'token',
          value: token,
          domain: 'minebit-casino.qa.sofon.one',
          path: '/'
        }]);
        await page.goto(QA_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);
        await page.screenshot({ path: path.join(RESULTS_DIR, '04_after_api_registration.png'), timeout: 5000 });
        console.log('  Screenshot: 04_after_api_registration.png');
      }
    } catch (apiErr) {
      console.log(`  API registration also failed: ${apiErr.message.substring(0, 100)}`);
    }
  }

  // ===== STEP 3: Monitor WebSocket connections =====
  console.log('\n[Step 3] Monitor WebSocket connections...');
  console.log(`  WS connections so far: ${wsConnections.length}`);
  for (const ws of wsConnections) {
    console.log(`    - ${ws.url} (closed: ${ws.closed || false})`);
  }

  // ===== STEP 4: Refresh and capture =====
  console.log('\n[Step 4] Refresh page and monitor...');
  
  // Reset counters before refresh
  const wsBeforeRefresh = wsConnections.length;
  const msgsBeforeRefresh = wsMessages.length;
  
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000); // Wait for WS to establish
  
  const newWs = wsConnections.length - wsBeforeRefresh;
  const newMsgs = wsMessages.length - msgsBeforeRefresh;
  
  console.log(`  New WS connections after refresh: ${newWs}`);
  console.log(`  New WS messages after refresh: ${newMsgs}`);
  
  await page.screenshot({ path: path.join(RESULTS_DIR, '05_after_refresh.png'), timeout: 5000 });
  console.log('  Screenshot: 05_after_refresh.png');
  
  // Wait more to capture any delayed WS messages
  console.log('  Waiting 5 more seconds for WS activity...');
  await page.waitForTimeout(5000);
  
  const finalNewMsgs = wsMessages.length - msgsBeforeRefresh;
  console.log(`  Total new messages after 10s wait: ${finalNewMsgs}`);

  // ===== STEP 5: Find Recent Winners =====
  console.log('\n[Step 5] Find Recent Winners element...');
  
  let recentWinnersFound = false;
  let recentWinnersData = null;
  
  // Try the data-cp selector from the task
  const recentWinnersEl = page.locator('[data-cp="cmVjZW50V2lubmVyR3JpZENvbnRhaW5lclByb3Bz"]');
  if (await recentWinnersEl.count() > 0) {
    recentWinnersFound = true;
    console.log('  Found Recent Winners via data-cp selector');
    
    // Get text content
    recentWinnersData = await recentWinnersEl.first().textContent();
    console.log(`  Content: ${recentWinnersData?.substring(0, 100)}`);
    
    await recentWinnersEl.first().screenshot({ path: path.join(RESULTS_DIR, '06_recent_winners.png') });
    console.log('  Screenshot: 06_recent_winners.png');
  }
  
  // Also try swiper-slide approach
  if (!recentWinnersFound) {
    const swiperSlides = page.locator('.swiper-slide');
    const slideCount = await swiperSlides.count();
    console.log(`  Swiper slides found: ${slideCount}`);
    
    for (let i = 0; i < Math.min(slideCount, 5); i++) {
      const text = await swiperSlides.nth(i).textContent();
      if (text && (text.includes('USD') || text.includes('@') || text.includes('Winner'))) {
        console.log(`  Slide ${i}: ${text?.substring(0, 80)}`);
      }
    }
  }
  
  // Wait 5 seconds and check for updates
  console.log('  Waiting 5s to observe updates...');
  await page.waitForTimeout(5000);
  
  if (recentWinnersFound) {
    await recentWinnersEl.first().screenshot({ path: path.join(RESULTS_DIR, '07_recent_winners_updated.png') });
    console.log('  Screenshot: 07_recent_winners_updated.png');
    
    const updatedData = await recentWinnersEl.first().textContent();
    console.log(`  Updated content: ${updatedData?.substring(0, 100)}`);
    console.log(`  Content changed: ${recentWinnersData !== updatedData ? 'YES (live updates working!)' : 'NO'}`);
  }

  // Also take full page screenshot showing Recent Winners area
  await page.screenshot({ path: path.join(RESULTS_DIR, '06_full_page_recent_winners.png'), timeout: 5000 });
  console.log('  Screenshot: 06_full_page_recent_winners.png');

  // ===== STEP 6: Console check =====
  console.log('\n[Step 6] Console check...');
  const wsConsoleErrors = consoleLogs.filter(l => 
    l.text.toLowerCase().includes('websocket') || 
    l.text.toLowerCase().includes('socket') ||
    l.text.toLowerCase().includes('ws:')
  );
  const allErrors = consoleLogs.filter(l => l.type === 'error');
  
  console.log(`  Total console entries: ${consoleLogs.length}`);
  console.log(`  Total errors: ${allErrors.length}`);
  console.log(`  WebSocket-related errors: ${wsConsoleErrors.length}`);
  
  if (wsConsoleErrors.length > 0) {
    wsConsoleErrors.forEach((e, i) => console.log(`    ${i+1}. ${e.text.substring(0, 100)}`));
  }
  
  // Save console log
  fs.writeFileSync(
    path.join(RESULTS_DIR, 'console-log.txt'),
    consoleLogs.map(l => `[${l.type}] ${l.text}`).join('\n')
  );

  // ===== STEP 7: Network log =====
  console.log('\n[Step 7] Network log...');
  const wsRequests = allRequests.filter(r => r.resourceType === 'websocket');
  const apiRequests = allRequests.filter(r => r.url.includes('graphql') || r.url.includes('api'));
  
  console.log(`  Total requests: ${allRequests.length}`);
  console.log(`  WebSocket requests: ${wsRequests.length}`);
  console.log(`  API requests: ${apiRequests.length}`);
  
  if (wsRequests.length > 0) {
    wsRequests.forEach((r, i) => console.log(`    WS ${i+1}: ${r.url} (${r.status || 'N/A'})`));
  }
  
  // Save network log
  fs.writeFileSync(
    path.join(RESULTS_DIR, 'network-log.json'),
    JSON.stringify({
      websocket: wsRequests,
      api: apiRequests.map(r => ({ url: r.url, method: r.method, status: r.status })),
      total: allRequests.length
    }, null, 2)
  );

  // ===== GENERATE REPORT =====
  console.log('\n=== GENERATING REPORT ===\n');
  
  const wsFound = wsConnections.length > 0;
  
  const report = {
    ticket: 'CT-798',
    test: 'WebSocket Connection Validation',
    environment: 'QA',
    url: QA_URL,
    timestamp: new Date().toISOString(),
    runId: 'CT-798-20260318-01',
    
    results: {
      websocketConnectionFound: wsFound,
      websocketConnections: wsConnections.map(c => ({
        url: c.url,
        closed: c.closed || false,
        time: c.time
      })),
      websocketMessages: {
        total: wsMessages.length,
        sent: wsMessages.filter(m => m.direction === 'sent').length,
        received: wsMessages.filter(m => m.direction === 'received').length,
        sampleFrames: wsMessages.slice(0, 10)
      },
      recentWinnersFound: recentWinnersFound,
      recentWinnersData: recentWinnersData?.substring(0, 200),
      consoleErrors: allErrors.length,
      wsConsoleErrors: wsConsoleErrors.length,
      totalRequests: allRequests.length,
      registeredEmail: email
    },
    
    summary: {
      wsConnectionExists: wsFound ? 'Y' : 'N',
      recentWinnersExists: recentWinnersFound ? 'Y' : 'N',
      overallStatus: wsFound ? 'PASS' : 'FAIL'
    }
  };
  
  fs.writeFileSync(path.join(RESULTS_DIR, 'results.json'), JSON.stringify(report, null, 2));
  
  // Console summary
  console.log('============================');
  console.log('  WS CONNECTION FOUND: ' + (wsFound ? 'YES ✅' : 'NO ❌'));
  console.log('  WS URLs:');
  wsConnections.forEach(c => console.log(`    ${c.url}`));
  console.log('  WS Messages: ' + wsMessages.length);
  console.log('  Recent Winners: ' + (recentWinnersFound ? 'Found ✅' : 'Not found ❌'));
  console.log('  Console Errors: ' + allErrors.length);
  console.log('  Total Requests: ' + allRequests.length);
  console.log('============================\n');
  
  console.log('Files saved:');
  console.log(`  ${RESULTS_DIR}/results.json`);
  console.log(`  ${RESULTS_DIR}/console-log.txt`);
  console.log(`  ${RESULTS_DIR}/network-log.json`);
  console.log(`  ${RESULTS_DIR}/01_homepage.png`);
  console.log(`  ${RESULTS_DIR}/02_sign_up_modal.png`);
  console.log(`  ${RESULTS_DIR}/03_form_filled.png`);
  console.log(`  ${RESULTS_DIR}/04_after_registration.png`);
  console.log(`  ${RESULTS_DIR}/05_after_refresh.png`);
  console.log(`  ${RESULTS_DIR}/06_recent_winners.png`);
  console.log(`  ${RESULTS_DIR}/06_full_page_recent_winners.png`);
  
  await browser.close();
  console.log('\nDone.');
})().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
