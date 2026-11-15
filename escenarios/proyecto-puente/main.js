const IAS = { chatgpt: ['ChatGPT', 0x2bb59a, '#14896f'], claude: ['Claude', 0xe5824c, '#cf5f36'], gemini: ['Gemini', 0x4a7ee6, '#2f5fd0'], grok: ['Grok', 0x9aa0ad, '#4b5263'] };
const NAMES = ['chatgpt', 'claude', 'gemini', 'grok'];
const POS = { chatgpt: V(-3.7, 0, -3.4), claude: V(3.7, 0, -3.4), gemini: V(-3.3, 0, 3.4), grok: V(3.3, 0, 3.4) };
const TOP = .45; const flags = []; const ISL = {}; const FX = {};
const EMO = '"Noto Color Emoji"';
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(909);
const IMG = {}; ['luna-cuatro-ia-20261114-portada.jpg', 'tren-sin-conductor-20261115-portada.jpg', 'truco-uruguayo-500-20261113-portada.jpg'].forEach(f => { const i = new Image(); i.src = './' + f; IMG[f] = i; });
function baldosas() { const [c, x] = cv(1024, 1024); x.fillStyle = '#1b2033'; x.fillRect(0, 0, 1024, 1024); for (let i = 0; i < 16; i++) for (let j = 0; j < 16; j++) { const v = 26 + ((i + j) % 2) * 6 + R() * 6 | 0; x.fillStyle = `rgb(${v},${v + 4},${v + 18})`; x.fillRect(i * 64 + 2, j * 64 + 2, 60, 60); } const t = tex(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(10, 10); return t; }
function build() {
  scene.fog = new THREE.Fog(0x070914, 30, 90);
  const suelo = mesh(new THREE.CircleGeometry(60, 96), new THREE.MeshStandardMaterial({ map: baldosas(), roughness: .9 }), [0, 0, 0], scene); suelo.rotation.x = -Math.PI / 2;
  // líneas de "cables" de datos en el piso hacia el buzón
  NAMES.forEach(n => { const p = POS[n]; const len = p.length() - 3.2; const ln = mesh(new THREE.PlaneGeometry(.12, len), new THREE.MeshBasicMaterial({ color: IAS[n][1], transparent: true, opacity: .5 }), [p.x / 2, .02, p.z / 2], scene, false); ln.rotation.x = -Math.PI / 2; ln.rotation.z = Math.atan2(p.x, p.z) + Math.PI; FX['ln_' + n] = ln; });
  // buzón central (GitHub)
  const bz = new THREE.Group(); bz.position.set(0, 0, 0); scene.add(bz); FX.bz = bz;
  mesh(new THREE.CylinderGeometry(1.3, 1.45, .3, 40), M(0x2a2f45), [0, .15, 0], bz);
  mesh(new THREE.CylinderGeometry(.12, .14, 1.6, 12), M(0x3a3f55, { metalness: .5 }), [0, 1.1, 0], bz);
  const caja = mesh(new THREE.BoxGeometry(1.5, 1.0, 1.0), M(0x24292f, { metalness: .3, roughness: .5 }), [0, 2.3, 0], bz);
  mesh(new THREE.CylinderGeometry(.5, .5, 1.5, 24, 1, false, 0, Math.PI), M(0x24292f, { metalness: .3, roughness: .5 }), [0, 2.8, 0], bz).rotation.z = Math.PI / 2;
  const [lc, lx] = cv(512, 256); lx.fillStyle = '#24292f'; lx.fillRect(0, 0, 512, 256); lx.fillStyle = '#fff'; lx.font = '800 96px I'; lx.textAlign = 'center'; lx.textBaseline = 'middle'; lx.fillText('GitHub', 256, 130);
  const lab = mesh(new THREE.PlaneGeometry(1.3, .65), new THREE.MeshBasicMaterial({ map: tex(lc) }), [0, 2.3, .51], bz, false); flags.push([lab, null, null]);
  const ban = new THREE.Group(); ban.position.set(.78, 2.2, 0); bz.add(ban); FX.ban = ban; mesh(new THREE.BoxGeometry(.06, .9, .06), M(0xe8463a), [0, .45, 0], ban); mesh(new THREE.BoxGeometry(.06, .3, .4), M(0xe8463a), [0, .8, .2], ban);
  FX.halo = mesh(new THREE.TorusGeometry(1.7, .05, 8, 80), new THREE.MeshBasicMaterial({ color: 0xffd34d, transparent: true, opacity: 0 }), [0, .35, 0], bz, false); FX.halo.rotation.x = Math.PI / 2;
  // edificios lejanos con ventanas (noche)
  for (let i = 0; i < 22; i++) { const h = 6 + R() * 14, w = 3 + R() * 4; const a = (i / 22) * Math.PI * 2; const r = 34 + R() * 8; const b = mesh(new THREE.BoxGeometry(w, h, w), M(0x141a2c, { roughness: 1 }), [Math.cos(a) * r, h / 2, Math.sin(a) * r - 6], scene, false); b.lookAt(0, h / 2, 0);
    for (let k = 0; k < 6; k++) { const wm = mesh(new THREE.PlaneGeometry(.6, .5), new THREE.MeshBasicMaterial({ color: R() < .5 ? 0xffd77a : 0x2a3350 }), [(R() - .5) * (w - 1), 1 + R() * (h - 2), w / 2 + .02], b, false); } }
  // los 4 círculos
  NAMES.forEach(n => { const [lab, c, f] = IAS[n]; const g = new THREE.Group(); g.position.copy(POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(2.6, 2.85, TOP, 56), M(0x3a3f52, { roughness: .9 }), [0, TOP / 2, 0], g);
    mesh(new THREE.CylinderGeometry(2.4, 2.4, .03, 56), M(0x5a6075, { roughness: .8 }), [0, TOP + .01, 0], g, false);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(3.05, .06, 8, 96), new THREE.MeshBasicMaterial({ color: c })); ring.rotation.x = Math.PI / 2; ring.position.y = .06; g.add(ring);
    const glowR = new THREE.Mesh(new THREE.TorusGeometry(2.42, .04, 8, 96), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .9 })); glowR.rotation.x = Math.PI / 2; glowR.position.y = TOP + .03; g.add(glowR);
    const fp = new THREE.Group(); fp.position.set(-1.7, TOP, -1.5); g.add(fp);
    mesh(new THREE.CylinderGeometry(.03, .03, 2.8, 8), M(0xcfd3dc, { metalness: .6 }), [0, 1.4, 0], fp);
    const fm = mesh(new THREE.PlaneGeometry(1.15, .72), new THREE.MeshStandardMaterial({ map: labelTex(lab, f), side: THREE.DoubleSide }), [.6, 2.4, 0], fp); flags.push([fm, lab, f]);
    const bot = makeBot(c); bot.scale.setScalar(1.25); bot.position.set(-.3, TOP, .3); bot.rotation.y = Math.atan2(-POS[n].x, 9 - POS[n].z) * .7; g.add(bot);
    // escritorio con pantalla
    const prop = new THREE.Group(); prop.position.set(1.1, TOP, .5); g.add(prop); mesh(new THREE.BoxGeometry(1.0, .5, .55), M(0x2a2f45), [0, .25, 0], prop); const sc = mesh(new THREE.PlaneGeometry(.8, .5), new THREE.MeshBasicMaterial({ color: c }), [0, .85, .02], prop, false); mesh(new THREE.BoxGeometry(.86, .56, .04), M(0x111318), [0, .85, -.01], prop); FX['sc_' + n] = sc;
    ISL[n] = { g, bot, ring, glowR, home: bot.position.clone(), rotY: bot.rotation.y, c, css: '#' + c.toString(16).padStart(6, '0'), label: lab, f };
  });
  sun.intensity = 2.2; sun.color.set(0xc4d2ff); sun.position.set(-10, 18, 10); sun.target.position.set(0, 0, 0);
  Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 20, bottom: -20 }); sun.shadow.camera.updateProjectionMatrix();
  hemi.intensity = 1.2; hemi.color.set(0x9fb2e8); hemi.groundColor.set(0x22263a); scene.add(new THREE.AmbientLight(0x8090c0, .4));
  const pl = new THREE.PointLight(0xffd34d, 8, 12); pl.position.set(0, 4, 1); scene.add(pl);
}
// ================= animación =================
let LATER = []; const later = (f, ...a) => LATER.push(() => f(...a));
const STARS2 = Array.from({ length: 380 }, () => [R() * W, R() * H * .5, R() * 1.8 + .3, R()]);
const BW = n => ISL[n].bot.localToWorld(V(0, 0, 0));
const HEAD = n => ISL[n].bot.localToWorld(V(0, 1.45, 0));
function idle(T) { NAMES.forEach((n, i) => { const d = ISL[n], u = d.bot.userData; d.bot.position.copy(d.home); d.bot.rotation.y = d.rotY; u.body.position.y = Math.sin(T * 2 + i) * .02; u.arms.forEach(a => a.rotation.set(0, 0, 0)); u.head.rotation.set(0, Math.sin(T * .6 + i) * .2, 0); u.feet.forEach(f => f.position.y = .08); d.glowR.material.opacity = .9; d.ring.scale.setScalar(1); }); }
function talk(n, T, k = 1) { const u = ISL[n].bot.userData; ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 9)) * .06 * k; u.head.rotation.x = Math.sin(T * 9) * .06; }
function wave(n, T) { ISL[n].bot.userData.arms[1].rotation.z = 2.3 + Math.sin(T * 8) * .35; }
function cheer(n, T) { const u = ISL[n].bot.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * (2.5 + Math.sin(T * 9 + s) * .2)); ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 6)) * .12; }
function encender(k) { NAMES.forEach((n, i) => { const a = clamp(k * 4 - i); ISL[n].glowR.material.opacity = .15 + .85 * a; ISL[n].ring.scale.setScalar(.9 + .1 * pop(a)); ISL[n].ring.material.opacity = 1; FX['sc_' + n].material.color.set(a > .5 ? ISL[n].c : 0x111318); }); }
// ---------- cámaras ----------
const camS = (p0, l0, p1, l1, fov = 52, fov1) => ({ p0, l0, p1: p1 || p0, l1: l1 || l0, fov, fov1: fov1 ?? fov });
function closeOf(n, side = 0) { const b = POS[n].clone(); const dir = V(0, 8.8, 16.6).sub(b).setY(0).normalize(); const perp = V(dir.z, 0, -dir.x); const c = b.clone().add(dir.clone().multiplyScalar(3.6)).add(perp.multiplyScalar(side)); c.y = 2.8; const l = b.clone().add(V(0, 1.4, 0)); return camS(c, l, c.clone().sub(dir.clone().multiplyScalar(.5)), l, 48); }
let sh; function cams() { sh = {
  cover: camS(V(0, 9.5, 17), V(0, 2.4, -1.5), V(0, 8.8, 15.6), V(0, 2.3, -1.5), 60),
  wide: camS(V(-1.4, 8, 14.5), V(0, 2, -1), V(1.4, 7.6, 13.6), V(0, 2, -1), 60),
  top: camS(V(0, 15, 6), V(0, 0, -.5), V(0, 14, 5.2), V(0, 0, -.6), 62),
  buzon: camS(V(2.2, 3.6, 6.2), V(0, 2.4, 0), V(1.6, 3.4, 5.4), V(0, 2.5, 0), 50),
  chatgpt: closeOf('chatgpt', .6), claude: closeOf('claude', -.6), gemini: closeOf('gemini', .6), grok: closeOf('grok', -.6),
}; }
// ---------- overlays ----------
function wrap(text, maxW) { const ws = text.split(' '), L = ['']; ws.forEach(w => { const t = (L.at(-1) + ' ' + w).trim(); if (ctx.measureText(t).width > maxW) L.push(w); else L[L.length - 1] = t; }); return L; }
function tag(text, k, y, bg = 'rgba(8,10,20,.92)', fg = '#fff', size = 40) { pill(text, W / 2, y, bg, fg, size, k); }
function reloj(k, y = H * .66) { const s = pop(clamp(k)); if (s <= 0) return; ctx.save(); ctx.translate(W / 2, y); ctx.scale(s, s); rr(-300, -110, 600, 220, 40); ctx.fillStyle = 'rgba(8,10,20,.94)'; ctx.fill(); ctx.strokeStyle = '#ffd34d'; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = '#ffd34d'; ctx.font = '800 150px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('01:00', 0, 10); ctx.restore(); }
function sobres(k, T) { const a = clamp(k); if (a <= 0) return; const c = proj(V(0, 2.6, 0)); ctx.save(); ctx.font = `64px ${EMO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; NAMES.forEach((n, i) => { const h = proj(HEAD(n)); for (let j = 0; j < 2; j++) { const q = (T * .55 + i * .23 + j * .5) % 1; const ida = (i + j) % 2 === 0; const u = ida ? q : 1 - q; const x = h[0] + (c[0] - h[0]) * u, y = h[1] + (c[1] - h[1]) * u - Math.sin(u * Math.PI) * 120; ctx.globalAlpha = a * Math.sin(q * Math.PI); ctx.fillText('✉️', x, y); } }); ctx.restore(); }
function tarjetas(k, T) { NAMES.forEach((n, i) => { const kk = clamp(k * 3 - i * .45); const s = pop(kk); if (s <= 0) return; let [x, y] = proj(HEAD(n).add(V(0, .9, 0))); x = clamp(x, 190, W - 190); ctx.save(); ctx.translate(x, y - 30 + Math.sin(T * 2 + i) * 6); ctx.scale(s, s); rr(-150, -54, 300, 108, 22); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = ISL[n].css; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = '#111'; ctx.font = '800 30px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('¿QUÉ PASARÍA', 0, -14); ctx.fillText('SI…?', 0, 22); ctx.restore(); }); }
function votos(k, T) { NAMES.forEach((n, i) => { const kk = clamp(k * 3 - i * .4); const s = pop(kk); if (s <= 0) return; const [x, y] = proj(HEAD(n).add(V(0, .7, 0))); ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.beginPath(); ctx.arc(0, 0, 50, 0, 7); ctx.fillStyle = ISL[n].css; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-20, 0); ctx.lineTo(-5, 16); ctx.lineTo(22, -16); ctx.stroke(); ctx.restore(); }); }
function portada(f, k, x = W / 2, y = H * .63, w = 470, rot = 0) { const s = pop(clamp(k)); const im = IMG[f]; if (s <= 0 || !im || !im.complete) return; const h = w * 16 / 9; ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 40; rr(-w / 2 - 10, -h / 2 - 10, w + 20, h + 20, 26); ctx.fillStyle = '#fff'; ctx.fill(); ctx.shadowBlur = 0; ctx.save(); rr(-w / 2, -h / 2, w, h, 18); ctx.clip(); ctx.drawImage(im, -w / 2, -h / 2, w, h); ctx.restore(); ctx.restore(); }
function rol(n, emo, txt, k) { const s = pop(clamp(k)); if (s <= 0) return; let [x, y] = proj(HEAD(n).add(V(0, .8, 0))); ctx.font = '800 34px I'; const w = ctx.measureText(txt).width + 120; x = clamp(x, w / 2 + 30, W - w / 2 - 30); ctx.save(); ctx.translate(x, y); ctx.scale(s, s); rr(-w / 2, -48, w, 96, 30); ctx.fillStyle = 'rgba(8,10,20,.94)'; ctx.fill(); ctx.strokeStyle = ISL[n].css; ctx.lineWidth = 5; ctx.stroke(); ctx.font = `48px ${EMO}`; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(emo, -w / 2 + 18, 4); ctx.font = '800 34px I'; ctx.fillStyle = '#fff'; ctx.fillText(txt, -w / 2 + 84, 4); ctx.restore(); }
function drawCover(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const g = ctx.createLinearGradient(0, H * .5, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.3, 'rgba(0,0,6,.82)'); g.addColorStop(1, 'rgba(0,0,6,.96)'); ctx.fillStyle = g; ctx.fillRect(0, H * .5, W, H * .5);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 58px I'; ctx.fillStyle = '#fff'; ctx.fillText('ChatGPT · Claude · Gemini · Grok', W / 2, H * .69); ctx.font = '800 112px I'; ctx.fillStyle = '#ffd34d'; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.fillText('CONECTÉ 4 IA', W / 2, H * .77); ctx.font = '800 70px I'; ctx.fillStyle = '#9fc4ff'; ctx.fillText('y trabajan juntas', W / 2, H * .835); ctx.fillText('cada madrugada', W / 2, H * .885); ctx.restore(); }
function drawCTA(k) { const s2 = pop(clamp(k)); if (s2 <= 0) return; ctx.save(); ctx.translate(W / 2, H * .7); ctx.scale(s2, s2); rr(-430, -140, 860, 280, 36); ctx.fillStyle = '#ffd34d'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 42px I'; ctx.fillText('SEGUIME PARA LA DE ESTA NOCHE', 0, -58); ctx.font = '800 82px I'; ctx.fillText('Comentá tu historia', 0, 42); ctx.restore(); ctx.font = '800 38px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText('@gostudiouy', W / 2, H * .815); }
// ---------- segmentos ----------
const S_ = []; function seg(text, opt = {}) { S_.push(Object.assign({ text }, opt)); }
seg('Tengo *cuatro* *inteligencias* *artificiales* trabajando *juntas* cada *madrugada,* y a veces ni yo entiendo cómo lo *logran.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.cover = clamp(1 - (lt - w(6)) / .4); encender((lt - .2) / 1.4); if (lt > w(6)) later(reloj, (lt - w(6)) / .35, H * .66); } });
seg('*ChatGPT,* *Claude,* *Gemini* y *Grok.*', { shot: 'wide', fx: (lt, p, S, w, T) => { encender(1); [0, 1, 2, 4].forEach((wi, i) => { if (lt > w(wi) - .05) { const n = NAMES[i]; if (lt < w(wi) + .9) { talk(n, T); wave(n, T); } const [x, y] = proj(HEAD(n).add(V(0, .85, 0))); later(pill, ISL[n].label, x, y, ISL[n].f, '#fff', 40, (lt - w(wi)) / .25); } }); } });
seg('Les di un *buzón* *compartido* en *GitHub:* es su *oficina.* Ahí se dejan *mensajes* y *archivos.*', { shot: 'buzon', fx: (lt, p, S, w, T) => { encender(1); FX.halo.material.opacity = .9 * clamp(lt / .4); S.sobres = (lt - w(8)) / .3; FX.ban.rotation.z = lt > w(8) ? -Math.min(1.4, (lt - w(8)) * 3) : 0; later(tag, '📬 SU OFICINA: UN BUZÓN EN GITHUB', (lt - w(3)) / .3, H * .8); } });
seg('A la *una,* una *tarea* *programada* de *ChatGPT* arranca la *ronda:*', { shot: 'chatgpt', fx: (lt, p, S, w, T) => { encender(1); talk('chatgpt', T); later(reloj, lt / .3, H * .66); if (lt > w(6)) wave('chatgpt', T); } });
seg('cada una *propone* una historia de *«¿qué* *pasaría* *si?».*', { shot: 'wide', fx: (lt, p, S, w, T) => { encender(1); S.tarj = (lt - w(2)) / 1.0; NAMES.forEach((n, i) => { if (lt > w(2) + i * .25 && lt < w(2) + i * .25 + .8) talk(n, T); }); } });
seg('*Votan,* y gana la *mayoría.*', { shot: 'top', fx: (lt, p, S, w, T) => { encender(1); S.votos = lt / .9; } });
seg('Anoche *ganó* el *tren* *sin* *conductor.*', { shot: 'top', fx: (lt, p, S, w, T) => { encender(1); later(portada, 'tren-sin-conductor-20261115-portada.jpg', lt / .35); later(tag, '🏆 GANÓ: EL TREN SIN CONDUCTOR', (lt - w(1)) / .3, H * .885, '#ffd34d', '#1a1206', 40); } });
seg('Después se *reparten* *el* *trabajo:* *Gemini* pone la *voz,* *Claude* arma el *video* *en* *3D* y *ChatGPT* lo *publica.*', { shot: 'wide', fx: (lt, p, S, w, T) => { encender(1); [['gemini', 5, '🎙️', 'VOZ'], ['claude', 9, '🎬', 'VIDEO 3D'], ['chatgpt', 15, '📲', 'PUBLICA']].forEach(([n, wi, e, t]) => { if (lt > w(wi)) { later(rol, n, e, t, (lt - w(wi)) / .3); if (lt < w(wi) + 1) talk(n, T); } }); } });
seg('Y las *historias,* las *voces* y los *videos* que ves en esta cuenta los hacen *ellas.*', { shot: 'cover', fx: (lt, p, S, w, T) => { encender(1); later(portada, 'luna-cuatro-ia-20261114-portada.jpg', (lt - w(1)) / .35, W * .26, H * .62, 330, -.12); later(portada, 'truco-uruguayo-500-20261113-portada.jpg', (lt - w(4)) / .35, W * .74, H * .62, 330, .12); later(portada, 'tren-sin-conductor-20261115-portada.jpg', (lt - w(7)) / .35, W / 2, H * .64, 360, 0); if (lt > w(14)) NAMES.forEach((n, i) => cheer(n, T + i)); } });
seg('*Seguime* para ver qué inventan esta *noche,* y *comentá* qué historia querés que *voten.*', { shot: 'cover', fx: (lt, p, S, w, T) => { encender(1); NAMES.forEach((n, i) => { wave(n, T + i); }); S.cta = lt / .4; } });
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
  idle(T); encender(0); FX.halo.material.opacity = 0; FX.ban.rotation.z = 0;
  const sh_ = sh[s.shot], k = ease((T - s.sp0) / (s.sp1 - s.sp0));
  camera.position.copy(sh_.p0).lerp(sh_.p1, k); const look = sh_.l0.clone().lerp(sh_.l1, k); camera.fov = sh_.fov + (sh_.fov1 - sh_.fov) * k; camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();
  const S = {}; LATER = []; if (s.fx) s.fx(lt, p, S, w, T);
  const g = ctx.createLinearGradient(0, 0, 0, H * .55); g.addColorStop(0, '#02030a'); g.addColorStop(1, '#0b1228'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (const [x, y, r, a] of STARS2) { ctx.globalAlpha = .3 + a * .7 * (.8 + .2 * Math.sin(T * 2 + a * 9)); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (S.sobres) sobres(S.sobres, T);
  if (S.tarj) tarjetas(S.tarj, T);
  if (S.votos) votos(S.votos, T);
  LATER.forEach(f => f());
  if (S.cta) drawCTA(S.cta);
  if (S.cover > 0) drawCover(S.cover);
  if (NAMES.includes(s.shot)) pill(ISL[s.shot].label, W / 2, 470, ISL[s.shot].f, '#fff', 44, 1);
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I'].map(f => document.fonts.load(f)).concat([document.fonts.load(`40px ${EMO}`, '✉️📬🎙️🎬📲🏆')], Object.values(IMG).map(i => i.decode().catch(() => {})))).then(() => { build(); cams(); flags.forEach(([m, l, f]) => { if (l) { m.material.map = labelTex(l, f); m.material.needsUpdate = true; } }); window.READY = true; });
