@echo off
echo ========================================
echo President University Chatbot
echo 2 AI Models: Llama 3.2 + Gemini 2.5
echo ========================================
echo.

echo [1/3] Starting Python Backend (FastAPI - Port 8000)...
start "Python Backend" cmd /k "cd /d %~dp0 && call nlp_env\Scripts\activate && python -m uvicorn main_backend:app --reload --port 8000"
timeout /t 3 >nul

echo [2/3] Starting Node.js Backend (Port 5000)...
start "Node Backend" cmd /k "cd /d %~dp0\backend && npm start"
timeout /t 3 >nul

echo [3/3] Starting Frontend (Port 5173)...
start "Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"
timeout /t 2 >nul

echo.
echo ========================================
echo ✅ All services started!
echo ========================================
echo.
echo 🐍 Python Backend:   http://localhost:8000
echo 🟢 Node.js Backend:  http://localhost:5000
echo 🌐 Frontend:         http://localhost:5173
echo.
echo Available Models:
echo   🦙 Llama 3.2 (Local Ollama)
echo   ✨ Gemini 2.5 Flash (Google Cloud)
echo.
echo ⚠️  Make sure Ollama is running for Llama model!
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping all services...
taskkill /FI "WindowTitle eq Python Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Node Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend*" /T /F >nul 2>&1

echo ✅ All services stopped.
pause
