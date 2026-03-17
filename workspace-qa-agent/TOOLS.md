# TOOLS.md - Clawver Local Notes

This file is for Clawver-specific local environment notes only.

Do not keep shared execution policy here. Shared behavior belongs in:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## Environments

### Internal Portals

Usually require Tailscale VPN.
Format:

- `https://{brand}-casino.{env}.sofon.one`

Examples:

- `https://minebit-casino.qa.sofon.one`
- `https://minebit-casino.prod.sofon.one`

### Public Domains

May require geo-VPN:

- `minebit.com`
- `minebit.io`

## Browser Tool

- **Primary tool:** `playwright-cli` (`@playwright/cli`)
- Installed globally via `npm install -g @playwright/cli@latest`
- Artifacts saved to `.playwright-cli/` in working directory

## Browser Notes

- Default mode: headless
- For headed mode: `playwright-cli open <url> --headed`
- Named sessions: `playwright-cli -s=<ticket> open <url>`

## Deprecated

- ~~Stagehand runner: `/Users/ihorsolopii/Documents/stagehand-runner`~~ — deprecated, do not use
