# Backend Development Guidelines

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **AI**: OpenAI Agents SDK
- **MCP**: Official MCP SDK (FastMCP)

## Architecture Rules

### Stateless Server (Constitution Principle II)
- The server MUST hold no memory between requests
- All state MUST be persisted to PostgreSQL
- No in-memory caching of user data

### Tool-Only Mutation (Constitution Principle IV)
- The AI agent MUST never directly modify the database
- All mutations MUST occur via MCP tools
- MCP tools are stateless and persist to database

### Single Chat Endpoint (Constitution Principle VI)
- All interactions flow through: `POST /api/{user_id}/chat`
- JWT token required in Authorization header
- User isolation enforced on every request

## MCP Tools Contract (Constitution Principle V)

Exactly 5 tools, no hidden parameters:
- `add_task(user_id, title)` → Create task
- `list_tasks(user_id)` → Get user's tasks
- `complete_task(user_id, task_id)` → Mark complete
- `delete_task(user_id, task_id)` → Remove task
- `update_task(user_id, task_id, title)` → Modify task

## File Structure

```
backend/
├── src/
│   ├── api/          # FastAPI route handlers
│   ├── models/       # SQLModel database models
│   ├── services/     # Business logic
│   └── mcp/          # MCP server and tools
├── main.py           # FastAPI application
├── middleware.py     # JWT verification
└── config.py         # Configuration
```

## Code Standards

- Use async/await for all database operations
- Log to stderr for MCP compatibility
- Return human-readable errors (no technical details)
- Verify user_id matches JWT sub claim on every request
