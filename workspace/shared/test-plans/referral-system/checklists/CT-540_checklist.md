# Test Checklist: CT-540 — BE: Services

**Status:** In Progress
**Component:** Backend Infrastructure
**Priority:** High

---

## 🎯 Ticket Summary

Create a new standalone microservice (Tech.Referral) for referral wager calculation and commission processing. The service consumes settled bet events from Kafka, filters for real-money only (no bonus), and calculates wager amounts.

---

## ✅ Acceptance Criteria Checklist

### Infrastructure Setup

- [ ] New repository created (tech.referral)
- [ ] Solution structure follows conventions:
  - [ ] Tech.Referral.Api
  - [ ] Tech.Referral.AppServices
  - [ ] Tech.Referral.Domain
  - [ ] Tech.Referral.Infrastructure
- [ ] Standard infrastructure configured:
  - [ ] appsettings.json per environment
  - [ ] Serilog logging
  - [ ] Health check endpoints
  - [ ] Dockerfile
- [ ] Dedicated PostgreSQL database created (tech_referral)
- [ ] EF Core DbContext configured
- [ ] Initial migration created for core wager tables
- [ ] Service runs locally

### Health Check

- [ ] Health check endpoint returns 200 OK
- [ ] Health check includes database connectivity check
- [ ] Health check includes Kafka connectivity check (if applicable)

---

## 🧪 Test Scenarios

### 1. Service Startup

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Service starts successfully | Start service locally | Service runs without errors |
| Database connection | Check health endpoint | Database connectivity: Healthy |
| Configuration loaded | Verify appsettings | All environments configured |

### 2. Database Migration

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Migration runs | Apply initial migration | Tables created successfully |
| Tables structure | Verify schema | ReferralProcessedBet, ReferralWager tables exist |
| Idempotent migration | Re-run migration | No errors, no data loss |

### 3. Health Check Endpoint

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| GET /health | Call health endpoint | 200 OK |
| DB health | Disconnect DB temporarily | Health check shows Unhealthy |
| Response time | Measure response time | < 100ms |

---

## 🔗 Dependencies

**Blocks:** CT-549 (Processing Bets), CT-541 (API), CT-545 (Claim), CT-546 (Templates)

**Depends on:** None (foundational service)

---

## 📝 Notes

- This is infrastructure ticket — focus on setup, not business logic
- Business logic tested in CT-549 (Processing Bets)
- Ensure DevOps has K8s manifests ready for deployment

---

**Test Type:** Backend Infrastructure
**Estimated Effort:** 5 hours
**Test Environment:** Dev/QA
