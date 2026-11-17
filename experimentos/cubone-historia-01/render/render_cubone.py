#!/usr/bin/env python3
"""Renderizar Cubone desde assets de internet elegidos (atribución en README) y voz de Gemini."""
from pathlib import Path
import subprocess,math,wave,os
import numpy as np
P=Path(__file__).resolve().parent.parent
OUT=P/"render";OUT.mkdir(exist_ok=True)
# Ventanas ajustadas a la locución de Gemini (Whisper base, verificadas).
cuts=[0.,6.8,14.2,17.5,24.8,27.2,34.6,40.7,47.9,55.2,59.5,61.752]
FPS=24
def execute(cmd):
 print("RUN",str(cmd[:12]),flush=True)
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-2800:])
for i in range(11):
 sec=cuts[i+1]-cuts[i]
 frames=round(sec*FPS)
 inp=P/"escenas"/f"escena-{i+1:02d}.jpg"
 out=OUT/f"clip-{i+1:02d}.mp4"
 # Ajustamos entrada a 1 fps, zoompan genera cuadros con efecto de acercamiento lento y sin deformar.
 vf=f"zoompan=z='min(1.0+on*0.00043,1.16)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=540x960:fps={FPS},format=yuv420p"
 cmd=['ffmpeg','-nostdin','-y','-loglevel','error','-loop','1','-framerate','1','-i',str(inp),'-vf',vf,
      '-frames:v',str(frames),'-c:v','libx264','-pix_fmt','yuv420p','-preset','fast','-crf','27',
      '-r',str(FPS),'-an','-movflags','+faststart',str(out)]
 execute(cmd)
 print(f'SEGMENTO {i+1}/11 {sec:.1f}s {out.stat().st_size//1024}KiB',flush=True)
with (OUT/"concat.txt").open('w') as f:
 for i in range(11):f.write(f"file '{OUT/f'clip-{i+1:02d}.mp4'}'\n")
execute(['ffmpeg','-nostdin','-y','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy',str(OUT/'sin_audio.mp4')])
# Música original: pads suaves, notas sin melodías externas, ambiente cinematográfico.
sr=22050
duration=62.5
t=np.arange(int(sr*duration),dtype=np.float32)/sr
music=np.zeros_like(t)
roots=[(0,146.83),(10,174.61),(20,130.81),(29,196),(39,174.61),(48,146.83),(56,174.61)]
for j,(start,root) in enumerate(roots):
 end=roots[j+1][0] if j+1<len(roots) else duration
 a=np.clip((t-start)/2,0,1)*np.clip((end-t)/2.4,0,1)
 for ratio,w in [(1,.48),(1.5,.2),(2,.17),(2.25,.15)]:
  m=root*ratio
  music+=a*w*(np.sin(2*np.pi*m*t+math.pi*j/2)+.16*np.sin(2*np.pi*2*m*t))
# Efecto de brillo disperso, sintetizado, no es música ajena.
for j,when in enumerate([3,9,15,26,30,36,42,49,55,59]):
 note=(440,523.25,659.25,587.33)[j%4]
 env=np.exp(-np.maximum(0,t-when)*2.6)*(t>=when)
 music+=env*.085*np.sin(2*np.pi*note*t)
music+=.010*np.sin(2*np.pi*42*t)
music*=np.clip(t/2,0,1)*np.clip((duration-t)/3,0,1)
music=np.clip(music*.26,-.7,.7)
with wave.open(str(OUT/'musica_original.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
 f.writeframes((music*32767).astype(np.int16).tobytes())
execute(['ffmpeg','-nostdin','-y','-loglevel','error',
 '-i',str(OUT/'sin_audio.mp4'),'-i',str(P/'voz-gemini-charon.mp3'),'-i',str(OUT/'musica_original.wav'),
 '-filter_complex','[1:a]loudnorm=I=-17:TP=-2:LRA=9[voz];[2:a]volume=0.35[mus];[voz][mus]amix=inputs=2:duration=first:weights=1 0.5,alimiter=limit=0.93[a]',
 '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',
 str(P/'cubone-historia-01.mp4')])
print('FINAL',str(P/'cubone-historia-01.mp4'),os.stat(P/'cubone-historia-01.mp4').st_size,flush=True)

