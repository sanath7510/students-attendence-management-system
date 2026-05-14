@echo off
title Hybrid AI Attendance System EXE Builder

:: Move to current project directory
cd /d "%~dp0"

echo ==========================================
echo   HYBRID AI ATTENDANCE SYSTEM BUILD
echo ==========================================
echo.

:: Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo ==========================================
echo Building EXE File...
echo ==========================================
echo.

pyinstaller ^
--noconfirm ^
--onedir ^
--windowed ^
--name "Hybrid_AI_Attendance_System" ^
--collect-all tensorflow ^
--collect-all keras ^
--collect-all cv2 ^
--hidden-import=PIL._tkinter_finder ^
--hidden-import=sklearn ^
--hidden-import=pandas ^
--hidden-import=numpy ^
--hidden-import=tkinter ^
--add-data "images;images" ^
--add-data "models;models" ^
--add-data "database;database" ^
MAIN_UI.py

echo.
echo ==========================================
echo EXE GENERATED SUCCESSFULLY
echo ==========================================
echo.
echo Open:
echo dist\Hybrid_AI_Attendance_System
echo.
echo Run:
echo Hybrid_AI_Attendance_System.exe
echo.

pause