#!/usr/bin/env python3
"""Genera ediciones.json desde carpetas de ediciones publicables.

Uso: python3 scripts/generar_catalogo.py --root . --output ediciones.json
No necesita API, autenticación ni instalar dependencias.
"""
import argparse
import datetime as dt
import json
import pathlib
import re

EDITION_DIR = re.compile(r'^(\d{1,4})Ed(ic|is)ion$', re.IGNORECASE)


def scan(root: pathlib.Path) -> list[dict]:
    result = {}
    for directory in root.iterdir():
        if not directory.is_dir() or directory.is_symlink():
            continue
        match = EDITION_DIR.fullmatch(directory.name)
        if not match:
            continue
        number = int(match.group(1))
        if number < 29:
            continue  # Las ediciones anteriores ya están registradas en el índice.
        index = directory / 'index.html'
        if not index.is_file():
            continue
        # Dar preferencia a la ortografía correcta «Edicion», si hay duplicados.
        priority = (match.group(2).lower() == 'ic', directory.name.endswith('Edicion'))
        previous = result.get(number)
        if previous and previous['_priority'] >= priority:
            continue
        item = {'edition': number, 'folder': directory.name,
                'url': f'{directory.name}/index.html', '_priority': priority}
        # No inventar PDF: mostrar enlace si la carpeta contiene uno.
        pdfs = sorted(p for p in directory.glob('*.pdf') if p.is_file())
        if pdfs:
            preferred = next((p for p in pdfs if p.name.startswith('Revista_ECYS_')), None)
            item['pdf'] = f'{directory.name}/{(preferred or pdfs[0]).name}'
        result[number] = item
    return [dict((k, v) for k, v in item.items() if k != '_priority')
            for _, item in sorted(result.items(), reverse=True)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=pathlib.Path, default=pathlib.Path('.'))
    parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('ediciones.json'))
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f'No existe la carpeta raíz: {args.root}')
    catalog = {
        'schema_version': 1,
        'generated_at_utc': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        'editions': scan(args.root),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Catálogo generado: {args.output}, {len(catalog["editions"])} ediciones modernas')
    for item in catalog['editions']:
        print(f'  {item["edition"]}: {item["url"]}')

if __name__ == '__main__':
    main()
