---
name: ai-orchestrator-learning
description: Learning system for AI Orchestrator career path with QA focus. Weekly trend monitoring, job market analysis, curated resources, progress tracking, and portfolio building.
homepage: https://clawhub.ai/skills/ai-orchestrator-learning
metadata:
  clawdbot:
    emoji: 🎓
    requires:
      bins: ["python3", "node"]
      env: ["TAVILY_API_KEY"]
    primaryEnv: TAVILY_API_KEY
    schedule:
      - task: trend_monitor
        cron: "0 10 * * 1"  # Monday 10:00 AM
      - task: job_analyzer
        cron: "0 10 * * 1"  # Monday 10:00 AM (after trend_monitor)
      - task: daily_reminder
        cron: "0 19 * * 1-5"  # Mon-Fri 7:00 PM CET
---

# AI Orchestrator Learning System

Personalized learning system for becoming an AI Orchestrator with QA specialization.

## Core Features

### 1. Trend Monitoring (Weekly - Monday)
Automatically searches for latest trends in AI agent orchestration:
- Multi-agent system research
- New frameworks and tools
- Production patterns
- Industry news

**Script:** `scripts/trend_monitor.py`

### 2. Job Market Analysis (Weekly - Monday)
Analyzes job postings for AI Orchestrator roles:
- Skill requirements extraction
- Salary trends
- Top companies hiring
- Keyword analysis for ATS

**Script:** `scripts/job_analyzer.py`

### 3. Resource Curation (On-demand)
Finds and curates free learning resources:
- Courses and tutorials
- Documentation and guides
- Research papers
- Video content

**Script:** `scripts/resource_curator.py`

### 4. Progress Tracking (Daily)
Tracks your learning progress:
- Lessons completed
- Projects built
- Skills mastered
- Time invested

**File:** `progress.md`

### 5. Smart Reminders (Daily)
Sends learning reminders via Telegram:
- Daily learning prompts
- Weekly progress summaries
- Milestone celebrations

### 6. Portfolio Builder
Templates and guidance for portfolio projects:
- QA Orchestrator System (your actual project)
- Multi-Agent Research Assistant
- Customer Support Agent Team

**Folder:** `projects/`

## Learning Path

### Phase 1: Fundamentals (Week 1-4)
- AI & LLM Foundations
- Agent Architecture Basics

### Phase 2: Frameworks (Week 5-10)
- LangChain & LangGraph
- CrewAI
- AutoGen & Others

### Phase 3: Advanced Patterns (Week 11-16)
- Orchestration Patterns
- Memory & Context Systems
- Tool Orchestration & MCP

### Phase 4: Production (Week 17-20)
- Observability & Monitoring
- Deployment & Scaling

### Phase 5: Career Prep (Week 21-24)
- Portfolio Projects
- Resume & Interview Prep

**Full curriculum:** `curriculum.md`

## Commands

### Get Today's Lesson
```
/learn today
```

### Check Progress
```
/learn progress
```

### Find Resources
```
/learn resources [topic]
```

### What's Next
```
/learn next
```

### Job Market Analysis
```
/jobs analyze
```

### Latest Trends
```
/trends
```

## File Structure

```
ai-orchestrator-learning/
├── SKILL.md                    # This file
├── curriculum.md               # Full learning roadmap
├── resources.md                # Curated free resources
├── progress.md                 # Your learning progress
├── job-analysis.md             # Weekly job market updates
├── trend-report.md             # Weekly trend monitoring
├── interview-prep.md           # Interview preparation
├── skills-matrix.md            # Skills tracking
├── scripts/
│   ├── trend_monitor.py        # Weekly trend search
│   ├── job_analyzer.py         # Job market analysis
│   ├── resource_curator.py     # Find best resources
│   └── progress_tracker.py     # Track your learning
├── projects/
│   ├── qa-orchestrator/        # Your Nexus project
│   ├── research-assistant/     # Multi-agent research
│   └── support-agents/         # Customer support team
└── templates/
    ├── portfolio-project.md    # Project documentation template
    ├── case-study.md           # Case study template
    └── resume-sections.md      # Resume sections for AI roles
```

## Integration with Your Work

### QA-Specific Focus
This learning path is integrated with your actual QA work:
- Build Nexus as your portfolio project
- Apply patterns directly to Clawver and Cipher
- Document your real multi-agent system

### Parallel Learning & Work
- 1 hour/day dedicated learning
- Apply concepts to current tasks
- Build portfolio while working

### General AI Orchestration Foundation
- Core patterns work across domains
- Transferable skills
- Industry-standard practices

## Metrics

Track your progress with:
- [ ] Lessons completed: 0/60
- [ ] Projects built: 0/3
- [ ] Skills mastered: 0/15
- [ ] Days learning: 0
- [ ] Hours invested: 0

## Next Steps

1. Read `curriculum.md` for your learning roadmap
2. Check `resources.md` for curated materials
3. Start with Phase 1, Week 1
4. Update `progress.md` as you learn
5. Build portfolio projects in `projects/`

---

**Created:** 2026-03-17
**Owner:** Ihor Solopii (Nexus User)
**Focus:** QA Orchestration + General AI Agent Systems
**Pace:** Moderate (1 hour/day)
**Duration:** 24 weeks (deep learning with parallel work)
