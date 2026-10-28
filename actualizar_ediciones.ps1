$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 'scripts/generar_catalogo.py' '--root' '.'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python 'scripts/generar_catalogo.py' '--root' '.'
} else {
    Write-Error 'Python 3 no esta instalado o no se encuentra en PATH.'
    exit 1
}
exit $LASTEXITCODE
