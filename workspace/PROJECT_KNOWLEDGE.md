# Master Project Knowledge & Abstracted Learnings

_This document is maintained autonomously by Nexus Orchestrator. It contains the abstracted rules, architectural facts, and recurring patterns discovered by QA Agent and API Agent over time. Nexus uses this to ensure mistakes are never repeated._

## 1. API & Backend Rules

### 1.1 Critical Flow Testing
- **Registration → Login**: Always test together. Broken login after registration = P0 blocker
- **OAuth Tokens**: Verify backend accepts mock tokens on dev/stage BEFORE designing OAuth tests
- **If mock tokens rejected**: Request real credentials or test mode flag from backend team

### 1.2 API Test Data Generation
- **Telegram WebApp hash**: Can generate using HMAC-SHA256 with bot token (Python libraries available)
- **Google OneTap JWT**: Can mock for testing with Playwright
- **Rule**: Always research solutions (web search, mocks, local generators) for at least 10 minutes before reporting blockers

---

## 2. UI & Playwright Patterns

### 2.1 Test Plan Design Rules
- **Tool Reality Check**: Test plans must use ONLY available tools (API, curl, Playwright, read, write, exec, web_search)
- **NO assumptions about**: DB access, admin APIs, external systems without verification
- **Alternative to DB queries**: Use API responses to validate state instead

### 2.2 Slack Communication Rules
- **Self-contained reports**: Every Slack report must include TL;DR with key flows/edge cases
- **Actionable without attachments**: Message should be enough to make decisions
- **Always include**: 3-5 key flows being tested + critical edge cases

### 2.3 Smoke Test Rules
- **Internal domains priority**: NEVER propose public domains (e.g., minebit.com) for backend smoke tests
- **Always prioritize**: Internal portals (e.g., minebit-casino.prod.sofon.one)
- **VPN check**: Verify VPN status before writing test plan
- **Auth required**: Guest checks rarely have value for casino/finance — always include authorized checks

### 2.4 Credentials Hunting (QA Agent)
- **Mandatory first step**: Search local E2E repository (`fixtures`, `locators`, `env`) for test credentials
- **Alternative**: Create new user via API before halting at login screen
- **FORBIDDEN**: Stop at login window and report error without attempting to find/create credentials

---

## 3. General Business Logic
*(Will be populated by Nexus)*
