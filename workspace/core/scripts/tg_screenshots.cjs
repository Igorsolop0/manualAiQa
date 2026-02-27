const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CHANNELS = [
  { name: 'Авточат Українці в Австрії', url: 'https://t.me/s/cKdatJS0rFU1OWQy' },
  { name: 'Австрія IT', url: 'https://t.me/s/austria_it_tg' }
];

const OUTPUT_DIR = '/Users/ihorsolopii/.openclaw/workspace/screenshots';

async function takeScreenshots() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 1200 }
  });
  
  const results = [];
  
  for (const channel of CHANNELS) {
    console.log(`\n=== Navigating to ${channel.name} ===`);
    const page = await context.newPage();
    
    try {
      await page.goto(channel.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      
      // Wait for messages to load
      await page.waitForTimeout(3000);
      
      // Take screenshot
      const screenshotPath = path.join(OUTPUT_DIR, `${channel.name.replace(/\s+/g, '_')}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: false });
      
      console.log(`Screenshot saved: ${screenshotPath}`);
      
      // Try to extract text content
      const content = await page.evaluate(() => {
        const messages = document.querySelectorAll('.tgme_channel_history, .tgme_widget_message, [class*="message"]');
        if (messages.length > 0) {
          return Array.from(messages).map(m => m.textContent).join('\n---\n');
        }
        return document.body.innerText;
      });
      
      results.push({ 
        name: channel.name, 
        path: screenshotPath, 
        content: content.substring(0, 5000),
        success: true 
      });
      
    } catch (error) {
      console.error(`Failed to capture ${channel.name}: ${error.message}`);
      results.push({ name: channel.name, error: error.message, success: false });
    }
    
    await page.close();
  }
  
  await browser.close();
  
  // Save results
  const resultsPath = path.join(OUTPUT_DIR, 'results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  console.log(`\nResults saved to: ${resultsPath}`);
}

takeScreenshots().catch(err => {
  console.error('Script failed:', err);
  process.exit(1);
});
