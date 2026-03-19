# Cipher Recipe Library

Reusable data preparation and API validation recipes.
All recipes use `env_config.py` for shared environment configuration.

## Quick Reference

| Recipe | Command | Purpose |
|--------|---------|---------|
| create-player | `python3 recipes/create_player.py --env qa` | Register new test player |
| login-player | `python3 recipes/login_player.py --email X --env qa` | Login and get fresh token |
| credit-balance | `python3 recipes/credit_balance.py --player-id X --amount 100` | Add money (wallet or BO) |
| deposit-flow | `python3 recipes/deposit_flow.py --player-id X --amount 100` | Full deposit via payment system |
| setup-test-player | `python3 recipes/setup_test_player.py --env qa --balance 500` | Create player + credit (composite) |
| get-bonuses | `python3 recipes/get_bonuses.py --env prod` | List active bonuses |
| activate-bonus | `python3 recipes/activate_bonus.py --client-id X --promocode Y` | Activate bonus via Smartico CRM |

## Environment Config

All recipes share `recipes/env_config.py`:

```python
from env_config import get_env, get_brand

get_env("qa")    # → graphql, website_api, backoffice_api, wallet_api, crm_gateway URLs
get_brand("minebit")  # → partner_id: 5, currency: USD
```

Supported environments: `qa`, `prod`
Supported brands: `minebit` (id:5), `turabet` (id:8), `betazo` (id:10), `motor` (id:12)

## Recipe Details

### create-player
```bash
python3 recipes/create_player.py --env qa --brand minebit --prefix ct-798
```
- Registers via GraphQL `PlayerRegisterUniversal` mutation
- Auto-generates email: `{prefix}-{timestamp}-{random}@nextcode.tech`
- Returns: `player_id`, `email`, `password`, `session_token`

### login-player
```bash
python3 recipes/login_player.py --email test@nextcode.tech --env qa
```
- Login via Website REST API `/api/v3/Client/Login`
- Returns: `session_token`, `player_id`, `balance`

### credit-balance
```bash
# Via Wallet API (fast, direct)
python3 recipes/credit_balance.py --player-id 123 --amount 100 --method wallet

# Via BackOffice API (safer, admin path)
python3 recipes/credit_balance.py --player-id 123 --amount 100 --method backoffice
```
- Wallet: `/api/v1/transaction/correction/debit` (fastest)
- BackOffice: `/api/Client/CreateDebitCorrection` (fallback if wallet fails)
- Verifies balance after credit
- Known issue: Wallet API may return 500 on QA, use `--method backoffice` as fallback

### deposit-flow
```bash
python3 recipes/deposit_flow.py --player-id 123 --amount 100 --env qa
```
- 3-step flow: create deposit request → mark as paid → verify balance
- Uses BackOffice API `MakeManualRedirectPayment` + `ChangeStatus`
- Simulates real payment flow (unlike direct credit)

### setup-test-player (composite)
```bash
python3 recipes/setup_test_player.py --env qa --balance 500 --prefix ct-798
```
- Combines: `create-player` → `credit-balance`
- Auto-fallback: wallet → backoffice if wallet fails
- Returns full player context ready for testing

### get-bonuses
```bash
python3 recipes/get_bonuses.py --env prod --brand minebit
python3 recipes/get_bonuses.py --env qa --all  # include inactive
```
- Retrieves bonus inventory from BackOffice API
- Returns: id, name, type, status, bet_real_percent, wagering_multiplier

### activate-bonus (CRM Gateway / Smartico)
```bash
# Activate by promo code
python3 recipes/activate_bonus.py --client-id 123 --promocode WELCOME100 --env qa

# Claim campaign bonus
python3 recipes/activate_bonus.py --client-id 123 --bonus-id 8301 --env qa

# List available campaigns
python3 recipes/activate_bonus.py --list-campaigns --env qa
```
- Uses CRM Gateway (Smartico) API
- Auth: `Api-UserId: 560` + `Api-Key` (configured in `env_config.py`)
- Supports: promo code activation, campaign bonus claim, campaign listing
- Returns: success status, API response

## How Nexus Uses Recipes

In task files, Nexus specifies data prep needs:

```markdown
**Data prep (Cipher):**
- `setup-test-player --env qa --balance 500 --prefix ct-798`
- Save credentials to `workspace/shared/credentials/CT-798-player.json`
```

Cipher executes the recipe and stores the result for Clawver.

## Adding New Recipes

1. Create `recipes/new_recipe.py`
2. Import from `env_config` for URLs/headers
3. Accept `env` and `brand` as parameters
4. Return structured dict with results
5. Add CLI interface with `argparse`
6. Add entry to this table
7. Test: `python3 recipes/new_recipe.py --env qa`

## Legacy Scripts

Old scripts in `scripts/` are preserved for reference but should not be used for new tasks.
Use recipes instead — they have proper error handling, env config, and CLI interface.
