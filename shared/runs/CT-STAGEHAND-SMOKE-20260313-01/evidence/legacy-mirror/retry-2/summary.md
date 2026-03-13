# CT-STAGEHAND-SMOKE retry-2 summary

Date: 2026-03-12
Scope: narrow auth-state recheck after Stagehand smoke failure

## Run A (retry-2)
- Output: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-STAGEHAND-SMOKE/retry-2/stagehand-output-retry2.clean.json`
- Artifact dir: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-STAGEHAND-SMOKE/retry-2/artifacts`
- Result: `FAIL (timeout)`
- Observation: login modal stayed open and submit did not complete auth-state confirmation.
- DOM evidence (`step-007-after-tool.html`):
  - `Username or Email is required.`
  - `Password is required.`
  - `value=""` for both login inputs

## Run B (retry-2b)
- Output: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-STAGEHAND-SMOKE/retry-2/stagehand-output-retry2b.clean.json`
- Artifact dir: `/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-STAGEHAND-SMOKE/retry-2/artifacts-b`
- Result: `TECHNICAL_FAIL (LLM context limit)`
- Technical error:
  - `This model's maximum context length is 131072 tokens... requested 516419 tokens`
- Despite technical error, Stagehand completed auth flow steps before failing:
  - Login modal opened
  - Credentials typed
  - Submit clicked
  - URL switched from `...?modal=iqs-sign-in` to `/`
  - Agent observed authenticated indicators: balance (`$178.53`), `Wallet`, user profile id (`899629`)

## Practical conclusion
- **Auth flow appears reproducible and successful in retry-2b before post-step model overflow.**
- Blocking issue is now mostly infrastructural (model/context handling), not locator discovery.

## Recommended next stabilization step
- For Stagehand smoke: use a model/provider with larger practical prompt budget or add early-stop after auth confirmation to avoid oversized message/context accumulation.
