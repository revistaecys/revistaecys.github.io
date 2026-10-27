# Revista ECYS — corrección del detector de nuevas ediciones

## Motivo del problema
El índice anterior dependía de la API pública de GitHub y no comprobaba nuevas carpetas cuando se abría como archivo (`file://`). También almacenaba una lista hasta 15 minutos.

## Nuevo comportamiento
La raíz verifica directamente rutas `30Edicion/index.html`, `31Edicion/index.html`, etc., y las variantes `30Edision`, `30edicion`, `30edision`. La API pública de GitHub permanece como método complementario para detectar saltos grandes en la numeración. No se requiere ninguna clave. El menú tiene un botón para volver a buscar en ese momento, sin esperar la caché.

**Nota:** un sitio estático no puede listar todas las carpetas del ordenador desde un HTML abierto con doble clic. Para probar el reconocimiento local, sirve el directorio raíz por HTTP como se indica abajo.

## Prueba local en Windows
1. Guarda el archivo `index.html` corregido en la raíz del repositorio local.
2. Comprueba que la carpeta `30Edicion` está al lado del índice y contiene `index.html` (no anidada dentro de `29Edicion`).
3. En PowerShell:

```powershell
cd "$env:USERPROFILE\Desktop\Revista-Git"
py -m http.server 8000
```

4. Abre `http://localhost:8000` en Chrome/Edge. La edición XXX debería aparecer. Puedes usar el botón «Buscar nuevas ediciones» si acabas de crear la carpeta. Para detener el servidor presiona `Ctrl+C`.

## Publicación
Si la carpeta de la edición XXX no se ha subido a GitHub, no aparecerá en el sitio público. Antes de publicar, comprueba en el repositorio local que se ve `30Edicion/index.html`:

```bash
git status
git add index.html 30Edicion/
git commit -m "Corregir detector automatico y agregar Edicion XXX"
git push origin master
```

Si `git commit` dice que no hay cambios, no es necesario repetirlo. Confirma en `https://revistaecys.github.io/30Edicion/index.html` que ya se puede abrir sin un error 404, y después revisa `https://revistaecys.github.io/`.

## Seguridad y compatibilidad
No se modifica la etiqueta `G-V6HS3KRG7S`, las 22 ediciones existentes, el archivo `.jekyllignore`, ni el archivo de verificación de Google. Las búsquedas limitadas en rutas sucesivas sirven de respaldo cuando la API no está disponible; la API ofrece la cobertura más amplia para ediciones con números no consecutivos.

## Prueba técnica
Se probaron en Chromium mediante respuestas simuladas: detección de `30Edicion` con API 403, detección de `31Edision` al actualizar y ausencia de ediciones inexistentes. No se realizó una comprobación directa del repositorio real por restricción de conexión externa en el entorno de pruebas.
