// ===== Islitas de las IA (estilo de las referencias de Gonzalo, 16/11/2026) =====
// Plataforma violeta redondeada, aro de neón del color de la IA (con resplandor),
// bandera con el nombre en un mástil plateado, pedestal violeta con botón del color
// y el robot chibi adelante. isla.luz(k) la ilumina (0 = tenue, 1 = encendida).
const ISLA_IAS = { chatgpt: ['ChatGPT', 0x2bd6a6, '#13896b'], claude: ['Claude', 0xff8a4c, '#d9622b'], gemini: ['Gemini', 0x3d8bff, '#1f4fe0'], grok: ['Grok', 0xdfe3ec, '#22242c'], github: ['GitHub', 0x5ec8ff, '#24292f'] };
function brillo(color) { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); const g = x.createRadialGradient(128, 128, 70, 128, 128, 128); const col = '#' + color.toString(16).padStart(6, '0'); g.addColorStop(0, col + '00'); g.addColorStop(.62, col + 'ff'); g.addColorStop(.72, col + '88'); g.addColorStop(1, col + '00'); x.fillStyle = g; x.fillRect(0, 0, 256, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function banderaTex(text, bg) { const c = document.createElement('canvas'); c.width = 640; c.height = 300; const x = c.getContext('2d'); x.fillStyle = bg; x.beginPath(); x.roundRect(0, 0, 640, 300, 26); x.fill(); x.fillStyle = 'rgba(255,255,255,.12)'; x.fillRect(0, 0, 640, 40); x.fillStyle = '#fff'; x.font = '800 118px I'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(text, 320, 160); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function crearIsla(n, R = 2.4) {
  const [lab, c, f] = ISLA_IAS[n]; const g = new THREE.Group();
  const violeta = M(0x4b4a86, { roughness: .55 }), violetaOsc = M(0x34336a, { roughness: .6 });
  // plataforma: cuerpo + borde redondeado + tapa
  mesh(new THREE.CylinderGeometry(R * .97, R * .9, R * .22, 64), violetaOsc, [0, R * .11, 0], g);
  const borde = mesh(new THREE.TorusGeometry(R * .9, R * .07, 16, 80), violeta, [0, R * .22, 0], g); borde.rotation.x = Math.PI / 2;
  mesh(new THREE.CylinderGeometry(R * .9, R * .9, R * .1, 64), violeta, [0, R * .24, 0], g);
  const top = R * .29;
  // aro de neón en la base + resplandor
  const aroR = n === 'grok' ? R * 1.12 : R * 1.02, aroT = n === 'grok' ? R * .02 : R * .035;
  const aroMat = new THREE.MeshBasicMaterial({ color: c }); const aro = mesh(new THREE.TorusGeometry(aroR, aroT, 12, 120), aroMat, [0, R * .03, 0], g, false); aro.rotation.x = Math.PI / 2;
  const halo = mesh(new THREE.PlaneGeometry(R * 2.9, R * 2.9), new THREE.MeshBasicMaterial({ map: brillo(c), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }), [0, R * .02, 0], g, false); halo.rotation.x = -Math.PI / 2;
  const halo2 = mesh(new THREE.TorusGeometry(aroR, R * .09, 10, 120), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .25, depthWrite: false, blending: THREE.AdditiveBlending }), [0, R * .05, 0], g, false); halo2.rotation.x = Math.PI / 2;
  // bandera
  const mastil = new THREE.Group(); mastil.position.set(-R * .62, top, -R * .5); g.add(mastil);
  mesh(new THREE.CylinderGeometry(R * .022, R * .022, R * 1.35, 12), M(0xc8ccd6, { metalness: .8, roughness: .25 }), [0, R * .675, 0], mastil);
  mesh(new THREE.SphereGeometry(R * .035, 12, 8), M(0xc8ccd6, { metalness: .8 }), [0, R * 1.36, 0], mastil);
  const band = mesh(new THREE.BoxGeometry(R * .62, R * .29, R * .025), new THREE.MeshStandardMaterial({ map: banderaTex(lab, f), roughness: .6 }), [R * .33, R * 1.18, 0], mastil);
  // pedestal con botón
  const ped = new THREE.Group(); ped.position.set(R * .5, top, -R * .3); g.add(ped);
  mesh(new THREE.BoxGeometry(R * .5, R * .32, R * .42), violetaOsc, [0, R * .16, 0], ped);
  const boton = mesh(new THREE.CylinderGeometry(R * .085, R * .09, R * .04, 24), new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: .6 }), [R * .07, R * .34, -R * .03], ped);
  if (n === 'grok') { boton.visible = false; ped.position.set(-R * .25, top, -R * .05); const hoja = mesh(new THREE.BoxGeometry(R * .3, R * .012, R * .24), M(0xc9c6dc, { roughness: .8 }), [0, R * .33, 0], ped); hoja.rotation.y = .25; }
  if (n === 'claude') { boton.visible = false; const base = mesh(new THREE.BoxGeometry(R * .36, R * .02, R * .26), M(0xff8a4c, { roughness: .4 }), [0, R * .33, R * .03], ped); const tapa = mesh(new THREE.BoxGeometry(R * .36, R * .24, R * .02), M(0xff8a4c, { roughness: .4 }), [0, R * .45, -R * .1], ped); tapa.rotation.x = -.25; const pant = mesh(new THREE.PlaneGeometry(R * .3, R * .19), new THREE.MeshStandardMaterial({ color: 0x1b1a2e, emissive: 0xff8a4c, emissiveIntensity: .25 }), [0, R * .45, -R * .085], ped, false); pant.rotation.x = -.25; }
  if (n === 'github') { boton.visible = false; const bandeja = mesh(new THREE.BoxGeometry(R * .44, R * .06, R * .34), new THREE.MeshStandardMaterial({ color: 0x5ec8ff, emissive: 0x1a4a70, emissiveIntensity: .5 }), [0, R * .35, 0], ped); for (let i = 0; i < 4; i++) { const p = mesh(new THREE.BoxGeometry(R * .32, R * .008, R * .24), M(0xf4f6fb), [R * (i * .01 - .015), R * (.39 + i * .012), R * (i % 2 ? .01 : -.01)], ped); p.rotation.y = (i - 1.5) * .06; } }
  // robot
  const bot = makeBot(c); bot.scale.setScalar(R * .72); bot.position.set(-R * .05, top, R * .22); g.add(bot);
  if (n === 'grok') bot.position.set(R * .25, top, R * .15);
  if (n === 'github') { bot.visible = false; ped.position.set(0, top, R * .05); ped.scale.setScalar(1.5); }
  const luzIA = new THREE.PointLight(c, 0, R * 3); luzIA.position.set(0, R * .9, R * .6); g.add(luzIA);
  g.userData = { lab, c, f, bot, aro, halo, halo2, boton, luzIA, top,
    luz(k) { k = Math.max(0, Math.min(1, k)); aroMat.color.setHex(c).multiplyScalar(.4 + .6 * k); halo.material.opacity = .12 + .88 * k; halo2.material.opacity = .05 + .55 * k; aro.scale.setScalar(1 + .015 * k); boton.material.emissiveIntensity = .5 + 1.5 * k; luzIA.intensity = 6 * k; } };
  g.userData.luz(0);
  return g;
}
