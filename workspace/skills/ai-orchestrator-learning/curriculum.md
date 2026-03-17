# AI Orchestrator Learning Curriculum

**Duration:** 24 weeks (6 months)
**Pace:** Moderate (1 hour/day)
**Focus:** QA Orchestration + General AI Agent Systems
**Style:** Deep learning with parallel work application

---

## Overview

This curriculum is designed for a Senior QA Engineer transitioning into AI Agent Orchestration. You'll build practical skills while applying concepts directly to your current QA automation work.

### Weekly Schedule
- **Daily:** 1 hour dedicated learning (Mon-Fri)
- **Weekend:** Optional review / project work
- **Weekly Total:** 5 hours minimum
- **24-Week Total:** ~120 hours

### Learning Philosophy
1. **Apply immediately** — Use concepts in your Nexus/Clawver/Cipher work
2. **Build portfolio** — Document your real projects as case studies
3. **Stay current** — Weekly trend monitoring included
4. **Practice over theory** — 60% hands-on, 40% theory

---

## Phase 1: Foundations (Weeks 1-4)
**Goal:** Understand AI agents and LLM fundamentals

### Week 1: LLM & Prompt Engineering Basics
**Time:** 5 hours
**Focus:** How LLMs work, prompt patterns

#### Day 1-2: LLM Fundamentals (2 hours)
- [ ] Watch: "How LLMs Work" (Andrej Karpathy, YouTube) - 1h
- [ ] Read: Transformers & Attention Mechanism - 30min
- [ ] Practice: Token counting and context windows - 30min

**Resources:**
- https://www.youtube.com/watch?v=kCc8FmEb1nY (Karpathy's GPT video)
- https://platform.openai.com/tokenizer (Token counter)
- https://www.anthropic.com/research/context-engineering

#### Day 3-4: Prompt Engineering (2 hours)
- [ ] Complete: OpenAI Prompt Engineering Guide - 1h
- [ ] Practice: Write 10 different prompt patterns - 1h
- [ ] Document: Your best prompts in notes

**Resources:**
- https://platform.openai.com/docs/guides/prompt-engineering
- https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/

#### Day 5: Application to QA (1 hour)
- [ ] Apply: Rewrite your Nexus prompts using patterns learned
- [ ] Compare: Before/after prompt quality
- [ ] Document: Prompt improvements made

**Deliverable:** 5 improved prompts for Nexus + documentation

---

### Week 2: Advanced Prompting & Context Management
**Time:** 5 hours
**Focus:** Chain-of-thought, few-shot, context optimization

#### Day 1-2: Advanced Patterns (2 hours)
- [ ] Learn: Chain-of-thought prompting - 45min
- [ ] Learn: Few-shot learning - 45min
- [ ] Practice: Self-consistency & tree-of-thought - 30min

**Resources:**
- https://www.promptingguide.ai/ (Comprehensive guide)
- https://arxiv.org/abs/2201.11903 (Chain-of-thought paper)

#### Day 3-4: Context Management (2 hours)
- [ ] Learn: Context window limitations - 30min
- [ ] Learn: Context compression techniques - 30min
- [ ] Practice: Sliding window implementation - 1h

**Resources:**
- https://www.anthropic.com/index/claudes-context-window
- https://python.langchain.com/docs/modules/memory/

#### Day 5: Application to QA (1 hour)
- [ ] Apply: Improve Clawver context handling
- [ ] Implement: Context summarization in Nexus
- [ ] Test: Compare results

**Deliverable:** Context management improvement in Nexus

---

### Week 3: Agent Architecture Fundamentals
**Time:** 5 hours
**Focus:** Agent loop, tool calling, memory systems

#### Day 1-2: Agent Loop & Reasoning (2 hours)
- [ ] Learn: ReAct pattern (Reasoning + Acting) - 1h
- [ ] Understand: Perceive → Reason → Act cycle - 30min
- [ ] Practice: Simple agent loop in Python - 30min

**Resources:**
- https://arxiv.org/abs/2210.03629 (ReAct paper)
- https://python.langchain.com/docs/modules/agents/

#### Day 3-4: Tool Calling & Function Execution (2 hours)
- [ ] Learn: Function calling with LLMs - 1h
- [ ] Practice: Define tools and call them - 1h
- [ ] Build: 3 simple tools for your QA workflow

**Resources:**
- https://platform.openai.com/docs/guides/function-calling
- https://python.langchain.com/docs/modules/tools/

#### Day 5: Application to QA (1 hour)
- [ ] Apply: Design tools for Clawver
- [ ] Document: Tool definitions for UI testing
- [ ] Compare: With current Clawver capabilities

**Deliverable:** Tool design document for Clawver

---

### Week 4: Memory Systems & State Management
**Time:** 5 hours
**Focus:** Agent memory types, state persistence

#### Day 1-2: Memory Architecture (2 hours)
- [ ] Learn: Working memory vs long-term memory - 45min
- [ ] Learn: Episodic & semantic memory - 45min
- [ ] Design: Memory architecture for Nexus - 30min

**Resources:**
- https://python.langchain.com/docs/modules/memory/types/
- https://www.pinecone.io/learn/series/memory/

#### Day 3-4: State Management (2 hours)
- [ ] Learn: State persistence patterns - 1h
- [ ] Practice: Implement state checkpointing - 1h

**Resources:**
- https://langchain-ai.github.io/langgraph/how-tos/persistence/

#### Day 5: Application to QA (1 hour)
- [ ] Apply: Improve Nexus memory system
- [ ] Implement: Persistent state for long workflows
- [ ] Test: State recovery after interruption

**Deliverable:** Memory system improvement for Nexus

---

## Phase 2: Frameworks (Weeks 5-10)
**Goal:** Master major agent frameworks

### Week 5-6: LangChain Fundamentals
**Time:** 10 hours
**Focus:** Chains, agents, tools, memory

#### Day 1-2: LangChain Basics (2 hours)
- [ ] Setup: LangChain environment - 30min
- [ ] Learn: LCEL (LangChain Expression Language) - 1h
- [ ] Practice: Build first chain - 30min

**Resources:**
- https://python.langchain.com/docs/get_started/introduction
- https://python.langchain.com/docs/expression_language/

#### Day 3-4: Chains & Agents (2 hours)
- [ ] Learn: Chain types (sequential, router, transform) - 1h
- [ ] Build: QA analysis chain - 1h

**Resources:**
- https://python.langchain.com/docs/modules/chains/

#### Day 5: Application to QA (1 hour - Week 5)
- [ ] Design: LangChain chain for test planning
- [ ] Document: Chain architecture

#### Day 1-2: Tools & Memory (2 hours - Week 6)
- [ ] Learn: Tool definitions - 1h
- [ ] Learn: Memory in LangChain - 1h

#### Day 3-4: Integration (2 hours - Week 6)
- [ ] Build: Complete agent with tools + memory - 1h
- [ ] Test: Agent behavior - 1h

#### Day 5: Application to QA (1 hour - Week 6)
- [ ] Prototype: LangChain-based QA agent
- [ ] Compare: With current Nexus architecture

**Deliverable:** Working LangChain agent for QA task

---

### Week 7-8: LangGraph Deep Dive
**Time:** 10 hours
**Focus:** Graph-based orchestration, state machines

#### Day 1-2: LangGraph Fundamentals (2 hours)
- [ ] Learn: StateGraph basics - 1h
- [ ] Practice: Simple graph workflow - 1h

**Resources:**
- https://langchain-ai.github.io/langgraph/tutorials/intro/

#### Day 3-4: Advanced Graphs (2 hours)
- [ ] Learn: Conditional edges - 1h
- [ ] Learn: Checkpointing & persistence - 1h

**Resources:**
- https://langchain-ai.github.io/langgraph/how-tos/

#### Day 5: Application to QA (1 hour - Week 7)
- [ ] Design: LangGraph for Nexus workflow
- [ ] Document: Graph architecture

#### Day 1-2: Human-in-the-Loop (2 hours - Week 8)
- [ ] Learn: Human approval nodes - 1h
- [ ] Practice: Interrupt & resume - 1h

#### Day 3-4: Multi-Agent Graphs (2 hours - Week 8)
- [ ] Learn: Multi-agent coordination in LangGraph - 1h
- [ ] Build: Supervisor pattern - 1h

#### Day 5: Application to QA (1 hour - Week 8)
- [ ] Prototype: LangGraph-based Nexus
- [ ] Test: Workflow execution

**Deliverable:** LangGraph prototype for QA orchestration

---

### Week 9-10: CrewAI & AutoGen
**Time:** 10 hours
**Focus:** Role-based agents, conversational patterns

#### Day 1-2: CrewAI Basics (2 hours - Week 9)
- [ ] Learn: Agent roles & tasks - 1h
- [ ] Build: Simple crew - 1h

**Resources:**
- https://docs.crewai.com/
- https://github.com/crewAIInc/crewAI-examples

#### Day 3-4: CrewAI Advanced (2 hours - Week 9)
- [ ] Learn: Hierarchical process - 1h
- [ ] Build: QA crew (researcher, planner, executor) - 1h

#### Day 5: Application to QA (1 hour - Week 9)
- [ ] Design: CrewAI for test execution
- [ ] Document: Agent roles

#### Day 1-2: AutoGen Basics (2 hours - Week 10)
- [ ] Learn: Conversational agents - 1h
- [ ] Build: Group chat - 1h

**Resources:**
- https://microsoft.github.io/autogen/

#### Day 3-4: AutoGen Advanced (2 hours - Week 10)
- [ ] Learn: Human proxy agents - 1h
- [ ] Build: Multi-agent research system - 1h

#### Day 5: Application to QA (1 hour - Week 10)
- [ ] Compare: LangChain vs LangGraph vs CrewAI vs AutoGen
- [ ] Document: Framework comparison

**Deliverable:** Framework comparison document + prototypes

---

## Phase 3: Advanced Patterns (Weeks 11-16)
**Goal:** Master orchestration patterns

### Week 11-12: Orchestration Patterns
**Time:** 10 hours
**Focus:** Hub-and-Spoke, Swarm, Mesh, Hierarchical

#### Day 1-2: Orchestrator-Worker Pattern (2 hours - Week 11)
- [ ] Learn: Pattern theory - 30min
- [ ] Study: Production examples - 30min
- [ ] Implement: Orchestrator-worker system - 1h

**Resources:**
- https://gurusup.com/blog/agent-orchestration-patterns

#### Day 3-4: Hierarchical Pattern (2 hours - Week 11)
- [ ] Learn: Tree-structured delegation - 1h
- [ ] Implement: Hierarchical system - 1h

#### Day 5: Application to QA (1 hour - Week 11)
- [ ] Analyze: Your Nexus architecture
- [ ] Document: How it fits orchestrator-worker pattern

#### Day 1-2: Swarm Pattern (2 hours - Week 12)
- [ ] Learn: Emergent coordination - 1h
- [ ] Implement: Simple swarm - 1h

#### Day 3-4: Mesh Pattern (2 hours - Week 12)
- [ ] Learn: Peer-to-peer coordination - 1h
- [ ] Implement: Agent mesh - 1h

#### Day 5: Application to QA (1 hour - Week 12)
- [ ] Compare: All patterns
- [ ] Document: Best pattern for QA orchestration

**Deliverable:** All 4 orchestration patterns implemented + comparison

---

### Week 13-14: Memory & Context Engineering
**Time:** 10 hours
**Focus:** Advanced memory systems, RAG

#### Day 1-2: Advanced Memory (2 hours - Week 13)
- [ ] Learn: Vector databases - 1h
- [ ] Setup: Chroma/Pinecone - 1h

**Resources:**
- https://www.pinecone.io/learn/
- https://docs.trychroma.com/

#### Day 3-4: RAG for Agents (2 hours - Week 13)
- [ ] Learn: RAG architecture - 1h
- [ ] Implement: RAG for agent memory - 1h

#### Day 5: Application to QA (1 hour - Week 13)
- [ ] Design: RAG for test case knowledge base
- [ ] Prototype: RAG-enhanced QA agent

#### Day 1-2: Context Compression (2 hours - Week 14)
- [ ] Learn: Summarization techniques - 1h
- [ ] Implement: Context compressor - 1h

#### Day 3-4: Sliding Windows (2 hours - Week 14)
- [ ] Learn: Window strategies - 1h
- [ ] Implement: Intelligent window - 1h

#### Day 5: Application to QA (1 hour - Week 14)
- [ ] Improve: Nexus context handling
- [ ] Test: Long workflow handling

**Deliverable:** RAG-enhanced memory system

---

### Week 15-16: Tool Orchestration & MCP
**Time:** 10 hours
**Focus:** Model Context Protocol, tool integration

#### Day 1-2: MCP Fundamentals (2 hours - Week 15)
- [ ] Learn: MCP architecture - 1h
- [ ] Explore: MCP servers - 1h

**Resources:**
- https://modelcontextprotocol.io/
- https://github.com/modelcontextprotocol/servers

#### Day 3-4: Custom MCP Server (2 hours - Week 15)
- [ ] Build: QA-specific MCP server - 2h

#### Day 5: Application to QA (1 hour - Week 15)
- [ ] Design: MCP integration for Nexus
- [ ] Document: Tool ecosystem

#### Day 1-2: Tool Discovery (2 hours - Week 16)
- [ ] Learn: Dynamic tool registration - 1h
- [ ] Implement: Tool discovery system - 1h

#### Day 3-4: Secure Tool Execution (2 hours - Week 16)
- [ ] Learn: Security patterns - 1h
- [ ] Implement: Secure tool runner - 1h

#### Day 5: Application to QA (1 hour - Week 16)
- [ ] Integrate: MCP tools into Nexus
- [ ] Test: Tool execution

**Deliverable:** MCP-integrated QA system

---

## Phase 4: Production (Weeks 17-20)
**Goal:** Deploy production-ready agent systems

### Week 17-18: Observability & Monitoring
**Time:** 10 hours
**Focus:** Tracing, metrics, debugging

#### Day 1-2: Observability Fundamentals (2 hours - Week 17)
- [ ] Learn: Agent observability patterns - 1h
- [ ] Setup: Langfuse - 1h

**Resources:**
- https://langfuse.com/docs
- https://opentelemetry.io/docs/

#### Day 3-4: Tracing & Metrics (2 hours - Week 17)
- [ ] Implement: Execution tracing - 1h
- [ ] Implement: Performance metrics - 1h

#### Day 5: Application to QA (1 hour - Week 17)
- [ ] Add: Observability to Nexus
- [ ] Test: Trace visualization

#### Day 1-2: Cost Monitoring (2 hours - Week 18)
- [ ] Learn: Token optimization - 1h
- [ ] Implement: Cost tracking - 1h

#### Day 3-4: Quality Metrics (2 hours - Week 18)
- [ ] Learn: Agent quality scoring - 1h
- [ ] Implement: Quality dashboard - 1h

#### Day 5: Application to QA (1 hour - Week 18)
- [ ] Create: QA agent monitoring dashboard
- [ ] Document: Metrics tracked

**Deliverable:** Observability system for Nexus

---

### Week 19-20: Deployment & Scaling
**Time:** 10 hours
**Focus:** API design, serverless, security

#### Day 1-2: API Design (2 hours - Week 19)
- [ ] Learn: Agent API patterns - 1h
- [ ] Design: REST API for agents - 1h

**Resources:**
- https://fastapi.tiangolo.com/

#### Day 3-4: Serverless Deployment (2 hours - Week 19)
- [ ] Learn: Serverless patterns - 1h
- [ ] Deploy: Agent to serverless - 1h

#### Day 5: Application to QA (1 hour - Week 19)
- [ ] Design: API for Nexus access
- [ ] Prototype: API endpoints

#### Day 1-2: Security (2 hours - Week 20)
- [ ] Learn: Agent security patterns - 1h
- [ ] Implement: Auth & authorization - 1h

#### Day 3-4: Session Isolation (2 hours - Week 20)
- [ ] Learn: Multi-tenancy patterns - 1h
- [ ] Implement: Session isolation - 1h

#### Day 5: Application to QA (1 hour - Week 20)
- [ ] Deploy: Production-ready Nexus
- [ ] Document: Deployment architecture

**Deliverable:** Production-deployed agent system

---

## Phase 5: Career Prep (Weeks 21-24)
**Goal:** Portfolio & job preparation

### Week 21-22: Portfolio Projects
**Time:** 10 hours
**Focus:** Polish portfolio projects

#### Project 1: QA Orchestrator System (Your Nexus)
- [ ] Document: Architecture decisions
- [ ] Create: System diagrams
- [ ] Write: Case study
- [ ] Record: Demo video

#### Project 2: Multi-Agent Research Assistant
- [ ] Build: Research + analysis + report agents
- [ ] Implement: Multiple orchestration patterns
- [ ] Add: Full observability
- [ ] Document: Project README

#### Project 3: Customer Support Agent Team
- [ ] Build: Triage + resolution + escalation
- [ ] Implement: Human-in-the-loop
- [ ] Create: Analytics dashboard
- [ ] Document: Use cases

**Deliverable:** 3 portfolio-ready projects on GitHub

---

### Week 23-24: Resume & Interview Prep
**Time:** 10 hours
**Focus:** Job application materials

#### Resume Optimization
- [ ] Analyze: Job descriptions (use /jobs-analyze)
- [ ] Update: Resume with AI orchestrator keywords
- [ ] Add: Portfolio projects
- [ ] Optimize: For ATS systems

**Keywords to include:**
- AI Agents, LLM, LangChain, LangGraph
- Multi-Agent Systems, Orchestration, Tool Integration
- Production Deployment, Observability
- Hub-and-Spoke, Orchestrator-Worker Pattern

#### Interview Preparation
- [ ] Prepare: System design answers
- [ ] Practice: Agent architecture questions
- [ ] Prepare: Behavioral examples
- [ ] Create: Technical presentation

#### Common Interview Topics
1. "Explain how you designed a multi-agent system"
2. "Compare orchestration patterns"
3. "How do you handle agent memory?"
4. "Describe your tool integration approach"
5. "How do you monitor agent performance?"

**Deliverable:** ATS-optimized resume + interview materials

---

## Weekly Progress Tracking

Use this template each week:

```markdown
# Week X Progress

## Completed
- [ ] Item 1
- [ ] Item 2

## Time Invested
- Day 1: X hours
- Day 2: X hours
- Day 3: X hours
- Day 4: X hours
- Day 5: X hours
- **Total:** X hours

## Key Learnings
1. Learning 1
2. Learning 2

## Applied to QA Work
- Application 1
- Application 2

## Blockers
- Blocker 1

## Next Week Focus
- Focus area
```

---

## Next Actions

1. **Start:** Phase 1, Week 1, Day 1
2. **Update:** `progress.md` daily
3. **Use:** `/learn-today` command to get daily tasks
4. **Apply:** Concepts to your Nexus work immediately
5. **Document:** Everything in your learning notes

---

**Last Updated:** 2026-03-17
**Current Phase:** Not started
**Current Week:** 0
**Status:** Ready to begin
