// ===== kit-escenas.js — piezas reutilizables para videos con los robots de siempre (sin FLUX) =====
// Se concatena DESPUÉS de base.js, islas.js y expresiones.js y ANTES del main.js del video:
//   cat ../base.js ../islas.js ../expresiones.js kit.js main.js > scene2.js
// Requiere en el main.js: B (robots por nombre) y, si se usa cable(), un objeto 3D de origen.
const EMO = '"Noto Color Emoji"';
const lerp = (a, b, t) => a + (b - a) * t;
// halo de luz suave: glow(x, y, radio, 'rgba(r,g,b,A)', alfa)
function glow(x, y, r, col, a) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); }
// punto de pantalla arriba de la cabeza de un robot
function cabeza(n) { return proj(B[n].userData.head.localToWorld(V(0, .55, 0))); }
// emoji que aparece con rebote (k: 0→1)
function emoji(e, x, y, size, k) { const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.font = `${size}px ${EMO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(e, 0, 0); ctx.restore(); }
// cartel con borde de color: cartel('⏱ 3:00', 540, 560, k, '#ff6b5a', 80)
function cartel(txt, x, y, k, col, size) { const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.font = `800 ${size}px I`; const w = ctx.measureText(txt).width + 60; rr(-w / 2, -size * .8, w, size * 1.6, 26); ctx.fillStyle = 'rgba(8,10,20,.88)'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.stroke(); ctx.fillStyle = col; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(txt, 0, 4); ctx.restore(); }
// batería con porcentaje (titila si < 5 %): bateria(x, y, porcentaje, alfa, T)
function bateria(x, y, p, a, T) { if (a <= 0) return; const blink = p < 5 ? (.55 + .45 * Math.sin(T * 6)) : 1; ctx.save(); ctx.globalAlpha = a * blink; const w = 120, h = 50;
  rr(x - w / 2, y - h / 2, w, h, 9); ctx.fillStyle = 'rgba(8,10,20,.85)'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.stroke(); rr(x + w / 2 + 2, y - 8, 7, 16, 3); ctx.fillStyle = '#fff'; ctx.fill();
  const f = Math.max(.04, p / 100); rr(x - w / 2 + 6, y - h / 2 + 6, (w - 12) * f, h - 12, 5); ctx.fillStyle = p < 10 ? '#ef4b3c' : p < 50 ? '#f2c230' : '#3ddc6a'; ctx.fill();
  ctx.font = '800 38px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#fff'; ctx.fillText(Math.round(p) + ' %', x, y + 54); ctx.restore(); }
// semáforo con peatón: semaforo(x, y, alfa, verdePeaton 0/1, parpadeo, T)
function semaforo(x, y, a, verde, parpadea, T) { if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const amen = parpadea ? (Math.sin(T * 14) > 0 ? .25 : 1) : 1;
  ctx.fillStyle = '#2b2f38'; ctx.fillRect(x - 8, y, 16, 400); rr(x - 46, y - 210, 92, 220, 18); ctx.fillStyle = '#1b1e26'; ctx.fill();
  ctx.beginPath(); ctx.arc(x, y - 160, 30, 0, 7); ctx.fillStyle = verde ? `rgba(255,60,50,${amen})` : '#3a1414'; ctx.fill(); if (verde) glow(x, y - 160, 70, 'rgba(255,60,50,A)', .5);
  ctx.beginPath(); ctx.arc(x, y - 60, 30, 0, 7); ctx.fillStyle = verde ? '#123a1c' : `rgba(60,220,110,${amen})`; ctx.fill(); if (!verde) glow(x, y - 60, 70, 'rgba(60,220,110,A)', .5 * amen);
  rr(x - 40, y + 30, 80, 90, 12); ctx.fillStyle = '#1b1e26'; ctx.fill(); ctx.font = `56px ${EMO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.globalAlpha = a * (verde ? 1 : .35); ctx.fillText(verde ? '🚶' : '🧍', x, y + 76); ctx.restore(); }
// cable con energía que corre (línea punteada animada) entre dos puntos de pantalla
function cableEnergia(x0, y0, x1, y1, k, T) { if (k <= 0) return; ctx.save(); ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.strokeStyle = '#111'; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.bezierCurveTo(x0 + 120, y0 + 60, x1 - 60, y0 + 40, x1, y1); ctx.stroke();
  ctx.setLineDash([24, 26]); ctx.lineDashOffset = -T * 120; ctx.strokeStyle = `rgba(255,230,90,${.9 * k})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.bezierCurveTo(x0 + 120, y0 + 60, x1 - 60, y0 + 40, x1, y1); ctx.stroke(); ctx.restore(); }
// lluvia por delante (llamar después del 3D): lluvia(T, intensidad 0..1)
const _LL = (s => Array.from({ length: 170 }, () => { s = (s * 16807) % 2147483647; const a = s / 2147483647; s = (s * 16807) % 2147483647; const b = s / 2147483647; return [a * 1200, b * 1920, 18 + a * 26, .6 + b * .8]; }))(77);
function lluvia(T, k) { if (k <= 0) return; ctx.save(); ctx.strokeStyle = `rgba(190,215,255,${.33 * k})`; ctx.lineWidth = 2; ctx.beginPath(); for (const [x, y, l, v] of _LL) { const yy = (y + T * 1400 * v) % 2000 - 40, xx = (x - T * 260 * v) % 1200; ctx.moveTo(xx, yy); ctx.lineTo(xx - l * .25, yy + l); } ctx.stroke(); ctx.restore(); }
// oscurecer toda la pantalla (apagón, reposo): oscuro(0..1)
function oscuro(k) { if (k > 0) { ctx.fillStyle = `rgba(2,3,12,${k})`; ctx.fillRect(0, 0, W, H); } }
// alarma roja que late en los bordes
function alarma(T, k) { if (k <= 0) return; const p = (.5 + .5 * Math.sin(T * 7)) * k; const g = ctx.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .75); g.addColorStop(0, 'rgba(255,40,40,0)'); g.addColorStop(1, `rgba(255,40,40,${.4 * p})`); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
// franja oscura para los subtítulos (llamar justo antes de drawCaption)
function franjaSubtitulos() { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
