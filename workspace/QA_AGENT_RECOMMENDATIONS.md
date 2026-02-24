# QA Agent Toolkit - Рекомендації

## ✅ Вже встановлено та налаштовано

### Browser Automation & Testing
- ✅ **Playwright** (Node.js v1.58.2) — E2E testing, browser automation
- ✅ **Playwright CLI** (v0.1.0) — Token-efficient browser automation for agents
- ✅ **Mobile Device Emulation** — Pixel 7, iPhone 14, iPad Pro
- ✅ **WebKit** — Safari browser engine for iOS testing

### Project Management & Communication
- ✅ **Gmail Integration** — Email monitoring via IMAP
- ✅ **Jira API** — Ticket management via go-jira CLI
- ✅ **GitHub CLI** (gh v2.86.0) — Repository management
- ✅ **Telegram** — Notifications and alerts

### Available Skills (52 total)
- ✅ **github** — Issues, PRs, CI/CD
- ✅ **apple-notes/reminders** — Note-taking
- ✅ **things-mac** — Task management
- ✅ **weather** — Weather checks
- ✅ **discord/slack** — Team communication
- ✅ **summarize** — Content summarization
- ✅ **video-frames** — Video frame extraction
- ✅ **healthcheck** — Security auditing

---

## 🔧 Рекомендовані інструменти для QA Agent

### 1. Test Reporting & Reporting

**Allure Report** — Beautiful test reports
```bash
brew install allure
```
- Interactive test reports
- History trends
- Attachments (screenshots, logs)
- Integration with Playwright, Jest, Mocha

**Mochawesome** — HTML test reports for Mocha/Playwright
```bash
npm install -g mochawesome-report-generator
```

---

### 2. API Testing

**Newman** — Postman CLI runner
```bash
npm install -g newman
```
- Run Postman collections from CLI
- CI/CD integration
- Environment variables support

**HTTPie** — Modern curl alternative
```bash
brew install httpie
```
- Human-friendly HTTP client
- Better than curl for API testing
- JSON support out of the box

---

### 3. Performance Testing

**k6** — Load testing tool
```bash
brew install k6
```
- Script load tests in JavaScript
- CI/CD integration
- Cloud or local execution
- Metrics: response time, RPS, error rate

**Lighthouse** — Performance auditing
```bash
npm install -g lighthouse
```
- Performance metrics
- Accessibility checks
- SEO audit
- Best practices

**Artillery** — Modern load testing
```bash
npm install -g artillery
```
- YAML-based test scenarios
- WebSocket support
- Cloud execution

---

### 4. Security Testing

**OWASP ZAP** — Security scanner
```bash
brew install --cask owasp-zap
```
- Automated security scans
- API security testing
- Active/passive scanning

**npm audit** — Dependency vulnerability scanning (built-in)
```bash
npm audit
npm audit fix
```

**Snyk** — Vulnerability scanner
```bash
brew install snyk
```
- Dependency scanning
- Container scanning
- IaC security

---

### 5. Accessibility Testing

**axe-core CLI** — Accessibility testing
```bash
npm install -g @axe-core/cli
```
- WCAG compliance
- Automated accessibility checks
- Integration with Playwright

**pa11y** — Accessibility testing CLI
```bash
npm install -g pa11y
```
- WCAG 2.1 testing
- HTML CodeSniffer
- CI/CD integration

---

### 6. Visual Regression Testing

**BackstopJS** — Visual regression testing
```bash
npm install -g backstopjs
```
- Screenshot comparison
- Responsive testing
- HTML reports

---

### 7. Code Quality & Linting

**ESLint** — JavaScript linting
```bash
npm install -g eslint
```

**Prettier** — Code formatter
```bash
npm install -g prettier
```

**SonarQube Scanner** — Code quality
```bash
brew install sonar-scanner
```

---

### 8. Environment & Infrastructure

**Docker** — Containerization
```bash
brew install --cask docker
```
- Test environment isolation
- Selenium Grid
- Database containers

**Kind/Minikube** — Local Kubernetes
```bash
brew install kind
# or
brew install minikube
```

---

### 9. Database Tools

**pgcli** — PostgreSQL CLI with autocomplete
```bash
brew install pgcli
```

**mycli** — MySQL CLI with autocomplete
```bash
brew install mycli
```

**redis-cli** — Redis CLI
```bash
brew install redis
```

---

### 10. Monitoring & Logging

**Sentry CLI** — Error tracking
```bash
brew install sentry-cli
```

**LogRocket** — Session replay (web-based)

**Datadog** — Monitoring (CLI available)

---

### 11. Documentation

**Swagger Codegen** — API documentation
```bash
brew install swagger-codegen
```

**Mermaid CLI** — Diagram generation
```bash
npm install -g @mermaid-js/mermaid-cli
```

---

### 12. Test Data Management

**Faker.js** — Generate fake data
```bash
npm install -g @faker-js/faker
```

**JSON Server** — Mock REST API
```bash
npm install -g json-server
```

---

### 13. CI/CD Tools

**GitHub Actions** — Already available via `gh` CLI ✅

**GitLab CI** — If using GitLab
```bash
brew install glab
```

**Jenkins CLI** — If using Jenkins
```bash
brew install jenkins-cli
```

---

## 🎯 Пріоритет для QA Agent

### Must Have (Високий пріоритет):
1. **Allure** — Test reporting
2. **Newman** — API testing (Postman collections)
3. **k6** — Performance testing
4. **Lighthouse** — Performance/Accessibility audit
5. **axe-core** — Accessibility testing
6. **HTTPie** — API testing (better than curl)

### Should Have (Середній пріоритет):
7. **pa11y** — Accessibility testing
8. **BackstopJS** — Visual regression
9. **Docker** — Environment isolation
10. **Snyk** — Security scanning

### Nice to Have (Низький пріоритет):
11. **OWASP ZAP** — Security scanning
12. **Artillery** — Load testing alternative
13. **pgcli/mycli** — Database tools
14. **Mermaid CLI** — Documentation
15. **Faker.js** — Test data generation

---

## 📊 Приклад використання для QA Agent

### Performance Testing Pipeline:
```bash
# 1. Run Lighthouse audit
lighthouse https://example.com --output html --output-path ./report.html

# 2. Run k6 load test
k6 run load-test.js

# 3. Generate Allure report
allure generate ./allure-results --clean
allure open
```

### API Testing Pipeline:
```bash
# 1. Run Postman collection
newman run collection.json -e environment.json

# 2. Test specific endpoint
http GET https://api.example.com/users Authorization:"Bearer token"

# 3. Generate report
newman run collection.json -r allure
allure serve
```

### Accessibility Testing Pipeline:
```bash
# 1. Run axe-core
axe https://example.com

# 2. Run pa11y
pa11y https://example.com

# 3. Lighthouse accessibility audit
lighthouse https://example.com --only-categories=accessibility
```

---

## 🔧 Skills для створення

### Потенційні нові skills:

1. **api-testing** — Newman + HTTPie wrapper
2. **performance-testing** — k6 + Lighthouse wrapper
3. **accessibility-testing** — axe-core + pa11y wrapper
4. **visual-regression** — BackstopJS wrapper
5. **security-testing** — OWASP ZAP + Snyk wrapper
6. **test-reporting** — Allure + Mochawesome wrapper

---

## 📝 Наступні кроки

1. **Встановити Must Have інструменти:**
   ```bash
   brew install allure k6 httpie
   npm install -g newman @axe-core/cli lighthouse
   ```

2. **Створити QA-specific skills:**
   - `api-testing` skill
   - `performance-testing` skill
   - `accessibility-testing` skill

3. **Налаштувати інтеграції:**
   - Jira + Allure reporting
   - GitHub Actions + k6
   - Playwright + axe-core

4. **Створити test data generators:**
   - Faker.js для тестових даних
   - JSON Server для mock APIs

---

## 💡 Специфіка для твоїх проектів

### Sdui (EdTech):
- Accessibility testing (WCAG 2.1)
- Performance testing (load testing for peak hours)
- Cross-browser testing (schools use different browsers)
- Mobile testing (students on mobile devices)

### NextCode (iGaming):
- Security testing (financial data)
- Load testing (high traffic during promotions)
- API testing (payment systems, game APIs)
- Visual regression (UI consistency)

---

Хочеш почати з встановлення Must Have інструментів? 🚀
