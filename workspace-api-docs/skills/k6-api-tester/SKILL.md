---
name: k6-api-tester
description: Functional, E2E, and Load Testing tool for APIs. Use this to write robust JavaScript tests with assertions for the API Docs Agent.
version: 1.0.0
---

# k6 API Testing Skill

Grafana k6 is your primary tool for creating functional API tests, regression suites, and load tests. Because k6 uses standard JavaScript (ES6+), you can easily write tests that chain requests together, manage tokens, and assert complex JSON structures.

## Requirements
- `k6` executable installed on the system (usually installed via Homebrew).
- Access to the API documentation or Swagger paths.

## 🛠️ How it works

When Nexus assigns you a task to do **"functional testing," "regression testing," or "check an entire flow,"** do NOT use `openapi2cli` or `curl`. Instead, write a `k6` test script and run it.

### Step 1: Write the Test Script (.js)
Create a `.js` file in your `scripts/` folder (e.g., `scripts/test_claim_bonus.js`). 

**ALWAYS use this template for your k6 scripts:**

```javascript
// test_claim_bonus.js
import http from 'k6/http';
import { check } from 'k6';

// 1. Setup Configuration (Optional but good for load testing later)
export const options = {
  // For functional QA tests, we just want 1 iteration.
  iterations: 1, 
  vus: 1,
};

// 2. Main Logic Function
export default function () {
  // A. Define the URL and Payload
  const url = 'https://adminwebapi.qa.sofon.one/api/v1/bonuses/claim';
  const payload = JSON.stringify({
    clientId: 59107,
    bonusId: 8301
  });

  // B. Define Headers (Authentication)
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'UserId': 'admin-id-123' // Or Authorization: Bearer <TOKEN>
    },
  };

  // C. Execute the Request
  const res = http.post(url, payload, params);

  // D. Assertions (CRITICAL: Status codes in GraphQL are deceptive!)
  check(res, {
    'is status 200': (r) => r.status === 200,
    'has no graphql errors': (r) => {
        try {
            const body = JSON.parse(r.body);
            return !body.errors;
        } catch(e) { return true; } // Not GraphQL or invalid JSON
    },
    'returns expected success code': (r) => {
        try {
            const body = JSON.parse(r.body);
            return body.ResponseCode === 'Success';
        } catch(e) { return false; }
    }
  });
}
```

### Step 2: Execute the Script
Run your newly created script using the `k6 run` command:

```bash
k6 run ./scripts/test_claim_bonus.js
```

### Step 3: Analyze the Output
`k6` will output a beautiful summary in the terminal showing:
- Which `check()` blocks passed (✓) or failed (✗).
- The exact response times (`http_req_duration`).

## 🧠 Best Practices for API Agent
- **GraphQL Warning:** Remember that POST requests to `/graphql` **always return 200 OK**, even if the query fails. You MUST add a `check()` that parses the `r.body` and looks for the `errors` array.
- **Log specifically:** If you need to see the exact API response to debug something, use `console.log(res.body);` right before your checks.
- **Negative Testing:** If you are testing a 401 Unauthorized scenario, your `check()` should intentionally look for `(r) => r.status === 401`.

## When to use this skill
- **Test Scenarios:** Creating a script that registers a user, deposits money, claims a bonus, and checks the final balance.
- **Regression:** Creating a suite of tests that Nexus can run automatically to ensure the Dev environment isn't broken.
- **Load Testing (Future):** By simply changing `options = { vus: 10, duration: '30s' }`, your functional test instantly becomes a load test!
