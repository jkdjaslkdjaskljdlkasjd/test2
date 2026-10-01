@echo off
setlocal EnableExtensions
title Sonny 2 - instalar version del mod

rem ---------------------------------------------------------------------------
rem  Copia el SONNY2.swf que esta junto a este archivo en la carpeta del juego.
rem  Antes guarda el que habia en Resources\_respaldos_mod (deja los 5 ultimos).
rem  Si tu juego esta en otra carpeta, cambia la linea DESTINO_DEFECTO.
rem ---------------------------------------------------------------------------
set "DESTINO_DEFECTO=C:\Program Files (x86)\Steam\steamapps\common\Sonny Legacy Collection\SonnyLegacy.app\Contents\Resources"

rem --- Program Files necesita permisos de administrador: si no los tiene, se vuelve a abrir pidiendolos
net session >nul 2>&1
if errorlevel 1 goto :elevar
goto :inicio

:elevar
echo Pidiendo permisos de administrador...
powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
exit /b

:inicio
cd /d "%~dp0"
set "ORIGEN=%~dp0SONNY2.swf"
if exist "%ORIGEN%" goto :origen_ok
rem --- si no esta al lado, se busca en las subcarpetas (por ejemplo I32\SONNY2.swf)
set "ORIGEN="
for /r "%~dp0." %%F in (SONNY2.swf) do if exist "%%F" if not defined ORIGEN set "ORIGEN=%%F"
if defined ORIGEN goto :origen_ok
echo.
echo [ERROR] No encuentro SONNY2.swf junto a este archivo ni en sus subcarpetas.
echo         Pon INSTALAR.bat en la carpeta de la version que descomprimiste.
goto :fin_error

:origen_ok
set "DESTINO=%DESTINO_DEFECTO%"
if exist "%DESTINO%\SONNY2.swf" goto :destino_ok
echo.
echo No encuentro el juego en la carpeta de siempre:
echo "%DESTINO%"
echo.
echo Pega la ruta de la carpeta Resources del juego (la que tiene SONNY2.swf)
echo y pulsa Enter. Puedes arrastrar la carpeta a esta ventana.
set /p "DESTINO=Ruta: "
set "DESTINO=%DESTINO:"=%"
if exist "%DESTINO%\SONNY2.swf" goto :destino_ok
echo.
echo [ERROR] En esa carpeta no hay ningun SONNY2.swf.
goto :fin_error

:destino_ok
rem --- el juego no puede estar abierto mientras se reemplaza el archivo
:esperar_juego
tasklist /FI "IMAGENAME eq Sonny Legacy Collection.exe" 2>nul | find /I "Sonny Legacy Collection.exe" >nul
if errorlevel 1 goto :juego_cerrado
echo.
echo El juego esta abierto. Cierralo y pulsa una tecla para seguir.
pause >nul
goto :esperar_juego

:juego_cerrado
for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "FECHA=%%T"
set "RESPALDOS=%DESTINO%\_respaldos_mod"
if not exist "%RESPALDOS%" mkdir "%RESPALDOS%"
copy /Y "%DESTINO%\SONNY2.swf" "%RESPALDOS%\SONNY2_%FECHA%.swf" >nul
if errorlevel 1 goto :error_respaldo

copy /Y "%ORIGEN%" "%DESTINO%\SONNY2.swf" >nul
if errorlevel 1 goto :error_copia

rem --- comprobar que el archivo instalado es identico al de la version
fc /b "%ORIGEN%" "%DESTINO%\SONNY2.swf" >nul
if errorlevel 1 goto :error_copia

rem --- dejar solo los 5 respaldos mas nuevos
powershell -NoProfile -Command "Get-ChildItem -LiteralPath $env:RESPALDOS -Filter 'SONNY2_*.swf' | Sort-Object LastWriteTime -Descending | Select-Object -Skip 5 | Remove-Item -Force" >nul 2>&1

for /f %%H in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 -LiteralPath $env:ORIGEN).Hash.ToLower()"') do set "HASH=%%H"
echo.
echo ============================================================
echo  Listo: SONNY2.swf instalado.
echo  SHA-256: %HASH%
echo  (compara las primeras letras con la tabla del LEEME.md)
echo.
echo  Respaldo del anterior: _respaldos_mod\SONNY2_%FECHA%.swf
echo  Para volver atras, usa RESTAURAR.bat.
echo ============================================================
echo.
pause
exit /b 0

:error_respaldo
echo.
echo [ERROR] No pude guardar el respaldo del SONNY2.swf actual. No se cambio nada.
goto :fin_error

:error_copia
echo.
echo [ERROR] No pude copiar el SONNY2.swf nuevo. Restaurando el anterior...
copy /Y "%RESPALDOS%\SONNY2_%FECHA%.swf" "%DESTINO%\SONNY2.swf" >nul
goto :fin_error

:fin_error
echo.
pause
exit /b 1
