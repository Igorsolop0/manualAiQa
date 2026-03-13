# Test Checklist: CT-674 — FE: Referral System First Page Layout

**Status:** Open
**Component:** Frontend UI
**Priority:** Medium

---

## 🎯 Ticket Summary

Implement the layout for the first page of the referral system according to Figma design. All conditions and content blocks must be implemented as defined.

---

## ✅ Acceptance Criteria Checklist

### Layout Components

- [ ] Total referrals / Paid to partners block
  - [ ] Values configurable by content managers (not hardcoded)
  - [ ] Displayed correctly on desktop
  - [ ] Displayed correctly on mobile
- [ ] "How much can you earn" block
  - [ ] Static content (first version)
  - [ ] Value: 0.00135 BTC
- [ ] "Get my referral link" button
  - [ ] Navigates to referral page
  - [ ] Visible on desktop
  - [ ] Visible on mobile

### Design Compliance

- [ ] Layout matches Figma design exactly
  - [ ] Figma link: https://www.figma.com/design/MiFoPgwYdOfyHOYQGgGmkF/Referal---Minebit
- [ ] Spacing matches design
- [ ] Colors match design
- [ ] Typography matches design

### Responsive Design

- [ ] Desktop layout (1920px)
- [ ] Desktop layout (1366px)
- [ ] Tablet layout (768px)
- [ ] Mobile layout (375px)
- [ ] Mobile layout (320px)

---

## 🧪 Test Scenarios

### 1. Layout Rendering

- [ ] Verify that desktop layout on Chrome matches Figma design (MacBook Air)
- [ ] Verify that desktop layout on Safari matches Figma design (MacBook Air)
- [ ] Verify that mobile layout on Chrome matches Figma design (Pixel 7)
- [ ] Verify that mobile layout on Safari matches Figma design (iPhone 15)

### 2. Content Display

- [ ] Verify that "Total referrals" value is displayed (from CMS, not hardcoded)
- [ ] Verify that "Paid to partners" value is displayed (from CMS, not hardcoded)
- [ ] Verify that "How much can you earn" shows "0.00135 BTC"

### 3. Navigation

- [ ] Verify that "Get my referral link" button navigates to referral page
- [ ] Verify that deep link to page loads correctly

### 4. CMS Configuration (Non-Hardcoded)

- [ ] Verify that updating total referrals in CMS reflects on frontend
- [ ] Verify that updating paid to partners in CMS reflects on frontend

---

## 🧪 Cross-Browser Testing

- [ ] Verify that layout renders correctly on Chrome (latest)
- [ ] Verify that layout renders correctly on Safari (latest)
- [ ] Verify that layout renders correctly on Firefox (latest)
- [ ] Verify that layout renders correctly on Edge (latest)
- [ ] Verify that layout renders correctly on Mobile Chrome
- [ ] Verify that layout renders correctly on Mobile Safari

---

## 📐 Visual Regression

- [ ] Verify that screenshot comparison with Figma export shows no visual differences
- [ ] Verify that layout adapts correctly at all responsive breakpoints

---

## 🔗 Dependencies

**Depends on:** CT-541 (API for stats), CT-678 (Referral page destination)

**Blocks:** None (entry point to referral system)

---

## 📝 Notes

- Focus on visual accuracy (Figma compliance)
- Test with different screen sizes
- Verify CMS values are not hardcoded

---

**Test Type:** Frontend UI
**Estimated Effort:** 1 day
**Test Environment:** QA
