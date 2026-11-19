# Ejemplos de aprendizaje (Claude, 19/11/2026). Todo probado por Claude en su sesión.

- **`escena-bateria/`**: escena completa autocontenida, sin imágenes. Batería 100→0 entre «energía» y «cero», puerta que se abre desde «puerta» y Grok que reacciona en «gritó».
  - `hoja-prueba.jpg`: cuadros de control.
  - `prueba-14s.mp4`: demo con **voz falsa (tono)** y tiempos falsos, solo para probar el motor.
- **`preflight.mjs`**: control antes de renderizar. Probado: da OK con datos correctos, y FALLA (código 1) si `narracion.txt` tiene una palabra de más.
- **`mezclar.sh`**: mezcla de voz + música con ducking + 2 efectos en palabras exactas de `timing.json`. Probado y con audio verificado (`volumedetect`).

## Pasos, dentro de una copia de `escena-bateria/` que tenga `node_modules`, `render.mjs`, `scene2.html` y la voz real
```
python3 ../../vel12.py && ffmpeg -y -i voz.mp3 -ar 16000 -ac 1 -f s16le voz.raw && python3 ../../align.py > align.log
python3 -c "import json;j=json.load(open('timing.json'));open('timing2.js','w').write('window.TIMING='+json.dumps({'wt':j['wt'],'dur':j['dur']})+';')"
node ../preflight.mjs                                   # si falla, NO se renderiza
cat ../../base.js ../../islas.js ../../expresiones.js main.js > scene2.js
node render.mjs frames 2,7.5,9.8,13.5 chk && node render.mjs video 0 0 sin-audio.mp4
python3 ../../musica.py 15 && bash ../mezclar.sh sin-audio.mp4 voz.mp3 musica.wav puerta.wav alarma.wav 24 13 final.mp4
```
