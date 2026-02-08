# Data Model: Todo AI Chatbot System

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-02-06
**ORM**: SQLModel
**Database**: Neon Serverless PostgreSQL

---

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │      Task       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │──┐    │ id (PK)         │
│ email           │  │    │ user_id (FK)    │──┐
│ name            │  │    │ title           │  │
│ email_verified  │  │    │ completed       │  │
│ created_at      │  │    │ created_at      │  │
│ updated_at      │  │    │ updated_at      │  │
└─────────────────┘  │    └─────────────────┘  │
                     │                         │
                     │    ┌─────────────────┐  │
                     │    │  Conversation   │  │
                     │    ├─────────────────┤  │
                     └────│ id (PK)         │  │
                          │ user_id (FK)    │──┘
                          │ created_at      │
                          │ updated_at      │
                          └─────────────────┘
                                   │
                                   │
                          ┌─────────────────┐
                          │    Message      │
                          ├─────────────────┤
                          │ id (PK)         │
                          │ conversation_id │
                          │ role            │
                          │ content         │
                          │ created_at      │
                          └─────────────────┘
```

---

## Entities

### User (Managed by Better Auth)

Better Auth manages the user table. Do not modify directly.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| name | VARCHAR(255) | NULLABLE | Display name |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Note**: Better Auth manages this table schema. Reference only.

---

### Task

User's todo items managed via MCP tools.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique identifier |
| user_id | UUID | FK → users.id, NOT NULL | Task owner |
| title | VARCHAR(500) | NOT NULL | Task description |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last modification |

**Indexes**:
- `idx_tasks_user_id` on (user_id)
- `idx_tasks_user_completed` on (user_id, completed)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=500, nullable=False)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- title: 1-500 characters, non-empty after trim
- user_id: must reference existing user
- completed: boolean only

**State Transitions**:
```
[Created] → completed=false
    │
    ▼
[Completed] → completed=true
    │
    ▼
[Deleted] → row removed
```

---

### Conversation

Chat session container for a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique identifier |
| user_id | UUID | FK → users.id, NOT NULL | Conversation owner |
| created_at | TIMESTAMP | DEFAULT NOW() | Session start time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last activity |

**Indexes**:
- `idx_conversations_user_id` on (user_id)

**SQLModel Definition**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Business Rules**:
- One active conversation per user (simplified for MVP)
- Conversation created on first chat message
- updated_at refreshed on each new message

---

### Message

Individual chat messages within a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique identifier |
| conversation_id | UUID | FK → conversations.id, NOT NULL | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender |
| content | TEXT | NOT NULL | Message text |
| created_at | TIMESTAMP | DEFAULT NOW() | Message timestamp |

**Indexes**:
- `idx_messages_conversation_id` on (conversation_id)
- `idx_messages_conversation_created` on (conversation_id, created_at)

**SQLModel Definition**:
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- role: must be 'user' or 'assistant'
- content: non-empty, max 10000 characters

---

## Database Migrations

### Migration 001: Initial Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tasks
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to conversations
CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Query Patterns

### Get User Tasks
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
ORDER BY created_at DESC;
```

### Get Conversation History
```sql
SELECT m.* FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE c.user_id = :user_id
ORDER BY m.created_at ASC;
```

### Get or Create Conversation
```sql
INSERT INTO conversations (user_id)
SELECT :user_id
WHERE NOT EXISTS (
    SELECT 1 FROM conversations WHERE user_id = :user_id
)
RETURNING *;
```
