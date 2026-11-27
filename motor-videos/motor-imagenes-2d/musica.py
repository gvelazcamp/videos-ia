import numpy as np, wave
sr=44100; T=131; t=np.arange(int(sr*T))/sr; out=np.zeros(len(t))
def add(sig,s):
    i=int(s*sr); m=min(len(sig),len(out)-i)
    if m>0: out[i:i+m]+=sig[:m]
mf=lambda m:440*2**((m-69)/12)
prog=[[57,60,64,71],[53,57,60,67],[48,52,55,62],[55,59,62,66]]  # Am9 Fmaj9 Cadd9 G
bar=4.0
for b in range(int(T/bar)+1):
    ac=prog[b%4]; s=b*bar
    n=int((bar+1.5)*sr); tt=np.arange(n)/sr
    env=np.minimum(tt/1.5,1)*np.minimum((bar+1.5-tt)/1.5,1)
    for m in ac:
        f=mf(m-12)
        add((np.sin(2*np.pi*f*tt)+.4*np.sin(2*np.pi*f*1.004*tt)+.2*np.sin(4*np.pi*f*tt))*env*.035,s)
    if b>=1:
        for j in range(8):
            m=ac[[0,2,1,3,2,0,3,1][j]]+12+(12 if j%4==3 else 0)
            n2=int(2.5*sr); t2=np.arange(n2)/sr
            e2=np.exp(-t2*2.5)*np.minimum(t2/.005,1)
            add((np.sin(2*np.pi*mf(m)*t2)+.3*np.sin(2*np.pi*mf(m)*3*t2))*e2*.05,s+j*bar/8)
# lluvia suave (ruido filtrado)
rng=np.random.default_rng(1); nz=rng.standard_normal(len(t))
k=np.ones(30)/30; nz=nz-np.convolve(nz,k,'same'); out+=nz*.012
fade=np.ones(len(t)); n=int(4*sr); fade[-n:]=np.linspace(1,0,n); fade[:int(2*sr)]=np.linspace(0,1,int(2*sr)); out*=fade
out=out/np.abs(out).max()*.8
d=(np.stack([out,out*.98],1)*32767).astype(np.int16)
w=wave.open('musica.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(d.tobytes());w.close()
