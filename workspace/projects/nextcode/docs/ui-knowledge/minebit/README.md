# MineBit UI Knowledge Base

This directory serves as the long-term memory for AI agents interacting with the MineBit and NextCode interfaces.

## Purpose
Instead of randomly parsing the DOM or guessing selectors, the agent MUST first check this directory for the relevant JSON page dictionary. This acts as an "AI Page Object Model".

## Workflow
1. **Action Request:** Ihor asks to interact with a page (e.g., "Click the first quest on bonuses page").
2. **Lookup:** Check `.json` files in this directory for known selectors and instructions.
3. **Execution:** Use the known selector via Playwright Script / MCP.
4. **Healing / Updating:** If the element is not found, run Stagehand exploration (`stagehand-runner`) to collect path + DOM/screenshot artifacts, find the new selector, and **update the JSON file immediately**. Notify Ihor about the selector change in Slack.

## Stagehand Artifact Source

Default location for exploration evidence:

`~/.openclaw/workspace/shared/test-results/<ticket-id>/stagehand/<run-id>/`

Use these files as evidence when updating page dictionaries:
- `stagehand-result.json`
- `step-*-after-tool.png`
- `step-*-after-tool.html`

## Format
Each page should be a `.json` file containing:
- `page_name`
- `url_pattern`
- `last_updated`
- `elements` (with `selector`, `description`, and `fallback_selectors`)
- `known_behaviors` (text notes on animations, waits, or quirks)

Use `bonuses-page.json` as a reference.
