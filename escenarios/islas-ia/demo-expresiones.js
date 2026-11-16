const ORDEN = ['chatgpt', 'claude', 'gemini', 'grok']; const B = {};
const NOMBRE = { contento: 'CONTENTO', sorprendido: 'SORPRENDIDO', pensando: 'PENSANDO', asustado: 'ASUSTADO', festejando: 'FESTEJANDO', triste: 'TRISTE' };
function build() {
  hemi.intensity = 1.2; hemi.color.set(0xc8d0ff); hemi.groundColor.set(0x1a1830); sun.intensity = 2.2; sun.position.set(-4, 10, 10); sun.target.position.set(0, 0, 0); scene.add(new THREE.AmbientLight(0x8a90c8, .35));
  const pos = { chatgpt: [-1.45, 0, -2.6], claude: [1.45, 0, -2.6], gemini: [-1.2, 0, 1.7], grok: [1.2, 0, 1.7] };
  ORDEN.forEach(n => { const c = ISLA_IAS[n][1]; const g = new THREE.Group(); g.position.set(...pos[n]); scene.add(g);
    mesh(new THREE.CylinderGeometry(.95, 1.0, .12, 48), M(0x2a2950), [0, .06, 0], g);
    const aro = mesh(new THREE.TorusGeometry(1.0, .04, 10, 64), new THREE.MeshBasicMaterial({ color: c }), [0, .1, 0], g, false); aro.rotation.x = Math.PI / 2;
    const halo = mesh(new THREE.PlaneGeometry(2.8, 2.8), new THREE.MeshBasicMaterial({ map: brillo(c), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }), [0, .02, 0], g, false); halo.rotation.x = -Math.PI / 2;
    const b = makeBot(c); b.scale.setScalar(1.5); b.position.set(0, .12, 0); g.add(b); B[n] = b; });
}
window.TOTAL = 12;
window.renderFrame = function (T) {
  const t0 = .8, paso = 1.8; const i = Math.max(0, Math.min(5, Math.floor((T - t0) / paso))); const expr = EXPRS[i]; const lt = T - t0 - i * paso;
  ORDEN.forEach((n, j) => { ponerExpresion(B[n], expr, T + j * .3); B[n].rotation.y = 0; });
  const a = Math.sin(T * .35) * .1, r = 10.6; camera.position.set(Math.sin(a) * r, 5.4, Math.cos(a) * r); camera.fov = 44; camera.updateProjectionMatrix(); camera.lookAt(0, 1.5, -.5);
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#07071a'); g.addColorStop(1, '#16143a'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  renderer.render(scene, camera); ctx.drawImage(renderer.domElement, 0, 0);
  ORDEN.forEach(n => iconoExpresion(B[n], expr, T, 1.15));
  const s = pop(Math.min(1, Math.max(0, lt) / .3)); ctx.save(); ctx.translate(W / 2, 330); ctx.scale(s, s); ctx.font = '800 76px I'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; const w = ctx.measureText(NOMBRE[expr]).width + 100; rr(-w / 2, -64, w, 128, 40); ctx.fillStyle = 'rgba(8,10,20,.9)'; ctx.fill(); ctx.strokeStyle = '#5ec8ff'; ctx.lineWidth = 5; ctx.stroke(); ctx.fillStyle = '#fff'; ctx.fillText(NOMBRE[expr], 0, 4); ctx.restore();
  const fo = Math.max(0, (T - 11.5) / .5); if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  return comp.toDataURL('image/jpeg', .9);
};
Promise.all(['700 40px I', '800 40px I', '900 40px I'].map(f => document.fonts.load(f))).then(() => { build(); window.READY = true; });
