# Confluence Integration - Options & Setup

## ✅ Reminder Set

**Tomorrow at 12:00 PM (Feb 15, 2026):**
- Reminder to provide Swagger documentation URLs
- API tokens for Backend, Strapi, Smartico
- Test accounts

---

## 🔍 Confluence Access Options

### Option 1: Confluence CLI (Recommended for AI Agents)

**Package:** `confluence-cli` (npm)
**Version:** 1.17.0
**Description:** Command-line interface for Atlassian Confluence

**Install:**
```bash
npm install -g confluence-cli
```

**Setup:**
```bash
# Configure credentials
confluence config set host https://yourcompany.atlassian.net/wiki
confluence config set username your-email@company.com
confluence config set password YOUR_API_TOKEN
```

**Features:**
- ✅ Search pages
- ✅ Create/edit pages
- ✅ Get page content
- ✅ List spaces
- ✅ Attach files

**Usage:**
```bash
# Search for content
confluence search "deposit bonus"

# Get page content
confluence page get PAGE_ID

# List pages in space
confluence page list --space NEXTCODE

# Create page
confluence page create --space NEXTCODE --title "API Testing Guide" --content "..."
```

---

### Option 2: Confluence REST API (Direct)

**API Base URL:**
```
https://yourcompany.atlassian.net/wiki/rest/api
```

**Authentication:**
- Email + API Token
- OAuth (more complex)

**Python Example:**
```python
import requests
from requests.auth import HTTPBasicAuth

CONFLUENCE_URL = "https://yourcompany.atlassian.net/wiki"
EMAIL = "ihor.so@nextcode.tech"
API_TOKEN = "YOUR_API_TOKEN"

def search_confluence(query):
    url = f"{CONFLUENCE_URL}/rest/api/content/search"
    params = {"cql": f"text ~ '{query}'"}
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    response = requests.get(url, params=params, auth=auth)
    return response.json()

def get_page(page_id):
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"
    params = {"expand": "body.storage"}
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    response = requests.get(url, params=params, auth=auth)
    return response.json()

# Usage
results = search_confluence("deposit streak bonus")
page = get_page("123456")
```

**Node.js Example:**
```javascript
const axios = require('axios');

const CONFLUENCE_URL = 'https://yourcompany.atlassian.net/wiki';
const EMAIL = 'ihor.so@nextcode.tech';
const API_TOKEN = 'YOUR_API_TOKEN';

async function searchConfluence(query) {
  const response = await axios.get(
    `${CONFLUENCE_URL}/rest/api/content/search`,
    {
      params: { cql: `text ~ '${query}'` },
      auth: { username: EMAIL, password: API_TOKEN }
    }
  );
  return response.data;
}
```

---

### Option 3: Playwright Browser Automation

**Use when:**
- No API access
- Need to navigate through UI
- Complex interactions required

**Example:**
```javascript
import { test } from '@playwright/test';

test('Search Confluence for bonus info', async ({ page }) => {
  // Login
  await page.goto('https://yourcompany.atlassian.net/wiki');
  await page.fill('input[name="os_username"]', 'ihor.so@nextcode.tech');
  await page.fill('input[name="os_password"]', API_TOKEN);
  await page.click('input[type="submit"]');

  // Search
  await page.fill('input[placeholder="Search"]', 'deposit bonus');
  await page.press('input[placeholder="Search"]', 'Enter');

  // Get results
  const results = await page.locator('.search-result').allTextContents();
});
```

---

### Option 4: Python Confluence Library

**Install:**
```bash
pip3 install atlassian-python-api
```

**Example:**
```python
from atlassian import Confluence

confluence = Confluence(
    url='https://yourcompany.atlassian.net/wiki',
    username='ihor.so@nextcode.tech',
    password='YOUR_API_TOKEN'
)

# Search
results = confluence.cql('text ~ "deposit bonus"')

# Get page
page = confluence.get_page_by_id('123456', expand='body.storage')

# Get pages in space
pages = confluence.get_all_pages_from_space('NEXTCODE')
```

---

## 🎯 Recommended Setup for QA Agent

### Best Approach: **Confluence CLI + REST API**

**Why:**
- ✅ CLI is fast and token-efficient
- ✅ REST API for complex queries
- ✅ Can create OpenClaw skill
- ✅ Works with all agents

**Setup Steps:**

### 1. Create Confluence API Token

**URL:** https://id.atlassian.com/manage-profile/security/api-tokens

1. Click "Create API token"
2. Label: "OpenClaw QA Agent"
3. Copy token

### 2. Install Confluence CLI

```bash
npm install -g confluence-cli
```

### 3. Configure

```bash
confluence config set host https://nextcode.atlassian.net/wiki
confluence config set username ihor.so@nextcode.tech
confluence config set password YOUR_API_TOKEN
```

### 4. Test

```bash
confluence space list
confluence search "deposit bonus"
```

---

## 📊 Confluence API Endpoints

**Common Endpoints:**

```
GET /rest/api/content/search?cql=text ~ 'query'
GET /rest/api/content/{id}
GET /rest/api/content/{id}?expand=body.storage
GET /rest/api/space/{spaceKey}/content
GET /rest/api/space
POST /rest/api/content
PUT /rest/api/content/{id}
```

**CQL Queries (Confluence Query Language):**

```sql
-- Search by text
text ~ "deposit bonus"

-- Search by space
space = "NEXTCODE" AND text ~ "API"

-- Search by label
label = "api-documentation"

-- Search recent pages
created >= "2026-01-01" ORDER BY created DESC

-- Search by author
creator = "ihor.so@nextcode.tech"
```

---

## 🔧 OpenClaw Skill for Confluence

**Create skill:**
```
/opt/homebrew/lib/node_modules/openclaw/skills/confluence/
├── SKILL.md
├── references/
│   ├── search.md
│   ├── pages.md
│   └── spaces.md
└── scripts/
    ├── confluence_search.py
    └── confluence_get_page.py
```

**SKILL.md example:**
```yaml
---
name: confluence
description: Search and retrieve information from Confluence wiki. Use when you need to find feature documentation, API specs, or project information stored in Confluence.
allowed-tools: Bash(confluence:*), Bash(confluence-search:*), Bash(confluence-get:*)
---

# Confluence Integration

## Quick Start

```bash
# Search Confluence
confluence search "deposit bonus"

# Get specific page
confluence page get PAGE_ID

# List spaces
confluence space list
```
```

---

## 📝 NextCode Confluence Structure

**Likely Spaces:**
- `NEXTCODE` — Main documentation
- `DEV` — Development docs
- `QA` — Testing documentation
- `API` — API specifications
- `FEATURES` — Feature specifications

**Key Pages to Search:**
- "Deposit Bonus Feature"
- "Smartico Integration"
- "Strapi CMS Setup"
- "API Documentation"
- "Backend Architecture"

---

## 🚀 Quick Setup (Choose One)

### Option A: Confluence CLI (Fastest)
```bash
npm install -g confluence-cli
confluence config set host https://nextcode.atlassian.net/wiki
confluence config set username ihor.so@nextcode.tech
confluence config set password YOUR_API_TOKEN
```

### Option B: Python + REST API
```bash
pip3 install atlassian-python-api requests
```

### Option C: Playwright (If no API access)
Already installed ✅

---

## 💡 Integration Ideas

### 1. Auto-search on Jira Ticket
```
New Jira ticket → Extract keywords → Search Confluence → Add related docs
```

### 2. Feature Documentation Lookup
```
User asks about feature → Search Confluence → Summarize → Answer
```

### 3. API Testing Documentation
```
Swagger URL provided → Search Confluence for related specs → Cross-reference
```

---

## 📋 Needed from You:

1. **Confluence URL:**
   - `https://nextcode.atlassian.net/wiki` (or custom domain?)

2. **API Token:**
   - Create at: https://id.atlassian.com/manage-profile/security/api-tokens

3. **Space Keys:**
   - What spaces exist?
   - Which spaces are most important?

4. **Common Searches:**
   - What information do you need frequently?
   - Key pages to bookmark?

---

## ✅ Benefits

**With Confluence access, you can:**
- 🔍 Search for feature documentation
- 📋 Get API specifications
- 📝 Access testing guidelines
- 🔗 Cross-reference with Jira tickets
- 📊 Find architecture diagrams
- 🎯 Understand business logic

---

**Next Step: Provide Confluence URL and API Token, and I'll set up the integration! 🚀**
