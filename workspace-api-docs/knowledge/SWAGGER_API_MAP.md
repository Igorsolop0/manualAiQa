# Swagger API Endpoint Map

Complete reference of all platform APIs available for QA testing.
Last updated: 2026-03-19

## API Overview

| API | Base URL (QA) | Base URL (Prod) | Auth | Swagger |
|-----|---------------|-----------------|------|---------|
| BackOffice (adminwebapi) | `adminwebapi.qa.sofon.one` | `adminwebapi.prod.sofon.one` | `UserId` header | `/swagger/index.html` |
| Website (websitewebapi) | `websitewebapi.qa.sofon.one` | `websitewebapi.prod.sofon.one` | Bearer token / session | `/swagger/index.html` |
| CRM Gateway (Smartico) | `crmgateway.qa.sofon.one` | `crmgateway.prod.sofon.one` | `Api-UserId` + `Api-Key` headers | `/swagger/index.html` |
| Wallet | `wallet.qa.sofon.one` | `wallet.prod.sofon.one` | Internal (no auth header) | N/A |

---

## 1. BackOffice API (adminwebapi)

Admin-facing API for player management, bonus operations, payments, and platform configuration.

### Player Management (Client)
| Method | Endpoint | QA Use | Recipe |
|--------|----------|--------|--------|
| POST | `/api/Client/GetClients` | Query/search players by filters | — |
| POST | `/api/Client/GetClientById` | Get full player profile | — |
| POST | `/api/Client/GetClientConatctInfo` | Get player contact details | — |
| POST | `/api/Client/ChangeClientDetails` | Update player info (name, etc.) | — |
| POST | `/api/Client/EditClientEmail` | Change player email | — |
| POST | `/api/Client/EditClientKYC` | Modify KYC verification | — |
| POST | `/api/Client/ChangeClientPassword` | Reset player password | — |
| POST | `/api/Client/DeactivateClients` | Deactivate player accounts | — |
| PUT | `/api/clients/{clientId}/sticky-note` | Add admin notes to player | — |
| POST | `/api/Client/CreateDebitCorrection` | Credit player balance (admin path) | `credit-balance --method backoffice` |

### Bonus Management
| Method | Endpoint | QA Use | Recipe |
|--------|----------|--------|--------|
| POST | `/api/Bonus/GetBonuses` | List all bonuses with filters | `get-bonuses` |
| GET | `/api/clients/{clientId}/bonuses/active` | Get player's active bonuses | — |
| GET | `/api/clients/{clientId}/bonuses/not-finalized` | Get in-progress bonuses | — |
| POST | `/api/Bonus/GetBonusInfo` | Detailed bonus info | — |
| POST | `/api/Bonus/GetBonusById` | Get bonus by ID | — |
| POST | `/api/Bonus/GetBonusesForManualClaim` | List manually claimable bonuses | — |
| POST | `/api/Bonus/ClaimBonusForClients` | Award bonus to player(s) | — |
| POST | `/api/Bonus/CreateBonus` | Create new bonus | — |
| POST | `/api/Bonus/UpdateBonus` | Modify bonus settings | — |
| POST | `/api/Bonus/BulkUpdateBonuses` | Mass update bonuses | — |
| POST | `/api/Bonus/CloneBonus` | Duplicate a bonus | — |
| POST | `/api/Bonus/GetBonusTags` | List bonus tags | — |

### Bonus Triggers
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/api/Bonus/SaveTriggerSetting` | Configure bonus triggers |
| POST | `/api/Bonus/GetTriggerSettings` | List trigger configs |
| PUT | `/api/Bonus/AddTriggerToBonus` | Link trigger to bonus |
| DELETE | `/api/Bonus/RemoveTriggerFromBonus` | Unlink trigger |

### Bonus Packages
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET | `/api/BonusPackage/GetAll` | List bonus packages |
| POST | `/api/BonusPackage/Create` | Create package |
| DELETE | `/api/BonusPackage/Delete` | Remove package |

### Bonus Settings (Partner-level)
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET | `/api/v1/Partners/{partnerId}/BonusSettings` | Get partner bonus config |
| POST | `/api/v1/Partners/{partnerId}/BonusSettings` | Create bonus settings |
| PUT | `/api/v1/Partners/{partnerId}/BonusSettings/{id}` | Update bonus settings |

### Calendar Bonuses
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET | `/api/CalendarBonusSetting/GetAll` | List calendar bonuses |
| POST | `/api/CalendarBonusSetting/Create` | Create calendar bonus |
| PUT | `/api/CalendarBonusSetting/Update` | Modify calendar bonus |
| DELETE | `/api/CalendarBonusSetting/Delete/{calendarId}` | Remove calendar bonus |

### Free Spins
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET | `/api/Bonus/GetAvailableFreeSpinAmounts/{id}` | List free spin amounts |
| GET | `/api/Bonus/GetFreeSpinAmounts/{id}` | Get free spin quantities |
| PUT | `/api/Bonus/UpdateFreeSpinAmount/{id}` | Update free spin amount |

### Complimentary Points
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/api/Bonus/SaveComplimentaryPointRate` | Set point rates |
| POST | `/api/Bonus/GetComplimentaryPointRates` | Get point rates |
| POST | `/api/Bonus/ApplyComplimentaryPointRatesToAllCurrencies` | Apply rates globally |

### Affiliates
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/api/Affiliate/GetAvailableAffiliates` | List affiliates |
| POST | `/api/Bonus/GetAffiliateRefferal` | Get affiliate referral bonuses |

### Platform Config
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/api/Base/GetObjectTypes` | Get object type reference |
| POST | `/api/Base/GetTranslationEntries` | Get translations |
| POST | `/api/Base/SaveTranslationEntries` | Update translations |
| DELETE | `/api/Cache/Clear/clear` | Clear platform cache |

---

## 2. Website API (websitewebapi)

Client-facing API used by the casino website. All endpoints require `{partnerId}` path param.

### Authentication & Registration
| Method | Endpoint | QA Use | Recipe |
|--------|----------|--------|--------|
| POST | `/{partnerId}/api/Main/RegisterClient` | Register new player | `create-player` (via GraphQL) |
| POST | `/{partnerId}/api/Main/LoginClient` | Login (encrypted creds) | — |
| POST | `/{partnerId}/api/Main/Login` | Login (standard) | `login-player` |
| POST | `/{partnerId}/api/Main/QuickSmsRegistration` | SMS registration | — |

### Account Management
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET/POST | `/{partnerId}/api/Main/GetClientByToken` | Get profile by session token |
| GET/POST | `/{partnerId}/api/Main/GetClientBalance` | Check player balance |
| POST | `/{partnerId}/api/Main/SendRecoveryToken` | Trigger password recovery |
| POST | `/{partnerId}/api/Main/RecoverPassword` | Execute password reset |
| POST | `/{partnerId}/api/Main/ClientUploadImage` | Upload document/image |

### Products & Games
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET/POST | `/{partnerId}/api/Main/GetProductUrl` | Get game launch URL |
| GET/POST | `/{partnerId}/api/Main/CheckProductAvailability` | Check game availability |

### Promotions & Reference
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/{partnerId}/api/Main/GetPromotions` | List active promotions |
| GET/POST | `/{partnerId}/api/Main/GetPaymentMethodTypesEnum` | List payment methods |
| GET/POST | `/{partnerId}/api/Main/GetBonusStatusesEnum` | Bonus status reference |
| GET/POST | `/{partnerId}/api/Main/GetRegions` | Territory list |

### Generic
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/{partnerId}/api/Main/ApiRequest` | Dynamic operation handler |

### Health
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET/POST | `/hc/ping` | Basic health check |

**Notes:**
- `partnerId` for Minebit = 5, Turabet = 8, Betazo = 10, Motor = 12
- Deprecated `/v1/` endpoints exist but should not be used for new tests
- Auth: session token in `RequestBase.Token` field

---

## 3. CRM Gateway (Smartico)

Smartico CRM integration for bonus campaigns, promo codes, and gamification.

### Bonus Operations
| Method | Endpoint | QA Use | Recipe |
|--------|----------|--------|--------|
| POST | `/api/CRM/ActivatePromocode` | Activate bonus by promo code | `activate-bonus --promocode X` |
| POST | `/api/CRM/ClaimToCampaignBonus` | Claim campaign bonus for player | `activate-bonus --bonus-id X` |
| POST | `/api/CRM/GetBonusCampaigns` | List bonus campaigns | `activate-bonus --list-campaigns` |
| POST | `/api/CRM/DeductClientBalance` | Deduct player balance (store items) | — |
| POST | `/api/CRM/AssignClientToLevel` | Assign player to loyalty level | — |

### Game Data
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET | `/api/CRM/GetGames` | List games for Smartico |
| POST | `/api/CRM/GetGameProviders` | List game providers |

### Promo Code Validation
| Method | Endpoint | QA Use |
|--------|----------|--------|
| POST | `/{partnerId}/api/v1/promo-codes/{promoCode}` | Validate promo code |

### Health
| Method | Endpoint | QA Use |
|--------|----------|--------|
| GET/POST | `/ping` | Health check |
| GET/POST | `/build` | Build version |

**Auth:** All endpoints require `Api-UserId: 560` and `Api-Key: ihorsnextcodebo` headers.

---

## QA-Critical Endpoints (Priority)

Endpoints most frequently needed for test preparation and validation:

### Data Preparation (before tests)
1. **Create player** → GraphQL `PlayerRegisterUniversal` (recipe: `create-player`)
2. **Credit balance** → Wallet `/api/v1/transaction/correction/debit` or BO `/api/Client/CreateDebitCorrection` (recipe: `credit-balance`)
3. **Setup full player** → Composite (recipe: `setup-test-player`)
4. **Activate bonus** → CRM `/api/CRM/ActivatePromocode` (recipe: `activate-bonus`)

### State Verification (during/after tests)
1. **Check balance** → Wallet `/api/v1/balance/{playerId}/{currency}` or Website `GetClientBalance`
2. **Check active bonuses** → BO `/api/clients/{clientId}/bonuses/active`
3. **Get player profile** → BO `/api/Client/GetClientById`
4. **List promotions** → Website `GetPromotions`

### Test Infrastructure
1. **Health checks** → All APIs have `/ping` or `/hc/ping`
2. **Cache clear** → BO `/api/Cache/Clear/clear` (useful when testing config changes)

---

## Potential New Recipes

Endpoints that could become recipes when needed:

| Candidate | Endpoint | Trigger |
|-----------|----------|---------|
| `claim-bonus` | BO `ClaimBonusForClients` | When test needs manual bonus award via BackOffice |
| `check-player-bonuses` | BO `clients/{id}/bonuses/active` | Pre-check bonus state before/after test |
| `get-player-profile` | BO `GetClientById` | Verify player data changes |
| `validate-promocode` | CRM `promo-codes/{code}` | Check if promo code is valid before using |
| `get-game-url` | Website `GetProductUrl` | Launch game for testing (Clawver needs URL) |
| `deduct-balance` | CRM `DeductClientBalance` | Clean up player balance after test |
| `reset-password` | Website `RecoverPassword` | Test password recovery flow |
