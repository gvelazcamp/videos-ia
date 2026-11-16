// ===== Expresiones de los robots (guía: referencias/recibidas/24-expresiones-islitas.webp) =====
// ponerExpresion(bot, 'contento'|'sorprendido'|'pensando'|'asustado'|'festejando'|'triste', T)
// iconoExpresion(bot, expr, T) dibuja en 2D el ícono sobre la cabeza (rayitas, !!, ?, gotas, confeti, lágrima).
const EXPRS = ['contento', 'sorprendido', 'pensando', 'asustado', 'festejando', 'triste'];
const _ojosTex = {};
function ojosTex(expr) { if (_ojosTex[expr]) return _ojosTex[expr]; const c = document.createElement('canvas'); c.width = 512; c.height = 220; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.strokeStyle = '#fff'; x.lineCap = 'round'; x.lineWidth = 38; x.shadowColor = '#dff4ff'; x.shadowBlur = 22;
  const L = 150, Rr = 362, Y = 108;
  if (expr === 'contento' || expr === 'festejando') { for (const cx of [L, Rr]) { x.beginPath(); x.arc(cx, Y + 42, 62, Math.PI * 1.15, Math.PI * 1.85); x.stroke(); } }
  if (expr === 'sorprendido') { for (const cx of [L, Rr]) { x.beginPath(); x.arc(cx, Y - 10, 60, 0, 7); x.fill(); } x.beginPath(); x.ellipse(256, Y + 78, 22, 28, 0, 0, 7); x.fill(); }
  if (expr === 'asustado') { for (const cx of [L, Rr]) { x.beginPath(); x.arc(cx, Y - 14, 54, 0, 7); x.fill(); } x.lineWidth = 16; x.beginPath(); x.moveTo(206, Y + 72); for (let i = 0; i <= 4; i++) x.lineTo(206 + i * 25, Y + 72 + (i % 2 ? -12 : 0)); x.stroke(); }
  if (expr === 'pensando') { for (const cx of [L, Rr]) { x.beginPath(); x.ellipse(cx, Y + 14, 64, 30, 0, Math.PI, 0, true); x.closePath(); x.fill(); } }
  if (expr === 'triste') { for (const cx of [L, Rr]) { x.beginPath(); x.ellipse(cx, Y + 22, 62, 28, cx === L ? .25 : -.25, Math.PI, 0, true); x.closePath(); x.fill(); } }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return (_ojosTex[expr] = t); }
function prepararCara(bot) { const u = bot.userData; if (u.cara) return; u.head.children.forEach(m => { if (m.geometry && m.geometry.parameters && m.geometry.parameters.radius === .052) m.visible = false; });
  u.cara = new THREE.Mesh(new THREE.PlaneGeometry(.5, .215), new THREE.MeshBasicMaterial({ map: ojosTex('contento'), transparent: true, depthWrite: false })); u.cara.position.set(0, .015, .335); u.head.add(u.cara);
  u.lagrima = new THREE.Mesh(new THREE.SphereGeometry(.035, 12, 10), new THREE.MeshBasicMaterial({ color: 0x5ec8ff })); u.lagrima.scale.set(1, 1.4, 1); u.head.add(u.lagrima); u.lagrima.visible = false; }
function ponerExpresion(bot, expr, T, home) { prepararCara(bot); const u = bot.userData; u.cara.material.map = ojosTex(expr); u.cara.material.needsUpdate = true;
  const [a0, a1] = u.arms; [a0, a1].forEach(a => a.rotation.set(0, 0, 0)); u.head.rotation.set(0, 0, 0); u.body.position.set(0, 0, 0); u.body.rotation.set(0, 0, 0); u.lagrima.visible = false; const by = home ?? bot.position.y;
  if (expr === 'contento') { u.head.rotation.z = Math.sin(T * 3) * .08; u.body.position.y = Math.abs(Math.sin(T * 3)) * .02; }
  if (expr === 'sorprendido') { a0.rotation.set(-1.0, 0, -2.2); a1.rotation.set(-1.0, 0, 2.2); u.head.rotation.x = -.12; }
  if (expr === 'pensando') { a1.rotation.set(-1.2, 0, 1.9); u.head.rotation.z = -.18; u.head.rotation.y = .2; }
  if (expr === 'asustado') { a0.rotation.set(-.6, 0, -1.6); a1.rotation.set(-.6, 0, 1.6); u.body.position.x = Math.sin(T * 40) * .012; u.body.position.y = -.03; }
  if (expr === 'festejando') { a0.rotation.z = -2.7 + Math.sin(T * 10) * .2; a1.rotation.z = 2.7 - Math.sin(T * 10) * .2; u.body.position.y = Math.abs(Math.sin(T * 6)) * .15; }
  if (expr === 'triste') { u.head.rotation.x = .06; u.body.position.y = -.04; u.body.rotation.x = .05; a0.rotation.z = .25; a1.rotation.z = -.25; u.lagrima.visible = true; u.lagrima.position.set(.12, -.13 - ((T * .35) % .2), .3); }
}
function iconoExpresion(bot, expr, T, escala = 1) { const p = bot.userData.head.localToWorld(new THREE.Vector3(.18, .32, 0)); const [x, y, vis] = proj(p); if (!vis) return; ctx.save(); ctx.translate(x, y); ctx.scale(escala, escala); ctx.lineCap = 'round';
  if (expr === 'contento') { ctx.strokeStyle = '#ffd34d'; ctx.lineWidth = 9; for (let i = 0; i < 3; i++) { const a = -1.2 + i * .45; ctx.beginPath(); ctx.moveTo(Math.cos(a) * 30, Math.sin(a) * 30); ctx.lineTo(Math.cos(a) * 58, Math.sin(a) * 58); ctx.stroke(); } }
  if (expr === 'sorprendido') { ctx.fillStyle = '#ffd34d'; ctx.font = '900 italic 80px I'; ctx.textAlign = 'center'; ctx.fillText('!!', 26, -6); }
  if (expr === 'pensando') { ctx.fillStyle = '#fff'; ctx.font = '900 76px I'; ctx.textAlign = 'center'; ctx.fillText('?', 20 + Math.sin(T * 2) * 4, -6); }
  if (expr === 'asustado') { ctx.fillStyle = '#5ec8ff'; for (let i = 0; i < 3; i++) { const a = -2.2 + i * .45; ctx.save(); ctx.translate(Math.cos(a) * 52 - 40, Math.sin(a) * 52); ctx.rotate(a + Math.PI / 2); ctx.beginPath(); ctx.ellipse(0, 0, 9, 16, 0, 0, 7); ctx.fill(); ctx.restore(); } }
  if (expr === 'festejando') { const cs = ['#ffd34d', '#ff5ea8', '#5ec8ff', '#7bd389', '#ff8a4c']; for (let i = 0; i < 10; i++) { const a = (i / 10) * Math.PI * 2 + T * .8, r = 60 + (i % 3) * 14; ctx.save(); ctx.translate(Math.cos(a) * r - 18, Math.sin(a) * r * .6 - 10); ctx.rotate(a * 3); ctx.fillStyle = cs[i % 5]; ctx.fillRect(-5, -11, 10, 22); ctx.restore(); } }
  ctx.restore(); }
