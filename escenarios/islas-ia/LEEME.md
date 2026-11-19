# Islitas de las IA: pieza fija para todos los videos (Gonzalo, 16/11/2026)

Estilo tomado de las referencias de Gonzalo (`islitas/isla-chatgpt.png`):
- Plataforma violeta redondeada.
- Aro de neón del color de cada IA, con resplandor.
- Bandera con el nombre en un mástil plateado.
- Pedestal violeta con botón del color (Grok: aro blanco más fino y separado, y una hoja en el pedestal; Claude: portátil naranja; GitHub: cartel negro entre dos postes y bandeja celeste con papeles, sin robot ni pedestal).
- El robot chibi adelante.

**Regla:** en cada video, cada IA está sobre su islita, y **la islita se ilumina cuando se nombra a esa IA o cuando habla**: `isla.userData.luz(1)`. Las demás quedan tenues: `luz(0)`.

Uso: `cat base.js islas.js main.js > scene2.js`. En `main.js`: `const g = crearIsla('chatgpt', 2.3); scene.add(g); g.userData.luz(k);`.

## Expresiones de los robots (expresiones.js)
6 caras: contento, sorprendido, pensando, asustado, festejando, triste.
`prepararCara(bot)` una vez; después `ponerExpresion(bot, 'festejando', T)` en cada cuadro y
`iconoExpresion(bot, expr, T)` dibuja el ícono arriba de la cabeza (rayitos, !!, ?, gotitas, papelitos, lágrima).
Demo: `cat base.js islas.js expresiones.js demo-expresiones.js > scene2.js`.

## Robots v2 (robots2.js), estilo de las portadas de ChatGPT
`makeBot2('chatgpt'|'claude'|'gemini'|'grok')`: cabeza grande de carcasa brillante, visor negro con ojos de neón del color de cada IA, y placa en el pecho.
Accesorios de cada uno:
- ChatGPT: auriculares verdes.
- Claude: auriculares naranjas y antenitas.
- Gemini: lentes celestes.
- Grok: casco oscuro con aletas y ojos verdes.

Funciona con `ponerExpresion` e `iconoExpresion`. Llamar `activarReflejos()` en `build()` y agregar `"three/addons/"` al importmap del HTML.
Ver `robots-nuevos-comparacion.jpg`.
