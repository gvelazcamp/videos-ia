"""Voltito 360 fiel: preparar archivos originales RGBA para visor táctil.
Dos imágenes provienen del usuario; frente reutiliza el recorte aprobado.
NO redibujar, deformar, borrar rasgos ni sustituir el diseño.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import io, math

ROOT=Path(__file__).resolve().parents[2]
DEST=Path(__file__).resolve().parent
DEST.mkdir(parents=True,exist_ok=True)

SOURCES={
  "espalda":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/09dda97b-7e34-4832-acbc-ade15f0a4fb4.png",
  "izquierda":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/b5bb9b76-6f0e-42a0-8bd0-49144a65e87b.png"
}
FRONT=ROOT/"experimentos/voltito-png-original-20261117/voltito-original-transparente.png"
SIZE=(1200,1550)

def load_image(name):
    if name=="frente":
        if not FRONT.is_file():
            raise FileNotFoundError(f"El frontal aprobado no está en Git: {FRONT}")
        with Image.open(FRONT) as im:
            im.load()
            return im.convert("RGBA")
    target=DEST/f"referencia-{name}-original.png"
    if not target.exists():
        req=Request(SOURCES[name],headers={"User-Agent":"Mozilla/5.0","Accept":"image/png,image/*"})
        with urlopen(req, timeout=60) as response:
            blob=response.read(15_000_001)
        if len(blob)>15_000_000:
            raise ValueError(f"Imagen {name} supera 15MB")
        with Image.open(io.BytesIO(blob)) as im:
            im.load()
            if min(im.size)<800 or im.mode!="RGBA":
                raise ValueError(f"Referencia no es PNG RGBA de alta resolución: {name}, {im.mode}, {im.size}")
            im.save(target,format="PNG",optimize=True)
        print("DESCARGADO",name,len(blob), flush=True)
    with Image.open(target) as im:
        im.load()
        return im.convert("RGBA")

def make_sprite(img, side=False):
    alpha=img.getchannel("A")
    if alpha.getextrema()!=(0,255):
        raise ValueError("Imagen no tiene fondo realmente transparente")
    # Evitar halos de Remove.bg sin adelgazar el pelaje: solo 1px de borde.
    cleaned=alpha.filter(ImageFilter.MinFilter(3))
    img=img.copy()
    img.putalpha(cleaned)
    bb=cleaned.point(lambda v: 255 if v>12 else 0).getbbox()
    if not bb:
        raise ValueError("El recorte está vacío")
    # conservar margen externo de pelo
    pad=5
    bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),
        min(img.width,bb[2]+pad),min(img.height,bb[3]+pad))
    img=img.crop(bb)
    if side:
        img=ImageOps.mirror(img)
    factor=min((SIZE[0]-100)/img.width,(SIZE[1]-80)/img.height)
    # No imponer resolución artificial: solo se remuestrea para el visor.
    img=img.resize((round(img.width*factor),round(img.height*factor)),Image.Resampling.LANCZOS)
    out=Image.new("RGBA",SIZE,(0,0,0,0))
    x=(SIZE[0]-img.width)//2
    y=SIZE[1]-img.height-35
    out.alpha_composite(img,(x,y))
    return out

def create_sheet(sprites):
    sheet=Image.new("RGB",(1600,670),(15,43,54))
    d=ImageDraw.Draw(sheet)
    for i,name in enumerate(("frente","izquierda","espalda","derecha")):
        left=i*400
        d.rounded_rectangle((left+7,12,left+393,652),radius=22, fill=(28,65,72),outline=(80,128,132),width=2)
        sprite=sprites[name].copy()
        sprite.thumbnail((378,555),Image.Resampling.LANCZOS)
        sheet.paste(sprite,(left+(400-sprite.width)//2,36),sprite)
        d.text((left+120,607),name.upper(),fill=(246,235,174))
    sheet.save(DEST/"vista-previa-4-vistas.png",format="PNG",optimize=True)

def make_gif(sprites):
    views=["frente","izquierda","espalda","derecha"]
    frames=[]
    for step in range(40):
        angle=step/40*4
        i=int(angle)%4
        t=angle-i
        next_i=(i+1)%4
        a=max(0.0,min(1.0,(t-.33)/.34))
        a=a*a*(3-2*a)
        frame=Image.new("RGBA",(460,600),(19,54,64,255))
        dr=ImageDraw.Draw(frame)
        dr.ellipse((70,554,393,582),fill=(8,30,37,200))
        for k,opacity in [(i,1-a),(next_i,a)]:
            if opacity<=0:continue
            spr=sprites[views[k]].resize((426,550),Image.Resampling.LANCZOS)
            if opacity<1:
                spr.putalpha(spr.getchannel("A").point(lambda v:int(v*opacity)))
            frame.alpha_composite(spr,(17,16))
        dr=ImageDraw.Draw(frame)
        dr.rounded_rectangle((188,558,271,587),radius=12,fill=(9,35,43,245))
        dr.text((207,567),str(round(step*360/40))+"°",fill=(255,235,174))
        frames.append(frame.convert("RGB").quantize(colors=128,method=Image.Quantize.FASTOCTREE))
    target=DEST/"voltito-giro-360.gif"
    frames[0].save(target,save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=2,optimize=True)
    with Image.open(target) as im:
        assert im.n_frames==40 and im.size==(460,600)
    print("GIF OK",target,target.stat().st_size, flush=True)

def main():
    source={name:load_image(name) for name in ("frente","izquierda","espalda")}
    # Exact same picture, mirrored as placeholder for missing right profile.
    sprites={name:make_sprite(source[name]) for name in source}
    sprites["derecha"]=make_sprite(source["izquierda"],side=True)
    for name,img in sprites.items():
        target=DEST/f"voltito-{name}.png"
        img.save(target,format="PNG",optimize=True)
        with Image.open(target) as checked:
            checked.load()
            assert checked.size==SIZE and checked.mode=="RGBA"
            assert checked.getchannel("A").getextrema()==(0,255)
        visible=sum(1 for a in img.getchannel("A").resize((90,120)).getdata() if a>120)
        if visible<900:
            raise ValueError(f"Sprite incorrecto {name} cobertura={visible}")
        print("VERIFICADO:",name,img.size,"cobertura:",visible,flush=True)
    create_sheet(sprites)
    make_gif(sprites)
    print("RESULTADO: recursos PNG transparentes y visor giratorio sin personajes redibujados.",flush=True)

if __name__=="__main__":
    main()
