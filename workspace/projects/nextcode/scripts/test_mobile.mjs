// Mobile Device Test - Standalone Script
// Run with: npx playwright mobile-test.mjs

import { chromium, webkit, devices } from 'playwright';

console.log('📱 Playwright Mobile Device Emulation Test\n');

// List available devices
console.log('Available devices:');
['Pixel 7', 'Pixel 5', 'Galaxy S5', 'iPhone 14', 'iPhone 13', 'iPhone 12', 'iPad Pro'].forEach(device => {
  if (devices[device]) {
    console.log(`  ✅ ${device}`);
  }
});

console.log('\n---\n');

// Test Pixel 7 with Chromium
async function testPixel7() {
  console.log('📱 Testing Pixel 7 (Chrome/Android)...');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ...devices['Pixel 7']
  });
  
  const page = await context.newPage();
  await page.goto('https://www.example.com');
  
  const title = await page.title();
  console.log(`  Title: ${title}`);
  console.log(`  Viewport: ${devices['Pixel 7'].viewport.width}x${devices['Pixel 7'].viewport.height}`);
  console.log(`  User Agent: ${devices['Pixel 7'].userAgent.substring(0, 50)}...`);
  
  await browser.close();
  console.log('  ✅ Pixel 7 test passed\n');
}

// Test iPhone 14 with WebKit
async function testiPhone() {
  console.log('📱 Testing iPhone 14 (Safari/WebKit)...');
  
  const browser = await webkit.launch({ headless: true });
  const context = await browser.newContext({
    ...devices['iPhone 14']
  });
  
  const page = await context.newPage();
  await page.goto('https://www.example.com');
  
  const title = await page.title();
  console.log(`  Title: ${title}`);
  console.log(`  Viewport: ${devices['iPhone 14'].viewport.width}x${devices['iPhone 14'].viewport.height}`);
  console.log(`  User Agent: ${devices['iPhone 14'].userAgent.substring(0, 50)}...`);
  
  await browser.close();
  console.log('  ✅ iPhone 14 test passed\n');
}

// Run tests
await testPixel7();
await testiPhone();

console.log('✅ All mobile device tests completed successfully!');
