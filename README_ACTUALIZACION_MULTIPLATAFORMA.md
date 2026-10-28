# Revista ECYS — detección de ediciones sin localhost

Esta actualización sustituye **la búsqueda de carpetas desde JavaScript** por un generador local y en CI/CD que reescribe el catálogo de `index.html`. Funciona al abrir el HTML con doble clic (`file://`) y durante la publicación en GitHub Pages.

## 1. Instalación (solo la primera vez)

1. Haz una copia de seguridad de la carpeta local de tu repositorio y, especialmente, de `index.html`.
2. Extrae el ZIP de actualización **en la raíz del repositorio que ya contiene `02Edicion/`, `28Edicion/`, `29Edicion/`, etc.** No lo extraigas dentro de `29Edicion/` ni borres las carpetas existentes.
3. Acepta sustituir el `index.html` raíz y el workflow anterior. El archivo `29Edicion/index.html` es distinto: **no debes sustituirlo**.
4. Conserva `.jekyllignore` y `google5029b875cce6dc89.html` sin cambios. La actualización no los incluye ni los borra.
5. Requiere Python 3.9 o superior, sin dependencias de `pip`.
6. Ejecuta el actualizador de tu sistema operativo. También puedes ejecutarlo de nuevo después de agregar una edición.

## 2. Actualizar en tu computadora

- **Windows (CMD / doble clic):** `actualizar_ediciones.bat`
- **Windows PowerShell:** `./actualizar_ediciones.ps1` (la política de scripts de tu equipo podría bloquear `.ps1`; en ese caso utiliza `.bat`).
- **Linux / WSL / macOS:** `./actualizar_ediciones.sh` (si se perdió el permiso de ejecución: `sh actualizar_ediciones.sh`).
- **Cualquier SO:** `python scripts/generar_catalogo.py` (en Linux/macOS también `python3`).

El script busca carpetas de ediciones **en la misma raíz que `index.html`**. Acepta `30Edicion`, `31Edicion`, `30Edision`, `30edicion`, `02Edicion` y similares. **Cada carpeta debe tener su propio `index.html`**. Una carpeta vacía no se publicará. Si existe `Revista_ECYS_XXX.pdf` u otro PDF en su raíz, el botón «Ver PDF» utilizará su nombre real; sin PDF, el botón se oculta. Si existen dos nombres de carpeta para la misma edición, prioriza `Edicion` frente a `Edision`.

**Archivos que modifica:** `index.html` y `ediciones.json` en la raíz. No toca el HTML ni las imágenes de las ediciones, tampoco modifica `scripts/ediciones_base.json`. El catálogo histórico original se conserva; el archivo base tiene los 22 registros históricos del índice aportado. Para modificar deliberadamente metadatos históricos, editar `scripts/ediciones_base.json` (no el bloque generado de `index.html`).

### Ejemplo: publicar edición 30 localmente

```text
revistaecys.github.io/
├── index.html
├── actualizar_ediciones.bat
├── actualizar_ediciones.sh
├── scripts/
│   ├── generar_catalogo.py
│   └── ediciones_base.json
├── 29Edicion/
│   └── index.html
└── 30Edicion/
    ├── index.html
    └── Revista_ECYS_XXX.pdf
```

Ejecuta el script; abre el `index.html` de la raíz **con doble clic**, sin servidor. Aparecerá la XXX como más reciente. Puedes usar `#edicion=30` en la URL para abrirla directamente. Si modificas o borras carpetas, vuelve a ejecutar el script y recarga el archivo en el navegador.

## 3. Publicación con GitHub Actions

La configuración está en `.github/workflows/publicar-revista.yml`; conserva la rama `master` que figura en tu workflow original. En GitHub ve a **Settings → Pages → Build and deployment → Source** y selecciona **GitHub Actions**. Es necesaria esa opción para que Pages despliegue el resultado generado por el workflow.

Al subir un commit a `master`, o ejecutar manualmente **Actions → Publicar Revista ECYS y detectar ediciones → Run workflow**, el workflow:

1. Descarga las carpetas del commit.
2. Ejecuta las pruebas automáticas.
3. Ejecuta `python3 scripts/generar_catalogo.py --root .` para modificar `index.html` y regenerar `ediciones.json` dentro del entorno de CI.
4. Publica la versión generada directamente en GitHub Pages, sin `git commit` ni `git push` automático.

Por tanto, si subes `30Edicion/index.html` **aunque hayas olvidado ejecutar el actualizador local**, GitHub Actions la detecta en la publicación. Si la carpeta está solo en tu disco y no la has subido, **no puede aparecer en GitHub Pages**. La detección no es en tiempo real: ocurre al ejecutar el script o cuando se inicia el flujo de GitHub.

```bash
# Desde la raíz del repositorio, después de instalar los archivos:
git add index.html ediciones.json actualizar_ediciones.bat actualizar_ediciones.ps1 actualizar_ediciones.sh scripts/generar_catalogo.py scripts/ediciones_base.json pruebas/test_catalogo.py .github/workflows/publicar-revista.yml README_ACTUALIZACION_MULTIPLATAFORMA.md
git commit -m "Activar catalogo ECYS multiplataforma y publicacion automatica"
git push origin master

# En el futuro, puedes subir nuevas ediciones sin editar el indice manualmente:
git add 30Edicion/
git commit -m "Publicar Edicion XXX"
git push origin master
```

Si quieres que **el repositorio Git conserve el `index.html` actualizado**, ejecuta el script local ANTES del `git add` y añade también `index.html` y `ediciones.json` al commit. Si no lo haces, el sitio publicado sí los tendrá actualizados, pero esos cambios estarán solo en el artefacto del CI.

## 4. Verificaciones

```bash
# Regenerar en local
python3 scripts/generar_catalogo.py

# Confirmar que index.html y ediciones.json ya coinciden con las carpetas
python3 scripts/generar_catalogo.py --check

# Pruebas unitarias (sin internet)
python3 -m unittest discover -s pruebas -p 'test_*.py' -v
```

**Protecciones:** el script ignora carpetas sin `index.html`, no inventa rutas PDF, no necesita tokens, no hace llamadas a la API de GitHub y no instala dependencias. Repetir su ejecución con los mismos archivos no vuelve a reescribir nada. Se mantiene el diseño del índice, el Google Analytics `G-V6HS3KRG7S` y los enlaces históricos aportados.

**Limitación técnica:** los archivos que carguen JavaScript externo o APIs dentro de una edición podrían seguir necesitando HTTP en su propia implementación. El catálogo principal y los enlaces de las carpetas no dependen de localhost.

**Estado:** el generador y el índice se han probado en un entorno local; no se ha ejecutado un push ni despliegue en el repositorio real.
