# OpenClaw Migration Checklist (macOS)

Цей чек-лист адаптований під твою поточну архітектуру (з кількома воркспейсами, моделями Z.AI/DeepSeek та Telegram/Slack інтеграціями).

## 1. Підготовка та бекап
- [ ] Перевірити поточну версію: `openclaw --version`
- [ ] Зробити бекап основного каталогу `~/.openclaw` (конфіг `openclaw.json`, сесії, канали, пам'ять).
- [ ] **⚠ ВАЖЛИВО: Зробити бекап УСІХ твоїх воркспейсів.** У тебе їх шість:
  - `~/.openclaw/workspace` (основний)
  - `~/.openclaw/workspace-api-docs`
  - `~/.openclaw/workspace-jira-watcher`
  - `~/.openclaw/workspace-qa-agent`
  - `~/.openclaw/workspace-research-agent`
  - `~/.openclaw/workspace-vision-scout`

## 2. Оновлення
- [ ] Виконати оновлення: `npm install -g openclaw@latest` (або `sudo npm install -g ...`, якщо так встановлював раніше) АБО просто `openclaw update`.

## 3. Перевірка Gateway Auth
- [ ] *Break-зміна тебе не повинна зачепити*. Згідно з твоїм конфігом `openclaw.json`, у тебе вже прописаний тільки токен та чітко вказано `"mode": "token"`. Пароль у тебе не використовується.
- [ ] Для впевності перевір: `openclaw config get gateway.auth.mode` (має повернути `token`).

## 4. Перезапуск служб
- [ ] Перезапустити gateway: `openclaw gateway restart`.
- [ ] Перевірити статус: `openclaw gateway status` (має бути `local`, порт `18789`).

## 5. Перевірки (Doctor & Tests)
- [ ] Прогнати міграції та перевірки: `openclaw doctor`.
- [ ] Перевірити, що Control UI відкривається та працює без помилок.
- [ ] Перевірити інтеграцію зі Slack (канали/DM) — особливо QA Agent та Nexus. Боти мають перепідключитися.
- [ ] Перевірити Telegram-бота (Nexus).
- [ ] Переконатися, що всі 6 агентів "піднялися" з власних директорій і не загубили контекст.

## 6. Тестування нових фіч та моделей
- [ ] Скинути HEIF-фото в Telegram або Slack (в канал, де слухає Nexus чи Vision Scout) і переконатись, що воно читається без конвертації.
- [ ] У тебе вже налаштовані моделі `glm-5`, `glm-4.7-flash`, `glm-4.7`, `glm-4.5v` та кілька версій `deepseek`. Перевір, чи вони продовжують працювати як fallback/primary відповідно до твого конфігу (зокрема `"mode": "merge"`).
