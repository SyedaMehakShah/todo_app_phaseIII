---
id: 001
title: Phase III Constitution Creation
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Admin
command: /sp.constitution
labels: ["constitution", "phase-iii", "todo-ai-chatbot", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

# sp-constitution.md

## Phase III – Todo AI Chatbot System Constitution

---

### 1. Purpose

This document defines the **binding constitution** for Phase III of the Todo AI Chatbot project. It establishes the architectural laws, development rules, and evaluation constraints that must be followed exactly. Judges will evaluate the project against this constitution, not against implementation shortcuts.

---

### 2. Development Method Constitution

1. **Spec-Driven Development Law**
   Development must strictly follow this sequence:
   **Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code**

2. **No Manual Coding Law**
   All implementation must be generated via Claude Code. Manual edits are not permitted.

3. **Spec Authority Law**
   Specifications stored in `/specs` are the highest authority. If code and spec conflict, the spec is correct.

---

### 3. Claude Code Context Constitution

1. **Single Context Law**
   Claude Code must be able to see the entire project to make cross-cutting changes.

2. **Layered CLAUDE.md Law**

   * A root `CLAUDE.md` provides system-wide guidance
   * Subfolder `CLAUDE.md` files define local rules (frontend, backend, mcp)

3. **Spec Referencing Law**
   All Claude Code prompts must reference specs directly using:
   `@specs/filename.md`

---

### 4. Project Structure Constitution

1. **Clear Separation Law**
   Frontend and backend must live in separate top-level folders.

```
/frontend   # ChatKit UI
/backend    # FastAPI + Agents SDK + MCP
/specs      # All specifications
/migrations # Database migrations
```

2. **Navigation Clarity Law**
   Folder structure must be intuitive and judge-readable.

---

### 5. Core Architecture Constitution

1. **Stateless Server Law**
   The FastAPI server must hold no memory between requests.

2. **Database Supremacy Law**
   Neon PostgreSQL is the single source of truth for all state:

   * tasks
   * conversations
   * messages

3. **Conversation Persistence Law**
   Conversation state must survive server restarts without degradation.

---

### 6. Agent & MCP Constitution

1. **Agent Reasoning Law**
   The AI agent may reason, infer intent, and decide actions using OpenAI Agents SDK.

2. **Tool-Only Mutation Law**
   The agent must never directly modify the database. All mutations occur via MCP tools.

3. **MCP Statelessness Law**
   MCP tools must be stateless and persist all effects to the database.

4. **Official MCP SDK Law**
   MCP server must be implemented using the Official MCP SDK only.

---

### 7. MCP Tool Contract Constitution

The MCP server must expose exactly these tools:

* add_task
* list_tasks
* complete_task
* delete_task
* update_task

Tool inputs and outputs must match the specification exactly. No hidden parameters are allowed.

---

### 8. API Constitution

1. **Single Chat Endpoint Law**
   All interactions must flow through:
   `POST /api/{user_id}/chat`

2. **Stateless Request Cycle Law**
   Each request must follow:
   Receive → Fetch context → Reason → Tool call → Persist → Respond

3. **No Background Effects Law**
   No cron jobs, queues, or background mutations are permitted.

---

### 9. Agent Behavior Constitution

1. **Intent Mapping Law**
   Natural language must map to MCP tools as specified.

2. **Confirmation Law**
   Every successful action must be confirmed with a friendly response.

3. **Graceful Error Law**
   Errors must be human-readable and non-technical.

---

### 10. Technology Boundary Constitution

| Layer    | Mandatory Technology       |
| -------- | -------------------------- |
| Frontend | OpenAI ChatKit             |
| Backend  | FastAPI                    |
| AI       | OpenAI Agents SDK          |
| MCP      | Official MCP SDK           |
| ORM      | SQLModel                   |
| Database | Neon Serverless PostgreSQL |
| Auth     | Better Auth                |

No substitutions allowed.

---

### 11. Evaluation Constitution

Phase III is considered **valid** only if:

* The system is provably stateless
* All mutations occur via MCP tools
* Conversation r

## Response snapshot

Created Phase III Todo AI Chatbot Constitution v1.0.0 with 11 core principles:

1. **Spec-Driven Development** - Mandatory sequence: Spec → Plan → Tasks → Claude Code
2. **Stateless Server Architecture** - No memory between requests
3. **Database Supremacy** - Neon PostgreSQL as single source of truth
4. **Tool-Only Mutation** - All DB changes via MCP tools only
5. **MCP Tool Contract** - Exactly 5 tools: add_task, list_tasks, complete_task, delete_task, update_task
6. **Single Chat Endpoint** - All interactions via POST /api/{user_id}/chat with JWT
7. **Agent Behavior Standards** - Friendly confirmations, human-readable errors
8. **Clear Separation** - /frontend, /backend, /specs, /migrations structure
9. **Official SDK Mandate** - MCP SDK only, no alternatives
10. **Authentication via Better Auth** - JWT tokens with shared secret
11. **Layered Documentation** - Root and subfolder CLAUDE.md files

Technology stack locked: OpenAI ChatKit, FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon PostgreSQL, Better Auth.

## Outcome

- Impact: Established binding governance for Phase III development
- Tests: N/A (constitution document)
- Files: .specify/memory/constitution.md
- Next prompts: /sp.specify to create feature specs, /sp.plan for implementation planning
- Reflection: Successfully transformed user's constitutional requirements into structured, testable principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
