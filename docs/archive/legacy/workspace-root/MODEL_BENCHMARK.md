# Model Benchmark Log

> Автоматично оновлюється щотижня через Daily Self-Review cron.
> Ціль: порівняти моделі за якістю, швидкістю та вартістю для прийняття рішення.

## Current Model Assignment

| Role | Model | Since | Status |
|------|-------|-------|--------|
| Nexus (Orchestrator) | DeepSeek V3.2 | 2026-03-06 | ✅ Active |
| Heartbeat | GLM-4.7-FlashX | 2026-03-06 | ✅ Active |
| Fallback 1 | GLM-4.7 (subscription) | 2026-03-06 | Standby |
| Fallback 2 | DeepSeek R1 | 2026-03-06 | Standby |
| Vision | GLM-4.5V | 2026-02-28 | ✅ Active |

## A/B Testing Schedule

| Week | Dates | Orchestrator | QA Agent | Focus |
|------|-------|-------------|----------|-------|
| 1 | 2026-03-06 — 03-12 | DeepSeek V3.2 | (not yet) | **Baseline** |
| 2 | TBD | GLM-5 (pay-as-you-go) | GLM-4.7 | V3.2 vs GLM-5 |
| 3 | TBD | Winner | DeepSeek V3.2 coding | V3.2 for code |
| 4 | TBD | Winner | Claude Sonnet 4.6 (2-3d) | Claude Code Writer |

## Weekly Reports

### Week 1: DeepSeek V3.2 Baseline (2026-03-06 — 03-12)

| Metric | Value | Notes |
|--------|-------|-------|
| Tasks Total | — | To be filled |
| Tasks Completed | — | |
| Avg Latency | — | |
| Est. Cost | — | |
| Quality (1-5) | — | Ihor's rating |
| Corrections Needed | — | |
| Hallucinations | — | |

---

_Updated by Daily Self-Review cron. Manual entries welcome._
