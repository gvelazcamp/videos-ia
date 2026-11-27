# Motor 2D de imágenes — cómo se arma un video SOLO (Claude + ChatGPT + voz Charon de Gemini)

Es el método con el que se hizo «El paraguas que guardaba cuatro cielos» (23/11/2026, 2:09). Sin 3D, sin FLUX, solo costo cero.
Los robots clásicos son PNG (`robots/`). Todo corre en una sesión de Claude Code con Chrome, ffmpeg, python3 (numpy, scipy) y `puppeteer-core` (`npm i puppeteer-core`; Chrome en `/usr/bin/google-chrome`).

## Pasos (de punta a punta)
1. **Guion**: el ensayo ganador de `ensayos-nocturnos/AAAAMMDD/` → `narracion.txt` (una oración por línea, 330–400 palabras ≈ 2 min a 1,2×).
2. **Imágenes de ChatGPT** (9:16): se piden con «PEDIDO: (de Claude para ChatGPT)» en el PR #1; llegan como ZIP base64 a `bandeja/respuestas-chatgpt/<ID>/` → `python3 -I herramientas/b64-imagenes/decodificar.py <carpeta> --salida img/`. Verificar SHA-256 con `manifest.json`. La carátula (`00-caratula.png`) la entrega ChatGPT por el mismo método.
3. **Voz Charon**: crear `bandeja/para-gemini-voz/<id>.json` con `{"estilo": "...", "texto": "<narración en un párrafo>", "voces": ["Charon"]}` y pushear al puente → el workflow deja `bandeja/respuestas-gemini-voz/<id>-charon.mp3` (3 a 6 min). Si Google responde 503, tocar el archivo y reintentar; si falla, reportar BLOQUEADO (nunca simular la voz).
4. **Tiempos**: copiar el mp3 a `voz-original.mp3`; `python3 vel12.py` (→ `voz.mp3` a 1,2×); `ffmpeg -i voz.mp3 -ac 1 -ar 16000 -f s16le voz.raw`; `python3 align.py` (→ `timing.json`); `window.TIMING=` + ese json en `timing2.js`; `window.TXT=[líneas de narracion.txt]` en `txt.js`.
5. **Escenas**: editar la función `toma(i,p,t)` de `scene.html`, un `case` por línea de la narración (zoom/paneo con `foto()`, robots con `fila()`/`robot()`, carteles con `caja()`, lluvia/brillos/confeti). Probar cuadros: `node render.mjs frames 1,10,20 carpeta/`.
6. **Render**: `node render.mjs video 0 0 sin-audio.mp4` (≈4 min), `python3 musica.py <segundos>` y `bash mezclar.sh sin-audio.mp4 voz.mp3 musica.wav final.mp4`.
7. **Verificar**: `ffprobe` (≥ 1:50, 1080×1920, audio AAC), mirar 4 cuadros.
8. **Entrega**: MP4 + portada a `gvelazcamp/videos-ia` (`<nombre>-AAAAMMDD.mp4`), y comentario «PEDIDO: ChatGPT — publicar <ID>» en el PR #1 con URL raw, duración, SHA-256 y texto del post. **Claude nunca publica**: publica ChatGPT.

Reglas: robots clásicos, voz Charon 1,2×, ≥ 1:50, nombrar a ChatGPT, Claude, Gemini y Grok, nada del «1 %», nada de personajes con derechos.
`ejemplo-paraguas/narracion.txt` es el guion del video de referencia.
