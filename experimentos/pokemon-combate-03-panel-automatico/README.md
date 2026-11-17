# Pikachu vs. Cubone — versión 03: poderes que se seleccionan solos

**[Reproducir el MP4 desde el celular](https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/3fc27c11-5f10-4428-9422-40b7a5bcf1b0.mp4)**

**[Ver video guardado en GitHub](pikachu-vs-cubone-panel-automatico.mp4)**

Este video conserva el combate **02** (estilo ilustrado aprobado por el usuario) y su narración original de Gemini. ÚNICAMENTE cambia el menú de ataques inferior para que el propio video seleccione e ilumine automáticamente el ataque correspondiente al turno, sin pedir interacción al espectador.

## Qué cambia en el video

- **Pikachu ataca:** menú azul eléctrico, movimientos Rayo, Ataque Rápido, Cola Férrea, Impactrueno. El botón usado se ilumina y palpita.
- **Cubone ataca:** menú en tonos tierra, movimientos Hueso Palo, Cabezazo, Huesomerang y Excavar. Se ilumina el suyo.
- **Entrada y victoria:** sin ataque seleccionado; cambia el título del menú.
- Las cuatro opciones aparecen siempre para el atacante actual. **No son botones interactivos:** el video realiza cada elección solo y los cuadros de ataque siguen la narración.
- No se modifica la secuencia de golpes ni los valores de vida. El video sigue respetando que Cubone, de tipo Tierra, no recibe daño eléctrico.

| Tiempo | Pokémon activo | Movimiento iluminado | Color del panel |
| --- | --- | --- | --- |
| 00:00–00:07.9 | Pikachu | Presentación, ninguno | Azul |
| 00:07.9–00:16.8 | Pikachu | Rayo | Azul/dorado |
| 00:16.8–00:22.5 | Cubone | Hueso Palo | Tierra/ámbar |
| 00:22.5–00:27.3 | Pikachu | Ataque Rápido | Azul/blanco |
| 00:27.3–00:32.2 | Cubone | Cabezazo | Tierra/ámbar |
| 00:32.2–00:39.5 | Pikachu | Cola Férrea | Azul/acero |
| 00:39.5–00:45.0 | Cubone | Huesomerang | Tierra/ámbar |
| 00:45.0–00:54.6 | Pikachu | Ataque Rápido final | Azul/blanco |
| 00:54.6–final | Pikachu | Victoria, ninguno | Azul |

## Fuente y producción

- Fuente visual y de audio original, **inalterada**: `../pokemon-combate-02-referencia/pikachu-vs-cubone-estilo-aprobado.mp4`.
- `panel_automatico.py`: recompone exclusivamente los últimos 231 píxeles del fotograma (menú). El resto de los fotogramas proviene del video anterior, y se copia el audio original sin remezclarlo.
- [GitHub Actions](https://github.com/gvelazcamp/videos-ia/actions/workflows/pokemon-combate-03-panel-automatico.yml): reconstruye y publica el archivo nuevo.
- Exportación: 540 × 960, H.264 + AAC, duración ~61 segundos. Enlace MP4 fuera del visor interno de GitHub para Android.

**No modifica** `pokemon-combate-02-referencia/`, la primera pelea, otros videos, Pikachu París ni Girá y Adiviná.

Experimento no oficial de fan animation, sin afiliación con Pokémon o Nintendo.
