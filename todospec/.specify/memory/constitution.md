<!--
  Sync Impact Report
  ===================
  Version change: 0.0.0 → 1.0.0 (MAJOR - initial constitution establishment)

  Modified principles: N/A (new constitution)

  Added sections:
    - Core Principles (11 principles)
    - Technology Boundary Requirements
    - Development Workflow
    - Governance

  Removed sections: N/A (template placeholders replaced)

  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ (Constitution Check section aligns)
    - .specify/templates/spec-template.md ✅ (Requirements structure compatible)
    - .specify/templates/tasks-template.md ✅ (Phase structure compatible)

  Follow-up TODOs: None
-->

# Todo AI Chatbot System Constitution

## Core Principles

### I. Spec-Driven Development

Development MUST strictly follow this sequence:
**Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code**

- Specifications stored in `/specs` are the highest authority
- If code and spec conflict, the spec is correct
- All implementation MUST be generated via Claude Code; manual edits are not permitted

### II. Stateless Server Architecture

The FastAPI server MUST hold no memory between requests.

- Each request follows: Receive → Fetch context → Reason → Tool call → Persist → Respond
- No cron jobs, queues, or background mutations are permitted
- Conversation state MUST survive server restarts without degradation

### III. Database Supremacy

Neon PostgreSQL is the single source of truth for all state.

- All persistent data MUST be stored in the database: tasks, conversations, messages
- No in-memory state may be trusted across request boundaries
- Database schema changes require migration scripts in `/migrations`

### IV. Tool-Only Mutation

The AI agent MUST never directly modify the database.

- All mutations MUST occur via MCP tools exclusively
- MCP tools MUST be stateless and persist all effects to the database
- The agent may reason, infer intent, and decide actions, but execution flows through tools

### V. MCP Tool Contract

The MCP server MUST expose exactly these tools with no hidden parameters:

- `add_task` - Create a new task
- `list_tasks` - Retrieve tasks for a user
- `complete_task` - Mark a task as complete
- `delete_task` - Remove a task
- `update_task` - Modify task properties

Tool inputs and outputs MUST match the specification exactly.

### VI. Single Chat Endpoint

All interactions MUST flow through: `POST /api/{user_id}/chat`

- JWT token MUST be included in the Authorization header
- Requests without valid token receive 401 Unauthorized
- Each user only sees/modifies their own tasks

### VII. Agent Behavior Standards

Natural language MUST map to MCP tools as specified.

- Every successful action MUST be confirmed with a friendly response
- Errors MUST be human-readable and non-technical
- The agent may use OpenAI Agents SDK for reasoning and intent inference

### VIII. Clear Separation

Frontend and backend MUST live in separate top-level folders.

```
/frontend   # OpenAI ChatKit UI
/backend    # FastAPI + Agents SDK + MCP
/specs      # All specifications
/migrations # Database migrations
```

- Folder structure MUST be intuitive and judge-readable
- Claude Code MUST be able to see the entire project for cross-cutting changes

### IX. Official SDK Mandate

MCP server MUST be implemented using the Official MCP SDK only.

- No alternative MCP implementations are permitted
- SDK version MUST be documented in requirements

### X. Authentication via Better Auth

User authentication MUST use Better Auth with JWT tokens.

- Both frontend and backend MUST use the same secret key (BETTER_AUTH_SECRET)
- JWT tokens provide stateless authentication between services
- Token expiry MUST be enforced (default: 7 days)

### XI. Layered Documentation

Project documentation follows a hierarchy:

- Root `CLAUDE.md` provides system-wide guidance
- Subfolder `CLAUDE.md` files define local rules (frontend, backend, mcp)
- All Claude Code prompts MUST reference specs directly using `@specs/filename.md`

## Technology Boundary Requirements

| Layer    | Mandatory Technology       | Substitution Allowed |
|----------|----------------------------|----------------------|
| Frontend | OpenAI ChatKit             | No                   |
| Backend  | FastAPI                    | No                   |
| AI       | OpenAI Agents SDK          | No                   |
| MCP      | Official MCP SDK           | No                   |
| ORM      | SQLModel                   | No                   |
| Database | Neon Serverless PostgreSQL | No                   |
| Auth     | Better Auth                | No                   |

No substitutions are allowed. Technology choices are binding.

## Development Workflow

### Request Cycle

Every API request MUST follow this exact flow:

1. Receive request with JWT token
2. Validate token and extract user identity
3. Fetch conversation context from database
4. AI agent reasons about intent
5. Agent calls MCP tools (never direct DB access)
6. MCP tools persist changes to database
7. Return response to user

### Validation Requirements

Phase III is considered **valid** only if:

- The system is provably stateless
- All mutations occur via MCP tools
- Conversation state persists across server restarts
- User isolation is enforced (each user sees only their data)
- All technologies match the boundary requirements exactly

### Test Requirements

- Contract tests for MCP tool interfaces
- Integration tests for the chat endpoint
- Statelessness verification tests (restart server mid-conversation)

## Governance

This constitution supersedes all other practices for Phase III development.

### Amendment Process

1. Amendments require documentation in an ADR
2. All changes must be approved before implementation
3. Migration plan required for breaking changes

### Compliance Verification

- All PRs/reviews MUST verify compliance with this constitution
- Complexity beyond these requirements MUST be justified
- Use `CLAUDE.md` files for runtime development guidance

### Version Policy

- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
