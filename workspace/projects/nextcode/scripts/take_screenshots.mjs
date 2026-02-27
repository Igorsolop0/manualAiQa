#!/usr/bin/env node
import puppeteer from 'puppeteer';
import { setTimeout as sleep } from 'timers/promises';
import fs from 'fs';
import path from 'path';

const CHANNELS = [
  { name: 'Авточат Українці в Австрії', url: 'https://t.me/cKdatJS0rFU1OWQy' },
  { name: 'Австрія IT', url: 'https://t.me/austria_it_tg' }
];

const OUTPUT_DIR = '/Users/ihorsolopii/.openclaw/workspace/screenshots';

async function takeScreenshots() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const results = [];
  
  for (const channel of CHANNELS) {
    console.log(`Navigating to ${channel.name}...`);
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 2000 });
    
    try {
      await page.goto(channel.url, { waitUntil: 'networkidle2', timeout: 30000 });
      await sleep(3000); // Wait for content to load
      
      const screenshotPath = path.join(OUTPUT_DIR, `${channel.name.replace(/\s+/g, '_')}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: false });
      
      console.log(`Screenshot saved: ${screenshotPath}`);
      results.push({ name: channel.name, path: screenshotPath, success: true });
    } catch (error) {
      console.error(`Failed to capture ${channel.name}: ${error.message}`);
      results.push({ name: channel.name, error: error.message, success: false });
    }
    
    await page.close();
  }
  
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
}

takeScreenshots().catch(console.error);
