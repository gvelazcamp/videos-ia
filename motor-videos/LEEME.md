# Motor de videos de Claude (copia de referencia, 19/11/2026)

Son los archivos reales con los que Claude armó los videos de los 4 robots. Proyecto de referencia: «El último mate del universo» (`ultimo-mate-20261116.mp4`).

| Archivo | Para qué |
|---|---|
| `base.js` | Escena Three.js, robots `makeBot`, composición en Canvas, `drawCaption` (subtítulos palabra por palabra) |
| `islas.js` | Islitas con aro de neón (`crearIsla`, `ISLA_IAS`, `brillo`) |
| `expresiones.js` | 6 caras (`ponerExpresion`, `iconoExpresion`) |
| `robots2.js` | Robots v2 al estilo de la portada (`makeBot2`, `activarReflejos`) |
| `scene2.html` | Página que carga las fuentes Inter, `timing2.js` y `scene2.js` |
| `render.mjs` | Puppeteer + Chrome: `renderFrame(t)` → JPEG → FFmpeg (30 fps, libx264, crf 19) |
| `vel12.py` | Acelera la voz sin cambiar el tono (recorta pausas y, si hace falta, `atempo`) |
| `align.py` | Saca de la voz el momento de cada palabra (`timing.json` → `wt`) |
| `musica.py` | Música de fondo sintetizada: `python3 musica.py <segundos>` → `musica.wav` |
| `ejemplo-ultimo-mate/` | `main.js` (escenas `seg(...)`) y `narracion.txt` del ejemplo |

Requisitos: `node_modules` con `three@0.187.0` y `puppeteer-core@25.17.0`, Chrome en `/usr/bin/google-chrome`, ffmpeg 6, python3 con numpy y scipy, y fuentes Inter en `/usr/share/fonts/opentype/inter/`.
