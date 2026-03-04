# Playwright CLI - Browser Automation

## ✅ Installed

**Version:** 0.1.0

**Package:** `@playwright/cli@latest` (global npm)

**Skills Location:**
- Claude: `/Users/ihorsolopii/.openclaw/workspace/.claude/skills/playwright-cli/`
- OpenClaw: `/opt/homebrew/lib/node_modules/openclaw/skills/playwright-cli/`

## 🚀 Quick Start

```bash
# Open browser
playwright-cli open https://example.com

# Take snapshot to get element refs
playwright-cli snapshot

# Interact with elements
playwright-cli click e3
playwright-cli type "search query"
playwright-cli fill e5 "user@example.com"

# Take screenshot
playwright-cli screenshot

# Close browser
playwright-cli close
```

## 📱 Mobile Device Testing

```bash
# Use specific browser
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit

# Headed mode (visible browser)
playwright-cli open --headed

# Persistent profile
playwright-cli open --persistent
```

## 🎯 Key Features

**Browser Automation:**
- Navigate pages
- Click, type, fill forms
- Drag & drop
- Hover, select
- Upload files
- Check/uncheck boxes

**DevTools:**
- Console logs
- Network monitoring
- JavaScript evaluation
- Tracing
- Video recording

**Storage:**
- Cookies
- LocalStorage
- SessionStorage
- State save/load

**Sessions:**
- Multiple browser instances
- Named sessions
- Profile management

## 📚 Reference Guides

Available in: `/opt/homebrew/lib/node_modules/openclaw/skills/playwright-cli/references/`

- `request-mocking.md` - Intercept and mock network requests
- `running-code.md` - Execute Playwright scripts
- `session-management.md` - Manage browser sessions
- `storage-state.md` - Persist browser state
- `test-generation.md` - Generate tests
- `tracing.md` - Record traces
- `video-recording.md` - Capture videos

## 🔧 Example: Form Submission

```bash
playwright-cli open https://example.com/login
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3

playwright-cli screenshot
playwright-cli close
```

## 💡 For Agents

This skill is now available for all agents (not just Claude):

**Location:** `/opt/homebrew/lib/node_modules/openclaw/skills/playwright-cli/SKILL.md`

**Description:** "Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages."

## 🎯 When to Use

Use playwright-cli when you need to:
- Test web applications
- Fill forms automatically
- Take screenshots
- Extract data from websites
- Automate repetitive browser tasks
- Debug web issues
- Record browser sessions

## 🕵️ Interactive Exploratory Testing (Crucial for Agents)

**CRITICAL INSTRUCTION:** When the user asks for "Exploratory testing" or asks you to "explore" a feature:
1. **DO NOT** just write static test scenarios or automation code.
2. **INSTANTLY** execute `playwright-cli open <URL> --browser=chromium` in the terminal. Always use Chromium to save time unless requested otherwise.
3. Use `playwright-cli snapshot`, `playwright-cli screenshot`, or `video-frames` to actually "see" the UI.
4. Interact with the page step-by-step (`click`, `fill`, etc.) in a loop, acting like a real QA engineer.
5. Report your findings based on the *actual* UI state you observe, not assumptions.
