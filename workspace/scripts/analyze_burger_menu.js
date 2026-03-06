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

  // Take snapshot
  const burgerMenu = await page.locator('button[aria-label*="menu"], button[aria-label*="Menu"], .burger, .hamburger, [data-testid*="menu"]').first();
  console.log('Burger menu element:', await burgerMenu.evaluate(el => ({
    tagName: el.tagName,
    className: el.className,
    ariaLabel: el.getAttribute('aria-label'),
    dataTestId: el.getAttribute('data-testid'),
    id: el.id,
    innerHTML: el.innerHTML.substring(0, 200)
  })));

  // Save selectors
  const selectors = {
    burgerMenu: {
      primary: 'button[aria-label*="menu"], button[aria-label*="Menu"]',
      fallback: '.burger, .hamburger, [data-testid*="menu"]',
      elementType: 'button',
      description: 'Icon to open side panel'
    },
    googlePlayButton: {
      primary: 'a[href*="play.google.com"], button:has-text("Google Play"), a:has-text("Get it on Google Play")',
      fallback: '.google-play, [data-testid*="google-play"]',
      elementType: 'a',
      description: 'Button to navigate to Google Play Store'
    }
  };

  const fs = require('fs');
  const path = '/Users/ihorsolopii/.openclaw/workspace/shared/UI_ELEMENTS.md';
  const content = `# UI Elements - Minebit Burger Menu & Google Play Button

Generated: ${new Date().toISOString()}

## 1. Burger Menu Icon

\`\`\`json
${JSON.stringify(selectors.burgerMenu, null, 2)}
\`\`\`

## 2. Google Play Button

\`\`\`json
${JSON.stringify(selectors.googlePlayButton, null, 2)}
\`\`\`

## Full Selectors Object

\`\`\`json
${JSON.stringify(selectors, null, 2)}
\`\`\`
`;

  if (!fs.existsSync('/Users/ihorsolopii/.openclaw/workspace/shared')) {
    fs.mkdirSync('/Users/ihorsolopii/.openclaw/workspace/shared', { recursive: true });
  }
  fs.writeFileSync(path, content);
  console.log(`Selectors saved to ${path}`);

  await browser.close();
})();
