#!/usr/bin/env python3
"""Overlays originales para Cubone 02; no modifica imágenes ni video originales."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops
from pathlib import Path
import math, json
ROOT=Path(__file__).resolve().parents[2]/"cubone-historia-01"
OUT=Path(__file__).resolve().parent.parent/"objetos"
OUT.mkdir(exist_ok=True)
Q=2; W=540;H=960
FONT="/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not Path(FONT).exists():FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not Path(REG).exists():REG=FONT
def i(x):return int(round(x*Q))
def f(size,bold=True):return ImageFont.truetype(FONT if bold else REG,i(size))
def pos(box):return tuple(i(x) for x in box)
def dr_box(d,box,fill,rad=0,outline=None,width=1):
    d.rounded_rectangle(pos(box),radius=i(rad),fill=fill,outline=outline,width=i(width))
def ellipse(d,box,fill,outline=None,width=1):d.ellipse(pos(box),fill=fill,outline=outline,width=i(width))
def line(d,points,fill,width=1,joint="curve"):d.line([(i(x),i(y)) for x,y in points],fill=fill,width=i(width),joint=joint)
def txt(d,x,y,text,size=18,color="#faf4e7",bold=True,stroke_width=0,stroke_fill="#152333"):
    d.text((i(x),i(y)),text,font=f(size,bold),fill=color,stroke_width=i(stroke_width),stroke_fill=stroke_fill)
def new():return Image.new("RGBA",(W*Q,H*Q),(0,0,0,0))
def save(im,name):
    im.resize((W,H),Image.Resampling.LANCZOS).save(OUT/name,optimize=True)
    print(name,(OUT/name).stat().st_size,flush=True)
def shadow(im,box,alpha=105,blur=12):
    l=Image.new("RGBA",im.size);d=ImageDraw.Draw(l)
    x,y,w,h=box;dr_box(d,(x+4,y+7,x+w+4,y+h+7),(4,10,28,alpha),20)
    l=l.filter(ImageFilter.GaussianBlur(i(blur)))
    im.alpha_composite(l)
def corner(d,x,y,a=18,col="#91d9ec"):
    line(d,[(x,y+a),(x,y),(x+a,y)],col,2)
def ball(d,cx,cy,r=23):
    ellipse(d,(cx-r-2,cy-r-2,cx+r+2,cy+r+2), "#1b2137")
    ellipse(d,(cx-r,cy-r,cx+r,cy+r), "#f2efe4")
    d.pieslice(pos((cx-r,cy-r,cx+r,cy+r)),180,360,fill="#cfe0ec")
    d.pieslice(pos((cx-r,cy-r,cx+r,cy+r)),180,360,fill="#f1f2e9")
    d.pieslice(pos((cx-r,cy-r,cx+r,cy+r)),180,360,fill="#ede7d8")
    d.pieslice(pos((cx-r,cy-r,cx+r,cy+r)),180,360,fill="#efefee")
    # Main red upper hemisphere (draw last)
    d.pieslice(pos((cx-r,cy-r,cx+r,cy+r)),180,360,fill="#e84a57")
    # top half via explicit clipping polygon to avoid orientation confusion
    ellipse(d,(cx-r,cy-r,cx+r,cy+r),None,outline="#19253c",width=3)
    line(d,[(cx-r+1,cy),(cx+r-1,cy)],"#1b2236",4)
    ellipse(d,(cx-8,cy-8,cx+8,cy+8),"#121a2e")
    ellipse(d,(cx-5,cy-5,cx+5,cy+5),"#fcfaf1")
    ellipse(d,(cx-r+7,cy-r+6,cx-r+16,cy-r+10),"#f9a5ae")
def skull(d,cx,cy,s=1):
    # Cráneo estilizado aislado de Cubone: máscara de hueso blanco, cuernos y cavidades.
    def box(x1,y1,x2,y2):return pos((cx+x1*s,cy+y1*s,cx+x2*s,cy+y2*s))
    d.polygon([(i(cx-44*s),i(cy-35*s)),(i(cx-62*s),i(cy-79*s)),(i(cx-33*s),i(cy-62*s)),(i(cx-19*s),i(cy-42*s))],fill="#f6edda")
    d.polygon([(i(cx+25*s),i(cy-43*s)),(i(cx+56*s),i(cy-78*s)),(i(cx+62*s),i(cy-42*s)),(i(cx+42*s),i(cy-28*s))],fill="#f6edda")
    d.rounded_rectangle(box(-51,-47,52,45),radius=i(29*s),fill="#ede8d8",outline="#7a7f81",width=i(3*s))
    d.ellipse(box(-34,-12,-5,22),fill="#32354c")
    d.ellipse(box(7,-11,34,21),fill="#32354c")
    d.polygon([(i(cx-6*s),i(cy+22*s)),(i(cx+7*s),i(cy+22*s)),(i(cx+1*s),i(cy+33*s))],fill="#5d5660")
    d.arc(box(-42,-38,42,40),220,335,fill="#faf4e7",width=i(3*s))
    d.arc(box(-47,-45,47,42),23,135,fill="#bfc3bc",width=i(2*s))
def isolated_skull(canvas,cx,cy):
    """Recorta visualmente la máscara craneal del Cubone de referencia, sin su cuerpo."""
    path=ROOT/"cubone.png"
    if not path.exists():path=ROOT/"assets"/"cubone.png"
    art=Image.open(path).convert("RGBA")
    if art.size!=(475,475):art=art.resize((475,475),Image.Resampling.LANCZOS)
    # Contorno manual aproximado basado en la referencia original; no se deforma el dibujo.
    pts=[(128,17),(183,53),(247,32),(309,43),(367,22),
         (342,70),(374,85),(401,144),(390,197),(350,220),
         (363,247),(330,254),(302,272),(264,264),(200,270),
         (132,258),(112,231),(123,167),(141,113),(159,80)]
    m=Image.new("L",art.size,0)
    dm=ImageDraw.Draw(m);dm.polygon(pts,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(1.2))
    art.putalpha(ImageChops.multiply(art.getchannel("A"),m))
    box=art.getbbox()
    if box:art=art.crop(box)
    art.thumbnail((i(127),i(120)),Image.Resampling.LANCZOS)
    canvas.alpha_composite(art,(i(cx)-art.width//2,i(cy)-art.height//2))

def bone(d,cx,cy,s=1):
    # Hueso de Cubone como OBJETO separado, no se atribuye su origen a la madre.
    d.ellipse(pos((cx-79*s,cy-28*s,cx-42*s,cy+6*s)),fill="#fbefdb",outline="#acaaa5",width=i(2*s))
    d.ellipse(pos((cx-63*s,cy-55*s,cx-28*s,cy-18*s)),fill="#fbefdb",outline="#acaaa5",width=i(2*s))
    d.polygon([(i(cx-44*s),i(cy-33*s)),(i(cx+47*s),i(cy+28*s)),(i(cx+33*s),i(cy+52*s)),(i(cx-54*s),i(cy-14*s))],fill="#f0e9d9")
    d.line([(i(cx-36*s),i(cy-20*s)),(i(cx+37*s),i(cy+32*s))],fill="#c2bdb3",width=i(3*s))
    d.ellipse(pos((cx+29*s,cy+19*s,cx+65*s,cy+55*s)),fill="#faeedb",outline="#acaaa5",width=i(2*s))
    d.ellipse(pos((cx+48*s,cy+1*s,cx+83*s,cy+36*s)),fill="#faeedb",outline="#acaaa5",width=i(2*s))
def panel(img,xywh,accent="#aeeefa"):
    x,y,w,h=xywh
    shadow(img,xywh)
    d=ImageDraw.Draw(img)
    dr_box(d,(x,y,x+w,y+h),(20,31,54,235),16,outline=(173,207,217,190),width=2)
    dr_box(d,(x+9,y+9,x+w-9,y+15),accent,3)
    corner(d,x+16,y+21,col=accent)
    return d
# Pokédex con pantalla, Cubone seleccionado e icono Poké Ball.
im=new();d=ImageDraw.Draw(im)
shadow(im,(295,356,224,281),120)
d=ImageDraw.Draw(im)
dr_box(d,(292,350,521,651),"#d84754",18,outline="#f5aab1",width=3)
dr_box(d,(300,358,512,644),"#b93443",13)
dr_box(d,(304,365,509,394),"#ed6570",8)
ellipse(d,(313,365,344,396),"#2a365c",outline="#f8e3d6",width=3)
ellipse(d,(320,372,338,390),"#7cc4e9")
ellipse(d,(324,376,331,382),"#fff9e2")
for j,c in enumerate(["#e6cb6f","#6edca2","#f4aab6"]):ellipse(d,(353+j*17,370,364+j*17,381),c)
dr_box(d,(309,407,505,575),"#222c44",10,outline="#f7c6a7",width=2)
dr_box(d,(318,417,496,563),"#c1e5db",5)
txt(d,329,425,"POKÉDEX   Nº 0104",13,"#213c4d")
line(d,[(328,448),(489,448)],"#638e9c",1)
# Mini Cubone 
cub=ROOT/"cubone.png"
if not cub.exists():cub=ROOT/"assets/cubone.png"
if cub.exists():
    icon=Image.open(cub).convert("RGBA")
    bbox=icon.getbbox()
    if bbox:icon=icon.crop(bbox)
    icon.thumbnail((i(103),i(94)),Image.Resampling.LANCZOS)
    im.alpha_composite(icon,(i(320),i(458)))
d=ImageDraw.Draw(im)
txt(d,424,462,"CUBONE",13,"#253848")
txt(d,423,484,"TIERRA",11,"#75573b")
txt(d,423,503,"SOLITARIO",9,"#253848")
for j in range(7):dr_box(d,(426+j*8,543,430+j*8,553),"#4e8d8d",1)
ball(d,330,609,17)
dr_box(d,(367,591,490,630),"#e88a96",6)
txt(d,380,601,"REGISTRADO",12,"#532838")
save(im,"01-pokedex.png")
# Ficha: cráneo
im=new();d=panel(im,(282,385,240,286),accent="#ecdeaa")
dr_box(d,(296,411,510,445),"#f2e1bd",7)
txt(d,304,418,"OBJETO · 01",15,"#3d3d50")
isolated_skull(im,399,521)
line(d,[(305,584),(505,584)],"#7b8d91",1)
txt(d,302,594,"CRÁNEO",19,"#fdf5e4")
txt(d,302,622,"Era de su madre.",12,"#eacda9",False)
txt(d,302,640,"Dato de la Pokédex",10,"#b9b7ba",False)
save(im,"02-craneo.png")
# Ficha: hueso
im=new();d=panel(im,(283,406,241,258),accent="#f2bd7d")
dr_box(d,(297,433,511,466),"#e1a376",7)
txt(d,306,438,"OBJETO · 02",15,"#372e40")
bone(d,404,528,.65)
line(d,[(301,584),(503,584)],"#9a8691",1)
txt(d,303,589,"HUESO",19,"#fff4e4")
txt(d,303,620,"Lo usa para luchar.",12,"#f6d8bb",False)
txt(d,303,640,"Objeto característico",10,"#bfbac1",False)
save(im,"03-hueso.png")
# Encuentro (Poké Ball como indicador de interfaz, no captura)
im=new();d=panel(im,(284,382,238,253),accent="#a0e2cf")
dr_box(d,(297,406,509,445),"#9fd9c6",8)
txt(d,307,417,"¡ENCUENTRO!",16,"#214653")
ball(d,328,511,30)
txt(d,370,475,"EEVEE",19)
txt(d,370,505,"Nº 0133",13,"#c8f3e7")
txt(d,307,575,"Viene a acompañarlo",11,"#ffead8",False)
txt(d,307,603,"Sin combate ni captura",10,"#b7bac8",False)
save(im,"04-encuentro.png")
# Medallón final discreto
im=new();d=ImageDraw.Draw(im)
shadow(im,(300,365,217,170),80,8)
dr_box(d,(299,365,522,544),(21,35,57,239),17,outline=(237,194,148,230),width=2)
ball(d,346,417,28)
txt(d,390,386,"POKÉDEX",17)
txt(d,390,411,"#0104",16,"#b4e2de")
txt(d,315,471,"UNA HISTORIA",14)
txt(d,315,496,"QUE SIGUE...",14,"#ffdaac")
save(im,"05-final.png")
# Poké Ball pictograma independiente, para animar su suave flotación.
im=new();d=ImageDraw.Draw(im)
ball(d,85,83,41)
im.crop(pos((32,30,138,136))).save(OUT/"06-pokeball.png")
# Bocetos para reutilizar en futuras historias.
im=new();d=ImageDraw.Draw(im);skull(d,260,310,2.4);im.crop(pos((80,115,450,505))).save(OUT/"07-craneo-objeto.png")
im=new();d=ImageDraw.Draw(im);bone(d,270,300,1.7);im.crop(pos((103,167,465,425))).save(OUT/"08-hueso-objeto.png")
(OUT/"escenas.json").write_text(json.dumps({
  "version":"02","duracion_original":61.754,
  "elementos":[
    {"asset":"01-pokedex.png","inicio":1.3,"fin":6.55,"descripcion":"Pokédex roja, Cubone #0104 tipo Tierra"},
    {"asset":"02-craneo.png","inicio":7.1,"fin":14.1,"descripcion":"Cráneo materno, ficha #01"},
    {"asset":"03-hueso.png","inicio":18.3,"fin":27.0,"descripcion":"Hueso para combatir, ficha #02"},
    {"asset":"04-encuentro.png","inicio":35.15,"fin":40.5,"descripcion":"Ficha Eevee #0133 con Poké Ball de interfaz"},
    {"asset":"05-final.png","inicio":59.65,"fin":61.55,"descripcion":"Pokédex actualizada, cierre"},
  ],
  "nota":"La Poké Ball es un elemento de interfaz; la historia no incluye captura"
},indent=2,ensure_ascii=False),encoding="utf8")
print("Assets listo",len(list(OUT.glob('*.png'))))

