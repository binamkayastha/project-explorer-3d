@echo off
echo ========================================
echo    Localhost Fix Script
echo ========================================
echo.

echo 🔧 Fixing localhost issues...
echo.

REM Kill any processes using port 3000
echo 1. Killing processes on port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo   Killing process PID: %%a
    taskkill /f /pid %%a >nul 2>&1
)

REM Clear npm cache
echo 2. Clearing npm cache...
npm cache clean --force

REM Remove node_modules and package-lock
echo 3. Removing old dependencies...
if exist "node_modules" (
    rmdir /s /q node_modules
    echo   Removed node_modules
)
if exist "package-lock.json" (
    del package-lock.json
    echo   Removed package-lock.json
)

REM Reinstall dependencies
echo 4. Reinstalling dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Try running as Administrator
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.

echo 🚀 Starting server...
echo 📍 Open: http://localhost:3000
echo.
echo Press Ctrl+C to stop
echo ========================================

npm run dev

