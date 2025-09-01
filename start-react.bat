@echo off
echo ========================================
echo    Sundai AI Explorer - Startup Fix
echo ========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js not found!
    echo Please install Node.js from: https://nodejs.org/
    echo Download the LTS version and restart your computer
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: npm not found!
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✅ npm found:
npm --version
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ ERROR: package.json not found!
    echo Make sure you're in the project directory
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo ✅ Found package.json
echo.

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ ERROR: Failed to install dependencies
        echo Try running: npm cache clean --force
        echo Then run this script again
        echo.
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed!
    echo.
)

REM Kill any process using port 3000
echo Checking if port 3000 is available...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo Found process using port 3000, killing it...
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo 🚀 Starting development server...
echo 📍 The app will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm run dev

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Failed to start server
    echo.
    echo Try these fixes:
    echo 1. Close any other terminals/command prompts
    echo 2. Restart your computer
    echo 3. Run: npm cache clean --force
    echo 4. Delete node_modules folder and run: npm install
    echo.
    pause
)
