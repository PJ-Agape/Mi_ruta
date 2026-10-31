# Estudio AGP

Aula virtual de formación para equipos de pastoral juvenil. Es un sitio estático (HTML, CSS y JavaScript) pensado para publicarse en GitHub Pages. No usa cuentas de usuario: los avances, las plantillas completadas y la bitácora de cada participante se guardan en su propio navegador.

## Qué incluye

- **Inicio:** lista de cursos con el avance de cada uno.
- **Página del curso:** módulos, clases, progreso, programa y sesiones en vivo.
- **Clase:** pestañas de Apunte, Plantilla (con casillas para escribir e imprimir), Guía del relator (visible al activar «Vista relator») y Aplicación (tareas marcables y bitácora personal).
- **Sesiones en vivo:** calendario de las 15 semanas con botón para entrar a la videollamada.

## Cómo configurar

Todo lo que se cambia a mano está en la carpeta `datos/`:

| Archivo | Para qué sirve |
| --- | --- |
| `datos/sitio.json` | Nombre del aula, lema y lista de cursos |
| `datos/curso-liderazgo.json` | Título, descripción, enlace de videollamada, fechas de sesiones, videos y presentaciones |
| `datos/indice-liderazgo.json` | Se genera solo (ver abajo); no editar a mano |

**Fechas y videollamadas.** En `sesiones`, completa `fecha`, `hora`, `lugar` y `enlace` de cada semana. Si todas las sesiones usan la misma sala, pon el enlace en `videollamada.enlace`.

**Videos y presentaciones.** En `recursos`, agrega una entrada por clase con su identificador (por ejemplo `m1-c01`, `m2-c12`, `m3-s14`):

```json
"recursos": {
  "m1-c01": {
    "video": "https://www.youtube.com/watch?v=XXXXXXXX",
    "presentacion": "https://docs.google.com/presentation/d/XXXXXXXX/edit"
  }
}
```

Se aceptan videos de YouTube, Vimeo y Google Drive, y presentaciones de Google Slides o PDF.

## Cómo actualizar el contenido

El texto de cada módulo está en `fuentes/modulo1.md`, `fuentes/modulo2.md` y `fuentes/modulo3.md`. Después de editarlos, ejecuta:

```
python3 herramientas/dividir.py
```

El script separa cada módulo en una clase por archivo (`contenido/liderazgo/`) y actualiza el índice. El programa del curso está en `contenido/liderazgo/programa.md`.

## Ver el sitio en el computador

Como el sitio carga archivos, necesita un servidor local:

```
python3 -m http.server 8000
```

y luego abrir `http://localhost:8000`.

## Publicar en GitHub Pages

En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, rama `main`, carpeta `/ (root)`. El sitio queda en `https://iperezconus84-coder.github.io/estudio_agp/`.

## Créditos

Usa [marked](https://github.com/markedjs/marked) (licencia MIT) para mostrar el contenido.
