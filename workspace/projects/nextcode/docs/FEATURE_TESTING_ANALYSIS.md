# Feature Testing Guidelines — Gap Analysis

**Date:** 2026-03-04
**Source:** PDF "QS-Feature testing Guidelines-040326-153326.pdf" (Confluence QA Space)
**Existing Documentation:**
- `TEAM_AND_PROCESSES.md`
- `workflows/QA_AUTOMATION_WORKFLOW_V2.md`
- `MINEBIT_PLAYWRIGHT_ARCHITECTURE.md`

---

## Summary

✅ **New document has been created:** `docs/FEATURE_TESTING_GUIDELINES.md`

The Confluence document provides a **clear, structured framework** for feature testing with well-defined entrance/exit criteria, MR status workflows, and production re-testing process.

---

## New Concepts NOT in Existing Documentation

### 1. Production Re-Testing Process ⭐ CRITICAL

**Status:** Not documented anywhere

**New Workflow:**
- Entrance criteria: successful deployment, smoke test passed, Strapi config done
- Re-testing steps: functional verification, limited regression, add results
- Exit criteria: all tests done, no high/critical bugs, statuses updated, stakeholders informed

**Recommendation:**
- Add as new section in `QA_AUTOMATION_WORKFLOW_V2.md` or create separate `PRODUCTION_RETESTING.md`

---

### 2. MR Status Workflow ⭐ HIGH VALUE

**Status:** Partially mentioned, not formalized

**New Logic:**
| MR Status | Task Status | Environment |
|-----------|-------------|-------------|
| Open MR | Ready for MR testing | Free environment (deploy before testing) |
| Merged MR | Ready for Testing | QA environment |
| No MR | Depends on config | QA (default) or Production |

**Recommendation:**
- Add to `TEAM_AND_PROCESSES.md` under "QA Processes"
- Update `QA_AUTOMATION_WORKFLOW_V2.md` STEP 1 to check MR status

---

### 3. Q&A Section ⭐ HIGH VALUE

**Status:** Not documented

**New Q&A:**
- Requirements unclear? → Don't proceed, communicate with PM/dev
- Part of task only testable in Prod? → Document in results, agree with PM/Team
- Known minor bug? → Only if documented, agreed with PO, logged as separate issue
- When to update regression tests? → When change affects existing flows
- When to create test automation task? → When tests can be automated and not insignificant config change

**Recommendation:**
- Add to `TEAM_AND_PROCESSES.md` under "QA Processes" or create "FAQ" section

---

### 4. Decision Making Framework ⭐ MEDIUM VALUE

**Status:** Not formalized

**New Logic:**
- **Reopen task** if key acceptance criteria NOT met
- **Move to "On Correction"** if functionality works but has bugs (link bug report)

**Recommendation:**
- Add to `TEAM_AND_PROCESSES.md` under "Bug Tracking"

---

### 5. Expanded Test Documentation Formats ⭐ LOW VALUE

**Status:** Partially covered

**New Formats:**
- TestRail testcases ✅ (already documented)
- Checklist in comments ⭐ (new)
- Google Sheet or other doc attached ⭐ (new)
- Screenshots for visual parts ⭐ (new)

**Recommendation:**
- Already covered in `QA_AUTOMATION_WORKFLOW_V2.md` (TestRail, screenshots)
- Optional: mention checklist and Google Sheet as alternatives

---

## Gaps in Existing Documentation

### TEAM_AND_PROCESSES.md

**Missing:**
- Production re-testing process
- MR status workflow
- Q&A section
- Decision making (reopen vs On Correction)

**Action:**
- Add references to `FEATURE_TESTING_GUIDELINES.md`
- Consider merging relevant sections

---

### QA_AUTOMATION_WORKFLOW_V2.md

**Missing:**
- MR status check in STEP 1
- Production re-testing workflow
- When to create test automation tasks (currently focuses on Playwright generation)

**Action:**
- Update STEP 1 to check MR status
- Add STEP 6 for Production Re-Testing
- Add note about when to create automation tasks

---

## Recommendations (Prioritized)

### Priority 1 — Add to Existing Docs

1. **MR Status Workflow** → Add to `TEAM_AND_PROCESSES.md`
2. **Q&A Section** → Add to `TEAM_AND_PROCESSES.md`
3. **Decision Making** → Add to `TEAM_AND_PROCESSES.md` (Bug Tracking section)

### Priority 2 — Create New Workflow

4. **Production Re-Testing Process** → Create `PRODUCTION_RETESTING.md` OR add to `QA_AUTOMATION_WORKFLOW_V2.md` as STEP 6

### Priority 3 — Update Existing Workflow

5. **QA_AUTOMATION_WORKFLOW_V2.md STEP 1** → Add MR status check
6. **Test Documentation Formats** → Mention checklist and Google Sheet as alternatives

---

## Files Created/Modified

✅ **Created:** `docs/FEATURE_TESTING_GUIDELINES.md` — Complete translation of Confluence document
✅ **Created:** `docs/FEATURE_TESTING_ANALYSIS.md` — This analysis document

---

## Next Steps

1. Review `FEATURE_TESTING_ANALYSIS.md` with PM/Team
2. Decide which recommendations to implement (Priority 1 is recommended)
3. Update `TEAM_AND_PROCESSES.md` with MR workflow, Q&A, decision making
4. Add production re-testing to `QA_AUTOMATION_WORKFLOW_V2.md`
5. Delete `FEATURE_TESTING_ANALYSIS.md` after integration complete
