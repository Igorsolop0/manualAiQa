import { chromium } from 'playwright';

async function exploreLobbyDetailed() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  console.log('🌐 Opening https://minebit-casino.prod.sofon.one/ ...');
  await page.goto('https://minebit-casino.prod.sofon.one/', { waitUntil: 'load', timeout: 60000 });

  // Wait a bit for dynamic content
  console.log('⏳ Waiting for dynamic content...');
  await page.waitForTimeout(3000);

  // Scroll to trigger lazy loading
  console.log('📜 Scrolling page for lazy loading...');
  await page.evaluate(() => {
    window.scrollTo(0, 500);
  });
  await page.waitForTimeout(1000);

  await page.evaluate(() => {
    window.scrollTo(0, 1500);
  });
  await page.waitForTimeout(1000);

  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });
  await page.waitForTimeout(1000);

  // Scroll back to top
  await page.evaluate(() => {
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(2000);

  // Full-page screenshot
  await page.screenshot({ path: '/tmp/minebit-lobby-detailed.png', fullPage: true });
  console.log('✅ Full-page screenshot saved to /tmp/minebit-lobby-detailed.png');

  // Extract all data-* attributes from the page
  console.log('\n🔍 Extracting data attributes...\n');

  const dataElements = await page.evaluate(() => {
    const result = [];

    // Helper to collect elements with data attributes
    function collectDataElements(root = document.body) {
      const all = root.querySelectorAll('*');
      all.forEach(el => {
        const dataAttrs = {};
        let hasDataAttr = false;

        // Check all data-* attributes
        for (let attr of el.attributes) {
          if (attr.name.startsWith('data-')) {
            dataAttrs[attr.name] = attr.value;
            hasDataAttr = true;
          }
        }

        if (hasDataAttr) {
          const tagName = el.tagName.toLowerCase();
          const textContent = el.textContent?.trim().substring(0, 50) || '';
          const className = el.className || '';
          const id = el.id || '';

          result.push({
            tag: tagName,
            id: id,
            className: className,
            dataAttrs: dataAttrs,
            text: textContent
          });
        }
      });

      return result;
    }

    return collectDataElements();
  });

  console.log(`📊 Found ${dataElements.length} elements with data-* attributes`);
  console.log('\n=== KEY ELEMENTS WITH DATA ATTRIBUTES ===\n');

  // Group by data-testid and data-organism
  const byTestid = {};
  const byOrganism = {};

  dataElements.forEach(el => {
    if (el.dataAttrs['data-testid']) {
      const tid = el.dataAttrs['data-testid'];
      if (!byTestid[tid]) {
        byTestid[tid] = [];
      }
      byTestid[tid].push(el);
    }

    if (el.dataAttrs['data-organism']) {
      const org = el.dataAttrs['data-organism'];
      if (!byOrganism[org]) {
        byOrganism[org] = [];
      }
      byOrganism[org].push(el);
    }
  });

  // Print data-testid findings
  if (Object.keys(byTestid).length > 0) {
    console.log('🎯 data-testid elements:');
    for (const [tid, elements] of Object.entries(byTestid)) {
      const el = elements[0];
      console.log(`  - ${tid}: <${el.tag}> text="${el.text.substring(0, 30)}"`);
    }
  }

  // Print data-organism findings
  if (Object.keys(byOrganism).length > 0) {
    console.log('\n🧬 data-organism elements:');
    for (const [org, elements] of Object.entries(byOrganism)) {
      const el = elements[0];
      console.log(`  - ${org}: <${el.tag}> text="${el.text.substring(0, 30)}" count=${elements.length}`);
    }
  }

  // Save raw data to file for analysis
  const fs = await import('fs');
  fs.writeFileSync('/tmp/minebit-lobby-data-elements.json', JSON.stringify(dataElements, null, 2));
  console.log('\n💾 Raw data saved to /tmp/minebit-lobby-data-elements.json');

  // Build Page Objects JSON based on findings
  const elements = {};

  // Helper: create element entry
  function createElement(name, strategies, description) {
    for (const strat of strategies) {
      const found = dataElements.find(el => {
        // Check if selector matches any element
        return el.dataAttrs['data-testid'] === strat.replace('[data-testid="', '').replace('"]', '') ||
               el.dataAttrs['data-organism'] === strat.replace('[data-organism="', '').replace('"]', '') ||
               el.dataAttrs['data-testid'] === strat;
      });

      if (found) {
        console.log(`✅ ${name}: ${strat}`);
        elements[name] = {
          selector: strat,
          description: description
        };
        return;
      }
    }
    console.log(`❌ ${name}: not found`);
  }

  console.log('\n=== BUILDING PAGE OBJECTS ===\n');

  // HEADER ELEMENTS
  createElement('login_btn',
    ['loginButton', 'btn-login', '[data-testid="loginButton"]'],
    'Login button in header'
  );

  createElement('sign_up_btn',
    ['signUpButton', 'btn-signup', '[data-testid="signUpButton"]'],
    'Sign up button in header'
  );

  createElement('menu_toggle',
    ['menuButton', 'hamburger', '[data-testid="menuButton"]'],
    'Menu toggle button (opens sidebar)'
  );

  createElement('language_switcher',
    ['languageSwitcher', 'lang-selector', '[data-testid="languageSwitcher"]'],
    'Language switcher dropdown'
  );

  // SIDEBAR / NAVIGATION
  createElement('sidebar',
    ['sidebar', 'navigation', '[data-testid="sidebar"]'],
    'Sidebar navigation panel'
  );

  createElement('games_category_all',
    ['category-all', 'nav-all-games', 'All games'],
    'Games category - All Games'
  );

  createElement('games_category_slots',
    ['category-slots', 'nav-slots', 'Slots'],
    'Games category - Slots'
  );

  createElement('games_category_live',
    ['category-live', 'nav-live', 'Live'],
    'Games category - Live Casino'
  );

  createElement('games_category_new',
    ['category-new', 'nav-new', 'New'],
    'Games category - New Games'
  );

  // HERO BANNER
  createElement('hero_banner',
    ['heroBanner', 'hero-slider', '[data-organism="HeroBanner"]'],
    'Hero banner/carousel section'
  );

  createElement('hero_next_btn',
    ['heroNext', 'hero-next', 'swiper-button-next'],
    'Hero banner - Next slide button'
  );

  createElement('hero_prev_btn',
    ['heroPrev', 'hero-prev', 'swiper-button-prev'],
    'Hero banner - Previous slide button'
  );

  // GAMES
  createElement('games_grid',
    ['gamesGrid', 'game-grid', '[data-organism="GamesGrid"]'],
    'Main games grid container'
  );

  createElement('game_card',
    ['gameCard', 'game-card', '[data-organism="GameCard"]'],
    'Single game card'
  );

  createElement('search_input',
    ['searchInput', 'game-search', 'input[type="search"]'],
    'Games search input field'
  );

  // FOOTER
  createElement('footer',
    ['footer', '[data-testid="footer"]'],
    'Footer section'
  );

  createElement('footer_license_link',
    ['license-link', 'footer-license', 'a:has-text("License")'],
    'License/Gambling Commission link'
  );

  createElement('footer_terms_link',
    ['terms-link', 'footer-terms', 'a:has-text("Terms")'],
    'Terms & Conditions link'
  );

  // Check for additional unique selectors found
  console.log('\n=== ADDITIONAL UNIQUE SELECTORS FOUND ===\n');
  const uniqueIds = new Set();
  dataElements.forEach(el => {
    if (el.id && !el.id.startsWith('_') && !uniqueIds.has(el.id)) {
      uniqueIds.add(el.id);
      console.log(`  #${el.id}: <${el.tag}> "${el.text.substring(0, 30)}"`);
    }
  });

  // Known behaviors to detect
  const behaviors = await page.evaluate(() => {
    const behaviors = [];

    // Check for sticky header
    const header = document.querySelector('header');
    if (header) {
      const style = window.getComputedStyle(header);
      if (style.position === 'fixed' || style.position === 'sticky') {
        behaviors.push('Header is sticky (position: fixed/sticky)');
      }
    }

    // Check for swiper/slider
    const hasSwiper = document.querySelector('.swiper') || document.querySelector('.swiper-container');
    if (hasSwiper) {
      behaviors.push('Page uses Swiper.js library for sliders');
    }

    // Check for lazy loading images
    const lazyImages = document.querySelectorAll('img[loading="lazy"], img[data-src]');
    if (lazyImages.length > 0) {
      behaviors.push(`Found ${lazyImages.length} lazy-loaded images`);
    }

    return behaviors;
  });

  console.log('\n=== KNOWN BEHAVIORS ===\n');
  behaviors.forEach(b => console.log(`  - ${b}`));

  await browser.close();

  // Build final JSON
  const result = {
    page_name: 'Lobby',
    url_pattern: '/',
    last_updated: new Date().toISOString().split('T')[0],
    elements: elements,
    known_behaviors: behaviors
  };

  return result;
}

// Run and export
exploreLobbyDetailed().then(result => {
  console.log('\n' + '='.repeat(60));
  console.log('📋 FINAL JSON OUTPUT:');
  console.log('='.repeat(60));
  console.log(JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});
