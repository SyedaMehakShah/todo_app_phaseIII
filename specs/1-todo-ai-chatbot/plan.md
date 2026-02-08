# Implementation Plan: Todo AI Chatbot System

**Branch**: `1-todo-ai-chatbot` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-todo-ai-chatbot/spec.md`

---

## Summary

Transform the todo application into a multi-user web application with an AI chatbot interface. Users interact via natural language chat to manage tasks. The system uses OpenAI Agents SDK for reasoning, MCP tools for task operations, and persists all state to Neon PostgreSQL. Authentication handled by Better Auth with JWT tokens verified in FastAPI backend.

---

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/Node.js 18+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK, Better Auth, Vercel AI SDK
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web (Linux server for backend, Vercel for frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5s response time for 95% of requests, 100 concurrent users
**Constraints**: Stateless server, all mutations via MCP tools, JWT auth required
**Scale/Scope**: MVP with single conversation per user, English only

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Following Spec → Plan → Tasks → Implement |
| II. Stateless Server | ✅ PASS | All state in PostgreSQL, no in-memory |
| III. Database Supremacy | ✅ PASS | Neon PostgreSQL as single source of truth |
| IV. Tool-Only Mutation | ✅ PASS | Agent uses MCP tools for all DB changes |
| V. MCP Tool Contract | ✅ PASS | 5 tools defined: add/list/complete/delete/update |
| VI. Single Chat Endpoint | ✅ PASS | POST /api/{user_id}/chat |
| VII. Agent Behavior | ✅ PASS | Friendly confirmations, human-readable errors |
| VIII. Clear Separation | ✅ PASS | /frontend, /backend, /specs, /migrations |
| IX. Official SDK Mandate | ✅ PASS | Using official MCP Python SDK (FastMCP) |
| X. Better Auth | ✅ PASS | JWT with shared secret for cross-service |
| XI. Layered Documentation | ✅ PASS | CLAUDE.md at root and in subfolders |

**Technology Substitution**: OpenAI ChatKit → Vercel AI SDK (ChatKit doesn't exist publicly). This maintains the spirit of the constitution while using an available technology. See [research.md](./research.md) for details.

---

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-ai-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology research
├── data-model.md        # Database schema
├── quickstart.md        # Setup guide
├── contracts/           # API contracts
│   ├── api.yaml         # OpenAPI spec
│   └── mcp-tools.md     # MCP tool contracts
└── tasks.md             # Implementation tasks (from /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── api/auth/[...all]/route.ts  # Better Auth handler
│   │   ├── chat/page.tsx               # Chat interface
│   │   ├── signin/page.tsx             # Sign in page
│   │   ├── signup/page.tsx             # Sign up page
│   │   └── page.tsx                    # Landing page
│   ├── components/
│   │   ├── Chat.tsx                    # Chat component
│   │   ├── MessageList.tsx             # Message display
│   │   └── MessageInput.tsx            # Input component
│   └── lib/
│       ├── auth.ts                     # Better Auth config
│       └── api.ts                      # API client
├── .env.local
└── package.json

backend/
├── src/
│   ├── api/
│   │   ├── chat.py                     # Chat endpoint
│   │   └── health.py                   # Health check
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py                     # Task model
│   │   ├── conversation.py             # Conversation model
│   │   └── message.py                  # Message model
│   ├── services/
│   │   ├── agent.py                    # OpenAI Agent service
│   │   ├── database.py                 # Database connection
│   │   └── conversation.py             # Conversation service
│   └── mcp/
│       ├── __init__.py
│       ├── server.py                   # MCP server setup
│       └── tools.py                    # MCP tool implementations
├── main.py                             # FastAPI app
├── middleware.py                       # JWT verification
├── config.py                           # Configuration
├── .env
└── requirements.txt

migrations/
├── 001_initial_schema.sql
└── README.md

tests/
├── backend/
│   ├── contract/
│   │   └── test_mcp_tools.py
│   ├── integration/
│   │   └── test_chat_endpoint.py
│   └── unit/
│       └── test_models.py
└── frontend/
    └── components/
        └── Chat.test.tsx
```

**Structure Decision**: Web application structure with separate frontend and backend directories as required by Constitution Principle VIII.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Better Auth │  │  Chat UI     │  │  Vercel AI SDK       │  │
│  │  (JWT)       │  │  Components  │  │  (Streaming)         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ JWT Token + Message
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  JWT         │  │  Chat        │  │  Conversation        │  │
│  │  Middleware  │──│  Endpoint    │──│  Service             │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   OpenAI Agents SDK                       │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Agent: Reasons about user intent                  │  │  │
│  │  │  → Calls MCP tools based on intent                 │  │  │
│  │  │  → Returns friendly response                       │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────┬───────────────────────────┘  │
│                                 │                                │
│                                 ▼                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      MCP Server                           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │ add_task │ │list_tasks│ │ complete │ │ delete   │    │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │  │
│  │  ┌──────────┐                                            │  │
│  │  │ update   │  All tools stateless, persist to DB        │  │
│  │  └──────────┘                                            │  │
│  └──────────────────────────────┬───────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Neon PostgreSQL                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  users   │  │  tasks   │  │ convers. │  │ messages │        │
│  │(BetterAuth│  │          │  │          │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Request Flow

```
1. User types message in Chat UI
         │
         ▼
2. Frontend sends POST /api/{user_id}/chat
   Headers: Authorization: Bearer <JWT>
   Body: { "message": "Add task: buy milk" }
         │
         ▼
3. JWT Middleware validates token
   - Verify signature with BETTER_AUTH_SECRET
   - Extract user_id from 'sub' claim
   - Verify user_id matches path parameter
         │
         ▼
4. Chat Endpoint fetches conversation context
   - Get or create conversation for user
   - Load recent messages from DB
         │
         ▼
5. OpenAI Agent processes message
   - Receives: user message + conversation history
   - Reasons about intent (add task? list? complete?)
   - Decides which MCP tool to call
         │
         ▼
6. Agent calls MCP tool (e.g., add_task)
   - Tool receives: user_id, title
   - Tool inserts task into PostgreSQL
   - Tool returns: success + task details
         │
         ▼
7. Agent generates friendly response
   - "I've added 'buy milk' to your tasks!"
         │
         ▼
8. Chat Endpoint persists messages
   - Save user message to DB
   - Save assistant response to DB
         │
         ▼
9. Return response to frontend
   { "message": "I've added...", "conversation_id": "..." }
```

---

## Complexity Tracking

No constitution violations requiring justification.

| Consideration | Decision | Rationale |
|--------------|----------|-----------|
| ChatKit substitution | Vercel AI SDK | ChatKit doesn't exist; AI SDK provides equivalent functionality |
| MCP transport | stdio | Single agent client, simpler than HTTP/SSE |
| Conversation model | One per user | MVP simplification, can extend later |

---

## Generated Artifacts

- [x] research.md - Technology research and decisions
- [x] data-model.md - Database schema and SQLModel definitions
- [x] contracts/api.yaml - OpenAPI specification
- [x] contracts/mcp-tools.md - MCP tool contracts
- [x] quickstart.md - Setup and verification guide

---

## Next Steps

Run `/sp.tasks` to generate implementation tasks based on this plan.
