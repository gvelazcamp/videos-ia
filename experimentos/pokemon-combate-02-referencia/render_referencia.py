#!/usr/bin/env python3
"""Video fan animation Pikachu vs Cubone / v2: animate user-approved reference illustration.
Separate project; original battle (v1) remains untouched.
Source art is user-selected, character ownership remains with respective holders.
"""
from __future__ import annotations
import argparse,math,random,wave,os,subprocess
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance

ROOT=Path(__file__).resolve().parent
AS=ROOT/"assets";AS.mkdir(exist_ok=True)
W,H=540,960;FPS=24; DURATION=61.032
SRC_URL="https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/b887cc84-8271-4316-98c8-63da7fd9e0dd.png"
FONT="/usr/share/fonts/truetype/higgsfield/Metropolis-ExtraBold.ttf"
if not Path(FONT).exists():FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTS={}
def f(size):
    if size not in FONTS:FONTS[size]=ImageFont.truetype(FONT,size)
    return FONTS[size]
def txt(d,x,y,s,sz=19,fill="#fff5e5",stroke=0):
    d.text((int(x),int(y)),s,font=f(sz),fill=fill,stroke_width=stroke,stroke_fill="#161625")
def center(d,y,s,sz=19,fill="#fff0db",stroke=0):
    box=d.textbbox((0,0),s,font=f(sz),stroke_width=stroke)
    txt(d,(W-(box[2]-box[0]))/2,y,s,sz,fill,stroke)
def E(t):t=max(0,min(1,t));return t*t*(3-2*t)
def progress(t,a,b):return max(0,min(1,(t-a)/max(1e-6,(b-a))))
def lin(a,b,t):return a+(b-a)*E(t)
def download():
    dst=AS/"referencia-estilo-aprobado.png"
    if dst.exists() and dst.stat().st_size>100000:return dst
    req=Request(SRC_URL,headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(req,timeout=40) as src: dst.write_bytes(src.read(12_000_000))
    im=Image.open(dst);im.verify();return dst
POLYS={
"pikachu":[(0,639),(32,651),(90,671),(123,689),(97,739),(64,756),(144,772),(148,792),
           (167,753),(144,695),(149,669),(168,656),(211,699),(263,753),
           (271,665),(285,648),(311,657),(365,717),(395,752),(407,788),(408,830),
           (385,855),(383,879),(368,903),(340,909),(354,947),(331,966),(282,954),
           (241,929),(210,944),(180,946),(165,958),(117,952),(90,943),
           (43,945),(13,951),(0,938)],
"cubone":[(506,585),(532,568),(541,557),(538,538),(555,544),(570,558),(592,565),
          (635,553),(658,544),(679,556),(694,548),(685,524),(702,513),(738,518),
          (774,490),(786,471),(820,463),(848,475),(857,491),(856,512),
          (847,533),(825,541),(797,538),(765,553),(745,568),(720,588),
          (719,604),(746,614),(785,632),(820,666),(838,686),(850,711),(840,727),
          (814,750),(801,765),(773,775),(749,772),(718,785),(690,800),
          (645,803),(605,795),(576,809),(550,802),(535,783),(528,760),
          (515,738),(518,716),(506,692),(502,661),(503,635)]
}
def split():
    p=download()
    a=cv2.imread(str(p),cv2.IMREAD_COLOR)
    hsv=cv2.cvtColor(a,cv2.COLOR_BGR2HSV)
    allmask=np.zeros(a.shape[:2],np.uint8)
    for name,poly in POLYS.items():
        existing=AS/(name+"-sprite.png")
        mask=np.zeros(a.shape[:2],np.uint8)
        cv2.fillPoly(mask,[np.array(poly,np.int32)],255)
        outer=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)),iterations=1)
        inner=cv2.erode(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(29,29)),iterations=1)
        gc=np.where(outer>0,cv2.GC_PR_FGD,cv2.GC_BGD).astype(np.uint8)
        gc[inner>0]=cv2.GC_FGD
        if name=="pikachu":
            yellow=(hsv[:,:,0]>12)&(hsv[:,:,0]<41)&(hsv[:,:,1]>95)&(hsv[:,:,2]>130)&(mask>0)
            gc[yellow]=cv2.GC_FGD
        else:
            white=(hsv[:,:,1]<89)&(hsv[:,:,2]>148)&(mask>0)
            gc[white]=cv2.GC_FGD
        bgmodel=np.zeros((1,65),np.float64);fgmodel=np.zeros((1,65),np.float64)
        cv2.grabCut(a,gc,None,bgmodel,fgmodel,7,cv2.GC_INIT_WITH_MASK)
        alpha=np.uint8(((gc==cv2.GC_FGD)|(gc==cv2.GC_PR_FGD))*255)
        purple=(hsv[:,:,0]>=108)&(hsv[:,:,0]<=168)&(hsv[:,:,1]>37)
        if name=="cubone": purple|=(hsv[:,:,0]>168)&(hsv[:,:,1]>58)
        alpha[purple]=0
        alpha=cv2.morphologyEx(alpha,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
        alpha=cv2.GaussianBlur(alpha,(3,3),.6)
        yy,xx=np.where(alpha>0)
        x1=max(0,int(xx.min())-3);y1=max(0,int(yy.min())-3)
        x2=min(a.shape[1],int(xx.max())+4);y2=min(a.shape[0],int(yy.max())+4)
        rgba=cv2.cvtColor(a[y1:y2,x1:x2],cv2.COLOR_BGR2RGBA)
        rgba[:,:,3]=alpha[y1:y2,x1:x2]
        Image.fromarray(rgba).save(existing,optimize=True)
        (AS/(name+"-box.txt")).write_text(f"{x1},{y1},{x2},{y2}")
        allmask=np.maximum(allmask,cv2.dilate(np.uint8(alpha>12)*255,np.ones((25,25),np.uint8)))
    cleaned=cv2.inpaint(a,allmask,10,cv2.INPAINT_TELEA)
    # Preserve 100% of the original art except the areas underneath characters.
    smooth=cv2.GaussianBlur(allmask,(35,35),12).astype(np.float32)/255
    orig=a.astype(np.float32);clr=cleaned.astype(np.float32)
    combined=np.uint8(np.clip(clr*smooth[:,:,None]+orig*(1-smooth[:,:,None]),0,255))
    cv2.imwrite(str(AS/"escenario-sin-personajes.jpg"),combined,[cv2.IMWRITE_JPEG_QUALITY,93])
    print("BACKGROUND + sprites extracted",flush=True)
def sources():
    if not (AS/"escenario-sin-personajes.jpg").exists() or not (AS/"cubone-sprite.png").exists() or not (AS/"pikachu-sprite.png").exists():
        split()
    image=Image.open(AS/"referencia-estilo-aprobado.png").convert("RGBA").resize((W,H),Image.Resampling.LANCZOS)
    background=Image.open(AS/"escenario-sin-personajes.jpg").convert("RGBA").resize((W,H),Image.Resampling.LANCZOS)
    data=[]
    for name in ("pikachu","cubone"):
        im=Image.open(AS/(name+"-sprite.png")).convert("RGBA")
        x1,y1,x2,y2=[int(v) for v in (AS/(name+"-box.txt")).read_text().split(",")]
        x1=int(round(x1*W/864));y1=int(round(y1*H/1536))
        im=im.resize((int(round(im.width*W/864)),int(round(im.height*H/1536))),Image.Resampling.LANCZOS)
        data.append((im,(x1,y1)))
    return image,background,*data
def sprite(img,art,x,y,dx=0,dy=0,rot=0,sc=1):
    w,h=art.size
    if sc!=1:
        art=art.resize((max(1,int(w*sc)),max(1,int(h*sc))),Image.Resampling.BICUBIC)
    if rot:
        art=art.rotate(rot,resample=Image.Resampling.BICUBIC,expand=True)
    X=int(round(x+dx+(w-art.width)/2))
    Y=int(round(y+dy+(h-art.height)/2))
    img.alpha_composite(art,(X,Y))
    return (X,Y,art.width,art.height)
def effect_bolt(d,ax,ay,bx,by,seed,thickness=3):
    r=random.Random(seed)
    pts=[(int(ax),int(ay))]
    for i in range(1,12):
        u=i/12
        pts.append((int(ax+(bx-ax)*u+r.randint(-16,16)),int(ay+(by-ay)*u+r.randint(-12,12))))
    pts.append((int(bx),int(by)))
    d.line(pts,fill="#ffac42",width=thickness+8,joint="curve")
    d.line(pts,fill="#fffaac",width=thickness+5,joint="curve")
    d.line(pts,fill="#ffffff",width=thickness,joint="curve")
    for k in range(2,10,3):
        x,y=pts[k];d.line([(x,y),(x+r.randint(-35,35),y+r.randint(-30,30))],fill="#ffd569",width=3)
def burst(d,x,y,strength,seed,color="#ffe7ad",n=28):
    rng=random.Random(seed)
    for j in range(n):
        an=rng.random()*math.tau
        dist=strength*(30+rng.random()*80)
        xx=x+math.cos(an)*dist;yy=y+math.sin(an)*dist
        rr=1+(1-strength)*rng.random()*5
        d.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),fill=color)
        if j%3==0:d.line((x,y,xx,yy),fill="#fbc6a8",width=2)
def bone_drawing():
    # Isolated projectile based on the same bone shown in the selected reference; drawn as original asset.
    im=Image.new("RGBA",(170,104))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((28,36,143,68),radius=15,fill="#f7ead1",outline="#7c5267",width=4)
    for x in [23,144]:
        d.ellipse((x-15,20,x+20,52),fill="#ffefdb",outline="#75536a",width=4)
        d.ellipse((x-15,48,x+20,84),fill="#ffefdb",outline="#75536a",width=4)
    d.line((45,42,130,46),fill="#fff9e7",width=6)
    return im
def hp_frame(img,turn,p_hp,c_hp,attack=None):
    # Repaint only the exact HP/gauge/numbers region, keeping the stunning original HUD art.
    d=ImageDraw.Draw(img)
    # cubone gauge, border and numeric
    d.rounded_rectangle((301,74,454,96),radius=7,fill="#232238",outline="#d5d3dd",width=2)
    fill=int(144*max(0,min(1,c_hp/54)))
    if fill:
        d.rounded_rectangle((305,79,305+fill,89),radius=4,fill=("#64ef95" if c_hp>27 else "#ffdc58" if c_hp>13 else "#f4777d"))
        d.line((307,80,303+fill,80),fill="#dcffe7",width=1)
    d.rounded_rectangle((458,74,528,103),radius=4,fill="#241c31")
    txt(d,459,75,f"{max(0,int(round(c_hp)))}/54",14,fill="#fff8ee",stroke=1)
    # Pikachu gauge, numeric
    d.rounded_rectangle((59,683,226,709),radius=6,fill="#2b3345",outline="#e4e5e1",width=2)
    pfill=int(156*max(0,min(1,p_hp/51)))
    if pfill:
        d.rounded_rectangle((64,690,64+pfill,699),radius=3,fill="#67f48d" if p_hp>25 else "#ffcb50" if p_hp>12 else "#f67275")
        d.line((65,690,62+pfill,690),fill="#e5ffed",width=1)
    d.rounded_rectangle((229,681,303,714),radius=6,fill="#292d43")
    txt(d,229,685,f"{max(0,int(round(p_hp)))}/51",14,fill="#fff8ec",stroke=1)
    # hide fixed TURN 3 from source picture via matching dark panel
    d.rounded_rectangle((203,111,338,146),radius=8,fill="#251c33",outline="#ffdbb1",width=2)
    center(d,115,f"TURNO {turn}",18,"#fff4d1")
    if attack:
        color={"RAYO":"#ffeb8d","ATAQUE RÁPIDO":"#fff2e3","COLA FÉRREA":"#e6f5fd"}.get(attack,"#ffeac7")
        # emphasis bracket around existing move button, leave all English UI fully readable
        bb={"RAYO":(20,779,277,859),"ATAQUE RÁPIDO":(290,780,518,855),"COLA FÉRREA":(25,866,278,933)}.get(attack)
        if bb: d.rounded_rectangle(bb,radius=10,outline=color,width=5)
def caption(img,line,secondary="",tone="#fff0d0"):
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((77,180,463,242),radius=11,fill="#251f3ce8",outline="#e9b0a0",width=2)
    size=17 if len(line)<31 else 14
    box=d.textbbox((0,0),line,font=f(size))
    txt(d,(W-(box[2]-box[0]))/2,189,line,size,tone)
    if secondary:
        box=d.textbbox((0,0),secondary,font=f(11))
        txt(d,(W-(box[2]-box[0]))/2,216,secondary,11,"#ffddc5")
def bar_at(t,a,b,old,new):
    return lin(old,new,progress(t,a,b))
def frame(t,images,bone,tick):
    original,bg,(pk,pkpos),(cb,cbpos)=images
    a=max(0,min(1,t/DURATION))
    # Use source art exactly as chosen whenever characters are at rest; on moves,
    # expose inpainted layer only where sprites change position.
    animate=any(x<=t<y for x,y in [(9.1,12.2),(16.8,20.0),(23.0,25.8),(28.0,30.8),(34.4,38.7),(40.0,44.7),(47.0,52.2)])
    image=(bg.copy() if animate else original.copy())
    ui=True
    pika_dx=0;pika_dy=0;pika_rot=0;pika_sc=1
    cub_dx=0;cub_dy=0;cub_rot=0;cub_sc=1
    pik_hp=51.; cub_hp=54.
    active_attack=None; headline=""; sub=""
    d=ImageDraw.Draw(image)
    # Ambient atmospheric elements that make every frame alive
    for j in range(24):
        rng=random.Random(j*77)
        px=(rng.random()*W+math.sin(t*.42+j*1.3)*13)%W
        py=(rng.random()*410+170-math.sin(t*.5+j)*6)%H
        r=1+((j%5)==0)
        d.ellipse((px-r,py-r,px+r,py+r),fill=(255,221,190,115))
    if t<7.9:
        headline="¡PIKACHU VS. CUBONE!"
        sub="UN COMBATE BAJO LA LUNA"
    elif t<16.8:
        headline="¡PIKACHU USÓ RAYO!"
        sub="CUBONE ES DE TIPO TIERRA"
        active_attack="RAYO"
        if 9.1<=t<12.2:
            k=math.sin(math.pi*progress(t,9.1,12.2))
            pika_dx=-7*k;pika_rot=-3*k
    elif t<22.5:
        headline="¡CUBONE USÓ HUESO PALO!"
        sub="¡GOLPE DIRECTO!"
        pik_hp=bar_at(t,18.9,21.2,51,29)
        if 16.8<=t<20.0:
            k=math.sin(math.pi*progress(t,16.8,20.0))
            cub_dx=-73*k;cub_dy=-17*k;cub_rot=12*k
    elif t<27.3:
        headline="¡ATAQUE RÁPIDO!"
        sub="PIKACHU CONTRAATACA"
        active_attack="ATAQUE RÁPIDO"
        cub_hp=bar_at(t,24.2,26.3,54,38)
        if 23<=t<25.8:
            k=math.sin(math.pi*progress(t,23,25.8))
            pika_dx=120*k;pika_dy=-13*k;pika_rot=-17*k;pika_sc=1+.07*k
    elif t<32.2:
        headline="¡CUBONE USÓ CABEZAZO!"
        sub="¡AMBOS SIGUEN EN PIE!"
        pik_hp=bar_at(t,29,31.1,29,17)
        cub_hp=38
        if 28<=t<30.8:
            k=math.sin(math.pi*progress(t,28,30.8))
            cub_dx=-100*k;cub_rot=15*k
    elif t<39.5:
        headline="¡COLA FÉRREA!"
        sub="PIKACHU CAMBIA SU ESTRATEGIA"
        active_attack="COLA FÉRREA"
        pik_hp=17
        cub_hp=bar_at(t,36.3,38.4,38,18)
        if 34.4<=t<38.7:
            k=math.sin(math.pi*progress(t,34.4,38.7))
            pika_dx=99*k;pika_dy=-30*k;pika_rot=-8*k;pika_sc=1+.09*k
    elif t<45.0:
        headline="¡CUBONE USÓ HUESOMERANG!"
        sub="¡PASA ROZANDO A PIKACHU!"
        pik_hp=17;cub_hp=18
        if 40<=t<44.7:
            k=math.sin(math.pi*progress(t,40,44.7))
            cub_dx=-22*k;cub_rot=8*k
    elif t<54.6:
        headline="¡ATAQUE RÁPIDO FINAL!"
        sub="¡PIKACHU USA SUS ÚLTIMAS FUERZAS!"
        active_attack="ATAQUE RÁPIDO"
        pik_hp=17;cub_hp=bar_at(t,49.7,53.0,18,0)
        if 47<=t<52.2:
            k=math.sin(math.pi*progress(t,47,52.2))
            pika_dx=146*k;pika_dy=-15*k;pika_rot=-20*k;pika_sc=1+.12*k
            cub_dx=30*k;cub_rot=-8*k
    else:
        headline="¡VICTORIA DE PIKACHU!"
        sub="¿QUIÉN DEBERÍA SER EL PRÓXIMO RIVAL?"
        pika_dy=-10*abs(math.sin(t*5))
        cub_rot=-8
        pik_hp=17;cub_hp=0
    # Correct initial stats and damage state when scene switched
    if 22.5<=t<32.2:pik_hp=29 if t<29 else pik_hp
    if 27.3<=t<34.4:cub_hp=38
    if 32.2<=t<54.6:pik_hp=17
    if 39.5<=t<54.6:cub_hp=18 if t<49.7 else cub_hp
    # Compositing only when the sprite layer moves; default original artwork remains pixel-perfect.
    if animate:
        sprite(image,cb,*cbpos,dx=cub_dx,dy=cub_dy,rot=cub_rot,sc=cub_sc)
        sprite(image,pk,*pkpos,dx=pika_dx,dy=pika_dy,rot=pika_rot,sc=pika_sc)
        d=ImageDraw.Draw(image)
    # Motion VFX
    if 9.1<t<12.2:
        power=math.sin(math.pi*progress(t,9.1,12.2))
        for n in range(3+int(4*power)):
            effect_bolt(d,245+random.Random(tick+n).randint(-20,30),
                        524+random.Random(tick*2+n).randint(-30,30),400+random.Random(tick*3+n).randint(-50,20),
                        449+random.Random(tick*5+n).randint(-50,50),tick+n)
        if t>11.3:
            burst(d,395,455,progress(t,11.3,12.2),tick,"#ffdf96",24)
    if 18.4<t<20.8:
        strength=progress(t,18.4,20.8)
        if strength<.8:
            bx=400-270*E(strength/.8);by=427+130*math.sin(math.pi*strength)
            spr=bone.rotate(int(t*560)%360,expand=True,resample=Image.Resampling.BICUBIC)
            image.alpha_composite(spr,(int(bx),int(by)))
            d=ImageDraw.Draw(image)
        if strength>.45:burst(d,137,518,progress(strength,.45,.95),tick,"#fbd7a1",35)
    if 23.3<t<26.0 or 47.4<t<52.4:
        for m in range(7):
            k=random.Random(tick+m)
            x=53+k.randint(-7,100)+int(max(0,pika_dx)*.5)
            y=480+m*15
            d.line((x,y,x+42+m*6,y-8),fill="#fff0bd" if m%2 else "#f8e5d2",width=3)
        if (t>25.0 and t<26) or t>50.4:burst(d,380,476,.7,tick,"#ffdda4",38)
    if 28.8<t<31.4:
        burst(d,170,500,progress(t,28.8,31.4),tick,"#f7d3b1",28)
    if 35.8<t<38.8:
        d.arc((115,330,476,625),190,349,fill="#fff3df",width=13)
        d.arc((126,341,465,616),190,349,fill="#a4e8ff",width=5)
        if t>37:burst(d,374,482,progress(t,37,38.8),tick,"#c7eeff",42)
    if 40.4<t<44.4:
        u=progress(t,40.4,44.4)
        X=415-287*math.sin(math.pi*u);Y=490-210*math.sin(math.pi*u)
        spr=bone.rotate((int(t*720))%360,expand=True,resample=Image.Resampling.BICUBIC)
        image.alpha_composite(spr,(int(X),int(Y)))
        d=ImageDraw.Draw(image)
        if t>43.1:burst(d,190,428,progress(t,43.1,44.4),tick,"#ffe6cb",17)
    if 54.6<t:
        for j in range(30):
            r=random.Random(j*13)
            x=(r.randint(0,W)+t*(j%3+1)*8)%W;y=(r.randint(210,590)+(t-54.6)*20)%660+180
            col=["#fff0a2","#fcd1c1","#a2e2fc","#e7b6f4"][j%4]
            d.polygon([(x,y),(x+3,y+5),(x,y+10),(x-3,y+5)],fill=col)
    # Health HUD; avoid covering original characters with clunky rectangles.
    turn=1 if t<22.5 else 2 if t<32.2 else 3 if t<45 else 4
    hp_frame(image,turn,pik_hp,cub_hp,active_attack)
    if t>55:
        d=ImageDraw.Draw(image)
        d.rounded_rectangle((73,294,467,375),radius=17,fill="#241c3bdf",outline="#ffd8a9",width=3)
        center(d,301,"¡VICTORIA!",38,"#ffdf8a",stroke=1)
        center(d,341,"PIKACHU GANA EL COMBATE",13,"#fff0e5")
    else:
        caption(image,headline,sub)
    # fast flashes for attack impact
    if any(abs(t-at)<.07 for at in [10.75,19.5,25.2,30.0,37.4,50.2]):
        flash=Image.new("RGBA",(W,H),(255,241,206,32))
        image.alpha_composite(flash)
    # subtle film grain, using limited drawing operations
    return image.convert("RGB")
def sfx(path,duration):
    sr=22050
    tt=np.arange(int(sr*(duration+.8)),dtype=np.float32)/sr
    audio=np.zeros(tt.shape,np.float32)
    events=[(9.7,"zap"),(19.4,"impact"),(24.7,"dash"),(30.1,"impact"),(37.1,"impact"),(41.0,"dash"),(50.1,"impact"),(54.7,"victory")]
    rng=np.random.default_rng(214)
    for when,kind in events:
        d=tt-when
        active=(d>=0)&(d<.63)
        x=np.maximum(0,d)
        env=np.exp(-8*x)
        if kind=="zap":fx=np.sin(2*np.pi*(350*x+1900*x*x))*(rng.uniform(.5,1,len(tt)))
        elif kind=="impact":fx=np.sin(2*np.pi*85*x)+rng.normal(0,.22,len(tt))
        elif kind=="dash":fx=np.sin(2*np.pi*(480*x+750*x*x))
        else:fx=np.sin(2*np.pi*880*x)+np.sin(2*np.pi*1120*x)
        audio+=np.where(active,fx*env*.18,0).astype(np.float32)
    # free original synth ambience
    notes=[130.81,174.61,146.83,196.0,155.56,130.81,174.61,196.0]
    for j,note in enumerate(notes):
        start=j*8;end=min(duration,start+9)
        rise=np.clip((tt-start)/1.2,0,1);fall=np.clip((end-tt)/1.2,0,1)
        envelope=rise*fall
        audio+=envelope*(.052*np.sin(2*np.pi*note*tt)+.028*np.sin(2*np.pi*note*1.5*tt))
    audio=np.int16(np.clip(audio*.60,-.94,.94)*32767)
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(audio.tobytes())
def command(cmd):
    print("RUN:",str(cmd[:8]),flush=True)
    subprocess.run(cmd,check=True)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--preview",action="store_true")
    p.add_argument("--output",default=str(ROOT/"pikachu-vs-cubone-estilo-aprobado.mp4"))
    p.add_argument("--voice",default=str(ROOT.parent/"pokemon-combate-01"/"voz-gemini-charon.mp3"))
    args=p.parse_args()
    images=sources();bone=bone_drawing()
    if args.preview:
        times=[1.3,10.6,19.1,24.8,29.9,36.9,42.0,49.8,57.0]
        for t in times:
            im=frame(t,images,bone,int(t*FPS))
            im.save(ROOT/f"preview-{int(t):02d}.jpg",quality=86,optimize=True)
        print("Previews:",len(times),flush=True);return
    dst=Path(args.output);dst.parent.mkdir(parents=True,exist_ok=True)
    temp=dst.with_suffix(".video.mp4")
    vcmd=["ffmpeg","-nostdin","-y","-hide_banner","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(temp)]
    proc=subprocess.Popen(vcmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        count=math.ceil(DURATION*FPS)
        for i in range(count):
            im=frame(i/FPS,images,bone,i)
            proc.stdin.write(im.tobytes())
            if i%120==0:print("Frame",i,"/",count,flush=True)
        proc.stdin.close()
        errors=proc.stderr.read().decode("utf-8","replace")
        if proc.wait()!=0:raise RuntimeError(errors[-4500:])
    except Exception:
        proc.kill();raise
    wav=ROOT/"sfx-originales.wav";sfx(wav,DURATION)
    voice=Path(args.voice)
    if not voice.exists():raise FileNotFoundError(f"Falta voz Gemini: {voice}")
    command(["ffmpeg","-nostdin","-y","-loglevel","error","-i",str(temp),"-i",str(voice),"-i",str(wav),
         "-filter_complex","[1:a]loudnorm=I=-17:TP=-2:LRA=9[voice];[2:a]volume=.42[sound];[voice][sound]amix=inputs=2:duration=first:weights=1 .5:normalize=0,alimiter=limit=.95[a]",
         "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","128k","-t",str(DURATION),"-movflags","+faststart",str(dst)])
    print("VIDEO",dst,dst.stat().st_size,flush=True)
if __name__=="__main__":
    main()

