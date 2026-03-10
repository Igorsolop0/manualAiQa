# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Local domains and test environments
- VPN requirements and routing rules
- SSH hosts and aliases
- Port configurations (e.g., CDP ports)
- Anything environment-specific

---

## My Cheat Sheet (QA Environment)

### Environments & Domains

#### Internal Portals (Requires Tailscale VPN)
Usually, I test on these internal domains. They are accessible **only when Tailscale VPN is connected**.
Format: `https://{brand}-casino.{env}.sofon.one`
- **Brands:** `minebit`, `alov`, `wagibet`
- **Environments:** `qa`, `dev`, `prod`
- *Example:* `https://minebit-casino.qa.sofon.one`

#### Public Web Domains (Requires Geo-VPN)
These are public-facing domains. They require a standard VPN (e.g., Hungary, Switzerland, Canada, etc.) to simulate real user traffic and bypass geo-blocks.
- **Domains:** `minebit.com`, `minebit.io`

### Browser Configuration
- **Playwright CDP Port:** 18801 (Profile 2 - nextcode)
