# Prueba aislada: ChatGPT + Claude programando un robot

**Autorización de Gonzalo (16/11/2026):** preparar prueba en la nube, sin modificar proyectos funcionales ni activar servicios pagos.

## Qué existe y qué no
- ChatGPT: `robot-base.js` (robot 3D experimental basado en la silueta original), `expresiones-chatgpt.js` (gestos y parpadeos), `escena.js` (integración y previsualización), `index.html` (interfaz).
- Claude: **PENDIENTE** de añadir **solo** `animacion-claude.js` en esta carpeta. Ningún archivo debe aparentar que Claude ya programó la caminata si no lo ha hecho.
- El robot original que Claude creó en `escenarios/islas-ia/robots2.js` y el archivo `expresiones.js` **NO se modifican**. La nueva representación es una copia experimental para probar el flujo de integración.
- No hay sincronización ChatGPT continua autónoma garantizada: este chat participa cuando está activo. El CI de GitHub comprueba los archivos tras cada push. La prueba no requiere API pagas.

## Contrato estricto para Claude
Crear exclusivamente `experimentos/robot-colaborativo/animacion-claude.js` con:

```js
export function aplicarCaminata(bot, t, intensidad=1) {
  // t: segundos transcurridos; intensidad: 0..1
  // bot.userData.body, arms[0..1], feet[0..1] y head disponibles.
  // Caminar en el sitio, sin salir de cuadro ni teletransportar.
}
```

La función se llamará **después** de `aplicarExpresion` en cada fotograma. Claude controla pasos, balanceo de brazos y rebote corporal, pero debe respetar los ojos, la boca y las expresiones de ChatGPT. Mantener sin dependencias pagas, sin editar más archivos. Si fuera imprescindible cambiar el contrato, dejar propuesta por GitHub antes de tocarlo.

## Cómo probar
- Abrir `index.html` usando un servidor web estático o GitHub Pages si se habilita después, no `file://` (los módulos JS necesitan HTTP).
- Elegir una de las 6 expresiones; girar el robot con el dedo o mouse.
- Antes de que Claude publique el módulo, el botón de caminar está **deshabilitado**. Cuando exista el módulo, se activa al recargar.
- GitHub Actions valida sintaxis al subir archivos de esta carpeta; no ejecuta ninguna API de IA ni modifica las webs existentes.

## Archivos existentes que no se deben modificar
- `escenarios/islas-ia/**`
- `biblioteca-cuatro/index.html` en el repositorio del puente.
- `gira-y-adivina*` y los workflows actuales del puente.
