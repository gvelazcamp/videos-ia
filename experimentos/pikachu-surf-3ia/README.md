# Pikachu haciendo surf — ChatGPT + Gemini + Grok

Proyecto aislado autorizado por Gonzalo, 16 de noviembre de 2026. Sin modificar Girá y Adiviná, biblioteca CUATRO ni el proyecto de robots.

**Vista web:** https://gvelazcamp.github.io/pikachu-surf-3ia/

- `referencia-original.png`: imagen exacta subida por Gonzalo, 298×342 píxeles. SHA-256: `5e5959e74a4d49844761b14d11cb97b3a10d9331f2883ee35452edde53633b99`.
- `recorte-personaje.webp`: recorte transparente preparado por ChatGPT a partir de los píxeles de la misma referencia. No es un redibujo: cara, colores y contornos internos siguen siendo los de la imagen. Algunos bordes pueden requerir retoque.
- `movimiento-grok.js`: coreografía JavaScript de 8 segundos entregada realmente por Grok CLI. [Respuesta de Grok](https://github.com/gvelazcamp/chatgpt-claude-puente/blob/main/bandeja/respuestas-grok/pikachu-surf-movimiento-20261116.md). Grok aclaró que no pudo ver la foto, por lo que solo diseñó el movimiento.
- `index.html`: integración por ChatGPT con SVG de olas, tabla de surf y trazado superpuesto extraído de segmentación de la silueta.
- **Gemini:** analizó realmente la referencia enviada a su puente de imágenes, generó una ficha de colores, coordenadas y sugerencias. [Respuesta de Gemini](https://github.com/gvelazcamp/chatgpt-claude-puente/blob/main/bandeja/respuestas-gemini/pikachu-surf-trazos-20261116.md). Parte de sus coordenadas eran aproximadas, de modo que **no se sustituyó el arte original por ese SVG**.

**Límite:** Se mueve el recorte íntegro del personaje (no articulación independiente de pies ni brazos), para conservar el mismo aspecto. El trazo resaltado es un contorno estimado de segmentación y no garantiza fidelidad vectorial píxel a píxel.

No se emplean APIs pagas nuevas. La vista de GitHub Pages se publica en una carpeta nueva, independiente de CUATRO.
