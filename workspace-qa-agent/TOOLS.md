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

## Browser Notes

- Playwright CDP port: `18801`
- Default Minebit browser profile: `Profile 2`
- Stagehand runner: `/Users/ihorsolopii/Documents/stagehand-runner`
- Stagehand Chrome path: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
