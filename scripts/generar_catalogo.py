#!/usr/bin/env python3
"""Actualiza el catálogo de ediciones DENTRO de index.html y ediciones.json.

Funciona en Windows, macOS y Linux; NO necesita localhost, pip ni API.
Ejecutar desde cualquier ruta: python scripts/generar_catalogo.py

El archivo scripts/ediciones_base.json preserva los registros históricos.
"""

import argparse
import json
import pathlib
import re
import sys
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve()
DEFAULT_ROOT = HERE.parent.parent
EDITION_DIR = re.compile(r"^(\d{1,4})Ed(ic|is)ion$", re.IGNORECASE)
BEGIN = "    // ECYS:CATALOGO_GENERADO:INICIO"
END = "    // ECYS:CATALOGO_GENERADO:FIN"
SEED = "scripts/ediciones_base.json"


def roman(number):
    if not 0 < number < 4000:
        return str(number)
    digits = ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
              (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
              (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    result = ""
    for value, letter in digits:
        while number >= value:
            result += letter
            number -= value
    return result


def edition_name(number):
    tens = {30: "Trigésima", 40: "Cuadragésima", 50: "Quincuagésima",
            60: "Sexagésima", 70: "Septuagésima", 80: "Octogésima",
            90: "Nonagésima"}
    units = ("", "Primera", "Segunda", "Tercera", "Cuarta", "Quinta",
             "Sexta", "Séptima", "Octava", "Novena")
    if 30 <= number < 100:
        return tens[number // 10 * 10] + (" " + units[number % 10] if number % 10 else "") + " Edición"
    return "Edición " + roman(number)


def pick_pdf(folder):
    pdfs = sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"),
                  key=lambda p: p.name.casefold())
    if not pdfs:
        return None
    preferred = next((p for p in pdfs if p.name.lower().startswith("revista_ecys_")), pdfs[0])
    return preferred.name


def scan(root):
    candidates = {}
    for directory in sorted(root.iterdir(), key=lambda p: p.name.casefold()):
        if not directory.is_dir() or directory.is_symlink():
            continue
        match = EDITION_DIR.fullmatch(directory.name)
        if not match:
            continue
        number = int(match.group(1))
        if not 1 <= number <= 3999:
            continue
        if not (directory / "index.html").is_file():
            print(f"  AVISO: omitida {directory.name}/ (no tiene index.html)")
            continue
        # Preferir 'Edicion' a 'Edision'; desempatar por grafía más legible.
        score = (match.group(2).casefold() == "ic", directory.name.endswith("Edicion"),
                 not directory.name.startswith("0"), directory.name)
        if number not in candidates or score > candidates[number][0]:
            candidates[number] = (score, directory)
    return {number: entry[1] for number, entry in candidates.items()}


def build_editions(root, originals):
    by_number = {}
    for item in originals:
        number = item.get("edition")
        if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= 3999:
            raise ValueError(f"Edición histórica inválida: {item}")
        if number in by_number:
            raise ValueError(f"Edición histórica duplicada: {number}")
        by_number[number] = dict(item)

    directories = scan(root)
    for number, directory in directories.items():
        item = by_number.get(number, {"id": f"ed_{number}", "edition": number,
                                         "name": edition_name(number)})
        # URL escapada: no hay rutas absolutas ni dependencias de la API.
        prefix = quote(directory.name)
        item["url"] = f"{prefix}/index.html"
        pdf_name = pick_pdf(directory)
        if pdf_name:
            item["pdf"] = f"{prefix}/{quote(pdf_name)}"
        else:
            item.pop("pdf", None)
        by_number[number] = item
    return [by_number[n] for n in sorted(by_number, reverse=True)]


def update_html(source, editions):
    """Reemplaza solo la zona marcada y preserva el HTML/CSS/JS restante."""
    serialized = json.dumps(editions, ensure_ascii=False, indent=2)
    generated = f"{BEGIN}\n    const editions = {serialized};\n{END}"
    if BEGIN in source or END in source:
        if source.count(BEGIN) != 1 or source.count(END) != 1:
            raise ValueError("Marcadores del catálogo duplicados o incompletos")
        pattern = re.compile(re.escape(BEGIN) + r"[\s\S]*?" + re.escape(END))
        return pattern.sub(lambda _: generated, source, count=1)

    # Compatibilidad con el index.html original (antes de instalar marcadores).
    pattern = re.compile(r"(?m)^\s*const editions\s*=\s*(\[[\s\S]*?\]);")
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise ValueError("No se encontró un único 'const editions = [...]' en index.html")
    # No actualizar a ciegas una página distinta: exigir JSON válido.
    json.loads(matches[0].group(1))
    return source[:matches[0].start()] + generated + source[matches[0].end():]


def write_if_changed(target, content, check=False):
    before = target.read_text(encoding="utf-8") if target.is_file() else None
    if before == content:
        print(f"  Sin cambios: {target.name}")
        return False
    if check:
        print(f"  DESACTUALIZADO: {target}", file=sys.stderr)
        return True
    target.parent.mkdir(parents=True, exist_ok=True)
    # Escritura reemplazando en el mismo directorio y sin alterar la codificación.
    import os
    import tempfile
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=str(target.parent), prefix=".ecys-", delete=False) as out:
            tmp = pathlib.Path(out.name)
            out.write(content)
        if target.exists():
            import stat
            os.chmod(tmp, stat.S_IMODE(target.stat().st_mode))
        os.replace(tmp, target)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    print(f"  Actualizado: {target}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                        help="Raíz del repositorio (por defecto: padre de scripts/)")
    parser.add_argument("--check", action="store_true",
                        help="Verifica sin escribir; devuelve 1 si falta regenerar")
    args = parser.parse_args()
    root = args.root.resolve()
    index_file = root / "index.html"
    seed_file = root / SEED
    if not index_file.is_file():
        parser.error(f"No existe el archivo de portada: {index_file}")
    if not seed_file.is_file():
        parser.error(f"No existe el catálogo histórico: {seed_file}")
    originals = json.loads(seed_file.read_text(encoding="utf-8-sig"))
    if not isinstance(originals, list):
        parser.error(f"El catálogo histórico no es una lista: {seed_file}")
    editions = build_editions(root, originals)
    html = update_html(index_file.read_text(encoding="utf-8-sig"), editions)
    # Archivo estático adicional para integraciones; la página no necesita fetch.
    json_text = json.dumps({"schema_version": 1, "editions": editions},
                           ensure_ascii=False, indent=2) + "\n"
    changed_index = write_if_changed(index_file, html, check=args.check)
    changed_json = write_if_changed(root / "ediciones.json", json_text, check=args.check)
    print(f"Catálogo: {len(editions)} ediciones; más reciente: {editions[0]['edition']}")
    for item in editions:
        print(f"  {item['edition']:>3}: {item['url']}")
    if args.check and (changed_index or changed_json):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
