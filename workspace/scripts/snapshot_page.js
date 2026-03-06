const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  // Open Minebit site
  await page.goto('https://minebit-casino.prod.sofon.one/');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: '/Users/ihorsolopii/.openclaw/workspace/shared/minebit_page.png', fullPage: true });

  // Get page content
  const html = await page.content();
  const fs = require('fs');
  fs.writeFileSync('/Users/ihorsolopii/.openclaw/workspace/shared/minebit_page.html', html);

  console.log('Screenshot saved to /Users/ihorsolopii/.openclaw/workspace/shared/minebit_page.png');
  console.log('HTML saved to /Users/ihorsolopii/.openclaw/workspace/shared/minebit_page.html');

  await browser.close();
})();
