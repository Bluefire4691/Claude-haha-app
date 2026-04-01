@echo off
REM ============================================================
REM  build.bat  –  Build haha.exe
REM  Run this once on a Windows machine with Python 3.9+ installed.
REM ============================================================

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (echo FAILED: pip install & pause & exit /b 1)

echo.
echo [2/4] Generating haha.gif...
python create_gif.py
if errorlevel 1 (echo FAILED: create_gif.py & pause & exit /b 1)

echo.
echo [3/4] Building haha.exe with PyInstaller...
pyinstaller ^
    --onefile ^
    --windowed ^
    --add-data "haha.gif;." ^
    --hidden-import pyttsx3.drivers ^
    --hidden-import pyttsx3.drivers.sapi5 ^
    --version-file version_info.txt ^
    --name professionalworkprogram ^
    haha.py
if errorlevel 1 (echo FAILED: pyinstaller & pause & exit /b 1)

echo.
echo [4/4] Done!
echo.
echo   Executable:  dist\haha.exe
echo.
echo   Drop haha.exe wherever you like and run it.
echo   It will sit silently in Task Manager as "haha.exe" and pop
echo   up a Nelson Muntz "HA HA!" every 3-15 minutes at random.
echo   Kill it any time via Task Manager -^> End Task on haha.exe
echo.
pause
