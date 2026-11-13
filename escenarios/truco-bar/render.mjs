import puppeteer from 'puppeteer-core';
import { spawn } from 'child_process';
import fs from 'fs';
const [mode, a, b, out] = process.argv.slice(2); // mode: frames|video
const browser = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new',
  args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files', '--ignore-gpu-blocklist'] });
const page = await browser.newPage();
page.on('console', m => console.log('PAGE', m.text())); page.on('pageerror', e => console.log('ERR', e.message));
await page.setViewport({ width: 400, height: 400 });
await page.goto('file://' + process.cwd() + '/scene2.html');
await page.waitForFunction('window.READY === true', { timeout: 60000 });
const total = await page.evaluate('window.TOTAL'); console.log('TOTAL', total);
if (mode === 'frames') {
  for (const t of a.split(',').map(Number)) { const d = await page.evaluate(t => renderFrame(t), t); fs.writeFileSync(`${b}/f_${String(t).padStart(6, '0')}.jpg`, Buffer.from(d.split(',')[1], 'base64')); }
} else {
  const fps = 30, N = Math.ceil(total * fps);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < N; f++) {
    const d = await page.evaluate(t => renderFrame(t), f / fps);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(f, N, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
