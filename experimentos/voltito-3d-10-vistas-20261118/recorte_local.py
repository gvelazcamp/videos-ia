"""Recorte local gratuito y reproducible tras bloqueo de descarga de Remove.bg web.
No crea otra imagen; genera alfa auténtico sobre los 6 recortes suministrados.
El sujeto amarillo/turquesa sobre blanco se segmenta por saturación + relleno
de silueta. No se eliminan zonas crema interiores ni se recorta la cola.
"""
from pathlib import Path
from PIL import Image,ImageFilter
import cv2
import numpy as np
ROOT=Path(__file__).resolve().parent
for name in ("045","135","225","315","superior","inferior"):
    source=ROOT/f"origen-{name}.png"
    with Image.open(source) as im:
        im.load()
        original=im.convert("RGB")
    ar=np.asarray(original,dtype=np.float32)/255.
    vmax=ar.max(axis=2)
    vmin=ar.min(axis=2)
    saturation=(vmax-vmin)/np.maximum(vmax,.01)
    subject=((saturation>.125)&(vmax>.14)) | ((vmax<.5)&(saturation>.08))
    mask=cv2.morphologyEx(subject.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    count,labels,stats,_=cv2.connectedComponentsWithStats(mask,connectivity=8)
    if count<2:raise RuntimeError("No se detectó Voltito en vista "+name)
    largest=np.argmax(stats[1:,cv2.CC_STAT_AREA])+1
    mask=np.uint8(labels==largest)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    # Las zonas crema interiores, ojos y sombras internas no son fondo.
    flood=mask.copy()
    cv2.floodFill(flood,None,(0,0),1)
    enclosed=np.uint8(flood==0)
    mask=np.maximum(mask,enclosed)
    a=Image.fromarray(mask*255,"L").filter(ImageFilter.GaussianBlur(.7))
    rgba=original.convert("RGBA")
    rgba.putalpha(a)
    if a.getextrema()!=(0,255) or mask.mean()<.04 or mask.mean()>.7:
        raise ValueError(f"Máscara inesperada en {name}: {mask.mean():.3f}")
    if max(int(mask[0,0]),int(mask[0,-1]),int(mask[-1,0]),int(mask[-1,-1]))>0:
        raise RuntimeError("Fondo no eliminado en esquinas: "+name)
    target=ROOT/f"removebg-{name}.png"
    rgba.save(target,"PNG",optimize=True)
    print("ALFA LOCAL GRATUITO",name,original.size,"cobertura",round(mask.mean(),3),flush=True)
print("Seis fondos eliminados sin usar API ni créditos",flush=True)
