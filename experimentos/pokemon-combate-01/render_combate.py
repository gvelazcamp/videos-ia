#!/usr/bin/env python3
"""Pikachu vs Cubone — video game battle reel, original fan animation.
All animations, battle text, stage, UI, sounds and music generated here.
Uses original PNG assets already present in GitHub / PokeAPI.
Original projects remain untouched.
"""
from __future__ import annotations
import argparse, math, os, random, subprocess, sys, wave
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

ROOT=Path(__file__).resolve().parent
AS=ROOT/"assets"; AS.mkdir(exist_ok=True)
OUT=ROOT/"pokemon-pikachu-vs-cubone.mp4"
W,H=540,960
FPS=24
FONT="/usr/share/fonts/truetype/higgsfield/Metropolis-ExtraBold.ttf"
BODY="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not Path(FONT).exists():FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not Path(BODY).exists():BODY=FONT
PALETTE={"ink":"#18213e","cream":"#fff3de","gold":"#f9cf73","pink":"#ee9eb8","light":"#f5b5cb","red":"#ee5d69","blue":"#70c8f1","shadow":"#15243b"}
f_cache={}
def font(n,heavy=True):
    key=(n,heavy)
    if key not in f_cache:f_cache[key]=ImageFont.truetype(FONT if heavy else BODY,n)
    return f_cache[key]
def text(d,xy,string,size=19,color="#fff4de",heavy=True,stroke=0):
    d.text(xy,string,font=font(size,heavy),fill=color,stroke_width=stroke,stroke_fill="#17203a")
def bbox_text(d,s,sz):return d.textbbox((0,0),s,font=font(sz))
def middle(d,cy,string,sz=20,col="#fff5df"):
    b=bbox_text(d,string,sz);text(d,((W-(b[2]-b[0]))//2,cy),string,sz,col)
def pill(d,box,color,outline=None,r=12,width=2):
    d.rounded_rectangle(box,radius=r,fill=color,outline=outline,width=width)
def lerp(a,b,t):return a+(b-a)*max(0,min(1,t))
def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def between(t,a,b):return max(0,min(1,(t-a)/(b-a)))
def get(src,path):
    if path.exists():return
    r=Request(src,headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(r,timeout=40) as f:data=f.read(5_500_001)
    if not data.startswith(b"\x89PNG"):raise ValueError(f"Asset no es PNG: {src}")
    path.write_bytes(data)
def assets():
    get("https://raw.githubusercontent.com/gvelazcamp/videos-ia/main/experimentos/pikachu-castillo-terror/personaje-removebg-web.png",AS/"pikachu-original.png")
    get("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/104.png",AS/"cubone-oficial.png")
    for name in ("pikachu-original.png","cubone-oficial.png"):
        img=Image.open(AS/name).convert("RGBA")
        if img.getchannel("A").getextrema()[0]>=255:raise ValueError("Sprite sin transparencia "+name)
def gradient(top,mid,low):
    ar=np.zeros((H,W,3),dtype=np.uint8)
    a=np.array(top);b=np.array(mid);c=np.array(low)
    for y in range(H):
        t=y/H
        co=(a*(1-t/.66)+b*t/.66) if t<.66 else (b*(1-(t-.66)/.34)+c*(t-.66)/.34)
        ar[y,:,:]=np.array(co,dtype=np.uint8)
    return Image.fromarray(ar)
def moon(base):
    layer=Image.new("RGBA",(W,H));d=ImageDraw.Draw(layer)
    x,y,r=265,272,125
    for scale,alpha in [(1.46,12),(1.28,19),(1.15,29)]:
        rr=int(r*scale);d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(255,208,170,alpha))
    layer=layer.filter(ImageFilter.GaussianBlur(20))
    base.alpha_composite(layer)
    d=ImageDraw.Draw(base)
    d.ellipse((x-r,y-r,x+r,y+r),fill="#ffd8aa",outline="#fff0d8",width=4)
    rr=random.Random(5)
    for k in range(17):
        xx=x+rr.randint(-103,103);yy=y+rr.randint(-105,105)
        if (xx-x)**2+(yy-y)**2 > (r-21)**2:continue
        rad=rr.randint(8,27)
        d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),fill="#eeb9a0",outline="#f4caab",width=2)
    d.arc((x-120,y-100,x+120,y+90),170,260,fill="#fff2d9",width=4)
def torch(d,x,y):
    d.rectangle((x-12,y,x+12,y+16),fill="#4c4053")
    d.polygon([(x-18,y),(x+18,y),(x+7,y-11),(x-7,y-11)],fill="#96717b")
    d.ellipse((x-21,y-43,x+21,y+4),fill="#f9b16f")
    d.polygon([(x-8,y-2),(x-17,y-23),(x,y-60),(x+7,y-38),(x+13,y-24),(x+8,y-3)],fill="#ffcd74")
    d.polygon([(x-5,y-3),(x-8,y-24),(x+4,y-35),(x+9,y-7)],fill="#fff3ab")
def banner(d,x,y):
    d.polygon([(x,y),(x+51,y),(x+50,y+156),(x+27,y+177),(x+3,y+157)],fill="#893b59",outline="#f4ad80")
    d.rectangle((x-8,y-7,x+60,y+3),fill="#c99466")
    d.ellipse((x+13,y+56,x+40,y+85),fill="#f3c9ba",outline="#743753",width=3)
    d.line((x+9,y+70,x+43,y+70),fill="#8d3d63",width=5)
    d.ellipse((x+23,y+64,x+29,y+76),fill="#8d3d63")
def wall(d,x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill="#77617a",outline="#332e53",width=5)
    d.rectangle((x-7,y-20,x+w+7,y),fill="#5b4d6e",outline="#c89a8d",width=3)
    for row in range(int(h/28)):
        yy=y+row*28
        d.line((x+3,yy,x+w-3,yy),fill="#b18b96",width=2)
        for j in range(3):
            xx=x+(j+((row%2)*.5))*w/3
            d.line((int(xx),yy,int(xx),min(y+h,yy+26)),fill="#473b60",width=2)
def stage():
    canvas=gradient((42,33,81),(167,95,139),(223,155,146)).convert("RGBA")
    d=ImageDraw.Draw(canvas)
    for k in range(11):
        x=(k*97+17)%W; y=37+(k*47)%230
        d.ellipse((x-31,y,x+40,y+13),fill=(105,57,114,90))
        d.ellipse((x-6,y-17,x+34,y+13),fill=(89,57,112,110))
    moon(canvas)
    d=ImageDraw.Draw(canvas)
    for k in range(22):
        x=k*32-12;h=600-random.Random(k+2).randint(27,140)
        d.polygon([(x-18,620),(x+14,h),(x+42,620)],fill="#624d76")
    d.rectangle((0,580,W,665),fill="#574763")
    # Ancient ruin gate in mid-ground
    d.ellipse((148,391,395,679),fill="#3f3659",outline="#a0879a",width=12)
    d.ellipse((178,427,365,689),fill="#ad7298",outline="#473955",width=10)
    d.rectangle((141,515,185,703),fill="#65546d",outline="#3a3558",width=7)
    d.rectangle((352,517,400,701),fill="#65546d",outline="#3a3558",width=7)
    for off in range(0,150,34):
        d.line((141,532+off,185,532+off),fill="#b295a0",width=3)
        d.line((352,532+off,400,532+off),fill="#b295a0",width=3)
    wall(d,-14,290,82,343);wall(d,474,285,86,355)
    banner(d,17,316);banner(d,491,314)
    torch(d,98,565);torch(d,438,573)
    # Arena stone floor
    d.polygon([(0,630),(540,630),(540,960),(0,960)],fill="#91748b")
    for yy in (651,685,732,787,852,920):
        d.line((0,yy,540,yy),fill="#d49d9a",width=3)
    for k in range(48):
        yy=645+(k//8)*50;xx=(k%8)*71+(25 if (k//8)%2 else 0)
        d.line((xx,yy,xx,yy+48),fill="#594968",width=3)
    d.ellipse((91,657,466,906),fill="#b28b9b",outline="#654f71",width=5)
    d.ellipse((146,700,405,866),fill="#cda49d",outline="#f9c5a8",width=7)
    d.ellipse((202,746,350,826),fill="#f3d2bd",outline="#a94e70",width=14)
    d.line((146,785,405,785),fill="#a94e70",width=10)
    d.ellipse((252,765,291,806),fill="#efceba",outline="#a94e70",width=8)
    # Wind / rubble
    rng=random.Random(84)
    for j in range(52):
        x=rng.randint(5,533);y=rng.randint(660,910)
        d.polygon([(x,y),(x+int(rng.random()*9)+2,y-3),(x+4,y-7)],fill="#e0ad9f")
    d.rounded_rectangle((8,9,532,43),radius=12,fill=(31,31,65,170),outline=(250,180,189,150),width=2)
    text(d,(18,17),"POKÉMON ARENA",16,"#ffe9cc")
    text(d,(379,19),"EPISODIO 01",12,"#e9b6ce")
    return canvas.convert("RGB")
def sprite(path,height):
    im=Image.open(path).convert("RGBA")
    bbox=im.getbbox()
    if bbox:im=im.crop(bbox)
    w=int(im.width*height/im.height)
    im=im.resize((w,height),Image.Resampling.LANCZOS)
    return im
def img_at(base,im,center_x,bottom_y,deg=0,scale=1,shadow=True,opacity=1):
    if scale!=1:im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.BICUBIC)
    if deg:im=im.rotate(deg,resample=Image.Resampling.BICUBIC,expand=True)
    cx=int(center_x-im.width/2);by=int(bottom_y-im.height)
    if opacity<1:
        a=im.getchannel("A").point(lambda k:int(k*opacity));im.putalpha(a)
    if shadow:
        layer=Image.new("RGBA",base.size)
        ellipse=ImageDraw.Draw(layer)
        ellipse.ellipse((cx+15,bottom_y-7,cx+im.width-15,bottom_y+15),fill=(24,17,42,130))
        layer=layer.filter(ImageFilter.GaussianBlur(10))
        base.alpha_composite(layer)
    base.alpha_composite(im,(cx,by))
def box(d,x,y,w,h,fill="#263254",stroke="#ddc6ba",radius=11):
    d.rounded_rectangle((x,y,x+w,y+h),radius=radius,fill=fill,outline=stroke,width=3)
def pokeball(d,x,y,r=12):
    d.ellipse((x-r,y-r,x+r,y+r),fill="#fff0e5",outline="#25304b",width=2)
    d.pieslice((x-r,y-r,x+r,y+r),180,360,fill="#ef556d")
    d.line((x-r,y,x+r,y),fill="#1d2b48",width=3)
    d.ellipse((x-4,y-4,x+4,y+4),fill="#fff9dd",outline="#1d2b48",width=2)
def health_card(d,name,level,maxhp,hp,x,y,w=249,enemy=False):
    h=84;box(d,x,y,w,h,fill="#272642",stroke="#e7a6bb")
    text(d,(x+41,y+10),name,23,PALETTE["cream"])
    text(d,(x+w-68,y+14),f"NV.{level}",13,PALETTE["gold"])
    pokeball(d,x+23,y+27,11)
    text(d,(x+16,y+47),"PS",14,"#ffaaa2")
    bx=x+54;by=y+47;bw=w-73
    d.rounded_rectangle((bx,by,bx+bw,by+15),radius=6,fill="#1b243c",outline="#eee5d4",width=2)
    ratio=max(0,min(1,hp/maxhp));p=int((bw-7)*ratio)
    if p>0:d.rounded_rectangle((bx+3,by+3,bx+3+p,by+12),radius=4,fill=("#54d58a" if ratio>.5 else "#f5c658" if ratio>.25 else "#f56e73"))
    text(d,(x+w-90,y+66),f"{max(0,int(round(hp)))}/{maxhp}",12)
def menu(d,move,mode):
    # Large game UI, buttons 2x2, active move highlighted
    if mode=="intro":return
    x,y=12,792
    d.rounded_rectangle((x,y,W-12,H-8),radius=19,fill="#29345d",outline="#99b8fa",width=5)
    d.rounded_rectangle((x+5,y+7,W-17,837),radius=14,fill="#202d57",outline="#b1c5ef",width=2)
    middle(d,803, "¡ELIGE UN ATAQUE!" if mode=="command" else "COMBATE POKÉMON",20)
    opts=[("RAYO","ELÉCTRICO"),("ATAQUE RÁPIDO","NORMAL"),("COLA FÉRREA","ACERO"),("IMPACTRUENO","ELÉCTRICO")]
    for k,(name,typ) in enumerate(opts):
        xx=25+(k%2)*253; yy=851+(k//2)*51
        active=name==move
        fill="#f7cc6a" if active else "#efe9dd" if k%2 else "#bacbe1"
        d.rounded_rectangle((xx,yy,xx+239,yy+45),radius=9,fill=fill,outline="#f0e3d4" if active else "#6982a4",width=3)
        text(d,(xx+13,yy+6),name,14,"#292c42")
        text(d,(xx+13,yy+25),typ,10,"#5a5160")
        if active:
            d.polygon([(xx+220,yy+15),(xx+229,yy+23),(xx+220,yy+31)],fill="#aa3f5b")
def dialogue(d,headline,detail="",color="#ffd5a6"):
    # Sits above permanent move bar, like attack feedback
    box(d,20,308,500,88,fill="#242844",stroke="#e8b3ba",radius=12)
    text(d,(35,326),headline,19,color)
    if detail:text(d,(38,361),detail,13,"#f8efde",False)
def lightning(d,x1,y1,x2,y2,t,rng):
    points=[(x1,y1)]
    for j in range(1,9):
        tt=j/9;off=rng.randint(-26,26)
        points.append((int(x1+(x2-x1)*tt+off),int(y1+(y2-y1)*tt+off)))
    points.append((x2,y2))
    d.line(points,fill="#fffbe8",width=8,joint="curve")
    d.line(points,fill="#fff087",width=5,joint="curve")
    d.line(points,fill="#ffe956",width=2,joint="curve")
    for j in range(3):
        a=points[rng.randrange(2,7)]
        d.line([a,(a[0]+rng.randint(-45,45),a[1]+rng.randint(-40,40))],fill="#ffe477",width=3)
def bone_img():
    im=Image.new("RGBA",(150,110))
    d=ImageDraw.Draw(im)
    d.polygon([(27,44),(120,44),(120,67),(27,67)],fill="#f5e6d3",outline="#b5aa9d")
    for x in (17,125):
        d.ellipse((x-14,25,x+24,57),fill="#fff2e4",outline="#c2b9b0",width=3)
        d.ellipse((x-14,52,x+24,84),fill="#fff2e4",outline="#c2b9b0",width=3)
    d.rectangle((34,48,112,62),fill="#f8ecde")
    return im
def particles(d,x,y,frac,seed,color="#fff2c9",n=32):
    rng=random.Random(seed)
    for j in range(n):
        theta=rng.random()*math.tau
        radius=frac*(40+rng.random()*92)
        px=x+math.cos(theta)*radius;py=y+math.sin(theta)*radius
        rr=2+rng.random()*5*(1-frac)
        d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=color)
def sfx(path,duration,events):
    sr=22050;n=int(sr*duration);a=np.zeros(n,dtype=np.float32)
    tt=np.arange(n,dtype=np.float32)/sr
    for sec,kind in events:
        v=tt-sec
        mask=(v>=0)&(v<.65)
        w=np.maximum(0,v)
        amp=np.exp(-6*w)
        if kind=="zap":z=np.sin(2*np.pi*(440*w+2000*w*w))*np.random.default_rng(26).uniform(.5,1.0,n)
        elif kind=="hit":z=np.sin(2*np.pi*80*w)*np.exp(-2*w)+np.random.default_rng(5).standard_normal(n)*.23
        elif kind=="move":z=np.sin(2*np.pi*(350+650*w)*w)
        else:z=np.sin(2*np.pi*(600+300*w)*w)
        a+=np.where(mask,z*amp*.19,0).astype(np.float32)
    # Original game-like ambient chord, intentionally not any Pokémon song.
    for start,note in [(0,130.81),(7,146.83),(14,174.61),(21,155.56),(28,130.81),(35,174.61),(42,196.0),(49,130.81),(56,174.61)]:
        stop=min(duration,start+8)
        envelope=np.clip((tt-start)/.85,0,1)*np.clip((stop-tt)/1.2,0,1)
        for mul,weight in [(1,.05),(1.25,.035),(1.5,.02),(2,.02)]:
            a+=envelope*weight*np.sin(2*np.pi*note*mul*tt)
    # Bass pulse every 0.62s at low gain.
    for b in np.arange(0,duration,.64):
        dt=tt-b
        v=np.clip(dt,0,.16)
        a+=np.where((dt>=0)&(dt<.16),np.sin(2*np.pi*(65-16*v)*v)*np.exp(-35*v)*.052,0)
    a=np.clip(a*.48,-.85,.85)
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes((a*32767).astype(np.int16).tobytes())
def battle_events(duration):
    # Narration is 106 Spanish words; beat map normalizes if TTS duration differs.
    # start,end,label,character(action),pikachuhp,cubonehp,attack,detail
    return [
      (.000,.147,"¡PIKACHU VS CUBONE!","intro",51,54,"","La batalla empieza bajo la luna"),
      (.147,.279,"¡PIKACHU USÓ RAYO!","zap",51,54,"RAYO","¡NO TIENE EFECTO! CUBONE ES TIERRA."),
      (.279,.361,"¡CUBONE USÓ HUESO PALO!","boneclub",29,54,"","¡GOLPE DIRECTO!"),
      (.361,.443,"¡PIKACHU USÓ ATAQUE RÁPIDO!","quick",29,38,"ATAQUE RÁPIDO","¡CUBONE RECIBE DAÑO!"),
      (.443,.525,"¡CUBONE USÓ CABEZAZO!","headbutt",17,38,"","AMBOS RESISTEN"),
      (.525,.639,"¡PIKACHU USÓ COLA FÉRREA!","irontail",17,18,"COLA FÉRREA","¡QUÉ IMPACTO!"),
      (.639,.738,"¡CUBONE USÓ HUESOMERANG!","bonemerang",17,18,"","¡FALLÓ POR POCO!"),
      (.738,.886,"¡ATAQUE RÁPIDO FINAL!","final",17,0,"ATAQUE RÁPIDO","¡CUBONE NO PUEDE CONTINUAR!"),
      (.886,1.01,"¡PIKACHU GANA!","victory",17,0,"","UNA BATALLA CON RESPETO"),
    ]
def getbeat(u):
    for start,end,*rest in battle_events(1):
        if start<=u<end:return start,end,*rest
    return battle_events(1)[-1]
def draw(t,duration,base,pika,cubo,bone,frameidx):
    u=min(1.0,t/duration)
    event=getbeat(u)
    start,end,label,action,pik_hp,cub_hp,sel,detail=event
    prog=between(u,start,end)
    img=base.copy().convert("RGBA")
    d=ImageDraw.Draw(img)
    rng=random.Random(frameidx//2+314)
    # Warm torch flicker and tiny motes
    for cx,cy in [(97,518),(438,525)]:
        x=rng.randint(-4,4);y=rng.randint(-7,4)
        d.ellipse((cx-22+x,cy-11+y,cx+19+x,cy+23+y),fill=(253,208,111,40))
        d.ellipse((cx-6+x,cy-16+y,cx+8+x,cy+6+y),fill="#fff1ab")
    for j in range(20):
        px=(frameidx*2+j*47)%W
        py=(frameidx+j*67)%520+100
        d.ellipse((px,py,px+2,py+2),fill="#ffe7df")
    leftx=129;rightx=403;leftbottom=705;rightbottom=686
    leftrot=math.sin(t*8)*1.4;rightrot=math.sin(t*7+.6)*1.7
    leftscale=1+math.sin(t*5)*.014;rightscale=1+math.sin(t*4.5)*.013
    # Character attack movement; whole silhouettes move, preserving art.
    if action in ("quick","final"):
        k=math.sin(math.pi*min(1,prog/.78))**1.5
        leftx+=182*k
        leftrot-=20*k;leftscale+=.12*k
    if action=="irontail":
        k=math.sin(math.pi*min(1,prog/.72))
        leftx+=125*k;leftrot=24*k
    if action=="headbutt":
        k=math.sin(math.pi*min(1,prog/.7))
        rightx-=150*k;rightrot=17*k
    if action=="boneclub":
        k=math.sin(math.pi*min(1,prog/.74))
        rightx-=90*k;rightrot=18*k
    if action=="victory":
        leftbottom-=22*abs(math.sin(t*4.2))
        rightrot=-16*ease(between(prog,.02,.40))
        rightscale=1-.13*ease(between(prog,.02,.40))
        rightbottom+=13*ease(between(prog,.02,.40))
    img_at(img,cubo,rightx,rightbottom,rightrot,rightscale,opacity=1 if action!="victory" else .8)
    img_at(img,pika,leftx,leftbottom,leftrot,leftscale)
    d=ImageDraw.Draw(img)
    # Opponent HP animates after attacks, otherwise stays at post-event values.
    pik_new=pik_hp; cub_new=cub_hp
    if action=="boneclub":pik_new=lerp(51,29,ease(between(prog,.50,.82)))
    if action=="quick":cub_new=lerp(54,38,ease(between(prog,.48,.78)))
    if action=="headbutt":pik_new=lerp(29,17,ease(between(prog,.45,.8)))
    if action=="irontail":cub_new=lerp(38,18,ease(between(prog,.48,.8)))
    if action=="final":cub_new=lerp(18,0,ease(between(prog,.53,.84)))
    health_card(d,"CUBONE",18,54,cub_new,284,55,w=245,enemy=True)
    health_card(d,"PIKACHU",20,51,pik_new,12,700,w=258)
    # Turn number HUD
    turn=1 if u<.361 else 2 if u<.525 else 3 if u<.738 else 4
    if action=="intro":
        box(d,183,170,175,50,fill="#282743",stroke="#edc38e",radius=14)
        middle(d,178,"ROUND 01",23,"#ffe0a7")
        text(d,(221,257),"VS",77,"#ffe29f",stroke=3)
    else:
        box(d,199,175,142,43,fill="#222c50",stroke="#eac98b",radius=10)
        middle(d,183,f"TURNO {turn}",19,"#ffe3a3")
    # Animated attack VFX
    if action=="zap" and prog>.15 and prog<.85:
        for q in range(4):
            lightning(d,165+rng.randint(-30,25),540+rng.randint(-45,30),370+rng.randint(-45,30),540+rng.randint(-20,35),prog,rng)
        if prog>.6:
            box(d,112,320,319,78,fill="#3d335b",stroke="#fedc72",radius=15)
            middle(d,332,"¡NO TIENE EFECTO!",20,"#ffe69c")
            middle(d,359,"CUBONE ES TIPO TIERRA",13,"#f2e1cd")
    elif action=="boneclub" and prog>.25 and prog<.83:
        deg=prog*360
        img_at(img,bone,lerp(367,168,ease(between(prog,.23,.73))),lerp(570,595,prog),deg=deg,scale=.60,shadow=False)
        d=ImageDraw.Draw(img)
        if prog>.60:particles(d,168,590,between(prog,.60,.89),22,"#ffce92",32)
    elif action in ("quick","final") and prog>.18 and prog<.86:
        d=ImageDraw.Draw(img)
        for k in range(8):
            xx=leftx-75-k*17;yy=565+k*18
            d.line((xx,yy,xx+45,yy-8),fill="#fff4bc" if k%2 else "#c5f1ff",width=3)
        if prog>.58:particles(d,359,569,between(prog,.58,.95),58,"#ffefb1",33)
    elif action=="headbutt" and prog>.4 and prog<.85:
        d=ImageDraw.Draw(img)
        if prog>.60:particles(d,178,587,between(prog,.6,.91),37,"#ffe1b6",44)
    elif action=="irontail" and prog>.27 and prog<.9:
        d=ImageDraw.Draw(img)
        p=between(prog,.3,.85)
        d.arc((112-40*p,444-20*p,454+20*p,687+30*p),205,340,fill="#fff8e7",width=12)
        d.arc((118-40*p,450-20*p,448+20*p,681+30*p),205,340,fill="#a4e7ff",width=5)
        if prog>.6:particles(d,350,556,between(prog,.60,.9),52,"#b8edff",42)
    elif action=="bonemerang" and prog>.15 and prog<.87:
        k=math.sin(math.pi*prog)
        bx=355-155*k
        by=480-130*k
        img_at(img,bone,bx,by,deg=t*950,scale=.72,shadow=False)
        d=ImageDraw.Draw(img)
        if prog>.57:
            box(d,173,319,195,58,fill="#313558",stroke="#d6cff6")
            middle(d,335,"¡FALLÓ!",25,"#fff5d5")
    elif action=="victory":
        d=ImageDraw.Draw(img)
        for k in range(18):
            x=(52+33*k+frameidx*2)%W; y=(360+37*k-(frameidx//2)%(110))%670
            col=("#ffe5a1","#f3a4c9","#ace9ff")[k%3]
            d.polygon([(x,y),(x+4,y+6),(x,y+13),(x-4,y+6)],fill=col)
        box(d,80,307,380,113,fill="#332b54",stroke="#ffe2a1",radius=16)
        middle(d,321,"¿QUIÉN SIGUE?" if prog>.62 else "¡VICTORIA!",34 if prog>.62 else 43,"#ffdc8a")
        middle(d,377,"PIKACHU GANA EL COMBATE" if prog<=.62 else "DEJÁ TU PRÓXIMO RIVAL",15,"#fff6df")
    # Keep game interface legible over the whole fight.
    mode="intro" if action=="intro" else "command" if action in ("zap","quick","irontail","final") else "battle"
    menu(d,sel,mode)
    if action!="intro" and action!="victory" and not (action=="zap" and prog>.60):
        dialogue(d,label,detail,color="#ffdcaa" if action in ("zap","irontail","final") else "#ffe0e7")
    # Cinematic local flash only near hits, so no text is lost.
    return img.convert("RGB")
def parse():
    p=argparse.ArgumentParser()
    p.add_argument("--duration",type=float,default=52)
    p.add_argument("--voice",default="")
    p.add_argument("--preview",action="store_true")
    p.add_argument("--output",default=str(OUT))
    return p.parse_args()
def main():
    args=parse();assets()
    stage_img=stage();pika=sprite(AS/"pikachu-original.png",244);cubo=sprite(AS/"cubone-oficial.png",245);bone=bone_img()
    print("Assets",pika.size,cubo.size,flush=True)
    if args.preview:
        for t in [1.2,8,15,22,30,36,44,50]:
            im=draw(t,args.duration,stage_img,pika,cubo,bone,int(t*FPS))
            im.save(ROOT/f"preview-{int(t):02}.jpg",quality=80,optimize=True)
        print("Previews saved",flush=True);return
    frames=math.ceil(args.duration*FPS)
    dst=Path(args.output)
    dst.parent.mkdir(exist_ok=True,parents=True)
    video_tmp=dst.with_suffix(".video.mp4")
    cmd=["ffmpeg","-nostdin","-y","-loglevel","error","-f","rawvideo","-vcodec","rawvideo","-s",f"{W}x{H}","-pix_fmt","rgb24","-r",str(FPS),"-i","-","-an","-vcodec","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(video_tmp)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for k in range(frames):
            frame=draw(k/FPS,args.duration,stage_img,pika,cubo,bone,k)
            proc.stdin.write(frame.tobytes())
            if k%96==0:print("FRAME",k,"/",frames,flush=True)
        proc.stdin.close()
        err=proc.stderr.read().decode("utf8","replace")
        rc=proc.wait()
        if rc!=0:raise RuntimeError(err[-4000:])
    except Exception:
        proc.kill();raise
    # Generate original low-volume background + attack sfx.
    events=[(args.duration*x,kind) for x,kind in [(0.10,"zap"),(.21,"hit"),(.31,"move"),(.42,"hit"),(.52,"hit"),(.65,"move"),(.77,"hit"),(.89,"victory")]]
    snd=ROOT/"battle-sounds-original.wav"
    sfx(snd,args.duration+1,events)
    if args.voice:
        cmd=["ffmpeg","-nostdin","-y","-loglevel","error","-i",str(video_tmp),"-i",args.voice,"-i",str(snd),
        "-filter_complex","[1:a]loudnorm=I=-17:TP=-2:LRA=9[voz];[2:a]volume=0.45[sfx];[voz][sfx]amix=inputs=2:duration=first:weights=1 0.65:normalize=0,alimiter=limit=0.96[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-t",str(args.duration),"-movflags","+faststart",str(dst)]
    else:
        cmd=["ffmpeg","-nostdin","-y","-loglevel","error","-i",str(video_tmp),"-i",str(snd),
        "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","128k","-t",str(args.duration),"-movflags","+faststart",str(dst)]
    subprocess.run(cmd,check=True)
    print("VIDEO",dst,dst.stat().st_size,flush=True)
if __name__=="__main__":main()
