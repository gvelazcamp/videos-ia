"""Voltito: extraer CUATRO vistas del mismo sheet 1103x1536 y eliminar fondo.
Se conserva el color original de la imagen; Remove.bg aporta sólo la máscara.
Todas las vistas tienen idéntica escala y tamaño (sin redibujar personajes).
"""
from pathlib import Path
from io import BytesIO
from urllib.request import Request,urlopen
from PIL import Image,ImageFilter
import numpy as np
import sys,json
ROOT=Path.cwd()
HERE=Path(__file__).resolve().parent
URL="https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/6650bb2e-8d7d-494b-9a32-a9be0d406f2c.jpg"
# Misma área útil, sin bordes de las tarjetas ni rótulos.
# Conservan mismo tamaño de imagen y posición de los pies.
BOXES={
 "frente":(105,107,451,659),
 "espalda":(607,107,953,659),
 "izquierda":(120,800,466,1352),
 "derecha":(616,800,962,1352)
}
SOURCE_SIZE=(1103,1536)
OUTPUT_SIZE=(768,1024)
def preparar():
    req=Request(URL,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
    with urlopen(req,timeout=60) as resp: content=resp.read(6_000_000)
    with Image.open(BytesIO(content)) as sheet:
        sheet.load()
        if sheet.size!=SOURCE_SIZE:raise RuntimeError(f"Dimensiones inesperadas {sheet.size}; no usar otra lámina")
        sheet.convert("RGB").save(HERE/"lamina-original.jpg",quality=98,subsampling=0,optimize=True)
        for name,box in BOXES.items():
            crop=sheet.crop(box).convert("RGB")
            if crop.size!=(346,552):raise RuntimeError(f"Vista desigual {name}: {crop.size}")
            crop.save(HERE/f"origen-{name}.png",optimize=True)
            print("LAMINA ORIGINAL",name,crop.size,flush=True)
def finalizar():
    stats={}
    for name in BOXES:
        with Image.open(HERE/f"origen-{name}.png") as r: rgb=r.convert("RGB")
        with Image.open(HERE/f"removebg-{name}.png") as m:
            m.load(); mask=m.convert("RGBA").getchannel("A")
        if mask.getextrema()!=(0,255):raise RuntimeError(f"Remove.bg no entregó PNG transparente: {name}")
        alpha=mask.resize(rgb.size,Image.Resampling.LANCZOS)
        alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.35))
        a=np.asarray(alpha,dtype=np.uint8)
        cov=float(np.mean(a>128))
        if not (.12<cov<.77):raise RuntimeError(f"Máscara inesperada {name}: cobertura {cov:.2f}")
        if max(int(a[0,0]),int(a[0,-1]),int(a[-1,0]),int(a[-1,-1]))>12:
            raise RuntimeError(f"La máscara conserva esquinas/bordes del panel: {name}")
        rgba=rgb.convert("RGBA")
        rgba.putalpha(alpha)
        # Corregir halos blancos en transición; nunca modificar píxeles interiores.
        col=np.array(rgba,dtype=np.uint8)
        edge=(col[:,:,3]>0)&(col[:,:,3]<240)
        color=col[:,:,:3].astype(np.float32)
        af=np.maximum(col[:,:,3].astype(np.float32)/255,.16)
        proposed=np.clip((color-250.*(1-af[:,:,None]))/af[:,:,None],0,255).astype(np.uint8)
        color[edge]=proposed[edge]
        col[:,:,:3]=color.astype(np.uint8)
        rgba=Image.fromarray(col,"RGBA")
        # MISMA escala y ubicación para las 4 poses (nunca encoger uno arbitrariamente).
        size=(583,930)
        resized=rgba.resize(size,Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",OUTPUT_SIZE,(0,0,0,0))
        canvas.alpha_composite(resized,((OUTPUT_SIZE[0]-size[0])//2,42))
        dest=HERE/f"voltito-{name}.png"
        canvas.save(dest,optimize=True)
        with Image.open(dest) as verify:
            verify.load()
            assert verify.size==OUTPUT_SIZE and verify.mode=="RGBA"
            assert verify.getchannel("A").getextrema()==(0,255)
        stats[name]={"input_size":list(rgb.size),"canvas_size":list(OUTPUT_SIZE),"alpha_coverage":round(cov,3),"bytes":dest.stat().st_size}
        print("REMOVE.BG RGBA VERIFICADO",name,stats[name],flush=True)
    (HERE/"vistas-diagnostico.json").write_text(json.dumps(stats,indent=2))
if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("preparar","finalizar"):raise SystemExit("Uso: procesar.py preparar|finalizar")
    (preparar if sys.argv[1]=="preparar" else finalizar)()
