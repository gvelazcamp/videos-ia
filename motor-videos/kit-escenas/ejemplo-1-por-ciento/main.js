// ===== «1 %» (uno-por-ciento-20261120) — robots clásicos, escena hecha con código =====
const ORDEN = ['chatgpt', 'claude', 'gemini', 'grok']; const B = {}; const HOME = {};
const POS = { chatgpt: [-1.35, 0, .1], claude: [-.45, 0, -.25], gemini: [.45, 0, -.25], grok: [1.35, 0, .1] };
const EMO = '"Noto Color Emoji"';
const R2 = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(101);
const EDIF = Array.from({ length: 11 }, (_, i) => ({ x: -40 + i * 105 + R2() * 30, w: 90 + R2() * 70, h: 380 + R2() * 520, v: Array.from({ length: 40 }, () => R2()) }));
const ESTR = Array.from({ length: 90 }, () => [R2() * 1080, 120 + R2() * 700, R2() * 1.6 + .4, R2()]);
let CARG;
function build() {
  hemi.intensity = 1.0; hemi.color.set(0xb8c4ff); hemi.groundColor.set(0x1a1830); sun.intensity = 1.6; sun.position.set(-3, 9, 9); sun.target.position.set(0, 0, 0);
  scene.add(new THREE.AmbientLight(0x8a90c8, .3));
  ORDEN.forEach(n => { const c = ISLA_IAS[n][1]; const g = new THREE.Group(); g.position.set(...POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(.38, .41, .08, 40), M(0x2a2950), [0, .04, 0], g);
    const aro = mesh(new THREE.TorusGeometry(.41, .022, 10, 56), new THREE.MeshBasicMaterial({ color: c }), [0, .07, 0], g, false); aro.rotation.x = Math.PI / 2; g.userData.aro = aro;
    const b = makeBot(c); b.scale.setScalar(.95); b.position.set(0, .08, 0); g.add(b); B[n] = b; HOME[n] = g; g.rotation.y = -g.position.x * .18; });
  // cargador (código): caja gris con enchufe y luz
  CARG = new THREE.Group(); CARG.position.set(0, 0, -1.4); scene.add(CARG);
  mesh(new THREE.BoxGeometry(.55, .8, .3), M(0x4b5263, { metalness: .4, roughness: .5 }), [0, .4, 0], CARG);
  mesh(new THREE.BoxGeometry(.3, .18, .04), M(0x1b1e26), [0, .52, .17], CARG);
  const luz = mesh(new THREE.SphereGeometry(.045, 14, 10), new THREE.MeshBasicMaterial({ color: 0x3ddc6a }), [.18, .72, .16], CARG, false); CARG.userData.luz = luz;
}
// ---------- segmentos ----------
const S_ = []; const seg = (text, o) => S_.push(Object.assign({ text }, o));
seg('Apagón en toda la *ciudad.*', { fx: (lt, S, w) => { S.expr = 'sorprendido'; S.entrada = clamp(lt / 1.2); S.apagon = clamp(lt / .25); S.bat = 1; } });
seg('*ChatGPT,* *Claude,* *Gemini* y *Grok,* con la batería al *uno* *por* *ciento.*', { fx: (lt, S, w) => { S.expr = 'asustado'; S.bat = 1; S.batVer = clamp((lt - w(8)) / .3);
  S.luzIA = { chatgpt: lt > w(0) && lt < w(1) + .4, claude: lt > w(1) && lt < w(2) + .4, gemini: lt > w(2) && lt < w(4) + .4, grok: lt > w(4) && lt < w(5) + .5 }; } });
seg('Y un solo *cargador* con energía.', { fx: (lt, S, w) => { S.expr = 'sorprendido'; S.bat = 1; S.batVer = 1; S.cargador = clamp((lt - w(3)) / .3); } });
seg('*ChatGPT* propuso *votar.*', { fx: (lt, S, w) => { S.expr = 'pensando'; S.cara = { chatgpt: 'contento' }; S.bat = 1; S.batVer = 1; S.cargador = 1; S.icono = ['chatgpt', '🗳️', clamp((lt - w(2)) / .3)]; S.luzIA = { chatgpt: 1 }; } });
seg('*Claude* calculó quién rendía *más.*', { fx: (lt, S, w) => { S.expr = 'pensando'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.icono = ['claude', '🧮', clamp((lt - w(1)) / .3)]; S.luzIA = { claude: 1 }; } });
seg('*Gemini* buscó otra *fuente.*', { fx: (lt, S, w) => { S.expr = 'pensando'; S.cara = { gemini: 'sorprendido' }; S.bat = 1; S.batVer = 1; S.cargador = 1; S.icono = ['gemini', '🔦', clamp((lt - w(1)) / .3)]; S.luzIA = { gemini: 1 }; S.gemMira = clamp(lt / .8); } });
seg('Y *Grok* intentó enchufarse a *escondidas.*', { fx: (lt, S, w) => { S.expr = 'sorprendido'; S.cara = { grok: 'contento' }; S.bat = 1; S.batVer = 1; S.cargador = 1; S.grokVa = clamp((lt - w(1)) / 1.4); S.luzIA = { grok: 1 }; } });
seg('Pero *Gemini* vio adónde iba el *cable:* al único *semáforo* que seguía andando.', { fx: (lt, S, w) => { S.expr = 'sorprendido'; S.cara = { gemini: 'sorprendido', grok: 'asustado' }; S.bat = 1; S.batVer = 1; S.cargador = 1;
  S.grokVa = 1 - clamp((lt - w(1)) / .8); S.cable = clamp((lt - w(6)) / (w(10) - w(6))); S.semaforo = clamp((lt - w(10)) / .3); S.luzIA = { gemini: 1 }; } });
seg('En la esquina, una *perra* y su *cachorro* esperaban para cruzar.', { fx: (lt, S, w) => { S.expr = 'triste'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.perros = clamp((lt - w(4)) / .35); S.zoomEsq = clamp(lt / .6); } });
seg('Si uno de ellos se cargaba, el semáforo se *apagaba.*', { fx: (lt, S, w) => { S.expr = 'asustado'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.perros = 1; S.amenaza = clamp((lt - w(8)) / .3); } });
seg('Se *miraron.*', { fx: (lt, S, w) => { S.expr = 'pensando'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.perros = 1; S.miran = clamp(lt / .5); } });
seg('*Nadie* se enchufó.', { fx: (lt, S, w) => { S.expr = 'contento'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.perros = 1; S.miran = 1 - clamp(lt / .6); } });
seg('Se quedaron en *reposo,* *juntos,* en la oscuridad.', { fx: (lt, S, w) => { S.expr = 'triste'; S.bat = 1; S.batVer = 1; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.perros = 1; S.reposo = clamp((lt - w(3)) / .8); } });
seg('El semáforo se puso en *verde,* y los perros *cruzaron.*', { fx: (lt, S, w) => { S.expr = 'triste'; S.reposo = 1; S.bat = 1; S.batVer = .6; S.cargador = 1; S.cable = 1; S.semaforo = 1; S.verde = clamp((lt - w(5)) / .2); S.perros = 1; S.cruce = clamp((lt - w(9)) / 1.6); S.zoomEsq = 1; } });
seg('A la *mañana* volvió la *luz.*', { fx: (lt, S, w) => { S.expr = 'triste'; S.reposo = 1; S.bat = 1; S.batVer = .6; S.manana = clamp((lt - w(2) + .2) / .9); S.luzCiudad = clamp((lt - w(5)) / .4); S.cruce = 1; S.perros = 1; S.verde = 1; S.semaforo = 1; } });
seg('Un *operario* los conectó, y las baterías empezaron a *subir.*', { fx: (lt, S, w) => { S.expr = lt > w(9) ? 'contento' : 'triste'; S.reposo = 1 - clamp((lt - w(9)) / .6); S.manana = 1; S.luzCiudad = 1; S.regleta = clamp((lt - w(1)) / .4); S.batVer = 1; S.bat = 1 + 39 * clamp((lt - w(9)) / 2.2); S.semaforo = 1; S.verde = 1; S.cruce = 1; S.perros = 1; } });
seg('Hay *cargas* que no se miden en *porcentaje.*', { fx: (lt, S, w) => { S.expr = 'festejando'; S.manana = 1; S.luzCiudad = 1; S.regleta = 1; S.batVer = 1; S.bat = 40 + 20 * clamp(lt / 3); S.semaforo = 1; S.verde = 1; S.cruce = 1; S.perros = 1; S.fin = clamp((lt - w(7) - .3) / .4); } });
// ---------- tiempos ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
const TOTAL = TM.dur + 2.4; window.TOTAL = TOTAL;
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TOTAL; s.dur = s.t1 - s.t0; });
// ---------- dibujo 2D ----------
const SEMX = 905, SEMY = 860;
function glow(x, y, r, col, a) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); }
function cabeza(n) { return proj(B[n].userData.head.localToWorld(V(0, .55, 0))); }
function emoji(e, x, y, size, k) { const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.font = `${size}px ${EMO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(e, 0, 0); ctx.restore(); }
function cartel(txt, x, y, k, col, size) { const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.font = `800 ${size}px I`; const w = ctx.measureText(txt).width + 60; rr(-w / 2, -size * .8, w, size * 1.6, 26); ctx.fillStyle = 'rgba(8,10,20,.88)'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.stroke(); ctx.fillStyle = col; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(txt, 0, 4); ctx.restore(); }
function bateria(x, y, p, a, T) { if (a <= 0) return; const blink = p < 5 ? (.55 + .45 * Math.sin(T * 6)) : 1; ctx.save(); ctx.globalAlpha = a * blink; const w = 120, h = 50;
  rr(x - w / 2, y - h / 2, w, h, 9); ctx.fillStyle = 'rgba(8,10,20,.85)'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.stroke(); rr(x + w / 2 + 2, y - 8, 7, 16, 3); ctx.fillStyle = '#fff'; ctx.fill();
  const f = Math.max(.04, p / 100); rr(x - w / 2 + 6, y - h / 2 + 6, (w - 12) * f, h - 12, 5); ctx.fillStyle = p < 10 ? '#ef4b3c' : p < 50 ? '#f2c230' : '#3ddc6a'; ctx.fill();
  ctx.font = '800 38px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#fff'; ctx.fillText(Math.round(p) + ' %', x, y + 54); ctx.restore(); }
function ciudad(T, S) { const m = S.manana || 0;
  const g = ctx.createLinearGradient(0, 0, 0, H * .75); g.addColorStop(0, m ? `rgb(${30 + 225 * m | 0},${30 + 150 * m | 0},${70 + 80 * m | 0})` : '#05060f'); g.addColorStop(1, m ? `rgb(${60 + 190 * m | 0},${40 + 150 * m | 0},${60 + 40 * m | 0})` : '#12142a'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (m < 1) for (const [x, y, r, a] of ESTR) { ctx.globalAlpha = (1 - m) * (.3 + .6 * a * (.6 + .4 * Math.sin(T * 2 + a * 9))); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
  if (m > 0) glow(780, 900, 380 * m, 'rgba(255,200,120,A)', .7 * m);
  const base = 1180; for (const e of EDIF) { ctx.fillStyle = m ? `rgb(${20 + 60 * m | 0},${20 + 40 * m | 0},${40 + 30 * m | 0})` : '#1a1f3d'; ctx.fillRect(e.x, base - e.h, e.w, e.h);
    let k = 0; for (let yy = base - e.h + 24; yy < base - 40; yy += 46) for (let xx = e.x + 14; xx < e.x + e.w - 20; xx += 30) { const v = e.v[k++ % 40]; const on = S.apagon !== undefined ? (1 - S.apagon) : 0; const lc = Math.max(on, (S.luzCiudad || 0)); if (v > .45 && lc > 0) { ctx.fillStyle = `rgba(255,214,120,${.85 * lc})`; ctx.fillRect(xx, yy, 14, 20); } } }
  ctx.fillStyle = m ? `rgb(${30 + 40 * m | 0},${30 + 30 * m | 0},${45 + 20 * m | 0})` : '#0c0d18'; ctx.fillRect(0, base, W, H - base);
  // cebra peatonal
  ctx.fillStyle = `rgba(230,230,240,${.25 + .35 * m})`; for (let i = 0; i < 9; i++) ctx.fillRect(420 + i * 72, 1640, 42, 120); }
function semaforo(T, S) { const a = S.semaforo || 0; if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const x = SEMX, y = SEMY;
  ctx.fillStyle = '#2b2f38'; ctx.fillRect(x - 8, y, 16, 400); rr(x - 46, y - 210, 92, 220, 18); ctx.fillStyle = '#1b1e26'; ctx.fill();
  const verde = S.verde || 0; const amen = S.amenaza ? (Math.sin(T * 14) > 0 ? .25 : 1) : 1;
  // autos: rojo cuando el peatón tiene verde
  ctx.beginPath(); ctx.arc(x, y - 160, 30, 0, 7); ctx.fillStyle = verde ? `rgba(255,60,50,${amen})` : '#3a1414'; ctx.fill(); if (verde) glow(x, y - 160, 70, 'rgba(255,60,50,A)', .5);
  ctx.beginPath(); ctx.arc(x, y - 60, 30, 0, 7); ctx.fillStyle = verde ? '#123a1c' : `rgba(60,220,110,${amen})`; ctx.fill(); if (!verde) glow(x, y - 60, 70, 'rgba(60,220,110,A)', .5 * amen);
  // peatón
  rr(x - 40, y + 30, 80, 90, 12); ctx.fillStyle = '#1b1e26'; ctx.fill(); ctx.font = `56px ${EMO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.globalAlpha = a * (verde ? 1 : .35); ctx.fillText(verde ? '🚶' : '🧍', x, y + 76); ctx.restore(); }
function cable(S, T) { const k = S.cable || 0; if (k <= 0) return; const [cx, cy] = proj(CARG.localToWorld(V(.25, .2, 0))); const pts = [[cx, cy], [cx + 120, cy + 60], [SEMX - 60, cy + 40], [SEMX, SEMY + 380]];
  ctx.save(); ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.strokeStyle = '#111'; ctx.beginPath(); ctx.moveTo(...pts[0]); ctx.bezierCurveTo(...pts[1], ...pts[2], ...pts[3]); ctx.stroke();
  ctx.setLineDash([24, 26]); ctx.lineDashOffset = -T * 120; ctx.strokeStyle = `rgba(255,230,90,${.9 * k})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(...pts[0]); ctx.bezierCurveTo(...pts[1], ...pts[2], ...pts[3]); ctx.stroke(); ctx.restore(); }
function perros(S, T) { const a = S.perros || 0; if (a <= 0) return; const c = ease(S.cruce || 0); const x = 1000 - c * 640, y = 1690 + Math.sin(c * 30) * 4 * (c > 0 && c < 1);
  emoji('🐕', x - 40, y, 170, a); emoji('🐶', x - 170, y + 30, 105, clamp(a * 1.5 - .3)); }
function regleta(S) { const k = S.regleta || 0; if (k <= 0) return; const s = pop(k); ctx.save(); ctx.translate(540, 1530); ctx.scale(s, s); rr(-300, -30, 600, 60, 16); ctx.fillStyle = '#e8e8ee'; ctx.fill(); ctx.strokeStyle = '#9aa0ad'; ctx.lineWidth = 4; ctx.stroke();
  for (let i = 0; i < 4; i++) { rr(-240 + i * 150, -16, 60, 32, 8); ctx.fillStyle = '#3a3d48'; ctx.fill(); } ctx.beginPath(); ctx.arc(250, 0, 12, 0, 7); ctx.fillStyle = '#ef4b3c'; ctx.fill(); ctx.restore();
  ORDEN.forEach((n, i) => { const [x, y] = proj(HOME[n].localToWorld(V(0, .05, 0))); ctx.strokeStyle = `rgba(30,30,40,${k})`; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x, 1530, 330 - 30 + i * 150 - 30 + 30, 1530); ctx.stroke(); }); }
// ---------- cuadro ----------
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  const S = {}; s.fx(lt, S, w);
  ORDEN.forEach((n, j) => { const g = HOME[n], b = B[n]; const e = (S.cara && S.cara[n]) || S.expr;
    ponerExpresion(b, e, T + j * .37, .08);
    const ent = i === 0 ? ease(clamp((S.entrada || 0) * 1.6 - j * .2)) : 1; b.position.y = .08 + (1 - ent) * 3.2; b.visible = ent > 0;
    g.position.set(...POS[n]); g.rotation.y = -g.position.x * .18;
    if (S.miran) g.rotation.y = lerp(-g.position.x * .18, -Math.sign(g.position.x) * 1.0, S.miran);
    if (S.reposo) { b.position.y = .08 - .06 * S.reposo; b.rotation.x = .22 * S.reposo; } else b.rotation.x = 0;
    g.userData.aro.material.color.set(ISLA_IAS[n][1]).multiplyScalar(S.luzIA && S.luzIA[n] ? 1 : .45); });
  if (S.grokVa) { const k = ease(S.grokVa); HOME.grok.position.x = 1.35 - 1.0 * k; HOME.grok.position.z = .1 - 1.1 * k; HOME.grok.rotation.y = -1.2 * k; }
  if (S.gemMira) HOME.gemini.rotation.y = -.4 - .8 * Math.sin(S.gemMira * Math.PI);
  CARG.visible = (S.cargador || 0) > 0; CARG.userData.luz.material.color.set(Math.sin(T * 5) > 0 ? 0x3ddc6a : 0x1a5a2a);
  const k = clamp(T / TOTAL); const z = S.zoomEsq ? ease(Math.min(1, S.zoomEsq)) : 0;
  camera.position.set(Math.sin(T * .35) * .3 + .15 + .3 * z, 3.0 - .15 * k + Math.sin(T * .5) * .08, 9.4 - .9 * k); camera.fov = 40; camera.updateProjectionMatrix(); camera.lookAt(.15 + .3 * z, 1.95, 0); camera.updateMatrixWorld();
  ciudad(T, S);
  const osc = (S.apagon ? .25 : 0) + (S.reposo || 0) * .35 * (1 - (S.manana || 0)); 
  semaforo(T, S);
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  cable(S, T); regleta(S);
  if (osc > 0) { ctx.fillStyle = `rgba(2,3,12,${osc})`; ctx.fillRect(0, 0, W, H); }
  if (S.perros) { const c = ease(S.cruce || 0); glow(1060 - c * 640, 1720, 230, 'rgba(255,214,140,A)', .35 * (1 - (S.manana || 0)) * S.perros); }
  perros(S, T); // después de la oscuridad: los perros se ven con su color
  if (S.batVer) ORDEN.forEach(n => { const [x, y] = cabeza(n); bateria(x, y - 70, S.bat || 1, S.batVer, T); });
  if (S.cargador && i === 2) { const [x, y] = proj(CARG.localToWorld(V(0, 1.0, 0))); cartel('⚡ 1 CARGADOR', x, y - 30, S.cargador, '#ffd34d', 54); }
  if (S.icono) { const [n, e, kk] = S.icono; const [x, y] = cabeza(n); emoji(e, x, y - 140, 100, kk); }
  if (S.amenaza) cartel('⚠ SI SE CARGA, SE APAGA', 540, 640, S.amenaza, '#ff6b5a', 52);
  ORDEN.forEach(n => { if (B[n].visible && B[n].position.y < .5 && !S.reposo) iconoExpresion(B[n], (S.cara && S.cara[n]) || S.expr, T, .8); });
  if (S.fin) { cartel('1 %', 540, 1540, S.fin, '#ffd34d', 120); }
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .6)) / .6); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
const lerp = (a, b, t) => a + (b - a) * t;
Promise.all(['500 40px I', '700 40px I', '800 40px I', `80px ${EMO}`].map(f => document.fonts.load(f))).then(() => { build(); window.READY = true; });
