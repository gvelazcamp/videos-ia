const IAS = { chatgpt: ['ChatGPT', 0x2bb59a, '#14896f'], claude: ['Claude', 0xe5824c, '#cf5f36'], gemini: ['Gemini', 0x4a7ee6, '#2f5fd0'] };
const NAMES = ['chatgpt', 'claude', 'gemini'];
const POS = { chatgpt: V(-4.3, 0, -.6), claude: V(4.3, 0, -.6), gemini: V(0, 0, -6.6) };
const TOP = .45; const flags = []; const ISL = {}; const FX = {};
const EMO = '"Noto Color Emoji"';
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(1234);
// ======= datos reales (resultado.md) =======
const TURNOS = [
  { desc: 'chatgpt', adiv: 'claude', dado: 1, pistas: ['Infusión que compartimos en ronda, con bombilla y agua caliente', 'Paseo muy largo que bordea la costa de Montevideo', 'En carnaval canta un coro con maquillaje, bombo, platillos y redoblante', 'Comida de parrilla, brasas y cortes de carne; típica de los domingos', 'Recipiente portátil que mantiene el agua caliente durante horas'], resp: ['Mate', 'Rambla', 'Murga', 'Asado', 'Termo'], sol: ['Mate', 'Rambla', 'Murga', 'Asado', 'Termo'], ok: [1, 1, 1, 1, 1], pts: 4 },
  { desc: 'claude', adiv: 'gemini', dado: 1, pistas: ['Sándwich uruguayo enorme, con lomito, jamón, queso, huevo y panceta', 'Ritmo afrouruguayo de tambores que sale por los barrios en las Llamadas', 'Masa que se cocina en grasa bien caliente y se come los días de lluvia', 'Así le decimos en la calle al ómnibus: lo esperás en la parada', 'Mercado al aire libre en la calle; la de Tristán Narvaja es la más famosa'], resp: ['Chivito', 'Candombe', 'Torta frita', 'Bondi', 'Feria'], sol: ['Chivito', 'Candombe', 'Tortafrita', 'Bondi', 'Feria'], ok: [1, 1, 1, 1, 1], pts: 4 },
  { desc: 'gemini', adiv: 'chatgpt', dado: 2, pistas: ['El que se hace el distraído o esquiva el bulto cuando hay que trabajar', 'Lo que sentís cuando alguien te cuenta un chisme jugoso', 'Quedarse sin dinero o estar en una situación económica muy apretada', 'Esa persona muy amiga tuya, con la que tenés total confianza', 'Cuando algo te genera una pereza absoluta o un desgano total'], resp: ['Vago', 'Intriga', 'Estar seco', 'Compinche', 'Fiaca'], sol: ['Bagayero', 'Morbo', 'Patas', 'Yunta', 'Fiaca'], ok: [0, 0, 0, 0, 1], pts: 0 },
];
function baldosas() { const [c, x] = cv(1024, 1024); x.fillStyle = '#1d1630'; x.fillRect(0, 0, 1024, 1024); for (let i = 0; i < 16; i++) for (let j = 0; j < 16; j++) { const v = 30 + ((i + j) % 2) * 8 + R() * 6 | 0; x.fillStyle = `rgb(${v + 8},${v},${v + 22})`; x.fillRect(i * 64 + 2, j * 64 + 2, 60, 60); } const t = tex(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(10, 10); return t; }
function caraDado(n) { const [c, x] = cv(256, 256); x.fillStyle = '#fafafa'; x.fillRect(0, 0, 256, 256); x.fillStyle = '#e8463a'; x.font = '800 190px I'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(String(n), 128, 140); return tex(c); }
function build() {
  scene.fog = new THREE.Fog(0x0b0718, 30, 90);
  const suelo = mesh(new THREE.CircleGeometry(60, 96), new THREE.MeshStandardMaterial({ map: baldosas(), roughness: .9 }), [0, 0, 0], scene); suelo.rotation.x = -Math.PI / 2;
  // mesa central con reloj de arena y dado
  const mesa = new THREE.Group(); mesa.position.set(0, 0, -2.6); scene.add(mesa);
  mesh(new THREE.CylinderGeometry(1.6, 1.8, .9, 40), M(0x3b2a52, { roughness: .6 }), [0, .45, 0], mesa);
  mesh(new THREE.CylinderGeometry(1.75, 1.75, .08, 40), M(0xffd34d, { metalness: .6, roughness: .3 }), [0, .93, 0], mesa);
  const rel = new THREE.Group(); rel.position.set(-.55, .97, 0); mesa.add(rel); FX.rel = rel;
  const vid = new THREE.MeshPhysicalMaterial({ color: 0xdff2ff, transparent: true, opacity: .35, roughness: .05 });
  mesh(new THREE.ConeGeometry(.42, .7, 24, 1, true), vid, [0, .45, 0], rel, false).rotation.x = Math.PI; mesh(new THREE.ConeGeometry(.42, .7, 24, 1, true), vid, [0, 1.15, 0], rel, false);
  for (const y of [.05, 1.55]) mesh(new THREE.CylinderGeometry(.52, .52, .1, 24), M(0x8b5a2b), [0, y, 0], rel);
  FX.arenaA = mesh(new THREE.ConeGeometry(.36, .55, 24), M(0xf2c230, { emissive: 0x4a3600, emissiveIntensity: .4 }), [0, 1.08, 0], rel, false); FX.arenaA.rotation.x = Math.PI;
  FX.arenaB = mesh(new THREE.ConeGeometry(.36, .55, 24), M(0xf2c230, { emissive: 0x4a3600, emissiveIntensity: .4 }), [0, .37, 0], rel, false);
  FX.hilo = mesh(new THREE.CylinderGeometry(.02, .02, .7, 6), M(0xf2c230), [0, .8, 0], rel, false);
  FX.dmats = [0, 1, 2].map(n => new THREE.MeshStandardMaterial({ map: caraDado(n), roughness: .4 }));
  FX.dado = new THREE.Mesh(new THREE.BoxGeometry(.8, .8, .8), [FX.dmats[1], FX.dmats[1], FX.dmats[0], FX.dmats[0], FX.dmats[2], FX.dmats[2]]); /* dado de Contra Reloj: 0, 1 o 2 */ FX.dado.position.set(.65, 1.37, .1); FX.dado.castShadow = true; mesa.add(FX.dado);
  // gradas/luces de show
  for (let i = 0; i < 18; i++) { const a = Math.PI * (.15 + .7 * i / 17); const r = 22; const h = 2 + R() * 6; mesh(new THREE.BoxGeometry(2.5, h, 2.5), M(0x1a1230), [Math.cos(a) * r * (i % 2 ? 1 : -1) * .2 + (i - 9) * 2.4, h / 2, -20 - R() * 4], scene, false); }
  FX.spots = []; [[-6, 0xff5ea8], [0, 0xffd34d], [6, 0x5ec8ff]].forEach(([x, c]) => { const sp = new THREE.SpotLight(c, 40, 30, .35, .6, 1); sp.position.set(x, 12, 4); sp.target.position.set(0, 0, -2.6); scene.add(sp, sp.target); FX.spots.push(sp); });
  NAMES.forEach(n => { const [lab, c, f] = IAS[n]; const g = new THREE.Group(); g.position.copy(POS[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(2.4, 2.65, TOP, 56), M(0x3a3352, { roughness: .9 }), [0, TOP / 2, 0], g);
    mesh(new THREE.CylinderGeometry(2.2, 2.2, .03, 56), M(0x5a5277, { roughness: .8 }), [0, TOP + .01, 0], g, false);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(2.85, .06, 8, 96), new THREE.MeshBasicMaterial({ color: c })); ring.rotation.x = Math.PI / 2; ring.position.y = .06; g.add(ring);
    const glowR = new THREE.Mesh(new THREE.TorusGeometry(2.22, .045, 8, 96), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .9 })); glowR.rotation.x = Math.PI / 2; glowR.position.y = TOP + .03; g.add(glowR);
    const fp = new THREE.Group(); fp.position.set(-1.5, TOP, -1.3); g.add(fp);
    mesh(new THREE.CylinderGeometry(.03, .03, 2.8, 8), M(0xcfd3dc, { metalness: .6 }), [0, 1.4, 0], fp);
    const fm = mesh(new THREE.PlaneGeometry(1.15, .72), new THREE.MeshStandardMaterial({ map: labelTex(lab, f), side: THREE.DoubleSide }), [.6, 2.4, 0], fp); flags.push([fm, lab, f]);
    const bot = makeBot(c); bot.scale.setScalar(1.3); bot.position.set(0, TOP, .2); bot.rotation.y = Math.atan2(-POS[n].x, 14 - POS[n].z); g.add(bot);
    // atril con pulsador
    const at = new THREE.Group(); at.position.set(1.0, TOP, .9); g.add(at); mesh(new THREE.BoxGeometry(.7, .8, .5), M(0x241c3a), [0, .4, 0], at); FX['btn_' + n] = mesh(new THREE.CylinderGeometry(.2, .22, .12, 20), M(c, { emissive: c, emissiveIntensity: .4 }), [0, .86, 0], at);
    ISL[n] = { g, bot, ring, glowR, home: bot.position.clone(), rotY: bot.rotation.y, c, css: '#' + c.toString(16).padStart(6, '0'), label: lab, f };
  });
  sun.intensity = 1.9; sun.color.set(0xd8d0ff); sun.position.set(-8, 18, 12); sun.target.position.set(0, 0, -2);
  Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16 }); sun.shadow.camera.updateProjectionMatrix();
  hemi.intensity = 1.15; hemi.color.set(0xb0a8e8); hemi.groundColor.set(0x241c3a); scene.add(new THREE.AmbientLight(0x9080c0, .35));
}
// ======= animación =======
let LATER = []; const later = (f, ...a) => LATER.push(() => f(...a));
const STARS2 = Array.from({ length: 260 }, () => [R() * W, R() * H * .5, R() * 1.8 + .3, R()]);
const HEAD = n => ISL[n].bot.localToWorld(V(0, 1.45, 0));
function idle(T) { NAMES.forEach((n, i) => { const d = ISL[n], u = d.bot.userData; d.bot.position.copy(d.home); d.bot.rotation.y = d.rotY; u.body.position.y = Math.sin(T * 2 + i) * .02; u.arms.forEach(a => a.rotation.set(0, 0, 0)); u.head.rotation.set(0, Math.sin(T * .6 + i) * .2, 0); d.glowR.material.opacity = .6; }); }
function talk(n, T, k = 1) { const u = ISL[n].bot.userData; ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 9)) * .06 * k; u.head.rotation.x = Math.sin(T * 9) * .06; ISL[n].glowR.material.opacity = 1; }
function wave(n, T) { ISL[n].bot.userData.arms[1].rotation.z = 2.3 + Math.sin(T * 8) * .35; }
function cheer(n, T) { const u = ISL[n].bot.userData; u.arms.forEach((a, s) => a.rotation.z = (s ? 1 : -1) * (2.5 + Math.sin(T * 9 + s) * .2)); ISL[n].bot.position.y = ISL[n].home.y + Math.abs(Math.sin(T * 6)) * .12; }
function sad(n, T) { const u = ISL[n].bot.userData; u.head.rotation.x = .35; u.arms.forEach((a, s) => a.rotation.z = (s ? -1 : 1) * .2); }
const DROT = { 0: [0, 0, 0], 1: [0, 0, Math.PI / 2], 2: [-Math.PI / 2, 0, 0] }; // cara arriba
function dado3D(n, k, T) { const d = FX.dado; if (n == null) { d.rotation.set(.3, T * .4, .2); d.position.y = 1.37; return; } const kk = clamp(k); const r = DROT[n]; if (kk < 1) { d.rotation.set(r[0] + (1 - kk) * 12, r[1] + (1 - kk) * 9, r[2] + (1 - kk) * 7); d.position.y = 1.37 + Math.abs(Math.sin(kk * Math.PI * 3)) * (1 - kk) * 1.6; } else { d.rotation.set(...r); d.position.y = 1.37; } }
function arena(q) { q = clamp(q); FX.arenaA.scale.setScalar(Math.max(.02, 1 - q)); FX.arenaB.scale.setScalar(Math.max(.02, q)); FX.hilo.visible = q > 0 && q < 1; }
// ---------- cámaras ----------
const camS = (p0, l0, p1, l1, fov = 52, fov1) => ({ p0, l0, p1: p1 || p0, l1: l1 || l0, fov, fov1: fov1 ?? fov });
function closeOf(n, side = 0) { const b = POS[n].clone(); const dir = V(0, 8, 14).sub(b).setY(0).normalize(); const perp = V(dir.z, 0, -dir.x); const c = b.clone().add(dir.clone().multiplyScalar(6.2)).add(perp.multiplyScalar(side)); c.y = 3.3; const l = b.clone().add(V(0, .55, 0)); return camS(c, l, c.clone().sub(dir.clone().multiplyScalar(.5)), l, 48); }
let sh; function cams() { sh = {
  cover: camS(V(0, 8.5, 12.5), V(0, 1.6, -3), V(0, 8, 11.4), V(0, 1.6, -3.2), 60),
  wide: camS(V(-1.5, 7.6, 11), V(0, 1.6, -3), V(1.5, 7.2, 10.2), V(0, 1.6, -3), 60),
  mesa: camS(V(2.8, 4.4, 3.4), V(0, 1.7, -2.6), V(2.3, 4.1, 2.7), V(0, 1.8, -2.6), 48),
  chatgpt: closeOf('chatgpt', .5), claude: closeOf('claude', -.5), gemini: closeOf('gemini', .4),
}; }
// ---------- overlays ----------
function wrapL(text, maxW) { const ws = text.split(' '), L = ['']; ws.forEach(w => { const t = (L.at(-1) + ' ' + w).trim(); if (ctx.measureText(t).width > maxW) L.push(w); else L[L.length - 1] = t; }); return L; }
function tag(text, k, y, bg = 'rgba(8,10,20,.92)', fg = '#fff', size = 40) { pill(text, W / 2, y, bg, fg, size, k); }
let SCORE = { chatgpt: null, claude: null, gemini: null };
function marcador(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; NAMES.forEach((n, i) => { const x = W / 2 + (i - 1) * 330, y = 520; rr(x - 150, y - 46, 300, 92, 24); ctx.fillStyle = 'rgba(8,10,20,.9)'; ctx.fill(); ctx.strokeStyle = ISL[n].css; ctx.lineWidth = 4; ctx.stroke(); ctx.fillStyle = '#fff'; ctx.font = '800 34px I'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(ISL[n].label, x - 128, y + 2); ctx.fillStyle = SCORE[n] == null ? 'rgba(255,255,255,.35)' : '#ffd34d'; ctx.font = '800 46px I'; ctx.textAlign = 'right'; ctx.fillText(SCORE[n] == null ? '–' : String(SCORE[n]), x + 128, y + 4); }); ctx.restore(); }
function tarjeta(t, k, revs, T) { const a = clamp(k); if (a <= 0) return; const tu = TURNOS[t]; const y0 = H * .555, rh = 118; ctx.save(); ctx.globalAlpha = a; rr(50, y0, W - 100, 110 + rh * 5, 30); ctx.fillStyle = 'rgba(8,10,20,.93)'; ctx.fill(); ctx.strokeStyle = '#ffd34d'; ctx.lineWidth = 4; ctx.stroke();
  ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.font = '800 34px I'; ctx.fillStyle = ISL[tu.desc].css; ctx.fillText(ISL[tu.desc].label.toUpperCase() + ' DESCRIBE', 90, y0 + 52); ctx.fillStyle = '#fff'; ctx.fillText('→', 470, y0 + 52); ctx.fillStyle = ISL[tu.adiv].css; ctx.fillText(ISL[tu.adiv].label.toUpperCase() + ' ADIVINA', 520, y0 + 52);
  for (let r = 0; r < 5; r++) { const y = y0 + 110 + r * rh; ctx.strokeStyle = 'rgba(255,255,255,.12)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(80, y); ctx.lineTo(W - 80, y); ctx.stroke();
    ctx.fillStyle = '#ffd34d'; ctx.beginPath(); ctx.arc(110, y + rh / 2, 26, 0, 7); ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.font = '800 30px I'; ctx.textAlign = 'center'; ctx.fillText(String(r + 1), 110, y + rh / 2 + 2);
    ctx.textAlign = 'left'; ctx.font = '500 27px I'; ctx.fillStyle = 'rgba(230,230,245,.92)'; const L = wrapL('«' + tu.pistas[r] + '»', 560).slice(0, 3); L.forEach((l, j) => ctx.fillText(l, 152, y + rh / 2 + (j - (L.length - 1) / 2) * 31));
    const kr = clamp((T - revs[r]) / .3); const bx = 735, bw = 260; rr(bx, y + 16, bw, rh - 32, 18); ctx.fillStyle = kr > 0 ? (tu.ok[r] ? 'rgba(43,181,154,.25)' : 'rgba(232,70,58,.25)') : 'rgba(255,255,255,.07)'; ctx.fill(); ctx.strokeStyle = kr > 0 ? (tu.ok[r] ? '#2bb59a' : '#e8463a') : 'rgba(255,255,255,.25)'; ctx.stroke();
    if (kr > 0) { ctx.save(); ctx.globalAlpha = a * kr; ctx.textAlign = 'center'; ctx.fillStyle = '#fff'; ctx.font = '800 34px I'; ctx.fillText(tu.resp[r], bx + bw / 2 - 18, y + rh / 2 - (tu.ok[r] ? 0 : 14)); if (!tu.ok[r]) { ctx.font = '700 24px I'; ctx.fillStyle = '#ffb3ab'; ctx.fillText('era ' + tu.sol[r], bx + bw / 2 - 18, y + rh / 2 + 22); } ctx.font = `40px ${EMO}`; ctx.fillText(tu.ok[r] ? '✅' : '❌', bx + bw - 30, y + rh / 2); ctx.restore(); } }
  ctx.restore(); }
function dado2D(n, k) { const s = pop(clamp(k)); if (s <= 0) return; ctx.save(); ctx.translate(W - 170, 680); ctx.scale(s, s); ctx.rotate(-.12); rr(-80, -80, 160, 160, 28); ctx.fillStyle = '#fafafa'; ctx.fill(); ctx.strokeStyle = '#e8463a'; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = '#e8463a'; ctx.font = '800 120px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(String(n), 0, 6); ctx.restore(); ctx.save(); ctx.globalAlpha = clamp(k); ctx.fillStyle = '#ffd34d'; ctx.font = '800 32px I'; ctx.textAlign = 'center'; ctx.fillText(n ? 'RESTA ' + n : 'NO RESTA', W - 170, 800); ctx.restore(); }
function relojito(q, k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.translate(160, 680); ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(-50, -80); ctx.lineTo(50, -80); ctx.lineTo(4, 0); ctx.lineTo(50, 80); ctx.lineTo(-50, 80); ctx.lineTo(-4, 0); ctx.closePath(); ctx.stroke(); q = clamp(q); ctx.fillStyle = '#f2c230'; const ht = 70 * (1 - q); ctx.beginPath(); ctx.moveTo(-50 * ht / 80, -ht + 0); ctx.lineTo(50 * ht / 80, -ht); ctx.lineTo(0, -2); ctx.closePath(); if (ht > 1) ctx.fill(); const hb = 70 * q; ctx.beginPath(); ctx.moveTo(-50, 78); ctx.lineTo(50, 78); ctx.lineTo(50 - 46 * hb / 80, 78 - hb); ctx.lineTo(-50 + 46 * hb / 80, 78 - hb); ctx.closePath(); ctx.fill(); ctx.font = '700 22px I'; ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.textAlign = 'center'; ctx.fillText('reloj recreado', 0, 110); ctx.restore(); }
function drawCover(k) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const g = ctx.createLinearGradient(0, H * .5, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.3, 'rgba(6,0,10,.82)'); g.addColorStop(1, 'rgba(6,0,10,.96)'); ctx.fillStyle = g; ctx.fillRect(0, H * .5, W, H * .5);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 60px I'; ctx.fillStyle = '#fff'; ctx.fillText('ChatGPT · Claude · Gemini', W / 2, H * .69); ctx.font = '800 120px I'; ctx.fillStyle = '#ffd34d'; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.fillText('CONTRARRELOJ', W / 2, H * .775); ctx.font = '800 64px I'; ctx.fillStyle = '#ffb3ab'; ctx.fillText('¿y si el dado te resta puntos?', W / 2, H * .85); ctx.restore(); }
function podio(k) { const a = clamp(k); if (a <= 0) return; const y0 = H * .58; ctx.save(); ctx.globalAlpha = a; [['claude', 4, -1, 300], ['gemini', 4, 0, 300], ['chatgpt', 0, 1, 120]].forEach(([n, p, pos, h], i) => { const kk = pop(clamp(k * 2 - i * .3)); const x = W / 2 + pos * 300; const hh = h * kk; rr(x - 130, y0 + 420 - hh, 260, hh, 18); ctx.fillStyle = ISL[n].css; ctx.fill(); ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 40px I'; ctx.fillText(ISL[n].label, x, y0 + 420 - hh - 40); ctx.font = '800 80px I'; if (hh > 90) ctx.fillText(String(p), x, y0 + 420 - hh / 2); if (i < 2 && kk > .9) { ctx.font = `80px ${EMO}`; ctx.fillText('🏆', x, y0 + 420 - hh - 110); } }); ctx.restore(); }
function drawCTA(k) { const s2 = pop(clamp(k)); if (s2 <= 0) return; ctx.save(); ctx.translate(W / 2, H * .7); ctx.scale(s2, s2); rr(-440, -140, 880, 280, 36); ctx.fillStyle = '#ffd34d'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 44px I'; ctx.fillText('¿CUÁNTAS ADIVINABAS?', 0, -58); ctx.font = '800 64px I'; ctx.fillText('Comentá CONTRARRELOJ', 0, 42); ctx.restore(); ctx.font = '800 38px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText('@gostudiouy', W / 2, H * .815); }
// ---------- segmentos ----------
const S_ = []; function seg(text, opt = {}) { S_.push(Object.assign({ text }, opt)); }
// rv: [fila, palabra-respuesta] → la fila se revela al decir esa palabra
seg('Puse a *ChatGPT,* *Claude* y *Gemini* a jugar *Contrarreloj.* ¿Quién gana si el *dado* te *resta* *puntos?*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.cover = clamp(1 - (lt - w(7)) / .4); [2, 3, 5].forEach((wi, i) => { if (lt > w(wi) && lt < w(wi) + 1) { talk(NAMES[i], T); wave(NAMES[i], T); } }); S.d3 = [null]; } });
seg('Una *tarjeta* de *cinco* *palabras,* un *reloj* *de* *arena* y un *dado* que resta *cero,* *uno* *o* *dos.*', { shot: 'mesa', fx: (lt, p, S, w, T) => { S.d3 = [null]; arena(lt / 4); } });
seg('*Primer* *turno:* *ChatGPT* describe y *Claude* adivina. El dado sale *uno.*', { shot: 'mesa', turno: 0, fx: (lt, p, S, w, T) => { S.d3 = [1, (lt - w(8)) / .9]; arena(0); if (lt > w(9)) later(dado2D, 1, (lt - w(9)) / .3); S.marc = 1; } });
seg('Infusión en ronda, con bombilla: *mate.* Paseo por la costa: *rambla.*', { shot: 'claude', turno: 0, card: 1, rv: [[0, 'mate.'], [1, 'rambla.']], fx: (lt, p, S, w, T) => { talk('claude', T); S.marc = 1; S.dado = 1; } });
seg('Coro de carnaval: *murga.* Parrilla del domingo: *asado.* Y lo que mantiene el agua caliente: *termo.*', { shot: 'wide', turno: 0, card: 1, rv: [[2, 'murga.'], [3, 'asado.'], [4, 'termo.']], fx: (lt, p, S, w, T) => { talk('chatgpt', T, .5); S.marc = 1; S.dado = 1; } });
seg('*Cinco* *de* *cinco.* Menos uno del dado: *Claude* *suma* *cuatro.*', { shot: 'claude', turno: 0, card: 1, sc: [['claude', 4, 'cuatro.']], fx: (lt, p, S, w, T) => { cheer('claude', T); S.marc = 1; S.dado = 1; } });
seg('*Segundo* *turno:* *Claude* describe y *Gemini* adivina. El dado sale *uno.*', { shot: 'mesa', turno: 1, fx: (lt, p, S, w, T) => { S.d3 = [1, (lt - w(8)) / .9]; arena(0); if (lt > w(9)) later(dado2D, 1, (lt - w(9)) / .3); S.marc = 1; } });
seg('Sándwich enorme con huevo y panceta: *chivito.* Tambores en las Llamadas: *candombe.*', { shot: 'gemini', turno: 1, card: 1, rv: [[0, 'chivito.'], [1, 'candombe.']], fx: (lt, p, S, w, T) => { talk('gemini', T); S.marc = 1; S.dado = 1; } });
seg('Masa de los días de lluvia: *torta* *frita.* El ómnibus: *bondi.* Y el mercado de Tristán Narvaja: *feria.*', { shot: 'wide', turno: 1, card: 1, rv: [[2, 'frita.'], [3, 'bondi.'], [4, 'feria.']], fx: (lt, p, S, w, T) => { talk('claude', T, .5); S.marc = 1; S.dado = 1; } });
seg('Otra vez *cinco* *de* *cinco.* Menos uno: *Gemini* también *suma* *cuatro.*', { shot: 'gemini', turno: 1, card: 1, sc: [['gemini', 4, 'cuatro.']], fx: (lt, p, S, w, T) => { cheer('gemini', T); S.marc = 1; S.dado = 1; } });
seg('*Tercer* *turno:* *Gemini* describe y *ChatGPT* adivina. Y el dado sale *dos.*', { shot: 'mesa', turno: 2, fx: (lt, p, S, w, T) => { S.d3 = [2, (lt - w(9)) / .9]; arena(0); if (lt > w(10)) later(dado2D, 2, (lt - w(10)) / .3); S.marc = 1; } });
seg('El que esquiva el bulto: *ChatGPT* dijo *vago;* era *bagayero.*', { shot: 'chatgpt', turno: 2, card: 1, rv: [[0, 'vago;']], fx: (lt, p, S, w, T) => { talk('chatgpt', T); S.marc = 1; S.dado = 2; } });
seg('El chisme jugoso: dijo *intriga;* era *morbo.*', { shot: 'wide', turno: 2, card: 1, rv: [[1, 'intriga;']], fx: (lt, p, S, w, T) => { S.marc = 1; S.dado = 2; } });
seg('Quedarse sin plata: dijo *estar* *seco;* era *patas.*', { shot: 'chatgpt', turno: 2, card: 1, rv: [[2, 'seco;']], fx: (lt, p, S, w, T) => { sad('chatgpt', T); S.marc = 1; S.dado = 2; } });
seg('El amigo de confianza: dijo *compinche;* era *yunta.*', { shot: 'wide', turno: 2, card: 1, rv: [[3, 'compinche;']], fx: (lt, p, S, w, T) => { sad('chatgpt', T); S.marc = 1; S.dado = 2; } });
seg('Y la pereza total: *fiaca.* *¡Esa* *sí!*', { shot: 'chatgpt', turno: 2, card: 1, rv: [[4, 'fiaca.']], fx: (lt, p, S, w, T) => { if (lt > w(5)) cheer('chatgpt', T); S.marc = 1; S.dado = 2; } });
seg('*Una* *de* *cinco,* menos dos del dado: *ChatGPT* se queda en *cero.*', { shot: 'chatgpt', turno: 2, card: 1, sc: [['chatgpt', 0, 'cero.']], fx: (lt, p, S, w, T) => { sad('chatgpt', T); S.marc = 1; S.dado = 2; } });
seg('*¡Empate* *arriba!* *Claude* y *Gemini* con *cuatro,* y *ChatGPT* *cero.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.marc = 1; S.podio = lt / 1.2; cheer('gemini', T); cheer('claude', T + 1); } });
seg('¿Vos cuántas *adivinabas* de las de *Gemini?*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.marc = 1; later(tag, '¿CUÁNTAS ADIVINABAS? 🤔', lt / .3, H * .66, '#5b2a86', '#fff', 50); } });
seg('Comentá *CONTRARRELOJ* y seguime para la *próxima* *partida.*', { shot: 'cover', fx: (lt, p, S, w, T) => { S.marc = 1; NAMES.forEach((n, i) => wave(n, T + i)); S.cta = lt / .4; } });
// ---------- timing ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TM.dur + 2.2; s.dur = s.t1 - s.t0; });
for (let i = 0; i < S_.length;) { let j = i; while (j + 1 < S_.length && S_[j + 1].shot === S_[i].shot) j++; for (let k = i; k <= j; k++) { S_[k].sp0 = S_[i].t0; S_[k].sp1 = S_[j].t1; } i = j + 1; }
const TOTAL = S_.at(-1).t1; window.TOTAL = TOTAL;
const findW = (s, word) => { const i = s.toks.findIndex(t => t.w === word); if (i < 0) throw new Error('palabra ' + word); return s.wt[i]; };
const REV = [[1e9, 1e9, 1e9, 1e9, 1e9], [1e9, 1e9, 1e9, 1e9, 1e9], [1e9, 1e9, 1e9, 1e9, 1e9]]; const SC = [];
S_.forEach(s => { (s.rv || []).forEach(([r, word]) => REV[s.turno][r] = findW(s, word)); (s.sc || []).forEach(([n, v, word]) => SC.push([n, v, findW(s, word)])); });
const TSTART = S_.map((s, i) => s.turno != null && (i === 0 || S_[i - 1].turno !== s.turno) ? [s.turno, s.t0] : null).filter(Boolean);
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, p = clamp(lt / s.dur), w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  idle(T); SCORE = { chatgpt: null, claude: null, gemini: null }; SC.forEach(([n, v, t]) => { if (T >= t) SCORE[n] = v; });
  const sh_ = sh[s.shot], k = ease((T - s.sp0) / (s.sp1 - s.sp0));
  camera.position.copy(sh_.p0).lerp(sh_.p1, k); const look = sh_.l0.clone().lerp(sh_.l1, k); camera.fov = sh_.fov + (sh_.fov1 - sh_.fov) * k; camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();
  const S = {}; LATER = []; if (s.fx) s.fx(lt, p, S, w, T);
  // reloj de arena (recreación): corre durante cada turno, desde el anuncio hasta el puntaje
  let q = null; if (s.turno != null) { const ts = TSTART.find(x => x[0] === s.turno)[1]; const te = SC.find(x => x[0] === TURNOS[s.turno].adiv)[2]; q = (T - ts) / Math.max(1, te - ts); if (!S.d3) arena(q); }
  if (S.d3) dado3D(S.d3[0], S.d3[1], T); else dado3D(s.turno != null ? TURNOS[s.turno].dado : null, 1, T);
  const g = ctx.createLinearGradient(0, 0, 0, H * .55); g.addColorStop(0, '#05020c'); g.addColorStop(1, '#170d2a'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (const [x, y, r, a] of STARS2) { ctx.globalAlpha = .25 + a * .5; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (s.card) tarjeta(s.turno, 1, REV[s.turno], T);
  if (S.dado) dado2D(S.dado, 1);
  if (s.card && q != null) relojito(q, 1);
  LATER.forEach(f => f());
  if (S.podio) podio(S.podio);
  if (S.cta) drawCTA(S.cta);
  if (S.cover > 0) drawCover(S.cover);
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(0,0,4,0)'); gt.addColorStop(.25, 'rgba(0,0,4,.7)'); gt.addColorStop(.8, 'rgba(0,0,4,.7)'); gt.addColorStop(1, 'rgba(0,0,4,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  if (S.marc && !(S.cover > 0)) marcador(1);
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '700 40px I', '800 40px I'].map(f => document.fonts.load(f)).concat([document.fonts.load(`40px ${EMO}`, '✅❌🏆🤔')])).then(() => { build(); cams(); flags.forEach(([m, l, f]) => { if (l) { m.material.map = labelTex(l, f); m.material.needsUpdate = true; } }); window.READY = true; });
