---
name: stagehand-explore
description: "Run Stagehand exploration for unstable Minebit UI flows (modals/iframes/dynamic locators) and return structured steps + artifacts for Jira and Playwright drafting."
activation: "Use when locators are unstable, iframe/modal path is unknown, or task provides a high-level goal (new ticket / test plan) without clear click-by-click steps."
progressive_disclosure:
  - metadata: Input/output contract and trigger policy.
  - instructions: Exact runner command and artifact handling.
  - resources: JSON payload template and post-processing checklist.
---

# Stagehand Explore Skill

Use this skill as a **discovery layer** before deterministic Playwright.

## Trigger Policy (mandatory)

Run Stagehand only when at least one condition is true:
1. Unstable locators (casino pages, dynamic Smartico blocks, frequent DOM drift).
2. Unknown iframe/modal path (cannot reliably identify where clickable control lives).
3. Task contains a high-level goal without concrete reproducible steps ("test plan", "new ticket", exploratory task).

If none of the above is true, use normal Playwright flow.

## Runner Location

- Runner project: `/Users/ihorsolopii/Documents/stagehand-runner`
- Entry point: `npm run run -- --input <payload.json>`

## Required Payload Fields

```json
{
  "goal": "Reach state where bonus modal is visible after opening bonuses section",
  "initialUrl": "https://minebit-casino.qa.sofon.one",
  "ticketId": "CT-000",
  "maxSteps": 25,
  "timeoutMs": 90000,
  "needScreenshots": true,
  "needDomSnapshots": true
}
```

Notes:
- `goal` must describe a **final expected state**.
- `ticketId` is strongly recommended to keep artifacts under one ticket.
- `artifactDir` is optional; if omitted, runner writes to
  `~/.openclaw/workspace/shared/test-results/<ticket-or-ad-hoc>/stagehand/<timestamp>-<run>/`.

## Command Pattern

```bash
RUNNER_DIR="/Users/ihorsolopii/Documents/stagehand-runner"
TASK_OUT_DIR="/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-XXX"
mkdir -p "$TASK_OUT_DIR"

PAYLOAD_FILE="$TASK_OUT_DIR/stagehand-payload.json"
OUTPUT_FILE="$TASK_OUT_DIR/stagehand-output.json"

cat > "$PAYLOAD_FILE" <<'JSON'
{
  "goal": "<goal>",
  "initialUrl": "<url>",
  "ticketId": "CT-XXX",
  "maxSteps": 25,
  "timeoutMs": 90000,
  "needScreenshots": true,
  "needDomSnapshots": true
}
JSON

cd "$RUNNER_DIR"
npm run run -- --input "$PAYLOAD_FILE" --pretty > "$OUTPUT_FILE"
```

## Expected Output

Runner returns JSON with:
- `success`
- `reason`
- `steps[]` (action, description, selector/method/url when available)
- `artifacts.screenshots[]`
- `artifacts.domSnapshots[]`
- `meta.artifactDir`

## Post-Run Rules

1. If `success=false`, still use partial `steps[]` + artifacts as evidence and report blocker cause.
2. Save final QA result into `shared/test-results/<ticket>/` as usual (`results.json`, `jira-comment.txt`, screenshots).
3. Convert useful `steps[]` into deterministic Playwright draft steps.
4. Update Minebit UI knowledge JSON only with validated selectors/paths (do not overwrite blindly).
