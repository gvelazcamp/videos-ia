import * as THREE from 'three';

const W = 1080, H = 1920, WD = 0.33, HOLD = 0.5;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => (x = clamp(x), x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const pop = x => { x = clamp(x); if (x === 0) return 0; if (x === 1) return 1; return Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * 2 * Math.PI / 3) + 1; };
const rnd = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(12345);

// ---------- renderer ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0, 0);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
const comp = document.createElement('canvas'); comp.width = W; comp.height = H;
const ctx = comp.getContext('2d');
document.body.appendChild(comp);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 300);
const hemi = new THREE.HemisphereLight(0xc8d4ff, 0x2a2438, 1.15); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 2.1);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 80 });
sun.shadow.bias = -0.0008; sun.shadow.radius = 4;
scene.add(sun, sun.target);

const M = (c, o = {}) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: .85, metalness: 0 }, o));
function mesh(g, m, p, parent, shadow = true) { const x = new THREE.Mesh(g, m); if (p) x.position.set(...p); x.castShadow = shadow; x.receiveShadow = true; if (parent) parent.add(x); return x; }

// ---------- builders ----------
function makeBot(color) {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const mb = M(color, { roughness: .6 }), mw = M(0xeceaf2, { roughness: .5 }), mk = M(0x0b0b10, { roughness: .3 });
  const torso = mesh(new THREE.SphereGeometry(.32, 28, 20), mb, [0, .43, 0], body); torso.scale.set(1, 1.08, .95);
  const head = new THREE.Group(); head.position.set(0, .93, 0); body.add(head);
  mesh(new THREE.SphereGeometry(.3, 28, 20), mw, [0, 0, 0], head);
  const vis = mesh(new THREE.SphereGeometry(.3, 28, 16), mk, [0, .01, .1], head); vis.scale.set(.86, .38, .74);
  for (const s of [-1, 1]) { const e = mesh(new THREE.SphereGeometry(.052, 12, 10), M(0xffffff, { emissive: 0xffffff, emissiveIntensity: .6 }), [s * .1, .015, .315], head, false); e.scale.set(1.1, .8, .5); }
  const arms = [];
  for (const s of [-1, 1]) {
    const pv = new THREE.Group(); pv.position.set(s * .3, .58, 0); body.add(pv);
    const a = mesh(new THREE.CapsuleGeometry(.075, .2, 6, 10), mb, [s * .06, -.14, 0], pv); a.rotation.z = s * .35; arms.push(pv);
  }
  const feet = [];
  for (const s of [-1, 1]) feet.push(mesh(new THREE.SphereGeometry(.11, 14, 10), mb, [s * .14, .08, .03], g));
  g.userData = { body, head, arms, feet };
  return g;
}
function labelTex(text, bg, fg = '#fff') {
  const c = document.createElement('canvas'); c.width = 512; c.height = 320; const x = c.getContext('2d');
  x.fillStyle = bg; x.fillRect(0, 0, 512, 320); x.fillStyle = fg; x.font = '800 92px I'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(text, 256, 166);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ---------- background ----------
const stars = Array.from({ length: 70 }, () => [rnd() * W, rnd() * H * .55, rnd() * 1.6 + .4, rnd()]);
function drawBg(dark) {
  const g = ctx.createRadialGradient(W / 2, H * .45, 60, W / 2, H * .45, H * .75);
  g.addColorStop(0, dark ? '#191a33' : '#22224a'); g.addColorStop(.55, dark ? '#0f1022' : '#14152e'); g.addColorStop(1, '#06060d');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (const [x, y, r, a] of stars) { ctx.globalAlpha = .15 + a * .3; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); }
  ctx.globalAlpha = 1;
}

// ---------- overlay helpers ----------
function rr(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
function proj(v) { const p = v.clone().project(camera); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H, p.z < 1]; }
function wpos(d, local) { return d.g.localToWorld(local.clone()); }
function badge(b, k) {
  const s = pop(k); if (s <= 0) return;
  ctx.save(); const x = b.x ?? W / 2, y = b.y ?? H * .67; ctx.translate(x, y); ctx.scale(s, s);
  ctx.font = '800 66px I'; const bw = ctx.measureText(b.big).width; ctx.font = '700 26px I'; const sw = b.small ? ctx.measureText(b.small).width + 10 : 0;
  const w = bw + sw + 44, h = 92; rr(-w / 2, -h / 2, w, h, 18); ctx.fillStyle = 'rgba(16,16,24,.9)'; ctx.fill();
  ctx.strokeStyle = 'rgba(255,255,255,.12)'; ctx.lineWidth = 2; ctx.stroke();
  ctx.textBaseline = 'alphabetic'; ctx.font = '800 66px I'; ctx.fillStyle = b.color || '#fff'; ctx.textAlign = 'left'; ctx.fillText(b.big, -w / 2 + 22, 23);
  if (b.small) { ctx.font = '700 26px I'; ctx.fillStyle = b.smallColor || (b.color && b.color !== '#fff' ? b.color : '#c8c8d4'); ctx.fillText(b.small, -w / 2 + 22 + bw + 10, 23); }
  if (b.sub) { ctx.font = '700 22px I'; ctx.fillStyle = '#d0d0dc'; ctx.textAlign = 'center'; ctx.fillText(b.sub, 0, 76); }
  ctx.restore();
}
function pill(text, x, y, bg, fg = '#fff', size = 40, k = 1) {
  const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.font = `800 ${size}px I`; const w = ctx.measureText(text).width + size * 1.1, h = size * 1.7;
  rr(-w / 2, -h / 2, w, h, size * .35); ctx.fillStyle = bg; ctx.fill();
  ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, size * .06); ctx.restore();
}
function bar(x, y, v, label) {
  const w = 300, h = 26; ctx.font = '800 26px I'; ctx.fillStyle = '#fff'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle'; ctx.fillText(label, x - w / 2 - 14, y + 1);
  rr(x - w / 2, y - h / 2, w, h, h / 2); ctx.fillStyle = 'rgba(10,10,16,.85)'; ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 2; ctx.stroke();
  if (v > .005) { rr(x - w / 2 + 4, y - h / 2 + 4, (w - 8) * v, h - 8, (h - 8) / 2); ctx.fillStyle = v > .5 ? '#3ddc6a' : v > .22 ? '#f2c230' : '#ef4b3c'; ctx.fill(); }
}
function bubble(text, x, y, k) {
  const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.font = '800 38px I'; const w = ctx.measureText(text).width + 50, h = 70;
  rr(-w / 2, -h, w, h, 16); ctx.fillStyle = '#fff'; ctx.fill(); ctx.beginPath(); ctx.moveTo(-14, -2); ctx.lineTo(0, 18); ctx.lineTo(14, -2); ctx.fill();
  ctx.fillStyle = '#111'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, -h / 2 + 2); ctx.restore();
}
function xmark(x, y, k) {
  const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.beginPath(); ctx.arc(0, 0, 44, 0, 7); ctx.fillStyle = '#e8463a'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 10; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-15, -15); ctx.lineTo(15, 15); ctx.moveTo(15, -15); ctx.lineTo(-15, 15); ctx.stroke(); ctx.restore();
}
function flash(x, y, k) {
  if (k <= 0) return; const r = 70 + 50 * k; const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, `rgba(255,255,255,${.95 * k})`); g.addColorStop(.25, `rgba(220,240,255,${.6 * k})`); g.addColorStop(1, 'rgba(200,230,255,0)');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  ctx.strokeStyle = `rgba(255,255,255,${.8 * k})`; ctx.lineWidth = 4; ctx.beginPath();
  for (let i = 0; i < 4; i++) { const a = i * Math.PI / 4 + .2; ctx.moveTo(x - Math.cos(a) * r * 1.1, y - Math.sin(a) * r * 1.1); ctx.lineTo(x + Math.cos(a) * r * 1.1, y + Math.sin(a) * r * 1.1); }
  ctx.stroke();
}
function tiles(y, k, list = ['chatgpt', 'claude', 'gemini'], x0 = W / 2, size = 120) {
  const short = { chatgpt: 'GPT', claude: 'C', gemini: 'G' };
  list.forEach((n, i) => {
    const kk = clamp(k * 1.6 - i * .25); const s = pop(kk); if (s <= 0) return;
    const x = x0 + (i - (list.length - 1) / 2) * (size + 34);
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); rr(-size / 2, -size / 2, size, size, size * .26); ctx.fillStyle = ISL[n].css; ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = `800 ${n === 'chatgpt' ? size * .3 : size * .48}px I`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(short[n], 0, 3); ctx.restore();
  });
}
function card(text, k) {
  const s = pop(k); if (s <= 0) return; ctx.save(); ctx.translate(W / 2, H * .44); ctx.scale(s, s);
  ctx.font = '800 64px I'; const w = ctx.measureText(text).width + 150, h = 170;
  ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 40; rr(-w / 2, -h / 2, w, h, 22); ctx.fillStyle = '#f4f4f6'; ctx.fill(); ctx.shadowBlur = 0;
  // simple mark: three dots
  ['#2bb59a', '#e5824c', '#4a7ee6'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(-w / 2 + 56 + (i % 2) * 18, -14 + i * 14, 11, 0, 7); ctx.fill(); });
  ctx.fillStyle = '#111'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(text, -w / 2 + 100, 4); ctx.restore();
}
function rec(t) { const x = 54, y = H * .62; rr(x, y, 104, 40, 8); ctx.fillStyle = 'rgba(0,0,0,.5)'; ctx.fill(); ctx.strokeStyle = '#e8463a'; ctx.lineWidth = 2; ctx.stroke(); ctx.fillStyle = (t * 1.5 % 1) < .6 ? '#ff3b30' : '#6a1a16'; ctx.beginPath(); ctx.arc(x + 22, y + 20, 7, 0, 7); ctx.fill(); ctx.fillStyle = '#ff6d62'; ctx.font = '800 22px I'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText('REC', x + 38, y + 21); }

// ---------- captions ----------
function drawCaption(seg, lt) {
  const toks = seg.toks; const T = seg.t0 + lt; let n = 0; while (n < toks.length && T >= seg.wt[n] - 0.03) n++; if (seg === S_[0]) n = Math.max(n, 1);
  const size = 50, lh = 66, maxW = 900; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  // layout all with bold
  ctx.font = `700 ${size}px I`; const space = ctx.measureText(' ').width;
  const lines = [[]]; let lw = 0;
  toks.forEach((t, i) => { const w = ctx.measureText(t.w).width; if (lw + w > maxW && lines.at(-1).length) { lines.push([]); lw = 0; } lines.at(-1).push({ ...t, i, ww: w }); lw += w + space; });
  // only layout lines containing revealed words (progressive like ref)
  const y0 = 250;
  lines.forEach((ln, li) => {
    const tw = ln.reduce((a, b) => a + b.ww, 0) + space * (ln.length - 1); let x = W / 2 - tw / 2; const y = y0 + li * lh;
    for (const t of ln) {
      if (t.i < n) {
        const age = T - seg.wt[t.i]; const k = clamp(age / .1);
        if (t.key) { ctx.globalAlpha = k; rr(x - 8, y - size + 4, t.ww + 16, size + 14, 6); ctx.fillStyle = 'rgba(40,52,140,.75)'; ctx.fill(); ctx.strokeStyle = 'rgba(170,185,255,.85)'; ctx.lineWidth = 2; ctx.stroke(); }
        const fresh = age < .55 || t.key;
        ctx.globalAlpha = k; ctx.font = `${fresh ? 700 : 500} ${size}px I`; ctx.fillStyle = fresh ? '#fff' : '#b9b9c9';
        ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 10; ctx.fillText(t.w, x, y); ctx.shadowBlur = 0; ctx.globalAlpha = 1;
      }
      x += t.ww + space;
    }
  });
}

