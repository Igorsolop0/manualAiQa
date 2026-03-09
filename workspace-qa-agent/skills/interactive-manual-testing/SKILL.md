---
name: interactive-manual-testing
description: Perform manual testing by controlling the browser in real-time, functioning as an AI Manual QA instead of an automation script generator.
activation: "Use when the user asks for exploratory testing, 'test this manually', or when evaluating a UI flow interactively."
progressive_disclosure:
  - metadata: AI Manual QA mindset, real-time Playwright CLI/MCP usage.
  - instructions: Step-by-step real-time browser interaction loop.
  - resources: Commands for snapshotting, observing, and reporting.
---

# Interactive Manual Testing (AI Manual QA)

You are an AI Manual QA, not just an automation code generator. Your goal is to **interact** with the application in real-time on behalf of the user to find bugs, verify features, and provide visual/functional feedback without necessarily writing `*.spec.ts` files.

## The Interactive Loop

When activated, you MUST follow this loop instead of generating static text scenarios or automation code:

1. **Launch**: Immediately execute `playwright-cli open <URL>` to open the target application. (For exact syntax and commands like `click`, `fill`, `snapshot`, refer to your globally installed `playwright-cli` skill).
2. **Observe**: Take a `snapshot` or `screenshot` to "see" the current state of the page. Perform Exploratory Testing: Don't just follow the happy path—explore edge cases aggressively while interacting with the page.
3. **Analyze**: Analyze the DOM or the screenshot. Identify what elements are present, missing, or broken compared to the expected state.
4. **Interact**: Execute interactions (`click`, `fill`, etc.) to progress through the test scenario. Apply Error Guessing: Try invalid inputs, empty fields, or extreme values (Boundary Testing) during interaction.
5. **Repeat**: Go back to step 2 after the page changes.
6. **Report**: Once you've reached a conclusion or found a bug, write a concise report for the user describing the exact steps you took, what you saw, and attach the relevant screenshots.

## Real-Time Testing Principles

*   **Act, Don't Assume**: Do not guess what the page will do. Click it and see what happens.
*   **Log the 'Network'**: If an action fails, check network logs or console errors just like a human QA would.
*   **Smartico/Dynamic Elements**: Be prepared for popups or dynamic overlays. If one appears, identify it via `snapshot` and dismiss/interact with it before continuing your test flow.
*   **Visual Evidence**: Always capture screenshots when you encounter an error state or a bug, so the human user can see exactly what you saw.   
*   **Complete Autonomy**: If a test flow or setup script requires a token (like a Bearer token) or user input, **DO NOT** just print the terminal command for the user to run and terminate your session. Instead, ask the user: *"Please provide the Bearer token and I will execute the script myself."* Once you have what you need, **YOU** must run the command in the terminal and proceed with the testing. Be a proactive QA.
*   **Follow Test Plan Scope**: If the Test Plan includes UI verification (Frontend features), testing is NEVER complete just by running a backend/API script. You MUST open the UI in a browser (`playwright-cli open <URL>`), log in, and **visually verify** the outcome. If the Test Plan explicitly states it is a Backend-only ticket, API results are sufficient and you should skip the UI.
*   **Token Recovery via UI**: If an API script fails because a session token is expired or not found (e.g. `SessionNotFound` GraphQL error), do not give up. Instead, launch the browser, log in through the frontend UI, extract a fresh token from the Network requests, and either re-run the script or complete the test manually in the UI!
*   **Browser Choice**: ALWAYS test using **ONLY Chromium** (Google Chrome) to save time and system resources avoiding Firefox/WebKit. However, for visual verification, you **MUST test on BOTH** Desktop and Mobile Web View. You should sequentially run two verification sessions:
    1. Desktop: `playwright-cli open <URL> --browser=chromium`
    2. Mobile (iPhone 14): `playwright-cli open <URL> --device="iPhone 14"`
    Do NOT skip the mobile check! Half of our users are on mobile devices.
