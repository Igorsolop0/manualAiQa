# Проєкт: NextCode (MineBit)

**Домен:** iGaming, Casino, Betting
**Стек тестування:** Playwright, API (REST/GraphQL)

## 📁 Структура Проєкту
- **`docs/`** — Загальна документація
  - `docs/ui-knowledge/` — Дані по локаторах та UI специфіках.
  - `docs/bonus-analysis/` — Аналіз системи бонусів та логіки (Smartico, Wager).
- **`scripts/`** — Скрипти автоматизації (Jira fetch, Slack/Gmail сповіщення, TestRail синхронізація).
- **`meeting-notes/`** — Нотатки з мітингів.
- **`test-cases/` & `test-plans/`** — Тест-кейси.

## 🔑 Токени та Доступи
У цій же папці лежать ключі для доступу:
- `.jira_token` — Токен для API Jira.
- `.testrail_config` — Кредоси для TestRail.
- `.gmail_config` та `.gmail_seen_ids.json` — Налаштування читання пошти для інтеграції Jira->Slack.

## 🌐 API та Інфраструктура
- **BackOffice v1/v2/v3 Swagger:** `swagger_backoffice_*.json` (368+ ендпойнтів).
- **Website v3 Swagger:** `swagger_website_*.json` (125+ ендпойнтів).
- **GraphQL:** `graphql_introspect.json`.
- **Global Documentation Analytics:** Читати файли `API_ANALYSIS_*.md` та `MINEBIT_PLAYWRIGHT_ARCHITECTURE.md`.
