# TOOLS.md - Cipher Local Notes

This file is for Cipher-specific local environment notes only.

Do not keep shared execution policy here. Shared behavior belongs in:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## Environments

- `DEV`: `*.dev.sofon.one`
- `QA`: `*.qa.sofon.one`
- `PROD`: `*.prod.sofon.one`

## VPN Notes

- Assume VPN is already on for internal `*.sofon.one` services unless Ihor explicitly says otherwise
- Tailscale VPN is commonly required for internal `.qa.` and `.dev.` services
- Geo-VPN may be required for public web domains
- If an internal service fails, verify with a real request first and report the exact failure instead of assuming VPN is off

## Execution Tools

Primary local tools:

- Python scripts in `workspace-api-docs/scripts/`
- `curl`
- `jq`

Secondary tools:

- `openapi2cli`
- `k6`

Prefer stable local scripts first when they already cover the requested action.
