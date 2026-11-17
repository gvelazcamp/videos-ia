# París Pixel Quest — minijuego pixel art

**Abrir:** https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/pikachu-paris-videojuego/index.html

Este juego es **independiente** de la escena animada original
`experimentos/pikachu-paris/index.html`, del castillo, del surf, y de Girá y Adiviná.

## Cómo jugar

- Celular: botones ◀ ▶ y SALTAR.
- Computadora: flechas izquierda/derecha o A/D; barra espaciadora, W o flecha arriba para saltar.
- Objetivo: juntar **al menos seis** de ocho croissants y alcanzar la salida del nivel en la zona de la Torre Eiffel.
- Hay cuatro charcos. Saltarlos evita perder vidas. Tenés tres vidas.
- Se puede reiniciar y volver a jugar después de ganar o perder.

## Técnica

- `index.html` es un minijuego HTML5 Canvas completo, autocontenido (no necesita `npm`, instalación o servidor).
- El escenario, edificios, café, puente del Sena, farolas, árboles, Torre Eiffel, monedas, charcos y terreno se dibujan por código en una resolución interna **400×256**, escalada con `image-rendering: pixelated`.
- Se carga la **imagen transparente existente de Pikachu** en:
  `experimentos/pikachu-castillo-terror/personaje-removebg-web.png`.
- Se carga el **SVG de ropa parisina existente** en:
  `experimentos/pikachu-paris/accesorios-paris.svg`.
- Los dos se rasterizan como un único sprite pequeño de **57×66 píxeles**. Esto conserva la cara y la silueta del Pikachu original, con boina negra, vestido, bolso, baguette y zapatos.
- Si los recursos externos no cargan, hay un sprite pixelado de respaldo, para que la partida no quede en blanco.
- La cámara sigue al personaje a lo largo de un mapa de 1380 píxeles del mundo.
- Movimiento horizontal, saltos con gravedad, colisiones, objetos recolectables, daño con invulnerabilidad temporal, vidas y victoria/derrota.
- Se puede jugar con teclado o controles táctiles; sin API ni cuentas.

## Comprobación real en Chromium

- Comprobadas medidas 390×844 (celular) y 1180×880.
- Controles y contador de croissants funcionando; sin errores de JavaScript ni desplazamiento horizontal de página.
- Se completó la misión de punta a punta: **victoria con 8/8 croissants y dos vidas restantes** usando controles de teclado.
- Botón táctil de avance comprobado con eventos de puntero y movimiento real.

**Limitación:** es un primer nivel arcade 2D. Los brazos y piernas del personaje no tienen articulación individual: la imagen y el vestuario se mueven juntos como sprite pixelado para conservar sus trazos.
