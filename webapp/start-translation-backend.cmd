@echo off
setlocal
for %%I in ("%~dp0..") do set "PIPELINE_ROOT=%%~fI"
cd /d "%PIPELINE_ROOT%"
set "HF_HOME=%PIPELINE_ROOT%\.cache\huggingface"
set "KAPAMPANGAN_MODEL_DIR=%PIPELINE_ROOT%\nllb\checkpoints"
set "PYTHONNOUSERSITE=1"
set "PYTHONPATH="
if not exist "%PIPELINE_ROOT%\.venv-translation\Scripts\python.exe" (
  echo Translation environment missing. Run webapp\setup-translation.cmd first.
  pause
  exit /b 1
)
"%PIPELINE_ROOT%\.venv-translation\Scripts\python.exe" "%PIPELINE_ROOT%\webapp\run-backend.py"
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%
