import { chromium } from 'playwright';

async function exploreLobby() {
  const browser = await chromium.launch({ headless: true, args: ['--disable-blink-features=AutomationControlled'] });
  const page = await browser.newPage();

  console.log('🌐 Opening https://minebit-casino.prod.sofon.one/ ...');
  await page.goto('https://minebit-casino.prod.sofon.one/', { waitUntil: 'domcontentloaded', timeout: 60000 });

  // Full-page screenshot
  await page.screenshot({ path: '/tmp/minebit-lobby-full.png', fullPage: true });
  console.log('✅ Full-page screenshot saved to /tmp/minebit-lobby-full.png');

  // Collect selectors using multiple strategies
  const elements = {};

  // Helper function to find element by multiple strategies
  async function findElement(strategies, description, category = '') {
    for (const strategy of strategies) {
      try {
        const element = await page.locator(strategy).first();
        if (await element.isVisible({ timeout: 1000 })) {
          console.log(`✅ Found: ${description} -> ${strategy}`);
          return strategy;
        }
      } catch (e) {
        // Try next strategy
      }
    }
    console.log(`❌ Not found: ${description}`);
    return null;
  }

  console.log('\n🔍 Scanning critical elements...\n');

  // === HEADER ===
  elements.login_btn = await findElement(
    ['[data-testid="loginButton"]', 'button[data-organism*="login"]', 'button:has-text("Log in")', 'a:has-text("Log in")'],
    'Login button',
    'header'
  );

  elements.sign_up_btn = await findElement(
    ['[data-testid="signUpButton"]', 'button[data-organism*="signup"]', 'button:has-text("Sign up")', 'a:has-text("Sign up")'],
    'Sign up button',
    'header'
  );

  elements.menu_toggle = await findElement(
    ['[data-testid="menuButton"]', 'button[aria-label="menu"]', 'button:has([data-testid="MenuIcon"])', 'button.hamburger'],
    'Menu toggle (sidebar)',
    'header'
  );

  // Language switcher
  elements.language_switcher = await findElement(
    ['[data-testid="languageSwitcher"]', '[data-organism*="language"]', '.language-selector', 'button:has([data-testid="LanguageIcon"])'],
    'Language switcher',
    'header'
  );

  // Balance display (hidden for guests, but check if exists)
  elements.balance_display = await findElement(
    ['[data-testid="balanceDisplay"]', '[data-organism*="balance"]', '.balance'],
    'Balance display (hidden for guests)',
    'header'
  );

  // === SIDEBAR / NAVIGATION ===
  elements.sidebar = await findElement(
    ['[data-testid="sidebar"]', '[data-organism*="sidebar"]', 'aside', '.sidebar', '.navigation-drawer'],
    'Sidebar navigation',
    'sidebar'
  );

  // Game categories
  elements.games_category_all = await findElement(
    ['[data-testid="category-all"]', 'button:has-text("All")', 'a:has-text("All games")'],
    'Games category - All',
    'sidebar'
  );

  elements.games_category_slots = await findElement(
    ['[data-testid="category-slots"]', 'button:has-text("Slots")', 'a:has-text("Slots")'],
    'Games category - Slots',
    'sidebar'
  );

  elements.games_category_live = await findElement(
    ['[data-testid="category-live"]', 'button:has-text("Live")', 'a:has-text("Live Casino")'],
    'Games category - Live',
    'sidebar'
  );

  elements.games_category_table = await findElement(
    ['[data-testid="category-table"]', 'button:has-text("Table")', 'a:has-text("Table Games")'],
    'Games category - Table Games',
    'sidebar'
  );

  elements.games_category_new = await findElement(
    ['[data-testid="category-new"]', 'button:has-text("New")', 'a:has-text("New Games")'],
    'Games category - New',
    'sidebar'
  );

  // Promotions section
  elements.promotions_section = await findElement(
    ['[data-testid="promotions"]', '[data-organism*="promotions"]', 'section:has-text("Promotions")'],
    'Promotions section',
    'sidebar'
  );

  // === HERO BANNER ===
  elements.hero_banner = await findElement(
    ['[data-testid="heroBanner"]', '[data-organism*="hero"]', '[data-organism*="banner"]', '.hero-banner', '.hero-section'],
    'Hero banner',
    'hero'
  );

  // Hero banner slider controls
  elements.hero_next_btn = await findElement(
    ['[data-testid="heroNext"]', 'button:has([data-testid="ArrowForwardIosIcon"])', '.hero-banner .next'],
    'Hero banner - Next button',
    'hero'
  );

  elements.hero_prev_btn = await findElement(
    ['[data-testid="heroPrev"]', 'button:has([data-testid="ArrowBackIosIcon"])', '.hero-banner .prev'],
    'Hero banner - Previous button',
    'hero'
  );

  // === GAME GRIDS ===
  elements.games_grid = await findElement(
    ['[data-testid="gamesGrid"]', '[data-organism*="game-grid"]', '[data-organism*="GameGrid"]', '.games-grid', '.game-grid'],
    'Games grid',
    'games'
  );

  elements.game_card = await findElement(
    ['[data-testid="gameCard"]', '[data-organism*="game-card"]', '[data-organism*="GameCard"]', '.game-card'],
    'Game card (single game)',
    'games'
  );

  elements.game_card_first = await findElement(
    ['[data-testid="gameCard"] >> nth=0', '.game-card >> nth=0', '[data-organism*="GameCard"] >> nth=0'],
    'First game card',
    'games'
  );

  // Search input
  elements.search_input = await findElement(
    ['[data-testid="searchInput"]', 'input[placeholder*="search" i]', 'input[type="search"]', '.search input'],
    'Search input',
    'search'
  );

  // === FOOTER ===
  elements.footer = await findElement(
    ['footer', '[data-testid="footer"]', '[data-organism*="footer"]'],
    'Footer',
    'footer'
  );

  // License links
  elements.footer_license_link = await findElement(
    ['a:has-text("License")', 'a:has-text("Gambling Commission")', 'a:has-text("MGA")', '.license-link'],
    'License link',
    'footer'
  );

  elements.footer_terms_link = await findElement(
    ['a:has-text("Terms")', 'a:has-text("Terms and Conditions")', '.terms-link'],
    'Terms & Conditions link',
    'footer'
  );

  elements.footer_privacy_link = await findElement(
    ['a:has-text("Privacy")', 'a:has-text("Privacy Policy")', '.privacy-link'],
    'Privacy Policy link',
    'footer'
  );

  elements.footer_responsible_gaming = await findElement(
    ['a:has-text("Responsible")', 'a:has-text("Responsible Gaming")', '.responsible-gaming-link'],
    'Responsible Gaming link',
    'footer'
  );

  // Social media links
  elements.footer_social_twitter = await findElement(
    ['a:has([data-testid="TwitterIcon"])', 'a[href*="twitter.com"]', '.social-twitter'],
    'Twitter link',
    'footer'
  );

  elements.footer_social_telegram = await findElement(
    ['a:has([data-testid="TelegramIcon"])', 'a[href*="t.me"]', '.social-telegram'],
    'Telegram link',
    'footer'
  );

  elements.footer_social_instagram = await findElement(
    ['a:has([data-testid="InstagramIcon"])', 'a[href*="instagram.com"]', '.social-instagram'],
    'Instagram link',
    'footer'
  );

  // Footer language switcher
  elements.footer_language_switcher = await findElement(
    ['footer [data-testid="languageSwitcher"]', 'footer .language-selector', 'footer button:has([data-testid="LanguageIcon"])'],
    'Footer language switcher',
    'footer'
  );

  // === BEHAVIORS TO DETECT ===
  const behaviors = [];

  // Check for sticky header
  const header = await page.locator('header').first();
  if (await header.isVisible()) {
    const headerPosition = await header.boundingBox();
    if (headerPosition && headerPosition.y < 10) {
      behaviors.push('Header is positioned at top (potential sticky header behavior)');
    }
  }

  // Check for lazy loading on games
  const games = await page.locator('.game-card, [data-testid="gameCard"]').all();
  if (games.length > 0) {
    behaviors.push(`Found ${games.length} game cards - may implement lazy loading for more games on scroll`);
  }

  // Check for slider animations (hero banner)
  const hasHeroSlider = await findElement(['[data-testid="heroBanner"]', '.hero-banner'], 'Hero banner slider');
  if (hasHeroSlider) {
    behaviors.push('Hero banner likely has auto-play slider functionality');
  }

  // Close browser
  await browser.close();

  // Build final JSON
  const result = {
    page_name: 'Lobby',
    url_pattern: '/',
    last_updated: new Date().toISOString().split('T')[0],
    elements: {},
    known_behaviors: behaviors
  };

  // Only include found elements
  for (const [key, selector] of Object.entries(elements)) {
    if (selector) {
      result.elements[key] = {
        selector: selector,
        description: `${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} element`
      };
    }
  }

  return result;
}

// Run and export
exploreLobby().then(result => {
  console.log('\n' + '='.repeat(60));
  console.log('📋 FINAL JSON OUTPUT:');
  console.log('='.repeat(60));
  console.log(JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});
