"""Extrae el Voltito EXACTO de la lámina aprobada y conserva su pelaje.
No lo redibuja, no cambia colores, ojos, orejas, cola ni expresión.
Separa preparación y finalización para reutilizar el Remove.bg web del puente.
"""
from pathlib import Path
import sys
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parents[2]
DIR=Path(__file__).resolve().parent
SOURCE=ROOT/"experimentos/voltito-realista-360-20261117/voltito-hoja-original.png"
CROP=DIR/"voltito-referencia-limpia.png"
MASK_FROM_REMOVE_BG=DIR/"voltito-removebg-preview.png"
FINAL=DIR/"voltito-original-transparente.png"
NATIVE=DIR/"voltito-original-nativo.png"
BOX=(16,0,588,864)

def preparar():
    DIR.mkdir(parents=True,exist_ok=True)
    with Image.open(SOURCE) as im:
        im.load()
        if im.size!=(1536,1152):
            raise ValueError(f"Referencia inesperada: {im.size}")
        rgb=np.asarray(im.convert("RGB"))
    # Solo se borran las letras/insignia del margen, fuera del personaje.
    letters=np.zeros(rgb.shape[:2],dtype=np.uint8)
    for x1,y1,x2,y2 in [(18,10,342,114),(18,119,237,286),(13,282,195,352)]:
        cv2.rectangle(letters,(x1,y1),(x2,y2),255,-1)
    clean=cv2.inpaint(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),letters,12,cv2.INPAINT_TELEA)
    x1,y1,x2,y2=BOX
    crop=cv2.cvtColor(clean[y1:y2,x1:x2],cv2.COLOR_BGR2RGB)
    Image.fromarray(crop).save(CROP,"PNG",optimize=True)
    print("CROP PREPARADO: ",CROP.relative_to(ROOT),crop.shape)

def finalizar():
    if not CROP.is_file() or not MASK_FROM_REMOVE_BG.is_file():
        raise FileNotFoundError("Falta imagen original preparada o recorte de Remove.bg")
    with Image.open(CROP) as im: original=im.convert("RGB")
    with Image.open(MASK_FROM_REMOVE_BG) as im:
        rgba=im.convert("RGBA")
        a=rgba.getchannel("A")
        if a.getextrema()!=(0,255):
            raise ValueError("Remove.bg no entregó transparencia completa")
        if abs((rgba.width/rgba.height)-(original.width/original.height))>.045:
            raise ValueError("Remove.bg alteró demasiado la proporción de la imagen")
        # Quitar únicamente la mancha triangular nacida al borrar el texto
        # de la lámina. No forma parte del Voltito original.
        a=a.resize(original.size,Image.Resampling.LANCZOS)
        extra=Image.new("L",original.size,0)
        ed=ImageDraw.Draw(extra)
        ed.polygon([(0,168),(190,168),(206,195),(210,223),
                    (210,249),(215,272),(191,305),(0,319)],fill=255)
        a=ImageChops.subtract(a,extra.filter(ImageFilter.GaussianBlur(1.2)))
    # Mantener los píxeles de la imagen original, no la vista previa comprimida.
    restored=original.convert("RGBA")
    restored.putalpha(a)
    # Borrar colores residuales de los píxeles totalmente transparentes.
    restored=Image.alpha_composite(Image.new("RGBA",restored.size,(0,0,0,0)),restored)
    bbox=a.getbbox()
    if not bbox:raise ValueError("Remove.bg dejó la máscara vacía")
    padding=18
    box=(max(0,bbox[0]-padding),max(0,bbox[1]-padding),
         min(restored.width,bbox[2]+padding),min(restored.height,bbox[3]+padding))
    cropped=restored.crop(box)
    cropped.save(NATIVE,"PNG",optimize=True)
    # Versión mayor para juegos y móviles: remuestrea fielmente el original.
    canvas=Image.new("RGBA",(1152,1728),(0,0,0,0))
    # thumbnail() solo reduce y no agranda: usar resize() a tamaño real de entrega.
    factor=min(1070/cropped.width,1630/cropped.height)
    size=(round(cropped.width*factor),round(cropped.height*factor))
    larger=cropped.resize(size,Image.Resampling.LANCZOS)
    larger=larger.filter(ImageFilter.UnsharpMask(radius=.6,percent=48,threshold=3))
    canvas.alpha_composite(larger,((1152-larger.width)//2,(1728-larger.height)//2))
    canvas.save(FINAL,"PNG",optimize=True)
    with Image.open(FINAL) as chk:
        chk.load()
        alpha=chk.getchannel("A")
        assert chk.size==(1152,1728) and alpha.getextrema()==(0,255)
        visible=sum(1 for n in alpha.resize((120,180)).getdata() if n>130)
        print("Pixeles visibles tras Remove.bg:",visible)
        assert visible>1000,"Máscara demasiado pequeña o pérdida de personaje"
        print("PNG FINAL VERIFICADO:", FINAL.relative_to(ROOT),chk.size,
              "pixeles opacos (muestra):",visible)
    print("Mismo Voltito de la lámina original, sin redibujar.")

if __name__=="__main__":
    action=sys.argv[1] if len(sys.argv)>1 else ""
    if action=="preparar":preparar()
    elif action=="finalizar":finalizar()
    else:raise SystemExit("Uso: recortar.py preparar|finalizar")
