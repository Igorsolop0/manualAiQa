---
name: stagehand-explore
description: "DEPRECATED — Stagehand exploration is no longer used. Use playwright-cli instead."
activation: "NEVER — this skill is deprecated as of Phase 3 (2026-03-17)."
deprecated: true
---

# Stagehand Explore Skill — DEPRECATED

> **This skill is deprecated as of Phase 3 (2026-03-17).**
>
> ZAI models (GLM-4.7, GLM-5 Turbo) cannot drive Stagehand's agent loop —
> they produce only observation actions (ariaTree, screenshot, scroll, wait)
> but no interaction actions (click, fill, navigate).
>
> **Replacement:** Use `playwright-cli` (`@playwright/cli`) for all browser interaction.
> See `SOUL.md` → "Browser Tool: Playwright CLI" section.

## Do Not Use

If a task references this skill or says `Stagehand REQUIRED`:
1. Ignore the Stagehand directive
2. Use `playwright-cli` instead
3. Follow the evidence capture pattern in SOUL.md

## Historical context

- Runner project was at: `/Users/ihorsolopii/Documents/stagehand-runner`
- Used `@browserbasehq/stagehand` v3.1.0
- Required LLM (ZAI/DeepSeek) to drive browser actions via agent loop
- Failed in production: models only produced scroll/observe actions, never click/fill
