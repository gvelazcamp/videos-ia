"""Voltito: visor de poses auténticas, sin sustitución por modelos 3D inventados.
Entrada: fotografía con frente y perfil derecho enviada por el usuario, más
perfil izquierdo y espalda YA presentes y aprobados en el repositorio.
Remove.bg Web (gratis) se ejecuta para las dos vistas sobre fondo blanco.
"""
from pathlib import Path
from urllib.request import urlopen, Request
from io import BytesIO
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
SOURCE_URL="https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/f4e943d9-e3c9-414d-9d0d-1fa3f7eccdfc.jpg"
PREVIOUS=ROOT/"experimentos/voltito-360-fiel-20261117"
FRONT_3Q=ROOT/"experimentos/voltito-png-original-20261117/voltito-original-transparente.png"
CANVAS=(1200,1550)
SRC_PARTS={
    "frente":(0,280,528,1238),
    "derecha":(540,280,1049,1238),
}
FINAL_NAMES=("frente","derecha","espalda","izquierda","trescuartos-original","trescuartos-reflejo")

def prepare():
    BASE.mkdir(parents=True,exist_ok=True)
    req=Request(SOURCE_URL,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
    with urlopen(req,timeout=55) as response:
        data=response.read(5_000_001)
    if len(data)>5_000_000:raise ValueError("Imagen de referencia demasiado grande")
    with Image.open(BytesIO(data)) as image:
        image.load()
        if image.size!=(1049,1536):
            raise ValueError(f"No es la lámina aportada: {image.size}")
        image=image.convert("RGB")
        for name,box in SRC_PARTS.items():
            crop=image.crop(box)
            if crop.width<400 or crop.height<850:raise ValueError("Recorte pequeño")
            crop.save(BASE/f"fuente-{name}.png","PNG",optimize=True)
            print("Fuente aportada por usuario:",name,crop.size,flush=True)

def rgba_original(path):
    with Image.open(path) as im:
        im.load()
        if im.mode!="RGBA":raise ValueError(f"No es PNG RGBA aprobado: {path}")
        rgba=im.copy()
    if rgba.getchannel("A").getextrema()!=(0,255):
        raise ValueError("Original sin transparencia real")
    return rgba

def free_cutout(name):
    """Aplicar máscara de Remove.bg al RGB HD original, sin reducir detalles."""
    with Image.open(BASE/f"fuente-{name}.png") as rgb:
        original=rgb.convert("RGB")
    with Image.open(BASE/f"removebg-{name}.png") as cut:
        cut.load()
        mask=cut.convert("RGBA").getchannel("A")
        if mask.getextrema()!=(0,255):
            raise ValueError("Remove.bg devolvió un PNG sin transparencia válida")
    # La descarga gratuita es vista previa; conservar RGB original y escalar alfa.
    alpha=mask.resize(original.size,Image.Resampling.LANCZOS)
    # Conservar rasgos finos; reducir un borde blanco de un solo píxel.
    alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.35))
    arr=np.asarray(original,dtype=np.float32)
    a=np.asarray(alpha,dtype=np.float32)/255.0
    # Quitar halo blanco del JPEG en los píxeles de transición, NO alterar el interior.
    lim=(a>.07)&(a<.98)
    fixed=arr.copy()
    safe=np.maximum(a[...,None],.09)
    fixed[lim]=np.clip(((arr-254*(1-safe))/safe),0,255)[lim]
    rgba=Image.fromarray(np.uint8(np.round(np.clip(fixed,0,255))),"RGB").convert("RGBA")
    rgba.putalpha(alpha)
    if np.count_nonzero(a>.7)<25000:
        raise ValueError(f"Mask de Remove.bg anormalmente pequeña ({name})")
    return rgba

def clean_existing(rgba):
    # A diferencia de las nuevas vistas, ya tienen el fondo eliminado.
    alpha=rgba.getchannel("A").filter(ImageFilter.MinFilter(3))
    out=rgba.copy()
    out.putalpha(alpha)
    return out

def normalize(image):
    rgba=image.convert("RGBA")
    bb=rgba.getchannel("A").point(lambda v:255 if v>14 else 0).getbbox()
    if bb is None:raise ValueError("Personaje invisible")
    # Margen externo mínimo y sin sombra del suelo.
    bb=(max(0,bb[0]-5),max(0,bb[1]-5),min(rgba.width,bb[2]+5),min(rgba.height,bb[3]+5))
    cut=rgba.crop(bb)
    factor=min(1120/cut.width,1420/cut.height)
    size=(max(1,round(cut.width*factor)),max(1,round(cut.height*factor)))
    cut=cut.resize(size,Image.Resampling.LANCZOS)
    bg=Image.new("RGBA",CANVAS,(0,0,0,0))
    bg.alpha_composite(cut,((CANVAS[0]-size[0])//2,CANVAS[1]-size[1]-52))
    return bg

def finish():
    originals={
        "frente":free_cutout("frente"),
        "derecha":free_cutout("derecha"),
        "izquierda":clean_existing(rgba_original(PREVIOUS/"referencia-izquierda-original.png")),
        "espalda":clean_existing(rgba_original(PREVIOUS/"referencia-espalda-original.png")),
        "trescuartos-original":clean_existing(rgba_original(FRONT_3Q)),
    }
    # Ángulo auxiliar: reflejo del dibujo original. No se presenta como foto real.
    originals["trescuartos-reflejo"]=ImageOps.mirror(originals["trescuartos-original"])
    sprites={}
    for name in FINAL_NAMES:
        img=normalize(originals[name])
        target=BASE/f"voltito-{name}.png"
        img.save(target,"PNG",optimize=True)
        with Image.open(target) as verify:
            verify.load()
            assert verify.format=="PNG" and verify.mode=="RGBA" and verify.size==CANVAS
            assert verify.getchannel("A").getextrema()==(0,255)
            # Validación de la silueta del personaje en todas las vistas.
            coverage=sum(v>100 for v in verify.getchannel("A").resize((96,124)).getdata())
            if coverage<1400:raise ValueError(f"PNG vacío o recortado: {name}: {coverage}")
        sprites[name]=img
        print("PNG fiel verificado:",name,img.size,target.stat().st_size,flush=True)
    # Lámina comparativa explícitamente sin confundirla con un modelo 3D.
    order=["frente","derecha","espalda","izquierda","trescuartos-original","trescuartos-reflejo"]
    sheet=Image.new("RGB",(1800,1200),(14,40,51))
    draw=ImageDraw.Draw(sheet)
    for i,name in enumerate(order):
        x=(i%3)*600; y=(i//3)*600
        draw.rounded_rectangle((x+10,y+8,x+590,y+585),radius=22,fill=(28,70,78),outline=(72,126,125),width=2)
        src=sprites[name].copy()
        src.thumbnail((570,510),Image.Resampling.LANCZOS)
        sheet.paste(src,(x+(600-src.width)//2,y+18),src)
        draw.text((x+35,y+555),name.replace("-"," ").upper(),fill=(255,236,178))
    sheet.save(BASE/"comparacion-vistas.jpg","JPEG",quality=86,optimize=True)
    print("ÉXITO: 6 vistas exactas/derivadas sin generar otro personaje",flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("preparar","finalizar"):
        raise SystemExit("Uso: procesar.py preparar | finalizar")
    (prepare if sys.argv[1]=="preparar" else finish)()
