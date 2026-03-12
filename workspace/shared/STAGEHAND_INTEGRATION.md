# Stagehand Integration (OpenClaw)

## Installed Components

- Runner project: `/Users/ihorsolopii/Documents/stagehand-runner`
- QA skill: `/Users/ihorsolopii/.openclaw/workspace-qa-agent/skills/stagehand-explore/SKILL.md`
- Policy updates:
  - QA soul: `/Users/ihorsolopii/.openclaw/workspace-qa-agent/SOUL.md`
  - Nexus soul: `/Users/ihorsolopii/.openclaw/workspace/SOUL.md`
  - Task template: `/Users/ihorsolopii/.openclaw/workspace/shared/tasks/README.md`

## Runner Setup

```bash
cd /Users/ihorsolopii/Documents/stagehand-runner
cp .env.example .env
```

Required at minimum:
- `STAGEHAND_MODEL` (default: `zai-coding/glm-4.7`)
- API key via one of:
  - `STAGEHAND_API_KEY`
  - provider key (`ZAI_API_KEY`, `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, ...)

Optional:
- `STAGEHAND_BASE_URL` for OpenAI-compatible providers.
- `STAGEHAND_CHROME_PATH` if Chrome is not at default macOS path.

Compatibility note:
- Keep `STAGEHAND_MODEL=zai-coding/glm-4.7` in OpenClaw style.
- Runner maps it internally for Stagehand aiSDK compatibility while preserving ZAI API/baseURL.

## Supported Model Patterns

1. ZAI Coding (recommended)
```env
STAGEHAND_MODEL=zai-coding/glm-4.7
ZAI_API_KEY=...
# STAGEHAND_BASE_URL is optional (runner resolves it automatically)
```

2. DeepSeek native (fallback)
```env
STAGEHAND_MODEL=deepseek/deepseek-chat
DEEPSEEK_API_KEY=...
```

## Manual Smoke Run

```bash
cd /Users/ihorsolopii/Documents/stagehand-runner
npm run build
node dist/index.js --payload '{
  "goal": "Open homepage and identify primary auth entry point",
  "initialUrl": "https://minebit-casino.qa.sofon.one",
  "ticketId": "CT-SMOKE",
  "maxSteps": 8,
  "timeoutMs": 60000,
  "needScreenshots": true,
  "needDomSnapshots": true
}' --pretty
```

## Output Contract

Runner always writes JSON to stdout and artifact files under:

`~/.openclaw/workspace/shared/test-results/<ticket-or-ad-hoc>/stagehand/<timestamp-run>/`

Main file inside artifact directory:
- `stagehand-result.json`

Fields:
- `success`
- `reason`
- `steps[]`
- `artifacts.screenshots[]`
- `artifacts.domSnapshots[]`
- `errors[]`
- `meta`

## Operational Rule

Use Stagehand only for discovery/path-finding (unstable locators, unknown iframe/modal, high-level goals).
For stable paths use deterministic Playwright directly.
