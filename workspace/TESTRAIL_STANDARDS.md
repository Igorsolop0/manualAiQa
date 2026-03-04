# TestRail Standards and Auto-Learning Dictionary

**CRITICAL GUARDRAIL:** All AI Agents MUST validate any TestRail test cases against these standards BEFORE sending them via API or presenting them to the user.

## 1. General Formatting Rules
- **Language Policy**: ALL TestRail cases MUST be written strictly in **English**.
- **Title Formatting**:
  - Titles MUST NOT contain environment names (e.g., dev, qa, prod).
  - Titles MUST NOT start with Jira ticket IDs (DO NOT use formats like `CT-824-E2E-01:`).
  - Titles should be concise and describe the action being tested.

## 2. Terminology Dictionary (Auto-Learning Mode)
The terms below must be strictly adhered to when generating steps, expected results, and titles for TestRail. 

**AGENT AUTO-LEARNING INSTRUCTION:**
If the user corrects you on a term or provides a new preferred term to use in TestRail (e.g., "use X instead of Y"), you MUST autonomously update this file (`TESTRAIL_STANDARDS.md`) to add that new mapping to the list below. This ensures you never make the same mistake twice.

### Dictionary
- `AvailableMain` ➡️ `Unused balance`
- `/bonuses-new` ➡️ `/bonuses`
- `"Rakeback Test"` ➡️ `"Rakeback"` (always use production-like names)
