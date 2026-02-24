---
date: 2026-02-19
title: Daily Standup - NextCode
attendees: [Андрій, Микола, Діма, Ігор, Кирило, Galadriel]
source: transcript
---

# Daily Standup - NextCode

**Date:** 2026-02-19
**Time:** ~08:02 - 08:41 (39 min)
**Attendees:** Андрій, Микола, Діма, Ігор, Кирило, Galadriel

---

## Summary

Daily standup covering release planning (today ~11:00), environment blockers for rakeback testing, task distribution concerns about Ihor's workload, and Recent Wins widget bugs requiring WebSocket implementation next sprint.

---

## Action Items

### 🔴 Critical / Today
- [ ] **@Team**: Release to production — *Today ~11:00*
- [ ] **@Андрій**: Confirm exact release time and notify team
- [ ] **@Ігор**: Continue with sprint tasks (CT-779, CT-783, CT-785) — *Priority*

### 🟡 This Week
- [ ] **@Dima**: Wait for release before deploying rakeback to QA
- [ ] **@Dima**: Configure rakeback on Dev or QA (after regression completes)
- [ ] **@Андрій**: Check if one service can be deployed to QA without blocking regression
- [ ] **@Кирило**: Add release to admin panel (already on prod)

### 📋 No Deadline
- [ ] **@Team**: WebSocket implementation for Recent Wins — *Next sprint*
- [ ] **@Team**: WebSocket implementation for Live Bets — *Next sprint*
- [ ] **@Dima**: Investigation for rakeback timer (3h estimate) — *Next sprint*
- [ ] **@Кирило**: Randomizer fix for Recent Wins (one bet per 2 seconds)

---

## Decisions

1. **Release today ~11:00** — Services already deployed to prod staging
2. **Ihor priority: sprint tasks first** — CT-517 (social linking) will wait until Ihor has capacity
3. **WebSocket for Recent Wins in next sprint** — Current implementation shows 15 bets instead of 30 due to polling limitations
4. **Next sprint team expansion** — Adding 1 QA + 2 fullstack developers to reduce Ihor's load
5. **Rakeback configuration** — Need `isManualClaimed` in Strapi + `finishedBonusButtons` in BO for manual claim flow

---

## Open Questions

1. Can one service be deployed to QA without breaking regression testing?
2. Should Dima deploy to Dev or wait for QA?
3. How to handle 30 bets display without WebSocket? (Currently shows 15)

---

## Technical Details

### Rakeback Configuration
- **Strapi**: Enable `isManualClaimed` in promotion settings
- **BO**: Configure `finishedBonusButtons` with `claimBonusReward` action
- **Bonus ID**: 2,469,172 (for testing on Alov QA)
- **Timer**: Need to duplicate configuration in bonus itself for timer display

### Recent Wins Bug
- **Issue**: Shows 15 bets instead of 30
- **Cause**: No WebSocket — polling every 20 seconds
- **Solution**: WebSocket implementation (planned next sprint)
- **Workaround**: Increase Strapi limit to 30 (temporary)

### Environments Status
- **Dev**: Blocked
- **QA**: Busy with regression
- **Prod**: Release today

---

## Team Updates

### Андрій
- Finished services refactoring
- Deployed to prod staging
- Coordinating release timing

### Микола
- Configuration work (multiple tasks)
- May take 1-2 days
- Bug found during regression — mock data not removed

### Dima
- Needs Dev environment for rakeback testing
- QA blocked by regression
- Waiting for release confirmation

### Ihor
- **Status**: Overloaded (5-6 tasks)
- **Priority**: Sprint tasks first
- **Next**: 5 tasks from release + possible CT-517

---

## Next Steps

1. **Immediate**: Release at ~11:00
2. **After release**: Ihor can take CT-517 if capacity allows
3. **Next sprint**: WebSocket implementation + team expansion
4. **Ongoing**: Configuration work by Микола

---

<details>
<summary>📝 Raw Transcript Summary (click to expand)</summary>

**Release Status:**
- Реліз сьогодні повинен бути. Там у нас задача оставалася в тестування, і реліз ЖД має бути сьогодні.
- Там кіа збираються в одинадцять, я думаю, десь вже в один одинадцяте буде реліз

**Ihor's Workload:**
- на Ігоря, насправді, зараз дуже велика нагрузка, бо в нас іде 5 розробників
- Нас з наступного спринта додає в нашу команду ще один QA, і тоді, ну, і ще два фулстака

**Recent Wins Issue:**
- Ресцент Винст максимум пятнадцать возвращает
- Задача просто была пропасть на 30
- Нам надо до этого из лайф туда брать эти сокетом следующий спринт

**Rakeback Testing:**
- Мені важно б задоволити на Дев, бо там мені буде простіше тестувати
- Банакиа хтось вже залиб в бапі
- Це краще перепитати, але я думаю, що не дозволять щось не дав заливати

</details>
