# MCP Tool Contracts

**Feature**: 1-todo-ai-chatbot
**Protocol**: Model Context Protocol (MCP)
**Transport**: stdio

---

## Overview

The MCP server exposes exactly 5 tools as defined in the constitution. Each tool is stateless and persists all effects to the PostgreSQL database.

---

## Tool Definitions

### 1. add_task

Create a new task for a user.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the user creating the task"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "The task title/description"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "completed": { "type": "boolean" },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example**:
```json
// Input
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries"
}

// Output
{
  "success": true,
  "task": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Buy groceries",
    "completed": false,
    "created_at": "2026-02-06T10:30:00Z"
  },
  "message": "Task 'Buy groceries' created successfully"
}
```

---

### 2. list_tasks

Retrieve all tasks for a user.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the user"
    },
    "include_completed": {
      "type": "boolean",
      "default": true,
      "description": "Whether to include completed tasks"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "format": "uuid" },
          "title": { "type": "string" },
          "completed": { "type": "boolean" },
          "created_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "count": { "type": "integer" },
    "message": { "type": "string" }
  }
}
```

**Example**:
```json
// Input
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}

// Output
{
  "success": true,
  "tasks": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Buy groceries",
      "completed": false,
      "created_at": "2026-02-06T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "title": "Call mom",
      "completed": true,
      "created_at": "2026-02-05T09:00:00Z"
    }
  ],
  "count": 2,
  "message": "Found 2 tasks"
}
```

---

### 3. complete_task

Mark a task as completed.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "completed": { "type": "boolean" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example**:
```json
// Input
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "660e8400-e29b-41d4-a716-446655440001"
}

// Output (success)
{
  "success": true,
  "task": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Buy groceries",
    "completed": true
  },
  "message": "Task 'Buy groceries' marked as complete"
}

// Output (not found)
{
  "success": false,
  "task": null,
  "message": "Task not found"
}
```

---

### 4. delete_task

Remove a task permanently.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "deleted_task_id": { "type": "string", "format": "uuid" },
    "message": { "type": "string" }
  }
}
```

**Example**:
```json
// Input
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "660e8400-e29b-41d4-a716-446655440001"
}

// Output (success)
{
  "success": true,
  "deleted_task_id": "660e8400-e29b-41d4-a716-446655440001",
  "message": "Task deleted successfully"
}

// Output (not found)
{
  "success": false,
  "deleted_task_id": null,
  "message": "Task not found"
}
```

---

### 5. update_task

Modify an existing task's title.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the user"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "The new task title"
    }
  },
  "required": ["user_id", "task_id", "title"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "completed": { "type": "boolean" },
        "updated_at": { "type": "string", "format": "date-time" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example**:
```json
// Input
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "Buy organic groceries"
}

// Output (success)
{
  "success": true,
  "task": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Buy organic groceries",
    "completed": false,
    "updated_at": "2026-02-06T11:00:00Z"
  },
  "message": "Task updated to 'Buy organic groceries'"
}
```

---

## Error Handling

All tools return structured errors:

```json
{
  "success": false,
  "task": null,
  "message": "Human-readable error description"
}
```

**Error Scenarios**:
- Task not found: `"Task not found"`
- User mismatch: `"You don't have permission to modify this task"`
- Validation error: `"Task title cannot be empty"`
- Database error: `"Unable to complete request. Please try again."`

---

## Implementation Notes

1. **User Isolation**: All tools MUST verify user_id matches the task owner
2. **Stateless**: No in-memory state; every call queries/updates database
3. **Idempotent**: `complete_task` on already-completed task returns success
4. **Async**: All database operations use async/await
5. **Logging**: All tool calls logged to stderr (not stdout for stdio transport)
