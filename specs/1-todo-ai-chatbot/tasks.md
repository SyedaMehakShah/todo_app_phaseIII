# Tasks: Todo AI Chatbot System

**Input**: Design documents from `/specs/1-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md

**Tests**: Tests included for critical paths (MCP tools, chat endpoint, auth flow)

**Organization**: Tasks organized by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, etc.)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and install dependencies

- [x] T001 Create project directory structure per plan.md at C:\Users\Admin\phase-III\
- [x] T002 [P] Initialize backend Python project with requirements.txt in backend/
- [x] T003 [P] Initialize frontend Next.js project with package.json in frontend/
- [x] T004 [P] Create backend/.env.example with required environment variables
- [x] T005 [P] Create frontend/.env.local.example with required environment variables
- [x] T006 [P] Create migrations/README.md with migration instructions
- [x] T007 Create CLAUDE.md files for backend/ and frontend/ directories
- [x] T008 [P] Configure backend linting with pyproject.toml in backend/
- [x] T009 [P] Configure frontend linting with eslint.config.js in frontend/

**Checkpoint**: Project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [x] T010 Create database connection service in backend/src/services/database.py
- [x] T011 Create Task model with SQLModel in backend/src/models/task.py
- [x] T012 [P] Create Conversation model in backend/src/models/conversation.py
- [x] T013 [P] Create Message model in backend/src/models/message.py
- [x] T014 Create models/__init__.py exporting all models in backend/src/models/__init__.py
- [x] T015 Create initial migration SQL in migrations/001_initial_schema.sql

### Backend Core

- [x] T016 Create configuration module in backend/config.py
- [x] T017 Create FastAPI application entry point in backend/main.py
- [x] T018 Create health check endpoint in backend/src/api/health.py
- [x] T019 Implement JWT verification middleware in backend/middleware.py

### MCP Server Setup

- [x] T020 Create MCP server initialization in backend/src/mcp/server.py
- [x] T021 Create MCP __init__.py in backend/src/mcp/__init__.py

### Frontend Core

- [x] T022 Create Better Auth configuration in frontend/src/lib/auth.ts
- [x] T023 Create API client utility in frontend/src/lib/api.ts
- [x] T024 Create auth API route handler in frontend/src/app/api/auth/[...all]/route.ts

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1)

**Goal**: Users can sign up, sign in, maintain sessions, and sign out

**Independent Test**: Complete signup → signin → session persist → signout flow

### Implementation for User Story 1

- [x] T025 [US1] Create landing page in frontend/src/app/page.tsx
- [x] T026 [P] [US1] Create signup page in frontend/src/app/signup/page.tsx
- [x] T027 [P] [US1] Create signin page in frontend/src/app/signin/page.tsx
- [x] T028 [US1] Create auth form components in frontend/src/components/AuthForm.tsx
- [x] T029 [US1] Implement protected route wrapper in frontend/src/components/ProtectedRoute.tsx
- [x] T030 [US1] Create chat page shell (protected) in frontend/src/app/chat/page.tsx
- [x] T031 [US1] Add signout functionality to chat page header
- [ ] T032 [US1] Test auth flow: signup creates account and auto-signs in
- [ ] T033 [US1] Test auth flow: signin with valid credentials redirects to chat
- [ ] T034 [US1] Test auth flow: session persists on browser refresh
- [ ] T035 [US1] Test auth flow: signout terminates session

**Checkpoint**: User Story 1 complete - authentication fully functional

---

## Phase 4: User Story 2 - Natural Language Task Creation (Priority: P2)

**Goal**: Users can create tasks via natural language chat

**Independent Test**: Send "Add task: buy milk" → receive confirmation → task exists in DB

### MCP Tool Implementation

- [x] T036 [US2] Implement add_task MCP tool in backend/src/mcp/tools.py

### Agent Setup

- [x] T037 [US2] Create OpenAI Agent service in backend/src/services/agent.py
- [x] T038 [US2] Implement agent tool registration for add_task

### Chat Endpoint

- [x] T039 [US2] Create conversation service in backend/src/services/conversation.py
- [x] T040 [US2] Implement chat endpoint in backend/src/api/chat.py
- [x] T041 [US2] Register chat router in backend/main.py

### Frontend Chat UI

- [x] T042 [US2] Create MessageInput component in frontend/src/components/MessageInput.tsx
- [x] T043 [US2] Create MessageList component in frontend/src/components/MessageList.tsx
- [x] T044 [US2] Create Chat component integrating input and messages in frontend/src/components/Chat.tsx
- [x] T045 [US2] Integrate Chat component into chat page frontend/src/app/chat/page.tsx
- [ ] T046 [US2] Test: send task creation message, verify confirmation response
- [ ] T047 [US2] Test: verify task persisted to database after creation

**Checkpoint**: User Story 2 complete - task creation via chat works

---

## Phase 5: User Story 3 - Task Listing and Querying (Priority: P3)

**Goal**: Users can view their tasks via chat

**Independent Test**: Ask "Show my tasks" → see list of tasks

### MCP Tool Implementation

- [x] T048 [US3] Implement list_tasks MCP tool in backend/src/mcp/tools.py
- [x] T049 [US3] Register list_tasks tool with agent in backend/src/services/agent.py

### Integration

- [x] T050 [US3] Update agent system prompt to handle list queries
- [ ] T051 [US3] Test: request task list with existing tasks, verify all displayed
- [ ] T052 [US3] Test: request task list with no tasks, verify appropriate response
- [ ] T053 [US3] Test: ask task count, verify accurate number returned

**Checkpoint**: User Story 3 complete - task listing works

---

## Phase 6: User Story 4 - Task Completion (Priority: P4)

**Goal**: Users can mark tasks complete via chat

**Independent Test**: Create task → say "I finished [task]" → task marked complete

### MCP Tool Implementation

- [x] T054 [US4] Implement complete_task MCP tool in backend/src/mcp/tools.py
- [x] T055 [US4] Register complete_task tool with agent in backend/src/services/agent.py

### Integration

- [x] T056 [US4] Update agent prompt to handle completion intents
- [ ] T057 [US4] Test: complete existing task, verify status change
- [ ] T058 [US4] Test: attempt to complete non-existent task, verify helpful error

**Checkpoint**: User Story 4 complete - task completion works

---

## Phase 7: User Story 5 - Task Deletion (Priority: P5)

**Goal**: Users can delete tasks via chat

**Independent Test**: Create task → say "Delete [task]" → task removed

### MCP Tool Implementation

- [x] T059 [US5] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [x] T060 [US5] Register delete_task tool with agent in backend/src/services/agent.py

### Integration

- [x] T061 [US5] Update agent prompt to handle deletion intents
- [ ] T062 [US5] Test: delete existing task, verify removed from DB
- [ ] T063 [US5] Test: attempt to delete non-existent task, verify helpful error

**Checkpoint**: User Story 5 complete - task deletion works

---

## Phase 8: User Story 6 - Task Updates (Priority: P6)

**Goal**: Users can modify task details via chat

**Independent Test**: Create task → say "Change [task] to [new title]" → task updated

### MCP Tool Implementation

- [x] T064 [US6] Implement update_task MCP tool in backend/src/mcp/tools.py
- [x] T065 [US6] Register update_task tool with agent in backend/src/services/agent.py

### Integration

- [x] T066 [US6] Update agent prompt to handle update intents
- [ ] T067 [US6] Test: update existing task title, verify change persisted
- [ ] T068 [US6] Test: attempt to update non-existent task, verify helpful error

**Checkpoint**: User Story 6 complete - task updates work

---

## Phase 9: User Story 7 - Conversation Persistence (Priority: P7)

**Goal**: Conversation history persists across sessions

**Independent Test**: Have conversation → close browser → sign in again → see history

### Implementation

- [x] T069 [US7] Implement message persistence in conversation service backend/src/services/conversation.py
- [x] T070 [US7] Add conversation history endpoint in backend/src/api/chat.py
- [x] T071 [US7] Load conversation history on chat page mount in frontend/src/app/chat/page.tsx
- [ ] T072 [US7] Test: conversation history loads on signin
- [ ] T073 [US7] Test: history persists across server restart

**Checkpoint**: User Story 7 complete - conversation persistence works

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T074 [P] Add error boundary component in frontend/src/components/ErrorBoundary.tsx
- [ ] T075 [P] Implement loading states for chat in frontend/src/components/Chat.tsx
- [ ] T076 [P] Add input validation for message length in frontend/src/components/MessageInput.tsx
- [ ] T077 [P] Implement user-friendly error messages in backend/src/api/chat.py
- [ ] T078 [P] Add request logging middleware in backend/main.py
- [ ] T079 Run quickstart.md validation checklist
- [ ] T080 Final integration test: complete user journey (signup → create → list → complete → delete)

**Checkpoint**: All user stories complete and polished

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ──────────────────────────────────────────┐
    │                                                             │
    ▼                                                             │
Phase 3 (US1: Auth) ─────────────────────────────────────────────┤
    │                                                             │
    ▼                                                             │
Phase 4 (US2: Create Tasks) ─────────────────────────────────────┤
    │                                                             │
    ├──► Phase 5 (US3: List Tasks) ──────────────────────────────┤
    │                                                             │
    ├──► Phase 6 (US4: Complete Tasks) ──────────────────────────┤
    │                                                             │
    ├──► Phase 7 (US5: Delete Tasks) ─────────────────────────────┤
    │                                                             │
    └──► Phase 8 (US6: Update Tasks) ─────────────────────────────┤
                                                                  │
Phase 9 (US7: Conversation Persistence) ◄─────────────────────────┤
    │                                                             │
    ▼                                                             │
Phase 10 (Polish) ◄───────────────────────────────────────────────┘
```

### User Story Dependencies

- **US1 (Auth)**: No dependencies - can start after Foundational
- **US2 (Create)**: Depends on US1 (need authenticated user)
- **US3 (List)**: Depends on US2 (need tasks to list)
- **US4 (Complete)**: Depends on US2 (need tasks to complete)
- **US5 (Delete)**: Depends on US2 (need tasks to delete)
- **US6 (Update)**: Depends on US2 (need tasks to update)
- **US7 (Persistence)**: Depends on US2 (need conversation to persist)

**Note**: US3-US6 can run in parallel after US2 completes

### Within Each User Story

1. MCP tools before agent integration
2. Backend before frontend
3. Core implementation before tests

### Parallel Opportunities

**Phase 1**:
- T002, T003, T004, T005, T006 can run in parallel
- T008, T009 can run in parallel

**Phase 2**:
- T012, T013 can run in parallel (after T011)

**Phase 3**:
- T026, T027 can run in parallel

**Phases 5-8** (after Phase 4):
- US3, US4, US5, US6 can all run in parallel

**Phase 10**:
- T074, T075, T076, T077, T078 can run in parallel

---

## Parallel Execution Example: Phases 5-8

After Phase 4 (US2) completes, these can run simultaneously:

```bash
# Terminal 1: US3 - List Tasks
T048 → T049 → T050 → T051-T053

# Terminal 2: US4 - Complete Tasks
T054 → T055 → T056 → T057-T058

# Terminal 3: US5 - Delete Tasks
T059 → T060 → T061 → T062-T063

# Terminal 4: US6 - Update Tasks
T064 → T065 → T066 → T067-T068
```

---

## Implementation Strategy

### MVP Scope (Recommended)

**Minimum Viable Product**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) + Phase 5 (US3)

This delivers:
- User authentication
- Task creation via chat
- Task listing via chat

**MVP Task Count**: 53 tasks (T001-T053)

### Incremental Delivery

| Milestone | User Stories | Cumulative Tasks |
|-----------|--------------|------------------|
| Auth MVP  | US1          | 35 tasks         |
| Core MVP  | US1, US2, US3| 53 tasks         |
| Full CRUD | US1-US6      | 68 tasks         |
| Complete  | US1-US7      | 80 tasks         |

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 80 |
| **Setup Phase** | 9 tasks |
| **Foundational Phase** | 15 tasks |
| **US1 (Auth)** | 11 tasks |
| **US2 (Create)** | 12 tasks |
| **US3 (List)** | 6 tasks |
| **US4 (Complete)** | 5 tasks |
| **US5 (Delete)** | 5 tasks |
| **US6 (Update)** | 5 tasks |
| **US7 (Persistence)** | 5 tasks |
| **Polish Phase** | 7 tasks |
| **Parallel Opportunities** | 23 tasks marked [P] |
| **Suggested MVP** | Phases 1-5 (53 tasks) |
