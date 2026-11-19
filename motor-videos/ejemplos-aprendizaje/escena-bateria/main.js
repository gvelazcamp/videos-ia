// ===== Ejemplo didáctico: batería 100→0, puerta que se abre y reacción de Grok =====
// Se concatena así:  cat ../../base.js ../../islas.js ../../expresiones.js main.js > scene2.js
// Usa SOLO funciones del motor (makeBot, mesh, M, ISLA_IAS, brillo, ponerExpresion, iconoExpresion,
// clamp, ease, pop, rr, drawCaption) más tres funciones NUEVAS de este archivo: dibujarBateria, dibujarPuerta, armarTiempos.
// No usa imágenes: batería y puerta se dibujan en Canvas, así el ejemplo corre sin assets.
const ORDEN = ['chatgpt', 'claude', 'gemini', 'grok']; const B = {}; const HOME = {};
const POS = { chatgpt: [-1.18, 0, -.2], claude: [-.42, 0, -.72], gemini: [.42, 0, -.72], grok: [1.18, 0, -.2] };
function build() {
  hemi.intensity = 1.0; sun.intensity = 1.9; sun.position.set(-3, 9, 9); scene.add(new THREE.AmbientLight(0x8a90c8, .3));
  ORDEN.forEach(n => { const c = ISLA_IAS[n][1]; const g = new THREE.Group(); g.position.set(...POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(.38, .41, .08, 40), M(0x2a2950), [0, .04, 0], g);
    const aro = mesh(new THREE.TorusGeometry(.41, .022, 10, 56), new THREE.MeshBasicMaterial({ color: c }), [0, .07, 0], g, false); aro.rotation.x = Math.PI / 2;
    const b = makeBot(c); b.scale.setScalar(.95); b.position.set(0, .08, 0); g.add(b); B[n] = b; HOME[n] = g; g.rotation.y = -g.position.x * .18; });
}
// ---------- segmentos: el texto tiene que coincidir palabra por palabra con narracion.txt (los * no cuentan) ----------
const S_ = []; const seg = (text, o) => S_.push(Object.assign({ text }, o));
seg('¿Qué pasaría si *ChatGPT,* *Claude,* *Gemini* y *Grok* quedaran encerrados sin energía?', { fx: (lt, S) => { S.expr = 'pensando'; S.bateria = 1; } });
seg('La *energía* cayó hasta *cero* mientras la puerta seguía cerrada.', { fx: (lt, S, w) => {
  S.bateria = 1 - clamp((lt - w(1)) / (w(4) - w(1)));      // palabra 1 «energía» → palabra 4 «cero»
  S.expr = lt < w(4) ? 'pensando' : 'asustado'; } });
seg('Entonces la *puerta* se abrió y *Grok* gritó.', { fx: (lt, S, w) => {
  S.bateria = 0; S.puerta = ease(clamp((lt - w(2)) / .6));  // abre en 0,6 s desde «puerta»
  S.expr = 'asustado'; S.grokExpr = lt > w(5) ? 'sorprendido' : 'asustado'; } });
// ---------- tiempos: copiado del ejemplo del mate (NUEVO solo el nombre armarTiempos) ----------
let TOTAL = 0;
function armarTiempos() { const TM = window.TIMING; let wi = 0;
  S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
  S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
  TOTAL = TM.dur + 1.5; window.TOTAL = TOTAL;
  S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TOTAL; s.dur = s.t1 - s.t0; }); }
// ---------- NUEVO: batería y puerta en Canvas ----------
function dibujarBateria(x, y, p) { const w = 300, h = 110;
  rr(x - w / 2, y - h / 2, w, h, 18); ctx.fillStyle = 'rgba(10,10,24,.85)'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; ctx.stroke();
  rr(x + w / 2 + 4, y - 22, 16, 44, 5); ctx.fillStyle = '#fff'; ctx.fill();
  if (p > .005) { rr(x - w / 2 + 12, y - h / 2 + 12, (w - 24) * p, h - 24, 10); ctx.fillStyle = p > .5 ? '#3ddc6a' : p > .2 ? '#f2c230' : '#ef4b3c'; ctx.fill(); }
  ctx.fillStyle = '#fff'; ctx.font = '800 54px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(Math.round(p * 100) + ' %', x, y + 92); }
function dibujarPuerta(x, y, k) { const w = 300, h = 470;
  ctx.fillStyle = '#05060c'; ctx.fillRect(x - w / 2, y - h / 2, w, h);                      // vano oscuro
  if (k > 0) { const g = ctx.createLinearGradient(x, y - h / 2, x, y + h / 2); g.addColorStop(0, `rgba(255,236,170,${.9 * k})`); g.addColorStop(1, `rgba(255,190,90,${.5 * k})`); ctx.fillStyle = g; ctx.fillRect(x - w / 2, y - h / 2, w, h); }
  const hoja = w * (1 - .85 * k);                                                         // la hoja se achica = gira hacia adentro
  ctx.fillStyle = '#5a4a8a'; ctx.fillRect(x - w / 2, y - h / 2, hoja, h); ctx.strokeStyle = '#2a2350'; ctx.lineWidth = 8; ctx.strokeRect(x - w / 2, y - h / 2, w, h);
  ctx.fillStyle = '#ffd34d'; ctx.beginPath(); ctx.arc(x - w / 2 + hoja - 30, y, 12, 0, 7); ctx.fill(); }
// ---------- renderFrame: mismo esqueleto que el ejemplo del mate ----------
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  const S = {}; s.fx(lt, S, w);
  ORDEN.forEach((n, j) => ponerExpresion(B[n], n === 'grok' && S.grokExpr ? S.grokExpr : S.expr, T + j * .37, .08));
  const k = clamp(T / TOTAL); camera.position.set(Math.sin(T * .15) * .15, 2.6 - .2 * k, 7.9 - .7 * k); camera.fov = 38; camera.updateProjectionMatrix(); camera.lookAt(0, 1.5, 0); camera.updateMatrixWorld();
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#0b0b22'); g.addColorStop(1, '#1d1a4a'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (S.puerta !== undefined) dibujarPuerta(540, 700, S.puerta);       // detrás de los robots
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (S.bateria !== undefined && S.puerta === undefined) dibujarBateria(540, 660, S.bateria);
  ORDEN.forEach(n => iconoExpresion(B[n], n === 'grok' && S.grokExpr ? S.grokExpr : S.expr, T, .8));
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I'].map(f => document.fonts.load(f))).then(() => { build(); armarTiempos(); window.READY = true; });
