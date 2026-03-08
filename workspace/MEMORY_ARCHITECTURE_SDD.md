# Software Design Document (SDD): OpenClaw Memory Architecture & RAG Implementation

## 1. Introduction
This document outlines the proposed architecture for managing the long-term memory of the OpenClaw agent ecosystem. As the context size has grown significantly (currently ~56KB for the main agent), it is necessary to logically separate knowledge domains and implement a Retrieval-Augmented Generation (RAG) system using OpenAI embeddings to maintain performance, reduce token costs, and prevent context dilution.

---

## 2. Current State Analysis (As-Is)

Currently, the `main` agent (`Nexus`) relies on a single, monolithic memory file:
**Location:** `/Users/ihorsolopii/.openclaw/workspace/MEMORY.md`
**Size:** ~56KB (1184+ lines)
**Status:** Exceeds the default bootstrap limit (truncation warnings observed: 60% truncated).

### 2.1 Content of Current `MEMORY.md`
The current file is an amalgamation of unrelated domains:
1. **Personal/Life Goals:** Austria Information Hub, Financial Goal (Apartment).
2. **Infrastructure/Integrations:** Gmail Checking, Jira API integrations, Slack Threading System.
3. **API Documentation:** Website API, BackOffice API, Wallet Service API endpoints and auth mechanisms.
4. **QA & Automation (Minebit/NextCode):** Playwright Framework Architecture, API Testing Strategy, UI Knowledge Base, Test Data Scripts, Burger Approach Methodology, TestRail specific learnings.
5. **Domain Knowledge (Casino/Crypto):** Bonus Configuration, Segmentation problems, Realtime Rakeback logic, Deposit Flows.

### 2.2 Problems with Current Architecture
- **High Cost:** Injecting 44KB+ of raw text into every prompt consumes unnecessary tokens.
- **Latency:** High Time To First Token (TTFT) due to massive context size.
- **Hallucinations/Confusion:** The agent may mix up Playwright testing logic with personal financial goals or unrelated API endpoints.
- **System Limits:** OpenClaw automatically truncates large bootstrap files, meaning critical information might be silently dropped during execution.

---

## 3. Proposed Memory Architecture (To-Be)

To align with the multi-agent workspace setup, the overarching principle is **Physical Separation of Concerns**. Each agent should only possess the memory relevant to its specific tasks.

### 3.1 Memory Distribution Strategy

We will split the monolithic `MEMORY.md` into specialized files across the existing workspaces:

#### A. QA Agent (`~/.openclaw/workspace-qa-agent/MEMORY.md`)
**Owner:** QA Agent
**Contents to Migrate:**
- Playwright Framework Architecture & Project Configuration.
- UI Knowledge Base & Locators.
- Structured Test Design Methodology (The "Burger Approach").
- QA Testing Learnings (e.g., CT‑824 Realtime Rakeback, test data script usage).
- TestRail Standards and integration notes.

#### B. API Docs Agent (`~/.openclaw/workspace-api-docs/MEMORY.md`)
**Owner:** API Docs Agent
**Contents to Migrate:**
- Website API (Client Frontend) overview.
- BackOffice API (AdminWeb vs BackOffice UI authentication flows).
- Wallet Service API operations (Debit vs Credit logic).
- Bonus Configuration logic (Domain knowledge about Strapi, Smartico).

#### C. Jira Watcher (`~/.openclaw/workspace-jira-watcher/MEMORY.md`)
**Owner:** Jira Watcher
**Contents to Migrate:**
- Jira API Integration (`go-jira` credentials).
- Gmail Jira notification integration details.
- Slack Threading System rules and workflows.

#### D. Nexus (Main) (`~/.openclaw/workspace/MEMORY.md`)
**Owner:** Nexus (Main Agent)
**Contents Retained:**
- Personal goals (Financial Goal: Apartment).
- Austria Information Hub.
- High-level orchestration notes and global skills.

---

## 4. Implementation RAG (Memory Search) via OpenAI

Even with split files, an individual agent's memory will eventually grow large. To solve this, we will activate OpenClaw's built-in **Memory Search (RAG)** using OpenAI's highly efficient embedding models.

### 4.1 Why OpenAI for Embeddings?
- **Cost-Efficiency:** `text-embedding-3-small` costs only $0.02 per 1,000,000 tokens.
- **Performance:** Industry standard for semantic search, ensuring high accuracy when retrieving relevant context blocks.
- **Decoupling:** You continue using Z.AI (GLM) and DeepSeek for generation (LLM), using OpenAI *strictly* for background vectorization.

### 4.2 Configuration Steps

**Step 1: Obtain OpenAI API Key**
Create an account on the OpenAI platform, add a minimum balance ($5 is sufficient for years of embedding usage), and generate an API key.

**Step 2: Add API Key to OpenClaw Environment**
Update `~/.openclaw/openclaw.json` to include the OpenAI API key securely:
```json
"env": {
  "DEEPSEEK_API_KEY": "...",
  "ZAI_API_KEY": "...",
  "OPENAI_API_KEY": "sk-proj-YOUR_OPENAI_KEY"
}
```

**Step 3: Define OpenAI Provider in Config**
Add the OpenAI provider specifically for embeddings in `openclaw.json` under `models.providers`:
```json
"openai": {
  "api": "openai-completions",
  "apiKey": "${OPENAI_API_KEY}",
  "models": [
    {
      "id": "text-embedding-3-small",
      "name": "Text Embedding 3 Small",
      "input": ["text"]
    }
  ]
}
```

**Step 4: Enable Memory Search in Defaults**
Configure the agents to use RAG automatically by updating `agents.defaults` in `openclaw.json`:
```json
"agents": {
  "defaults": {
    "memorySearch": {
      "enabled": true,
      "provider": "openai/text-embedding-3-small",
      "chunkSize": 1000,
      "overlap": 200
    }
  }
}
```

**Step 5: Initialization and Verification**
Once configured, run the following command to index the existing memory files:
```bash
openclaw memory status --deep
```
This command will chunk the `.md` files, send them to OpenAI to create vector embeddings, and store them in the local session state.

### 4.3 RAG Workflow at Runtime
1. **User asks a question** (e.g., "How do I trigger a bonus?").
2. **OpenClaw intercepts** the request before sending it to DeepSeek/GLM.
3. OpenClaw converts the user's question into a vector using OpenAI.
4. It compares this vector against the stored Memory vectors.
5. It extracts only the Top-K most relevant chunks (e.g., the specific paragraph about `MakeManualRedirectPayment`).
6. It dynamically injects *only* those specific chunks into the LLM prompt.

---

## 5. Execution Plan

1. **Phase 1: Architecture Review** (Current Step) — Review and approve this SDD.
2. **Phase 2: Physical Splitting** — Execute a script to chunk `~/.openclaw/workspace/MEMORY.md` into the specialized workspace directories.
3. **Phase 3: Cleanup** — Remove the moved sections from the main `MEMORY.md`.
4. **Phase 4: API Key Provisioning** — User creates OpenAI key and provisions it in the environment.
5. **Phase 5: RAG Activation** — Apply `openclaw.json` updates and run the memory indexer.
