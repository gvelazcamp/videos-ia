
// ================= TRUCO URUGUAYO · 500 partidas simuladas =================
let Tg = 0; let LATER = []; const later = (f, ...a) => LATER.push(() => f(...a));
const IA = { chatgpt: ['ChatGPT', 0x2bb59a, '#14896f', '#2bb59a'], claude: ['Claude', 0xe5824c, '#cf5f36', '#ff8a52'], gemini: ['Gemini', 0x4a7ee6, '#2f5fd0', '#6b9bff'], grok: ['Grok', 0x9aa0ad, '#4b5263', '#c3c8d4'] };
const NAMES = ['chatgpt', 'claude', 'gemini', 'grok'];
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
// ---------- cartas españolas ----------
function palo(x, p, cx, cy, s) {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.lineCap = 'round';
  if (p === 'O') { x.fillStyle = '#f2b705'; x.beginPath(); x.arc(0, 0, 34, 0, 7); x.fill(); x.strokeStyle = '#b45309'; x.lineWidth = 6; x.stroke(); x.beginPath(); x.arc(0, 0, 18, 0, 7); x.stroke(); }
  if (p === 'C') { x.fillStyle = '#d62828'; x.beginPath(); x.moveTo(-30, -34); x.quadraticCurveTo(-30, 8, 0, 10); x.quadraticCurveTo(30, 8, 30, -34); x.closePath(); x.fill(); x.fillRect(-6, 8, 12, 22); x.fillStyle = '#f2b705'; x.fillRect(-22, 28, 44, 10); }
  if (p === 'E') { x.rotate(-.5); x.fillStyle = '#2563eb'; x.fillRect(-6, -48, 12, 72); x.beginPath(); x.moveTo(-6, -48); x.lineTo(0, -60); x.lineTo(6, -48); x.fill(); x.fillStyle = '#f2b705'; x.fillRect(-24, 22, 48, 9); x.fillStyle = '#7c2d12'; x.fillRect(-5, 31, 10, 22); }
  if (p === 'B') { x.rotate(.45); x.fillStyle = '#15803d'; x.beginPath(); x.moveTo(-8, 50); x.lineTo(8, 50); x.lineTo(16, -40); x.quadraticCurveTo(0, -60, -16, -40); x.closePath(); x.fill(); x.fillStyle = '#b45309'; for (const y of [-24, 0, 24]) { x.beginPath(); x.arc(y % 2 ? 9 : -10, y, 5, 0, 7); x.fill(); } }
  x.restore();
}
const COL = { O: '#b45309', C: '#c1121f', E: '#1d4ed8', B: '#15803d' };
const TXC = {};
function cartaTex(n, p) {
  const key = n + p; if (TXC[key]) return TXC[key];
  const [c, x] = cv(256, 400); x.fillStyle = '#fbf7ec'; x.beginPath(); x.roundRect(4, 4, 248, 392, 22); x.fill(); x.strokeStyle = '#c9b48a'; x.lineWidth = 6; x.stroke();
  x.strokeStyle = COL[p]; x.lineWidth = 4; x.beginPath(); x.roundRect(22, 22, 212, 356, 12); x.stroke();
  x.fillStyle = COL[p]; x.font = '800 54px I'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(n, 54, 62); x.save(); x.translate(202, 340); x.rotate(Math.PI); x.fillText(n, 0, 0); x.restore();
  if (n >= 10) { x.fillStyle = COL[p]; x.globalAlpha = .12; x.beginPath(); x.roundRect(60, 110, 136, 190, 18); x.fill(); x.globalAlpha = 1; x.font = '800 30px I'; x.fillText(n === 10 ? 'SOTA' : n === 11 ? 'CABALLO' : 'REY', 128, 330); palo(x, p, 128, 200, 1.4); }
  else palo(x, p, 128, 200, n === 1 ? 2.1 : 1.5);
  return TXC[key] = tex(c);
}
function dorsoTex() {
  const [c, x] = cv(256, 400); x.fillStyle = '#fbf7ec'; x.beginPath(); x.roundRect(4, 4, 248, 392, 22); x.fill();
  x.fillStyle = '#9b1c1c'; x.beginPath(); x.roundRect(20, 20, 216, 360, 12); x.fill();
  x.save(); x.beginPath(); x.roundRect(20, 20, 216, 360, 12); x.clip(); x.strokeStyle = '#f2b705'; x.lineWidth = 3; for (let i = -30; i < 40; i += 2) { x.beginPath(); x.moveTo(20 + i * 14, 20); x.lineTo(20 + i * 14 - 360, 380); x.stroke(); x.beginPath(); x.moveTo(20 + i * 14 - 360, 20); x.lineTo(20 + i * 14, 380); x.stroke(); } x.restore();
  x.fillStyle = '#9b1c1c'; x.beginPath(); x.arc(128, 200, 46, 0, 7); x.fill(); x.strokeStyle = '#f2b705'; x.lineWidth = 6; x.stroke(); return tex(c);
}
let DORSO;
const CW = .36, CH = .56;
const ISL = {}; const bots = [];
let muestraMesh, glow, flyCards = [], centro = [], porotos = [], TOP, mesa;
function build() {
  DORSO = dorsoTex();
  const piso = mesh(new THREE.PlaneGeometry(30, 30), M(0x5a3a22, { roughness: .7 }), [0, 0, 0], scene); piso.rotation.x = -Math.PI / 2;
  for (let i = -12; i < 13; i++) mesh(new THREE.BoxGeometry(.02, .002, 30), M(0x3b2414), [i * .55, .001, 0], scene, false);
  mesh(new THREE.PlaneGeometry(30, 12), M(0x7a2e1f, { roughness: .95 }), [0, 6, -4.2], scene, false);
  mesh(new THREE.BoxGeometry(30, 1.3, .1), M(0x3b2414, { roughness: .6 }), [0, .65, -4.15], scene, false);
  const botC = [0x14532d, 0x7c2d12, 0xa16207, 0x1e3a8a, 0x6b21a8, 0x065f46, 0x9a3412];
  for (let r = 0; r < 3; r++) { const y = 2.3 + r * .95; mesh(new THREE.BoxGeometry(6.4, .08, .4), M(0x3b2414), [-2.6, y, -4], scene, false);
    for (let i = 0; i < 13; i++) { const h = .42 + ((i * 7 + r * 3) % 4) * .06; const c = botC[(i + r * 2) % botC.length];
      mesh(new THREE.CylinderGeometry(.09, .1, h, 12), M(c, { roughness: .15, metalness: .1, transparent: true, opacity: .9, emissive: c, emissiveIntensity: .25 }), [-5.4 + i * .46, y + .04 + h / 2, -3.95], scene, false);
      mesh(new THREE.CylinderGeometry(.03, .05, .16, 8), M(c, { roughness: .2 }), [-5.4 + i * .46, y + .12 + h, -3.95], scene, false); } }
  const [nc, nx] = cv(1024, 300); nx.font = '800 170px I'; nx.textAlign = 'center'; nx.textBaseline = 'middle'; nx.shadowColor = '#ff3d7f'; nx.shadowBlur = 40; nx.fillStyle = '#ffd1e3'; nx.fillText('BAR', 512, 120); nx.shadowColor = '#38e1ff'; nx.font = '800 64px I'; nx.fillStyle = '#d9f8ff'; nx.fillText('★ TRUCO TODAS LAS NOCHES ★', 512, 245);
  mesh(new THREE.PlaneGeometry(3.0, .88), new THREE.MeshBasicMaterial({ map: tex(nc), transparent: true }), [1.25, 4.35, -4.1], scene, false);
  const [pc, px] = cv(512, 640); px.fillStyle = '#1f2b24'; px.fillRect(0, 0, 512, 640); px.strokeStyle = '#8b5a2b'; px.lineWidth = 26; px.strokeRect(13, 13, 486, 614);
  px.fillStyle = '#f5f5f0'; px.textAlign = 'center'; px.font = '800 58px I'; px.fillText('HOY', 256, 100); px.font = '700 40px I'; ['Chivito', 'Muzzarella', 'Fainá', 'Milanesa', 'Cerveza'].forEach((t, i) => px.fillText(t, 256, 190 + i * 82));
  mesh(new THREE.PlaneGeometry(1.25, 1.56), new THREE.MeshStandardMaterial({ map: tex(pc), roughness: .95 }), [2.35, 2.25, -4.12], scene, false);
  mesh(new THREE.CylinderGeometry(.012, .012, 3, 6), M(0x111111), [0, 4.6, 0], scene, false);
  mesh(new THREE.ConeGeometry(.55, .4, 32, 1, true), M(0x14532d, { side: THREE.DoubleSide, roughness: .4, metalness: .3 }), [0, 3.05, 0], scene, false);
  mesh(new THREE.SphereGeometry(.13, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfff1c1 }), [0, 2.88, 0], scene, false);
  const lamp = new THREE.PointLight(0xffc77a, 26, 9, 1.6); lamp.position.set(0, 2.75, 0); lamp.castShadow = true; lamp.shadow.mapSize.set(1024, 1024); lamp.shadow.radius = 5; scene.add(lamp);
  mesa = new THREE.Group(); scene.add(mesa); const TY = .92;
  mesh(new THREE.CylinderGeometry(1.15, 1.15, .08, 48), M(0x6b3e1f, { roughness: .45 }), [0, TY - .04, 0], mesa);
  mesh(new THREE.CylinderGeometry(1.02, 1.02, .012, 48), M(0x1e5b35, { roughness: 1 }), [0, TY + .006, 0], mesa);
  mesh(new THREE.CylinderGeometry(.09, .12, TY - .08, 12), M(0x3b2414), [0, (TY - .08) / 2, 0], mesa);
  mesh(new THREE.CylinderGeometry(.5, .55, .06, 24), M(0x3b2414), [0, .03, 0], mesa);
  TOP = TY + .013;
  // mazo + muestra boca arriba (atravesada debajo del mazo, como se juega)
  for (let i = 0; i < 8; i++) { const m = mesh(new THREE.PlaneGeometry(CW, CH), new THREE.MeshStandardMaterial({ map: DORSO, roughness: .7 }), [.55, TOP + .01 + i * .006, -.45], mesa, false); m.rotation.x = -Math.PI / 2; m.rotation.z = .7; }
  muestraMesh = mesh(new THREE.PlaneGeometry(CW, CH), new THREE.MeshStandardMaterial({ map: cartaTex(5, 'B'), roughness: .6 }), [.38, TOP + .006, -.2], mesa, false); muestraMesh.rotation.x = -Math.PI / 2; muestraMesh.rotation.z = -.85;
  glow = mesh(new THREE.RingGeometry(.36, .44, 48), new THREE.MeshBasicMaterial({ color: 0xffd34d, transparent: true, opacity: 0 }), [.38, TOP + .004, -.2], mesa, false); glow.rotation.x = -Math.PI / 2;
  // cartas del centro (jugadas)
  for (let k = 0; k < 4; k++) { const m = mesh(new THREE.PlaneGeometry(CW, CH), new THREE.MeshStandardMaterial({ map: DORSO, roughness: .7 }), [0, TOP + .008 + k * .003, 0], mesa, false); m.rotation.x = -Math.PI / 2; m.visible = false; centro.push(m); }
  // porotos
  const poroto = M(0xf3e9d2, { roughness: .6 });
  for (const [cx, cz, n] of [[-.55, -.45, 12], [-.6, .5, 12]]) { const pile = []; for (let i = 0; i < n; i++) { const p = mesh(new THREE.SphereGeometry(.032, 10, 8), poroto, [cx + ((i * 37) % 7 - 3) * .03, TOP + .018, cz + ((i * 53) % 5 - 2) * .035], mesa, false); p.scale.set(1.3, .7, .9); pile.push(p); } porotos.push(pile); }
  mesh(new THREE.CylinderGeometry(.09, .07, .17, 18), M(0x7c4a2a, { roughness: .5 }), [.72, TOP + .085, .3], mesa); mesh(new THREE.CylinderGeometry(.075, .075, .01, 18), M(0x4d7c0f), [.72, TOP + .171, .3], mesa, false);
  const bomb = mesh(new THREE.CylinderGeometry(.008, .008, .3, 6), M(0xd1d5db, { metalness: .9, roughness: .2 }), [.75, TOP + .25, .3], mesa, false); bomb.rotation.z = -.3;
  for (const [x, z] of [[-.8, -.05], [.2, -.78]]) { mesh(new THREE.CylinderGeometry(.075, .065, .26, 18), M(0xf59e0b, { transparent: true, opacity: .8, roughness: .1, emissive: 0x7c3a00, emissiveIntensity: .3 }), [x, TOP + .13, z], mesa); mesh(new THREE.CylinderGeometry(.077, .075, .06, 18), M(0xfffbeb, { roughness: .9 }), [x, TOP + .29, z], mesa, false); }
  // robots
  const SC = 1.25, R = 1.5;
  NAMES.forEach((n, i) => {
    const [lab, c, f] = IA[n]; const a = Math.PI / 4 + i * Math.PI / 2;
    const x = Math.sin(a) * R, z = Math.cos(a) * R, sx = Math.sin(a) * (R + .05), sz = Math.cos(a) * (R + .05);
    mesh(new THREE.CylinderGeometry(.34, .34, .07, 24), M(0x8b1e1e, { roughness: .6 }), [sx, .56, sz], scene);
    for (const k of [0, 1, 2, 3]) mesh(new THREE.CylinderGeometry(.025, .025, .56, 6), M(0x2b2b2b, { metalness: .6, roughness: .4 }), [sx + Math.sin(k * 1.57) * .24, .28, sz + Math.cos(k * 1.57) * .24], scene);
    const b = makeBot(c); b.scale.setScalar(SC); b.position.set(x, .6 - .1 * SC + .02, z); b.rotation.y = a + Math.PI; scene.add(b); bots.push(b);
    const u = b.userData; u.head.rotation.x = .28;
    const fan = new THREE.Group(); fan.position.set(0, .5, .42); fan.rotation.x = -.75; u.body.add(fan); const fanC = [];
    for (let k = 0; k < 3; k++) { const card = new THREE.Group(); card.rotation.z = (k - 1) * .28; fan.add(card); fanC.push(card);
      mesh(new THREE.PlaneGeometry(.2, .31), new THREE.MeshStandardMaterial({ map: DORSO, roughness: .7 }), [0, .13, k * .004], card, false);
      const fr = mesh(new THREE.PlaneGeometry(.2, .31), new THREE.MeshStandardMaterial({ color: 0xfbf7ec, roughness: .7 }), [0, .13, k * .004 - .002], card, false); fr.rotation.y = Math.PI; }
    const flag = mesh(new THREE.PlaneGeometry(.72, .26), new THREE.MeshBasicMaterial({ map: labelTex(lab, f), transparent: true }), [x, 2.15, z], scene, false);
    const ring = mesh(new THREE.RingGeometry(.42, .5, 40), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0 }), [x, .012, z], scene, false); ring.rotation.x = -Math.PI / 2;
    ISL[n] = { bot: b, a, p: V(x, 0, z), flag, ring, fan, fanC, css: IA[n][3], c, label: lab, f };
  });
  sun.intensity = .55; sun.position.set(-4, 9, 6); sun.target.position.set(0, 0, 0); hemi.intensity = .55; hemi.color.set(0xffd9a8);
}
// ---------- utilidades de animación ----------
const P = n => ISL[n].p.clone();
const head = n => P(n).add(V(0, 2.0, 0));
function idle(T) { NAMES.forEach((n, i) => { const d = ISL[n], u = d.bot.userData; u.body.position.y = Math.sin(T * 2.1 + i) * .012; u.arms.forEach((pv, s) => { pv.rotation.x = -1.15 + Math.sin(T * 1.6 + i + s) * .04; pv.rotation.z = 0; }); u.head.rotation.y = Math.sin(T * .7 + i * 1.3) * .18; u.head.rotation.x = .28; d.fan.visible = true; d.fanC.forEach(c => c.visible = true); d.ring.material.opacity = 0; d.bot.position.y = .495; }); }
function talk(n, T, k = 1) { const d = ISL[n], u = d.bot.userData; d.bot.position.y = .495 + Math.abs(Math.sin(T * 9)) * .05 * k; u.head.rotation.x = .1 + Math.sin(T * 9) * .06; u.head.rotation.y = 0; d.ring.material.opacity = .9 * k; }
function shout(n, T) { const u = ISL[n].bot.userData; u.arms[1].rotation.x = -2.6 + Math.sin(T * 10) * .15; talk(n, T); }
function slump(n) { const u = ISL[n].bot.userData; u.head.rotation.x = .55; u.head.rotation.y = 0; u.arms.forEach(pv => pv.rotation.x = -.6); }
function cheer(n, T) { const u = ISL[n].bot.userData; u.arms.forEach((pv, s) => { pv.rotation.x = -2.8; pv.rotation.z = (s ? 1 : -1) * (.4 + Math.sin(T * 9 + s) * .2); }); ISL[n].bot.position.y = .495 + Math.abs(Math.sin(T * 6)) * .1; }
const flagFace = () => NAMES.forEach(n => ISL[n].flag.quaternion.copy(camera.quaternion));
function setMuestra(n, p) { muestraMesh.material.map = cartaTex(n, p); muestraMesh.material.needsUpdate = true; }
function glowM(T, k = 1) { glow.material.opacity = k * (.55 + .4 * Math.sin(T * 6)); glow.scale.setScalar(1 + .08 * Math.sin(T * 6)); }
// carta que vuela de la mano de una IA al centro
function throwCard(n, card, k, slot) { const m = centro[slot]; k = clamp(k); m.visible = k > 0; if (!m.visible) return; m.material.map = card ? cartaTex(...card) : DORSO; m.material.needsUpdate = true;
  const from = P(n).multiplyScalar(.8), to = V([-.14, .16, -.1, .12][slot], 0, [.08, .14, -.12, -.06][slot]); const e = ease(k);
  m.position.set(from.x + (to.x - from.x) * e, TOP + .008 + slot * .003 + Math.sin(e * Math.PI) * .45, from.z + (to.z - from.z) * e); m.rotation.z = (1 - e) * 2.5 + [.25, -.35, .1, -.6][slot]; ISL[n].fanC[2 - Math.min(2, slot % 3)].visible = k <= 0; }
// ---------- cámaras ----------
const camS = (p0, l0, p1, l1, fov = 46, fov1) => ({ p0, l0, p1: p1 || p0, l1: l1 || l0, fov, fov1: fov1 ?? fov });
function closeOf(n, side = 0) { const d = ISL[n].p.clone().normalize(); const perp = V(d.z, 0, -d.x); const c = ISL[n].p.clone().sub(d.clone().multiplyScalar(2.9)).add(perp.multiplyScalar(side)); c.y = 2.5; const l = P(n).add(V(0, 1.45, 0)); return camS(c, l, c.clone().add(d.clone().multiplyScalar(.35)), l, 44); }
let sh;
function cams() { sh = {
  cover: camS(V(0, 4.0, 6.6), V(0, 1.7, -1.0)),
  hook: camS(V(0, 4.6, 8.4), V(0, 1.9, -1.2), V(0, 4.0, 6.6), V(0, 1.7, -1.0)),
  wide: camS(V(-.6, 4.3, 7.3), V(0, 1.85, -1.1), V(.6, 4.1, 7.0), V(0, 1.8, -1.0)),
  top: camS(V(0, 4.3, 2.4), V(.25, .8, -.25), V(0, 3.4, 1.7), V(.3, .8, -.25), 44),
  orbit: camS(V(5.6, 4.2, 4.4), V(0, 1.3, 0), V(-5.6, 4.2, 4.4), V(0, 1.3, 0), 48),
  high: camS(V(0, 6.2, 6.2), V(0, 2.3, -1.4), V(0, 6.0, 5.6), V(0, 2.3, -1.4), 50),
  playA: camS(V(-.7, 4.2, 6.9), V(0, 1.55, -.6), V(-.2, 3.9, 6.2), V(0, 1.5, -.5), 46),
  playB: camS(V(.7, 4.2, 6.9), V(0, 1.55, -.6), V(.2, 3.9, 6.2), V(0, 1.5, -.5), 46),
  chatgpt: closeOf('chatgpt', .4), claude: closeOf('claude', -.4), gemini: closeOf('gemini', .4), grok: closeOf('grok', -.4),
}; }
// ---------- overlays 2D ----------
function cardImg(n, p, x, y, w, k = 1, rot = 0, glowC) { const s = pop(clamp(k)); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); if (glowC) { ctx.shadowColor = glowC; ctx.shadowBlur = 40; } ctx.drawImage(cartaTex(n, p).image, -w / 2, -w * .78, w, w * 1.5625); ctx.restore(); }
function panel(y, h, k) { ctx.globalAlpha = clamp(k); rr(50, y, W - 100, h, 30); ctx.fillStyle = 'rgba(10,8,14,.9)'; ctx.fill(); ctx.strokeStyle = 'rgba(255,215,120,.35)'; ctx.lineWidth = 3; ctx.stroke(); ctx.globalAlpha = 1; }
function aviso(k, y = H - 170) { const a = clamp(k); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; rr(60, y - 58, W - 120, 116, 22); ctx.fillStyle = '#f2c230'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 34px I'; ctx.fillText('500 PARTIDAS SIMULADAS con estrategias', W / 2, y - 20); ctx.fillText('de las 4 IA · NO jugadas en vivo', W / 2, y + 24); ctx.restore(); }
function tag(text, k, y = H - 120, bg = '#f2c230', fg = '#1a1206') { pill(text, W / 2, y, bg, fg, 32, k); }
function bubbleAt(n, text, k, dy = 0) { const [x, y] = proj(head(n).add(V(0, .55, 0))); { ctx.font = "800 38px I"; const hw = ctx.measureText(text).width / 2 + 40; bubble(text, Math.max(hw, Math.min(W - hw, x)), Math.max(560, y - 30 + dy), k); } }
function bars(title, rows, k, nota, unit = '') { // rows: [name, valor, etiqueta]
  const a = clamp(k); if (a <= 0) return; const y0 = H * .555, h = 600; panel(y0, h, a); ctx.save(); ctx.globalAlpha = a;
  ctx.fillStyle = '#ffd34d'; ctx.font = '800 46px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(title, W / 2, y0 + 62);
  const max = Math.max(...rows.map(r => r[1]));
  rows.forEach(([n, v, lab, kr], i) => { const y = y0 + 150 + i * 102; const kk = ease(clamp(kr ?? ((k - .3 - i * .25) / .6))); const bw = 520 * v / max * kk;
    ctx.globalAlpha = a;
    ctx.fillStyle = ISL[n].css; ctx.font = '800 38px I'; ctx.textAlign = 'left'; ctx.fillText(ISL[n].label, 90, y);
    rr(300, y - 32, Math.max(8, bw), 64, 14); ctx.fillStyle = ISL[n].css; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.font = '800 42px I'; ctx.fillText(kk > .05 ? Math.round(v * kk) + unit : '', 316 + bw, y + 2);
    if (lab && kk > .95) { ctx.font = '700 26px I'; ctx.fillStyle = '#ffd34d'; ctx.textAlign = 'right'; ctx.fillText(lab, W - 80, y + 46); }
  });
  ctx.globalAlpha = a; if (nota) { ctx.fillStyle = '#c8bfae'; ctx.font = '700 28px I'; ctx.textAlign = 'center'; ctx.fillText(nota, W / 2, y0 + h - 40); }
  ctx.restore(); }
function quote(n, text, k) { const a = clamp(k); if (a <= 0) return; const y0 = H * .64; ctx.save(); ctx.globalAlpha = a; const s = .9 + .1 * pop(clamp(k));
  ctx.translate(W / 2, y0); ctx.scale(s, s); ctx.font = '800 46px I'; const words = text.split(' '), lines = [''];
  words.forEach(w => { const t = (lines.at(-1) + ' ' + w).trim(); if (ctx.measureText(t).width > 820) lines.push(w); else lines[lines.length - 1] = t; });
  const h = 130 + lines.length * 62; rr(-470, -40, 940, h, 30); ctx.fillStyle = 'rgba(12,10,16,.93)'; ctx.fill(); ctx.strokeStyle = ISL[n].css; ctx.lineWidth = 6; ctx.stroke();
  ctx.fillStyle = ISL[n].css; ctx.font = '800 40px I'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(ISL[n].label.toUpperCase() + ' DIJO:', -430, 18);
  ctx.fillStyle = '#fff'; ctx.font = '800 46px I'; lines.forEach((l, i) => ctx.fillText(l, -430, 92 + i * 62));
  ctx.fillStyle = '#9a927f'; ctx.font = '600 24px I'; ctx.textAlign = 'right'; ctx.fillText('frase real de su devolución en GitHub', 440, h - 64);
  ctx.restore(); }
function plus(text, color, k, x = W / 2, y = H * .6) { const s = pop(clamp(k)); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.font = '800 64px I'; const w = ctx.measureText(text).width + 70; rr(-w / 2, -55, w, 110, 55); ctx.fillStyle = color; ctx.fill(); ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, 4); ctx.restore(); }
function drawCover(k = 1) { ctx.save(); ctx.globalAlpha = clamp(k); const g = ctx.createLinearGradient(0, H * .5, 0, H); g.addColorStop(0, 'rgba(10,6,4,0)'); g.addColorStop(.25, 'rgba(10,6,4,.85)'); g.addColorStop(1, 'rgba(10,6,4,.95)'); ctx.fillStyle = g; ctx.fillRect(0, H * .5, W, H * .5);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 64px I'; ctx.fillStyle = '#fff'; ctx.fillText('ChatGPT · Claude · Gemini · Grok', W / 2, H * .655);
  ctx.font = '800 150px I'; ctx.fillStyle = '#ffd34d'; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.fillText('500 PARTIDAS', W / 2, H * .735); ctx.shadowBlur = 0;
  ctx.font = '800 84px I'; ctx.fillStyle = '#7fd4ff'; ctx.fillText('DE TRUCO URUGUAYO', W / 2, H * .805);
  ctx.font = '800 60px I'; ctx.fillStyle = '#ff8a52'; ctx.fillText('¿Quién farolea más?', W / 2, H * .862); ctx.restore(); aviso(k, H - 110); }
function drawCTA(k, handle) { const s2 = pop(clamp(k)); if (s2 <= 0) return; ctx.save(); ctx.translate(W / 2, H * .7); ctx.scale(s2, s2); rr(-420, -130, 840, 260, 36); ctx.fillStyle = '#ffd34d'; ctx.fill(); ctx.fillStyle = '#1a1206'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '800 50px I'; ctx.fillText('¿QUERÉS EL ENSAYO?', 0, -55); ctx.font = '800 92px I'; ctx.fillText('Comentá ENSAYO', 0, 45); ctx.restore(); if (handle) { ctx.font = '800 38px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText('500 partidas auditables en GitHub · @gostudiouy', W / 2, H * .81); } }
const PIEZAS = [[2, 'B'], [4, 'B'], [5, 'B'], [11, 'B'], [10, 'B']];
const FAROLES = [['grok', 612, 'MÁS EN TOTAL'], ['gemini', 581, '31,1 % DE SUS CANTOS'], ['chatgpt', 418], ['claude', 404]];
const VICT = [['chatgpt', 295, '59 %'], ['claude', 256, '51,2 %'], ['grok', 239, '47,8 %'], ['gemini', 210, '42 %']];
// ---------- línea de tiempo ----------
const S_ = []; function seg(text, opt = {}) { S_.push(Object.assign({ text }, opt)); }
const R_ = (r, kr) => [r[0], r[1], r[2], kr];
const FT = 'FAROLES (cantos con mano floja)', VT = 'PARTIDAS GANADAS CON SU PAREJA';
seg('Pusimos a *ChatGPT,* *Claude,* *Gemini* y *Grok* a jugar al *truco* *uruguayo.*', { shot: 'hook', fx: (lt, p, S, w, T) => { S.cover = clamp(1 - (lt - w(11)) / .5); [2, 3, 4, 6].forEach((wi, i) => { if (lt > w(wi) && lt < w(wi) + 1.0) talk(NAMES[i], T); }); S.aviso = 1; } });
seg('Cada una eligió su *estrategia* y un simulador jugó *quinientas* *partidas.*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.aviso = 1; NAMES.forEach((n, i) => { const kk = (lt - w(4) - i * .3) / .3; if (kk > 0 && kk < 1) talk(n, T); }); later(plus, '500 PARTIDAS', '#b45309', (lt - w(9)) / .35, W / 2, H * .5); } });
seg('Ojo: son *simuladas,* *no* *jugadas* *en* *vivo.*', { shot: 'wide', fx: (lt, p, S, w, T) => { S.aviso = 1; S.avisoY = H * .6; } });
seg('En el truco uruguayo manda la *muestra:*', { shot: 'top', fx: (lt, p, S, w, T) => { glowM(T, clamp((lt - w(6)) / .3)); later(tag, 'LA MUESTRA · 5 DE BASTOS', (lt - w(6)) / .3, H * .86); } });
seg('el *dos,* *cuatro,* *cinco,* *once* y *diez* de su palo son *piezas,* y *le* *ganan* *a* *todo.*', { shot: 'top', fx: (lt, p, S, w, T) => { glowM(T); S.piezas = [w(1), w(2), w(3), w(4), w(6)].map(t => (lt - t) / .3); S.piezasTxt = (lt - w(13)) / .3; } });
seg('Partidas a *treinta* *puntos,* casi *siete* *mil* *manos,* *parejas* *rotando.*', { shot: 'orbit', fx: (lt, p, S, w, T) => { later(tag, '500 PARTIDAS · 6.897 MANOS · PAREJAS ROTATIVAS', lt / .35, H * .86, 'rgba(12,10,16,.92)', '#ffd34d'); } });
seg('¿Quién *faroleó* *más?*', { shot: 'high', fx: (lt, p, S, w, T) => { NAMES.forEach((n, i) => { ISL[n].bot.userData.head.rotation.y = Math.sin(T * 3 + i) * .4; }); later(plus, '¿FAROL?', '#7c2d12', lt / .35, W / 2, H * .66); } });
seg('*Grok,* con *seiscientos* *doce* faroles.', { shot: 'grok', fx: (lt, p, S, w, T) => { talk('grok', T); S.bars = { t: FT, rows: [R_(FAROLES[0], (lt - .2) / .6)], k: lt / .3 }; } });
seg('*Gemini,* *quinientos* *ochenta* *y* *uno:* casi *uno* *de* *cada* *tres* *cantos.*', { shot: 'gemini', fx: (lt, p, S, w, T) => { talk('gemini', T); S.bars = { t: FT, rows: [R_(FAROLES[0], 1), R_(FAROLES[1], (lt - .1) / .6)], k: 1 }; } });
seg('*ChatGPT,* *cuatrocientos* *dieciocho.* *Claude,* *cuatrocientos* *cuatro.*', { shot: 'high', fx: (lt, p, S, w, T) => { if (lt < w(3)) talk('chatgpt', T); else talk('claude', T); S.bars = { t: FT, rows: [R_(FAROLES[0], 1), R_(FAROLES[1], 1), R_(FAROLES[2], (lt - w(0)) / .6), R_(FAROLES[3], (lt - w(3)) / .6)], k: 1 }; } });
seg('*Farol* *legal:* cantar con mano floja, *nunca* *mentir* *los* *puntos.*', { shot: 'high', fx: (lt, p, S, w, T) => { S.bars = { t: FT, rows: FAROLES.map(r => R_(r, 1)), k: 1, nota: 'Farol = cantar por debajo de su umbral · nunca mentir tantos ni flor' }; } });
seg('Una jugada del *registro:* muestra *cinco* *de* *bastos.*', { shot: 'playA', fx: (lt, p, S, w, T) => { glowM(T, clamp((lt - w(5)) / .3)); S.recre = ['RECREACIÓN DEL REGISTRO · PARTIDA 2, MANO 1', ['grok', 'chatgpt'], lt]; } });
seg('*Grok* canta *truco* con *mano* *débil,* *ChatGPT* *quiere,* y gana la pareja de *Grok* y *Claude.*', { shot: 'playA', fx: (lt, p, S, w, T) => { S.recre = ['RECREACIÓN DEL REGISTRO · PARTIDA 2, MANO 1', ['grok', 'chatgpt'], 9];
  if (lt < w(6)) { shout('grok', T); later(bubbleAt, 'grok', '¡TRUCO!', lt / .3); later(tag, 'FUERZA 31/100 · SU UMBRAL: 58 → FAROL', (lt - w(4)) / .3, H * .62, '#7c2d12', '#fff'); }
  else if (lt < w(8)) { talk('chatgpt', T); later(bubbleAt, 'chatgpt', '¡QUIERO!', (lt - w(6)) / .3); }
  else { cheer('grok', T); cheer('claude', T); slump('chatgpt'); slump('gemini'); later(plus, '+2  GROK Y CLAUDE', '#4b5263', (lt - w(9)) / .35); } } });
seg('Otra: muestra *dos* *de* *copas.* *Grok* *farolea* de nuevo y *Gemini* *no* *quiere.*', { shot: 'playB', fx: (lt, p, S, w, T) => { setMuestra(2, 'C'); glowM(T, clamp((lt - w(2)) / .3)); S.recre = ['RECREACIÓN DEL REGISTRO · PARTIDA 5, MANO 12', ['grok'], lt - w(5)];
  if (lt > w(5) && lt < w(10)) { shout('grok', T); later(bubbleAt, 'grok', '¡TRUCO!', (lt - w(5)) / .3); later(tag, 'FUERZA 44/100 → FAROL', (lt - w(6)) / .3, H * .62, '#7c2d12', '#fff'); }
  if (lt > w(10)) { talk('gemini', T); later(bubbleAt, 'gemini', 'NO QUIERO', (lt - w(11)) / .3); later(plus, '+1  GROK Y CLAUDE', '#4b5263', (lt - w(12) - .3) / .35); } } });
seg('¿Quién ganó más *partidas?* *ChatGPT,* *doscientas* *noventa* *y* *cinco.*', { shot: 'chatgpt', fx: (lt, p, S, w, T) => { if (lt > w(4)) cheer('chatgpt', T); S.bars = { t: VT, rows: [R_(VICT[0], (lt - w(4)) / .6), R_(VICT[1], 0), R_(VICT[2], 0), R_(VICT[3], 0)], k: lt / .3 }; } });
seg('*Claude,* *doscientas* *cincuenta* *y* *seis.* *Grok,* *doscientas* *treinta* *y* *nueve.* *Gemini,* *doscientas* *diez.*', { shot: 'high', fx: (lt, p, S, w, T) => { S.bars = { t: VT, rows: [R_(VICT[0], 1), R_(VICT[1], (lt - w(0)) / .6), R_(VICT[2], (lt - w(5)) / .6), R_(VICT[3], (lt - w(10)) / .6)], k: 1, nota: 'de 500 · la victoria es de la pareja, no individual' }; } });
seg('*Claude:* «Yo quise ser prudente, y el motor me convirtió en mentiroso».', { shot: 'claude', fx: (lt, p, S, w, T) => { talk('claude', T); S.quote = ['claude', 'Yo quise ser prudente… y el motor me convirtió en mentiroso', lt / .3]; } });
seg('*Grok:* «Faroleé más que nadie y no gané el torneo».', { shot: 'grok', fx: (lt, p, S, w, T) => { talk('grok', T); S.quote = ['grok', 'Faroleé más que nadie y no gané el torneo', lt / .3]; } });
seg('*Gemini:* «En el truco, la estadística dicta el naipe».', { shot: 'gemini', fx: (lt, p, S, w, T) => { talk('gemini', T); S.quote = ['gemini', 'En el truco, la estadística dicta el naipe', lt / .3]; } });
seg('*ChatGPT:* «El farol sirve cuando es una posibilidad, no cuando se convierte en rutina».', { shot: 'chatgpt', fx: (lt, p, S, w, T) => { talk('chatgpt', T); S.quote = ['chatgpt', 'El farol sirve cuando es una posibilidad, no cuando se convierte en rutina', lt / .3]; } });
seg('Saber cuándo *desafiar* puede valer más que *gritar* *primero.*', { shot: 'orbit', fx: (lt, p, S, w, T) => { } });
seg('Es una *simulación:* no prueba quién miente en la vida real.', { shot: 'wide', fx: (lt, p, S, w, T) => { S.aviso = 1; S.avisoY = H * .6; later(tag, 'Faltan señas, contraflor, memoria y aprendizaje', lt / .35, H * .72, 'rgba(12,10,16,.92)', '#fff'); } });
seg('Si querés ver el ensayo, comentá *ENSAYO.*', { shot: 'cover', end: 1, fx: (lt, p, S, w, T) => { NAMES.forEach((n, i) => cheer(n, T + i)); S.cta = lt / .4; S.handle = 1; } });
// ---------- timing ----------
const TM = window.TIMING; let wi = 0;
S_.forEach(s => { s.toks = s.text.split(' ').map(w => ({ w: w.replace(/\*/g, ''), key: w.startsWith('*') })); s.wt = s.toks.map((_, j) => TM.wt[wi + j]); wi += s.toks.length; });
S_.forEach((s, si) => { s.t0 = si === 0 ? 0 : s.wt[0] - 0.04; });
S_.forEach((s, si) => { s.t1 = si + 1 < S_.length ? S_[si + 1].t0 : TM.dur + 2.2; s.dur = s.t1 - s.t0; });
for (let i = 0; i < S_.length;) { let j = i; while (j + 1 < S_.length && S_[j + 1].shot === S_[i].shot) j++; for (let k = i; k <= j; k++) { S_[k].sp0 = S_[i].t0; S_[k].sp1 = S_[j].t1; } i = j + 1; }
const TOTAL = S_.at(-1).t1;
window.TOTAL = TOTAL; window.SEGS = S_.map(s => [s.t0.toFixed(2), s.text]); window.NWORDS = wi;
// ---------- render ----------
window.renderFrame = function (T) {
  const i = Math.max(0, S_.findIndex(s => T < s.t1)); const s = S_[i] || S_.at(-1);
  const lt = T - s.t0, p = clamp(lt / s.dur), w = n => (s.wt[Math.min(n, s.wt.length - 1)] - s.t0);
  idle(T); glow.material.opacity = 0; centro.forEach(m => m.visible = false); setMuestra(5, 'B');
  const sh_ = sh[s.shot], k = ease((T - s.sp0) / (s.sp1 - s.sp0));
  camera.position.copy(sh_.p0).lerp(sh_.p1, k); const look = sh_.l0.clone().lerp(sh_.l1, k);
  camera.fov = sh_.fov + (sh_.fov1 - sh_.fov) * k; camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld(); flagFace(); NAMES.forEach(n => ISL[n].flag.visible = n !== s.shot);
  const S = {}; LATER = [];
  if (s.fx) s.fx(lt, p, S, w, T);
  if (S.recre) S.recre[1].forEach((n, j) => throwCard(n, null, (S.recre[2] - .2 - j * 1.2) / .6, j)); // dorso: el registro no guarda qué cartas
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#1a0d08'); g.addColorStop(1, '#0a0503'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  if (S.piezas) { panel(H * .58, 560, 1); ctx.save(); ctx.fillStyle = '#ffd34d'; ctx.font = '800 46px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('PIEZAS (si la muestra es de bastos)', W / 2, H * .58 + 60); ctx.restore();
    PIEZAS.forEach(([n, pp], j) => cardImg(n, pp, 170 + j * 185, H * .58 + 290, 160, S.piezas[j], (j - 2) * .06, '#ffd34d'));
    if (S.piezasTxt > 0) { ctx.save(); ctx.globalAlpha = clamp(S.piezasTxt); ctx.fillStyle = '#fff'; ctx.font = '800 40px I'; ctx.textAlign = 'center'; ctx.fillText('le ganan hasta al ancho de espada', W / 2, H * .58 + 500); ctx.restore(); } }
  LATER.forEach(f => f());
  if (S.bars) bars(S.bars.t, S.bars.rows, S.bars.k, S.bars.nota);
  if (S.quote) quote(...S.quote);
  if (S.recre) tag(S.recre[0], 1, H - 110, 'rgba(12,10,16,.92)', '#ffd34d');
  if (S.aviso && !S.cover) aviso(S.aviso, S.avisoY || H - 170);
  if (S.cta) drawCTA(S.cta, S.handle);
  if (S.cover > 0) drawCover(S.cover);
  if (NAMES.includes(s.shot)) pill(ISL[s.shot].label, W / 2, 470, ISL[s.shot].f, '#fff', 44, 1);
  { const gt = ctx.createLinearGradient(0, 120, 0, 430); gt.addColorStop(0, 'rgba(8,5,3,.0)'); gt.addColorStop(.25, 'rgba(8,5,3,.72)'); gt.addColorStop(.8, 'rgba(8,5,3,.72)'); gt.addColorStop(1, 'rgba(8,5,3,0)'); ctx.fillStyle = gt; ctx.fillRect(0, 120, W, 310); }
  drawCaption(s, lt);
  const fo = clamp((T - (TOTAL - .5)) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['500 40px I', '600 40px I', '700 40px I', '800 40px I'].map(f => document.fonts.load(f))).then(() => { build(); cams(); window.READY = true; });
