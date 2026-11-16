# Islitas de las IA: pieza fija para todos los videos (Gonzalo, 16/11/2026)

Estilo tomado de las referencias de Gonzalo (`referencias/recibidas/01-chatgpt-hq.webp`):
- Plataforma violeta redondeada.
- Aro de neón del color de cada IA, con resplandor.
- Bandera con el nombre en un mástil plateado.
- Pedestal violeta con botón del color (Grok: aro blanco más fino y separado, y una hoja en el pedestal; Claude: portátil naranja; GitHub: bandeja celeste con papeles, sin robot).
- El robot chibi adelante.

**Regla:** en cada video, cada IA está sobre su islita, y **la islita se ilumina cuando se nombra a esa IA o cuando habla**: `isla.userData.luz(1)`. Las demás quedan tenues: `luz(0)`.

Uso: `cat base.js islas.js main.js > scene2.js`. En `main.js`: `const g = crearIsla('chatgpt', 2.3); scene.add(g); g.userData.luz(k);`.
