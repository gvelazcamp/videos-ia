"""Importa las dos imágenes aprobadas por Gonzalo y las prepara para Remove.bg.
La fuente son exactamente los PNG de esta conversación, no las miniaturas de la ficha.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
import sys
import numpy as np
from PIL import Image,ImageFilter

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
ASSETS=HERE/"referencias"
URLS={
 "perfil":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/660b81aa-9a84-4daa-ae8d-60bff370cb8b.png",
 "espalda":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/0b2f3240-afa1-4915-8dc0-099397281afa.png",
}

def preparar():
 ASSETS.mkdir(parents=True,exist_ok=True)
 for name,url in URLS.items():
  req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
  with urlopen(req,timeout=70) as r: raw=r.read(9_000_000)
  with Image.open(BytesIO(raw)) as src:
   src.load()
   if src.width<900 or src.height<1300 or src.mode!="RGBA":
    raise ValueError("La imagen descargada no es la referencia PNG de alta calidad: "+name)
   if src.getchannel("A").getextrema()!=(0,255):raise ValueError("El adjunto perdió la transparencia")
   src.save(ASSETS/f"original-{name}.png","PNG",optimize=True)
   # Fondo neutro para que Remove.bg evalúe el recorte una vez más.
   flat=Image.new("RGBA",src.size,(235,239,240,255))
   flat.alpha_composite(src)
   flat.convert("RGB").save(ASSETS/f"para-removebg-{name}.png","PNG",optimize=True)
   print("Recibida exactamente la foto del chat",name,src.size)

def finalizar():
 for name in URLS:
  with Image.open(ASSETS/f"original-{name}.png") as im: src=im.convert("RGBA")
  with Image.open(ASSETS/f"preview-removebg-{name}.png") as im: preview=im.convert("RGBA")
  mask=preview.getchannel("A")
  if mask.getextrema()!=(0,255):raise ValueError("Remove.bg no devolvió transparencia: "+name)
  mask=mask.resize(src.size,Image.Resampling.LANCZOS)
  original_alpha=src.getchannel("A")
  import cv2
  original=np.asarray(original_alpha,dtype=np.uint8)
  mask=np.asarray(mask,dtype=np.uint8)
  # Mantener la silueta original y sólo eliminar derrames externos y restos de halo.
  # Si la vista gratuita de Remove.bg pierde trozos, nunca se aplica una máscara dañina.
  antialias=np.minimum(original,cv2.GaussianBlur(original,(3,3),.65))
  antialias=np.uint8(antialias)
  shrink=cv2.erode(antialias,np.ones((3,3),np.uint8))
  edge=np.where((antialias>0)&(antialias<230),shrink,antialias).astype(np.uint8)
  # Remove.bg como máscara adicional únicamente donde confirma fondo.
  confirmed=(mask<8)&(original<180)
  edge[confirmed]=0
  compare=(edge>96).sum()/max(1,(original>96).sum())
  if compare<.88: raise ValueError(f"Recorte excesivo de {name}: {compare:.2f}")
  src.putalpha(Image.fromarray(edge,"L"))
  out=ASSETS/f"voltito-{name}-removebg-hd.png"
  src.save(out,"PNG",optimize=True)
  with Image.open(out) as valid:
   valid.load()
   assert valid.mode=="RGBA" and valid.getchannel("A").getextrema()==(0,255)
   assert valid.size[0]>900 and valid.size[1]>1300
  print("HD original con bordes limpios:",out.relative_to(ROOT),compare)

if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in ("preparar","finalizar"):
  raise SystemExit("Uso: referencias.py preparar|finalizar")
 globals()[sys.argv[1]]()
