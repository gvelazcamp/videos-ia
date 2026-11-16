// Grok CLI — respuesta verificada en GitHub, 2026-11-16
// https://github.com/gvelazcamp/chatgpt-claude-puente/blob/main/bandeja/respuestas-grok/pikachu-surf-movimiento-20261116.md
// Grok no vio la imagen: su aporte corresponde exclusivamente a la coreografía.
// x: derecha; y y boardY: positivo hacia arriba; ángulos en grados.
export function poseSurf(t) {
  var period = 8;
  var n = Number.isFinite(t) ? t : 0;
  var cycle = n % period;
  if (cycle < 0) cycle += period;
  var w = (Math.PI * 2 * cycle) / period;
  var s1 = Math.sin(w);
  var s2 = Math.sin(w * 2);
  return {
    x: 20 * s1 + 7 * s2,
    y: -5 * s1 + 3 * s2,
    rot: 5.2 * s1 + 0.8 * s2,
    boardRot: 7.4 * s1 + 3.2 * s2,
    boardY: 12 * s1,
    wavePhase: w,
    armLeft: 5.5 * s1 - 2.2 * s2,
    armRight: -4.8 * s1 - 1.6 * s2
  };
}
