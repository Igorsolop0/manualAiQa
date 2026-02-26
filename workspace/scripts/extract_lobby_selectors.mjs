import { chromium } from 'playwright';

async function extractLobbySelectors() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('🌐 Opening https://minebit-casino.prod.sofon.one/ ...');
  await page.goto('https://minebit-casino.prod.sofon.one/', { timeout: 30000, waitUntil: 'commit' });

  await page.waitForSelector('body', { timeout: 10000 });
  await page.waitForTimeout(2000);

  console.log('🔍 Extracting full DOM structure...\n');

  // Extract comprehensive page data
  const pageData = await page.evaluate(() => {
    // Helper: decode base64
    function decodeBase64(str) {
      try {
        return atob(str);
      } catch (e) {
        return str;
      }
    }

    const result = {
      header: null,
      sidebar: null,
      hero: null,
      games: null,
      footer: null,
      allElements: []
    };

    // Find main containers
    const header = document.querySelector('header');
    const sidebar = document.querySelector('aside, .sidebar, [data-testid*="sidebar"], [data-organism*="sidebar"]');
    const footer = document.querySelector('footer');

    if (header) {
      result.header = {
        exists: true,
        html: header.outerHTML.substring(0, 500),
        children: header.querySelectorAll('*').length
      };
    }

    if (sidebar) {
      result.sidebar = {
        exists: true,
        html: sidebar.outerHTML.substring(0, 500),
        children: sidebar.querySelectorAll('*').length
      };
    }

    if (footer) {
      result.footer = {
        exists: true,
        html: footer.outerHTML.substring(0, 500),
        children: footer.querySelectorAll('*').length
      };
    }

    // Extract all elements with data attributes
    const allWithAttrs = document.querySelectorAll('*[data-testid], *[data-organism], *[id]');
    allWithAttrs.forEach(el => {
      const testId = el.getAttribute('data-testid');
      const organism = el.getAttribute('data-organism');
      const id = el.id;
      const tag = el.tagName.toLowerCase();
      const className = el.className ? el.className.toString().substring(0, 100) : '';
      const text = (el.textContent || '').trim().substring(0, 60);
      const href = el.getAttribute('href') || '';

      // Only collect meaningful elements
      if (testId || organism || id) {
        result.allElements.push({
          tag,
          id: id || '',
          className,
          testId: testId || '',
          testIdDecoded: testId ? decodeBase64(testId) : '',
          organism: organism || '',
          text,
          href
        });
      }
    });

    // Find actionable buttons
    const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'))
      .filter(btn => btn.textContent?.trim())
      .map(btn => ({
        tag: btn.tagName.toLowerCase(),
        text: btn.textContent.trim().substring(0, 40),
        testId: btn.getAttribute('data-testid'),
        testIdDecoded: btn.getAttribute('data-testid') ? decodeBase64(btn.getAttribute('data-testid')) : '',
        className: btn.className ? btn.className.toString().substring(0, 80) : '',
        href: btn.getAttribute('href') || ''
      }))
      .slice(0, 50); // First 50 buttons

    result.buttons = buttons;

    return result;
  });

  console.log(`📊 Header exists: ${pageData.header?.exists}`);
  console.log(`📊 Sidebar exists: ${pageData.sidebar?.exists}`);
  console.log(`📊 Footer exists: ${pageData.footer?.exists}`);
  console.log(`📊 Buttons found: ${pageData.buttons.length}`);

  // Print buttons with text
  console.log('\n=== KEY BUTTONS ===\n');
  pageData.buttons.slice(0, 30).forEach(btn => {
    if (btn.text && btn.text.length > 0) {
      console.log(`  [${btn.tag.toUpperCase()}] "${btn.text}"`);
      if (btn.testIdDecoded) {
        console.log(`    → data-testid: ${btn.testIdDecoded}`);
      }
    }
  });

  // Print data-organism values
  console.log('\n=== DATA-ORGANISM VALUES ===\n');
  const organisms = [...new Set(pageData.allElements.map(e => e.organism).filter(Boolean))];
  organisms.forEach(org => console.log(`  - ${org}`));

  // Build Page Objects JSON
  console.log('\n=== BUILDING PAGE OBJECTS ===\n');

  const elements = {};

  // Helper: find best selector
  function findBestSelector(keyword, elementType = 'button') {
    const keywordLower = keyword.toLowerCase();

    // First try: data-testid (decoded)
    const byTestid = pageData.allElements.find(e =>
      e.testIdDecoded.toLowerCase().includes(keywordLower)
    );

    if (byTestid && byTestid.testId) {
      return `[data-testid="${byTestid.testId}"]`;
    }

    // Second: data-organism
    const byOrganism = pageData.allElements.find(e =>
      e.organism.toLowerCase().includes(keywordLower)
    );

    if (byOrganism) {
      return `[data-organism="${byOrganism.organism}"]`;
    }

    // Third: id
    const byId = pageData.allElements.find(e =>
      e.id.toLowerCase().includes(keywordLower)
    );

    if (byId) {
      return `#${byId.id}`;
    }

    // Fourth: by text content
    const byText = pageData.buttons.find(b =>
      b.text.toLowerCase().includes(keywordLower)
    );

    if (byText) {
      if (byText.tag === 'a') {
        return `a:has-text("${keyword}")`;
      } else {
        return `button:has-text("${keyword}")`;
      }
    }

    return null;
  }

  // HEADER ELEMENTS
  const loginSel = findBestSelector('login', 'button');
  if (loginSel) {
    elements.login_btn = { selector: loginSel, description: 'Login button in header' };
    console.log(`✅ login_btn: ${loginSel}`);
  }

  const signUpSel = findBestSelector('sign up', 'button');
  if (signUpSel) {
    elements.sign_up_btn = { selector: signUpSel, description: 'Sign up button in header' };
    console.log(`✅ sign_up_btn: ${signUpSel}`);
  }

  const menuSel = findBestSelector('menu', 'button');
  if (menuSel) {
    elements.menu_toggle = { selector: menuSel, description: 'Menu toggle button (opens sidebar)' };
    console.log(`✅ menu_toggle: ${menuSel}`);
  }

  const langSel = findBestSelector('language', 'button');
  if (langSel) {
    elements.language_switcher = { selector: langSel, description: 'Language switcher dropdown' };
    console.log(`✅ language_switcher: ${langSel}`);
  }

  // SIDEBAR / NAVIGATION
  const sidebarSel = findBestSelector('sidebar', 'container');
  if (sidebarSel) {
    elements.sidebar = { selector: sidebarSel, description: 'Sidebar navigation panel' };
    console.log(`✅ sidebar: ${sidebarSel}`);
  }

  const slotsSel = findBestSelector('slots', 'button');
  if (slotsSel) {
    elements.games_category_slots = { selector: slotsSel, description: 'Games category - Slots' };
    console.log(`✅ games_category_slots: ${slotsSel}`);
  }

  const liveSel = findBestSelector('live', 'button');
  if (liveSel) {
    elements.games_category_live = { selector: liveSel, description: 'Games category - Live Casino' };
    console.log(`✅ games_category_live: ${liveSel}`);
  }

  const newSel = findBestSelector('new', 'button');
  if (newSel) {
    elements.games_category_new = { selector: newSel, description: 'Games category - New Games' };
    console.log(`✅ games_category_new: ${newSel}`);
  }

  // HERO BANNER
  const heroSel = findBestSelector('hero', 'section');
  if (heroSel) {
    elements.hero_banner = { selector: heroSel, description: 'Hero banner/carousel section' };
    console.log(`✅ hero_banner: ${heroSel}`);
  }

  // GAMES
  const gamesGridSel = findBestSelector('games', 'container');
  if (gamesGridSel) {
    elements.games_grid = { selector: gamesGridSel, description: 'Main games grid container' };
    console.log(`✅ games_grid: ${gamesGridSel}`);
  }

  const gameCardSel = findBestSelector('gamecard', 'div');
  if (gameCardSel) {
    elements.game_card = { selector: gameCardSel, description: 'Single game card' };
    console.log(`✅ game_card: ${gameCardSel}`);
  }

  const searchSel = findBestSelector('search', 'input');
  if (searchSel) {
    elements.search_input = { selector: searchSel, description: 'Games search input field' };
    console.log(`✅ search_input: ${searchSel}`);
  }

  // FOOTER
  const footerSel = findBestSelector('footer', 'footer');
  if (footerSel) {
    elements.footer = { selector: footerSel, description: 'Footer section' };
    console.log(`✅ footer: ${footerSel}`);
  }

  // FOOTER LINKS
  const termsSel = findBestSelector('terms', 'a');
  if (termsSel) {
    elements.footer_terms_link = { selector: termsSel, description: 'Terms & Conditions link' };
    console.log(`✅ footer_terms_link: ${termsSel}`);
  }

  const privacySel = findBestSelector('privacy', 'a');
  if (privacySel) {
    elements.footer_privacy_link = { selector: privacySel, description: 'Privacy Policy link' };
    console.log(`✅ footer_privacy_link: ${privacySel}`);
  }

  const licenseSel = findBestSelector('license', 'a');
  if (licenseSel) {
    elements.footer_license_link = { selector: licenseSel, description: 'License/Gambling Commission link' };
    console.log(`✅ footer_license_link: ${licenseSel}`);
  }

  // KNOWN BEHAVIORS
  const behaviors = [
    'Uses Base64-encoded data-testid values',
    'Uses data-organism attribute for component identification',
    'ComponentSliderGamesSlider - Games carousel slider',
    'ComponentSliderRecentWinnersSlider - Recent winners carousel'
  ];

  await browser.close();

  // Final JSON
  const result = {
    page_name: 'Lobby',
    url_pattern: '/',
    last_updated: new Date().toISOString().split('T')[0],
    elements: elements,
    known_behaviors: behaviors
  };

  return result;
}

extractLobbySelectors().then(result => {
  console.log('\n' + '='.repeat(60));
  console.log('📋 FINAL JSON OUTPUT:');
  console.log('='.repeat(60));
  console.log(JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});
