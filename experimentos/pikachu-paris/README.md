# Pikachu en París — escena nueva e independiente

**Punto de acceso:** [Abrir la escena](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/pikachu-paris/index.html)

El mismo personaje de referencia de Gonzalo pasa de la escena del castillo a una postal caricaturesca de París.

## Archivos

- `index.html`: composición animada responsive con paseo (balanceo y desplazamiento), pétalos, atardecer/noche, botones de vestuario, pausa y saludo.
- `escenario-paris.svg`: **asset independiente** para el fondo, ilustrado en SVG con Torre Eiffel, puente del Sena, café, faroles y árboles rosados.
- `accesorios-paris.svg`: **asset independiente** de vestuario superpuesto sobre Pikachu: boina negra con lazo rojo, vestido blanco/negro a rayas con cuello crema, moño rojo, zapatos, bolso y baguette. Son piezas **recreadas en estilo caricatura** siguiendo el conjunto de accesorios elegido; no son recortes píxel a píxel de la lámina original.
- PNG de Pikachu reutilizado desde `../pikachu-castillo-terror/personaje-removebg-web.png`, recortado anteriormente con remove.bg.

## Funcionamiento

Los tres recursos son independientes: el escenario, el PNG original del personaje y la capa de vestuario. Quitar accesorios no modifica el personaje, y el fondo se puede mostrar solo.

La animación mueve la composición completa para no deformar cara, orejas ni proporciones. No simula todavía articulación independiente de piernas.

No se modificaron las escenas anteriores (`pikachu-surf-3ia`, `pikachu-castillo-terror`) ni Girá y Adiviná. No requiere API.

## Pruebas
- Chromium 390×844 y 1180×840.
- Cargan los tres recursos de imagen.
- Funciona poner/quitar accesorios, cambiar día/noche y mostrar el saludo.
- Ningún desbordamiento horizontal ni errores de JavaScript en la prueba.
