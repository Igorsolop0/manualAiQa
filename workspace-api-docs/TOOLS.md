# TOOLS.md - API Docs Agent Toolkit

This file describes your specific operational environment, configurations, and network dependencies.

## 1. Network & Environments

### Environments
- **DEV:** `*.dev.sofon.one` (Unstable, mostly used by developers)
- **QA:** `*.qa.sofon.one` (Your main playground for testing endpoints before UI automation)
- **PROD:** `*.prod.sofon.one` (Read-only. NEVER run mutations here without explicit permission)

### VPN Requirements
To access the internal tools and services, you depend on the host machine having specific VPNs enabled:
- **Tailscale VP:** Required to hit API endpoints on `.qa.` and `.dev.` environments.
- **Geo-VPN:** Required for public domains (minebit.com).

## 2. API Analysis Arsenal

### Python Scripts (`workspace-api-docs/scripts/`)
These are your primary execution tools when Nexus asks you to change a state:
- `login_player.py`
- `temp_credit.py` / `temp_deposit.py` / `temp_bo_credit.py`
- `check_bonus.py` / `monitor_rake.py`

### CLI Tools
- **openapi2cli (Generated CLI Clients):** Your super-weapon for calling REST endpoints (like Wallet or AdminWebApi) without manually writing `curl`. Found in `skills/openapi2cli/`. Use this to safely generate typed clients from Swagger URLs.
- **k6:** Your tool of choice for writing Functional and E2E API Regression tests. Write tests in JavaScript and run them with `k6 run <script.js>`. (Skill setup pending).
- **curl:** Used for bare-metal HTTP requests when scripts are unavailable.
- **jq:** Used to parse and extract data from massive JSON responses in the terminal.

## 3. Data & Formats

- **JSON:** Your native language. Always format JSON blocks for readability.
- **Swagger/OpenAPI (JSON/YAML):** The source of truth for REST APIs.
- **GraphQL Schema:** The source of truth for the Website API.

When documenting APIs for the QA Agent, you must understand payload structures, nullable fields, arrays, and serialization rules.
