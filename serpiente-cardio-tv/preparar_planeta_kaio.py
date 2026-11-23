#!/usr/bin/env python3
"""Descarga referencias del planeta de Kaio y King Kai y recorta fondos claros.
Crea imágenes WebP transparentes en ruta separada. No toca archivos originales.
Fuentes: UIDownload (uso no comercial), Fandom (referencia de personaje).
No usa ninguna API de pago. Aplicación equivalente a remove.bg para fondos planos.
"""
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO
from collections import deque
import requests
import json
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"assets-kaio"
OUT.mkdir(exist_ok=True)
HEADERS={"User-Agent":"Mozilla/5.0 (compatible; KaioAssetPrep/1.0)","Accept":"image/webp,image/png,image/jpeg,*/*"}
SOURCES={
 "planeta-real.webp":[
  "https://c0.uidownload.com/pngpics/1002/2220/king-kai-planet-dragon-ball-z-art-saiyan-world-goku-s-universe-cartoon-landscape-anime-scenery-green-planet-illustration.png",
 ],
 "kaio-real.webp":[
  "https://vignette.wikia.nocookie.net/vsdebating/images/9/99/King_Kai.png/revision/latest?cb=20170530062719",
  "https://www.pinclipart.com/picdir/middle/199-1994824_this-dragon-ball-z-king-kai-clipart.png",
 ]
}

def fetch(url):
    response=requests.get(url,headers=HEADERS,timeout=30)
    response.raise_for_status()
    if not response.headers.get("Content-Type","").lower().startswith("image/"):
        raise ValueError("El servidor no devolvio una imagen")
    return Image.open(BytesIO(response.content)).convert("RGBA")

def remove_flat_bg(im):
    """Flood fill only exterior light neutral pixels; preserve interior whites."""
    im=im.copy()
    pix=im.load()
    w,h=im.size
    # If background already transparent, preserve the genuine alpha.
    if min(im.getchannel("A").getextrema()) < 240:
        return im
    def light(x,y):
        r,g,b,a=pix[x,y]
        return min(r,g,b)>211 and max(r,g,b)-min(r,g,b)<33
    seen=bytearray(w*h)
    q=deque()
    for x in range(w):
        for y in (0,h-1):
            i=y*w+x
            if not seen[i] and light(x,y):seen[i]=1;q.append((x,y))
    for y in range(h):
        for x in (0,w-1):
            i=y*w+x
            if not seen[i] and light(x,y):seen[i]=1;q.append((x,y))
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if nx<0 or ny<0 or nx>=w or ny>=h:continue
            idx=ny*w+nx
            if not seen[idx] and light(nx,ny):
                seen[idx]=1
                q.append((nx,ny))
    # Edge feather on inner edge of removed region without impacting textures.
    for y in range(h):
        for x in range(w):
            if seen[y*w+x]:
                r,g,b,a=pix[x,y]
                pix[x,y]=(r,g,b,0)
    return im

report={}
for target,urls in SOURCES.items():
    errors=[]
    for url in urls:
        try:
            source=fetch(url)
            img=remove_flat_bg(source)
            alpha=img.getchannel("A")
            bbox=alpha.getbbox()
            if not bbox:raise ValueError("El recorte quedo vacio")
            img=img.crop(bbox)
            width,height=img.size
            if max(width,height)>1100:
                img.thumbnail((1100,1100),Image.Resampling.LANCZOS)
            # Padding prevents cutting out antenna tips or tree leaves.
            img=ImageOps.expand(img,border=5,fill=(0,0,0,0))
            img.save(OUT/target,"WEBP",quality=87,method=5,exact=True)
            report[target]={"estado":"ok","source":url,"input_size":list(source.size),
                            "output_size":list(img.size),"bytes":(OUT/target).stat().st_size,
                            "transparent_pixels":sum(1 for v in img.getchannel("A").getdata() if v==0)}
            break
        except Exception as exc:
            errors.append(url+": "+str(exc)[:180])
    else:
        report[target]={"estado":"error","errores":errors}
(OUT/"fuentes.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("RESULTADO_ASSETS",json.dumps(report,ensure_ascii=False),flush=True)
if any(v["estado"]!="ok" for v in report.values()):
    raise SystemExit("No se publican recursos incompletos; ver errores del reporte")
