# CRON Schedule Setup for Regular Bonuses

## Overview

CRON expressions define when a scheduled bonus becomes available for claim. The system calculates `nextAvailableAt` and `previousAvailableAt` based on the CRON schedule.

---

## CRON Expression Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday = 0)
│ │ │ │ │
* * * * *
```

---

## Common Schedules for Bonuses

### Daily Bonuses

| CRON | Description | Active At |
|------|-------------|-----------|
| `0 0 * * *` | Every day at 00:00 UTC | Midnight |
| `0 12 * * *` | Every day at 12:00 UTC | Noon |
| `0 18 * * *` | Every day at 18:00 UTC | 6 PM |
| `30 9 * * *` | Every day at 09:30 UTC | 9:30 AM |

**Use case:** Daily cashback, daily free spins

---

### Weekly Bonuses

| CRON | Description | Active At |
|------|-------------|-----------|
| `0 0 * * 1` | Every Monday at 00:00 UTC | Weekly start |
| `0 0 * * 5` | Every Friday at 00:00 UTC | Weekend bonus |
| `0 18 * * 5` | Every Friday at 18:00 UTC | Friday evening |
| `0 12 * * 0` | Every Sunday at 12:00 UTC | Weekly end |

**Day of week:** 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday

**Use case:** Weekly cashback, weekend bonuses

---

### Monthly Bonuses

| CRON | Description | Active At |
|------|-------------|-----------|
| `0 0 1 * *` | 1st of every month at 00:00 UTC | Monthly |
| `0 0 15 * *` | 15th of every month at 00:00 UTC | Mid-month |
| `0 12 1 * *` | 1st of every month at 12:00 UTC | Monthly noon |

**Use case:** Monthly cashback, VIP monthly bonus

---

### Custom Schedules

| CRON | Description |
|------|-------------|
| `0 0 1,15 * *` | 1st and 15th of every month |
| `0 12 * * 1-5` | Every weekday (Mon-Fri) at 12:00 |
| `0 0 * * 1,4` | Every Monday and Thursday |
| `0 0 1 1 *` | January 1st only (yearly) |

---

## How It Works

### Claim Flow with CRON

```
┌─────────────────────────────────────────────────────────────┐
│  CRON: 0 0 * * 1 (Every Monday 00:00)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Mon (Week 1)                                               │
│  ├── 00:00 → Bonus becomes available                        │
│  │          isAvailable = true                              │
│  │          nextAvailableAt = null                          │
│  │                                                          │
│  ├── User claims bonus                                      │
│  │          isAvailable = false                             │
│  │          nextAvailableAt = Mon (Week 2) 00:00            │
│  │          previousAvailableAt = Mon (Week 1) 00:00        │
│  │                                                          │
│  Mon (Week 2)                                               │
│  ├── 00:00 → Bonus becomes available again                  │
│  │          isAvailable = true                              │
│  │                                                          │
└─────────────────────────────────────────────────────────────┘
```

### New User (Never Claimed) — CT-756 Feature

```
Before CT-756:
├── nextAvailableAt = null (or default datetime)
├── No progress bar shown
└── User doesn't know when bonus becomes available

After CT-756:
├── nextAvailableAt = <next cron datetime>
├── previousAvailableAt = <previous cron datetime>
├── lastClaimedAt = null
├── isPendingCalculation = false
└── Progress bar CAN be shown with countdown
```

---

## BackOffice Configuration

### Required Fields

| Field | Value | Description |
|-------|-------|-------------|
| `IsScheduled` | `true` | Enable scheduled bonus |
| `CronExpression` | `0 0 * * 1` | CRON schedule |
| `CampaignStartTime` | `2026-01-01` | When campaign starts |
| `CampaignFinishTime` | `2026-12-31` | When campaign ends |

### Example Bonus Setup

```json
{
  "id": 25125,
  "name": "Weekly Cashback",
  "type": "Cashback",
  "isScheduled": true,
  "cronExpression": "0 0 * * 1",
  "campaignStartTime": "2026-01-01T00:00:00Z",
  "campaignFinishTime": "2026-12-31T23:59:59Z"
}
```

---

## Validation Rules

1. **CronExpression must be valid** — system validates format
2. **CampaignFinishTime required** — bonus must have end date
3. **Timezone: UTC** — all times in CRON are UTC
4. **Minimum period: 1 day** — don't set more frequent than daily

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Bonus never shows | Invalid CRON | Use crontab.guru to validate |
| Bonus shows at wrong time | Timezone mismatch | Remember CRON uses UTC |
| nextAvailableAt is null | CT-756 not deployed | Check feature deployment |
| Progress bar not shown | CT-767 not deployed | FE needs previousAvailableAt |

---

## Useful Tools

- **CRON Generator:** https://crontab.guru/
- **CRON Validator:** https://crontab.guru/
- **Timezone Converter:** https://www.timeanddate.com/worldclock/converter.html

---

## Related Documentation

- **CT-756:** Set NextAvailableAt for scheduled bonuses
- **CT-767:** FE support for previousAvailableAt
- **Confluence:** https://next-t-code.atlassian.net/wiki/spaces/QS/pages/204111989/Bonuses+setup
