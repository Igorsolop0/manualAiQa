// Playwright Mobile Device Emulation Examples
// Run with: node mobile_devices.js

const { chromium, webkit, devices } = require('playwright');

// Device configurations
const pixel7 = devices['Pixel 7'];
const iPhone14 = devices['iPhone 14'];

async function testPixel7() {
  console.log('📱 Testing Pixel 7 (Chrome/Android)...');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    ...pixel7,
    locale: 'en-US',
    timezoneId: 'America/New_York'
  });
  
  const page = await context.newPage();
  await page.goto('https://www.google.com');
  
  console.log(`  Device: ${pixel7.userAgent}`);
  console.log(`  Viewport: ${pixel7.viewport.width}x${pixel7.viewport.height}`);
  console.log(`  Device Scale Factor: ${pixel7.deviceScaleFactor}`);
  console.log(`  Is Mobile: ${pixel7.isMobile}`);
  console.log(`  Has Touch: ${pixel7.hasTouch}`);
  
  await page.screenshot({ path: 'pixel7-test.png' });
  console.log('  ✅ Screenshot saved: pixel7-test.png');
  
  await browser.close();
}

async function testiPhone() {
  console.log('\n📱 Testing iPhone 14 (Safari/WebKit)...');
  
  const browser = await webkit.launch({ headless: false });
  const context = await browser.newContext({
    ...iPhone14,
    locale: 'en-US',
    timezoneId: 'America/New_York'
  });
  
  const page = await context.newPage();
  await page.goto('https://www.apple.com');
  
  console.log(`  Device: ${iPhone14.userAgent}`);
  console.log(`  Viewport: ${iPhone14.viewport.width}x${iPhone14.viewport.height}`);
  console.log(`  Device Scale Factor: ${iPhone14.deviceScaleFactor}`);
  console.log(`  Is Mobile: ${iPhone14.isMobile}`);
  console.log(`  Has Touch: ${iPhone14.hasTouch}`);
  
  await page.screenshot({ path: 'iphone-test.png' });
  console.log('  ✅ Screenshot saved: iphone-test.png');
  
  await browser.close();
}

// List all available devices
function listDevices() {
  console.log('\n📋 Available Mobile Devices:\n');
  
  const deviceList = Object.keys(devices).filter(name => 
    name.includes('Pixel') || 
    name.includes('iPhone') || 
    name.includes('Galaxy') ||
    name.includes('iPad')
  );
  
  deviceList.forEach(device => {
    console.log(`  • ${device}`);
  });
}

// Run tests
(async () => {
  listDevices();
  await testPixel7();
  await testiPhone();
  
  console.log('\n✅ All mobile device tests completed!');
})();
