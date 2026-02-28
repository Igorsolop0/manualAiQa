# CRYPTO-2: Bonus Page Feature - Comprehensive Analysis

**Date Created:** 2026-02-28
**Project:** NextCode - Minebit Casino
**Ticket ID:** CRYPTO-2
**Status:** Ready for BA
**Priority:** URGENT
**Type:** Epic

---

## 📋 Executive Summary

CRYPTO-2 is a major Epic for implementing a comprehensive Bonus Page for Minebit Casino. This involves complete revamp of how bonuses are displayed, managed, and claimed by users. The feature includes Welcome Pack redesign, Special Bonuses, Regular Bonuses, and integration with Smartico for bonus management.

**Key Architectural Challenge:** Welcome Pack Revamp requires significant BE changes to support strict bonus sequencing, manual claiming, and real-time wagering tracking.

---

## 🎯 CRYPTO-2 Main Ticket Details

### Basic Information
- **Assignee:** Galadriel
- **Reporter:** Tetiana Ho
- **Created:** 389 days ago
- **Design:** [Figma Link](https://www.figma.com/design/qkzG2IGMeL6JEpJSmIEQxE/Minebit--Workfile-?node-id=12703-14504&t=ZliG8ig2KmFswxCd-1)

### Key Requirements (from Jira Description)

The Bonus Page feature includes:

1. **Join Now Button** → Opens registration form
2. **Bonus Widget in Header** → Shows bonus status (frontend, not Smartico widget)
3. **Info Tooltips** → Four template modal types for bonus details
4. **Calendar of Bonuses** → Weekly/Monthly cashback distribution
5. **Daily Quests Section** → Separate task (CRYPTO-24)
6. **Welcome Pack Revamp** → 4-step sequential bonus system
7. **Special Bonuses** → Rakeback, Cashback, Weekly, Monthly
8. **Regular Bonuses** → Deposit, Freespins, Reload, Spin
9. **FAQ Section** → For unauthorized and authorized users

### Initial Estimates
- BE: 80h
- FE: 80h

---

## 🔄 Documentation Review

⚠️ **Note:** Confluence page at https://next-t-code.atlassian.net/wiki/x/YADOBw is not accessible via web_fetch (requires authentication). Analysis below is based on Jira ticket content and comments.

### Gaps in Documentation

From the extensive comment thread between FE team (Meowfia) and Product (Danylo Ayaks), several clarifications were needed:

1. **Bonus Widget:** Confirmed this is NOT Smartico widget, but frontend implementation with Smartico API integration
2. **Modals:** 4 modal templates needed (Deposit/FS, Special bonuses, Calendar rules, Success popups)
3. **Calendar Navigation:** Arrow scrolling behavior (week vs month) was debated and refined
4. **Button States:** Multiple states for "Play game", "Play", "Go to wagering" needed clarification
5. **Daily Quests:** Separately documented in CRYPTO-24
6. **Claim Success:** Two drawer/modal variants (mobile vs desktop) discussed

### What We Learned from Documentation Review

The documentation provided by Danylo Ayaks clarifies:

**Bonus States (FNL Cards):**
- Waiting for deposit
- Wagering (with progress bar)
- Awaiting for claim
- Available for activation
- Claimed / Expired

**Welcome Pack Logic:**
- 4 strict sequential bonuses
- Timers: Activation time (3 days) + Wagering time (5 days)
- Manual claim required after wagering
- Next bonus only available after previous is finished

---

## 🧩 Linked Tickets Structure

### ✅ Completed Tickets

| Ticket | Summary | Status | Notes |
|---------|----------|--------|-------|
| **CT-27** | (CRYPTO-2) [FE] Bonus Modals | **Done** | 2 modal templates created, cancel bonus action implemented |
| **CT-29** | (CRYPTO-2) [FE] Other Bonuses and FAQ Sections | **Done** | Other bonuses (Daily Quests, Personal Bonus, Birthday, Bonus For Levels) + FAQ |
| **CRYPTO-24** | Quests (FE+Smartico) | **Closed** | Daily Quests page, separate from CRYPTO-2 |
| **CT-48** | [BE CAB] 6. Track and store history of bonus-related events | **Done** | ClientBonusHistory table created, status tracking implemented |
| **CT-68** | [BE, CorePlatform] 1 Create API endpoint for manual bonus claim | **Done** | `POST /Bonus/ClaimBonus/{clientBonusId}` endpoint created |

### ⏸️ On Hold / Blocked

| Ticket | Summary | Status | Blocking Issue |
|---------|----------|--------|----------------|
| **CT-36** | (CRYPTO-2)[BE] Welcome Pack Revamp | **HOLD** | Largest architectural change, needs validation from Galadriel |
| **CT-47** | [BE] Timers for Welcome bonuses | **Open** | Blocked by CT-36 |

### 🚀 In Progress / Ready for QA

| Ticket | Summary | Status | Dependencies |
|---------|----------|--------|-------------|
| **CRYPTO-497** | Personal Account on Bonus page | **Development** | CT-58 (Done), CT-657 (Testing), CT-664 (Done), CT-724 (Done) |
| **CRYPTO-259** | [Change request] Display turnover immediately | **Ready for BA** | No reload required after deposit |

### 🎬 Ready for Release

| Ticket | Summary | Status | Dependencies |
|---------|----------|--------|-------------|
| **CRYPTO-459** | (CRYPTO-2) Regular bonuses Section | **Release** | CT-45 (Done), CT-44 (Done), CT-558 (Done), CT-559 (Done), CT-61 (Done), CT-736 (Done), CT-756 (Done) |
| **CRYPTO-461** | (CRYPTO-2) Special bonuses Section | **Release** | CT-62 (Done), CT-40 (Done), CT-560 (Done) |

### ❌ Canceled

| Ticket | Summary | Status | Reason |
|---------|----------|--------|--------|
| **CRYPTO-460** | (CRYPTO-2) Aggregation Data | **Canceled** | Merged into CRYPTO-497; CT-43, CT-64 no longer relevant |

---

## 🏗️ Task Dependency Tree

```
CRYPTO-2 (Main Epic)
├── FE Tasks (Completed)
│   ├── CT-27: Bonus Modals ✅
│   └── CT-29: Other Bonuses + FAQ ✅
│
├── Daily Quests (Separate Epic)
│   └── CRYPTO-24: Quests (FE+Smartico) ✅
│
├── Welcome Pack Revamp (BE Focus - CRITICAL PATH)
│   ├── CT-36: Welcome Pack Revamp ⏸️ HOLD
│   │   ├── CT-47: Timers ⏸️ Open (Blocked by CT-36)
│   │   ├── CT-48: Bonus History ✅
│   │   └── CT-68: Manual Claim API ✅
│   │
│   ├── Subtasks of CT-36:
│   │   ├── CT-47: [Open] - Timers
│   │   ├── CT-48: [Done] - History tracking
│   │   ├── CT-49: [Open] - ?
│   │   ├── CT-53: [Open] - ?
│   │   ├── CT-68: [Done] - Manual claim API
│   │   ├── CT-78: [Canceled]
│   │   ├── CT-79: [Canceled]
│   │   ├── CT-83: [Done]
│   │   ├── CT-84: [Done]
│   │   ├── CT-85: [Done]
│   │   ├── CT-86: [Done]
│   │   ├── CT-87: [Done]
│   │   └── CT-89: [Open]
│
├── Regular Bonuses Section
│   └── CRYPTO-459: Regular bonuses 🎬 Release
│       ├── CT-45: Regular Bonuses ✅
│       ├── CT-44: Bonus Cards ✅
│       ├── CT-558: [Done]
│       ├── CT-559: [Done]
│       ├── CT-61: [Done]
│       ├── CT-736: Regular Bonuses prod config ✅
│       └── CT-756: [Done]
│
├── Special Bonuses Section
│   └── CRYPTO-461: Special bonuses 🎬 Release
│       ├── CT-62: [Done]
│       ├── CT-40: [Done]
│       └── CT-560: Special bonuses redesign ✅
│
├── Bonus Page Core Features
│   └── CRYPTO-497: Personal Account on Bonus page 🚀 Development
│       ├── CT-58: Profile section ✅
│       ├── CT-664: [Done]
│       ├── CT-657: Bonus tags 🔄 Testing
│       └── CT-724: [Done]
│
└── Change Requests
    └── CRYPTO-259: Turnover updates without reload ✅ Ready for BA
```

---

## 🔍 Subtasks Analysis (CT-36 - Welcome Pack Revamp)

### Current Status: ⏸️ HOLD
**Why on Hold:** Requires additional architecture validation due to large impact. Requested by Galadriel for BA review.

### Completed Subtasks:
- CT-44: Done ✅
- CT-45: Done ✅
- CT-68: Done ✅ (Manual claim API)
- CT-78: Canceled
- CT-79: Canceled
- CT-83: Done ✅
- CT-84: Done ✅
- CT-85: Done ✅
- CT-86: Done ✅
- CT-87: Done ✅

### Open Subtasks:
- CT-47: [Open] - Timers for Welcome bonuses (depends on CT-53)
- CT-48: [Done] - History tracking
- CT-49: [Open] - ?
- CT-53: [Open] - ?
- CT-89: [Open] - ?

### Key Implementation Requirements (from CT-36):

**Welcome Pack States:**
1. **Awaiting Deposit** - First bonus auto-activated after registration
2. **Activated / Wagering** - After deposit, shows progress + timer
3. **Awaiting for Claim** - After wagering complete, manual claim required
4. **Available for Activation** - Subsequent bonuses, shows "Activate" button
5. **Claimed / Expired / Cancelled**

**Timer Logic:**
- **Bonus Activation Time:** 3 days (configurable) to activate bonus
  - Starts from registration (1st bonus) or previous bonus completion
- **Bonus Wagering Time:** 5 days (configurable) to complete wagering
  - Starts after successful deposit

**Critical Rules:**
- Strict sequential order (can't activate bonus #2 before #1 is finished)
- Only ONE active bonus at a time
- Manual claim required after wagering
- Blocked from activating new bonus until current is claimed

---

## 🎨 FE Implementation Summary

### Completed Features:

**CT-27 - Bonus Modals:**
- 2 modal templates (Deposit/FS + Special bonuses)
- Cancel bonus action with confirmation popup
- Configurable content via Strapi
- Game slider for eligible games
- Rich text for T&C

**CT-29 - Other Bonuses + FAQ:**
- 4 non-clickable cards (Daily Quests, Personal Bonus, Birthday Bonus, Bonus For Levels)
- FAQ section for authorized users
- Images, titles, descriptions

**CT-36 FE Part (Documentation):**
- Welcome Pack card states and FNL card states documented
- All bonus states visually defined in Figma
- Timer display requirements specified

---

## 🤔 Clarifying Questions

### For Galadriel (BE Team Lead):

1. **CT-36 Architecture Validation:**
   - What specific architecture validation is needed for Welcome Pack Revamp?
   - Is there a concern about backwards compatibility with existing active bonuses?
   - Are there performance concerns with real-time wagering tracking?

2. **Open Subtasks (CT-49, CT-53, CT-89):**
   - What's the scope of CT-49?
   - What's the scope of CT-53? (CT-47 mentions it as a dependency)
   - What's the scope of CT-89?

3. **CT-47 Timers:**
   - When can CT-47 be unblocked? (Currently depends on CT-53)
   - Are the timer implementation requirements clear?

### For Danylo Ayaks (Product):

1. **Confluence Documentation:**
   - Can we get direct access to the Confluence page https://next-t-code.atlassian.net/wiki/x/YADOBw?
   - Or can the key requirements be summarized in a new ticket comment?

2. **Calendar Bonuses:**
   - Are Weekly and Monthly bonuses still implemented via Smartico?
   - What's the exact schedule for crediting (Saturday for Weekly? 1st day of month for Monthly?)
   - How should the calendar display past distributed bonuses?

3. **Daily Quests:**
   - Are Daily Quests part of CRYPTO-2 or completely separate (CRYPTO-24)?
   - Should Daily Quests appear on the Bonuses page?

### For QA Team:

1. **CRYPTO-259 (Turnover Display):**
   - Should this be tested alongside CRYPTO-2 release?
   - Is it a separate deployment?

2. **Test Environment:**
   - DEV environment was broken in CT-68 testing. Is it stable now?
   - When can we start regression testing for Welcome Pack?

---

## 📊 Progress Summary

### Overall CRYPTO-2 Progress: **~65%**

**Completed Components:**
- ✅ Bonus Modals (CT-27)
- ✅ Other Bonuses + FAQ (CT-29)
- ✅ Daily Quests (CRYPTO-24 - separate)
- ✅ Special Bonuses Section (CRYPTO-461 - Ready for Release)
- ✅ Regular Bonuses Section (CRYPTO-459 - Ready for Release)
- ✅ Manual Claim API (CT-68)
- ✅ Bonus History Tracking (CT-48)

**In Progress / Blocked:**
- ⏸️ Welcome Pack Revamp (CT-36 - HOLD)
- 🚀 Personal Account on Bonus Page (CRYPTO-497 - Development)
- ⏸️ Timers for Welcome Bonuses (CT-47 - Open, blocked)

**Completed / Done in MEMORY.md:**
- CT-727 - Recent wins widget ✅ Done
- CT-736 - Regular Bonuses prod config ✅ Done
- CT-560 - Special bonuses redesign ✅ Done

---

## 🚨 Critical Path

**The critical path for CRYPTO-2 completion:**

1. **CT-36 (Welcome Pack Revamp)** - Must exit HOLD status
   - Depends on architecture validation from Galadriel

2. **CT-47 (Timers)** - Can't start until CT-53 is done
   - CT-53 scope needs clarification

3. **CT-68 (Manual Claim)** - ✅ Done, tested on prod

4. **CRYPTO-459 + CRYPTO-461** - 🎬 Ready for Release
   - Regular and Special bonuses sections complete

5. **CRYPTO-497** - 🚀 Development in progress
   - Personal Account + Bonus Tags

6. **CRYPTO-259** - ✅ Ready for BA (Change request)

**Estimated Time to Complete (excluding CT-36):**
- CRYPTO-497: 1-2 weeks (dev + test)
- Final regression testing: 1 week
- Deployment: 1 week

**If CT-36 stays blocked:** CRYPTO-2 cannot be fully deployed to production.

---

## 📚 Additional Resources

### Design:
- [Figma - Bonus Page](https://www.figma.com/design/qkzG2IGMeL6JEpJSmIEQxE/Minebit--Workfile-?node-id=12703-14504)
- [Figma - Bonus Fix](https://www.figma.com/design/mF67jid1XZO5zzb9YG9tK3/-crypto--bonus-fixes?node-id=0-1)
- [Figma - Welcome Pack States](https://www.figma.com/design/qkzG2IGMeL6JEpJSmIEQxE/Minebit--Workfile-?node-id=10405-10493&t=XF0ZViqM7wb7Pxv1-1)

### Confluence (Needs Access):
- [Bonuses Page Documentation](https://next-t-code.atlassian.net/wiki/x/YADOBw)
- [Welcome Pack Page](https://next-t-code.atlassian.net/wiki/spaces/~712020f8028073e91146f78c047bfe0605bf02/pages/255295957/Welcome+Pack)
- [Client Bonus Pack](https://next-t-code.atlassian.net/wiki/spaces/Platform/pages/263749661/Client+Bonus+Pack)

### Related Jira Tickets:
- CT-22: Bonus Tags (moved to CRYPTO-497)
- CT-23: Bonus History (moved to CRYPTO-497)
- CT-24: Bonus Statuses (moved to CRYPTO-497)

---

## 📝 Next Steps

1. **Get clarity on CT-36 HOLD status** from Galadriel
2. **Define scope of open subtasks** (CT-49, CT-53, CT-89)
3. **Coordinate with QA** for CRYPTO-459 and CRYPTO-461 release testing
4. **Monitor CRYPTO-497 progress** (Personal Account + Bonus Tags)
5. **Schedule CRYPTO-259 testing** (Turnover display without reload)

---

*Last Updated: 2026-02-28*
