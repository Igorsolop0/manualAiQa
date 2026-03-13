# Test Checklist: CT-678 — FE: Share Your Referral Links Form

**Status:** In Progress
**Component:** Frontend UI
**Priority:** Medium

---

## 🎯 Ticket Summary

Implement a new "Share your referral links" form according to Figma design. The form must display two fields with copy functionality: Referral link and Referral code. Both fields must be read-only with copy capability.

---

## ✅ Acceptance Criteria Checklist

### Form Fields

- [ ] Referral link field
  - [ ] Read-only (cannot edit)
  - [ ] Copy button works
  - [ ] Value from backend API
- [ ] Referral code field
  - [ ] Read-only (cannot edit)
  - [ ] Copy button works
  - [ ] Value from backend API

### Copy Functionality

- [ ] Copy button on referral link
  - [ ] Click copies to clipboard
  - [ ] Visual feedback (e.g., "Copied!" tooltip)
- [ ] Copy button on referral code
  - [ ] Click copies to clipboard
  - [ ] Visual feedback

### Default Values

- [ ] Default referral link generated on registration
- [ ] Default referral code generated on registration
- [ ] Backend provides values to display

### Navigation

- [ ] "About referral system" link returns to starting page
- [ ] Promo materials link (out of scope for now, but placeholder exists)

### Design Compliance

- [ ] Layout matches Figma design
  - [ ] Figma link: https://www.figma.com/design/MiFoPgwYdOfyHOYQGgGmkF/Referal---Minebit
- [ ] Spacing, colors, typography match design

### Responsive Design

- [ ] Desktop layout
- [ ] Mobile layout

---

## 🧪 Test Scenarios

### 1. Field Display

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Referral link displayed | Open form | Link visible and populated |
| Referral code displayed | Open form | Code visible and populated |
| Fields are read-only | Try to type in fields | Cannot edit |

### 2. Copy Functionality

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Copy referral link | Click copy button | Link copied to clipboard |
| Copy referral code | Click copy button | Code copied to clipboard |
| Copy feedback | After copy | Visual feedback shown (e.g., "Copied!") |

### 3. Clipboard Verification

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Paste referral link | Copy, paste in text editor | Exact link text |
| Paste referral code | Copy, paste in text editor | Exact code text |

### 4. Navigation

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| About referral system link | Click link | Returns to starting page |
| Back navigation | Browser back button | Returns to previous page |

### 5. Responsive Design

| Test Case | Device | Expected Result |
|-----------|--------|-----------------|
| Desktop layout | MacBook Air | Form matches Figma |
| Mobile layout | Pixel 7 | Form matches Figma, copy buttons accessible |

---

## 🧪 Cross-Browser Testing

- [ ] Chrome (desktop + mobile)
- [ ] Safari (desktop + mobile)
- [ ] Firefox
- [ ] Edge

---

## 🔗 API Integration

### Required Endpoint: GET /api/referral/defaultCampaign

- [ ] Returns referral code
- [ ] Response includes referral link (constructed from code)
- [ ] Error handling if API fails

---

## 🔗 Dependencies

**Depends on:** CT-541 (API endpoint for default campaign)

**Blocks:** None

---

## 📝 Notes

- Test clipboard permissions (some browsers restrict clipboard access)
- Verify copy works on mobile (touch events)
- Test with long referral links (overflow handling)

---

**Test Type:** Frontend UI
**Estimated Effort:** 4 hours
**Test Environment:** QA
