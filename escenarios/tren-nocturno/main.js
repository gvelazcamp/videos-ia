const IAS = { chatgpt: ['ChatGPT', 0x2bb59a, '#14896f'], claude: ['Claude', 0xe5824c, '#cf5f36'], gemini: ['Gemini', 0x4a7ee6, '#2f5fd0'], grok: ['Grok', 0x9aa0ad, '#4b5263'] };
const NAMES = ['chatgpt', 'claude', 'gemini', 'grok'];
const POS = { chatgpt: V(0, 1.15, -7), claude: V(0, 1.15, -1), gemini: V(0, 1.15, 5), grok: V(0, 1.15, 11) };
const TOP = .45; const SIDE = { chatgpt: 1, claude: -1, gemini: 1, grok: -1 }; const flags = []; const ISL = {}; const FX = {};
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(4242);
const EMO = '"Noto Color Emoji"';
// ================= mundo =================
const SCROLL = []; // objetos que pasan (z se recalcula)
function scrollObj(o, z0, span) { SCROLL.push([o, z0, span]); }
function pasto() { const [c, x] = cv(512, 512); x.fillStyle = '#16241a'; x.fillRect(0, 0, 512, 512); for (let i = 0; i < 5000; i++) { const v = 20 + R() * 30 | 0; x.fillStyle = `rgba(${v},${v + 18},${v + 4},.6)`; x.fillRect(R() * 512, R() * 512, 2, 2 + R() * 4); } const t = tex(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(30, 30); return t; }
function build() {
  scene.fog = new THREE.Fog(0x0a0f22, 40, 150);
  const suelo = mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshStandardMaterial({ map: pasto(), roughness: 1, color: 0x9aa89c }), [0, 0, 0], scene); suelo.rotation.x = -Math.PI / 2;
  // terraplén y rieles
  mesh(new THREE.BoxGeometry(7, .3, 400), M(0x3a3632, { roughness: 1 }), [0, .15, 0], scene);
  for (const x of [-2.1, 2.1]) mesh(new THREE.BoxGeometry(.16, .16, 400), M(0xb8bcc6, { metalness: .9, roughness: .3 }), [x, .42, 0], scene);
  for (let i = 0; i < 120; i++) { const s = mesh(new THREE.BoxGeometry(5.4, .12, .45), M(0x4a3626, { roughness: 1 }), [0, .32, 0], scene, false); scrollObj(s, i * 1.4, 168); }
  // postes y árboles que pasan
  for (let i = 0; i < 14; i++) { const p = new THREE.Group(); mesh(new THREE.CylinderGeometry(.09, .11, 5, 8), M(0x5a4636), [0, 2.5, 0], p); mesh(new THREE.BoxGeometry(1.6, .1, .1), M(0x5a4636), [0, 4.6, 0], p); p.position.x = 5.2; scene.add(p); scrollObj(p, i * 12, 168); }
  for (let i = 0; i < 70; i++) { const t = new THREE.Group(); const h = 2 + R() * 4; mesh(new THREE.CylinderGeometry(.15, .2, h * .4, 6), M(0x3b2a1e), [0, h * .2, 0], t); mesh(new THREE.ConeGeometry(h * .35, h, 7), M(0x1f3d2a, { flatShading: true }), [0, h * .4 + h * .5, 0], t); const sd = R() < .5 ? -1 : 1; t.position.x = sd * (9 + R() * 30); scene.add(t); scrollObj(t, R() * 168, 168); }
  // montaña con túnel (se acerca)
  const mon = new THREE.Group(); scene.add(mon); FX.mon = mon;
  const m1 = mesh(new THREE.SphereGeometry(30, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), M(0x26302a, { flatShading: true, roughness: 1 }), [0, -2, -26], mon, false); m1.scale.set(1.6, .75, .9);
  const boca = mesh(new THREE.CircleGeometry(4.2, 40, 0, Math.PI), new THREE.MeshBasicMaterial({ color: 0x020203 }), [0, 0, .05], mon, false); boca.position.set(0, .2, 0.3);
  const marco = mesh(new THREE.TorusGeometry(4.5, .45, 10, 40, Math.PI), M(0x6b6660, { roughness: 1 }), [0, .2, .4], mon, false);
  mesh(new THREE.BoxGeometry(14, 6, 1), M(0x26302a, { roughness: 1 }), [-9.4, 3, -0.2], mon, false); mesh(new THREE.BoxGeometry(14, 6, 1), M(0x26302a, { roughness: 1 }), [9.4, 3, -0.2], mon, false);
  mesh(new THREE.BoxGeometry(5, 3, 1), M(0x26302a, { roughness: 1 }), [0, 6.5, -0.2], mon, false);
  // luna
  const lu = mesh(new THREE.SphereGeometry(5, 32, 16), new THREE.MeshBasicMaterial({ color: 0xf1ecd6 }), [-30, 38, -140], scene, false); lu.material.fog = false;
  // locomotora
  const lo = new THREE.Group(); lo.position.set(0, .5, -14.5); scene.add(lo); FX.lo = lo;
  const azul = M(0x1d3557, { metalness: .4, roughness: .5 }), rojo = M(0xb3261e, { metalness: .3, roughness: .5 });
  mesh(new THREE.BoxGeometry(4.6, 2.4, 7), azul, [0, 1.8, 0], lo);
  mesh(new THREE.BoxGeometry(4.8, .35, 7.2), rojo, [0, .7, 0], lo);
  mesh(new THREE.BoxGeometry(4.2, 1.6, 2.6), azul, [0, 3.8, 2.0], lo);
  for (const sx of [-1, 1]) mesh(new THREE.PlaneGeometry(1.2, .8), new THREE.MeshBasicMaterial({ color: 0x0a0c12 }), [sx * 2.11, 3.9, 2.0], lo, false).rotation.y = sx * Math.PI / 2;
  const faro = mesh(new THREE.CircleGeometry(.45, 24), new THREE.MeshBasicMaterial({ color: 0xfff4c2 }), [0, 2.3, -3.52], lo, false); faro.rotation.y = Math.PI;
  const sp = new THREE.SpotLight(0xfff0c0, 60, 60, .45, .5, 1.2); sp.position.set(0, 2.3, -3.6); sp.target.position.set(0, 0, -30); lo.add(sp, sp.target);
  const beam = mesh(new THREE.ConeGeometry(3.2, 22, 24, 1, true), new THREE.MeshBasicMaterial({ color: 0xfff4c2, transparent: true, opacity: .07, depthWrite: false, side: THREE.DoubleSide }), [0, 1.5, -14.6], lo, false); beam.rotation.x = -Math.PI / 2;
  for (const [x, z] of [[-1.9, -2.4], [1.9, -2.4], [-1.9, 2.4], [1.9, 2.4]]) mesh(new THREE.CylinderGeometry(.45, .45, .3, 18), M(0x222226), [x, .2, z], lo).rotation.z = Math.PI / 2;
  // palanca del desvío (en la cabina, arriba)
  const lev = new THREE.Group(); lev.position.set(1.4, 4.6, 2.6); lo.add(lev); FX.lev = lev;
  mesh(new THREE.BoxGeometry(.6, .25, .6), M(0x333338), [0, 0, 0], lev);
  const arm = new THREE.Group(); lev.add(arm); FX.levArm = arm; mesh(new THREE.CylinderGeometry(.06, .06, 1.2, 8), M(0xd0d0d6, { metalness: .8 }), [0, .6, 0], arm); mesh(new THREE.SphereGeometry(.16, 12, 10), M(0xe8463a, { emissive: 0x5a0a06, emissiveIntensity: .6 }), [0, 1.2, 0], arm); arm.rotation.x = -.6;
  // vagones-plataforma con los 4 círculos
  NAMES.forEach(n => { const [lab, c, f] = IAS[n];
    const car = new THREE.Group(); car.position.set(0, 0, POS[n].z); scene.add(car);
    mesh(new THREE.BoxGeometry(6.2, .5, 5.6), M(0x2c2f38, { metalness: .5, roughness: .5 }), [0, .9, 0], car);
    for (const [x, z] of [[-2, -1.9], [2, -1.9], [-2, 1.9], [2, 1.9]]) mesh(new THREE.CylinderGeometry(.42, .42, .28, 18), M(0x18181c), [x, .5, z], car).rotation.z = Math.PI / 2;
    mesh(new THREE.BoxGeometry(.3, .2, .6), M(0x111114), [0, .8, -3.0], car);
    const g = new THREE.Group(); g.position.copy(POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(2.5, 2.7, TOP, 56), M(0x5a5e68, { roughness: .9 }), [0, TOP / 2, 0], g);
    mesh(new THREE.CylinderGeometry(2.3, 2.3, .03, 56), M(0x8a8f99, { roughness: .8 }), [0, TOP + .01, 0], g, false);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(2.75, .05, 8, 96), new THREE.MeshBasicMaterial({ color: c })); ring.rotation.x = Math.PI / 2; ring.position.y = .06; g.add(ring);
    const glowR = new THREE.Mesh(new THREE.TorusGeometry(2.32, .035, 8, 96), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .9 })); glowR.rotation.x = Math.PI / 2; glowR.position.y = TOP + .03; g.add(glowR);
    const fp = new THREE.Group(); fp.position.set(-1.8, TOP, -1.0); g.add(fp);
    mesh(new THREE.CylinderGeometry(.03, .03, 2.6, 8), M(0xcfd3dc, { metalness: .6 }), [0, 1.3, 0], fp);
    const fm = mesh(new THREE.PlaneGeometry(1.15, .72), new THREE.MeshStandardMaterial({ map: labelTex(lab, f), side: THREE.DoubleSide }), [.6, 2.25, 0], fp); flags.push([fm, lab, f]); FX['flag_' + n] = fm;
    const bot = makeBot(c); bot.scale.setScalar(1.25); bot.position.set(.2, TOP, .3); bot.rotation.y = Math.atan2(4.3 * SIDE[n], 3.6) * .85; g.add(bot);
    // bufanda (viento)
    mesh(new THREE.TorusGeometry(.26, .06, 8, 20), M(c, { roughness: .9 }), [0, .7, 0], bot.userData.body).rotation.x = Math.PI / 2;
    const prop = new THREE.Group(); prop.position.set(1.2, TOP, -.9); g.add(prop);
    if (n === 'chatgpt') { mesh(new THREE.BoxGeometry(.8, .5, .45), M(0x5b4636, { roughness: .8 }), [0, .25, 0], prop); mesh(new THREE.CircleGeometry(.14, 16), M(0x111), [-.18, .3, .23], prop, false); mesh(new THREE.BoxGeometry(.28, .18, .02), M(0xf2c230, { emissive: 0x5a4000, emissiveIntensity: .5 }), [.18, .32, .23], prop, false); mesh(new THREE.CylinderGeometry(.015, .015, .8, 6), M(0xcccccc), [.3, .9, 0], prop); FX.radio = prop; }
    if (n === 'claude') { const mp = mesh(new THREE.PlaneGeometry(1.0, .7), new THREE.MeshStandardMaterial({ map: mapaTex(), side: THREE.DoubleSide }), [0, .05, 0], prop, false); mp.rotation.x = -Math.PI / 2; FX.mapa = mp; }
    if (n === 'gemini') { mesh(new THREE.BoxGeometry(.7, .05, .5), M(0x1f2937), [0, .05, 0], prop); const sc = mesh(new THREE.PlaneGeometry(.6, .4), M(0x0b1530, { emissive: 0x4a7ee6, emissiveIntensity: .9 }), [0, .08, 0], prop, false); sc.rotation.x = -Math.PI / 2; }
    if (n === 'grok') { const fr = new THREE.Group(); prop.add(fr); FX.freno = fr; mesh(new THREE.BoxGeometry(.4, .3, .4), M(0x333338), [0, .15, 0], fr); const a = new THREE.Group(); a.position.y = .3; fr.add(a); FX.frenoArm = a; mesh(new THREE.CylinderGeometry(.05, .05, 1.1, 8), M(0xb3261e), [0, .55, 0], a); mesh(new THREE.SphereGeometry(.12, 10, 8), M(0xf2c230), [0, 1.1, 0], a); FX.frenoTop = a.children[1]; }
    ISL[n] = { g, bot, ring, home: bot.position.clone(), rotY: bot.rotation.y, c, css: '#' + c.toString(16).padStart(6, '0'), label: lab, f };
  });
  // dos coches de pasajeros
  FX.win = [];
  [17.5, 24.5].forEach(z => { const co = new THREE.Group(); co.position.set(0, .5, z); scene.add(co);
    mesh(new THREE.BoxGeometry(4.6, 3.0, 6.4), M(0x7a1f1a, { roughness: .6 }), [0, 2.0, 0], co); mesh(new THREE.BoxGeometry(4.8, .25, 6.6), M(0x2a2a2e), [0, 3.6, 0], co);
    for (const sx of [-1, 1]) for (let k = 0; k < 4; k++) { const w = mesh(new THREE.PlaneGeometry(.95, .8), new THREE.MeshBasicMaterial({ color: 0x1a2240 }), [sx * 2.31, 2.3, -2.2 + k * 1.45], co, false); w.rotation.y = sx * Math.PI / 2; FX.win.push(w); }
    for (const [x, zz] of [[-1.9, -2.4], [1.9, -2.4], [-1.9, 2.4], [1.9, 2.4]]) mesh(new THREE.CylinderGeometry(.42, .42, .28, 18), M(0x18181c), [x, .1, zz], co).rotation.z = Math.PI / 2; });
  sun.intensity = 2.6; sun.color.set(0xc4d2ff); sun.position.set(-12, 20, 6); sun.target.position.set(0, 0, 0);
  Object.assign(sun.shadow.camera, { left: -22, right: 22, top: 30, bottom: -30 }); sun.shadow.camera.updateProjectionMatrix();
  hemi.intensity = 1.25; hemi.color.set(0x9fb2e8); hemi.groundColor.set(0x2a2e3a); scene.add(new THREE.AmbientLight(0x8090c0, .45));
}
function mapaTex() { const [c, x] = cv(512, 360); x.fillStyle = '#efe3c2'; x.fillRect(0, 0, 512, 360); x.strokeStyle = '#3a2a1a'; x.lineWidth = 8; x.beginPath(); x.moveTo(40, 300); x.lineTo(470, 300); x.stroke(); x.strokeStyle = '#e5824c'; x.beginPath(); x.moveTo(300, 300); x.quadraticCurveTo(380, 290, 430, 120); x.stroke(); x.fillStyle = '#111'; x.fillRect(440, 260, 40, 60); return tex(c); }
// ================= línea de tiempo =================
let LATER = []; const later = (f, ...a) => LATER.push(() => f(...a));
const STARS2 = Array.from({ length: 380 }, () => [R() * W, R() * H * .5, R() * 1.8 + .3, R()]);
const BW = n => ISL[n].bot.localToWorld(V(0, 0, 0));
const HEAD = n => ISL[n].bot.localToWorld(V(0, 1.45, 0));
function idle(T, wind = 1) { NAMES.forEach((n, i) => { const d = ISL[n], u = d.bot.userData; d.bot.position.copy(d.home); d.bot.rotation.y = d.rotY; d.bot.rotation.z = 0; u.body.position.y = Math.sin(T * 7 + i) * .015 * wind; u.arms.forEach(a => a.rotation.set(0, 0, 0)); u.head.rotation.set(0, Math.sin(T * .6 + i) * .2, 0); u.feet.forEach(f => f.position.y = .08); }); }
function talk(n, T, k = 1) { const u = ISL[n].bot.userData; ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 9)) * .06 * k; u.head.rotation.x = Math.sin(T * 9) * .06; }
function wave(n, T) { ISL[n].bot.userData.arms[1].rotation.z = 2.3 + Math.sin(T * 8) * .35; }
function cheer(n, T) { const u = ISL[n].bot.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * (2.5 + Math.sin(T * 9 + s) * .2)); ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 6)) * .12; }
function lookFront(n) { ISL[n].bot.rotation.y = Math.PI; }
// recorrido de Grok por arriba de los vagones (local a su círculo)
const GROK_PATH = [V(.2, TOP, .3), V(2.3, TOP, -1), V(2.3, TOP, -20), V(1.4, TOP + 3.3, -21.6)];
function grokWalk(k, T) { const d = ISL.grok, b = d.bot; k = clamp(k); let p; if (k < .1) p = GROK_PATH[0].clone().lerp(GROK_PATH[1], k / .1); else if (k < .9) p = GROK_PATH[1].clone().lerp(GROK_PATH[2], (k - .1) / .8); else p = GROK_PATH[2].clone().lerp(GROK_PATH[3], (k - .9) / .1);
  b.position.copy(p); b.rotation.y = Math.PI; b.rotation.z = Math.sin(T * 5) * .12; const u = b.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * (1.2 + Math.sin(T * 6 + s) * .3)); if (k > 0 && k < 1) u.feet.forEach((f, s) => f.position.y = .08 + Math.max(0, Math.sin(T * 11 + s * Math.PI)) * .1); }
// ---------- cámaras ----------
const camS = (p0, l0, p1, l1, fov = 52, fov1) => ({ p0, l0, p1: p1 || p0, l1: l1 || l0, fov, fov1: fov1 ?? fov });
function closeOf(n, side = 1) { const b = POS[n].clone(); const c = b.clone().add(V(4.3 * side, 2.7, 3.6)); const l = b.clone().add(V(0, 1.4, 0)); return camS(c, l, c.clone().add(V(-.5 * side, -.1, -.6)), l, 46); }
let sh; function cams() { sh = {
  cover: camS(V(0, 10.5, 27), V(0, 2, -10), V(0, 9.8, 24.5), V(0, 2, -12), 58),
  tunnel: camS(V(-3.2, 5.2, -15), V(0, 3, -60), V(-3, 5, -17), V(0, 3, -60), 56),
  items: camS(V(9, 10, 16), V(0, 1.5, 0), V(8.4, 9.4, 14.6), V(0, 1.5, -.5), 56),
  chatgpt: closeOf('chatgpt', 1), claude: closeOf('claude', -1), gemini: closeOf('gemini', 1), grok: closeOf('grok', -1),
  freno: camS(V(-4.6, 3.8, 15.2), V(1.2, 2.4, 10.2), V(-4.1, 3.6, 14.5), V(1.2, 2.4, 10.2), 44),
  wide: camS(V(10.5, 9, 9), V(0, 1.5, -3), V(10, 8.5, 7.5), V(0, 1.5, -3.5), 58),
  coches: camS(V(12.5, 5.2, 31), V(0, 2.4, 18), V(12, 5, 29.5), V(0, 2.4, 18.5), 52),
  lever: camS(V(5.2, 7.6, -8.5), V(1.4, 5, -12.4), V(4.6, 7.2, -9), V(1.4, 5, -12.4), 50),
  final: camS(V(-7, 6, -2), V(0, 3, -24), V(-6.5, 5.6, -3.5), V(0, 3, -24), 58),
}; }
function followGrok(k) { const p = ISL.grok.bot.localToWorld(V(0, 1, 0)); return camS(p.clone().add(V(5.5, 3.2, 6.5)), p, p.clone().add(V(5.2, 3.0, 6.0)), p, 52); }
// ---------- overlays ----------
function wrap(text, maxW) { const ws = text.split(' '), L = ['']; ws.forEach(w => { const t = (L.at(-1) + ' ' + w).trim(); if (ctx.measureText(t).width > maxW) L.push(w); else L[L.length - 1] = t; }); return L; }
function panel(y, h, k, border = 'rgba(160,190,255,.4)') { ctx.globalAlpha = clamp(k); rr(60, y, W - 120, h, 28); ctx.fillStyle = 'rgba(8,10,20,.92)'; ctx.fill(); ctx.strokeStyle = border; ctx.lineWidth = 3; ctx.stroke(); ctx.globalAlpha = 1; }
function tag(text, k, y, bg = 'rgba(8,10,20,.92)', fg = '#fff', size = 40) { pill(text, W / 2, y, bg, fg, size, k); }
function quote(n, text, k) { const a = clamp(k); if (a <= 0) return; const d = ISL[n]; ctx.save(); ctx.globalAlpha = a; ctx.translate(W / 2, H * .66); const s = .92 + .08 * pop(clamp(k)); ctx.scale(s, s); ctx.font = '800 48px I'; const L = wrap('«' + text + '»', 830); const h = 110 + L.length * 64; rr(-470, -40, 940, h, 30); ctx.fillStyle = 'rgba(8,10,20,.94)'; ctx.fill(); ctx.strokeStyle = d.css; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = d.css; ctx.font = '800 38px I'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(d.label.toUpperCase(), -430, 16); ctx.fillStyle = '#fff'; ctx.font = '800 48px I'; L.forEach((l, i) => ctx.fillText(l, -430, 86 + i * 64)); ctx.restore(); }
const ITEMS = [['🛑', 'FRENO TRABADO'], ['📻', 'RADIO VIEJA'], ['🗺️', 'MAPA DE LAS VÍAS']];
function items(ks, k, tachar = 0) { const a = clamp(k); if (a <= 0) return; const y0 = H * .6; panel(y0, 420, a, '#ffd34d'); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#ffd34d'; ctx.font = '800 44px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('SOLO TIENEN:', W / 2, y0 + 58);
  ITEMS.forEach(([e, t], i) => { const kk = clamp(ks[i]); if (kk <= 0) return; const y = y0 + 150 + i * 96; ctx.save(); ctx.globalAlpha = a * kk; ctx.translate(0, (1 - pop(kk)) * 30); ctx.font = `80px ${EMO}`; ctx.textAlign = 'center'; ctx.fillText(e, 210, y); ctx.font = '800 52px I'; ctx.textAlign = 'left'; ctx.fillStyle = '#fff'; ctx.fillText(t, 290, y + 4); if (i === 0 && tachar > 0) { ctx.strokeStyle = '#ff4b3c'; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(280, y + 4); ctx.lineTo(280 + 520 * ease(clamp(tachar)), y + 4); ctx.stroke(); } ctx.restore(); }); ctx.restore(); }
function hud(dist, secs, k = 1) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; rr(60, 520, 440, 104, 22); ctx.fillStyle = 'rgba(8,10,20,.88)'; ctx.fill(); ctx.strokeStyle = '#e8463a'; ctx.lineWidth = 3; ctx.stroke(); ctx.font = `48px ${EMO}`; ctx.textBaseline = 'middle'; ctx.textAlign = 'left'; ctx.fillText('🚇', 82, 574); ctx.fillStyle = '#ffb3ab'; ctx.font = '800 30px I'; ctx.fillText('TÚNEL', 150, 552); ctx.fillStyle = '#fff'; ctx.font = '800 46px I'; ctx.fillText(Math.max(0, Math.round(dist)).toLocaleString('es-UY') + ' m', 150, 596);
  if (secs != null) { rr(W - 500, 520, 440, 104, 22); ctx.fillStyle = 'rgba(8,10,20,.88)'; ctx.fill(); ctx.strokeStyle = '#4a7ee6'; ctx.stroke(); ctx.font = `48px ${EMO}`; ctx.fillText('⏱️', W - 478, 574); ctx.fillStyle = '#9fc4ff'; ctx.font = '800 30px I'; ctx.fillText('AL DESVÍO', W - 410, 552); ctx.fillStyle = '#fff'; ctx.font = '800 46px I'; ctx.fillText(Math.max(0, Math.ceil(secs)) + ' s', W - 410, 596); } ctx.restore(); }
function mapa(k, kd, kt) { const a = clamp(k); if (a <= 0) return; const y0 = H * .6; panel(y0, 440, a, '#e5824c'); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#ffb38a'; ctx.font = '800 40px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('EL MAPA DE CLAUDE', W / 2, y0 + 52);
  const yv = y0 + 330, x0 = 130, xd = 600, xt = 900; ctx.lineCap = 'round'; ctx.strokeStyle = '#cfd3dc'; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(x0, yv); ctx.lineTo(xt, yv); ctx.stroke();
  ctx.fillStyle = '#111'; rr(xt - 10, yv - 80, 70, 110, 30); ctx.fill(); ctx.strokeStyle = '#6b6660'; ctx.lineWidth = 8; ctx.stroke(); ctx.fillStyle = '#ffb3ab'; ctx.font = '800 30px I'; ctx.fillText('TÚNEL', xt + 25, yv - 110);
  ctx.strokeStyle = '#e5824c'; ctx.lineWidth = 12; ctx.setLineDash([]); const kd2 = ease(clamp(kd)); if (kd2 > 0) { ctx.beginPath(); ctx.moveTo(xd, yv); for (let i = 0; i <= 20 * kd2; i++) { const u = i / 20; ctx.lineTo(xd + u * 230, yv - u * u * 190); } ctx.stroke(); ctx.fillStyle = '#ffb38a'; ctx.font = '800 32px I'; ctx.globalAlpha = a * clamp(kd * 2 - 1); ctx.fillText('DESVÍO ↗ CUESTA', xd + 120, yv - 225); ctx.globalAlpha = a; }
  // tren
  const t = clamp(kt); let tx, ty; if (t < .6) { tx = x0 + 40 + (xd - x0 - 40) * (t / .6); ty = yv; } else { const u = (t - .6) / .4 * .8; tx = xd + u * 230; ty = yv - u * u * 190; } ctx.fillStyle = '#ffd34d'; ctx.beginPath(); ctx.arc(tx, ty, 20, 0, 7); ctx.fill(); ctx.strokeStyle = '#1a1206'; ctx.lineWidth = 4; ctx.stroke(); ctx.restore(); }
function ondas(n, k, T, ok = false) { const a = clamp(k); if (a <= 0) return; const [x, y] = proj(HEAD(n).add(V(.6, .6, 0))); ctx.save(); for (let i = 0; i < 3; i++) { const q = (T * .9 + i / 3) % 1; ctx.globalAlpha = a * (1 - q); ctx.strokeStyle = ok ? '#7ee0c2' : '#f2c230'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(x, y, 30 + q * 120, -1.1, .3); ctx.stroke(); } ctx.restore(); }
function guia(k, T) { const a = clamp(k); if (a <= 0) return; const [x1, y1] = proj(HEAD('gemini')), [x2, y2] = proj(HEAD('grok')); ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = '#8fb6ff'; ctx.lineWidth = 7; ctx.setLineDash([18, 14]); ctx.lineDashOffset = -T * 80; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo((x1 + x2) / 2, Math.min(y1, y2) - 160, x2, y2); ctx.stroke(); ctx.restore(); }
function viento(k, T) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.strokeStyle = 'rgba(220,235,255,.35)'; ctx.lineWidth = 4; ctx.lineCap = 'round'; for (let i = 0; i < 26; i++) { const y = (i * 97) % H, sp = 1400 + (i * 53) % 600, x = W - ((T * sp + i * 311) % (W + 400)); ctx.globalAlpha = a * (.4 + (i % 3) * .2); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 160 + (i % 4) * 40, y); ctx.stroke(); } ctx.restore(); }
function drawCover(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const g = ctx.createLinearGradient(0, H * .52, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.3, 'rgba(0,0,6,.8)'); g.addColorStop(1, 'rgba(0,0,6,.95)'); ctx.fillStyle = g; ctx.fillRect(0, H * .52, W, H * .48);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 58px I'; ctx.fillStyle = '#fff'; ctx.fillText('ChatGPT · Claude · Gemini · Grok', W / 2, H * .7); ctx.font = '800 76px I'; ctx.fillStyle = '#9fc4ff'; ctx.fillText('¿QUÉ PASARÍA SI', W / 2, H * .77); ctx.font = '800 108px I'; ctx.fillStyle = '#ffd34d'; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.fillText('UN TREN VA', W / 2, H * .835); ctx.fillText('SIN CONDUCTOR?', W / 2, H * .9); ctx.restore(); }
function drawCTA(k) { const s2 = pop(clamp(k)); if (s2 <= 0) return; ctx.save(); ctx.translate(W / 2, H * .7); ctx.scale(s2, s2); rr(-420, -130, 840, 260, 36); ctx.fillStyle = '#ffd34d'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 50px I'; ctx.fillText('¿QUERÉS EL ENSAYO?', 0, -55); ctx.font = '800 92px I'; ctx.fillText('Comentá ENSAYO', 0, 45); ctx.restore(); ctx.font = '800 38px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText('@gostudiouy', W / 2, H * .81); }
// ---------- estado del tren ----------
let OFF = 0, DIST = 2000, VEL = 1;
function frenoRoto(k) { FX.frenoArm.rotation.x = k > 0 ? -1.3 * ease(clamp(k)) : 0; FX.frenoTop.visible = k < .6; }
function luces(k) { FX.win.forEach((w, i) => w.material.color.set(clamp(k * 3 - i * .15) > .5 ? 0xffd77a : 0x1a2240)); }
function palanca(k) { FX.levArm.rotation.x = -.6 + 1.2 * ease(clamp(k)); }
// ---------- segmentos ----------
const S_ = []; function seg(text, opt = {}) { S_.push(Object.assign({ text }, opt)); }
const D = (a, b, lt, dur) => a + (b - a) * clamp(lt / dur);
seg('¿Qué pasaría si *ChatGPT,* *Claude,* *Gemini* y *Grok* despertaran en un *tren* *nocturno,* sin *conductor?*', { shot: 'cover', d: [2000, 2000], fx: (lt, p, S, w, T) => { S.cover = clamp(1 - (lt - w(13)) / .5); [4, 5, 6, 8].forEach((wi, i) => { if (lt > w(wi) && lt < w(wi) + 1.1) { talk(NAMES[i], T); wave(NAMES[i], T); } }); } });
seg('El tren *acelera.* Adelante, a *dos* *kilómetros,* un *túnel.* Atrás, *cuarenta* *pasajeros* *dormidos.*', { shot: 'tunnel', d: [2000, 1850], fx: (lt, p, S, w, T) => { S.hud = [1]; if (lt > w(8)) later(tag, '40 PASAJEROS DURMIENDO 💤', (lt - w(9)) / .3, H * .8); } });
seg('Solo tienen *tres* *cosas:* un *freno* *trabado,* una *radio* *vieja* y un *mapa* *de* *las* *vías.*', { shot: 'items', d: [1850, 1700], fx: (lt, p, S, w, T) => { S.items = [[(lt - w(5)) / .3, (lt - w(8)) / .3, (lt - w(12)) / .3], lt / .3]; } });
seg('*ChatGPT* agarra la *radio* y llama a la *estación.* *Nadie* *contesta.*', { shot: 'chatgpt', d: [1700, 1580], fx: (lt, p, S, w, T) => { talk('chatgpt', T); S.ondas = ['chatgpt', (lt - w(3)) / .3]; if (lt > w(8)) later(tag, 'SIN RESPUESTA', (lt - w(8)) / .3, H * .8, '#e8463a', '#fff', 44); } });
seg('*Grok* se cuelga del *freno* y tira con *todo.* La palanca *se* *rompe.*', { shot: 'freno', d: [1580, 1450], fx: (lt, p, S, w, T) => { const u = ISL.grok.bot.userData; ISL.grok.bot.rotation.y = -0.9; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * 2.4); ISL.grok.bot.position.y = ISL.grok.home.y + (lt > w(6) && lt < w(10) ? Math.abs(Math.sin(T * 14)) * .1 : 0); frenoRoto((lt - w(10)) / .25); if (lt > w(10)) { const [x, y] = proj(BW('grok').add(V(1, 2.2, -.9))); later(xmark, x, y, (lt - w(10)) / .3); } } });
seg('*Ya* *no* *hay* *freno.*', { shot: 'items', d: [1450, 1400], fx: (lt, p, S, w, T) => { frenoRoto(1); S.items = [[1, 1, 1], 1, lt / .5]; } });
seg('*Claude* despliega el *mapa:* antes del túnel hay un *desvío* que *sube* *una* *cuesta.* Si lo toman, el tren *frena* *solo.*', { shot: 'claude', d: [1400, 1200], fx: (lt, p, S, w, T) => { frenoRoto(1); talk('claude', T); S.mapa = [lt / .3, (lt - w(7)) / .8, lt / 10 * .2]; } });
seg('«No hace falta frenar el tren: hace falta *cambiarle* *el* *camino».*', { shot: 'claude', d: [1200, 1120], fx: (lt, p, S, w, T) => { frenoRoto(1); talk('claude', T); S.quote = ['claude', 'No hace falta frenar el tren: hace falta cambiarle el camino.', lt / .3]; } });
seg('*Gemini* calcula: al desvío llegan en *noventa* *segundos.*', { shot: 'gemini', d: [1120, 1040], fx: (lt, p, S, w, T) => { frenoRoto(1); talk('gemini', T); S.hud = [1]; S.secs = lt > w(6) ? 90 : null; if (lt > w(6)) later(tag, '⏱️ 90 SEGUNDOS', (lt - w(6)) / .3, H * .8, '#4a7ee6', '#fff', 48); } });
seg('Pero la *palanca* *del* *desvío* está en la *locomotora,* y hay que cruzar por *arriba* *de* *los* *vagones.*', { shot: 'wide', d: [1040, 900], timer: true, fx: (lt, p, S, w, T) => { frenoRoto(1); S.hud = [1]; if (lt > w(7)) { const [x, y] = proj(V(1.4, 6.5, -12)); later(pill, '¡ACÁ!', x, y, '#e8463a', '#fff', 44, (lt - w(7)) / .3); } } });
seg('*Grok* sube al *techo.* El *viento* casi lo *tira.*', { shot: 'follow', d: [900, 800], timer: true, gk: [0, .35], fx: (lt, p, S, w, T) => { frenoRoto(1); S.hud = [1]; S.viento = 1; } });
seg('*Gemini* lo *guía* por la radio, *metro* *a* *metro.*', { shot: 'wideG', d: [800, 690], timer: true, gk: [.35, .62], fx: (lt, p, S, w, T) => { frenoRoto(1); S.hud = [1]; S.viento = .6; talk('gemini', T); S.guia = lt / .4; if (lt > w(6)) later(tag, 'METRO A METRO', (lt - w(6)) / .3, H * .8, '#4a7ee6', '#fff', 44); } });
seg('*ChatGPT* despierta a los *pasajeros,* con *calma:* que se *agarren* *fuerte.*', { shot: 'coches', d: [690, 560], timer: true, gk: [.62, .8], fx: (lt, p, S, w, T) => { frenoRoto(1); S.hud = [1]; luces((lt - w(4)) / 1.2); later(tag, '¡AGÁRRENSE FUERTE! 🙌', (lt - w(9)) / .3, H * .8, '#2bb59a', '#06110d', 44); } });
seg('*Grok* llega a la *locomotora,* y *baja* *la* *palanca.*', { shot: 'lever', d: [560, 420], timer: true, gk: [.8, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); S.hud = [1]; const u = ISL.grok.bot.userData; if (lt > w(6)) { u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * 2.2); palanca((lt - w(6)) / .4); } if (lt > w(7)) later(tag, '¡DESVÍO!', (lt - w(7)) / .3, H * .8, '#ffd34d', '#1a1206', 52); } });
seg('El tren *gira,* *sube* *la* *cuesta* y se *detiene* a *veinte* *metros* del *túnel.*', { shot: 'final', d: [420, 20], stop: true, gk: [1, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); palanca(1); S.hud = [1]; S.mapa = [lt / .3, 1, .6 + .4 * clamp(lt / (w(9) || 3))]; } });
seg('*Cuarenta* *pasajeros,* *a* *salvo.*', { shot: 'coches', d: [20, 20], stop: true, gk: [1, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); palanca(1); NAMES.filter(n => n !== 'grok').forEach((n, i) => cheer(n, T + i)); later(tag, '40 PASAJEROS A SALVO ✅', lt / .3, H * .8, '#2bb59a', '#06110d', 48); } });
seg('Nadie lo lograba *solo:* hizo falta el *mapa,* la *radio,* la *calma* y el *coraje.*', { shot: 'cover', d: [20, 20], stop: true, gk: [1, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); palanca(1); [['claude', 6], ['chatgpt', 8], ['chatgpt', 10], ['grok', 13]].forEach(([n, wi]) => { if (lt > w(wi) && lt < w(wi) + 1) cheer(n, T); }); } });
seg('¿Vos qué hacías: *tirabas* *del* *freno* o *buscabas* *el* *desvío?*', { shot: 'wide', d: [20, 20], stop: true, gk: [1, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); palanca(1); later(tag, '¿FRENO O DESVÍO?', lt / .35, H * .66, '#5b2a86', '#fff', 52); } });
seg('Si querés ver el ensayo, comentá *ENSAYO.*', { shot: 'cover', d: [20, 20], stop: true, gk: [1, 1], fx: (lt, p, S, w, T) => { frenoRoto(1); luces(1); palanca(1); NAMES.filter(n => n !== 'grok').forEach((n, i) => cheer(n, T + i)); S.cta = lt / .4; } });
// ---------- timing ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TM.dur + 2.2; s.dur = s.t1 - s.t0; });
for (let i = 0; i < S_.length;) { let j = i; while (j + 1 < S_.length && S_[j + 1].shot === S_[i].shot) j++; for (let k = i; k <= j; k++) { S_[k].sp0 = S_[i].t0; S_[k].sp1 = S_[j].t1; } i = j + 1; }
const TOTAL = S_.at(-1).t1; window.TOTAL = TOTAL;
const T90 = S_[8].wt[6]; // cuando Gemini dice «noventa»
const TSTOP = S_[14].t0;
// desplazamiento del mundo: velocidad que baja a 0 en el segmento 15
function offAt(T) { const v = 9; if (T < TSTOP) return v * T; const d = Math.min(T - TSTOP, 4); return v * TSTOP + v * (d - d * d / 8); }
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, p = clamp(lt / s.dur), w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  idle(T); frenoRoto(0); luces(0); palanca(0);
  const dist = s.d[0] + (s.d[1] - s.d[0]) * (s.stop ? ease(clamp(lt / 3.5)) : p);
  // mundo
  const off = offAt(T); SCROLL.forEach(([o, z0, span]) => { o.position.z = ((z0 + off) % span) - span * .62; });
  FX.mon.position.z = -18.5 - dist * .045;
  if (s.gk) grokWalk(s.gk[0] + (s.gk[1] - s.gk[0]) * p, T);
  let sh_ = s.shot === 'follow' ? followGrok() : s.shot === 'wideG' ? camS(V(12, 11, 16), V(0, 2, -2), V(11.5, 10.5, 14.5), V(0, 2, -3), 60) : sh[s.shot];
  const k = ease((T - s.sp0) / (s.sp1 - s.sp0));
  const shake = s.stop ? 0 : .03; camera.position.copy(sh_.p0).lerp(sh_.p1, k).add(V(Math.sin(T * 31) * shake, Math.sin(T * 23) * shake, 0)); const look = sh_.l0.clone().lerp(sh_.l1, k); camera.fov = sh_.fov + (sh_.fov1 - sh_.fov) * k; camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();
  const S = {}; LATER = []; if (s.fx) s.fx(lt, p, S, w, T);
  const g = ctx.createLinearGradient(0, 0, 0, H * .55); g.addColorStop(0, '#02030a'); g.addColorStop(1, '#0a1024'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (const [x, y, r, a] of STARS2) { ctx.globalAlpha = .3 + a * .7 * (.8 + .2 * Math.sin(T * 2 + a * 9)); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (S.viento) viento(S.viento, T);
  if (S.guia) guia(S.guia, T);
  if (S.ondas) ondas(...S.ondas, T);
  LATER.forEach(f => f());
  if (S.hud) { let secs = S.secs ?? null; if (s.timer || (T > T90 && T < TSTOP)) secs = Math.max(0, 90 - (T - T90) * (90 / Math.max(1, TSTOP - T90))); hud(dist, secs, S.hud[0]); }
  if (S.items) items(...S.items);
  if (S.mapa) mapa(...S.mapa);
  if (S.quote) quote(...S.quote);
  if (S.cta) drawCTA(S.cta);
  if (S.cover > 0) drawCover(S.cover);
  if (NAMES.includes(s.shot)) pill(ISL[s.shot].label, W / 2, 470, ISL[s.shot].f, '#fff', 44, 1);
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I', `40px ${EMO}`].map(f => document.fonts.load(f, '🛑📻'))).then(() => { build(); cams(); flags.forEach(([m, l, f]) => { if (l) { m.material.map = labelTex(l, f); m.material.needsUpdate = true; } }); window.READY = true; });
