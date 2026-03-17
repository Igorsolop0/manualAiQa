# Stagehand Integration (OpenClaw) — DEPRECATED

> **DEPRECATED as of Phase 3 (2026-03-17).**
>
> ZAI models (GLM-4.7, GLM-5 Turbo) cannot drive Stagehand's agent loop.
> They produce only observation actions (ariaTree, screenshot, scroll, wait)
> but never generate interaction actions (click, fill, navigate).
>
> **Replacement:** `playwright-cli` (`@playwright/cli`)
> See: `workspace-qa-agent/SOUL.md` → "Browser Tool: Playwright CLI"

## Do Not Use

- Do not run stagehand-runner for any task
- Do not reference Stagehand mode in task files
- If legacy task files say `Stagehand REQUIRED`, use `playwright-cli` instead

## Historical Reference

- Runner project: `/Users/ihorsolopii/Documents/stagehand-runner`
- QA skill: `/Users/ihorsolopii/.openclaw/workspace-qa-agent/skills/stagehand-explore/SKILL.md` (deprecated)
- Used `@browserbasehq/stagehand` v3.1.0 with ZAI/DeepSeek models
- Failed in production: CT-527 showed 11 steps of scroll-only loop, zero browser interactions
