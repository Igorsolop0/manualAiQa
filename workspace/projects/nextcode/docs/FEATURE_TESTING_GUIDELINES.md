# Feature Testing Guidelines

**Source:** Confluence QA Space
**Exported:** 2026-03-04
**Purpose:** Ensure quality feature testing

---

## Scope

Testing of features, tasks, bug reports, etc.

---

## Types of Testing Performed

- **Functional Testing**
- **UI/UX Validation**
- **Cross-browser/device Testing** (if applicable)
- **Regression Testing** (describe when triggered)
- **Negative Testing**

---

## Test Documentation and Reporting

### Where

Test results should be available either in:
- TestRail testrun
- OR provided as a comment to the task

### Possible Forms

- TestRail testcases
- Checklist in comments
- Google Sheet or other doc attached in comments

### Proof

If task has visual part, better to provide some screenshots

---

## Testing Process

### Entrance Criteria

- ✅ Jira task status is either **Ready for MR testing** or **Ready for testing**
- ✅ Task has linked MR and it's status corresponds to tasks status:
  - **Open MR** → Ready for MR testing
  - **Merged MR** → Ready for Testing
- ✅ QA have access to needed accounts and linked documents
- ✅ Requirements are clear. Linked product task description and tasks comment sections are reviewed by QA.
- ✅ Make sure you've selected correct environment and brand for testing:
  - **If MR is open** — you should ask in team chat and deploy it to free environment before testing, than lock deploy to this environment
  - **If MR is Merged** — tasks should be tested on QA environment
  - **If task has no MR** — task should be tested where it is configured. As default Live brands tasks are configured on QA env before release, otherwise task can be configured directly in production

### Decision Making

- If all needed data is present, access to docs granted, task/MR status corresponds → testing can be started.
- Otherwise, request needed changes by tagging proper person in comments (Config from dev, access from PO, etc.)
- **Reopen vs separate bug report:**
  - If key acceptance criteria is not met → reopen task.
  - Otherwise, if functionality works but has some bugs in it → move task to **On Correction** status and link bug report.

### Exit Criteria

- ✅ Functional and non-functional testing completed
- ✅ No open high or critical bugs
- ✅ No critical regressions in related areas
- ✅ Acceptance criteria met
- ✅ As a result of testing there must be provided some kind of test documentation. See *Feature testing Guidelines | Test Documentation and Reporting:*

---

## Production Re-Testing Process

### Entrance Criteria

- ✅ The deployment to production has successfully completed
- ✅ Smoke testing in production has been executed and passed
- ✅ If task involves CMS configuration, task must be in **"Strapi Config Done"** status in Jira

### Re-testing Steps

1. Execute functional verification of fixed/implemented feature in production.
2. Perform limited regression checks around the impacted area if needed
3. Add testing results as comment.
4. If defects are found:
   - Raise a new bug linked to production task.
5. If no issues:
   - Close task with Resolution "Done"
   - Move linked product task/incident to **Ready for review** or similar status

### Exit Criteria

- ✅ Functional and non-functional testing completed
- ✅ No open high or critical bugs
- ✅ No critical regressions in related areas
- ✅ Acceptance criteria met
- ✅ As a result of testing there must be provided some kind of test documentation. See *Feature testing Guidelines | Test Documentation and Reporting:*
- ✅ Task and Parent task statuses updated in Jira
- ✅ Stakeholders are informed in case of failures
- ✅ Task for test automation and/or existing tests adjustments created in QA Automation epic **PR-504: [Q2 - 2025] Portal test automation** CLOSED

---

## Q&A

### What if requirements are unclear or missing?

**Answer:** Do not proceed with testing. Communicate with PM or developer to clarify requirements.

---

### What if part of task can be only tested in Prod?

**Answer:** It should be mentioned in test results, agreed with PM/Team, risks considered. Subtask for testing created.

---

### Can a task be marked "Done" if there's a known minor bug?

**Answer:** Only if it's documented, agreed with the PO, and logged as a separate issue.

---

### When do I update regression tests?

**Answer:** When change affects existing flows. The test suite must reflect latest functionality.

---

### When do I create task for test automation?

**Answer:** Tests can be automated and it is not insignificant config change task.

---

## Related Documentation

- **Team & Processes:** `TEAM_AND_PROCESSES.md`
- **QA Automation Workflow:** `workflows/QA_AUTOMATION_WORKFLOW_V2.md`
- **Playwright Architecture:** `MINEBIT_PLAYWRIGHT_ARCHITECTURE.md`
- **TestRail:** https://nexttcode.testrail.io/
- **Confluence Original:** https://next-t-code.atlassian.net/wiki/spaces/QS/pages/225214492/Feature+testing+Guidelines
