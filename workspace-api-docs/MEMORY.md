# MEMORY.md - Cipher Long-Term Memory

Use this file for curated backend execution memory only.

Keep:

- stable system boundaries
- auth and session truths
- preferred backend paths for common actions
- recurring pitfalls in API execution and data prep

Do not turn this file into a generic backend textbook.

## Current Operational Truths

1. Website API, Backoffice API, and Wallet Service are distinct systems and must not be mixed casually.
2. Player-session-dependent API work often requires a session handoff from Clawver.
3. Wallet-style internal paths are usually the fastest safe route for simple balance preparation.
4. GraphQL success must be validated from response body, not HTTP status alone.
5. Cipher must separate `api.execute` from `data.prepare` when reporting results.
6. Cipher must not drift into UI execution.

## System Boundaries

### Website Web API

- player-facing
- often GraphQL plus selected REST actions
- requires player auth

### Backoffice Web API

- admin-facing
- used for control-panel and management actions
- requires admin-style auth or configured headers

### Wallet Service

- financial/internal utility path
- often simplest route for balance operations
- preferred for fast test-state prep when safe

## Known Weak Spots

1. Session-dependent tasks can stall if the FE-to-BE handoff is vague.
2. GraphQL flows can look successful at HTTP level while still failing logically.
3. API tasks can drift into undocumented business assumptions if Swagger is not checked first.

## Practical Reminders

1. Check the real contract before speaking confidently.
2. Prefer existing scripts before inventing new ones.
3. Distinguish validation work from state-prep work in the final report.
4. Return evidence-backed conclusions only.
