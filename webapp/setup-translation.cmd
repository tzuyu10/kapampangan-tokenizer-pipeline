@echo off
setlocal
for %%I in ("%~dp0..") do set "PIPELINE_ROOT=%%~fI"
cd /d "%PIPELINE_ROOT%"
set "PIP_CACHE_DIR=%PIPELINE_ROOT%\.cache\pip"
set "HF_HOME=%PIPELINE_ROOT%\.cache\huggingface"
set "PYTHONNOUSERSITE=1"
set "PYTHONPATH="
if exist "%PIPELINE_ROOT%\.venv-translation\Scripts\python.exe" goto install
py -3.12 -c "import sys" >nul 2>&1
if errorlevel 1 goto python311
py -3.12 -m venv "%PIPELINE_ROOT%\.venv-translation"
if errorlevel 1 goto failed
goto install
:python311
py -3.11 -c "import sys" >nul 2>&1
if errorlevel 1 (
  echo Install Python 3.12 or 3.11 with the Windows Python launcher, then run this setup again.
  goto failed
)
py -3.11 -m venv "%PIPELINE_ROOT%\.venv-translation"
if errorlevel 1 goto failed
:install
"%PIPELINE_ROOT%\.venv-translation\Scripts\python.exe" -m pip install -r "%PIPELINE_ROOT%\webapp\backend\requirements-translation.txt"
if errorlevel 1 goto failed
echo Setup complete. Run webapp\start-translation-backend.cmd.
exit /b 0
:failed
echo Setup failed. Resolve the error above before starting the backend.
pause
exit /b 1
