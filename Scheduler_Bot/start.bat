chcp 65001
@echo off
setlocal enabledelayedexpansion

REM 1. 读取 config.yml 中的 booking_month 和 booking_day
set "CONFIG_PATH=..\Smart_Play_Bot\config.yml"
set "MONTH="
set "DAY="

for /f "usebackq tokens=1,2 delims=: " %%A in (`findstr /R "^booking_month: ^booking_day:" "%CONFIG_PATH%"`) do (
    if "%%A"=="booking_month" set "MONTH=%%B"
    if "%%A"=="booking_day" set "DAY=%%B"
)

set "MONTH=!MONTH:'=!"
set "DAY=!DAY:'=!"

REM 计算当前年份
for /f %%i in ('powershell -Command "[datetime]::Now.Year"') do set YEAR=%%i

REM 计算星期几
for /f "delims=" %%i in ('powershell -Command "$d=Get-Date -Year %YEAR% -Month !MONTH! -Day !DAY!; $d.ToString('dddd', [System.Globalization.CultureInfo]::GetCultureInfo('zh-CN'))"') do set WEEKDAY=%%i

REM 2. 显示当前预约时间和星期几，询问是否调整
:ask_modify
cls
echo.
echo 當前預約時間：
echo   月份：!MONTH!
echo   日期：!DAY!
echo   星期：!WEEKDAY!
echo.
set /p MODIFY=是否要調整預約時間？(y/n): 
if /i "%MODIFY%"=="y" goto modify_time
if /i "%MODIFY%"=="n" goto run_scheduler
echo 請輸入 y 或 n
pause
goto ask_modify

:modify_time
set /p NEW_MONTH=請輸入新的 booking_month（數字）: 
set /p NEW_DAY=請輸入新的 booking_day（數字）: 
REM 重新计算星期几
for /f %%i in ('powershell -Command "$d=Get-Date -Year %YEAR% -Month %NEW_MONTH% -Day %NEW_DAY%; $d.ToString('dddd', [System.Globalization.CultureInfo]::GetCultureInfo('zh-CN'))"') do set NEW_WEEKDAY=%%i
echo.
echo 新預約時間：
echo   月份：%NEW_MONTH%
echo   日期：%NEW_DAY%
echo   星期：%NEW_WEEKDAY%
set /p CONFIRM=確認修改為以上預約時間？(y/n): 
if /i "%CONFIRM%"=="y" goto update_config
goto ask_modify

:update_config
REM 用 powershell 修改 config.yml
powershell -Command "(Get-Content '%CONFIG_PATH%') -replace 'booking_month:.*', 'booking_month: ''%NEW_MONTH%''' | Set-Content '%CONFIG_PATH%'"
powershell -Command "(Get-Content '%CONFIG_PATH%') -replace 'booking_day:.*', 'booking_day: ''%NEW_DAY%''' | Set-Content '%CONFIG_PATH%'"
set "MONTH=%NEW_MONTH%"
set "DAY=%NEW_DAY%"
set "WEEKDAY=%NEW_WEEKDAY%"
goto run_scheduler

:run_scheduler
REM 检查虚拟环境
if not exist "..\Smart_Play_Bot\venv" (
    echo Virtual environment not found in ..\Smart_Play_Bot\venv
    echo Please create virtual environment first
    pause
    exit /b 1
)
REM 激活虚拟环境
call ..\Smart_Play_Bot\venv\Scripts\activate.bat
REM 安装依赖
echo Installing requirements...
pip install -r requirements.txt
REM 启动 scheduler
echo Launching scheduler...
python scheduler.py
pause
