const IAS = { chatgpt: ['ChatGPT', 0x2bb59a, '#14896f'], claude: ['Claude', 0xe5824c, '#cf5f36'], gemini: ['Gemini', 0x4a7ee6, '#2f5fd0'], grok: ['Grok', 0x9aa0ad, '#4b5263'] };
const NAMES = ['chatgpt', 'claude', 'gemini', 'grok'];
const POS = { chatgpt: V(-1.35, 0, -1.0), claude: V(1.35, 0, -1.0), gemini: V(-1.35, 0, 1.4), grok: V(1.35, 0, 1.4) };
const TOP = .12; const flags = []; const ISL = {}; const FX = {};
const EMO = '"Noto Color Emoji"';
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(4747);
function acero() { const [c, x] = cv(512, 512); x.fillStyle = '#8a8f99'; x.fillRect(0, 0, 512, 512); for (let i = 0; i < 512; i += 2) { const v = 128 + (R() - .5) * 30 | 0; x.fillStyle = `rgba(${v},${v + 4},${v + 10},.35)`; x.fillRect(0, i, 512, 1); } x.strokeStyle = 'rgba(0,0,0,.25)'; x.lineWidth = 4; for (let i = 0; i <= 512; i += 128) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, 512); x.stroke(); } const t = tex(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; }
function build() {
  scene.fog = new THREE.Fog(0x05060c, 18, 60);
  const ac = acero(); const pared = new THREE.MeshStandardMaterial({ map: ac, metalness: .6, roughness: .45, color: 0xb8bcc6 });
  // hueco del edificio (oscuro, con rieles y luces de piso)
  const hueco = new THREE.Group(); scene.add(hueco);
  mesh(new THREE.BoxGeometry(18, 60, .5), M(0x1a1c24), [0, 10, -6], hueco, false);
  for (const x of [-4.2, 4.2, 6.2, 10.6]) mesh(new THREE.BoxGeometry(.25, 60, .25), M(0x3a3d48, { metalness: .7 }), [x, 10, -4], hueco, false);
  for (let i = -3; i < 6; i++) { const y = i * 4.2; mesh(new THREE.BoxGeometry(18, .2, .4), M(0x2a2d38), [0, y, -5.6], hueco, false); const [lc, lx] = cv(256, 128); lx.fillStyle = '#111'; lx.fillRect(0, 0, 256, 128); lx.fillStyle = '#ffb000'; lx.font = '800 80px I'; lx.textAlign = 'center'; lx.textBaseline = 'middle'; lx.fillText(String(47 + i), 128, 68); const pl = mesh(new THREE.PlaneGeometry(1.2, .6), new THREE.MeshBasicMaterial({ map: tex(lc) }), [-6.5, y + 2, -5.7], hueco, false); }
  // cabina (abierta hacia la cámara)
  const cab = new THREE.Group(); scene.add(cab); FX.cab = cab;
  mesh(new THREE.BoxGeometry(6.4, .25, 6.4), M(0x2d2f38, { roughness: .8 }), [0, -.125, 0], cab);
  mesh(new THREE.BoxGeometry(6.4, .25, 6.4), pared, [0, 5.1, 0], cab);
  mesh(new THREE.BoxGeometry(6.4, 5.2, .2), pared, [0, 2.5, -3.2], cab);
  // pared derecha con rendija hacia la cabina vecina
  mesh(new THREE.BoxGeometry(.2, 5.2, 2.4), pared, [3.2, 2.5, -2.0], cab); mesh(new THREE.BoxGeometry(.2, 5.2, 2.0), pared, [3.2, 2.5, 2.2], cab);
  mesh(new THREE.BoxGeometry(.2, 2.6, 2.2), pared, [3.2, 3.9, .2], cab); mesh(new THREE.BoxGeometry(.2, 1.4, 2.2), pared, [3.2, .7, .2], cab);
  // pared izquierda = puertas con vidrio
  FX.puertaA = new THREE.Group(); FX.puertaB = new THREE.Group(); cab.add(FX.puertaA, FX.puertaB);
  for (const [g, z] of [[FX.puertaA, -1.6], [FX.puertaB, 1.6]]) { g.position.set(-3.2, 0, z); mesh(new THREE.BoxGeometry(.2, 5.0, 3.2), pared, [0, 2.5, 0], g); const vid = mesh(new THREE.PlaneGeometry(1.6, 1.6), new THREE.MeshPhysicalMaterial({ color: 0x9fd4ff, transparent: true, opacity: .35, roughness: .1 }), [.12, 3.0, 0], g, false); vid.rotation.y = Math.PI / 2; }
  // S.O.S. de cinta en el vidrio (aparece de a letras)
  FX.sos = []; const cinta = new THREE.MeshBasicMaterial({ color: 0xfff1a8 });
  const T_ = (g, x, y, w, h, r = 0) => { const m = mesh(new THREE.BoxGeometry(.02, h, w), cinta, [.16, y, x], g, false); m.rotation.x = r; return m; };
  const L = l => { const g = new THREE.Group(); FX.puertaA.add(g); g.visible = false; FX.sos.push(g); return g; };
  { const g = L(); T_(g, -.45, 3.55, .5, .08); T_(g, -.68, 3.3, .08, .5); T_(g, -.45, 3.0, .5, .08); T_(g, -.22, 2.75, .08, .5); T_(g, -.45, 2.5, .5, .08); }
  { const g = L(); T_(g, .25, 3.55, .5, .08); T_(g, .25, 2.5, .5, .08); T_(g, .02, 3.02, .08, 1.05); T_(g, .48, 3.02, .08, 1.05); }
  { const g = L(); FX.sos[0].position.z = .3; FX.sos[1].position.z = .25; g.position.z = -1.2; FX.sos.forEach(q => q.scale.z = -1); T_(g, -.45, 3.55, .5, .08); T_(g, -.68, 3.3, .08, .5); T_(g, -.45, 3.0, .5, .08); T_(g, -.22, 2.75, .08, .5); T_(g, -.45, 2.5, .5, .08); }
  // escotilla en el techo
  FX.escot = mesh(new THREE.BoxGeometry(1.4, .06, 1.4), M(0x3a3d48, { metalness: .7 }), [1.3, 4.97, 1.2], cab, false);
  // luz de emergencia roja
  FX.emer = new THREE.PointLight(0xff2a2a, 6, 14); FX.emer.position.set(0, 4.6, 0); cab.add(FX.emer); FX.emerBulb = mesh(new THREE.SphereGeometry(.15, 12, 8), new THREE.MeshBasicMaterial({ color: 0xff3030 }), [0, 4.9, 0], cab, false);
  FX.techo = new THREE.PointLight(0xfff4e0, 0, 16); FX.techo.position.set(0, 4.7, 1); cab.add(FX.techo);
  // cabina vecina (más baja) con la nena
  const vec = new THREE.Group(); vec.position.set(6.6, -1.0, .2); scene.add(vec); FX.vec = vec;
  mesh(new THREE.BoxGeometry(6, .25, 5), M(0x2d2f38), [0, -.125, 0], vec); mesh(new THREE.BoxGeometry(6, 5.2, .2), pared, [0, 2.5, -2.5], vec); mesh(new THREE.BoxGeometry(6, .25, 5), pared, [0, 5.1, 0], vec);
  const nena = new THREE.Group(); nena.position.set(-1.6, 0, .3); vec.add(nena); FX.nena = nena;
  mesh(new THREE.CylinderGeometry(.28, .38, .9, 16), M(0xf2c230), [0, .65, 0], nena); const cab2 = mesh(new THREE.SphereGeometry(.3, 20, 16), M(0xf1c7a3), [0, 1.35, 0], nena);
  mesh(new THREE.SphereGeometry(.32, 20, 16, 0, Math.PI * 2, 0, 1.4), M(0x5a3420), [0, 1.42, -.03], nena); for (const s of [-1, 1]) mesh(new THREE.SphereGeometry(.12, 10, 8), M(0x5a3420), [s * .33, 1.35, -.05], nena);
  for (const s of [-1, 1]) mesh(new THREE.SphereGeometry(.04, 8, 6), M(0x111111), [s * .1, 1.38, .27], nena, false);
  FX.nenaLuz = new THREE.PointLight(0xffd9a0, 2, 6); FX.nenaLuz.position.set(-1, 2, 1); vec.add(FX.nenaLuz);
  // linterna, celular y cinta en el piso
  const it = new THREE.Group(); it.position.set(0, 0, .25); cab.add(it);
  const lin = mesh(new THREE.CylinderGeometry(.08, .1, .5, 12), M(0x333338, { metalness: .6 }), [-.4, .1, 0], it); lin.rotation.z = Math.PI / 2;
  FX.cel = mesh(new THREE.BoxGeometry(.28, .03, .5), M(0x111114), [.1, .02, .1], it); FX.celPant = mesh(new THREE.PlaneGeometry(.24, .44), new THREE.MeshBasicMaterial({ color: 0x4a7ee6 }), [.1, .04, .1], it, false); FX.celPant.rotation.x = -Math.PI / 2;
  mesh(new THREE.TorusGeometry(.16, .07, 10, 24), M(0xfff1a8), [.55, .07, -.1], it).rotation.x = Math.PI / 2;
  // bomberos: luces que llegan por el hueco
  FX.bomb = [0xff2020, 0xffffff].map((c, i) => { const p = new THREE.PointLight(c, 0, 20); p.position.set(-5.5, 3, i ? -1 : 1); scene.add(p); return p; });
  // los 4 robots con su aro de color en el piso
  NAMES.forEach(n => { const [lab, c, f] = IAS[n]; const g = new THREE.Group(); g.position.copy(POS[n]); cab.add(g);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.95, .045, 8, 64), new THREE.MeshBasicMaterial({ color: c })); ring.rotation.x = Math.PI / 2; ring.position.y = .03; g.add(ring);
    const glowR = new THREE.Mesh(new THREE.CircleGeometry(.92, 48), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .12 })); glowR.rotation.x = -Math.PI / 2; glowR.position.y = .02; g.add(glowR);
    const bot = makeBot(c); bot.scale.setScalar(1.35); bot.position.set(0, TOP, 0); bot.rotation.y = Math.atan2(-POS[n].x * .4, 8 - POS[n].z); g.add(bot);
    const vis = new THREE.PointLight(c, 1.2, 3); vis.position.set(0, 1.4, .6); g.add(vis);
    ISL[n] = { g, bot, ring, glowR, vis, home: bot.position.clone(), rotY: bot.rotation.y, c, css: '#' + c.toString(16).padStart(6, '0'), label: lab, f };
  });
  sun.intensity = .35; sun.color.set(0x8090ff); sun.position.set(-6, 14, 12); sun.target.position.set(0, 1, 0);
  Object.assign(sun.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10 }); sun.shadow.camera.updateProjectionMatrix();
  hemi.intensity = .5; hemi.color.set(0x8a90c0); hemi.groundColor.set(0x1a1820); FX.amb = new THREE.AmbientLight(0x8090c0, .25); scene.add(FX.amb);
}
// ======= animación =======
let LATER = []; const later = (f, ...a) => LATER.push(() => f(...a));
const HEAD = n => ISL[n].bot.localToWorld(V(0, 1.45, 0));
function idle(T) { NAMES.forEach((n, i) => { const d = ISL[n], u = d.bot.userData; d.bot.position.copy(d.home); d.bot.rotation.y = d.rotY; u.body.position.y = Math.sin(T * 2 + i) * .02; u.arms.forEach(a => a.rotation.set(0, 0, 0)); u.head.rotation.set(0, Math.sin(T * .6 + i) * .2, 0); u.feet.forEach(f => f.position.y = .08); d.glowR.material.opacity = .12; d.vis.intensity = 1.2; }); }
function talk(n, T, k = 1) { const d = ISL[n], u = d.bot.userData; d.bot.position.y = d.home.y + Math.abs(Math.sin(T * 9)) * .05 * k; u.head.rotation.x = Math.sin(T * 9) * .06; d.glowR.material.opacity = .45; d.vis.intensity = 3.5; }
function wave(n, T) { ISL[n].bot.userData.arms[1].rotation.z = 2.3 + Math.sin(T * 8) * .35; }
function cheer(n, T) { const u = ISL[n].bot.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * (2.5 + Math.sin(T * 9 + s) * .2)); ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 6)) * .12; }
function mirar(n, x, z) { const d = ISL[n]; d.bot.rotation.y = Math.atan2(x - POS[n].x, z - POS[n].z); }
function luces(k) { FX.techo.intensity = 14 * k; FX.amb.intensity = .25 + .6 * k; hemi.intensity = .5 + .9 * k; }
function emergencia(T, on = 1) { const f = on * (.55 + .45 * Math.abs(Math.sin(T * 2.2))); FX.emer.intensity = 7 * f; FX.emerBulb.material.color.setRGB(f, .1 * f, .1 * f); }
function sosK(k) { FX.sos.forEach((g, i) => g.visible = k * 3 > i + .2); }
function bomberos(k, T) { FX.bomb.forEach((p, i) => p.intensity = 30 * clamp(k) * (Math.sin(T * 12 + i * Math.PI) > 0 ? 1 : .15)); }
function puertas(k) { const e = ease(clamp(k)); FX.puertaA.position.z = -1.6 - 1.5 * e; FX.puertaB.position.z = 1.6 + 1.5 * e; }
// ---------- cámaras ----------
const camS = (p0, l0, p1, l1, fov = 52, fov1) => ({ p0, l0, p1: p1 || p0, l1: l1 || l0, fov, fov1: fov1 ?? fov });
function closeOf(n, side = 0) { const b = POS[n].clone(); const c = b.clone().add(V(side * 1.2, 2.3, 4.2)); const l = b.clone().add(V(0, 1.0, 0)); return camS(c, l, c.clone().add(V(0, -.1, -.5)), l, 46); }
let sh; function cams() { sh = {
  cover: camS(V(0, 3.4, 10.5), V(0, 2.1, 0), V(0, 3.2, 9.4), V(0, 2.1, 0), 50),
  wide: camS(V(-2.2, 4.2, 9), V(.3, 1.6, 0), V(-1.6, 4.0, 8.2), V(.3, 1.6, 0), 52),
  techo: camS(V(2.8, 2.0, 5.5), V(1.3, 4.8, 1.2), V(2.4, 1.8, 4.8), V(1.3, 4.9, 1.1), 52),
  rendija: camS(V(2.6, 3.0, 9.2), V(3.6, 1.3, 0), V(3.0, 2.8, 8.2), V(3.8, 1.2, 0), 48),
  puerta: camS(V(1.8, 3.4, 4.4), V(-3.1, 3.0, -.7), V(1.4, 3.3, 3.8), V(-3.1, 3.0, -.7), 44),
  celu: camS(V(.8, 2.6, 2.4), V(.35, 0, .35), V(.6, 2.2, 2.0), V(.35, 0, .35), 44),
  hueco: camS(V(-1, 6, 11), V(-3, 2.5, 0), V(-.6, 5.6, 10), V(-3, 2.5, 0), 56),
  chatgpt: closeOf('chatgpt', -1), claude: closeOf('claude', 1), gemini: closeOf('gemini', -1), grok: closeOf('grok', 1),
}; }
// ---------- overlays ----------
function tag(text, k, y, bg = 'rgba(8,10,20,.92)', fg = '#fff', size = 40) { pill(text, W / 2, y, bg, fg, size, k); }
function panel(y, h, k, border) { ctx.globalAlpha = clamp(k); rr(60, y, W - 120, h, 28); ctx.fillStyle = 'rgba(8,10,20,.93)'; ctx.fill(); ctx.strokeStyle = border; ctx.lineWidth = 3; ctx.stroke(); ctx.globalAlpha = 1; }
const ITEMS = [['🔦', 'LINTERNA SIN PILAS'], ['📱', 'CELULAR CON 3 %'], ['🧻', 'UN ROLLO DE CINTA']];
function items(ks, k, tachar = 0) { const a = clamp(k); if (a <= 0) return; const y0 = H * .6; panel(y0, 420, a, '#ffd34d'); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#ffd34d'; ctx.font = '800 44px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('SOLO TIENEN:', W / 2, y0 + 58);
  ITEMS.forEach(([e, t], i) => { const kk = clamp(ks[i]); if (kk <= 0) return; const y = y0 + 150 + i * 96; ctx.save(); ctx.globalAlpha = a * kk; ctx.font = `76px ${EMO}`; ctx.textAlign = 'center'; ctx.fillText(e, 200, y); ctx.font = '800 50px I'; ctx.textAlign = 'left'; ctx.fillStyle = '#fff'; ctx.fillText(t, 280, y + 4); if (i === 0 && tachar > 0) { ctx.strokeStyle = '#ff4b3c'; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(270, y + 4); ctx.lineTo(270 + 560 * ease(clamp(tachar)), y + 4); ctx.stroke(); } ctx.restore(); }); ctx.restore(); }
function bateria(pct, k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const x = W - 300, y = 520; rr(x, y - 48, 240, 96, 24); ctx.fillStyle = 'rgba(8,10,20,.9)'; ctx.fill(); ctx.strokeStyle = pct <= 1 ? '#e8463a' : '#f2c230'; ctx.lineWidth = 4; ctx.stroke(); rr(x + 24, y - 20, 110, 40, 8); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.stroke(); ctx.fillStyle = '#fff'; ctx.fillRect(x + 136, y - 9, 8, 18); const w = 102 * Math.max(.04, pct / 10); ctx.fillStyle = pct <= 1 ? '#e8463a' : '#f2c230'; ctx.fillRect(x + 28, y - 16, Math.min(102, w), 32); ctx.font = '800 40px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(pct + ' %', x + 152, y + 2); ctx.restore(); }
function piso(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const x = 60, y = 520; rr(x, y - 48, 260, 96, 24); ctx.fillStyle = 'rgba(8,10,20,.9)'; ctx.fill(); ctx.strokeStyle = '#ffb000'; ctx.lineWidth = 4; ctx.stroke(); ctx.fillStyle = '#ffb000'; ctx.font = '800 50px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('▼ 47', x + 130, y + 4); ctx.restore(); }
function mensaje(k) { const s = pop(clamp(k)); if (s <= 0) return; ctx.save(); ctx.translate(W / 2, H * .66); ctx.scale(s, s); rr(-430, -150, 860, 300, 40); ctx.fillStyle = '#0b1530'; ctx.fill(); ctx.strokeStyle = '#4a7ee6'; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = '#9fc4ff'; ctx.font = '800 34px I'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText('📱 MENSAJE (1 %)', -390, -100); ctx.fillStyle = '#fff'; ctx.font = '800 50px I'; ['Ascensor B · piso 47', '4 adentro + una nena', 'al lado'].forEach((l, i) => ctx.fillText(l, -390, -20 + i * 62)); ctx.restore(); }
function golpes(k, T) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a * (Math.sin(T * 9) > 0 ? 1 : .35); ctx.fillStyle = '#fff'; ctx.font = '800 64px I'; ctx.textAlign = 'center'; ctx.fillText('¡TOC! ¡TOC!', W / 2, H * .7); ctx.restore(); }
function drawCover(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const g = ctx.createLinearGradient(0, H * .5, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.3, 'rgba(4,0,0,.82)'); g.addColorStop(1, 'rgba(4,0,0,.96)'); ctx.fillStyle = g; ctx.fillRect(0, H * .5, W, H * .5);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 58px I'; ctx.fillStyle = '#fff'; ctx.fillText('ChatGPT · Claude · Gemini · Grok', W / 2, H * .69); ctx.font = '800 76px I'; ctx.fillStyle = '#ff8a7a'; ctx.fillText('¿QUÉ PASARÍA SI', W / 2, H * .765); ctx.font = '800 104px I'; ctx.fillStyle = '#ffd34d'; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.fillText('SE CORTA LA LUZ', W / 2, H * .83); ctx.fillText('EN EL PISO 47?', W / 2, H * .895); ctx.restore(); }
function drawCTA(k) { const s2 = pop(clamp(k)); if (s2 <= 0) return; ctx.save(); ctx.translate(W / 2, H * .7); ctx.scale(s2, s2); rr(-420, -130, 840, 260, 36); ctx.fillStyle = '#ffd34d'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 50px I'; ctx.fillText('¿QUERÉS EL ENSAYO?', 0, -55); ctx.font = '800 92px I'; ctx.fillText('Comentá ENSAYO', 0, 45); ctx.restore(); ctx.font = '800 38px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText('@gostudiouy', W / 2, H * .81); }
// ---------- segmentos ----------
const S_ = []; function seg(text, opt = {}) { S_.push(Object.assign({ text }, opt)); }
seg('¿Qué pasaría si *ChatGPT,* *Claude,* *Gemini* y *Grok* quedaran encerrados en un *ascensor,* en el *piso* *cuarenta* *y* *siete,* en pleno *apagón?*', { shot: 'cover', luz: [1, 1], fx: (lt, p, S, w, T) => { S.cover = clamp(1 - (lt - w(18)) / .4); [3, 4, 5, 7].forEach((wi, i) => { if (lt > w(wi) && lt < w(wi) + .9) { talk(NAMES[i], T); wave(NAMES[i], T); } }); S.luz = lt > w(20) ? 0 : 1; } });
seg('Se *apagan* *las* *luces.* Solo brillan sus *cuatro* *visores.* Y desde abajo, alguien *golpea.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.luz = clamp(1 - lt / .25); S.emer = 1; S.piso = 1; if (lt > w(12)) { S.golpes = (lt - w(12)) / .2; NAMES.forEach(n => mirar(n, 3, 0)); } } });
seg('Es una *nena,* *sola,* atrapada en el *ascensor* *de* *al* *lado.*', { shot: 'rendija', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; FX.nena.rotation.y = -.2 + Math.sin(T * 1.5) * .25; } });
seg('Solo tienen *tres* *cosas:* una *linterna* *sin* *pilas,* un *celular* con *tres* *por* *ciento* de batería y un *rollo* *de* *cinta.*', { shot: 'celu', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.items = [[(lt - w(4)) / .3, (lt - w(8)) / .3, (lt - w(17)) / .3], lt / .3]; S.bat = [3, (lt - w(8)) / .3]; } });
seg('*Grok* quiere *trepar* por la *escotilla* *del* *techo.*', { shot: 'techo', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; talk('grok', T); const u = ISL.grok.bot.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * 2.7); u.head.rotation.x = -.5; } });
seg('Los otros lo *frenan:* en un hueco de ascensor *no* *se* *trepa.* Se espera a *los* *que* *saben.*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; NAMES.filter(n => n !== 'grok').forEach(n => { mirar(n, POS.grok.x, POS.grok.z); talk(n, T, .4); }); later(tag, '⛔ EN UN HUECO DE ASCENSOR NO SE TREPA', (lt - w(4)) / .3, H * .8, '#e8463a', '#fff', 38); } });
seg('*ChatGPT* propone no gastar la batería en *llamadas:* un *solo* *mensaje,* bien *escrito.*', { shot: 'chatgpt', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; talk('chatgpt', T); later(tag, '✉️ UN SOLO MENSAJE', (lt - w(7)) / .3, H * .8, '#2bb59a', '#06110d', 44); } });
seg('*Gemini* mira la *linterna:* sin pilas, *no* *sirve.* Pero la *cinta* *sí.*', { shot: 'gemini', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; talk('gemini', T); S.items = [[1, 1, 1], 1, (lt - w(4)) / .4]; } });
seg('*Claude* le *habla* a la *nena* por la *rendija,* para que *no* *tenga* *miedo,* y le cuenta lo que van haciendo.', { shot: 'rendija', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; mirar('claude', 6, 0); talk('claude', T); FX.nena.rotation.y = -1.2 + Math.sin(T) * .2; } });
seg('Con la *cinta,* arman en el *vidrio* *de* *la* *puerta* un *S.O.S.* *gigante.*', { shot: 'puerta', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; S.bat = [3, 1]; sosK((lt - w(2)) / (w(10) - w(2) + .4)); NAMES.forEach(n => mirar(n, -3, 0)); } });
seg('Y con el *último* *uno* *por* *ciento,* mandan el *mensaje:* ascensor B, piso cuarenta y siete, cuatro adentro y una nena al lado.', { shot: 'celu', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; sosK(1); S.bat = [1, 1]; S.msg = (lt - w(7)) / .35; } });
seg('La *pantalla* *se* *apaga.* *Silencio.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.emer = .5; S.piso = 1; sosK(1); S.bat = [0, 1]; S.celOff = 1; } });
seg('Diez minutos después, *luces* *en* *el* *hueco:* llegan los *bomberos.*', { shot: 'hueco', fx: (lt, p, S, w, T) => { S.emer = 1; S.piso = 1; sosK(1); S.celOff = 1; S.bomb = (lt - w(3)) / .5; later(tag, '🚒 BOMBEROS', (lt - w(9)) / .3, H * .8, '#e8463a', '#fff', 52); NAMES.forEach(n => mirar(n, -3, 0)); } });
seg('Abren las *puertas* con sus *herramientas,* y *salen* *todos.* La *nena* *primero.*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.piso = 1; sosK(1); S.celOff = 1; S.bomb = 1; puertas((lt - w(1)) / 1.5); if (lt > w(6)) { NAMES.forEach((n, i) => cheer(n, T + i)); S.luz = clamp((lt - w(6)) / 1); } later(tag, '✅ TODOS A SALVO', (lt - w(10)) / .3, H * .8, '#2bb59a', '#06110d', 50); } });
seg('Con *tres* *por* *ciento* no se puede hacer *todo:* hay que *elegir* *bien* *qué.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.luz = 1; puertas(1); sosK(1); S.celOff = 1; NAMES.forEach((n, i) => { if (i % 2) cheer(n, T + i); }); } });
seg('¿Vos qué hacías con el *tres* *por* *ciento?*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.luz = 1; puertas(1); sosK(1); S.celOff = 1; later(tag, '¿QUÉ HACÍAS CON EL 3 %? 🤔', lt / .3, H * .66, '#5b2a86', '#fff', 50); } });
seg('Comentá *ENSAYO* y seguime para la *próxima* *historia.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.luz = 1; puertas(1); sosK(1); S.celOff = 1; NAMES.forEach((n, i) => wave(n, T + i)); S.cta = lt / .4; } });
// ---------- timing ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TM.dur + 2.2; s.dur = s.t1 - s.t0; });
for (let i = 0; i < S_.length;) { let j = i; while (j + 1 < S_.length && S_[j + 1].shot === S_[i].shot) j++; for (let k = i; k <= j; k++) { S_[k].sp0 = S_[i].t0; S_[k].sp1 = S_[j].t1; } i = j + 1; }
const TOTAL = S_.at(-1).t1; window.TOTAL = TOTAL;
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, p = clamp(lt / s.dur), w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  idle(T); sosK(0); puertas(0); FX.nena.rotation.y = -.2;
  const sh_ = sh[s.shot], k = ease((T - s.sp0) / (s.sp1 - s.sp0));
  camera.position.copy(sh_.p0).lerp(sh_.p1, k); const look = sh_.l0.clone().lerp(sh_.l1, k); camera.fov = sh_.fov + (sh_.fov1 - sh_.fov) * k; camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();
  const S = { luz: 0 }; LATER = []; if (s.fx) s.fx(lt, p, S, w, T);
  luces(S.luz ?? 0); emergencia(T, S.emer ?? 0); bomberos(S.bomb ?? 0, T); FX.celPant.material.color.set(S.celOff ? 0x050505 : 0x4a7ee6);
  ctx.fillStyle = '#04050a'; ctx.fillRect(0, 0, W, H);
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (S.golpes) golpes(S.golpes, T);
  LATER.forEach(f => f());
  if (S.items) items(...S.items);
  if (S.msg) mensaje(S.msg);
  if (S.cta) drawCTA(S.cta);
  if (S.cover > 0) drawCover(S.cover);
  if (NAMES.includes(s.shot)) pill(ISL[s.shot].label, W / 2, 470, ISL[s.shot].f, '#fff', 44, 1);
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  if (S.piso && !(S.cover > 0) && !NAMES.includes(s.shot)) piso(1);
  if (S.bat && !NAMES.includes(s.shot)) bateria(...S.bat);
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I'].map(f => document.fonts.load(f)).concat([document.fonts.load(`40px ${EMO}`, '🔦📱🧻⛔✉️🚒✅🤔')])).then(() => { build(); cams(); window.READY = true; });
