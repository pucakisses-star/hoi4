@echo off
setlocal enabledelayedexpansion
title DSA layered mod builder

REM ---------------------------------------------------------------------
REM  build-mod.bat -- assemble the mod one layer at a time.
REM
REM  Each layer is a mod that actually loads, so you can launch after every
REM  step. Whichever layer first fails to reach the main menu contains the
REM  cause. Double-click this file and answer one question.
REM
REM  Nothing here edits your existing mods. It builds a separate folder
REM  called dsa-test and writes its .mod descriptor for you.
REM ---------------------------------------------------------------------

set "SRC=%~dp0..\MOD"
if not exist "%SRC%\descriptor.mod" (
  echo Could not find the MOD folder next to this script.
  echo Expected: %SRC%
  echo Keep build-mod.bat inside the repo's tools\ folder.
  pause & exit /b 1
)

set "MODDIR=%USERPROFILE%\Documents\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" set "MODDIR=%USERPROFILE%\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" set "MODDIR=%USERPROFILE%\OneDrive\Dokumenter\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" (
  echo Could not find your Hearts of Iron IV mod folder.
  echo Looked under Documents and OneDrive^\Documents.
  echo Open the game launcher once to create it, then run this again.
  pause & exit /b 1
)

echo.
echo   Hearts of Iron IV mod folder:
echo     %MODDIR%
echo.
echo   Layer   Adds                                          Approx
echo   -----   -------------------------------------------   ------
echo     0     descriptor only  ^(baseline: does it load?^)      1 MB
echo     1     + localisation                                   6 MB
echo     2     + gfx, interface, portraits, sound, music      833 MB
echo     3     + map, history                                 113 MB
echo     4     + common ^(units, tech, characters, tags^)        55 MB
echo     5     + ideas, focus trees, decisions, bookmarks       9 MB
echo     6     + events            ^(= the complete mod^)         4 MB
echo.
echo   Start at 3. If it loads, try 5. If it crashes, try 1.
echo   Three launches narrows it to one layer.
echo.
set "LEVEL="
set /p "LEVEL=Build which layer (0-6)? "
if not defined LEVEL goto :bad
if "%LEVEL%"=="0" goto :ok
if "%LEVEL%"=="1" goto :ok
if "%LEVEL%"=="2" goto :ok
if "%LEVEL%"=="3" goto :ok
if "%LEVEL%"=="4" goto :ok
if "%LEVEL%"=="5" goto :ok
if "%LEVEL%"=="6" goto :ok
:bad
echo Please enter a number from 0 to 6.
pause & exit /b 1
:ok

set "DEST=%MODDIR%\dsa-test"
echo.
echo Clearing %DEST% ...
if exist "%DEST%" rmdir /s /q "%DEST%"
mkdir "%DEST%" 2>nul

set "RC=/NJH /NJS /NDL /NC /NS /NP /R:2 /W:1"
echo Copying layer 0 ...
robocopy "%SRC%" "%DEST%" descriptor.mod thumbnail.png %RC% >nul
if errorlevel 8 goto :copyfail

if %LEVEL% GEQ 1 (
  echo Copying localisation ...
  robocopy "%SRC%\localisation" "%DEST%\localisation" /E %RC% >nul
  if errorlevel 8 goto :copyfail
)
if %LEVEL% GEQ 2 (
  echo Copying art and audio ^(this is the slow one^) ...
  for %%D in (gfx interface portraits sound music) do (
    if exist "%SRC%\%%D" robocopy "%SRC%\%%D" "%DEST%\%%D" /E %RC% >nul
  )
)
if %LEVEL% GEQ 3 (
  echo Copying map and history ...
  robocopy "%SRC%\map" "%DEST%\map" /E /XF provinces.psd %RC% >nul
  robocopy "%SRC%\history" "%DEST%\history" /E %RC% >nul
)
if %LEVEL% GEQ 4 (
  echo Copying common ...
  robocopy "%SRC%\common" "%DEST%\common" /E /XD ideas national_focus decisions bookmarks %RC% >nul
)
if %LEVEL% GEQ 5 (
  echo Copying ideas, focus trees, decisions, bookmarks ...
  for %%D in (ideas national_focus decisions bookmarks) do (
    if exist "%SRC%\common\%%D" robocopy "%SRC%\common\%%D" "%DEST%\common\%%D" /E %RC% >nul
  )
)
if %LEVEL% GEQ 6 (
  echo Copying events ...
  robocopy "%SRC%\events" "%DEST%\events" /E %RC% >nul
)

REM ---- write both descriptors; path= needs forward slashes ----
set "FWD=%DEST:\=/%"
set "DESCNAME=DSA test - layer %LEVEL%"

> "%DEST%\descriptor.mod" echo version="1.3"
>>"%DEST%\descriptor.mod" echo name="%DESCNAME%"
>>"%DEST%\descriptor.mod" echo supported_version="1.19.*"
if %LEVEL% GEQ 4 >>"%DEST%\descriptor.mod" echo replace_path="common/on_actions"

> "%MODDIR%\dsa-test.mod" echo version="1.3"
>>"%MODDIR%\dsa-test.mod" echo name="%DESCNAME%"
>>"%MODDIR%\dsa-test.mod" echo supported_version="1.19.*"
if %LEVEL% GEQ 4 >>"%MODDIR%\dsa-test.mod" echo replace_path="common/on_actions"
>>"%MODDIR%\dsa-test.mod" echo path="%FWD%"

echo.
echo   Built layer %LEVEL%.
echo.
echo   Now open the Hearts of Iron IV launcher, go to Mods, and enable
echo     "%DESCNAME%"
echo   Make sure every OTHER mod is unchecked. Then Play.
echo.
echo   Reached the main menu?  Run this again with a HIGHER number.
echo   Crashed?                Run this again with a LOWER number.
echo.
pause
exit /b 0

:copyfail
echo.
echo Copy failed. Check you have disk space and that the game is closed.
pause & exit /b 1
