# Revista ECYS — Publicación automática de ediciones (GitHub Pages)

Este paquete modifica **una sola vez** la raíz de `revistaecys/revistaecys.github.io`. Las ediciones anteriores permanecen intactas.

## ¿Qué contiene?

- `index.html`: archivo principal con el diseño institucional y un catálogo automático. Conserva Google Analytics `G-V6HS3KRG7S`.
- `.github/workflows/publicar-revista.yml`: flujo que se ejecuta al publicar cambios en `master` y despliega el sitio completo en GitHub Pages.
- `scripts/generar_catalogo.py`: detecta las carpetas con nombre `29Edicion`, `30Edicion`, `30Edision`, `31Edicion`, etc. Exige un archivo `index.html` dentro de cada una.
- `ediciones.json`: **no debes crearlo manualmente**; el flujo lo genera al construir el sitio publicado. El catálogo se encuentra en `https://revistaecys.github.io/ediciones.json` al completar el despliegue.

## Instalación inicial (una sola vez)

1. Haz una copia de seguridad del `index.html` de la raíz.
2. Extrae este ZIP **encima de la raíz de tu copia local del repositorio**, no dentro de `29Edicion` ni de otra carpeta. Los archivos existentes (`28Edicion/`, `.jekyllignore`, archivo de verificación Google, etc.) se mantienen.
3. En Git Bash, ejecuta:

   ```bash
   cd "/c/Users/pabda/Desktop/Revista-Git"
   git status
   git add index.html .github/workflows/publicar-revista.yml scripts/generar_catalogo.py
   git commit -m "Automatizar publicación de ediciones ECYS"
   git push origin master
   ```

4. En GitHub entra a **Settings > Pages > Build and deployment > Source** y selecciona **GitHub Actions**. Esto es indispensable para usar el flujo de generación automática del catálogo y despliegue.
5. Abre **Actions > Publicar Revista ECYS y detectar ediciones**. Si el primer despliegue no se inició (por haber cambiado la opción Pages después de subir los archivos), usa **Run workflow**.
6. Cuando el workflow finalice correctamente, verifica el catálogo: `https://revistaecys.github.io/ediciones.json` y el sitio `https://revistaecys.github.io/`.

## Publicar la Edición XXX, XXXI o cualquiera posterior

1. En la raíz del repositorio, añade `30Edicion/` (o `31Edicion/`, etc.). Cada carpeta necesita su `index.html` y los archivos CSS, imágenes y PDF que utilice.
2. Publica la carpeta con Git:

   ```bash
   git add 30Edicion/
   git commit -m "Publicar Edicion XXX"
   git push origin master
   ```

3. GitHub Actions detecta y publica la nueva edición. **No se toca otra vez el index.html**. Al abrir la página principal, la edición de mayor número publicada aparece primera y seleccionada automáticamente.

## Importante

- **No requiere un servidor local**, no requiere conexión a la API pública de GitHub ni clave/token en el sitio web.
- La actualización no ocurre por crear una carpeta solamente en el disco de Windows. La carpeta debe estar **subida a GitHub** y el despliegue de Pages debe haber terminado. Esto es una limitación inevitable de una página remota.
- El menú se actualiza al abrir el sitio, al regresar a la pestaña, o automáticamente cada dos minutos si la página permanece abierta; no necesita botón manual.
- Si tienes una carpeta `30Edicion` que es una copia de `29Edicion`, la navegación mostrará «Trigésima Edición», pero el **contenido interno seguirá siendo el de la XXIX** hasta que actualices esos archivos.
- Se aceptan los nombres `Edicion` y `Edision` para conservar compatibilidad, pero se recomienda `30Edicion`.
- Si hay carpetas `30Edicion` y `30Edision`, se prefiere `30Edicion`.
- La cuenta de Google Analytics general se conserva; la medición exclusiva de la XXIX es una configuración diferente y no se crea con este paquete.
- Si en `Settings > Pages` no tienes permisos para elegir GitHub Actions o en el repositorio se prohíben los workflows, necesitarás solicitar acceso al administrador.

### Prueba de funcionamiento

La generación del catálogo se probó con carpetas ficticias 29, 30, 31 y 50, incluyendo nombres duplicados y carpetas sin `index.html`. La actualización de menú se verificó con un navegador Chromium y un catálogo simulado (XXIX, XXX y XXXI). La publicación real al repositorio **no está realizada**.
