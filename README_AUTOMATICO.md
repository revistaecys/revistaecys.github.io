# Revista ECYS — índice con detección automática de ediciones

## Función

El `index.html` de la raíz conserva el diseño institucional de la revista, las 22 ediciones ya conocidas y el identificador de Google Analytics `G-V6HS3KRG7S`.

A partir de la edición XXX, la página detecta **automáticamente** directorios nuevos en la raíz del repositorio público `revistaecys/revistaecys.github.io`, rama `master`, mediante la API pública de GitHub, sin claves ni cambios posteriores en este `index.html`.

Reconoce carpetas como `30Edicion`, `31Edicion`, `32Edicion`, etc. También admite la variante `30Edision` (aunque se recomienda usar `Edicion`). Se conservan las mayúsculas y minúsculas reales del nombre de carpeta.

La carpeta solo se agrega al menú si contiene un `index.html` que responda correctamente desde el sitio publicado. Se evita así anunciar ediciones que todavía no se pueden abrir.

## Publicar ahora el nuevo índice

1. Copia el `index.html` descargado a la **raíz** del repositorio local (`Revista-Git/index.html`), sin borrar ninguna edición histórica.
2. Conserva los archivos `google5029b875cce6dc89.html` y `.jekyllignore` sin cambios.
3. Revisa la modificación y publícala:

   ```bash
   git status
   git add index.html
   git commit -m "Activar deteccion automatica de nuevas ediciones"
   git push origin master
   ```

4. Comprueba `https://revistaecys.github.io/`.

## Publicar la edición XXX o cualquier posterior

Crea la carpeta con un `index.html` dentro:

```
revistaecys.github.io/
├── index.html                  ← ya no necesita modificarse
├── 29Edicion/
│   └── index.html
├── 30Edicion/
│   └── index.html              ← se descubrirá automáticamente
└── 31Edicion/
    └── index.html              ← también se descubrirá
```

Añade la nueva carpeta y publícala. Cuando GitHub Pages termine el despliegue, la página principal mostrará la edición más reciente al iniciar y ordenará el menú de mayor a menor. Los enlaces directos `#edicion=30`, `#edicion=31` funcionan si dichas ediciones están disponibles.

## Comportamiento en fallos y límites

- GitHub Pages no expone automáticamente un listado de directorios, de ahí la necesidad de consultar el repositorio público.
- La API REST pública de GitHub limita a **60 solicitudes por hora por dirección IP** sin autenticación. El sitio guarda la lista en el navegador durante **15 minutos** para reducir consultas; cada visitante puede tener su propia caché.
- Si GitHub no responde o se llega al límite, permanecen visibles las ediciones históricas; si existen datos locales almacenados, se utilizan provisionalmente.
- El cambio se detecta cuando se carga o recarga el sitio, no mientras está abierto sin recargar.
- La lista automática solo se comprueba al abrir el sitio por HTTP(S); el archivo `index.html` abierto mediante `file://` presenta la lista original.
- Para futuras ediciones se oculta el botón PDF de la cabecera principal, porque no es posible deducir sin riesgo el nombre del PDF. Cada nueva edición puede proporcionar su propio enlace PDF dentro de su `index.html`.
- No se modifican la medición de Analytics ni las carpetas de ediciones anteriores.

## Comprobación técnica

Se probaron con ejecución de JavaScript en Node.js los casos de: sin ediciones nuevas, incorporación de 30 y 31, carpeta 33 sin `index.html`, acceso directo con `#edicion=30` y fallo HTTP 403 de GitHub. Todos los escenarios simulados funcionaron. **La prueba visual en Chromium y el despliegue real están pendientes**.
