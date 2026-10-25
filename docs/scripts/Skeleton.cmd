@echo off
SETLOCAL EnableExtensions DisableDelayedExpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python is not installed or not added to your PATH environment variable.
    echo Please install Python to run this script.
    pause
    exit /b
)

:: Run the Python script passing along the current directory context
python "%~dp0import_rom.py"

endlocal
