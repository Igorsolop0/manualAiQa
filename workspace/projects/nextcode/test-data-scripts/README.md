# Test Data Scripts for Minebit/NextCode

Автоматизовані скрипти для підготовки тестових даних у проекті Minebit/NextCode.

## 📁 Структура проекту

```
test-data-scripts/
├── config/
│   ├── environments.yaml          # Налаштування середовищ (dev/qa/prod)
│   └── credentials.example.yaml   # Шаблон для облікових даних
├── scripts/
│   ├── generate_test_data.py      # Утиліти генерації тестових даних
│   ├── api_clients.py             # API клієнти (Website, BO, Wallet, GraphQL)
│   ├── 01_create_test_player.py   # Створення тестового гравця
│   ├── 02_set_test_player_balance.py  # Встановлення балансу
│   ├── 03_create_deposit_flow.py  # Повний флоу депозиту
│   ├── 04_get_player_info.py      # Отримання інформації про гравця
│   ├── 05_create_bonus.py         # Створення тестового бонусу
│   └── 07_test_data_orchestrator.py   # Оркестратор сценаріїв
├── fixtures/
│   └── (future: Playwright fixtures)
├── test_data_log.json             # Лог створених тестових даних
└── README.md                      # Ця документація
```

## 🚀 Швидкий старт

### 1. Встановлення залежностей

```bash
# Перевірка наявних залежностей
python3 -c "import yaml, requests; print('✅ All dependencies available')"

# Якщо не встановлено:
pip3 install pyyaml requests
```

### 2. Налаштування конфігурації

```bash
# Конфігурація вже готова для використання
# За бажанням можна налаштувати credentials.yaml для спеціальних випадків

cd /Users/ihorsolopii/.openclaw/workspace/projects/nextcode/test-data-scripts
```

### 3. Базові приклади використання

#### Створення гравця з балансом

```bash
# Створити гравця з балансом $100 в QA
python3 scripts/01_create_test_player.py --env qa --balance 100

# Створити гравця для конкретного тікету
python3 scripts/01_create_test_player.py --env qa --ticket CT-727 --balance 200

# Без балансу
python3 scripts/01_create_test_player.py --env qa --no-balance
```

#### Встановлення балансу

```bash
# Додати баланс через Wallet API (швидко)
python3 scripts/02_set_test_player_balance.py 123456 --amount 100 --env qa

# Додати баланс через BackOffice депозит (повний флоу)
python3 scripts/02_set_test_player_balance.py 123456 --amount 50 --env qa --method backoffice

# Перевірити баланс
python3 scripts/02_set_test_player_balance.py 123456 --check --env qa
```

#### Створення депозиту

```bash
# Повний флоу депозиту
python3 scripts/03_create_deposit_flow.py 123456 --amount 30 --env qa
```

#### Отримання інформації про гравця

```bash
# Детальна інформація
python3 scripts/04_get_player_info.py 123456 --env qa

# З збереженням у файл
python3 scripts/04_get_player_info.py 123456 --env qa --output player_info.json
```

#### Створення бонусу

```bash
# Welcome бонус
python3 scripts/05_create_bonus.py --type welcome --trigger deposit --env qa

# Бонус для конкретного гравця
python3 scripts/05_create_bonus.py --type deposit --trigger promocode --client-id 123456 --env qa

# Перегляд шаблонів
python3 scripts/05_create_bonus.py --list-templates
```

#### Сценарії оркестратора

```bash
# Список доступних сценаріїв
python3 scripts/07_test_data_orchestrator.py --list

# Виконання сценарію
python3 scripts/07_test_data_orchestrator.py --scenario player_with_balance --env qa

# З тікетом
python3 scripts/07_test_data_orchestrator.py --scenario full_setup --env qa --ticket CT-727
```

## 📋 Доступні сценарії

| Сценарій | Опис | Кроки |
|----------|------|-------|
| `player_with_balance` | Гравець з балансом | create_player + setup_balance |
| `player_with_bonus` | Гравець з бонусом | create_player + balance + bonus |
| `player_kyc_pending` | Гравець з pending KYC | create_player (KYC manual) |
| `deposit_streak` | Гравець з 3 депозитами | create_player + 3 deposits |
| `high_roller` | Гравець з великим балансом | create_player + $1000 balance |
| `full_setup` | Повне налаштування | player + balance + deposit + bonus + info |

## 🔧 API Клієнти

### WebsiteApiClient
- **Базовий URL:** `https://websitewebapi.{env}.sofon.one`
- **Автентифікація:** Session Token в заголовку `Authorization`
- **Методи:** register_client, login, get_client_balance, get_games, get_active_bonuses

### BackOfficeApiClient
- **Базовий URL:** `https://adminwebapi.{env}.sofon.one`
- **Автентифікація:** Header `UserId: <adminUserId>`
- **Методи:** get_client_by_id, register_client, change_client_details, create_manual_payment, change_payment_status, create_bonus_campaign

### WalletApiClient
- **Базовий URL:** `https://wallet.{env}.sofon.one`
- **Автентифікація:** Не потрібна (відкритий API)
- **Методи:** get_balance, create_debit_correction (додає гроші ✅), create_credit_correction (знімає гроші ❌), get_transactions

### GraphQLClient
- **Базовий URL:** `https://minebit-casino.{env}.sofon.one/graphql`
- **Методи:** register_player (PlayerRegisterUniversal mutation)

## ⚠️ Важливі правила

### 1. Безпека в Production
- Всі скрипти автоматично позначають гравців як `IsTest = true`
- Для Prod середовища вимагається підтвердження дій
- Ніколи не виконуйте дії з реальними гравцями без перевірки

### 2. Інвертована логіка Wallet API
```python
# Додати гроші ✅
create_debit_correction(amount=100)  # credits balance

# Зняти гроші ❌
create_credit_correction(amount=50)  # debits balance
```

### 3. Депозити через BackOffice
1. `MakeManualRedirectPayment` - створити депозит
2. `Payment/ChangeStatus` → `MarkAsPaid` - підтвердити оплату

Обов'язково виконувати обидва кроки!

### 4. Логування тестових даних
Всі створені об'єкти зберігаються в `test_data_log.json` для подальшого очищення.

## 🧪 Інтеграція з Playwright

### Приклад fixture для гравця з балансом

```python
import pytest
import sys
from pathlib import Path

# Add test-data-scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "test-data-scripts" / "scripts"))

from create_test_player import create_test_player

@pytest.fixture
def test_player_with_balance(api_context):
    """Create test player with $100 balance."""
    player = create_test_player(
        env="qa",
        setup_balance=True,
        balance_amount=100
    )
    
    yield player
    
    # Optional: Cleanup after test
    # (Could mark as inactive or delete if API supports)
```

### Використання в тестах

```python
def test_deposit_flow(test_player_with_balance):
    """Test deposit functionality."""
    player = test_player_with_balance
    
    # Use player credentials
    assert player["clientId"]
    assert player["sessionToken"]
    
    # Navigate with authenticated session
    # ... test logic
```

## 📊 Вихідні файли

Скрипти автоматично створюють файли з результатами:

- `last_player.json` - Дані останнього створеного гравця
- `last_balance_operation.json` - Результат операції з балансом
- `last_deposit_flow.json` - Результат депозиту
- `last_player_info.json` - Інформація про гравця
- `last_bonus_creation.json` - Результат створення бонусу
- `scenario_*.json` - Результат виконання сценарію
- `test_data_log.json` - Загальний лог всіх операцій

## 🔄 Повідомлення про проблеми

Якщо виникли помилки:
1. Перевірте з'єднання з API (мережа, VPN)
2. Перевірте правильність `UserId` для BackOffice (560 для Prod, 1 для QA/Dev)
3. Перевірте, чи гравець позначений як `IsTest = true`
4. Перегляньте `test_data_log.json` для історії операцій

## 📝 TODO

- [ ] Додати скрипт очищення тестових даних
- [ ] Додати Playwright fixtures
- [ ] Додати інтеграцію з TestRail для створення тест-кейсів
- [ ] Додати генерація тестових даних для Lorypten (Solana)

---

**Автор:** BMW M5 (FamAssistant)  
**Дата створення:** 2026-03-03  
**Версія:** 1.0.0