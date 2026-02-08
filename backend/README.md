---
title: Todo AI Backend
emoji: 🤖
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# Todo AI Backend

FastAPI backend with Google Gemini AI for intelligent task management.

## Features

- 🔐 JWT Authentication
- 🤖 AI-powered task management with Google Gemini
- 💾 SQLite database (for development)
- 🔒 Secure password hashing
- 🚀 RESTful API

## API Endpoints

- POST `/api/v1/auth/signup` - Create new user
- POST `/api/v1/auth/signin` - Sign in user
- POST `/api/{user_id}/chat` - Chat with AI assistant
- GET `/api/{user_id}/conversations` - Get chat history
- GET `/health` - Health check

## Environment Variables

Required:
- `GEMINI_API_KEY` - Google Gemini API key
- `BETTER_AUTH_SECRET` - JWT signing secret
- `DATABASE_URL` - SQLite database path

## Local Development

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Deployment

This app is configured for Hugging Face Spaces deployment using Docker.
