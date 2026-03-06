---
name: qa-browser-testing
description: "AI Manual QA testing via browser. Combines Playwright MCP, CLI, and OpenClaw browser for real-time interactive testing. Use when QA Agent needs to open a browser and test manually."
activation: "Use when testing a feature manually, verifying a bug fix, or performing exploratory testing in the browser."
---

# QA Browser Testing Skill

This skill combines Playwright MCP, Playwright CLI, and OpenClaw browser capabilities for AI Manual QA testing.

## Browser Launch Rules

> ⚠️ ALWAYS follow these rules:

### Desktop Testing
```bash
# Use ONLY Chrome (Chromium)
playwright-cli open <URL> --browser=chromium

# Or via Playwright MCP
npx @playwright/mcp --browser chromium
```

### Mobile Testing  
```bash
# Use ONLY Pixel 7
playwright-cli open <URL> --device="Pixel 7"
```

### NEVER DO:
- ❌ Launch Firefox or WebKit
- ❌ Launch multiple browsers simultaneously
- ❌ Run all projects from playwright.config
- ❌ Skip mobile testing

### Minebit Testing
```bash
# Use nextcode browser profile with CDP
playwright-cli open https://minebit.qa.sofon.one --browser=chromium
```

## Testing Flow

1. **Open URL** → Desktop Chrome
2. **Snapshot** → Get page state
3. **Interact** → Click, fill, navigate
4. **Verify** → Check expected behavior
5. **Screenshot** → Capture evidence
6. **Mobile** → Repeat key flows on Pixel 7
7. **Report** → Structured test report

## Screenshot Evidence

Save all screenshots to: `~/.openclaw/workspace/shared/test-results/CT-XXX/`

Naming convention:
- `screenshot_001_desktop_homepage.png`
- `screenshot_002_desktop_feature.png`
- `screenshot_003_mobile_homepage.png`
- `recording_desktop_full_flow.webm`

## Playwright MCP Tools

| Tool | Use For |
|------|---------|
| `browser_navigate` | Open URL |
| `browser_click` | Click element |
| `browser_type` | Fill input |
| `browser_snapshot` | Get page structure |
| `browser_get_text` | Extract text |
| `browser_evaluate` | Run JS |
| `browser_press` | Keyboard input |
| `browser_choose_file` | File upload |

## Error Handling

- **Token expired?** → Log in via UI, extract fresh token from Network tab
- **Smartico popup?** → Snapshot, identify, dismiss it
- **Element not found?** → Try alternative selectors (role, text, testId)
- **Timeout?** → Increase timeout, check if page loaded
