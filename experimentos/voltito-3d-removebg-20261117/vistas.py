"""Prepara y finaliza tres vistas transparentes de referencia para el visor 3D.
No modifica las imágenes originales. El recorte de fondo lo hace Remove.bg web.
"""
from pathlib import Path
from PIL import Image, ImageFilter
import sys

ROOT=Path(__file__).resolve().parents[2]
DEST=Path(__file__).resolve().parent
SOURCE=ROOT/"experimentos/voltito-realista-360-20261117/voltito-hoja-original.png"
BOXES={"izquierda":(840,14,1031,333),"derecha":(1044,14,1239,333),"espalda":(1151,14,1390,333)}
# Espalda en ficha: última vista a partir x 1150.
OUT_SIZE=(700,920)

def preparar():
    with Image.open(SOURCE) as image:
        original=image.convert("RGB")
        if original.size!=(1536,1152): raise ValueError(f"Referencia inesperada {original.size}")
        DEST.mkdir(parents=True,exist_ok=True)
        for name,box in BOXES.items():
            im=original.crop(box)
            # Original conserva color, bordes y detalles; remove.bg limpia el fondo.
            im.save(DEST/f"origen-{name}.png","PNG",optimize=True)
            print("Referencia",name,im.size)

def finalizar():
    for name in BOXES:
        raw=DEST/f"origen-{name}.png"
        out=DEST/f"removebg-{name}.png"
        with Image.open(raw) as im: rgb=im.convert("RGB")
        with Image.open(out) as im:
            rgba=im.convert("RGBA")
            alpha=rgba.getchannel("A")
            if alpha.getextrema()!=(0,255): raise ValueError(f"Remove.bg no devolvió alpha válido: {name}")
            alpha=alpha.resize(rgb.size,Image.Resampling.LANCZOS)
        # Encoger 1 píxel los bordes elimina halos claros antes de suavizar.
        alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.35))
        person=rgb.convert("RGBA")
        person.putalpha(alpha)
        bbox=alpha.getbbox()
        if not bbox: raise ValueError(f"Recorte vacío: {name}")
        person=person.crop(bbox)
        person.thumbnail((630,820),Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",OUT_SIZE,(0,0,0,0))
        canvas.alpha_composite(person,((OUT_SIZE[0]-person.width)//2,(OUT_SIZE[1]-person.height)//2))
        target=DEST/f"voltito-{name}-removebg.png"
        canvas.save(target,"PNG",optimize=True)
        with Image.open(target) as check:
            check.load()
            if check.mode!="RGBA" or check.getchannel("A").getextrema()!=(0,255):
                raise ValueError(f"PNG transparente inválido: {name}")
            if check.getchannel("A").getbbox() is None:
                raise ValueError(f"PNG vacío: {name}")
        print("VERIFICADO",target,canvas.size)

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("preparar","finalizar"):
        raise SystemExit("Uso: vistas.py preparar|finalizar")
    globals()[sys.argv[1]]()
