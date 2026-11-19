// preflight.mjs — control ANTES de renderizar. Uso (dentro de la carpeta del proyecto):
//   node ../preflight.mjs            → escribe preflight.json y sale con código 1 si hay errores
// Revisa: narracion.txt ≡ textos de seg(...) en main.js (sin *), timing.json (wt/dur/ratio),
// voz.mp3 (existe, duración, no muda) e imágenes de NOMBRES en img/ (existen, tamaño, alfa).
import fs from 'fs';
import { execFileSync, spawnSync } from 'child_process';
const err = [], info = {};
const leer = f => { try { return fs.readFileSync(f, 'utf8'); } catch { err.push(`falta ${f}`); return ''; } };
const palabras = t => t.replace(/\*/g, '').split(/\s+/).filter(Boolean);
const limpia = w => w.toLowerCase().replace(/[^a-záéíóúüñ0-9]/g, '');

// 1) narración vs seg
const narr = palabras(leer('narracion.txt'));
const main = leer('main.js');
const segs = [...main.matchAll(/seg\('((?:[^'\\]|\\.)*)'/g)].map(m => m[1]);
const segW = segs.flatMap(palabras);
info.palabras = { narracion: narr.length, seg: segW.length, segmentos: segs.length };
if (!segs.length) err.push('no encontré seg(\'...\') en main.js');
if (narr.length !== segW.length) err.push(`narracion.txt tiene ${narr.length} palabras y los seg ${segW.length}`);
const n = Math.min(narr.length, segW.length);
for (let i = 0; i < n; i++) if (limpia(narr[i]) !== limpia(segW[i])) { err.push(`palabra ${i}: narracion «${narr[i]}» ≠ seg «${segW[i]}»`); break; }

// 2) timing.json
let tm = null; try { tm = JSON.parse(leer('timing.json')); } catch { err.push('timing.json inválido'); }
if (tm) {
  const wt = tm.wt || [];
  if (wt.length !== narr.length) err.push(`timing.json tiene ${wt.length} tiempos y la narración ${narr.length} palabras`);
  for (let i = 1; i < wt.length; i++) if (!(wt[i] > wt[i - 1])) { err.push(`wt no crece en la palabra ${i} (${wt[i - 1]} → ${wt[i]})`); break; }
  if (wt.length && !(wt.at(-1) < tm.dur)) err.push(`última palabra (${wt.at(-1)}) no es menor que dur (${tm.dur})`);
  info.dur_voz = tm.dur;
}
const log = fs.existsSync('align.log') ? fs.readFileSync('align.log', 'utf8') : '';
const r = log.match(/ratio ([\d.]+)/); if (r) { info.ratio = +r[1]; if (info.ratio < .8 || info.ratio > 1.15) err.push(`ratio de align ${info.ratio} fuera de 0,8–1,15`); }

// 3) voz
const probe = (f, args) => execFileSync('ffprobe', ['-v', 'error', ...args, '-of', 'json', f], { encoding: 'utf8' });
if (fs.existsSync('voz.mp3')) {
  const d = +JSON.parse(probe('voz.mp3', ['-show_entries', 'format=duration'])).format.duration; info.voz_mp3 = d;
  if (tm && Math.abs(d - tm.dur) > .3) err.push(`voz.mp3 dura ${d.toFixed(2)} s y timing.json dice ${tm.dur}`);
} else err.push('falta voz.mp3');
if (fs.existsSync('voz.mp3')) {
  const vd = spawnSync('ffmpeg', ['-hide_banner', '-i', 'voz.mp3', '-af', 'volumedetect', '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const m = vd.match(/max_volume: (-?[\d.]+)/); info.max_volume = m ? +m[1] : null;
  if (!m || info.max_volume < -30) err.push(`voz.mp3 parece muda (max_volume ${info.max_volume} dB)`);
}

// 4) imágenes declaradas en NOMBRES (si el main.js usa imágenes)
const nom = main.match(/const NOMBRES\s*=\s*\[([^\]]*)\]/);
if (nom) for (const q of nom[1].matchAll(/'([^']+)'/g)) {
  const f = fs.existsSync('img') ? fs.readdirSync('img').find(x => x.includes(q[1])) : null;
  if (!f) { err.push(`falta imagen img/*${q[1]}*`); continue; }
  const st = JSON.parse(probe('img/' + f, ['-show_entries', 'stream=width,height,pix_fmt'])).streams[0];
  info['img:' + f] = `${st.width}x${st.height} ${st.pix_fmt}`;
  if (/obj-/.test(f) && !/a/.test(st.pix_fmt.replace('yuv', ''))) err.push(`${f} no tiene alfa (${st.pix_fmt})`);
}

const ok = err.length === 0;
fs.writeFileSync('preflight.json', JSON.stringify({ ok, errores: err, info }, null, 1));
console.log(ok ? 'PREFLIGHT OK' : 'PREFLIGHT FALLÓ:\n- ' + err.join('\n- '));
process.exit(ok ? 0 : 1);
