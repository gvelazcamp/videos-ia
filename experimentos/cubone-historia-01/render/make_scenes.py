from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
from pathlib import Path
import numpy as np, math, random, os
P=Path(__file__).resolve().parent.parent; W,H=720,1280; random.seed(104)
OUT=P/"escenas";OUT.mkdir(exist_ok=True)
FONT="/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
TEXT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(s,bold=True):return ImageFont.truetype(FONT if bold else TEXT,s)
def blend(c1,c2,t):return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))
def background(phase=0):
    pal=[
      [(44,39,89),(214,120,146),(250,180,132)],
      [(25,37,83),(96,80,132),(176,121,142)],
      [(12,29,64),(46,58,108),(96,83,124)],
      [(11,26,60),(25,47,85),(59,71,99)],
      [(17,31,67),(33,61,92),(74,88,108)],
      [(20,29,61),(57,52,105),(113,82,126)],
      [(31,40,81),(97,77,125),(184,119,144)],
      [(44,48,88),(151,106,137),(225,156,146)],
      [(52,57,99),(139,104,138),(212,152,144)],
      [(74,88,122),(214,151,141),(248,195,133)],
      [(86,96,140),(223,160,166),(245,190,146)]
    ][phase]
    arr=np.zeros((H,W,3),dtype=np.uint8)
    stops=[0,.55,1.]
    for y in range(H):
      t=y/(H-1)
      k=0 if t<.55 else 1
      a=(t-stops[k])/(stops[k+1]-stops[k])
      arr[y,:,:]=blend(pal[k],pal[k+1],a)
    bg=Image.fromarray(arr,"RGB").convert("RGBA")
    if phase in [0,1,9,10]:
      # Fuente de internet CC0: el cielo pintado original como textura suave.
      sky=Image.open(P/"assets/atardecer.png").convert("RGB")
      sky=sky.resize((W,600)).convert("RGBA")
      sky.putalpha(85 if phase in [0,9,10] else 42)
      bg.alpha_composite(sky,(0,0))
    return bg
def glow(base,x,y,r,color=(255,221,169),strength=90):
    light=Image.new("RGBA",(W,H));d=ImageDraw.Draw(light)
    d.ellipse((x-r,y-r,x+r,y+r),fill=color+(strength,))
    light=light.filter(ImageFilter.GaussianBlur(r*.6))
    base.alpha_composite(light)
def ellipse(base,bbox,fill,outline=None,width=1):
    ImageDraw.Draw(base).ellipse(tuple(int(k) for k in bbox),fill=fill,outline=outline,width=width)
def mountains(base,phase):
    d=ImageDraw.Draw(base)
    if phase in [0,9,10]:colors=["#8c6f93","#665b85","#413f69"]
    else:colors=["#4e6586","#374c70","#273957"]
    for k in range(3):
       seed=14+k*29+phase;rand=random.Random(seed)
       points=[(0,H)]
       basey=780+85*k
       for x in range(-60,W+100,66):
         points.append((x,basey-rand.randint(30,185)))
       points.extend([(W,H)])
       d.polygon(points,fill=colors[k])
def forest(base,phase,opacity=125):
    path=P/"assets"/("bosque-02.png" if phase in [0,7,9,10] else "bosque-01.png")
    forest=Image.open(path).convert("RGBA")
    forest=forest.resize((W,420),Image.Resampling.LANCZOS)
    alpha=forest.getchannel("A").point(lambda a:int(a*(opacity/255)))
    forest.putalpha(alpha)
    base.alpha_composite(forest,(0,700))
def ground(base,phase):
    d=ImageDraw.Draw(base)
    c=("#433f61" if phase not in [0,9,10] else "#70576d")
    d.polygon([(0,1080),(85,1060),(180,1074),(270,1055),(380,1067),(525,1048),(720,1058),(720,1280),(0,1280)],fill=c)
    d.ellipse((-180,1064,900,1390),fill=("#343750" if phase not in [0,9,10] else "#4c4359"))
    for i in range(45):
      x=(i*43+phase*11)%W; y=1070+(i*37)%220
      d.line((x,y,x+2,y-13),fill=("#8a7e85" if phase not in [0,9,10] else "#ba998c"),width=2)
      if i%6==0:
         d.ellipse((x-3,y-12,x+4,y-6),fill="#edb0ba")
def sky_object(base,phase):
   if phase in [2,3,4,5,8]:
      glow(base,525,310,150,(185,213,249),85)
      ellipse(base,(466,243,596,373),(241,237,217,255))
      d=ImageDraw.Draw(base)
      d.ellipse((480,270,501,293),fill="#d5d6d0")
      d.ellipse((532,333,550,351),fill="#d2d2ca")
   else:
      glow(base,508,447,177,(255,200,151),115)
      ellipse(base,(448,397,571,520),(255,219,167,240))
def stars(base,phase):
   if phase in [0,9,10]:return
   d=ImageDraw.Draw(base)
   rand=random.Random(42+phase)
   for i in range(60):
       x=rand.randint(13,695);y=rand.randint(15,610)
       r=1 if i%5 else 2
       d.ellipse((x-r,y-r,x+r,y+r),fill=(243,233,210,rand.randint(85,230)))
def draw_sprite(base,asset,x,y,h,flip=False,opacity=255,blur=0,rotate=0):
   img=Image.open(P/"assets"/asset).convert("RGBA")
   if flip:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   bbox=img.getbbox()
   if bbox:img=img.crop(bbox)
   ratio=img.width/img.height
   img=img.resize((int(h*ratio),int(h)),Image.Resampling.LANCZOS)
   if opacity<255:
      a=img.getchannel("A").point(lambda k:int(k*opacity/255));img.putalpha(a)
   if blur>0:img=img.filter(ImageFilter.GaussianBlur(blur))
   if rotate:img=img.rotate(rotate,resample=Image.Resampling.BICUBIC,expand=True)
   X=int(x-img.width/2);Y=int(y-img.height)
   layer=Image.new("RGBA",(W,H));layer.paste(img,(X,Y),img)
   sh=Image.new("RGBA",(W,H));shadow=img.getchannel("A").filter(ImageFilter.GaussianBlur(22)).point(lambda k:int(k*.34))
   sh.paste((14,11,30,255),(X+13,Y+15,X+13+img.width,Y+15+img.height),shadow)
   base.alpha_composite(sh);base.alpha_composite(layer)
def title(base,top,bottom,highlight=None):
   d=ImageDraw.Draw(base)
   # Tirita superior y chapita de episodio, neutras y con espacio para interfaz de Instagram.
   d.rounded_rectangle((33,72,366,119),radius=18,fill=(27,28,59,190),outline=(248,208,191,110),width=2)
   d.text((50,85),"HISTORIAS POKÉMON   •   01",font=font(18),fill=(255,236,217))
   lines=top.split("\n")
   center=250
   for line in lines:
     size=46 if len(line)>20 else 55
     f=font(size)
     bound=d.textbbox((0,0),line,font=f)
     wx=bound[2]-bound[0]
     yy=center-(len(lines)-1)*30+lines.index(line)*62
     x=int((W-wx)/2)
     d.rounded_rectangle((max(18,x-13),yy-7,min(W-18,x+wx+13),yy+size+6),radius=9,fill=(23,28,54,195))
     d.text((x,yy-2),line,font=f,fill=(255,237,207),stroke_width=1,stroke_fill=(55,39,69))
   d.rounded_rectangle((45,1150,675,1199),radius=14,fill=(28,27,50,155))
   f=font(20,False);bound=d.textbbox((0,0),bottom,font=f)
   d.text(((W-(bound[2]-bound[0]))/2,1162),bottom,font=f,fill=(236,225,218))
   d.rectangle((47,1221,673,1226),fill=(239,218,199,65))
def add_tears(base,px,py):
    d=ImageDraw.Draw(base)
    d.ellipse((px-12,py-20,px+5,py+13),fill="#75bbd5")
    d.ellipse((px-10,py-16,px-5,py-3),fill="#dceffe")
    d.ellipse((px+11,py+33,px+22,py+56),fill="#8ed3ed")
def fireflies(base,n=18,color="#ffe9a5",central=False,seed=0):
   d=ImageDraw.Draw(base);rand=random.Random(seed)
   for i in range(n):
      x=rand.randrange(60,W-70) if not central else rand.randrange(360,600)
      y=rand.randrange(430,1060)
      r=rand.randrange(2,6)
      d.ellipse((x-r,y-r,x+r,y+r),fill=color)
      d.ellipse((x-r*3,y-r*3,x+r*3,y+r*3),outline=(253,224,171,95),width=2)
SCENES=[
 ("¿SABÍAS QUE\nCUBONE LLORA?", "HAY HISTORIAS QUE NO SE OLVIDAN",0),
 ("UN CRÁNEO,\nUN RECUERDO", "NO ES UN DISFRAZ",1),
 ("CUANDO SALE\nLA LUNA...", "LOS RECUERDOS REGRESAN",2),
 ("CAMINA\nSOLITO", "UNA NOCHE MÁS EN EL BOSQUE",3),
 ("Y SU LLANTO\nRESUENA...", "COMO UN ECO ENTRE LOS ÁRBOLES",4),
 ("PERO ESA NOCHE\nTODO CAMBIA", "UNA PEQUEÑA LUZ EN LA OSCURIDAD",5),
 ("¿QUIÉN ESTÁ\nAHÍ?", "ALGUIEN LO ESPERA EN EL CLARO",6),
 ("NO LE PIDE\nQUE NO LLORE", "SIMPLEMENTE SE QUEDA A SU LADO",7),
 ("SER VALIENTE\nNO ES OLVIDAR", "ES SEGUIR CAMINANDO",8),
 ("TODAVÍA HAY\nCOMPAÑÍA", "DESPUÉS DE LA NOCHE, AMANECE",9),
 ("¿CONOCÍAS\nSU HISTORIA?", "CUBONE  •  POKÉMON #104",10)]
for i,(head,foot,phase) in enumerate(SCENES):
    bg=background(phase)
    sky_object(bg,phase);stars(bg,phase);mountains(bg,phase)
    forest(bg,phase,opacity=145 if i<8 else 96)
    ground(bg,phase)
    if i==0:
      draw_sprite(bg,'cubone.png',356,1065,455,flip=True)
    elif i==1:
      draw_sprite(bg,'marowak.png',525,896,375,opacity=78,blur=13)
      draw_sprite(bg,'cubone.png',311,1090,510,flip=True)
    elif i==2:
      draw_sprite(bg,'cubone.png',260,1100,390)
    elif i==3:
      draw_sprite(bg,'cubone.png',355,1050,405)
    elif i==4:
      draw_sprite(bg,'cubone.png',290,1195,750)
      add_tears(bg,469,714)
    elif i==5:
      fireflies(bg,20,central=True,seed=10)
      glow(bg,503,690,95,(254,239,159),220)
      draw_sprite(bg,'cubone.png',267,1070,360,flip=True)
    elif i==6:
      fireflies(bg,35,central=True,seed=24)
      draw_sprite(bg,'cubone.png',262,1080,385)
      draw_sprite(bg,'eevee.png',541,1095,260,flip=True)
    elif i==7:
      draw_sprite(bg,'cubone.png',285,1088,390)
      draw_sprite(bg,'eevee.png',517,1092,296,flip=True)
      fireflies(bg,16,seed=17)
    elif i==8:
      draw_sprite(bg,'cubone.png',260,1090,405)
      draw_sprite(bg,'eevee.png',509,1080,275)
      fireflies(bg,9,seed=23)
    elif i==9:
      draw_sprite(bg,'cubone.png',279,1084,401,flip=True)
      draw_sprite(bg,'eevee.png',494,1084,296,flip=True)
    else:
      draw_sprite(bg,'cubone.png',275,1077,433)
      draw_sprite(bg,'eevee.png',498,1095,300)
    title(bg,head,foot)
    bg.convert("RGB").save(OUT/f"escena-{i+1:02d}.jpg",quality=91,optimize=True)
    print(i+1,head.replace('\n',' '),flush=True)
# Contact sheet para revisión visual
thumb=Image.new("RGB",(220*6,392*2),(18,16,35))
for i in range(len(SCENES)):
 im=Image.open(OUT/f"escena-{i+1:02d}.jpg")
 im.thumbnail((220,392))
 thumb.paste(im,((i%6)*220,(i//6)*392))
thumb.save(P/"contacto.jpg",quality=55,optimize=True)
print("CONTACT",os.stat(P/"contacto.jpg").st_size,flush=True)

