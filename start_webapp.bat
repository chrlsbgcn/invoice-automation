@echo off
echo ============================================================
echo 🚀 Invoice Data Extractor Web Application
echo ============================================================
echo.
echo Starting the web server...
echo 📱 Open your browser and go to: http://localhost:5000
echo 🔄 Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the web application
python run_webapp.py

pause 