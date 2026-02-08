@echo off
echo Installing Node.js dependencies...
cd /d "C:\Users\Admin\phase-III\frontend"

npm install

echo Starting Next.js frontend server...
echo Frontend will be available at: http://localhost:3000
npm run dev