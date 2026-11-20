# Kit de escenas — para armar videos rápido con los robots de siempre (sin FLUX)

**Regla de Gonzalo (20/11/2026):** robots de siempre (`makeBot`), escenas con código, sin FLUX, voz Charon 1,2×.

## Piezas listas (`kit.js`)
| Función | Qué dibuja |
|---|---|
| `bateria(x,y,%,alfa,T)` | batería con porcentaje (roja que titila si < 5 %) |
| `cartel(txt,x,y,k,color,tamaño)` | cartel con borde de color que aparece con rebote |
| `emoji(e,x,y,tamaño,k)` | emoji que aparece con rebote (íconos sobre los robots, animales, objetos) |
| `semaforo(x,y,alfa,verdePeatón,parpadea,T)` | semáforo con luz para autos y peatón |
| `cableEnergia(x0,y0,x1,y1,k,T)` | cable con energía corriendo |
| `lluvia(T,k)`, `oscuro(k)`, `alarma(T,k)`, `glow(...)` | clima, apagón, alarma roja, halos de luz |
| `cabeza(n)` | punto arriba de la cabeza de un robot (para baterías, íconos) |
| `franjaSubtitulos()` | franja oscura antes de `drawCaption` |

**Truco aprendido:** lo que tiene que verse con color en la oscuridad (animales, objetos) se dibuja **después** de `oscuro()`, con un `glow` debajo.

## Pasos (en una carpeta nueva, con los archivos de `motor-videos/`)
```bash
cp voz-charon.mp3 voz-original.mp3 && python3 vel12.py          # 1,2×
ffmpeg -y -i voz.mp3 -ac 1 -ar 16000 -f s16le voz.raw && python3 align.py | tee align.log
echo "window.TIMING=$(cat timing.json);" > timing2.js
cat base.js islas.js expresiones.js kit-escenas/kit.js main.js > scene2.js
node ejemplos-aprendizaje/preflight.mjs                          # controla texto, tiempos y voz
node render.mjs frames 2,10,20,30 ctl                           # cuadros de control
node render.mjs video 0 0 sin-audio.mp4
python3 musica.py <duración> && bash ejemplos-aprendizaje/mezclar.sh sin-audio.mp4 voz.mp3 musica.wav silencio.wav silencio.wav 0 0 final.mp4
```
Ejemplo completo: `ejemplo-1-por-ciento/` (video «1 %», 20/11/2026). Ese `main.js` tiene sus propias copias de las piezas; para un video nuevo usar `kit.js` y escribir solo los `seg(...)` y el `renderFrame`.
