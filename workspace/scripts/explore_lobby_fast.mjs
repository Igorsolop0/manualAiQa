import { chromium } from 'playwright';

async function exploreLobbyFast() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('🌐 Opening https://minebit-casino.prod.sofon.one/ (no wait)...');
  await page.goto('https://minebit-casino.prod.sofon.one/', { timeout: 30000, waitUntil: 'commit' });

  // Wait for body to be present
  await page.waitForSelector('body', { timeout: 10000 });
  console.log('✅ Page body loaded');

  // Small wait for React/initial render
  await page.waitForTimeout(2000);

  // Take screenshot
  await page.screenshot({ path: '/tmp/minebit-lobby-fast.png', fullPage: false });
  console.log('✅ Screenshot saved');

  // Extract all data attributes using page.evaluate
  console.log('\n🔍 Extracting data attributes...\n');

  const dataElements = await page.evaluate(() => {
    const result = [];

    // Collect all elements with data attributes
    const all = document.querySelectorAll('*');
    all.forEach(el => {
      const dataAttrs = {};

      for (let attr of el.attributes) {
        if (attr.name.startsWith('data-')) {
          dataAttrs[attr.name] = attr.value;
        }
      }

      if (Object.keys(dataAttrs).length > 0) {
        const tagName = el.tagName.toLowerCase();
        const textContent = (el.textContent || '').trim().substring(0, 40);
        const className = el.className ? (el.className.toString() || '') : '';
        const id = el.id || '';

        result.push({
          tag: tagName,
          id: id,
          className: className.substring(0, 50),
          dataAttrs: dataAttrs,
          text: textContent
        });
      }
    });

    return result;
  });

  console.log(`📊 Found ${dataElements.length} elements with data-* attributes`);

  // Group and find important elements
  const important = {};

  // Find key elements by patterns
  dataElements.forEach(el => {
    const { dataAttrs, tag, id, className, text } = el;

    // Login button
    if (dataAttrs['data-testid']?.toLowerCase().includes('login') ||
        text.toLowerCase().includes('log in')) {
      if (!important.login_btn) {
        important.login_btn = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("Log in")`,
          description: 'Login button in header'
        };
      }
    }

    // Sign up button
    if (dataAttrs['data-testid']?.toLowerCase().includes('signup') ||
        text.toLowerCase().includes('sign up')) {
      if (!important.sign_up_btn) {
        important.sign_up_btn = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("Sign up")`,
          description: 'Sign up button in header'
        };
      }
    }

    // Menu button
    if (dataAttrs['data-testid']?.toLowerCase().includes('menu') ||
        dataAttrs['data-testid']?.toLowerCase().includes('hamburger') ||
        id.toLowerCase().includes('menu') ||
        id.toLowerCase().includes('hamburger')) {
      if (!important.menu_toggle) {
        important.menu_toggle = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `#${id}`,
          description: 'Menu toggle button (opens sidebar)'
        };
      }
    }

    // Language switcher
    if (dataAttrs['data-testid']?.toLowerCase().includes('language') ||
        dataAttrs['data-testid']?.toLowerCase().includes('lang') ||
        id.toLowerCase().includes('language')) {
      if (!important.language_switcher) {
        important.language_switcher = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `#${id}`,
          description: 'Language switcher dropdown'
        };
      }
    }

    // Games categories
    if (dataAttrs['data-organism']?.toLowerCase().includes('game') ||
        dataAttrs['data-testid']?.toLowerCase().includes('category') ||
        text === 'Slots' || text === 'Live' || text === 'New' || text === 'All') {
      if (text === 'Slots' && !important.games_category_slots) {
        important.games_category_slots = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("Slots")`,
          description: 'Games category - Slots'
        };
      }
      if (text === 'Live' && !important.games_category_live) {
        important.games_category_live = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("Live")`,
          description: 'Games category - Live Casino'
        };
      }
      if (text === 'New' && !important.games_category_new) {
        important.games_category_new = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("New")`,
          description: 'Games category - New Games'
        };
      }
      if (text === 'All' && !important.games_category_all) {
        important.games_category_all = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `${tag}:has-text("All")`,
          description: 'Games category - All Games'
        };
      }
    }

    // Hero banner
    if (dataAttrs['data-organism']?.toLowerCase().includes('hero') ||
        dataAttrs['data-organism']?.toLowerCase().includes('banner') ||
        dataAttrs['data-testid']?.toLowerCase().includes('hero')) {
      if (!important.hero_banner) {
        important.hero_banner = {
          selector: dataAttrs['data-organism'] ? `[data-organism="${dataAttrs['data-organism']}"]` : dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `.hero-banner`,
          description: 'Hero banner/carousel section'
        };
      }
    }

    // Games grid
    if (dataAttrs['data-organism']?.toLowerCase().includes('gamegrid') ||
        dataAttrs['data-organism']?.toLowerCase().includes('game-grid') ||
        id.toLowerCase().includes('game-grid') ||
        className.toLowerCase().includes('game-grid')) {
      if (!important.games_grid) {
        important.games_grid = {
          selector: dataAttrs['data-organism'] ? `[data-organism="${dataAttrs['data-organism']}"]` : id ? `#${id}` : '.game-grid',
          description: 'Main games grid container'
        };
      }
    }

    // Game card
    if (dataAttrs['data-organism']?.toLowerCase().includes('gamecard') ||
        className.toLowerCase().includes('game-card')) {
      if (!important.game_card) {
        important.game_card = {
          selector: dataAttrs['data-organism'] ? `[data-organism="${dataAttrs['data-organism']}"]` : '.game-card',
          description: 'Single game card'
        };
      }
    }

    // Search input
    if (tag === 'input' && (id.toLowerCase().includes('search') || dataAttrs['data-testid']?.toLowerCase().includes('search'))) {
      if (!important.search_input) {
        important.search_input = {
          selector: dataAttrs['data-testid'] ? `[data-testid="${dataAttrs['data-testid']}"]` : `#${id}`,
          description: 'Games search input field'
        };
      }
    }
  });

  // Print found elements
  console.log('\n=== CRITICAL ELEMENTS FOUND ===\n');
  for (const [key, val] of Object.entries(important)) {
    console.log(`✅ ${key}: ${val.selector}`);
  }

  // Print all data-testid and data-organism values found
  console.log('\n=== ALL data-testid VALUES ===\n');
  const testids = [...new Set(dataElements.map(e => e.dataAttrs['data-testid']).filter(Boolean))].sort();
  testids.forEach(tid => console.log(`  - ${tid}`));

  console.log('\n=== ALL data-organism VALUES ===\n');
  const organisms = [...new Set(dataElements.map(e => e.dataAttrs['data-organism']).filter(Boolean))].sort();
  organisms.forEach(org => console.log(`  - ${org}`));

  await browser.close();

  // Build final JSON
  const result = {
    page_name: 'Lobby',
    url_pattern: '/',
    last_updated: new Date().toISOString().split('T')[0],
    elements: important,
    known_behaviors: [
      'Page renders with React/Next.js (dynamic content)',
      'Uses data-testid and data-organism attributes for testability'
    ]
  };

  return result;
}

// Run and export
exploreLobbyFast().then(result => {
  console.log('\n' + '='.repeat(60));
  console.log('📋 FINAL JSON OUTPUT:');
  console.log('='.repeat(60));
  console.log(JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});
