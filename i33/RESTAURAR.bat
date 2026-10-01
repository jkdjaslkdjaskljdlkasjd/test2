@echo off
setlocal EnableExtensions
title Sonny 2 - volver a la version anterior

rem ---------------------------------------------------------------------------
rem  Vuelve a poner el ultimo respaldo de _respaldos_mod (el SONNY2.swf que habia
rem  antes de la ultima instalacion). El que esta ahora tambien se guarda.
rem ---------------------------------------------------------------------------
set "DESTINO_DEFECTO=C:\Program Files (x86)\Steam\steamapps\common\Sonny Legacy Collection\SonnyLegacy.app\Contents\Resources"

net session >nul 2>&1
if errorlevel 1 goto :elevar
goto :inicio

:elevar
echo Pidiendo permisos de administrador...
powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
exit /b

:inicio
set "DESTINO=%DESTINO_DEFECTO%"
if exist "%DESTINO%\SONNY2.swf" goto :destino_ok
echo Pega la ruta de la carpeta Resources del juego y pulsa Enter:
set /p "DESTINO=Ruta: "
set "DESTINO=%DESTINO:"=%"
if exist "%DESTINO%\SONNY2.swf" goto :destino_ok
echo [ERROR] En esa carpeta no hay ningun SONNY2.swf.
goto :fin_error

:destino_ok
set "RESPALDOS=%DESTINO%\_respaldos_mod"
set "ULTIMO="
for /f "delims=" %%F in ('dir /b /o-d "%RESPALDOS%\SONNY2_*.swf" 2^>nul') do if not defined ULTIMO set "ULTIMO=%%F"
if defined ULTIMO goto :hay_respaldo
echo [ERROR] No hay respaldos en _respaldos_mod.
goto :fin_error

:hay_respaldo
:esperar_juego
tasklist /FI "IMAGENAME eq Sonny Legacy Collection.exe" 2>nul | find /I "Sonny Legacy Collection.exe" >nul
if errorlevel 1 goto :juego_cerrado
echo El juego esta abierto. Cierralo y pulsa una tecla para seguir.
pause >nul
goto :esperar_juego

:juego_cerrado
echo Se va a restaurar: %ULTIMO%
for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "FECHA=%%T"
copy /Y "%DESTINO%\SONNY2.swf" "%RESPALDOS%\antes_de_restaurar_%FECHA%.swf.bak" >nul
copy /Y "%RESPALDOS%\%ULTIMO%" "%DESTINO%\SONNY2.swf" >nul
if errorlevel 1 goto :fin_error
del "%RESPALDOS%\%ULTIMO%" >nul
echo.
echo Listo: se restauro %ULTIMO%.
echo (la version que quitaste quedo en _respaldos_mod\antes_de_restaurar_%FECHA%.swf.bak)
echo.
pause
exit /b 0

:fin_error
echo.
pause
exit /b 1
