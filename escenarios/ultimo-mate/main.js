// ===== El último mate del universo (ultimo-mate-20261116) =====
const ORDEN = ['chatgpt', 'claude', 'gemini', 'grok']; const B = {}; const HOME = {}; const IMG = {};
const POS = { chatgpt: [-1.18, 0, -.2], claude: [-.42, 0, -.72], gemini: [.42, 0, -.72], grok: [1.18, 0, -.2] };
const NOMBRES = ['portada', 'fondo-atras', 'fondo-medio', 'fondo-frente', 'obj-mate', 'obj-mate-diagonal', 'obj-termo', 'obj-termo-diagonal', 'obj-nota', 'obj-reloj-2359', 'obj-reloj-0000', 'obj-pantalla', 'obj-mapa-luces'];
const cargar = n => new Promise(r => { const i = new Image(); i.onload = () => { IMG[n] = i; r(); }; i.src = 'img/ultimo-mate-' + n + '.webp'; });
const R2 = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(2026);
const PUNTOS = Array.from({ length: 140 }, () => [R2(), R2(), R2()]);
const POLVO = Array.from({ length: 40 }, () => [R2() * 1080, R2() * 1920, R2() * 2 + 1, R2()]);
let mesaTop;
function build() {
  hemi.intensity = 1.0; hemi.color.set(0xb8c4ff); hemi.groundColor.set(0x1a1830); sun.intensity = 1.9; sun.position.set(-3, 9, 9); sun.target.position.set(0, 0, 0);
  scene.add(new THREE.AmbientLight(0x8a90c8, .3));
  const fill = new THREE.PointLight(0x5ec8ff, 6, 9); fill.position.set(0, 3.2, 1.5); scene.add(fill);
  // mesa redonda
  const mesa = new THREE.Group(); mesa.position.set(0, 0, .7); scene.add(mesa);
  mesh(new THREE.CylinderGeometry(.14, .2, .46, 24), M(0x34336a, { roughness: .5, metalness: .4 }), [0, .23, 0], mesa);
  mesh(new THREE.CylinderGeometry(.66, .63, .07, 56), M(0x4b4a86, { roughness: .45, metalness: .3 }), [0, .49, 0], mesa);
  const aroM = mesh(new THREE.TorusGeometry(.66, .018, 10, 80), new THREE.MeshBasicMaterial({ color: 0x5ec8ff }), [0, .52, 0], mesa, false); aroM.rotation.x = Math.PI / 2;
  mesaTop = .53;
  ORDEN.forEach(n => { const c = ISLA_IAS[n][1]; const g = new THREE.Group(); g.position.set(...POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(.38, .41, .08, 40), M(0x2a2950), [0, .04, 0], g);
    const aro = mesh(new THREE.TorusGeometry(.41, .022, 10, 56), new THREE.MeshBasicMaterial({ color: c }), [0, .07, 0], g, false); aro.rotation.x = Math.PI / 2;
    const halo = mesh(new THREE.PlaneGeometry(1.25, 1.25), new THREE.MeshBasicMaterial({ map: brillo(c), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }), [0, .015, 0], g, false); halo.rotation.x = -Math.PI / 2;
    const b = makeBot(c); b.scale.setScalar(.95); b.position.set(0, .08, 0); g.add(b); B[n] = b; HOME[n] = g;
    g.rotation.y = -g.position.x * .18; });
}
// ---------- segmentos ----------
const S_ = []; const seg = (text, o) => S_.push(Object.assign({ text }, o));
seg('¿Qué pasaría si cuatro robots encontraran el *último* *mate* del *universo?*', { fx: (lt, S) => { S.cover = 1 - clamp((lt - .75) / .3); S.entrada = clamp((lt - .9) / 1.4); S.expr = 'sorprendido'; S.mate = 1; S.luz = .55; } });
seg('En una estación espacial abandonada, al lado del mate, había una nota: «No lo *cebes* después de *medianoche».*', { fx: (lt, S, w) => { S.expr = 'pensando'; S.mate = 1; S.nota = clamp((lt - w(9) + .2) / .35); S.luz = .55; } });
seg('El reloj marcaba las *once* y *cincuenta* y *nueve.*', { fx: (lt, S) => { S.expr = 'pensando'; S.mate = 1; S.notaChica = 1; S.reloj = clamp(lt / .3); S.luz = .5; } });
seg('*Grok* no aguantó la curiosidad. *Cebó.*', { fx: (lt, S, w, p) => { S.expr = 'asustado'; S.grokExpr = 'contento'; S.mate = 1; S.notaChica = 1; S.reloj = 1; S.grokVa = clamp(lt / .9); S.ceba = clamp((lt - w(5) + .3) / .5); S.luz = .5; S.cero = lt > w(5) + .25; } });
seg('Y justo a la *medianoche,* se prendió una *transmisión:* «Si estás *cebando,* no estás *solo».*', { fx: (lt, S, w) => { S.expr = lt < w(3) ? 'asustado' : 'sorprendido'; S.mate = 1; S.notaChica = 1; S.reloj = 1; S.cero = true; S.grokVa = 1; S.flash = clamp(1 - lt / .35); S.pantalla = clamp((lt - w(5) + .2) / .35); S.msgPant = clamp((lt - w(7)) / .25); S.luz = .9; } });
seg('En el mapa se encendieron *miles* de *estaciones,* todas con un mate en la mano.', { fx: (lt, S, w) => { S.expr = lt < w(4) ? 'sorprendido' : 'festejando'; S.mate = 1; S.grokVa = 1 - clamp(lt / .8); S.mapa = clamp(lt / .35); S.puntos = clamp((lt - w(3)) / 1.6); S.luz = 1; } });
seg('Porque, hasta en el fin del universo, un mate nunca se toma *solo.*', { fx: (lt, S, w, p, T) => { S.expr = 'contento'; S.ronda = T; S.luz = 1; S.fin = clamp((lt - w(11) - .4) / .4); } });
// ---------- timing ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
const TOTAL = Math.max(TM.dur + 3.2, 40); window.TOTAL = TOTAL;
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TOTAL; s.dur = s.t1 - s.t0; });
// ---------- dibujo 2D ----------
function img(n, x, y, w, a = 1, rot = 0) { const i = IMG[n]; if (!i || a <= 0) return; const h = w * i.height / i.width; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot); ctx.drawImage(i, -w / 2, -h / 2, w, h); ctx.restore(); }
function capa(n, z, dy = 0) { const i = IMG[n]; if (!i) return; const w = W * z, h = H * z; ctx.drawImage(i, (W - w) / 2, (H - h) / 2 + dy, w, h); }
function enMesa(x, z, y = 0) { return proj(V(x, mesaTop + y, .7 + z)); }
function manoDe(n) { const b = B[n]; const p = b.userData.arms[1].localToWorld(V(.12, -.3, .1)); return proj(p); }
function glow(x, y, r, col, a) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); }
function cartelFin(k) { const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(W / 2, 690); ctx.scale(s, s);
  ctx.font = '800 64px I'; const w = 860, h = 230; rr(-w / 2, -h / 2, w, h, 40); ctx.fillStyle = 'rgba(10,10,30,.88)'; ctx.fill(); ctx.strokeStyle = '#5ec8ff'; ctx.lineWidth = 6; ctx.shadowColor = '#5ec8ff'; ctx.shadowBlur = 30; ctx.stroke(); ctx.shadowBlur = 0;
  ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('EL ÚLTIMO MATE', 0, -42); ctx.fillStyle = '#ffd34d'; ctx.fillText('DEL UNIVERSO', 0, 42); ctx.restore(); }
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, p = clamp(lt / s.dur), w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  const S = {}; s.fx(lt, S, w, p, T);
  // robots
  ORDEN.forEach((n, j) => { const g = HOME[n]; const b = B[n]; const e = n === 'grok' && S.grokExpr ? S.grokExpr : S.expr;
    ponerExpresion(b, e, T + j * .37, .08);
    const ent = i === 0 ? ease(clamp(S.entrada * 1.6 - j * .2)) : 1; b.position.y = .08 + (1 - ent) * 3.2; b.visible = ent > 0;
    g.position.set(...POS[n]); });
  if (S.grokVa) { const k = ease(S.grokVa); HOME.grok.position.x = 1.18 - .33 * k; HOME.grok.position.z = -.2 + .25 * k; }
  if (S.ceba) { const a1 = B.grok.userData.arms[1]; a1.rotation.set(-1.4, 0, .9 + .3 * Math.sin(T * 6)); }
  if (S.ronda !== undefined) { ORDEN.forEach(n => { const a1 = B[n].userData.arms[1]; }); }
  // cámara (empuje lento)
  const k = clamp(T / TOTAL); camera.position.set(Math.sin(T * .15) * .15, 2.6 - .2 * k, 7.9 - .7 * k); camera.fov = 38; camera.updateProjectionMatrix(); camera.lookAt(0, 1.5, 0); camera.updateMatrixWorld();
  // fondo en capas (parallax)
  ctx.fillStyle = '#05060c'; ctx.fillRect(0, 0, W, H);
  capa('fondo-atras', 1.02 + .05 * k, -10 * k);
  if (S.mapa) { ctx.globalAlpha = S.mapa * .55; ctx.fillStyle = '#0a1030'; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }
  capa('fondo-medio', 1.03 + .08 * k, 0);
  const parp = S.luz < .8 ? (Math.sin(T * 17) > .85 ? .25 : 0) : 0; const osc = clamp(1 - S.luz + parp, 0, .7); if (osc > 0) { ctx.fillStyle = `rgba(2,3,10,${osc * .7})`; ctx.fillRect(0, 0, W, H); }
  // pantalla (transmisión) sobre la ventana
  if (S.pantalla) { const s2 = pop(S.pantalla); const fl = Math.sin(T * 40) > .3 ? 1 : .8; glow(540, 590, 420, 'rgba(94,200,255,A)', .45 * S.pantalla); img('obj-pantalla', 540, 590, 760 * s2, fl);
    if (S.msgPant) { ctx.save(); ctx.globalAlpha = S.msgPant; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#e8fbff'; ctx.shadowColor = '#5ec8ff'; ctx.shadowBlur = 18; ctx.font = '800 50px I'; ctx.fillText('SI ESTÁS CEBANDO,', 540, 668); ctx.fillStyle = '#ffd34d'; ctx.fillText('NO ESTÁS SOLO', 540, 730); ctx.restore(); } }
  // mapa con luces
  if (S.mapa) { const s2 = pop(S.mapa); img('obj-mapa-luces', 540, 610, 800 * s2); const n = Math.floor(S.puntos * PUNTOS.length);
    for (let q = 0; q < n; q++) { const [px, py, pr] = PUNTOS[q]; const x = 540 + (px - .5) * 560 * s2, y = 610 + (py - .5) * 400 * s2; const tw = .6 + .4 * Math.sin(T * 6 + q); glow(x, y, 14 + pr * 10, 'rgba(255,211,77,A)', .9 * tw); ctx.fillStyle = '#fff6c8'; ctx.beginPath(); ctx.arc(x, y, 3 + pr * 2, 0, 7); ctx.fill(); } }
  // 3D
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  // objetos sobre la mesa
  const [mx, my] = enMesa(-.12, .2); const [tx, ty] = enMesa(.28, .05); const [nx, ny] = enMesa(-.42, .25);
  if (S.notaChica || S.nota >= 1) img('obj-nota', nx, ny - 20, 110, 1, -.15);
  if (S.ronda !== undefined) {
    const per = 1.15, idx = Math.floor((T - s.t0) / per), f = ((T - s.t0) % per) / per; const a = manoDe(ORDEN[idx % 4]), b = manoDe(ORDEN[(idx + 1) % 4]); const e = ease(clamp(f * 1.8 - .5));
    const x = a[0] + (b[0] - a[0]) * e, y = a[1] + (b[1] - a[1]) * e - Math.sin(e * Math.PI) * 90; glow(x, y, 120, 'rgba(255,190,90,A)', .35); img('obj-mate', x, y, 140, 1, Math.sin(T * 3) * .1);
    img('obj-termo', tx, ty - 55, 115);
  } else if (S.mate) {
    if (S.ceba) { const [gx, gy] = manoDe('grok'); const tk = ease(S.ceba); const x = tx + (mx + 60 - tx) * tk, y = ty - 55 + (my - 140 - (ty - 55)) * tk; img('obj-termo-diagonal', x, y, 140, 1, -.3 * tk);
      if (tk > .6) { ctx.strokeStyle = 'rgba(190,230,255,.85)'; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x - 70, y + 10); ctx.quadraticCurveTo(mx - 10, my - 150, mx, my - 85); ctx.stroke(); for (let q = 0; q < 3; q++) { const st = (T * .8 + q / 3) % 1; ctx.globalAlpha = (1 - st) * .6; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(mx + Math.sin(T * 4 + q) * 12, my - 110 - st * 90, 10 + st * 12, 0, 7); ctx.fill(); ctx.globalAlpha = 1; } } }
    else img('obj-termo', tx, ty - 55, 115);
    glow(mx, my - 40, 120, 'rgba(255,190,90,A)', .3 + .1 * Math.sin(T * 3)); img('obj-mate', mx, my - 55, 140);
  }
  // nota grande
  if (S.nota && !S.notaChica) { const s2 = pop(S.nota); img('obj-nota', 540, 720, 620 * s2, 1, -.06); }
  // reloj
  if (S.reloj) { const s2 = pop(S.reloj); const chico = S.cero && lt > 1.2 || S.pantalla; const [qx, qy] = enMesa(.5, -.25); const big = chico ? .3 : 1; const rx = chico ? qx : 540, ry = chico ? qy - 40 : 720; if (S.cero) glow(rx, ry, 260 * big, 'rgba(255,60,60,A)', .5 + .3 * Math.sin(T * 10)); img(S.cero ? 'obj-reloj-0000' : 'obj-reloj-2359', rx, ry, 640 * big * s2); }
  if (S.flash) { ctx.fillStyle = `rgba(255,255,255,${S.flash * .7})`; ctx.fillRect(0, 0, W, H); }
  // capa frente + polvo
  capa('fondo-frente', 1.04 + .1 * k, 0);
  for (const [x, y, r, a] of POLVO) { ctx.globalAlpha = .25 + .3 * a; ctx.fillStyle = '#cfe8ff'; ctx.beginPath(); ctx.arc(x + Math.sin(T * .5 + a * 9) * 20, (y - T * 18 * (a + .3) + 1920) % 1920, r, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
  // iconos de expresiones
  ORDEN.forEach(n => { if (B[n].position.y < .5) iconoExpresion(B[n], n === 'grok' && S.grokExpr ? S.grokExpr : S.expr, T, .8); });
  if (S.fin) cartelFin(S.fin);
  // franja de subtítulos
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  if (S.cover > 0) { ctx.globalAlpha = S.cover; ctx.drawImage(IMG.portada, 0, 0, W, H); ctx.globalAlpha = 1; }
  const fo = clamp((T - (TOTAL - .6)) / .6); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I', '900 40px I'].map(f => document.fonts.load(f)).concat(NOMBRES.map(cargar))).then(() => { build(); window.READY = true; });
