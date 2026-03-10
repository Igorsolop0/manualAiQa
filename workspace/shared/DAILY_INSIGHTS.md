# Daily Agent Insights & Errors

_This file is used by QA Agent (Clawver) and API Docs Agent (Cipher) to continuously log their mistakes, unexpected findings, and manual corrections from Ihor._

_Every night at 23:00, Nexus Orchestrator reads this file, abstracts the learned rules into `PROJECT_KNOWLEDGE.md`, and then clears this file._

---

## 2026-03-10 — CT-709 Test Plan Review Feedback

### Mistake #1: Non-informative Slack Report
**Context:** Created test plan for CT-709 and posted Slack message saying only "22 test cases created, see file".

**Error:** Message was not actionable. User had to open the full document to understand what's being tested. No key flows or edge cases highlighted.

**Root Cause:** Did not think from user's perspective — what would be most useful for them to know immediately?

**How to Avoid:**
- Always include TL;DR summary in Slack messages
- Highlight 3-5 key flows being tested
- Mention critical edge cases
- Make message actionable without opening external files

**Rule Added:** Slack reports must be self-contained with enough detail to make decisions without opening attachments.

---

### Mistake #2: Unrealistic Tool Dependencies (DB Access)
**Context:** Test plan included many steps like "Query DB: SELECT * FROM ExternalIdentity" without checking if I have DB access.

**Error:** Assumed database query capabilities without verifying available tools. This makes test plan non-executable by me autonomously.

**Root Cause:** Did not review available tools (read, write, exec, web_search) before designing test approach.

**How to Avoid:**
- ALWAYS check available tools first
- Design tests to use only available capabilities (API calls, Playwright, curl)
- If DB verification needed, find alternative API endpoints
- Use API responses to validate state instead of direct DB queries

**Rule Added:** Test plans must be executable with available tools only. No assumptions about DB access, admin APIs, or external systems without verification.

---

### Mistake #3: Passive Position on Test Data Blockers
**Context:** Immediately stopped work and waited for Google OAuth tokens and Telegram hashes from Ihor, marking task as "Waiting".

**Error:** Did not attempt to solve the problem independently. Could have researched how to generate test data locally or use mocks.

**Root Cause:** Habit of asking for data instead of researching solutions. Forgot SOUL.md principle: "Persistence (No Blockers): Do not wait for someone to explain."

**How to Avoid:**
- Always research solutions via web_search/tavily before asking
- Look for Python libraries, mock frameworks, local generators
- Check if project has existing mock skills
- Propose concrete solutions, not just problems

**Solution Found (via Tavily):**
- **Telegram WebApp hash:** Can generate using HMAC-SHA256 with bot token. Python libraries available.
- **Google OneTap JWT:** Can mock JWT tokens for testing with Playwright.

**Rule Added:** Before reporting blockers, research solutions for at least 10 minutes. Always propose a concrete approach.

---

## 2026-03-10 — CT-709 API Testing Findings (API Docs Agent)

### Finding #1: Critical Bug - NullReferenceException in Login Endpoint
**Context:** API Docs Agent (Cipher) executed CT-709 tests and discovered a critical bug in the login endpoint.

**Bug Details:**
- **Endpoint:** `/{partnerId}/api/v3/Client/Login`
- **Error:** `NullReferenceException` after successful user registration
- **Trace ID:** `02cf66a98218c0806af386e41b050740`
- **Environment:** Dev (https://websitewebapi.dev.sofon.one)
- **Repro:** Register new user (clientId 59160) → Try to login → Crash

**Impact:**
- Blocks all regression testing on dev
- Suggests OAuth refactor may have broken traditional auth flow
- Users cannot login after registration

**Rule Added:** Always test critical flows (registration → login) together. Broken login after registration = P0 blocker that should be reported immediately.

---

### Finding #2: Backend Doesn't Accept Mock OAuth Tokens
**Context:** Created mock Google JWT tokens via `scripts/mock_google_jwt.js`, but backend accepts them silently and returns `responseObject: null` instead of validating.

**Issue:**
- OneTapAuth endpoint accepts mock tokens without validation
- No test mode flag available on dev/stage
- Real OAuth tokens required for testing

**Workaround Used:**
- Created generators for test data (Telegram hash, Google JWT)
- Unable to complete OAuth tests without real credentials

**Root Cause:** Backend team didn't include test mode for mock tokens during OAuth refactor.

**Rule Added:** Before designing OAuth tests, verify if backend accepts mock tokens on dev/stage. If not, request real credentials or test mode flag from backend team.

---

## 2026-03-10 — CT-476 Prod Smoke Test Findings (Clawver & Nexus)

### КРИТИЧНИЙ ВИСНОВОК З ТЕСТУВАННЯ CT-476:
1. **Правила створення Test Plan (Для Nexus):** Ніколи не пропонуй використовувати публічні домени (напр. minebit.com) для smoke-тестування бекенд фіч, якщо не вказано інше. Завжди пріоритезуй внутрішні портали (напр. minebit-casino.prod.sofon.one) та перевірку того, чи увімкнений VPN, перед тим як писати план. Гостьові перевірки (неавторизовані) рідко мають цінність для каси чи фінансів — завжди включай авторизовані перевірки.
2. **Правила пошуку Credentials (Для QA Agent - Clawver):** Якщо для тесту потрібна авторизація, Clawver СУВОРО ЗОБОВ'ЯЗАНИЙ спочатку піти у локальний E2E репозиторій (/Users/ihorsolopii/Documents/minebit-e2e-playwright) та прочитати файли в директоріях `fixtures`, `locators` або `env`, щоб знайти тестові credentials. ЗАБОРОНЕНО зупинятися на вікні логіну і просто репортити помилку, не здійснивши спробу знайти кредо або створити нового юзера самостійно через API чи скрипт.

---

## Summary of New Rules

1. **Slack TL;DR:** Every Slack report must include actionable summary with key flows/edge cases
2. **Tool Reality Check:** Test plans must use only available tools (API, curl, Playwright)
3. **Proactive Blocker Resolution:** Research solutions (web search, mocks, local generators) before asking for data
4. **Critical Flow Testing:** Always test registration → login together. Broken login after registration = P0 blocker
5. **Mock Token Validation:** Verify backend accepts mock tokens before using them in tests. If not, request test mode or real credentials
6. **Internal Domains Priority:** Never propose public domains for backend smoke tests. Prioritize internal portals and verify VPN status. Always include authorized checks for financial flows.
7. **Credentials Hunting:** QA Agent MUST search the local E2E repository (`fixtures`, `locators`, `env`) for test credentials before testing authorized flows, or attempt to create a valid user via API. Never halt at a login screen.
