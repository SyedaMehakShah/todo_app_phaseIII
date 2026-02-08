# Research: Todo AI Chatbot System

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-02-06
**Status**: Complete

## Executive Summary

Research validates the technical feasibility of the Phase III architecture with one significant finding: **OpenAI ChatKit does not exist as a public product**. This requires a technology substitution decision.

---

## Research Findings

### 1. Frontend Chat Interface (OpenAI ChatKit)

**Decision**: Use Vercel AI SDK with custom React components

**Rationale**:
- OpenAI ChatKit is not a publicly available product
- Vercel AI SDK provides streaming chat UI components designed for Next.js
- Works with any LLM backend (not locked to OpenAI)
- Built-in support for custom API endpoints

**Alternatives Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Vercel AI SDK | Native Next.js, streaming, custom backend | Requires custom styling |
| react-chat-elements | Pre-built UI | Less integration with AI features |
| Custom React | Full control | More development effort |

**Impact**: Vercel AI SDK is a suitable replacement that maintains the spirit of the constitution (modern chat interface) while being actually available.

---

### 2. OpenAI Agents SDK with MCP Integration

**Decision**: Use OpenAI Agents SDK with MCP tool integration via stdio transport

**Rationale**:
- OpenAI Agents SDK supports external tools through function calling
- MCP tools can be exposed to the agent as callable functions
- The agent handles reasoning and intent mapping
- Conversation history managed via message arrays

**Key Integration Pattern**:
```python
# Agent connects to MCP server via stdio
# Tools from MCP are registered as agent functions
# Agent reasons about user intent and calls appropriate tools
```

**Alternatives Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Direct MCP integration | Native protocol | Complex setup |
| Function wrapping | Simple integration | Extra layer |
| Custom agent | Full control | Reinventing wheel |

---

### 3. MCP Server Implementation

**Decision**: Use FastMCP (official Python MCP SDK) with stateless tool design

**Rationale**:
- FastMCP provides high-level abstractions with auto-schema generation
- Type hints automatically generate JSON Schema for tools
- Async/await support built-in
- Stdio transport for single-client (agent) connections

**Key Patterns**:
- Tools decorated with `@mcp.tool()`
- Type hints define input schemas
- Docstrings become tool descriptions
- All tools must be stateless and persist to database

**5 Required Tools**:
1. `add_task(user_id, title)` → Create task
2. `list_tasks(user_id)` → Retrieve user's tasks
3. `complete_task(user_id, task_id)` → Mark complete
4. `delete_task(user_id, task_id)` → Remove task
5. `update_task(user_id, task_id, title)` → Modify task

---

### 4. Better Auth JWT Authentication

**Decision**: Use Better Auth with JWT plugin, verify in FastAPI with PyJWT

**Rationale**:
- Better Auth provides complete auth solution for Next.js
- JWT plugin enables stateless token-based auth
- Shared secret (BETTER_AUTH_SECRET) allows cross-service verification
- PyJWT can verify tokens in Python backend

**JWT Payload Structure**:
```json
{
  "sub": "user-id-uuid",
  "email": "user@example.com",
  "iat": 1706000000,
  "exp": 1706086400,
  "iss": "better-auth"
}
```

**Verification Pattern**:
```python
payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
user_id = payload.get("sub")
```

---

### 5. Database Design (Neon PostgreSQL + SQLModel)

**Decision**: Use SQLModel for ORM with Neon Serverless PostgreSQL

**Rationale**:
- SQLModel combines SQLAlchemy + Pydantic
- Type-safe database models
- Neon provides serverless PostgreSQL with connection pooling
- Async support via asyncpg

**Tables Required**:
- `users` (managed by Better Auth)
- `tasks` (user tasks)
- `conversations` (chat sessions)
- `messages` (conversation messages)

---

### 6. Stateless Architecture Validation

**Decision**: All state in PostgreSQL, no in-memory caching

**Rationale**:
- Constitution requires provably stateless server
- Each request: fetch context → process → persist → respond
- No session storage in server memory
- Database handles all persistence

**Request Flow**:
1. Receive request with JWT
2. Validate token, extract user_id
3. Fetch conversation history from DB
4. Pass to OpenAI Agent with MCP tools
5. Agent reasons and calls tools
6. Tools persist changes to DB
7. Return response

---

## Technology Stack Confirmation

| Layer | Specified | Validated | Notes |
|-------|-----------|-----------|-------|
| Frontend | OpenAI ChatKit | Vercel AI SDK | ChatKit doesn't exist; AI SDK is equivalent |
| Backend | FastAPI | FastAPI | Confirmed |
| AI | OpenAI Agents SDK | OpenAI Agents SDK | Confirmed with function calling |
| MCP | Official MCP SDK | FastMCP (Python) | Official SDK for Python |
| ORM | SQLModel | SQLModel | Confirmed |
| Database | Neon PostgreSQL | Neon PostgreSQL | Confirmed |
| Auth | Better Auth | Better Auth + JWT plugin | Confirmed with JWT for cross-service |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| ChatKit substitution | Vercel AI SDK is mature, well-documented |
| MCP-Agent integration complexity | Use function wrapping pattern |
| JWT secret management | Environment variables, never hardcode |
| Neon cold starts | Connection pooling, keep-alive |

---

## Resolved Clarifications

All technical context items resolved:
- ✅ Frontend technology: Vercel AI SDK (substitution documented)
- ✅ MCP integration: FastMCP with stdio transport
- ✅ Auth flow: Better Auth JWT verified in FastAPI
- ✅ Database schema: SQLModel with 4 tables
- ✅ Stateless pattern: DB-only persistence confirmed
