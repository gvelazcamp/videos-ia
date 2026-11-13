
// ===== Las 4 IA jugando al truco en un bar =====
const IAS = [['ChatGPT', 0x2bb59a, '#14896f'], ['Claude', 0xe5824c, '#cf5f36'], ['Gemini', 0x4a7ee6, '#2f5fd0'], ['Grok', 0x9aa0ad, '#4b5263']];
const flags = [], bots = [];
const tex = c => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };
const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
// --- cartas españolas ---
function palo(x, p, cx, cy, s) {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.lineCap = 'round';
  if (p === 'oro') { x.fillStyle = '#f2b705'; x.beginPath(); x.arc(0, 0, 34, 0, 7); x.fill(); x.strokeStyle = '#b45309'; x.lineWidth = 6; x.stroke(); x.beginPath(); x.arc(0, 0, 18, 0, 7); x.stroke(); }
  if (p === 'copa') { x.fillStyle = '#d62828'; x.beginPath(); x.moveTo(-30, -34); x.quadraticCurveTo(-30, 8, 0, 10); x.quadraticCurveTo(30, 8, 30, -34); x.closePath(); x.fill(); x.fillRect(-6, 8, 12, 22); x.fillStyle = '#f2b705'; x.fillRect(-22, 28, 44, 10); }
  if (p === 'espada') { x.rotate(-.5); x.fillStyle = '#2563eb'; x.fillRect(-6, -48, 12, 72); x.beginPath(); x.moveTo(-6, -48); x.lineTo(0, -60); x.lineTo(6, -48); x.fill(); x.fillStyle = '#f2b705'; x.fillRect(-24, 22, 48, 9); x.fillStyle = '#7c2d12'; x.fillRect(-5, 31, 10, 22); }
  if (p === 'basto') { x.rotate(.45); x.fillStyle = '#15803d'; x.beginPath(); x.moveTo(-8, 50); x.lineTo(8, 50); x.lineTo(16, -40); x.quadraticCurveTo(0, -60, -16, -40); x.closePath(); x.fill(); x.fillStyle = '#b45309'; for (const y of [-24, 0, 24]) { x.beginPath(); x.arc(y % 2 ? 9 : -10, y, 5, 0, 7); x.fill(); } }
  x.restore();
}
function cartaTex(n, p) {
  const [c, x] = cv(256, 400); x.fillStyle = '#fbf7ec'; x.beginPath(); x.roundRect(4, 4, 248, 392, 22); x.fill(); x.strokeStyle = '#c9b48a'; x.lineWidth = 6; x.stroke();
  const col = { oro: '#b45309', copa: '#c1121f', espada: '#1d4ed8', basto: '#15803d' }[p];
  x.strokeStyle = col; x.lineWidth = 4; x.beginPath(); x.roundRect(22, 22, 212, 356, 12); x.stroke();
  x.fillStyle = col; x.font = '800 54px I'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(n, 50, 62); x.save(); x.translate(206, 340); x.rotate(Math.PI); x.fillText(n, 0, 0); x.restore();
  if (n === 1) palo(x, p, 128, 200, 2.1); else palo(x, p, 128, 200, 1.5);
  return tex(c);
}
function dorsoTex() {
  const [c, x] = cv(256, 400); x.fillStyle = '#fbf7ec'; x.beginPath(); x.roundRect(4, 4, 248, 392, 22); x.fill();
  x.fillStyle = '#9b1c1c'; x.beginPath(); x.roundRect(20, 20, 216, 360, 12); x.fill();
  x.strokeStyle = '#f2b705'; x.lineWidth = 3; for (let i = -20; i < 40; i += 2) { x.beginPath(); x.moveTo(20 + i * 14, 20); x.lineTo(20 + i * 14 - 360, 380); x.stroke(); x.beginPath(); x.moveTo(20 + i * 14 - 360, 20); x.lineTo(20 + i * 14, 380); x.stroke(); }
  x.fillStyle = '#9b1c1c'; x.beginPath(); x.arc(128, 200, 46, 0, 7); x.fill(); x.strokeStyle = '#f2b705'; x.lineWidth = 6; x.stroke(); return tex(c);
}
let DORSO;
const CW = .36, CH = .56;
function build() { DORSO = dorsoTex();
function carta(n, p, parent, pos, rotY = 0, cara = true) {
  const g = new THREE.Group(); g.position.set(...pos); parent.add(g);
  const f = mesh(new THREE.PlaneGeometry(CW, CH), new THREE.MeshStandardMaterial({ map: cara ? cartaTex(n, p) : DORSO, roughness: .7 }), [0, 0, 0], g); f.rotation.x = -Math.PI / 2; f.rotation.z = rotY; f.position.y = .004;
  return g;
}
// --- el bar ---
const piso = mesh(new THREE.PlaneGeometry(30, 30), M(0x5a3a22, { roughness: .7 }), [0, 0, 0], scene); piso.rotation.x = -Math.PI / 2;
for (let i = -12; i < 13; i++) mesh(new THREE.BoxGeometry(.02, .002, 30), M(0x3b2414), [i * .55, .001, 0], scene, false);
const pared = mesh(new THREE.PlaneGeometry(30, 12), M(0x7a2e1f, { roughness: .95 }), [0, 6, -4.2], scene, false);
mesh(new THREE.BoxGeometry(30, 1.3, .1), M(0x3b2414, { roughness: .6 }), [0, .65, -4.15], scene, false); // zócalo de madera
// estantes con botellas
const botC = [0x14532d, 0x7c2d12, 0xa16207, 0x1e3a8a, 0x6b21a8, 0x065f46, 0x9a3412];
for (let r = 0; r < 3; r++) { const y = 2.3 + r * .95; mesh(new THREE.BoxGeometry(6.4, .08, .4), M(0x3b2414), [-2.6, y, -4], scene, false);
  for (let i = 0; i < 13; i++) { const h = .42 + ((i * 7 + r * 3) % 4) * .06; const c = botC[(i + r * 2) % botC.length];
    mesh(new THREE.CylinderGeometry(.09, .1, h, 12), M(c, { roughness: .15, metalness: .1, transparent: true, opacity: .9, emissive: c, emissiveIntensity: .25 }), [-5.4 + i * .46, y + .04 + h / 2, -3.95], scene, false);
    mesh(new THREE.CylinderGeometry(.03, .05, .16, 8), M(c, { roughness: .2 }), [-5.4 + i * .46, y + .12 + h, -3.95], scene, false); } }
// cartel de neón
const [nc, nx] = cv(1024, 300); nx.font = '800 170px I'; nx.textAlign = 'center'; nx.textBaseline = 'middle'; nx.shadowColor = '#ff3d7f'; nx.shadowBlur = 40; nx.fillStyle = '#ffd1e3'; nx.fillText('BAR', 512, 120); nx.shadowColor = '#38e1ff'; nx.font = '800 64px I'; nx.fillStyle = '#d9f8ff'; nx.fillText('★ TRUCO TODAS LAS NOCHES ★', 512, 245);
mesh(new THREE.PlaneGeometry(3.0, .88), new THREE.MeshBasicMaterial({ map: tex(nc), transparent: true }), [1.25, 4.35, -4.1], scene, false);
// pizarra
const [pc, px] = cv(512, 640); px.fillStyle = '#1f2b24'; px.fillRect(0, 0, 512, 640); px.strokeStyle = '#8b5a2b'; px.lineWidth = 26; px.strokeRect(13, 13, 486, 614);
px.fillStyle = '#f5f5f0'; px.textAlign = 'center'; px.font = '800 58px I'; px.fillText('HOY', 256, 100); px.font = '700 40px I'; ['Chivito', 'Muzzarella', 'Faina', 'Milanesa', 'Cerveza'].forEach((t, i) => px.fillText(t, 256, 190 + i * 82));
mesh(new THREE.PlaneGeometry(1.25, 1.56), new THREE.MeshStandardMaterial({ map: tex(pc), roughness: .95 }), [2.35, 2.25, -4.12], scene, false);
// lámpara colgante
mesh(new THREE.CylinderGeometry(.012, .012, 3, 6), M(0x111111), [0, 4.6, 0], scene, false);
const pant = mesh(new THREE.ConeGeometry(.55, .4, 32, 1, true), M(0x14532d, { side: THREE.DoubleSide, roughness: .4, metalness: .3 }), [0, 3.05, 0], scene, false);
mesh(new THREE.SphereGeometry(.13, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfff1c1 }), [0, 2.88, 0], scene, false);
const lamp = new THREE.PointLight(0xffc77a, 26, 9, 1.6); lamp.position.set(0, 2.75, 0); lamp.castShadow = true; lamp.shadow.mapSize.set(1024, 1024); lamp.shadow.radius = 5; scene.add(lamp);
// mesa redonda de madera con paño
const mesa = new THREE.Group(); scene.add(mesa); const TY = .92;
mesh(new THREE.CylinderGeometry(1.15, 1.15, .08, 48), M(0x6b3e1f, { roughness: .45 }), [0, TY - .04, 0], mesa);
mesh(new THREE.CylinderGeometry(1.02, 1.02, .012, 48), M(0x1e5b35, { roughness: 1 }), [0, TY + .006, 0], mesa);
mesh(new THREE.CylinderGeometry(.09, .12, TY - .08, 12), M(0x3b2414), [0, (TY - .08) / 2, 0], mesa);
mesh(new THREE.CylinderGeometry(.5, .55, .06, 24), M(0x3b2414), [0, .03, 0], mesa);
const TOP = TY + .013;
// cartas jugadas en el centro
carta(1, 'espada', mesa, [-.16, TOP, .12], .25); carta(7, 'oro', mesa, [.2, TOP + .002, .08], -.35); carta(3, 'copa', mesa, [.02, TOP + .004, -.2], .1); carta(1, 'basto', mesa, [.02, TOP + .006, .34], -.6);
// mazo
for (let i = 0; i < 8; i++) carta(0, 0, mesa, [.62, TOP + i * .006, -.42], .7, false);
// porotos para anotar
const poroto = M(0xf3e9d2, { roughness: .6 });
for (const [cx, cz, n] of [[-.55, -.45, 9], [-.6, .5, 6]]) for (let i = 0; i < n; i++) { const p = mesh(new THREE.SphereGeometry(.032, 10, 8), poroto, [cx + ((i * 37) % 7 - 3) * .03, TOP + .018, cz + ((i * 53) % 5 - 2) * .035], mesa, false); p.scale.set(1.3, .7, .9); }
// mate y cervezas
const mate = mesh(new THREE.CylinderGeometry(.09, .07, .17, 18), M(0x7c4a2a, { roughness: .5 }), [.7, TOP + .085, .32], mesa); mesh(new THREE.CylinderGeometry(.075, .075, .01, 18), M(0x4d7c0f), [.7, TOP + .171, .32], mesa, false);
const bomb = mesh(new THREE.CylinderGeometry(.008, .008, .3, 6), M(0xd1d5db, { metalness: .9, roughness: .2 }), [.73, TOP + .25, .32], mesa, false); bomb.rotation.z = -.3;
for (const [x, z] of [[-.78, -.05], [.35, -.7]]) { mesh(new THREE.CylinderGeometry(.075, .065, .26, 18), M(0xf59e0b, { transparent: true, opacity: .8, roughness: .1, emissive: 0x7c3a00, emissiveIntensity: .3 }), [x, TOP + .13, z], mesa); mesh(new THREE.CylinderGeometry(.077, .075, .06, 18), M(0xfffbeb, { roughness: .9 }), [x, TOP + .29, z], mesa, false); }
// --- los 4 robots sentados ---
const SC = 1.25, R = 1.5;
IAS.forEach(([n, c, f], i) => {
  const a = Math.PI / 4 + i * Math.PI / 2; // 45°,135°,225°,315°
  const x = Math.sin(a) * R, z = Math.cos(a) * R;
  // banqueta
  const sx = Math.sin(a) * (R + .05), sz = Math.cos(a) * (R + .05);
  mesh(new THREE.CylinderGeometry(.34, .34, .07, 24), M(0x8b1e1e, { roughness: .6 }), [sx, .56, sz], scene);
  for (const k of [0, 1, 2, 3]) { const b = mesh(new THREE.CylinderGeometry(.025, .025, .56, 6), M(0x2b2b2b, { metalness: .6, roughness: .4 }), [sx + Math.sin(k * 1.57) * .24, .28, sz + Math.cos(k * 1.57) * .24], scene); }
  const b = makeBot(c); b.scale.setScalar(SC); b.position.set(x, .6 - .1 * SC + .02, z); b.rotation.y = a + Math.PI; scene.add(b); bots.push(b);
  const u = b.userData; u.arms.forEach(pv => { pv.rotation.x = -1.15; });
  u.head.rotation.x = .28;
  // abanico de 3 cartas en la mano (dorso hacia afuera)
  const fan = new THREE.Group(); fan.position.set(0, .5, .42); fan.rotation.x = -.75; u.body.add(fan);
  for (let k = 0; k < 3; k++) { const card = new THREE.Group(); card.rotation.z = (k - 1) * .28; fan.add(card);
    const back = mesh(new THREE.PlaneGeometry(.2, .31), new THREE.MeshStandardMaterial({ map: DORSO, roughness: .7 }), [0, .13, k * .004], card, false);
    const front = mesh(new THREE.PlaneGeometry(.2, .31), new THREE.MeshStandardMaterial({ map: cartaTex([4, 5, 6][k], ['oro', 'copa', 'basto'][k]), roughness: .7 }), [0, .13, k * .004 - .002], card, false); front.rotation.y = Math.PI; }
  const fl = mesh(new THREE.PlaneGeometry(.72, .26), new THREE.MeshBasicMaterial({ map: labelTex(n, f), transparent: true }), [x, 2.15, z], scene, false); flags.push([fl, n, f]);
});
}
function cam() { camera.fov = 46; camera.updateProjectionMatrix();
camera.position.set(0, 4.3, 7.3); camera.lookAt(0, 1.85, -1.1);
flags.forEach(([m]) => m.quaternion.copy(camera.quaternion));
sun.intensity = .55; sun.position.set(-4, 9, 6); sun.target.position.set(0, 0, 0); hemi.intensity = .55; hemi.color.set(0xffd9a8); }

window.TOTAL = 1;
window.renderFrame = function (T) {
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#1a0d08'); g.addColorStop(1, '#0a0503'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  pill('LAS 4 IA JUGANDO AL TRUCO', W / 2, 150, 'rgba(16,16,24,.9)', '#fff', 50, 1);
  const hp = i => { const p = bots[i].position.clone(); p.y += 1.95; return proj(p); };
  let [x, y] = hp(1); bubble('¡TRUCO!', x, y - 10, 1);
  [x, y] = hp(2); bubble('¡QUIERO RETRUCO!', x, y - 10, 1);
  return comp.toDataURL('image/jpeg', .92);
};
Promise.all(['500 40px I','700 40px I','800 40px I'].map(f => document.fonts.load(f))).then(() => { build(); cam(); flags.forEach(([m, n, f]) => { m.material.map = labelTex(n, f); m.material.needsUpdate = true; }); window.READY = true; });
