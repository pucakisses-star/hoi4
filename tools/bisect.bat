@echo off
setlocal enabledelayedexpansion
title DSA 1886 - crash bisector

REM Builds the mod one layer at a time so a crash can be localised in two or
REM three launches instead of guessed at. Each layer is a mod that loads on its
REM own. Double-click, answer one question, launch, repeat.

set "SRC=%~dp0..\MOD"
if not exist "%SRC%\descriptor.mod" (
  echo Could not find the MOD folder next to this script.
  echo Expected: %SRC%
  pause & exit /b 1
)
set "MODDIR=%USERPROFILE%\Documents\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" set "MODDIR=%USERPROFILE%\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" set "MODDIR=%USERPROFILE%\OneDrive\Dokumenter\Paradox Interactive\Hearts of Iron IV\mod"
if not exist "%MODDIR%" (
  echo Could not find your Hearts of Iron IV mod folder.
  pause & exit /b 1
)

echo.
echo   Layer   Contains                                        Tests
echo   -----   ---------------------------------------------   -----------------------
echo     0     descriptor only                                 does the mod load at all
echo     1     + country tags, country files, colours          the tag and colour layer
echo     2     + localisation                                  text keys
echo     3     + history/states  ^(857 states^)                  the map
echo     4     + history/countries, history/units              governments and armies
echo     5     + bookmark            ^(= the complete mod^)      the 1886 start
echo.
echo   Start at 1. If it loads try 3, then 5. Two or three launches finds it.
echo.
set "L="
set /p "L=Build which layer (0-5)? "
if "%L%"=="" goto :bad
for %%v in (0 1 2 3 4 5) do if "%L%"=="%%v" goto :ok
:bad
echo Enter a number from 0 to 5.
pause & exit /b 1
:ok

set "DEST=%MODDIR%\dsa-bisect"
echo Clearing %DEST% ...
if exist "%DEST%" rmdir /s /q "%DEST%"
mkdir "%DEST%" 2>nul
set "RC=/NJH /NJS /NDL /NC /NS /NP /R:2 /W:1"

robocopy "%SRC%" "%DEST%" descriptor.mod thumbnail.png %RC% >nul
if %L% GEQ 1 robocopy "%SRC%\common\country_tags" "%DEST%\common\country_tags" /E %RC% >nul
if %L% GEQ 1 robocopy "%SRC%\common\countries"   "%DEST%\common\countries"   /E %RC% >nul
if %L% GEQ 2 robocopy "%SRC%\localisation"       "%DEST%\localisation"       /E %RC% >nul
if %L% GEQ 3 robocopy "%SRC%\history\states"     "%DEST%\history\states"     /E %RC% >nul
if %L% GEQ 4 robocopy "%SRC%\history\countries"  "%DEST%\history\countries"  /E %RC% >nul
if %L% GEQ 4 robocopy "%SRC%\history\units"      "%DEST%\history\units"      /E %RC% >nul
if %L% GEQ 5 robocopy "%SRC%\common\bookmarks"   "%DEST%\common\bookmarks"   /E %RC% >nul

REM replace_path is only declared for a directory once that directory is
REM actually present. Declaring it for a directory the layer has not copied
REM would blank vanilla's without supplying a replacement, which crashes for a
REM reason that has nothing to do with the layer being tested.
set "FWD=%DEST:\=/%"
set "NAME=DSA bisect - layer %L%"
> "%MODDIR%\dsa-bisect.mod" echo version="0.4"
>>"%MODDIR%\dsa-bisect.mod" echo name="%NAME%"
>>"%MODDIR%\dsa-bisect.mod" echo supported_version="1.19.*"
if %L% GEQ 3 >>"%MODDIR%\dsa-bisect.mod" echo replace_path="history/states"
if %L% GEQ 4 >>"%MODDIR%\dsa-bisect.mod" echo replace_path="history/countries"
if %L% GEQ 4 >>"%MODDIR%\dsa-bisect.mod" echo replace_path="history/units"
if %L% GEQ 5 >>"%MODDIR%\dsa-bisect.mod" echo replace_path="common/bookmarks"
>>"%MODDIR%\dsa-bisect.mod" echo path="%FWD%"

copy /y "%MODDIR%\dsa-bisect.mod" "%DEST%\descriptor.mod" >nul
echo.
echo   Built layer %L%.
echo   Enable "%NAME%" in the launcher, every OTHER mod unchecked, then Play.
echo.
echo   Reached the menu?  Run again with a HIGHER number.
echo   Crashed?           Run again with a LOWER number.
echo.
echo   Then tell me the highest layer that loaded and the lowest that crashed.
echo.
pause
