# Frontend Development Guidelines

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Auth**: Better Auth
- **UI**: React with Tailwind CSS
- **AI Integration**: Vercel AI SDK

## Architecture Rules

### Clear Separation (Constitution Principle VIII)
- Frontend in `/frontend` directory
- All API calls go to FastAPI backend
- No direct database access from frontend

### Authentication (Constitution Principle X)
- Better Auth handles signup/signin
- JWT tokens stored and sent with API requests
- Shared secret with backend (BETTER_AUTH_SECRET)

## File Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/auth/   # Better Auth route handler
│   │   ├── chat/       # Chat interface (protected)
│   │   ├── signin/     # Sign in page
│   │   └── signup/     # Sign up page
│   ├── components/     # React components
│   │   ├── Chat.tsx
│   │   ├── MessageList.tsx
│   │   └── MessageInput.tsx
│   └── lib/
│       ├── auth.ts     # Better Auth config
│       └── api.ts      # API client
└── package.json
```

## Code Standards

- Use TypeScript for all files
- Components use "use client" when needed
- Protected routes check auth state
- Display user-friendly error messages
- Handle loading states appropriately

## API Client Pattern

```typescript
// All API calls include JWT token
const response = await fetch(`${API_URL}/api/${userId}/chat`, {
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ message }),
});
```
