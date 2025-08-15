@echo off
chcp 65001 >nul
title Python Virtual Environment Manager for Custom Web Bot

:menu
cls
echo ========================================
echo    Python 虚拟环境管理器
echo    Custom Web Bot 项目
echo ========================================
echo.
echo 请选择要执行的操作:
echo.
echo [1] 安装所有虚拟环境 (推荐首次使用)
echo [2] 激活根目录虚拟环境
echo [3] 激活 Smart_Play_Bot 虚拟环境
echo [4] 激活 Scheduler_Bot 虚拟环境
echo [5] 清理所有虚拟环境
echo [6] 退出
echo.
echo ========================================
set /p choice=请输入选项 (1-6): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto activate_root
if "%choice%"=="3" goto activate_smartplay
if "%choice%"=="4" goto activate_scheduler
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto exit
goto invalid

:install
cls
echo ========================================
echo 正在安装所有虚拟环境...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未安装Python或Python不在PATH中
    echo 请安装Python 3.8+并重试
    echo.
    pause
    goto menu
)

echo 检查根目录虚拟环境...
if exist "venv" (
    echo 根目录虚拟环境已存在
    echo 是否重新创建? (y/n)
    set /p recreate=
    if /i "%recreate%"=="y" (
        echo 正在删除现有虚拟环境...
        rmdir /s /q "venv"
        echo 正在创建根目录虚拟环境...
        python -m venv venv
        echo 正在安装根目录依赖...
        call venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        echo 根目录虚拟环境设置完成!
    ) else (
        echo 跳过根目录虚拟环境创建
    )
) else (
    echo 正在创建根目录虚拟环境...
    python -m venv venv
    echo 正在安装根目录依赖...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo 根目录虚拟环境设置完成!
)

echo.
echo 检查 Smart_Play_Bot 虚拟环境...
if exist "Smart_Play_Bot\venv" (
    echo Smart_Play_Bot 虚拟环境已存在
    echo 是否重新创建? (y/n)
    set /p recreate=
    if /i "%recreate%"=="y" (
        echo 正在删除现有虚拟环境...
        rmdir /s /q "Smart_Play_Bot\venv"
        echo 正在创建 Smart_Play_Bot 虚拟环境...
        cd Smart_Play_Bot
        python -m venv venv
        echo 正在安装 Smart_Play_Bot 依赖...
        call venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        cd ..
        echo Smart_Play_Bot 虚拟环境设置完成!
    ) else (
        echo 跳过 Smart_Play_Bot 虚拟环境创建
    )
) else (
    echo 正在创建 Smart_Play_Bot 虚拟环境...
    cd Smart_Play_Bot
    python -m venv venv
    echo 正在安装 Smart_Play_Bot 依赖...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo Smart_Play_Bot 虚拟环境设置完成!
)

echo.
echo 检查 Scheduler_Bot 虚拟环境...
if exist "Scheduler_Bot\venv" (
    echo Scheduler_Bot 虚拟环境已存在
    echo 是否重新创建? (y/n)
    set /p recreate=
    if /i "%recreate%"=="y" (
        echo 正在删除现有虚拟环境...
        rmdir /s /q "Scheduler_Bot\venv"
        echo 正在创建 Scheduler_Bot 虚拟环境...
        cd Scheduler_Bot
        python -m venv venv
        echo 正在安装 Scheduler_Bot 依赖...
        call venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        cd ..
        echo Scheduler_Bot 虚拟环境设置完成!
    ) else (
        echo 跳过 Scheduler_Bot 虚拟环境创建
    )
) else (
    echo 正在创建 Scheduler_Bot 虚拟环境...
    cd Scheduler_Bot
    python -m venv venv
    echo 正在安装 Scheduler_Bot 依赖...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo Scheduler_Bot 虚拟环境设置完成!
)

echo.
echo ========================================
echo 所有虚拟环境设置完成!
echo ========================================
echo.
echo 现在您可以使用以下选项激活虚拟环境:
echo - 选项 2: 激活根目录虚拟环境
echo - 选项 3: 激活 Smart_Play_Bot 虚拟环境
echo - 选项 4: 激活 Scheduler_Bot 虚拟环境
echo.
pause
goto menu

:activate_root
cls
echo ========================================
echo 正在激活根目录虚拟环境...
echo ========================================
echo.

if not exist "venv" (
    echo 错误: 根目录虚拟环境不存在
    echo 请先选择选项 1 安装虚拟环境
    echo.
    pause
    goto menu
)

echo 激活根目录虚拟环境...
call venv\Scripts\activate.bat
echo.
echo 虚拟环境激活成功!
echo 当前Python位置: %VIRTUAL_ENV%\Scripts\python.exe
echo.
echo 要退出虚拟环境，请输入: deactivate
echo 要返回主菜单，请输入: exit
echo.
cmd /k

:activate_smartplay
cls
echo ========================================
echo 正在激活 Smart_Play_Bot 虚拟环境...
echo ========================================
echo.

if not exist "Smart_Play_Bot\venv" (
    echo 错误: Smart_Play_Bot 虚拟环境不存在
    echo 请先选择选项 1 安装虚拟环境
    echo.
    pause
    goto menu
)

echo 激活 Smart_Play_Bot 虚拟环境...
cd Smart_Play_Bot
call venv\Scripts\activate.bat
echo.
echo 虚拟环境激活成功!
echo 当前Python位置: %VIRTUAL_ENV%\Scripts\python.exe
echo 当前工作目录: %CD%
echo.
echo 要退出虚拟环境，请输入: deactivate
echo 要返回主菜单，请输入: exit
echo.
cmd /k

:activate_scheduler
cls
echo ========================================
echo 正在激活 Scheduler_Bot 虚拟环境...
echo ========================================
echo.

if not exist "Scheduler_Bot\venv" (
    echo 错误: Scheduler_Bot 虚拟环境不存在
    echo 请先选择选项 1 安装虚拟环境
    echo.
    pause
    goto menu
)

echo 激活 Scheduler_Bot 虚拟环境...
cd Scheduler_Bot
call venv\Scripts\activate.bat
echo.
echo 虚拟环境激活成功!
echo 当前Python位置: %VIRTUAL_ENV%\Scripts\python.exe
echo 当前工作目录: %CD%
echo.
echo 要退出虚拟环境，请输入: deactivate
echo 要返回主菜单，请输入: exit
echo.
cmd /k

:cleanup
cls
echo ========================================
echo 虚拟环境清理脚本
echo ========================================
echo.
echo 此脚本将删除所有虚拟环境。
echo 警告: 此操作无法撤销!
echo.
echo 是否继续? (y/n)
set /p confirm=
if /i not "%confirm%"=="y" goto menu

echo.
echo 正在删除根目录虚拟环境...
if exist "venv" (
    rmdir /s /q "venv"
    echo 根目录虚拟环境已删除。
) else (
    echo 根目录虚拟环境不存在。
)

echo.
echo 正在删除 Smart_Play_Bot 虚拟环境...
if exist "Smart_Play_Bot\venv" (
    rmdir /s /q "Smart_Play_Bot\venv"
    echo Smart_Play_Bot 虚拟环境已删除。
) else (
    echo Smart_Play_Bot 虚拟环境不存在。
)

echo.
echo 正在删除 Scheduler_Bot 虚拟环境...
if exist "Scheduler_Bot\venv" (
    rmdir /s /q "Scheduler_Bot\venv"
    echo Scheduler_Bot 虚拟环境已删除。
) else (
    echo Scheduler_Bot 虚拟环境不存在。
)

echo.
echo ========================================
echo 清理完成!
echo ========================================
echo.
echo 要重新安装虚拟环境，请选择选项 1
echo.
pause
goto menu

:invalid
echo.
echo 无效选项，请重新选择...
timeout /t 2 >nul
goto menu

:exit
cls
echo ========================================
echo 感谢使用 Python 虚拟环境管理器!
echo ========================================
echo.
echo 再见!
timeout /t 3 >nul
exit
