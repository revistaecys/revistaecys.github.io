#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 scripts/generar_catalogo.py --root .
fi
exec python scripts/generar_catalogo.py --root .
