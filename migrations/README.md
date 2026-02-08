# Database Migrations

This directory contains SQL migration files for the Todo AI Chatbot system.

## Prerequisites

- Neon PostgreSQL database
- Database URL configured in `.env`

## Running Migrations

### Option 1: Direct SQL (Recommended for initial setup)

```bash
# Connect to your Neon database and run:
psql $DATABASE_URL -f migrations/001_initial_schema.sql
```

### Option 2: Using Neon Console

1. Open your Neon project dashboard
2. Go to SQL Editor
3. Copy and paste the migration file contents
4. Execute

## Migration Files

| File | Description |
|------|-------------|
| 001_initial_schema.sql | Creates tasks, conversations, messages tables |

## Rollback

To rollback migrations, run the corresponding down migration or drop tables:

```sql
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS tasks;
```

**Note**: The `users` table is managed by Better Auth. Do not modify it directly.
