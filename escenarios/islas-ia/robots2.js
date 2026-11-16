// ===== Robots v2 (estilo de las portadas de ChatGPT, 16/11/2026) =====
// makeBot2('chatgpt'|'claude'|'gemini'|'grok') → robot chibi: cabeza grande de carcasa brillante, visor negro
// con ojos de neón del color de la IA, accesorios propios y placa en el pecho. Mantiene la misma
// estructura que makeBot (userData.body/head/arms/feet) para que funcionen ponerExpresion e iconoExpresion.
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
function activarReflejos(int = .45) { const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = int; }
const BOT2 = {
  chatgpt: { col: 0x2bd6a6, ojo: '#5dffd0', casco: 0xf2f0f6, letra: 'GPT', acc: 'auris' },
  claude: { col: 0xff8a4c, ojo: '#ffc35a', casco: 0xf4efe9, letra: 'C', acc: 'antenas' },
  gemini: { col: 0x3d8bff, ojo: '#6fd8ff', casco: 0xeef2f8, letra: 'G', acc: 'lentes' },
  grok: { col: 0xdfe3ec, ojo: '#7dff8a', casco: 0x2b2e37, letra: 'X', acc: 'casco' },
};
function placaTex(txt, bg) { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); x.fillStyle = bg; x.beginPath(); x.roundRect(8, 8, 240, 240, 48); x.fill(); x.fillStyle = '#fff'; x.font = `800 ${txt.length > 1 ? 92 : 150}px I`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, 128, 138); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function lentesTex(col) { const c = document.createElement('canvas'); c.width = 512; c.height = 220; const x = c.getContext('2d'); x.strokeStyle = col; x.shadowColor = col; x.shadowBlur = 20; x.lineWidth = 16; x.lineJoin = 'round';
  for (const cx of [150, 362]) { x.beginPath(); x.roundRect(cx - 92, 30, 184, 150, 36); x.stroke(); } x.beginPath(); x.moveTo(242, 90); x.quadraticCurveTo(256, 76, 270, 90); x.stroke(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function makeBot2(n) {
  const d = BOT2[n]; const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const shell = (c, o = {}) => new THREE.MeshPhysicalMaterial(Object.assign({ color: c, roughness: .32, metalness: .05, clearcoat: 1, clearcoatRoughness: .18 }, o));
  const mCasco = shell(d.casco), mCol = shell(d.col, { roughness: .38 }), mBlanco = shell(n === 'grok' ? 0xc9ced8 : 0xf6f5fa);
  const mVisor = new THREE.MeshPhysicalMaterial({ color: 0x05060a, roughness: .08, metalness: .2, clearcoat: 1, clearcoatRoughness: .04 });
  // cuerpo
  const torso = mesh(new THREE.SphereGeometry(.25, 32, 24), mBlanco, [0, .4, 0], body); torso.scale.set(1, 1.1, .9);
  const cint = mesh(new THREE.TorusGeometry(.235, .03, 12, 40), mCol, [0, .3, 0], body); cint.rotation.x = Math.PI / 2;
  const placa = mesh(new THREE.PlaneGeometry(.17, .17), new THREE.MeshStandardMaterial({ map: placaTex(d.letra, n === 'grok' ? '#1a1c22' : '#' + new THREE.Color(d.col).multiplyScalar(.75).getHexString()), roughness: .4 }), [0, .43, .226], body, false); placa.rotation.x = -.12;
  // cabeza
  const head = new THREE.Group(); head.position.set(0, .93, 0); body.add(head);
  const craneo = mesh(new THREE.SphereGeometry(.37, 40, 30), mCasco, [0, 0, 0], head); craneo.scale.set(1.1, .96, .98);
  const tapa = mesh(new THREE.SphereGeometry(.375, 40, 16, 0, Math.PI * 2, 0, .55), mCol, [0, .0, 0], head); tapa.scale.set(1.1, .96, .98); tapa.rotation.x = -.35;
  const visor = mesh(new THREE.SphereGeometry(.34, 48, 32), mVisor, [0, -.02, .07], head); visor.scale.set(1.04, .74, .92);
  
  // ojos de neón (ponerExpresion cambia la textura)
  const cara = new THREE.Mesh(new THREE.PlaneGeometry(.5, .215), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, toneMapped: false })); cara.position.set(0, -.02, .395); head.add(cara);
  const lagrima = new THREE.Mesh(new THREE.SphereGeometry(.035, 12, 10), new THREE.MeshBasicMaterial({ color: 0x5ec8ff })); lagrima.scale.set(1, 1.4, 1); lagrima.visible = false; head.add(lagrima);
  const brilloVisor = mesh(new THREE.PlaneGeometry(.5, .3), new THREE.MeshBasicMaterial({ map: brillo(new THREE.Color(d.ojo).getHex()), transparent: true, opacity: .35, depthWrite: false, blending: THREE.AdditiveBlending }), [0, -.01, .37], head, false);
  // accesorios
  if (d.acc === 'auris' || d.acc === 'antenas') {
    for (const s of [-1, 1]) { const ar = new THREE.Group(); ar.position.set(s * .4, -.02, 0); head.add(ar);
      const cup = mesh(new THREE.CylinderGeometry(.12, .12, .07, 32), mBlanco, [0, 0, 0], ar); cup.rotation.z = Math.PI / 2;
      const neon = mesh(new THREE.TorusGeometry(.1, .018, 10, 40), new THREE.MeshBasicMaterial({ color: d.col, toneMapped: false }), [s * .04, 0, 0], ar, false); neon.rotation.y = Math.PI / 2;
      mesh(new THREE.CylinderGeometry(.085, .085, .02, 28), mCol, [s * .042, 0, 0], ar).rotation.z = Math.PI / 2; }
    const banda = mesh(new THREE.TorusGeometry(.41, .028, 12, 48, Math.PI), mCol, [0, -.02, 0], head); banda.scale.set(1, .98, 1);
  }
  if (d.acc === 'antenas') for (const s of [-1, 1]) { const an = new THREE.Group(); an.position.set(s * .2, .3, -.02); an.rotation.z = -s * .35; head.add(an);
    mesh(new THREE.CylinderGeometry(.014, .014, .22, 10), M(0xc8ccd6, { metalness: .8, roughness: .3 }), [0, .11, 0], an); mesh(new THREE.SphereGeometry(.045, 16, 12), new THREE.MeshStandardMaterial({ color: d.col, emissive: d.col, emissiveIntensity: .8 }), [0, .24, 0], an); }
  if (d.acc === 'lentes') { const l = new THREE.Mesh(new THREE.PlaneGeometry(.5, .215), new THREE.MeshBasicMaterial({ map: lentesTex(d.ojo), transparent: true, depthWrite: false, toneMapped: false })); l.position.set(0, -.02, .4); head.add(l);
    for (const s of [-1, 1]) mesh(new THREE.SphereGeometry(.1, 24, 16), mCol, [s * .4, -.02, 0], head).scale.set(.45, 1, 1); }
  if (d.acc === 'casco') { for (const s of [-1, 1]) { const al = mesh(new THREE.BoxGeometry(.04, .2, .3), shell(0x9aa0ad, { metalness: .6, roughness: .25 }), [s * .4, .02, -.02], head); al.rotation.z = s * .15; }
    mesh(new THREE.BoxGeometry(.08, .05, .5), shell(0x9aa0ad, { metalness: .6, roughness: .25 }), [0, .36, -.02], head).rotation.x = -.2; }
  // brazos con manos
  const arms = [];
  for (const s of [-1, 1]) { const pv = new THREE.Group(); pv.position.set(s * .25, .55, 0); body.add(pv);
    const a = mesh(new THREE.CapsuleGeometry(.065, .16, 6, 12), mCol, [s * .05, -.12, 0], pv); a.rotation.z = s * .35;
    mesh(new THREE.SphereGeometry(.075, 18, 14), mBlanco, [s * .1, -.25, .01], pv); arms.push(pv); }
  const feet = [];
  for (const s of [-1, 1]) { const f = mesh(new THREE.SphereGeometry(.1, 18, 12), mCol, [s * .12, .07, .03], g); f.scale.set(1, .75, 1.25); feet.push(f); }
  g.userData = { body, head, arms, feet, cara, lagrima, ojo: d.ojo };
  return g;
}
