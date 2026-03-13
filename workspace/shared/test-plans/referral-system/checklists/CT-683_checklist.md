# Test Checklist: CT-683 — FE: Share Your Referral Links Layout

**Status:** Open
**Component:** Frontend UI
**Priority:** Medium

---

## 🎯 Ticket Summary

Implement the layout of the "Share your referral links" block according to Figma design. This task covers UI layout only — no business logic, validation, or data handling.

---

## ✅ Acceptance Criteria Checklist

### Layout Structure

- [ ] Referral link field displayed
- [ ] Referral code field displayed
- [ ] Copy actions for both fields
- [ ] Layout matches Figma design exactly
  - [ ] Figma link: https://www.figma.com/design/MiFoPgwYdOfyHOYQGgGmkF/Referal---Minebit

### Design Compliance

- [ ] Spacing matches design
- [ ] Colors match design
- [ ] Typography matches design
- [ ] Icons match design (copy icons)

### Responsive Design

- [ ] Desktop layout
- [ ] Mobile layout

---

## 🧪 Test Scenarios

### 1. Visual Layout

| Test Case | Device | Expected Result |
|-----------|--------|-----------------|
| Desktop layout | MacBook Air | Layout matches Figma |
| Mobile layout | Pixel 7 | Layout matches Figma |

### 2. Component Presence

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Referral link field visible | View block | Field present |
| Referral code field visible | View block | Field present |
| Copy buttons visible | View block | Buttons present |

### 3. Responsive Behavior

| Test Case | Viewport | Expected Result |
|-----------|----------|-----------------|
| Desktop 1920px | 1920px wide | Full layout |
| Tablet 768px | 768px wide | Adapted layout |
| Mobile 375px | 375px wide | Mobile layout |
| Mobile 320px | 320px wide | No overflow |

---

## 📐 Visual Regression

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Screenshot comparison | Compare with Figma | No differences |

---

## 🔗 Dependencies

**Depends on:** None (layout only, no logic)

**Related:** CT-678 (Form implementation adds logic to this layout)

---

## 📝 Notes

- This is a **layout-only** ticket — no interaction testing needed
- Focus on visual accuracy
- Business logic tested in CT-678

---

**Test Type:** Frontend UI (Layout)
**Estimated Effort:** 4 hours
**Test Environment:** QA
