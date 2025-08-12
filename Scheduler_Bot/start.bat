@echo off
echo Starting Smart Play Bot Scheduler...

REM Check if virtual environment exists
if not exist "..\Smart_Play_Bot\venv" (
    echo Virtual environment not found in ..\Smart_Play_Bot\venv
    echo Please create virtual environment first
    pause
    exit /b 1
)

REM Activate virtual environment
call ..\Smart_Play_Bot\venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start scheduler
echo Launching scheduler...
python scheduler.py

pause
