---
name: testrail-manager
description: "Manage TestRail test cases: create, update, and query test cases via TestRail API. Use when QA Agent needs to add test cases, check existing cases, or update test results."
activation: "Use when user asks to 'add test cases to TestRail', 'create test cases', 'update TestRail', 'check TestRail', or when the QA workflow requires creating/updating test cases."
---

# TestRail Manager Skill

Manage test cases in TestRail (nexttcode.testrail.io) via API.

## Configuration

```python
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"
PROJECT_ID = 1   # Portal (contains Minebit suite)
SUITE_ID = 631   # Minebit test suite
```

## API Reference

### Add Test Case

```bash
curl -s -u "$EMAIL:$API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "title": "Test Case Title — English Only",
    "priority_id": 3,
    "type_id": 11,
    "custom_preconds": "<p>Preconditions here</p>",
    "custom_steps_separated": [
      {
        "content": "<p>Step description</p>",
        "expected": "<p>Expected result</p>"
      }
    ]
  }' \
  "$TESTRAIL_URL/index.php?/api/v2/add_case/SECTION_ID"
```

### Get Cases in Section

```bash
curl -s -u "$EMAIL:$API_KEY" \
  "$TESTRAIL_URL/index.php?/api/v2/get_cases/SECTION_ID"
```

### Get Sections

```bash
curl -s -u "$EMAIL:$API_KEY" \
  "$TESTRAIL_URL/index.php?/api/v2/get_sections/$PROJECT_ID&suite_id=$SUITE_ID"
```

### Add Section

```bash
curl -s -u "$EMAIL:$API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"name": "Section Name", "suite_id": 631}' \
  "$TESTRAIL_URL/index.php?/api/v2/add_section/$PROJECT_ID"
```

## TestRail Standards (CRITICAL)

> Read from `/Users/ihorsolopii/.openclaw/workspace/TESTRAIL_STANDARDS.md` before creating test cases!

### Rules:
1. **Language:** English ONLY — no Ukrainian
2. **Title format:** No Jira IDs (e.g., NOT "CT-123: Login test"). Use descriptive titles.
3. **Steps format:** Use HTML tags: `<p>`, `<ul>`, `<li>`
4. **Preconditions:** Always include in `custom_preconds`
5. **Priority IDs:**
   - 1 = Low
   - 2 = Critical
   - 3 = High
   - 4 = Medium
6. **Type IDs:**
   - 1 = Automated
   - 2 = Functionality
   - 11 = Acceptance

## Python Script Template

Use this template when adding multiple test cases:

```python
#!/usr/bin/env python3
"""Add test cases to TestRail for [Feature Name]"""

import json
import subprocess

TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"
SECTION_ID = XXXX  # ← Set section ID

def add_test_case(case_data):
    """Add a test case to TestRail"""
    cmd = [
        'curl', '-s', '-u', f"{EMAIL}:{API_KEY}",
        '-H', 'Content-Type: application/json',
        '-X', 'POST',
        '-d', json.dumps(case_data),
        f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{SECTION_ID}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

test_cases = [
    # Add cases here following the standard format
]

print(f"Adding {len(test_cases)} test cases to TestRail...")
for i, case in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] Adding: {case['title']}")
    result = add_test_case(case)
    if 'error' in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  ✅ Success! Case ID: {result['id']}")
print("Done!")
```

## Known Sections (Minebit)

| Section Name | Section ID | Area |
|-------------|-----------|------|
| Regular Bonuses | 6478 | Bonuses |
| Cashier Navigation | 7216 | Cashier |
| MetaMask Integration | 7213 | Crypto |
| WebSocket — Live Bets & Events (CT-799) | 7596 | WebSocket |

## Existing Scripts Reference

Scripts in `/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/scripts/`:
- `testrail_add_cases.py` — Regular Bonuses
- `testrail_add_cashier_navigation.py` — Cashier
- `testrail_add_metamask_integration.py` — MetaMask
- `add_cashier_section.py` — Section creation
- `move_cashier_cases.py` — Move cases between sections
- `testrail_summary.json` — Summary data
