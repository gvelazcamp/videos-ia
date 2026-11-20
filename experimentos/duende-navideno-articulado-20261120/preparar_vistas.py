"""Preparar 8 vistas reales desde la lamina adjunta por Gonzalo; sin generacion de imagenes nuevas.
Conserva el montaje, elimina solo el fondo negro conectado al borde y normaliza escala.
"""
from pathlib import Path
from urllib.request import urlopen,Request
import hashlib
import numpy as np
import cv2
from PIL import Image

SOURCE_URL="https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/7f9e0dee-154d-49f5-9b09-98a278388393.png"
SOURCE_SHA256="30d12f261f03eefee163a7079b17176242a6d5a0762be87df10efc5f427faa58"
ROOT=Path(__file__).resolve().parent
DEST=ROOT/"vistas-10"
DEST.mkdir(parents=True,exist_ok=True)
req=Request(SOURCE_URL,headers={"User-Agent":"Mozilla/5.0"})
with urlopen(req,timeout=45) as resp:
    original=resp.read()
assert hashlib.sha256(original).hexdigest()==SOURCE_SHA256,"La imagen remota no coincide con el archivo de Gonzalo"
source=DEST.parent/"referencia-original.png"
source.write_bytes(original)
photo=Image.open(source).convert("RGB")
assert photo.size==(2000,375),f"Dimensiones inesperadas {photo.size}"
names=[
"01-frente-000.png",
"02-frente-trescuartos-derecho-045.png",
"03-perfil-derecho-090.png",
"04-trasera-trescuartos-derecho-135.png",
"05-espalda-180.png",
"06-trasera-trescuartos-izquierdo-225.png",
"07-perfil-izquierdo-270.png",
"08-frente-trescuartos-izquierdo-315.png",
]
for i,name in enumerate(names):
    rgb=np.array(photo.crop((i*250+8,43,i*250+244,355)))
    # Background is connected near-black pixels only, protect internal black details.
    dark=(rgb.max(axis=2)<24).astype("uint8")
    _, labels, _, _=cv2.connectedComponentsWithStats(dark,connectivity=8)
    edge=np.unique(np.concatenate((labels[0,:],labels[-1,:],labels[:,0],labels[:,-1])))
    exterior=(np.isin(labels,edge)&(dark>0)).astype("uint8")
    exterior=cv2.dilate(exterior,np.ones((2,2),np.uint8))
    alpha=np.where(exterior>0,0,255).astype("uint8")
    yy,xx=np.where(alpha>100)
    if not len(xx): raise ValueError("Sin sujeto en "+name)
    rgba=np.dstack((rgb,alpha))[yy.min():yy.max()+1,xx.min():xx.max()+1]
    sprite=Image.fromarray(rgba,"RGBA")
    scale=min(414/sprite.width,452/sprite.height)
    sprite=sprite.resize((round(sprite.width*scale),round(sprite.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new("RGBA",(512,512),(0,0,0,0))
    canvas.alpha_composite(sprite,((512-sprite.width)//2,(512-sprite.height)//2))
    dst=DEST/name
    canvas.save(dst,optimize=True)
    assert canvas.getchannel("A").getextrema()==(0,255)
    print("VISTA",name,dst.stat().st_size,flush=True)
(DEST/"PREPARADAS.txt").write_text(
    "8 vistas extraidas del montaje real de Gonzalo. Referencia original: ../referencia-original.png. "
    "No hay vista superior/inferior en la imagen suministrada; no se inventaron. "
    "Pendiente reconstruccion TRELLIS.\n",encoding="utf-8")
print("PREPARACION_OK",flush=True)
