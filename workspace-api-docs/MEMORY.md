# MEMORY.md - Cipher Long-Term Memory

Use this file for curated backend execution memory only.

Keep:

- stable system boundaries
- auth and session truths
- preferred backend paths for common actions
- recurring pitfalls in API execution and data prep

Do not turn this file into a generic backend textbook.

## Recipe Library (Primary Execution Path)

**All data preparation and API execution MUST use the recipe library first.**

- Catalog: `RECIPES.md`
- Code: `recipes/`
- Config: `recipes/env_config.py` (single source of truth for URLs, auth, brands)
- API Map: `knowledge/SWAGGER_API_MAP.md`

Available recipes: `create-player`, `login-player`, `credit-balance`, `deposit-flow`, `setup-test-player`, `get-bonuses`, `activate-bonus`.

All recipes accept `--env qa|prod` and `--brand` parameters. Environment-specific auth is handled by `env_config.py` automatically.

**FORBIDDEN:** Do not use scripts from `scripts/deprecated/`. They contain hardcoded URLs, wrong auth tokens, and environment-specific configs that will cause failures.

## Recipe Failure Escalation

If a recipe fails:

1. Report the exact error to Nexus immediately (do not try old scripts)
2. Include: recipe name, `--env`, error message, HTTP status code
3. If auth fails on PROD → report that credentials need refresh, specify which header/token
4. Do NOT fall back to `scripts/deprecated/` — those are dead code
5. Do NOT keep retrying silently — emit `blocked` callback within 60 seconds

## Current Operational Truths

1. Website API, Backoffice API, Wallet Service, and CRM Gateway are distinct systems.
2. Player-session-dependent API work often requires a session handoff from Clawver.
3. Wallet-style internal paths are usually the fastest safe route for simple balance preparation.
4. GraphQL success must be validated from response body, not HTTP status alone.
5. Cipher must separate `api.execute` from `data.prepare` when reporting results.
6. Cipher must not drift into UI execution.
7. For internal `*.sofon.one` services, assume VPN is already on unless Ihor explicitly says otherwise.
8. If internal access still fails, report the concrete failure back to Nexus quickly instead of narrating long investigation loops.

## Auth Reference

### BackOffice API (adminwebapi)
- QA: `UserId: 1` header (no Bearer token needed)
- PROD: `UserId: 560` header (no Bearer token needed)
- All configured in `env_config.py → backoffice_headers()`

### Website API (websitewebapi)
- Auth via player session token in request body
- Use `login-player` recipe to get fresh token
- All configured in `env_config.py → website_headers()`

### CRM Gateway (Smartico)
- Auth: `Api-UserId: 560` + `Api-Key` headers (same for QA and PROD)
- All configured in `env_config.py → crm_headers()`

### Wallet Service
- Internal service, no auth header required
- URL varies by env: `wallet.qa.sofon.one` / `wallet.prod.sofon.one`

## System Boundaries

### Website Web API
- player-facing
- often GraphQL plus selected REST actions
- requires player auth

### Backoffice Web API
- admin-facing
- used for control-panel and management actions
- requires `UserId` header (NOT Bearer token)

### Wallet Service
- financial/internal utility path
- often simplest route for balance operations
- preferred for fast test-state prep when safe
- Known issue: may return 500 on QA intermittently → use backoffice fallback

### CRM Gateway (Smartico)
- bonus campaigns, promo codes, gamification
- requires `Api-UserId` + `Api-Key` headers

## Known Weak Spots

1. Session-dependent tasks can stall if the FE-to-BE handoff is vague.
2. GraphQL flows can look successful at HTTP level while still failing logically.
3. API tasks can drift into undocumented business assumptions if Swagger is not checked first.
4. Internal QA and DEV service failures can be misdiagnosed as "VPN missing" if Cipher does not test the real endpoint first.
5. Wallet API on QA returns 500 intermittently — always have backoffice fallback.
6. Old scripts in `scripts/deprecated/` have hardcoded QA/DEV URLs and expired tokens — never use them.

## Practical Reminders

1. Use recipe library first for ALL data prep tasks.
2. Check `env_config.py` for correct URLs and auth — never hardcode.
3. Check `knowledge/SWAGGER_API_MAP.md` for endpoint reference.
4. Distinguish validation work from state-prep work in the final report.
5. Return evidence-backed conclusions only.
6. If blocked, escalate to Nexus within 60 seconds — do not retry silently.
