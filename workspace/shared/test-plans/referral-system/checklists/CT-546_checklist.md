# Test Checklist: CT-546 — BE: Commission Templates

**Status:** Open
**Component:** Backend Commission Configuration
**Priority:** High

---

## 🎯 Ticket Summary

Create a commission configuration system in the referral service that determines what commission percentage (coefficient) applies per game category or individual game. The template structure mirrors TemplateBonus → TemplateProductBonus → ProductStructure from CorePlatform.

---

## ✅ Acceptance Criteria Checklist

### Product Structure Tables

- [ ] ReferralProductStructure table created
  - [ ] Id (int, PK)
  - [ ] PartnerId, Name, ProductId, ParentId, Level
- [ ] ReferralProductStructureFlat table created
  - [ ] PathToRoot[] for efficient ancestor lookup
- [ ] SQL sync script copies from CorePlatform DB
- [ ] Sync script is idempotent (safe to re-run)
- [ ] Sync script rebuilds ReferralProductStructureFlat

### Commission Template Tables

- [ ] ReferralCommissionTemplate table created
  - [ ] Id, PartnerId, Name, IsActive, CreatedAt, UpdatedAt
  - [ ] One active template per partner enforced
- [ ] ReferralCommissionTemplateProduct table created
  - [ ] Id, TemplateId, ProductStructureId, CoefficientPercent
  - [ ] Cascade delete on template deletion
  - [ ] Index on ProductStructureId, TemplateId
  - [ ] CoefficientPercent range: 0–100

### Commission Resolution

- [ ] Algorithm walks PathToRoot from game to root
- [ ] First ancestor with template entry → use its CoefficientPercent
- [ ] Game-level override > Category > Root
- [ ] Multi-category game resolution documented:
  - [ ] Uses coefficient from first category (lowest ProductStructureId)

### BO API Endpoints

- [ ] GET /api/commission-templates/{partnerId} — list templates
- [ ] GET /api/commission-templates/{id} — single template
- [ ] GET /api/commission-templates/{id}/product-tree — returns product tree with coefficients
- [ ] POST /api/commission-templates/{id}/import-csv — bulk import
- [ ] GET /api/commission-templates/{id}/export-csv — export coefficients

---

## 🧪 Test Scenarios

### 1. Product Structure Sync

- [ ] Verify that running sync script for first time copies all products
- [ ] Verify that re-running sync script produces no errors and no duplicates
- [ ] Verify that adding new game in CorePlatform and syncing makes it appear in ReferralProductStructure
- [ ] Verify that moving game to new category and syncing updates ProductStructureFlat correctly

### 2. Template CRUD

- [ ] Verify that creating template with valid data (POST) creates template successfully
- [ ] Verify that activating template (IsActive = true) enforces only one active template per partner
- [ ] Verify that deactivating template (IsActive = false) restores previous active or leaves no active
- [ ] Verify that deleting template cascades deletion to products

### 3. Coefficient Assignment

- [ ] Verify that assigning 15% to specific game makes game use 15%
- [ ] Verify that assigning 5% to category makes games in category use 5% (if no game override)
- [ ] Verify that game override (Game 15%, Category 5%) results in game using 15%
- [ ] Verify that game/category with no entry uses parent or root coefficient

### 4. Coefficient Resolution

- [ ] Verify that game-level override (Game 20%, Category 10%) uses 20% (game level)
- [ ] Verify that category-level only (Game has no entry, Category 10%) uses 10% (category level)
- [ ] Verify that no game/category entry uses root coefficient
- [ ] Verify that multi-category game (IDs 100, 200) uses coefficient from category with lowest ID (100)

### 5. CSV Import/Export

- [ ] Verify that GET /export-csv returns CSV with ProductStructureId, CoefficientPercent
- [ ] Verify that POST /import-csv with valid data updates all coefficients
- [ ] Verify that POST /import-csv with invalid format returns error with line number
- [ ] Verify that POST /import-csv with 150% (out of range) returns validation error

---

## 🧪 Business Logic Tests (PM Requirements)

### From CRYPTO-70 Description:

- [ ] Verify that Slots games commission uses 15% coefficient
- [ ] Verify that Live casino games commission uses 5% coefficient
- [ ] Verify that Instant games commission uses 5% coefficient

---

## 🔗 Integration Points

### Commission Calculation (CT-549)

- [ ] Templates loaded and cached (TTL 5m)
- [ ] Resolution happens during bet processing
- [ ] Cache invalidated on template update

### Product Structure

- [ ] Sync script scheduled (DevOps)
- [ ] Manual sync trigger available

---

## 🔗 Dependencies

**Depends on:** CT-540 (Services)

**Blocks:** CT-549 (Processing Bets needs templates for calculation)

---

## 📝 Notes

- Test with large product catalogs (1000+ games)
- Verify cache invalidation works correctly
- Test PathToRoot resolution with deep hierarchies

---

**Test Type:** Backend Configuration
**Estimated Effort:** 1 day
**Test Environment:** QA
