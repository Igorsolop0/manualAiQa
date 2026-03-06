---
name: jira-commenter
description: "Generate structured Jira ticket comments in Ihor's exact format. Use after testing is complete to prepare a ready-to-copy comment for Slack."
activation: "Use after completing manual or API testing to generate the Jira comment that Ihor will copy into the ticket."
---

# Jira Comment Generator

Generate structured Jira comments in Ihor's exact format after testing is complete.

## Important

- Comments go to **Slack**, NOT directly to Jira
- Ihor will **copy and paste** from Slack to the Jira ticket manually
- Evidence files are saved **locally** — provide file paths in Slack

## Comment Templates

### 1. UI Testing — Feature Verification

```
Tested on the {envName}, devices: {devices}, browsers: {browsers}. VPN: {yes/no}.

✅ Tested:
- {Feature 1} — works as expected
- {Feature 2} — works as expected

{screenshots/video attached as evidences}
```

**Variables:**
- `{envName}` — QA / DEV / PROD / Staging
- `{devices}` — MacBook Air, iPhone 15 Pro Max, Pixel 10
- `{browsers}` — Safari, Chrome (or just Chrome for QA Agent)
- Features — list each tested item with result

### 2. UI Testing — Bug Found

```
Tested on the {envName}, devices: {devices}, browsers: {browsers}. VPN: {yes/no}.

⚠️ Issues found:
- {Bug description 1} — [screenshot: {filename}]
- {Bug description 2} — [screenshot: {filename}]

✅ Working correctly:
- {Feature that works}

Evidence path: {local/path/to/screenshots}
```

### 3. API Testing — Endpoint Verification

```
Tested on the {env} endpoint: {endpoint}

✅ Verified:
- Response status: {statusCode}
- {What was checked — field values, business logic, etc.}

Response body:
```json
{response JSON — trimmed if too large}
```
```

### 4. API Testing — Multiple Endpoints

```
Tested on the {env}:

1. GET /api/v3/{endpoint1}
   ✅ Status: 200, {brief verification}

2. POST /api/v3/{endpoint2}
   ✅ Status: 201, {brief verification}

3. PUT /api/v3/{endpoint3}
   ⚠️ Status: 400, {issue description}

Evidence: response bodies saved at {path}
```

### 5. Combined (UI + API)

```
Tested on the {envName}:

**API Testing:**
- Endpoint: {endpoint}
- ✅ Response 200, data correct

**UI Testing:**
- Devices: MacBook Air, Pixel 7
- Browsers: Chrome
- ✅ Feature displayed correctly
- ✅ Data matches API response

Evidence: {screenshot paths}
```

## Evidence Path Format

```
~/.openclaw/workspace/shared/test-results/CT-XXX/
├── screenshot_001_desktop_homepage.png
├── screenshot_002_desktop_feature.png
├── screenshot_003_mobile_homepage.png
├── api_response_getUserBonuses.json
└── recording_desktop_flow.webm
```

## Slack Message Format

When sending to Slack, wrap the Jira comment in a block:

```
📝 **Ready to copy → Jira CT-XXX:**

---
[Jira comment text here]
---

📎 Evidence saved at: `shared/test-results/CT-XXX/`
Files: screenshot_001.png, screenshot_002.png
```

## Rules

1. Always use the **exact template format** — Ihor has a specific style
2. **Environment name** must be exact: QA, DEV, PROD (not "qa environment")
3. List **all** tested features, not just "everything works"
4. For API: always include at least one response body sample
5. For UI: always mention devices and browsers tested
6. Evidence paths must be **absolute** or relative to workspace
