# Deploying to Hugging Face Spaces

## 🚀 Quick Deployment Steps

### 1. Prepare Your Local Repository

Your backend is ready! All files are configured for Hugging Face deployment.

### 2. Go to Your Hugging Face Space

Visit: https://huggingface.co/spaces/SyedaMehakShah/todo_ai_backend

### 3. Set Up Environment Variables (IMPORTANT!)

In your Hugging Face Space settings, add these secrets:

```
GEMINI_API_KEY=AIzaSyAyEOt_BNfdr-SeSuNUZO5zKWoWuAbzxBc
BETTER_AUTH_SECRET=Nog3Yh2Bkv69AeIGJVnnfKXsDCI2YUEtZEEm-1cJOO1f29rsRPFJSGZMYQ_K8w0xZqjZ6sl1NgkhXoLhykqq7Q
DATABASE_URL=sqlite:///./todo_app.db
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://your-frontend-url.com,http://localhost:3000
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7
LOG_LEVEL=INFO
LOG_FORMAT=text
```

### 4. Upload Backend Files

You need to upload these files to your Hugging Face Space:

#### Required Files:
- ✅ `Dockerfile` (already exists)
- ✅ `requirements.txt` (updated with google-generativeai)
- ✅ `README.md` (created)
- ✅ `.dockerignore` (created)

#### Backend Code (entire `backend/` directory):
```
backend/
├── src/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   ├── chat.py
│   │   └── middleware/
│   │       └── jwt_auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_gemini.py (NEW - Gemini integration)
│   │   ├── auth_service.py
│   │   ├── conversation.py
│   │   └── database.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── tools.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .dockerignore
```

### 5. Upload Methods

#### Option A: Git Push (Recommended)

```bash
# In your backend directory
cd backend

# Initialize git if not already done
git init

# Add Hugging Face Space as remote
git remote add hf https://huggingface.co/spaces/SyedaMehakShah/todo_ai_backend

# Add all files
git add .

# Commit
git commit -m "Deploy FastAPI backend with Gemini AI"

# Push to Hugging Face
git push hf main
```

#### Option B: Web UI Upload

1. Go to https://huggingface.co/spaces/SyedaMehakShah/todo_ai_backend/tree/main
2. Click "Add file" → "Upload files"
3. Drag and drop all backend files
4. Commit the changes

### 6. Configure Space Settings

In your Space settings (⚙️ icon):

1. **SDK:** Docker
2. **Hardware:** CPU Basic (free tier)
3. **Visibility:** Public or Private (your choice)
4. **Sleep time:** Can be set to prevent idle timeout

### 7. Wait for Build

- Hugging Face will automatically build your Docker image
- This takes 5-10 minutes
- Watch the build logs for any errors

### 8. Verify Deployment

Once deployed, your API will be available at:
```
https://syedamehakshah-todo-ai-backend.hf.space
```

Test endpoints:
- GET `/health` - Should return `{"status":"healthy"}`
- POST `/api/v1/auth/signup` - Create user
- GET `/docs` - Interactive API documentation

### 9. Update Frontend

After deployment, update your frontend `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://syedamehakshah-todo-ai-backend.hf.space
```

## 🔒 Security Checklist

Before deploying:

- ✅ Environment variables configured as Secrets
- ✅ CORS origins updated for production domain
- ✅ Debug mode disabled in production
- ✅ Database URL configured
- ✅ JWT secret is strong and unique
- ✅ API keys stored as secrets (not in code)

## 🐛 Troubleshooting

### Build Fails

Check:
1. All dependencies in `requirements.txt` are compatible
2. Python version is 3.11
3. Environment variables are set

### Runtime Errors

Check:
1. Logs in Hugging Face Space interface
2. Environment variables are correct
3. PORT is set correctly (Hugging Face uses 7860)

### Database Issues

For production, consider:
- Using Neon PostgreSQL instead of SQLite
- Update `DATABASE_URL` to PostgreSQL connection string
- Uncomment `asyncpg` in requirements if using PostgreSQL

## 📚 Useful Commands

```bash
# Test local build
docker build -t todo-backend .
docker run -p 8000:7860 --env-file .env todo-backend

# Check space status
git push hf main

# View logs
# Use Hugging Face web interface
```

## 🎉 Next Steps

After successful deployment:

1. Test all API endpoints
2. Update frontend to use new backend URL
3. Deploy frontend to Vercel/Netlify
4. Monitor logs for any issues
5. Set up database backups (if using PostgreSQL)
