# Quickstart: Todo AI Chatbot System

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-02-06

---

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Neon PostgreSQL account
- OpenAI API key

---

## Environment Setup

### 1. Clone and Navigate

```bash
cd C:\Users\Admin\phase-III
```

### 2. Create Environment Files

**Frontend (.env.local)**:
```bash
# Create frontend/.env.local
BETTER_AUTH_SECRET=your-32-char-secret-key-here-min
BETTER_AUTH_URL=http://localhost:3000/api/auth
DATABASE_URL=postgresql://user:pass@your-neon-host/dbname?sslmode=require
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env)**:
```bash
# Create backend/.env
BETTER_AUTH_SECRET=your-32-char-secret-key-here-min
DATABASE_URL=postgresql://user:pass@your-neon-host/dbname?sslmode=require
OPENAI_API_KEY=sk-your-openai-api-key
```

**Generate Secret**:
```bash
openssl rand -base64 32
```

---

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn sqlmodel asyncpg python-dotenv pyjwt httpx mcp openai-agents
```

### 3. Run Migrations

```bash
# Using alembic or direct SQL
python -m alembic upgrade head
```

### 4. Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Install Required Packages

```bash
npm install better-auth ai @ai-sdk/openai
```

### 3. Start Development Server

```bash
npm run dev
```

---

## Verification Steps

### 1. Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}
```

### 2. Create Test User

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email and password
4. Verify redirect to chat interface

### 3. Test Chat Flow

1. Type: "Add a task to buy milk"
2. Verify response: "I've added 'buy milk' to your tasks!"
3. Type: "Show my tasks"
4. Verify task appears in list
5. Type: "I finished buying milk"
6. Verify task marked complete

### 4. Test Persistence

1. Close browser
2. Reopen http://localhost:3000
3. Sign in with same credentials
4. Verify conversation history displays
5. Verify tasks persist

### 5. Test Statelessness

1. Stop backend server (Ctrl+C)
2. Start backend server again
3. Refresh frontend
4. Verify all data persists (tasks, conversations)

---

## Project Structure

```
C:\Users\Admin\phase-III\
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/auth/[...all]/route.ts
│   │   │   ├── chat/page.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   └── Chat.tsx
│   │   └── lib/
│   │       └── auth.ts
│   ├── .env.local
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── src/
│   │   ├── api/
│   │   │   └── chat.py
│   │   ├── models/
│   │   │   ├── task.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── services/
│   │   │   ├── agent.py
│   │   │   └── database.py
│   │   └── mcp/
│   │       └── tools.py
│   ├── main.py
│   ├── middleware.py
│   ├── .env
│   └── requirements.txt
│
├── migrations/               # Database migrations
│   └── 001_initial.sql
│
├── specs/                    # Specifications
│   └── 1-todo-ai-chatbot/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       └── contracts/
│           ├── api.yaml
│           └── mcp-tools.md
│
└── CLAUDE.md                 # Project guidance
```

---

## Common Issues

### JWT Verification Fails

- Ensure BETTER_AUTH_SECRET is identical in both .env files
- Check token hasn't expired
- Verify algorithm is HS256

### Database Connection Error

- Verify DATABASE_URL is correct
- Check Neon dashboard for connection limits
- Ensure SSL mode is enabled (?sslmode=require)

### MCP Tools Not Working

- Check OpenAI API key is valid
- Verify MCP server is running
- Check logs for tool invocation errors

### CORS Errors

- Ensure frontend URL is in backend CORS whitelist
- Check API URL in frontend .env matches backend

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Follow task order: Setup → Foundational → User Stories
3. Test each user story independently before proceeding
