@echo off
REM Check if a ROM path was dragged-and-dropped or passed as an argument
if "%~1"=="" (
    echo Please drag and drop a ROM file onto this script, or run: run_rom.cmd "path\to\rom.nes"
    pause
    exit /b
)

REM Run the Python script with the provided ROM file
python import_rom.py "%~1"

pause
