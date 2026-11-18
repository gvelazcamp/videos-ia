"""Preparar las 6 vistas NUEVAS de Voltito: 4 diagonales + superior/inferior.
Usar las cuatro vistas ya aprobadas como fuente de las cardinales.
NO generar ni redibujar imágenes y NO alterar el modelo vigente.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
from PIL import Image,ImageFilter
import sys,json
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SHEETS={
 "diagonales":{
   "url":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/6474b2d7-93ff-4b87-bc30-52efcfb02e58.jpg",
   "boxes":{
     "045":(65,108,490,653), "135":(567,108,992,653),
     "225":(65,777,490,1322), "315":(567,777,992,1322)
   }
 },
 "verticales":{
   "url":"https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/b27a4edb-9b93-4730-9db1-1908fddb312a.jpg",
   "boxes":{"superior":(65,70,1000,586),"inferior":(65,782,1000,1310)}
 }
}
REQUIRED=["045","135","225","315","superior","inferior"]
CARDINAL=ROOT/"experimentos/voltito-hunyuan-4v-20261118"
OUTPUT=(768,1024)
def preparar():
    for sheet,settings in SHEETS.items():
        req=Request(settings["url"],headers={"User-Agent":"Mozilla/5.0"})
        with urlopen(req,timeout=60) as response:
            raw=response.read(8_000_000)
        with Image.open(BytesIO(raw)) as im:
            im.load()
            if im.size!=(1103,1536):raise RuntimeError(f"Lámina no coincide: {sheet} {im.size}")
            im.convert("RGB").save(HERE/f"fuente-{sheet}.jpg",quality=95,optimize=True)
            for name,box in settings["boxes"].items():
                out=im.crop(box).convert("RGB")
                if out.width<400 or out.height<500:raise RuntimeError(f"Vista demasiado pequeña: {name}")
                out.save(HERE/f"origen-{name}.png",optimize=True)
                print("RECIBIDO",name,out.size,flush=True)

def finalizar():
    info={}
    for name in REQUIRED:
        with Image.open(HERE/f"origen-{name}.png") as original: rgb=original.convert("RGB")
        with Image.open(HERE/f"removebg-{name}.png") as removed:
            removed.load(); alpha=removed.convert("RGBA").getchannel("A")
        if alpha.getextrema()!=(0,255):raise RuntimeError("Remove.bg sin alfa: "+name)
        alpha=alpha.resize(rgb.size,Image.Resampling.LANCZOS)
        alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.5))
        aa=np.array(alpha)
        coverage=float(np.mean(aa>130))
        if not .04<coverage<.83:raise RuntimeError(f"Remove.bg máscara sospechosa {name}: {coverage:.3f}")
        corners=[aa[0,0],aa[0,-1],aa[-1,0],aa[-1,-1]]
        if max(corners)>12:raise RuntimeError("Remove.bg dejó borde del marco: "+name)
        rgba=rgb.convert("RGBA")
        rgba.putalpha(alpha)
        # Mantener RGB real de la ilustración y suavizar solamente borde anti-alias
        data=np.array(rgba,dtype=np.uint8)
        a=np.maximum(data[:,:,3].astype(np.float32)/255,.13)
        edge=(data[:,:,3]>0)&(data[:,:,3]<230)
        src=data[:,:,:3].astype(np.float32)
        dewhite=np.clip((src-250*(1-a[:,:,None]))/a[:,:,None],0,255)
        src[edge]=dewhite[edge]
        data[:,:,:3]=src.astype(np.uint8)
        rgba=Image.fromarray(data,"RGBA")
        # Los 4 ángulos comparten escala con las vistas cardinales originales.
        # Las vistas cenital/nadir poseen geometría proyectada distinta y
        # se mantienen completas y sin deformación.
        if name in ("superior","inferior"):
            size=(700,round(rgb.height*700/rgb.width))
        else:
            size=(round(rgb.width*930/rgb.height),930)
        size=tuple(int(n) for n in size)
        if size[0]>OUTPUT[0]-10: size=(OUTPUT[0]-10,round(size[1]*(OUTPUT[0]-10)/size[0]))
        resized=rgba.resize(size,Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",OUTPUT,(0,0,0,0))
        x=(OUTPUT[0]-size[0])//2
        y=(OUTPUT[1]-size[1])//2 if name in ("superior","inferior") else 42
        canvas.alpha_composite(resized,(x,y))
        dest=HERE/f"voltito-{name}.png"
        canvas.save(dest,optimize=True)
        with Image.open(dest) as verify:
            assert verify.size==OUTPUT and verify.getchannel("A").getextrema()==(0,255)
        info[name]={"size":list(OUTPUT),"alpha_coverage":round(coverage,3),"bytes":dest.stat().st_size}
        print("PNG TRANSPARENTE",name,info[name],flush=True)
    for name in ("frente","derecha","espalda","izquierda"):
        p=CARDINAL/f"voltito-{name}.png"
        with Image.open(p) as image:
            assert image.mode=="RGBA" and image.size==OUTPUT and image.getchannel("A").getextrema()==(0,255)
        info[name]={"source":str(p.relative_to(ROOT)),"no_modificado":True}
    (HERE/"manifest-vistas.json").write_text(json.dumps({
        "personaje":"Voltito",
        "metodo":"4 vistas cardinales existentes + 6 nuevos recortes con Remove.bg",
        "vistas":info,
        "nota":"Hunyuan3D-2mv admite cuatro entradas de forma por ejecución; las diagonales y verticales aportan referencias para proyección de color y evaluación, no son seis entradas directas al modelo."
    },ensure_ascii=False,indent=2))
    print("LISTAS DIEZ REFERENCIAS REALES",flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("preparar","finalizar"):raise SystemExit("Uso: preparar_10.py preparar|finalizar")
    globals()[sys.argv[1]]()
