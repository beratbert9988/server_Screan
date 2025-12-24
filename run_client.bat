@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please create one as .venv or ensure python is in path.
)
set PYTHONPATH=%PYTHONPATH%;.
python -m client.main
pause
