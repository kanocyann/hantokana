@echo off
setlocal EnableExtensions
pushd "%~dp0"

set "VENV_DIR=%~dp0.venv_build"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
if not defined ISCC_EXE set "ISCC_EXE=D:\software\work\Inno Setup 6\ISCC.exe"

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist output rmdir /s /q output

if not exist "%VENV_PY%" (
    echo Creating build virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 goto :fail
)

echo Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 goto :fail
"%VENV_PY%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :fail

echo Building application...
"%VENV_PY%" -m PyInstaller hantokana.spec
if errorlevel 1 goto :fail

if exist "%ISCC_EXE%" (
    echo Building installer...
    "%ISCC_EXE%" installer.iss
    if errorlevel 1 goto :fail
) else (
    echo Inno Setup compiler not found, skipping installer.
    echo Set ISCC_EXE to the path of ISCC.exe to enable installer generation.
)

echo Done!
popd
pause
exit /b 0

:fail
echo Build failed.
popd
pause
exit /b 1
