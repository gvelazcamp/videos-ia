import math,wave,array
SR=44100;BPM=104;beat=60/BPM;DUR=float(__import__("sys").argv[1]) if len(__import__("sys").argv)>1 else 40.0
prog=[(45,[57,60,64]),(41,[57,60,65]),(48,[55,60,64]),(43,[55,59,62])]  # Am F C G
mel=[76,74,72,74,76,79,76,74, 72,74,72,69,72,74,76,72]
f=lambda m:440*2**((m-69)/12)
n=int(DUR*SR);buf=[0.0]*n
bar=4*beat
for i in range(n):
    t=i/SR;b=int(t/bar)%4;tb=t%bar;bass,ch=prog[b]
    v=0
    # bajo triángulo en negras
    tq=tb%beat;ph=(f(bass)*t)%1;v+=(4*abs(ph-.5)-1)*.16*math.exp(-tq*2.5)
    # acordes pad suaves
    for m in ch:ph=(f(m)*t)%1;v+=(1 if ph<.5 else -1)*.012
    # melodía pulso en corcheas, sólo cada 2 compases para dejar lugar a la voz
    k=int(t/(beat/2));te=t%(beat/2)
    if (int(t/bar)%2)==0:
        m=mel[k%16];ph=(f(m)*t)%1;v+=(1 if ph<.25 else -1)*.035*math.exp(-te*6)
    # hi-hat ruido
    if te<0.02:v+=((hash((k,7))%200)/100-1)*.03
    fade=min(1,t/1.5,(DUR-t)/2.5);buf[i]=v*fade
out=array.array('h',(int(max(-1,min(1,x))*32767*.7) for x in buf))
w=wave.open('musica.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(out.tobytes());w.close()
print('ok')
