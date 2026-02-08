#!/bin/bash

# Deployment script for Hugging Face Spaces
# Usage: ./deploy.sh

echo "=============================================="
echo "Deploying to Hugging Face Spaces"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Check if HF remote exists
if ! git remote get-url hf > /dev/null 2>&1; then
    echo "Adding Hugging Face remote..."
    git remote add hf https://huggingface.co/spaces/SyedaMehakShah/todo_ai_backend
    echo "✅ Remote added"
    echo ""
fi

echo "Staging files..."
git add .
echo "✅ Files staged"
echo ""

echo "Creating commit..."
git commit -m "Deploy FastAPI backend with Gemini AI integration"
echo "✅ Commit created"
echo ""

echo "Pushing to Hugging Face..."
echo "⚠️  You may be prompted for your Hugging Face credentials"
echo ""

git push hf main

echo ""
echo "=============================================="
echo "Deployment initiated!"
echo "=============================================="
echo ""
echo "Check deployment status at:"
echo "https://huggingface.co/spaces/SyedaMehakShah/todo_ai_backend"
echo ""
echo "Your API will be available at:"
echo "https://syedamehakshah-todo-ai-backend.hf.space"
echo ""
