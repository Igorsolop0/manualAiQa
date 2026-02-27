# LEARNINGS.md — Lessons Learned

**Purpose:** Document corrections, better approaches, and key learnings to avoid repeating mistakes.

**Updated:** 2026-02-24

---

## 🎯 Section 1: Data Sources — ALWAYS Verify

### Learning: BO Prod Data = Source of Truth

**Date:** 2026-02-23  
**Context:** Writing test cases for Regular Bonuses  
**Mistake:** I assumed Weekly bonuses have wagering because documentation mentioned it  
**Correction:** Ihor pointed out that BO Prod data shows `TurnoverCount: null` for ALL Regular Bonuses  
**Lesson:** 
- **ALWAYS** fetch real data from BO Prod before making assumptions
- Documentation (Confluence) may be outdated
- Verify with actual API responses: `curl adminwebapi.prod.sofon.one`

**Applied to:** All bonus-related testing

---

## 🎯 Section 2: Bonus System — Real Data

### Learning: Regular Bonuses Have NO Wagering

**Date:** 2026-02-23  
**Source:** BO Prod Data (adminwebapi)  
**Fact:**
```
Monthly (ID 8301): TurnoverCount: null, BonusTypeId: 11
Weekly (ID 8299): TurnoverCount: null, BonusTypeId: 11  
Cashback (ID 7207): TurnoverCount: null, BonusTypeId: 11
```

**Implications:**
- NO wagering progress bar on Regular Bonus cards
- Progress bar shows TIME until next period, NOT wagering
- Amount credited directly to real balance (no "Active Bonuses" entry)

**DO NOT:**
- Create test cases about wagering for Regular Bonuses
- Assume Weekly/Monthly have different logic

---

### Learning: Regular Bonus States (Real Names)

**Date:** 2026-02-23  
**Source:** Ihor correction + HTML inspection  
**States:**
1. **Waiting for reward** — Timer visible, waiting for calculation
2. **Ready for claim** — Amount calculated, button "Claim ${amount}"
3. **Claimed** — Amount credited to balance

**DO NOT USE (invented):**
- ❌ AwaitingForActivation
- ❌ ReadyForActivation
- ❌ Closed
- ❌ Finished

---

### Learning: CT-45 Applies to ALL Regular Bonuses

**Date:** 2026-02-23  
**Source:** Ihor correction  
**Fact:** CT-45 (parallel claim) applies to **ALL** Regular Bonuses (Cashback, Rakeback, Weekly, Monthly)

**Reason:** All have `BonusTypeId: 11` (CampaignCash) and `TurnoverCount: null`

**DO NOT:**
- Create test cases claiming Weekly "cannot claim parallel"
- Differentiate between Regular Bonus types for parallel claim logic

---

## 🎯 Section 3: Special vs Regular Bonuses — Key Differences

### Learning: Special Bonuses HAVE Wagering (Most)

**Date:** 2026-02-23  
**Source:** BO Prod Data  
**Fact:**
- Special Bonuses: `TurnoverCount > 0` (most have wagering)
- Regular Bonuses: `TurnoverCount: null` (NO wagering)

**Differences:**

| Parameter | Regular | Special |
|-----------|---------|---------|
| Wagering | ❌ None | ✅ Most have |
| States | 3 | 5 |
| Parallel Claim | ✅ Yes (CT-45) | ❌ Mono-bonus |
| Active Bonus Position | In list | Always FIRST |
| Progress Bar | TIME % | Wagering % |

---

## 🎯 Section 4: Test Case Design

### Learning: E2E Flow, Not Short Checks

**Date:** 2026-02-23  
**Source:** Ihor feedback  
**Correction:** "Test cases should have E2E flow, not short checks"

**Before (WRONG):**
```
TC-RB-002: State Transition AwaitingForActivation → ReadyForActivation
Steps: 1. Wait for timer, 2. Check state
```

**After (CORRECT):**
```
TC-RB-002: Cashback — Ready for Claim State
Steps: 1. Login, 2. Navigate, 3. Check state, 4. Check amount, 5. Click Claim, 6. Verify balance, 7. Check return to Waiting
```

**Lesson:** Each test case should cover a complete user journey

---

### Learning: TestRail Format — Follow Existing Structure

**Date:** 2026-02-23  
**Source:** TestRail Footer section analysis  
**Format:**
```json
{
  "title": "Verify ...",
  "priority_id": 2 (Critical) | 3 (High) | 4 (Medium),
  "type_id": 11 (Acceptance),
  "custom_preconds": "<p>Precondition 1</p><p>Precondition 2</p>",
  "custom_steps_separated": [
    {
      "content": "<p>Step description</p>",
      "expected": "<p>Expected result</p>"
    }
  ]
}
```

**DO:**
- Use HTML tags (`<p>`) in preconds and steps
- Separate steps logically (not too many in one step)
- Always include expected result

---

## 🎯 Section 5: API Documentation

### Learning: BonusTypeId Meanings

**Date:** 2026-02-23  
**Source:** BO Prod Data  
**Mapping:**
- **11** = CampaignCash (Regular Bonuses)
- **10** = Unknown (Cash Drop, Low Balance bonuses)
- **14** = FreeSpin-related
- **16** = Deposit+FS combination

**Action:** When unsure, check BO Prod for examples

---

## 🎯 Section 6: Clarification Questions

### Learning: Ask Before Assuming

**Date:** 2026-02-23  
**Context:** I invented bonus states and wagering logic  
**Correction:** Ihor had to correct multiple assumptions

**Better Approach:**
1. Fetch real data from BO Prod
2. Check HTML/UI if user provides it
3. Ask clarification questions if documentation unclear
4. Mark unclear info as "TBD" instead of guessing

---

## 🎯 Section 7: Cron Jobs & Automation

### Learning: Cron Job Failures Need Investigation

**Date:** 2026-02-23  
**Source:** Multiple cron failures  
**Fact:** Gmail Check cron was failing systematically with "LLM request timed out" (33-35s runtime, 0 output)

**Issue:**
- z.ai API timeout ~33-35 seconds
- Model not responding within timeout limit
- Multiple failures in one day

**Actions:**
1. Monitor cron job failures
2. Report systematic issues immediately
3. Suggest solutions (increase timeout, change model)

---

## 🎯 Section 8: Integration Knowledge

### Learning: Gmail + Jira Integration Setup

**Date:** 2026-02-14  
**Source:** Session memory  
**Components:**
- Gmail IMAP with App Password
- `go-jira` CLI for API access
- Cron job for automatic checks (every 30 min, 9:00-18:00 CET)
- Jira ticket extraction and summarization
- Telegram notifications

**Files:**
- `scripts/gmail_checker.py` — Email detector
- `scripts/jira_fetch.py` — Ticket fetcher
- `.gmail_config` — App Password
- `.jira_token` — API Token

**Usage:** Use `jira_fetch.py CT-XXX` to get ticket details quickly

---

## 🎯 Section 9: Wallet Service API

### Learning: Wallet Service — Alternative to BO API for Balance Operations

**Date:** 2026-02-24  
**Source:** Ihor discovery  
**Swagger:** https://wallet.dev.sofon.one/swagger/index.html

**Environments:**
- **Dev:** https://wallet.dev.sofon.one
- **QA:** https://wallet.qa.sofon.one
- **Prod:** https://wallet.prod.sofon.one

**Auth:** No authentication required (open API)

---

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **GET** | `/{partnerId}/api/v1/balance/{clientId}/{currency}` | Check client balance |
| **GET** | `/{partnerId}/api/v1/client-state/{clientId}/{currency}` | Get client state |
| **GET** | `/{partnerId}/api/v1/transaction/list/client/{clientId}` | List transactions |
| **GET** | `/{partnerId}/api/v1/transaction/{transactionId}` | Transaction details |
| **POST** | `/{partnerId}/api/v1/transaction/correction/credit` | Remove money ❌ |
| **POST** | `/{partnerId}/api/v1/transaction/correction/debit` | Add money ✅ |
| **POST** | `/{partnerId}/api/v1/transaction/payment/direct-deposit` | Direct deposit |
| **POST** | `/{partnerId}/api/v1/transaction/payment/withdrawal` | Withdrawal |
| **POST** | `/{partnerId}/api/v1/transaction/bet/credit` | Bet credit |
| **POST** | `/{partnerId}/api/v1/transaction/bet/debit` | Bet debit |
| **POST** | `/{partnerId}/api/v1/transaction/rollback` | Rollback transaction |

---

### Balance Check (Verified Working!)

```bash
curl 'https://wallet.dev.sofon.one/5/api/v1/balance/59107/USD'
```

**Response:**
```json
{
  "Balances": {
    "Unused": 30.91
  },
  "AvailableMain": 30.91,
  "AvailableBonus": 0.0,
  "Currency": "USD",
  "SportBonus": 0.0
}
```

---

### Operation Types

- `BetCredit` / `BetDebit` — Bets
- `Deposit` / `Withdrawal` — Deposit/Withdrawal
- `CorrectionCredit` / `CorrectionDebit` — Corrections
- `BonusAwarding` / `BonusRelease` / `BonusCancel` — Bonuses
- `Rollback` — Rollback

---

### Direct Deposit Issue

**Problem:** `direct-deposit` returns `InvalidRateBalances` error  
**Workaround:** Use `correction/debit` instead  
**BO API Alternative:** `/api/Client/CreateDebitCorrection` works on adminwebapi

---

### Comparison: BO API vs Wallet API

| Feature | BO API (adminwebapi) | Wallet API |
|---------|---------------------|------------|
| Balance Check | ❌ Complex | ✅ Simple GET |
| Add Money | ✅ CreateDebitCorrection | ✅ correction/debit |
| Auth | `UserId` header | None (open) |
| Transaction History | ✅ Available | ✅ Available |
| Best For | Admin operations | Balance operations |

**Recommendation:** Use Wallet API for balance checks, BO API for complex admin operations

---

## 🎯 Section 10: Page Object Model — Composition vs Duplication

### Learning: Use Composition, Not Duplication

**Date:** 2026-02-26  
**Context:** Creating LobbyPage.ts with Recent Top Wins widget  
**Mistake:** Duplicated all RecentTopWinsWidget locators and methods in LobbyPage.ts  
**Correction:** Ihor pointed out to use composition instead: `public readonly recentWins = new RecentTopWinsWidget(page);`

**What I did WRONG:**
```typescript
// Duplicated ~50 lines of code
readonly recentTopWinsWidget: Locator;
readonly recentTopWinsNextBtn: Locator;
readonly recentTopWinsPrevBtn: Locator;

async nextRecentWinsSlide(): Promise<void> {
  await this.recentTopWinsNextBtn.click();
}

async prevRecentWinsSlide(): Promise<void> {
  await this.recentTopWinsPrevBtn.click();
}

async isRecentTopWinsWidgetVisible(): Promise<boolean> {
  return await this.recentTopWinsWidget.isVisible();
}
```

**What I should have done (CORRECT):**
```typescript
// One line - composition!
import { RecentTopWinsWidget } from '../../components/widgets/RecentTopWinsWidget';

export class LobbyPage extends BasePage {
  public readonly recentWins = new RecentTopWinsWidget(page);

  // Now tests can access all widget methods:
  // await lobbyPage.recentWins.clickNext();
  // await lobbyPage.recentWins.assertIsVisible();
  // const count = await lobbyPage.recentWins.getWinCardsCount();
}
```

**Key Benefits of Composition:**
- ✅ **DRY principle**: No duplicate code
- ✅ **Single Source of Truth**: Widget logic lives in one place
- ✅ **Maintainability**: Bug fixes in widget apply everywhere
- ✅ **Discoverability**: All widget methods accessible via IntelliSense
- ✅ **Testability**: Widget can be tested independently

**Anti-Patterns to Avoid:**
1. ❌ Copying widget locators into page objects
2. ❌ Recreating widget methods in pages (clickNext, clickPrevious, etc.)
3. ❌ Wrapping widget methods without adding value
4. ❌ Not checking if widget/component already exists

**When to use composition:**
- **Widgets**: Sliders, carousels, cards, forms
- **Components**: Headers, footers, sidebars, modals
- **Reusable elements**: Tables, lists, grids

**When Page Objects should have direct locators:**
- Page-specific unique elements (e.g., main page container)
- Page-level orchestration (combining multiple widgets)
- Navigation between pages

**Applied to:** All Playwright Page Objects going forward

---

## 🎯 Section 11: Page Object Model — Parameterized Navigation Methods

### Learning: Use Parameterized Methods Instead of Hardcoded Text Variables

**Date:** 2026-02-27  
**Context:** Refactoring QuestsPage.ts for quests page navigation  
**Mistake:** Original QuestsPage.ts had hardcoded variables for quest tabs: `availableTab = page.locator('#missions_available_btn');`, `completedTab = page.locator('#missions_completed_btn');`, etc.  
**Correction:** Created parameterized method `navigateToQuestTab(tabName: string)` using `getByRole()` with regex

**What I did WRONG:**
```typescript
// Anti-pattern: Hardcoded text variables
readonly availableTab: Locator;
readonly completedTab: Locator;
readonly lockedTab: Locator;
readonly allTab: Locator;

constructor(page: any) {
  super(page);
  this.availableTab = page.locator('#missions_available_btn');
  this.completedTab = page.locator('#missions_completed_btn');
  this.lockedTab = page.locator('#missions_locked_btn');
  this.allTab = page.locator('.mission-tabs-container')
    .getByRole('button', { name: 'All', exact: true });
}

async switchToTab(tab: 'available' | 'completed' | 'locked' | 'all'): Promise<void> {
  const tabMap = {
    available: this.availableTab,
    completed: this.completedTab,
    locked: this.lockedTab,
    all: this.allTab,
  };
  await tabMap[tab].click();
}
```

**What I should have done (CORRECT):**
```typescript
// Best practice: Parameterized method with flexible matching
async navigateToQuestTab(tabName: string): Promise<void> {
  const tabButton = this.page.getByRole('button', {
    name: new RegExp(tabName, 'i')  // Case-insensitive regex
  });
  await tabButton.click();
  
  // Wait for tab to become active (has selected class)
  await expect(tabButton).toHaveClass(/selected/);
}
```

**Key Benefits of Parameterized Methods:**
- ✅ **Flexibility**: Handles text variations (capitalization, translations)
- ✅ **Maintainability**: One method instead of N variables
- ✅ **Extensibility**: Easy to add new tabs without modifying Page Object
- ✅ **Stability**: Uses accessibility-based `getByRole()` instead of fragile selectors
- ✅ **DRY**: No duplicate code for similar functionality

**Anti-Patterns to Avoid:**
1. ❌ Hardcoding text-based selectors as Page Object properties
2. ❌ Using IDs that may change (e.g., `#missions_available_btn`)
3. ❌ Creating separate variables for each navigation item
4. ❌ Not using accessibility-first locators (`getByRole`, `getByLabel`)

**When to use parameterized methods:**
- **Navigation tabs**: Quest tabs, category tabs, filter tabs
- **Menu items**: Sidebar navigation, dropdown options
- **Category lists**: Game categories, bonus types, sections
- **Any repeated pattern**: Where elements differ only by text content

**When Page Objects should have direct locators:**
- Unique page elements (e.g., main content container)
- Elements with stable data attributes (`data-testid`, `data-organism`)
- Elements that need specific wait conditions or complex interactions

**Applied to:** QuestsPage.ts refactoring - replaced 4+ hardcoded tab variables with single `navigateToQuestTab()` method

---

## 🎯 Section 12: PandaSen Ticket Testing System (Trial: 2026-02-24 to 2026-03-10)

**Date:** 2026-02-24  
**Status:** 🧪 **TRIAL PERIOD** — Testing this system for next 2 weeks  
**Purpose:** Automated testing pipeline for tickets assigned to PandaSen (Ihor) with human-in-the-loop review

### 🏗️ System Architecture

**Components:**
1. **Detector** → Jira webhook/Gmail parser for new PandaSen assignments
2. **Classifier** → Analyzes ticket type: `[FE]`, `[BE]`, `[API]`, `[Bug]`, `[QA]`
3. **Test Generator** → Creates test plan (automated + manual cases)
4. **[NEW] Ihor Review Step** → Detailed report for approval before execution
5. **Environment Health Check** → Verifies site/API availability before testing
6. **Test Executor (Dual Mode)**:
   - **A. Playwright as "hands"** → Interactive testing (Ihor sees screenshots/results)
   - **B. Automated tests** → Regression/smoke tests (fully autonomous)
7. **TestRail Integration** → Adds manual test cases to TestRail
8. **Reporter** → Updates Jira with results, attaches artifacts

### 🔄 Workflow (Human-in-the-Loop)
```
1. Detection → New ticket assigned to PandaSen
2. Classification → Ticket type analysis
3. Test Generator → Create test plan
4. ⭐ Ihor Review → Detailed report + approval required
5. Environment Check → Verify site/API availability
6. Execution:
   ├── Playwright as "hands" (interactive)
   └── Automated tests (regression)
7. TestRail Population → Add manual test cases
8. Reporting → Jira update + artifact attachment
```

### 🎯 Test Distribution Logic

| Criteria | Automate (Playwright) | Add to TestRail (Manual) |
|----------|----------------------|--------------------------|
| **Frequency** | Often (>1/day) | Rare (once per sprint) |
| **Stability** | Stable UI/API | Frequently changing/new features |
| **Complexity** | Simple, deterministic | Complex, requires human judgment |
| **Example** | "Slider appears on page" | "Matches Figma design exactly" |

### 🚀 Trigger Mechanism

**How to activate this system:**
- **Explicit command:** "протестуй тікет", "PandaSen workflow", "тестувальний пайплайн"
- **Heartbeat auto-detection:** When Gmail checker finds new PandaSen assignments
- **Manual trigger:** Mention ticket ID with testing context

**Ihor Review Report includes:**
- Ticket details (status, dependencies, priority)
- Test coverage plan (automated + manual)
- Environment health check results
- Required test data (player, balance, etc.)
- Test environment URLs + accessibility status

### 📋 Success Metrics (Trial Period)
- ✅ Reduced manual testing time by 30%+
- ✅ All PandaSen tickets get consistent test coverage
- ✅ TestRail stays updated with manual test cases
- ✅ Ihor maintains control via review step
- ✅ Environment issues caught before testing begins

### ⚠️ Trial Period Rules (2026-02-24 to 2026-03-10)
1. **Always generate Ihor Review report** before any test execution
2. **Wait for explicit approval** ("Go", "Запускай", "Схвалюю")
3. **Use Playwright as "hands"** for interactive testing during review
4. **Follow test distribution logic** (auto vs manual)
5. **Update this section** with learnings from trial period

---

## 📊 Summary of Key Principles

1. **Source of Truth:** BO Prod data > Documentation
2. **Verify:** Always fetch real data before writing tests
3. **Names:** Use exact names from UI/API, don't invent
4. **Flow:** Write E2E tests, not short checks
5. **Ask:** If uncertain, ask instead of assuming
6. **Learn:** Record corrections immediately
7. **Monitor:** Watch for systematic failures (cron jobs, API issues)
8. **Control:** Human-in-the-loop for PandaSen ticket testing (Trial Period)

---

## 🔄 Update Log

| Date | Learning | Section |
|------|----------|---------|
| 2026-02-23 | BO Prod = Source of Truth | 1 |
| 2026-02-23 | Regular Bonuses NO Wagering | 2 |
| 2026-02-23 | Regular Bonus States | 2 |
| 2026-02-23 | CT-45 Applies to ALL Regular | 2 |
| 2026-02-23 | Special vs Regular Differences | 3 |
| 2026-02-23 | E2E Flow Tests | 4 |
| 2026-02-23 | TestRail Format | 4 |
| 2026-02-23 | BonusTypeId Mapping | 5 |
| 2026-02-23 | Ask Before Assuming | 6 |
| 2026-02-24 | Wallet Service API | 9 |
| 2026-02-24 | PandaSen Ticket Testing System (Trial) | 12 |
| 2026-02-23 | Cron Job Failure Monitoring | 7 |
| 2026-02-14 | Gmail + Jira Integration | 8 |
| 2026-02-26 | POM: Use Composition, Not Duplication | 10 |
| 2026-02-27 | POM: Parameterized Navigation Methods | 11 |
