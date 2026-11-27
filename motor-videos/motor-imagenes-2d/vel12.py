import re,subprocess,sys
src='voz-original.mp3'
D=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout)
out=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-36dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',out)];se=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',out)]
sil=list(zip(ss,se+[D]*(len(ss)-len(se))))
# segmentos de voz
sp=[];t=0
for a,b in sil:
    if a>t+0.01: sp.append([t,a])
    t=b
if t<D-0.01: sp.append([t,D])
sp=[[max(0,a-0.04),min(D,b+0.04)] for a,b in sp]
gaps=[sp[i+1][0]-sp[i][1] for i in range(len(sp)-1)]
speech=sum(b-a for a,b in sp); target=D/1.2
def tot(k): return speech+sum(min(g,(0.32 if g>=0.7 else 0.12)*k) for g in gaps)
tempo=1.0
if tot(1)>target: tempo=tot(1)/target; k=1
else:
    lo,hi=1,20
    for _ in range(60):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if tot(m)<target else (lo,m)
    k=lo
ng=[min(g,(0.32 if g>=0.7 else 0.12)*k) for g in gaps]
parts=[];f=[]
for i,(a,b) in enumerate(sp):
    f.append(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}]');parts.append(f'[s{i}]')
    if i<len(ng): f.append(f'aevalsrc=0:d={ng[i]:.3f}:s=24000,aformat=channel_layouts=mono[g{i}]');parts.append(f'[g{i}]')
f.append(''.join(parts)+f'concat=n={len(parts)}:v=0:a=1,atempo={tempo:.4f}[o]')
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',';'.join(f),'-map','[o]','-ar','24000','-ac','1','-b:a','160k','voz.mp3'],check=True)
print('D',D,'target',round(target,2),'k',round(k,2),'tempo',round(tempo,3))
