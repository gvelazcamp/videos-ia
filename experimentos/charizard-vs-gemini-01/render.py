#!/usr/bin/env python3
"""CHARIZARD VS GÉMINI — original fan battle video, noninteractive / GitHub.
Layers: previously generated fantasy castle, Charizard official art via PokeAPI,
original four-point-star Gemini cyber-knight SVG, game HUD and original VFX.
Renders new MP4; never edits preceding Pokémon battle files.
"""
from __future__ import annotations
import argparse,math,random,subprocess,sys,wave
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance,ImageOps

ROOT=Path(__file__).resolve().parent
AS=ROOT/"assets";AS.mkdir(exist_ok=True)
W,H,FPS=540,960,24
DURATION=70.704
BG_SRC=ROOT.parent/"pikachu-castillo-terror"/"escenario-castillo.webp"
VOICE=ROOT/"voz-gemini-charon.mp3"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
for q in ["/usr/share/fonts/truetype/higgsfield/Metropolis-ExtraBold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
    if Path(q).exists():FONT=q;break
FONTS={}
def f(n):
    n=int(n)
    if n not in FONTS:FONTS[n]=ImageFont.truetype(FONT,n)
    return FONTS[n]
def txt(d,x,y,s,n=17,col="#fff5e4",stroke=0):
    d.text((int(x),int(y)),str(s),font=f(n),fill=col,stroke_width=stroke,stroke_fill="#142039")
def center(d,y,s,n=19,col="#fff5df"):
    b=d.textbbox((0,0),s,font=f(n))
    txt(d,(W-(b[2]-b[0]))/2,y,s,n,col)
def rect(d,box,fill,outline=None,width=2,r=8):
    d.rounded_rectangle(tuple(map(int,box)),radius=r,fill=fill,outline=outline,width=width)
def clamp(x):return max(0,min(1,x))
def p(t,a,b):return clamp((t-a)/max(b-a,1e-5))
def ease(v):v=clamp(v);return v*v*(3-2*v)
def mix(a,b,t):return a+(b-a)*ease(t)
def sinf(t,freq=1):return math.sin(t*freq)
def source_assets():
    char=AS/"charizard-oficial.png"
    if not char.exists() or char.stat().st_size<1000:
        req=Request("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",headers={"User-Agent":"Mozilla/5.0"})
        with urlopen(req,timeout=40) as r:char.write_bytes(r.read(5000000))
    robot=AS/"gemini-guardian.png"
    if not robot.exists():
        svg=ROOT/"gemini-guardian.svg"
        if not svg.exists():raise RuntimeError("Falta asset gemini-guardian.svg")
        subprocess.run(["rsvg-convert","-w","900","-h","1050","-o",str(robot),str(svg)],check=True)
    bg=BG_SRC if BG_SRC.exists() else AS/"castillo.webp"
    if not bg.exists():
        req=Request("https://raw.githubusercontent.com/gvelazcamp/videos-ia/main/experimentos/pikachu-castillo-terror/escenario-castillo.webp")
        with urlopen(req,timeout=30) as resp:bg.write_bytes(resp.read())
    return bg,char,robot
def skyback(path):
    # Detailed castle backdrop from our own earlier illustration, color graded
    # into vivid violet/orange game-arena aesthetic.
    im=Image.open(path).convert("RGB")
    w,h=im.size
    # Choose panoramic center, excluding owl, cauldron and unwanted peripheral objects.
    cut=im.crop((int(w*.30),0,int(w*.78),h))
    b=ImageOps.fit(cut,(W,H),method=Image.Resampling.LANCZOS,centering=(.53,.44))
    # Cartoon-color rendition and evening purple/orange staging.
    b=ImageEnhance.Color(b).enhance(1.33)
    b=ImageEnhance.Contrast(b).enhance(1.17)
    b=b.convert("RGBA")
    veil=Image.new("RGBA",(W,H),(0,0,0,0))
    v=ImageDraw.Draw(veil)
    for yy in range(H):
        if yy<570:
            a=56 if yy<180 else int(45+46*(yy-180)/390)
            col=(94,36,138,a)
        else:
            a=int(68+44*(yy-570)/(H-570))
            col=(113,54,116,a)
        v.line((0,yy,W,yy),fill=col)
    b.alpha_composite(veil)
    # Huge rosy moon, a visual signature of the user's approved Pokémon battle look.
    moon_layer=Image.new("RGBA",(W,H),(0,0,0,0))
    md=ImageDraw.Draw(moon_layer)
    for radius,alpha in [(157,12),(134,22),(117,38)]:
        md.ellipse((265-radius,240-radius,265+radius,240+radius),
                   fill=(255,156,186,alpha))
    b.alpha_composite(moon_layer.filter(ImageFilter.GaussianBlur(26)))
    m=Image.new("RGBA",(W,H),(0,0,0,0))
    md=ImageDraw.Draw(m)
    md.ellipse((172,147,358,333),fill=(255,202,184,255),outline=(255,233,204,255),width=5)
    b.alpha_composite(m)
    crater=Image.new("RGBA",(W,H),(0,0,0,0))
    cr=ImageDraw.Draw(crater)
    moon_noise=random.Random(410)
    for q in range(23):
        xx=265+moon_noise.randint(-71,71)
        yy=240+moon_noise.randint(-70,70)
        if (xx-265)**2+(yy-240)**2>69**2:continue
        rr=moon_noise.randint(4,13)
        cr.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),
                   fill=(199,121,159,moon_noise.randint(33,83)))
    b.alpha_composite(crater)
    # Clouds must be alpha-composited, not painted as translucent replacement pixels.
    cloud_layer=Image.new("RGBA",(W,H),(0,0,0,0))
    cd=ImageDraw.Draw(cloud_layer)
    rng=random.Random(122)
    for k in range(26):
        x=rng.randint(-90,560);y=rng.randint(95,380)
        if k%3==0:
            cd.ellipse((x-30,y-4,x+38,y+13),fill=(212,117,169,69))
            cd.ellipse((x-7,y-16,x+30,y+10),fill=(240,130,174,58))
    b.alpha_composite(cloud_layer)
    # Digital portal, behind the duel.
    fx=Image.new("RGBA",(W,H),(0,0,0,0));g=ImageDraw.Draw(fx)
    for i in range(6):
        r=72+i*17
        g.ellipse((268-r,439-r*1.15,268+r,439+r*1.15),outline=(109,209,252,max(0,95-i*13)),width=5)
    for k in range(32):
        a=k/32*math.tau
        r=88+rng.random()*54
        xx=270+r*math.cos(a);yy=450+r*math.sin(a)
        g.polygon([(xx,yy-7),(xx+5,yy),(xx,yy+7),(xx-5,yy)],fill=(184,173,255,rng.randrange(45,165)))
    fx=fx.filter(ImageFilter.GaussianBlur(5))
    b.alpha_composite(fx)
    # Stylized cobbled arena ring foreground y 628–788.
    d=ImageDraw.Draw(b)
    d.ellipse((-90,627,636,827),fill=(57,42,77,225),outline="#b78aa4",width=13)
    d.ellipse((-2,645,544,801),fill=(136,91,115,200),outline="#dfb2ad",width=8)
    d.ellipse((89,660,458,782),fill=(85,69,104,230),outline="#f1cfb9",width=6)
    d.ellipse((178,683,357,760),fill="#e5b8a4",outline="#653f78",width=12)
    d.line((125,719,410,719),fill="#f3c4ad",width=12)
    d.ellipse((251,700,286,737),fill="#ffe3b4",outline="#965575",width=7)
    # Perspective pavement bricks with tiny highlights
    for i in range(11):
        yy=728+i*i*1.7
        if yy>=960:break
        d.line((-20,yy,W+20,yy),fill=(54,40,74,155),width=2+i//4)
        for j in range(10):
            x=int((j+.5*(i%2))*70-15+(i-4)*2)
            d.line((x,yy,x+int((i+3)*1.5),min(960,yy+i+15)),fill=(44,31,73,110),width=2)
    for k in range(68):
        x=rng.randint(0,540);y=rng.randint(635,910)
        l=rng.randint(3,12)
        d.line((x,y,x+l,y-rng.randint(0,7)),fill=(250,189,172,rng.randint(50,130)),width=2)
    # Crimson banners / torches to connect with the selected Pokémon reference
    for x in (32,493):
        # Banners on castle side walls
        d.polygon([(x-29,224),(x+28,224),(x+26,386),(x,402),(x-26,386)],fill="#852a56",outline="#deb06c")
        d.line((x-33,222,x+33,222),fill="#ebb777",width=6)
        d.ellipse((x-21,282,x+21,326),fill="#f3d4c6",outline="#612b56",width=4)
        d.line((x-21,304,x+21,304),fill="#743550",width=6)
        d.ellipse((x-7,297,x+7,311),fill="#7e476d")
        # Torches
        flame_x=110 if x<100 else 430
        d.rectangle((flame_x-11,515,flame_x+11,529),fill="#5a4054")
        d.polygon([(flame_x-18,517),(flame_x,497),(flame_x+18,517)],fill="#ffa95b")
        d.polygon([(flame_x-8,511),(flame_x-12,492),(flame_x+1,476),(flame_x+12,501),(flame_x+7,515)],fill="#ffcf78")
    return b.convert("RGB")
def sprite(path,height):
    im=Image.open(path).convert("RGBA")
    box=im.getbbox()
    if box:im=im.crop(box)
    im=im.resize((round(height*im.width/im.height),height),Image.Resampling.LANCZOS)
    return im
def character(base,spr,cx,bottom,rot=0,scale=1,glow=None,opacity=255,shadow=True):
    im=spr
    if scale!=1:im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.BICUBIC)
    if rot:im=im.rotate(rot,expand=True,resample=Image.Resampling.BICUBIC)
    if opacity<255:
        im=im.copy()
        im.putalpha(im.getchannel("A").point(lambda a:int(a*opacity/255)))
    x=round(cx-im.width/2);y=round(bottom-im.height)
    if shadow:
        s=Image.new("RGBA",(W,H));d=ImageDraw.Draw(s)
        d.ellipse((cx-im.width*.31,bottom-10,cx+im.width*.31,bottom+17),fill=(13,11,34,160))
        base.alpha_composite(s.filter(ImageFilter.GaussianBlur(11)))
    if glow is not None:
        layer=Image.new("RGBA",base.size)
        mask=im.getchannel("A").filter(ImageFilter.MaxFilter(21))
        rgb=Image.new("RGBA",im.size,glow)
        rgb.putalpha(mask.point(lambda a:int(a*.55)))
        layer.paste(rgb,(x,y),rgb)
        base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))
    base.alpha_composite(im,(x,y))
def electric_line(d,start,end,seed,color="#9ef9ff",secondary="#fff2ff",width=9):
    rng=random.Random(seed)
    sx,sy=start;ex,ey=end
    points=[(sx,sy)]
    for k in range(1,9):
        u=k/9
        points.append((sx+(ex-sx)*u+rng.randint(-17,17),sy+(ey-sy)*u+rng.randint(-14,14)))
    points.append((ex,ey))
    d.line(points,fill="#4137a1",width=width+8,joint="curve")
    d.line(points,fill=color,width=width,joint="curve")
    d.line(points,fill=secondary,width=max(2,width//3),joint="curve")
def particles(d,x,y,tick,strength=1,color="#ffd7af",count=22,stretch=1):
    rng=random.Random(tick+71)
    for j in range(count):
        a=rng.random()*math.tau;r=(20+rng.random()*110)*strength
        xx=x+math.cos(a)*r*stretch;yy=y+math.sin(a)*r
        s=1+rng.random()*4
        d.ellipse((xx-s,yy-s,xx+s,yy+s),fill=color)
        if j%4==0:d.line((x,y,xx,yy),fill=color,width=2)
def fireball(d,x,y,power,seed):
    rng=random.Random(seed)
    for k in range(18):
        theta=k*2*math.pi/18
        r=(18+rng.randint(10,65))*power
        xx=x+math.cos(theta)*r;yy=y+math.sin(theta)*r
        sz=9+rng.randint(0,16)
        col=["#fff8be","#ffe680","#ff934c","#e64d5f"][k%4]
        d.ellipse((xx-sz,yy-sz,xx+sz,yy+sz),fill=col)
    d.ellipse((x-27,y-27,x+27,y+27),fill="#fffcc1",outline="#ff9a37",width=8)
def flare(d,x,y,r,tick):
    for k in range(12):
        ang=(k*math.tau/12)+tick*.06
        dx=math.cos(ang);dy=math.sin(ang)
        d.polygon([(x+dx*r*.15,y+dy*r*.15),(x+dx*r*1.22,y+dy*r*1.22),
                   (x+math.cos(ang+.2)*r*.42,y+math.sin(ang+.2)*r*.42)],
                   fill=["#ff8b55","#fff9ae","#f7bc70"][k%3])
    d.ellipse((x-r*.57,y-r*.57,x+r*.57,y+r*.57),fill="#fff4bc")
def shield(d,x,y,t,damage=False):
    r=85+6*math.sin(t*5)
    for i in range(2):
        rr=r+i*13
        d.polygon([(x+rr*math.cos(k*math.tau/6),y+rr*math.sin(k*math.tau/6)) for k in range(6)],
                  fill=(35,189,236,44) if i==0 else None,
                  outline="#a2faff" if i==0 else "#7778ed",width=5 if i==0 else 3)
    for k in range(12):
        a=k*math.tau/12+t*.7
        xx=x+(r+9)*math.cos(a);yy=y+(r+9)*math.sin(a)
        d.ellipse((xx-3,yy-3,xx+3,yy+3),fill="#e9ffff")
    if damage:
        d.line([(x-22,y-77),(x+3,y-32),(x-15,y),(x+35,y+66)],fill="#fff8e3",width=7)
def icon(d,x,y,name,color):
    if name in ("LANZALLAMAS","ENVITE ÍGNEO","LLAMARADA"):
        d.polygon([(x-10,y+13),(x-13,y-1),(x,y-16),(x+7,y-4),(x+13,y-12),(x+14,y+9),(x+3,y+16)],fill=color,outline="#95405b")
        d.polygon([(x-1,y+13),(x-5,y+2),(x+4,y-6),(x+8,y+11)],fill="#fff4a3")
    elif name in ("GARRA DRAGÓN",):
        for i in range(3):
            d.line((x-11+i*7,y-9,x-5+i*7,y+12),fill=color,width=4)
    elif name in ("ESCUDO DE DATOS",):
        d.polygon([(x,y-14),(x+13,y-8),(x+9,y+8),(x,y+15),(x-9,y+8),(x-13,y-8)],fill=color,outline="#2e5499")
    elif name in ("RAYO CUÁNTICO",):
        d.line((x-11,y+10,x+12,y-10),fill=color,width=7)
        d.line((x-4,y-12,x+4,y+13),fill="#ffffff",width=4)
    elif name=="PREDICCIÓN":
        d.ellipse((x-13,y-13,x+13,y+13),outline=color,width=3)
        d.line((x,y,x+8,y-7),fill=color,width=3)
    else:
        d.arc((x-14,y-14,x+14,y+14),25,300,fill=color,width=4)
        d.polygon([(x-14,y+1),(x-6,y+1),(x-7,y+11)],fill=color)
def bar(d,x,y,w,value,maxvalue,active,color):
    rect(d,(x,y,x+w,y+14),"#111730","#c6b8cb",2,5)
    frac=clamp(value/maxvalue);fill=int((w-6)*frac)
    if fill>1:rect(d,(x+3,y+3,x+3+fill,y+11),color,None,1,3)
    d.line((x+5,y+4,x+4+fill,y+4),fill="#dcfff4" if frac>.4 else "#fff6c2",width=2)
def hud(image,t,mon,move,charhp,gemhp,turn,mode):
    d=ImageDraw.Draw(image)
    # symmetrical game HUD; exactly the same size for both fighters.
    for side,(x,name,sub,hp,total,col) in enumerate([
        (12,"CHARIZARD","FUEGO / VOLADOR",charhp,160,"#ff995f"),
        (283,"GÉMINI · IA","TIPO DIGITAL",gemhp,100,"#a7d4ff")
    ]):
        active=mon==("CHARIZARD" if side==0 else "GÉMINI")
        outline=("#fff0aa" if active else "#bb92ba")
        rect(d,(x,39,x+245,117),"#231e42",outline,2,13)
        d.polygon([(x+1,56),(x+12,40),(x+36,40),(x+23,60)],fill=col)
        txt(d,x+11,46,name,19 if side==0 else 18,"#fff6e7")
        txt(d,x+13,71,sub,10,col)
        txt(d,x+12,89,"PS" if side==0 else "SYS",11,"#f6d9dd")
        bar(d,x+47,91,145,hp,total,active,"#60eaaa" if hp/total>.5 else "#ffd26a" if hp/total>.25 else "#ff7488")
        txt(d,x+195,90,f"{int(hp)}/{total}",10,"#fff4e9")
        if active:
            d.rounded_rectangle((x-2,37,x+247,119),radius=14,outline=col,width=2)
    rect(d,(205,128,334,164),"#211b3a","#f4d6ac",2,9)
    center(d,132,f"TURNO {turn}",18)
    txt(d,242,174,"VS",28,"#ffd18f",stroke=2)
    # Speech caption above menu
    if mode:
        rect(d,(38,680,502,744),"#252443","#edc9bd",2,12)
        n=18 if len(mode)<30 else 15
        center(d,688,mode,n,"#fff3e6")
        if move:
            center(d,717,"¡MOVIMIENTO ACTIVADO!",11,"#ffd98d" if mon=="CHARIZARD" else "#a9edff")
def menu(image,t,actor,move,ending=False):
    d=ImageDraw.Draw(image)
    mons={
      "CHARIZARD":(["LANZALLAMAS","GARRA DRAGÓN","ENVITE ÍGNEO","LLAMARADA"],
                   "#ef904b","#d45752","#fff2bb","#efc9a8","#46304e"),
      "GÉMINI":(["ESCUDO DE DATOS","RAYO CUÁNTICO","PREDICCIÓN","REINICIAR"],
                "#8ce9fa","#7465d9","#e5fbff","#c3d5fd","#242955")}
    moves,primary,secondary,light,soft,dark=mons[actor]
    # shadow and trapezoid corners match selected elaborate Pokémon HUD style
    d.polygon([(0,761),(30,744),(120,744),(133,757),(403,757),(417,744),(512,744),(540,761),
               (540,956),(0,956)],fill=secondary,outline="#faf0dd")
    d.polygon([(7,767),(32,752),(116,752),(131,765),(408,765),(422,752),(511,752),(532,767),
               (532,948),(7,948)],fill=dark,outline=primary)
    d.polygon([(147,761),(159,745),(382,745),(394,761),(380,788),(160,788)],fill=dark,outline=primary)
    center(d,750,"¡VICTORIA!" if ending else f"ATACA · {actor}",19,light)
    for k,name in enumerate(moves):
        x=21+(k%2)*260;y=802+(k//2)*73
        selected=(move==name) and not ending
        bg=light if selected else soft
        rim="#fffdd6" if selected else "#b8b1c1"
        rect(d,(x+3,y+7,x+249,y+70),"#151528",None,1,10)
        rect(d,(x,y,x+246,y+64),bg,rim,2,10)
        rect(d,(x+5,y+4,x+241,y+59),bg,None,1,7)
        d.line((x+9,y+7,x+238,y+7),fill="#ffffff",width=2)
        icon(d,x+29,y+29,name,primary if actor=="GÉMINI" else "#c64f48")
        n=17 if len(name)<=13 else 13
        txt(d,x+53,y+9,name,n,"#25213a")
        txt(d,x+54,y+38,"PP 15/15" if k<2 else "PP 10/10",11,"#54485f")
        if selected:
            pulse=(1+math.sin(t*9.4))/2
            border=4+int(pulse*2)
            d.rounded_rectangle((x-2,y-2,x+248,y+66),radius=12,outline=primary,width=border)
            marker="#ff5959" if actor=="CHARIZARD" else "#75ffff"
            for xx,direction in [(x+9,1),(x+237,-1)]:
                for yy,dy in [(y+9,1),(y+55,-1)]:
                    d.line([(xx,yy+9*dy),(xx,yy),(xx+9*direction,yy)],fill=marker,width=4)
def event(t):
    # Timing verified from Gemini voice (faster-whisper).
    # (start,end,actor,move,caption,turn)
    phases=[
        (0,10.0,"CHARIZARD",None,"¡CHARIZARD VS. GÉMINI IA!",0),
        (10,15.3,"CHARIZARD","LANZALLAMAS","¡CHARIZARD USA LANZALLAMAS!",1),
        (15.3,20.3,"GÉMINI","ESCUDO DE DATOS","¡ESCUDO DE DATOS! BLOQUEADO",1),
        (20.3,26.4,"GÉMINI","RAYO CUÁNTICO","¡GÉMINI USA RAYO CUÁNTICO!",2),
        (26.4,31.2,"CHARIZARD","GARRA DRAGÓN","¡CHARIZARD USA GARRA DRAGÓN!",2),
        (31.2,37.7,"GÉMINI","PREDICCIÓN","VICTORIA CALCULADA: 99 %",3),
        (37.7,44.7,"CHARIZARD","ENVITE ÍGNEO","¡ERROR DE PREDICCIÓN!",3),
        (44.7,51.8,"GÉMINI","REINICIAR","¡REINICIAR SIMULACIÓN!",4),
        (51.8,60.0,"CHARIZARD","LLAMARADA","¡CHARIZARD USA LLAMARADA!",4),
        (60.0,70.71,"CHARIZARD",None,"¡VICTORIA DE CHARIZARD!",4)]
    for i,(a,b,actor,move,caption,turn) in enumerate(phases):
        if a<=t<b:return a,b,actor,move,caption,turn
    return phases[-1]
def frame(t,stage,charizard,gemini,idx):
    a,b,actor,move,caption,turn=event(t)
    u=p(t,a,b)
    img=stage.copy().convert("RGBA")
    d=ImageDraw.Draw(img)
    rng=random.Random(idx//2+42)
    # Ambient ash, embers and data stars; faint, behind character.
    for j in range(24):
        x=(j*73+idx*(j%4+1)*.31)%W
        y=(j*147-idx*(j%5+1)*.22)%630+75
        s=1+(j%4==0)*2
        col="#eeb2bf" if j%3==0 else "#7be5fa" if j%3==1 else "#ffe6b0"
        d.ellipse((x-s,y-s,x+s,y+s),fill=col)
    # light stage silhouettes
    cx=155+5*sinf(t,2.7);cy=659+3*sinf(t,3.1)
    gx=392+4*sinf(t,2.2);gy=645+5*sinf(t,2.6)
    crot=sinf(t,1.8)*1.4;grot=sinf(t+1,2.1)*1.8
    cscale=1+.014*sinf(t,3.2);gscale=1+.023*sinf(t,2.8)
    if move=="LANZALLAMAS":cx+=38*math.sin(math.pi*u);crot-=7*math.sin(math.pi*u)
    if move=="RAYO CUÁNTICO":gx-=26*math.sin(math.pi*u)
    if move=="GARRA DRAGÓN":cx+=138*math.sin(math.pi*u);crot=-19*math.sin(math.pi*u)
    if move=="ENVITE ÍGNEO":cx+=170*math.sin(math.pi*u);cy-=39*math.sin(math.pi*u);crot-=18*math.sin(math.pi*u)
    if move=="REINICIAR":gx+=13*math.sin(2*math.pi*u);grot=-9*math.sin(math.pi*u)
    if move=="LLAMARADA":cx+=36*math.sin(math.pi*u);cscale+=.09*math.sin(math.pi*u)
    if t>=60:gx+=10*u;grot=-10
    # game art highlighted with rim-light, intact source sprites
    character(img,charizard,cx,cy,rot=crot,scale=cscale,glow=(255,116,50,130))
    character(img,gemini,gx,gy,rot=grot,scale=gscale,glow=(93,202,255,155),opacity=255 if t<65 else 180)
    d=ImageDraw.Draw(img)
    # attack effects: each is original code animation, no existing game sound/art copied
    if move=="LANZALLAMAS":
        theta=math.sin(math.pi*u)
        for k in range(12):
            px=mix(230,390,u*.6)+rng.randint(-21,21)
            yy=460+(k%5-2)*16+rng.randint(-25,25)
            d.polygon([(190+rng.randint(-10,20),500),(px,yy-27),(px+42,yy),(px,yy+23)],
                      fill=["#ffb454","#ffed7d","#e95b5e"][k%3])
        if u>.28:fireball(d,375,484,theta,idx)
    elif move=="ESCUDO DE DATOS":
        shield(d,385,505,t)
        for k in range(5):
            electric_line(d,(285,470+k*12),(325,510+k*7),idx+k,"#ffd887","#fff7c2",5)
    elif move=="RAYO CUÁNTICO":
        for k in range(5):
            electric_line(d,(372,501+rng.randint(-32,27)),(195,499+rng.randint(-43,33)),idx+k,"#86e8ff","#edfbff",6)
        burst=math.sin(math.pi*u)
        particles(d,195,505,idx,burst,"#b5ebff",35,1)
    elif move=="GARRA DRAGÓN":
        strength=math.sin(math.pi*u)
        for i in range(3):
            x=329+i*21
            d.arc((x-76,375+i*16,x+119,630+i*10),195,322,fill="#e8f6ff",width=8)
            d.arc((x-72,380+i*16,x+112,623+i*10),195,322,fill="#ffae73",width=3)
        particles(d,376,502,idx,strength,"#fbe9cc",37,1)
    elif move=="PREDICCIÓN":
        # 99% prediction floats, glitching into red warning later
        rect(d,(292,276,507,345),"#22244b","#8feefa",2,12)
        txt(d,307,284,"PROB. DE VICTORIA",12,"#b8f1fc")
        txt(d,330,302,"99 %",28,"#a8faff")
        for i in range(5):
            yy=360+i*30;xx=324+(idx*5+i*63)%170
            d.line((xx,yy,xx+31,yy),fill="#ad94ff",width=2)
    elif move=="ENVITE ÍGNEO":
        k=math.sin(math.pi*u)
        for i in range(18):
            theta=i*math.tau/18
            r=35+i%3*20
            px=cx+math.cos(theta)*r
            yy=cy-175+math.sin(theta)*r
            d.ellipse((px-15*k,yy-15*k,px+15*k,yy+15*k),
                      fill=["#ffa244","#ffe27c","#ff6d6f"][i%3])
        if u>.43:
            particles(d,365,493,idx,p(u,.43,.95),"#ffd4a9",48,1.3)
            shield(d,384,497,t,True)
        if u>.8:
            txt(d,294,368,"¡ERROR!",21,"#fff3ce")
    elif move=="REINICIAR":
        # Rewind time: cyan rings, digital stripes and clock reversion.
        for k in range(3):
            rr=70+35*k+18*sinf(t,3+k)
            d.arc((gx-rr,488-rr,gx+rr,488+rr),45,300,fill="#c7c6ff" if k%2 else "#8df5ff",width=5)
        for j in range(15):
            x=rng.randint(20,510);y=rng.randint(184,672)
            d.line((x,y,x+rng.randint(9,58),y),fill="#a5f9f4",width=3)
        rect(d,(125,304,413,366),"#28254e","#b2d8ff",2,11)
        center(d,316,"REINICIANDO...",21,"#e5efff")
    elif move=="LLAMARADA":
        strength=p(t,54.5,58.8)
        amp=math.sin(math.pi*clamp((t-54.5)/4.9))
        for k in range(27):
            angle=k*math.tau/27+(idx%20)*.02
            px=359+math.cos(angle)*rng.uniform(18,120)*max(.1,amp)
            py=485+math.sin(angle)*rng.uniform(17,155)*max(.1,amp)
            r=16+rng.random()*33
            d.ellipse((px-r,py-r,px+r,py+r),fill=["#fff4aa","#ffc879","#ff834b","#e75058"][k%4])
        if strength>.2:fireball(d,368,475,.7+strength,idx)
        if t>57.3:
            particles(d,385,481,idx,.6,"#fff4cf",44,1)
    # Closing cards
    if t>=60:
        if t<62.3:
            rect(d,(78,295,462,390),"#272042","#ffe1a7",3,18)
            center(d,306,"¡VICTORIA!",39,"#ffe3a6")
            center(d,358,"CHARIZARD",19,"#fff1e0")
        elif t<67.8:
            rect(d,(60,290,485,396),"#201f49","#8df3f4",3,15)
            center(d,300,"GÉMINI · REGISTRO",22,"#b0efff")
            center(d,344,"APRENDÍ DE ESTA DERROTA",15,"#f4f1ff")
        else:
            rect(d,(74,306,472,389),"#242044","#ffe7b6",3,15)
            center(d,321,"¿QUIÉN SERÁ EL",22,"#fff5e3")
            center(d,350,"PRÓXIMO RIVAL?",22,"#fff5e3")
    # HP remaining progression
    charhp=160
    gemhp=100
    if t>=20.3:charhp=mix(160,108,p(t,23.3,26.0))
    if t>=26.4:gemhp=mix(100,77,p(t,28.0,31.0))
    if t>=37.7:gemhp=mix(77,26,p(t,39.0,44.3))
    if t>=44.7:gemhp=mix(26,46,p(t,48.0,51.7))
    if t>=51.8:gemhp=mix(46,0,p(t,57.0,60.0))
    # late boost after AI counter, charizard still stands
    if t>=44.7:charhp=108
    hud(img,t,actor,move,charhp,gemhp,turn,caption)
    menu(img,t,actor,move,ending=t>=60)
    return img.convert("RGB")
def audio_original(path,duration):
    """Simple original fantasy synth score and attack cues (no copyrighted music)."""
    sr=22050
    t=np.arange(round(sr*(duration+.4)),dtype=np.float32)/sr
    out=np.zeros(len(t),dtype=np.float32)
    roots=[(0,146.83),(8,174.61),(15,130.81),(21,196),(27,155.56),(33,146.83),(40,174.61),(47,130.81),(54,196),(62,174.61)]
    for i,(start,note) in enumerate(roots):
        end=roots[i+1][0] if i+1<len(roots) else duration+.4
        env=np.clip((t-start)/2,0,1)*np.clip((end-t)/2,0,1)
        for ratio,mult in [(1,.070),(1.25,.023),(1.5,.029),(2,.018)]:
            out+=env*mult*np.sin(2*np.pi*note*ratio*t)
    rng=np.random.default_rng(31)
    for when,kind in [(10.9,"fire"),(15.8,"block"),(24.0,"laser"),(29.5,"hit"),(39.8,"hit"),(48.0,"rewind"),(57.8,"fire"),(60.0,"win")]:
        v=t-when;dt=np.maximum(0,v);on=(v>=0)&(v<1.2)
        if kind=="fire":z=rng.normal(0,1,len(t))*.55+np.sin(2*np.pi*(310*dt+580*dt*dt))
        elif kind=="laser":z=np.sin(2*np.pi*(720*dt+1000*dt*dt))
        elif kind=="rewind":z=np.sin(2*np.pi*(880*dt-320*dt*dt))
        elif kind=="hit":z=np.sin(2*np.pi*78*dt)+rng.normal(0,.20,len(t))
        elif kind=="win":z=np.sin(2*np.pi*660*dt)+np.sin(2*np.pi*880*dt)
        else:z=np.sin(2*np.pi*450*dt)
        out+=np.where(on,z*np.exp(-5*dt)*.17,0).astype(np.float32)
    out*=np.clip(t/1,0,1)*np.clip((duration-t)/3,0,1)
    out=np.int16(np.clip(out*.6,-.94,.94)*32767)
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(out.tobytes())
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--preview",action="store_true")
    parser.add_argument("--output",default=str(ROOT/"charizard-vs-gemini.mp4"))
    parser.add_argument("--voice",default=str(VOICE))
    args=parser.parse_args()
    bg,cp,gp=source_assets()
    stage=skyback(bg)
    charizard=sprite(cp,365)
    gemini=sprite(gp,338)
    print("IMAGES",charizard.size,gemini.size,stage.size,flush=True)
    if args.preview:
        for ts in [3,12,17,24,29,35,40,48,57,63,69]:
            frame(ts,stage,charizard,gemini,int(ts*FPS)).save(ROOT/f"preview-{int(ts):02d}.jpg",quality=83,optimize=True)
        print("PREVIEW DONE",flush=True)
        return
    dst=Path(args.output);dst.parent.mkdir(parents=True,exist_ok=True)
    tmp=dst.with_suffix(".video.mp4")
    cmd=["ffmpeg","-nostdin","-y","-hide_banner","-loglevel","error",
         "-f","rawvideo","-pix_fmt","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),
         "-i","pipe:0","-c:v","libx264","-preset","ultrafast","-crf","24",
         "-pix_fmt","yuv420p","-movflags","+faststart",str(tmp)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        n=math.ceil(DURATION*FPS)
        for k in range(n):
            image=frame(k/FPS,stage,charizard,gemini,k)
            proc.stdin.write(image.tobytes())
            if k%120==0:print(f"RENDER {k}/{n}",flush=True)
        proc.stdin.close()
        err=proc.stderr.read().decode("utf8","replace")
        if proc.wait()!=0:raise RuntimeError(err[-3000:])
    except Exception:
        proc.kill();raise
    bgw=ROOT/"musica-y-sfx-original.wav"
    audio_original(bgw,DURATION)
    voice=Path(args.voice)
    if not voice.exists() or voice.stat().st_size<100000:raise FileNotFoundError(voice)
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error",
        "-i",str(tmp),"-i",str(voice),"-i",str(bgw),
        "-filter_complex","[1:a]loudnorm=I=-17:TP=-2:LRA=9[voz];[2:a]volume=.36[mus];[voz][mus]amix=inputs=2:duration=first:weights=1 .55:normalize=0,alimiter=limit=.95[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","128k",
        "-t",str(DURATION),"-movflags","+faststart",str(dst)],check=True)
    print("VIDEO",dst,dst.stat().st_size,flush=True)
if __name__=="__main__":
    main()

