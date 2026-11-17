#!/usr/bin/env python3
"""Cubone V2: sobreimpresiones educativas originales; conserva voz, escenas y música V1."""
from pathlib import Path
import subprocess, json, math, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[2]/"cubone-historia-01"
OBJ=Path(__file__).resolve().parent.parent/"objetos"
ORIGINAL=ROOT/"cubone-historia-01.mp4"
DEST=Path(__file__).resolve().parent.parent/"cubone-historia-02.mp4"
def run(cmd):
    print("Ejecutando:",cmd[0],cmd[-1],flush=True)
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-4500:])
def ui_sound(path):
    sr=22050;dur=62.0;t=np.arange(int(sr*dur),dtype=np.float32)/sr
    audio=np.zeros(len(t),dtype=np.float32)
    cue=[1.35,7.15,18.4,35.2,59.75]
    for k,start in enumerate(cue):
        tt=t-start
        active=(tt>=0)&(tt<0.48)
        v=np.clip(tt,0,.48)
        fade=(1-np.minimum(v/.48,1))**2
        base=[830,660,735,988,784][k]
        chirp=np.sin(2*np.pi*(base*v+120*v*v))*.55+np.sin(2*np.pi*(base*1.5*v))*.18
        audio+=np.where(active,chirp*fade*0.14,0)
    data=np.asarray(np.clip(audio,-.99,.99)*32767,dtype=np.int16)
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(data.tobytes())
def main():
    if not ORIGINAL.exists():
        raise FileNotFoundError("Primero debe existir el render original cubone-historia-01.mp4")
    metadata=json.loads((OBJ/"escenas.json").read_text(encoding="utf8"))
    items=metadata["elementos"]
    sound=OBJ/"sonidos-ui.wav"
    ui_sound(sound)
    cmd=["ffmpeg","-nostdin","-y","-hide_banner","-loglevel","error",
         "-i",str(ORIGINAL)]
    for item in items:
        cmd+=["-loop","1","-framerate","24","-i",str(OBJ/item["asset"])]
    sound_id=len(items)+1
    cmd+=["-i",str(sound)]
    filters=[]
    last="[0:v]"
    for n,item in enumerate(items,start=1):
        start,end=item["inicio"],item["fin"]
        fadeout=end-0.42
        filters.append(f"[{n}:v]format=rgba,fade=t=in:st={start}:d=0.36:alpha=1,fade=t=out:st={fadeout}:d=0.42:alpha=1[p{n}]")
        label=f"[o{n}]"
        xx=f"if(lt(t,{start+0.65}),max(0,82-128*(t-{start})),0)"
        yy=f"3*sin(2.4*t)"
        filters.append(f"{last}[p{n}]overlay=x='{xx}':y='{yy}':eval=frame:shortest=1:format=auto{label}")
        last=label
    filters.append(f"[0:a][{sound_id}:a]amix=inputs=2:duration=first:weights=1 0.28:normalize=0,alimiter=limit=0.96[aout]")
    cmd+=["-filter_complex",";".join(filters),"-map",last,"-map","[aout]","-c:v","libx264",
          "-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-r","24",
          "-c:a","aac","-b:a","160k","-t","61.754","-movflags","+faststart",str(DEST)]
    run(cmd)
    print("VIDEO V2",DEST,DEST.stat().st_size,flush=True)
if __name__=="__main__":main()

