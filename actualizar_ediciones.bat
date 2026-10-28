@echo off
setlocal
pushd "%~dp0" || exit /b 1
where py >nul 2>nul
if not errorlevel 1 (
  py -3 scripts\generar_catalogo.py --root .
) else (
  python scripts\generar_catalogo.py --root .
)
set "RESULTADO=%ERRORLEVEL%"
popd
if not "%RESULTADO%"=="0" echo ERROR: No se pudo actualizar el catalogo ECYS.
exit /b %RESULTADO%
