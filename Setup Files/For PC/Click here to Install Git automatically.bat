@echo off
title Setting up this PC for Claude Code
echo.
echo ================================================
echo   Setting up this PC for Claude Code
echo ================================================
echo.

where git >nul 2>nul
if %errorlevel%==0 (
    echo Git is already installed:
    git --version
    goto :done
)

where winget >nul 2>nul
if not %errorlevel%==0 (
    echo Windows Package Manager ^(winget^) was not found on this PC.
    echo That usually means Windows itself needs updating.
    echo.
    echo Please install Git by hand instead:
    echo   1. Go to https://git-scm.com/install/windows
    echo   2. Download and run the installer, clicking Next through the defaults.
    echo.
    goto :end
)

echo Installing Git now. This can take a minute.
echo If Windows asks "Do you want to allow this app to make changes?" click Yes.
echo.
winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements

where git >nul 2>nul
if %errorlevel%==0 (
    goto :done
) else (
    echo.
    echo Git was installed, but this window can't see it yet.
    echo Close this window, open a NEW Command Prompt, and run: git --version
    goto :end
)

:done
echo.
echo ================================================
echo   All done! You can close this window now
echo   and go back to setting up Claude.
echo ================================================
echo.

:end
pause
