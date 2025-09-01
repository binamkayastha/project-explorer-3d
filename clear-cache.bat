@echo off
echo ========================================
echo    Cache Clear & Restart Script
echo ========================================
echo.

echo 🔄 Stopping development server...
taskkill /f /im node.exe >nul 2>&1

echo.
echo 🧹 Clearing cache and restarting...
echo.

REM Clear npm cache
npm cache clean --force

REM Remove dist folder if it exists
if exist "dist" (
    rmdir /s /q dist
    echo Removed dist folder
)

echo.
echo 🚀 Starting development server...
echo 📍 Open: http://localhost:3000
echo.
echo 💡 If you still see old content:
echo    1. Press Ctrl+Shift+R to hard refresh
echo    2. Or open in incognito/private mode
echo.
echo ========================================

npm run dev

