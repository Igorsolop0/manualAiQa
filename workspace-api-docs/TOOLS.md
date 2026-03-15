# TOOLS.md - Cipher Local Notes

This file is for Cipher-specific local environment notes only.

Do not keep shared execution policy here. Shared behavior belongs in:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## Environments

- `DEV`: `*.dev.sofon.one`
- `QA`: `*.qa.sofon.one`
- `PROD`: `*.prod.sofon.one`

## VPN Notes

- Tailscale VPN is commonly required for internal `.qa.` and `.dev.` services
- Geo-VPN may be required for public web domains

## Execution Tools

Primary local tools:

- Python scripts in `workspace-api-docs/scripts/`
- `curl`
- `jq`

Secondary tools:

- `openapi2cli`
- `k6`

Prefer stable local scripts first when they already cover the requested action.
