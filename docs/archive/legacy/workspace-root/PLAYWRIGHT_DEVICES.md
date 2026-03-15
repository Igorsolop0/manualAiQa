# Playwright Mobile Device Emulation

## ✅ Installed & Tested

**Browsers:**
- Chromium 1208 ✅
- WebKit 2248 ✅ (Safari engine)
- Firefox ❌ (not installed)

**Mobile Devices:**
- Pixel 7 (Android/Chrome) ✅
- iPhone 14 (iOS/Safari) ✅
- Pixel 5, Galaxy S5, iPhone 12, iPhone 13 ✅
- iPad Pro ✅

## 🚀 Quick Test

```bash
cd /Users/ihorsolopii/.openclaw/workspace/scripts
node test_mobile.mjs
```

## 📝 Usage Examples

### Pixel 7 (Chrome/Android)
```javascript
import { chromium, devices } from 'playwright';

const browser = await chromium.launch({ headless: false });
const context = await browser.newContext({
  ...devices['Pixel 7']
});
const page = await context.newPage();
await page.goto('https://example.com');
```

### iPhone 14 (Safari/WebKit)
```javascript
import { webkit, devices } from 'playwright';

const browser = await webkit.launch({ headless: false });
const context = await browser.newContext({
  ...devices['iPhone 14']
});
const page = await context.newPage();
await page.goto('https://example.com');
```

## 🔧 Device Specifications

**Pixel 7:**
- Viewport: 412x839
- Device Scale Factor: 2.625
- User Agent: Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36

**iPhone 14:**
- Viewport: 390x664
- Device Scale Factor: 3
- User Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15

## 📂 Files

- `test_mobile.mjs` - Standalone test script
- `mobile_devices.js` - Example with screenshots
- `mobile_test.spec.js` - Playwright Test format

## 🎯 Next Steps

Run tests:
```bash
npx playwright test mobile_test.spec.js
```

Install Firefox (optional):
```bash
npx playwright install firefox
```
