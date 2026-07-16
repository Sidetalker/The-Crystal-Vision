@echo off
title Lumina — CrystalCore local companion
cd /d "%~dp0"

echo.
echo  CrystalCore edge node — Lumina
echo  Project: %CD%
echo.

where ollama >nul 2>&1
if errorlevel 1 (
  echo  [FAIL] Ollama not found on PATH. Install from https://ollama.com
  pause
  exit /b 1
)

set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"

echo  Starting... (first reply can take up to a minute)
echo.
"%PY%" clementine.py
echo.
echo  Lumina stopped.
pause
