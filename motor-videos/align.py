import numpy as np, re, json, subprocess
from scipy.signal import butter, sosfiltfilt, find_peaks
sr=16000
x=np.fromfile('voz.raw',dtype=np.int16).astype(np.float32)/32768
dur=len(x)/sr
sos=butter(4,[300,2500],btype='band',fs=sr,output='sos'); y=sosfiltfilt(sos,x)
hop=160; n=len(y)//hop
env=np.sqrt(np.mean(y[:n*hop].reshape(n,hop)**2,axis=1))
k=np.hanning(7); k/=k.sum(); env=np.convolve(env,k,'same')
edb=20*np.log10(env+1e-6)
# silences
out=subprocess.run(['ffmpeg','-i','voz.mp3','-af','silencedetect=noise=-36dB:d=0.06','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',out)]; se=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',out)]
sil=[(0.0,se[0])] if se[0]<ss[0] else []
sil+= [(a,b) for a,b in zip(ss, se[1:] if se[0]<ss[0] else se)]
m=[]
for a,b in sorted(sil):
    if m and a-m[-1][1]<0.05: m[-1]=(m[-1][0],max(b,m[-1][1]))
    else: m.append((a,b))
sil=m
speech_start=sil[0][1] if sil[0][0]==0 else 0.0
# peaks (syllable nuclei)
pk,_=find_peaks(edb,prominence=4,distance=7,height=edb.max()-38)
pt=pk*hop/sr
# text
txt=[l.strip() for l in open('narracion.txt',encoding='utf-8') if l.strip()]
words=[];segw=[]
for si,l in enumerate(txt):
    toks=l.split(' '); segw.append(len(toks))
    for t in toks: words.append((si,t))
V='aeiouáéíóúü'
def syl(w):
    w=w.lower(); w=re.sub(r'[^a-záéíóúüñ]','',w)
    special={'chatgpt':4,'ia':2,'claude':1,'gemini':3,'bitcoin':2,'grok':1,'github':2,'premium':3}
    if w in special: return special[w]
    w=w.replace('qu','q').replace('gue','ge').replace('gui','gi')
    c=0; prev=None
    for ch in w:
        if ch in V:
            if prev is None: c+=1
            else:
                strong=lambda v: v in 'aeoáéóíú'
                if strong(prev) and strong(ch): c+=1
            prev=ch
        else: prev=None
    return max(c,1)
S=[syl(t) for _,t in words]
cum=np.concatenate([[0],np.cumsum(S)])
punct=[bool(re.search(r'[,.:?!»]$',t)) or (i+1<len(words) and words[i+1][0]!=words[i][0] and False) for i,(_,t) in enumerate(words)]
# gaps: index g = after word g (0..N-2)
N=len(words)
P=len(pt); r=P/cum[-1]
pk_before=lambda t: np.searchsorted(pt,t)
inner=[s for s in sil if s[0]>speech_start+0.05 and s[1]<dur-0.05]
M=len(inner)
# DP: assign each silence i to gap g (increasing)
INF=1e18
cost=np.full((M+1,N),INF); back=np.zeros((M+1,N),int)
# anchor 0: start (gap -1) -> represent with cum[0], peaks 0
speech_total=dur-sum(b-a for a,b in sil); R=cum[-1]/speech_total
def c(dP,dS,pun,dT=None,L=0):
    v=(dP-dS*r)**2/(dS*r+3) + (0 if pun else (2.5 if L<0.1 else 14))
    if dT is not None:
        e=dS/R; v+=1.5*(dT-e)**2/(e+0.25)
        rate=dS/max(dT,0.05)
        if rate>10: v+=(rate-10)*3
    return v
prevP=0
for i,(a,b) in enumerate(inner):
    Pi=pk_before((a+b)/2)
    for g in range(N-1):
        Sg=cum[g+1]
        if i==0: cost[1][g]=c(Pi,Sg,punct[g],a-speech_start,b-a)
        else:
            Pp=pk_before(sum(inner[i-1])/2)
            best=INF;bj=-1
            for h in range(max(0,g-40),g):
                if cost[i][h]<INF:
                    v=cost[i][h]+c(Pi-Pp,Sg-cum[h+1],punct[g],a-inner[i-1][1],b-a)
                    if v<best: best=v;bj=h
            cost[i+1][g]=best; back[i+1][g]=bj
# end
Pend=P
tot=[cost[M][g]+c(Pend-pk_before(sum(inner[-1])/2),cum[-1]-cum[g+1],True) for g in range(N-1)]
g=int(np.argmin(tot)); asg=[0]*M
for i in range(M,0,-1): asg[i-1]=g; g=back[i][g]
# spans: list of (word_start_idx, word_end_idx_excl, t_start, t_end)
bounds=[(-1,speech_start)]+[(asg[i],inner[i][1]) for i in range(M)]
ends=[inner[i][0] for i in range(M)]+[ [s for s in sil if s[1]>=dur-0.05][0][0] if sil[-1][1]>=dur-0.05 else dur]
wt=[0]*N; report=[]
for j,((gidx,t0),t1) in enumerate(zip(bounds,ends)):
    w0=gidx+1; w1=(bounds[j+1][0]+1) if j+1<len(bounds) else N
    pks=pt[(pt>=t0)&(pt<=t1)]
    nsy=cum[w1]-cum[w0]
    for w in range(w0,w1):
        off=cum[w]-cum[w0]
        if w==w0: wt[w]=t0
        else:
            q=off*len(pks)/nsy if nsy else 0
            iq=int(np.floor(q)); fr=q-iq
            if len(pks)>=2:
                a=pks[min(iq,len(pks)-1)]; b=pks[min(iq+1,len(pks)-1)] if iq+1<len(pks) else t1
                tp=a+(b-a)*fr if iq<len(pks) else t1
                wt[w]=max(wt[w-1]+0.08, tp-0.07)
            else: wt[w]=t0+(t1-t0)*off/nsy
    report.append((round(t0,2),round(t1,2),len(pks),int(nsy),' '.join(t for _,t in words[w0:w1])))
for rr in report: print(rr)
json.dump({'wt':wt,'segw':segw,'dur':dur,'speech_start':speech_start},open('timing.json','w'))
print('peaks',P,'syll',cum[-1],'ratio',round(r,3),'silences',M)
