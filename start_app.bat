@echo off
echo 🚀 Starting Project Explorer Pro...
echo ==================================================
echo.
echo 📱 The app will open at: http://localhost:8512
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ==================================================
echo.

python -m streamlit run streamlit_app_production.py --server.port 8512

pause
