"""TRELLIS real, multivista, SIN pagos ni reemplazar Voltito anterior.

Fuente del modelo: trellis-community/TRELLIS (Space ZeroGPU). Esta prueba
usa un servicio remoto comunitario con cuotas, no garantiza disponibilidad.
No crear un GLB ficticio si la generación remota falla.
"""
from pathlib import Path
from time import time
import json, shutil, struct, traceback
from PIL import Image
from gradio_client import Client, handle_file
from urllib.request import Request, urlopen

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=ROOT/"experimentos/voltito-hunyuan-4v-20261118"
NEW=ROOT/"experimentos/voltito-3d-10-vistas-20261118"
DEST=HERE/"voltito-trellis-multivista-candidato.glb"
SOURCE_VIEWS=[
    ("000","frente",OLD),
    ("045","045",NEW),
    ("090","derecha",OLD),
    ("135","135",NEW),
    ("180","espalda",OLD),
    ("225","225",NEW),
    ("270","izquierda",OLD),
    ("315","315",NEW),
]
def prepare():
    inputs=HERE/"entradas"
    inputs.mkdir(exist_ok=True)
    generated=[]
    report=[]
    for n,name,folder in SOURCE_VIEWS:
        original=folder/f"voltito-{name}.png"
        with Image.open(original) as im:
            im.load()
            if im.mode!="RGBA" or im.size!=(768,1024) or im.getchannel("A").getextrema()!=(0,255):
                raise ValueError("Imagen fuente alterada/incompleta "+str(original))
            a=im.getchannel("A")
            bb=a.point(lambda p: 255 if p>12 else 0).getbbox()
            if bb is None:raise ValueError("Silueta inexistente "+name)
            cropped=im.crop(bb)
            cropped.thumbnail((464,464),Image.Resampling.LANCZOS)
            canvas=Image.new("RGBA",(512,512),(0,0,0,0))
            canvas.alpha_composite(cropped,((512-cropped.width)//2,(512-cropped.height)//2))
            path=inputs/f"voltito-{n}.png"
            canvas.save(path,"PNG",optimize=True)
            generated.append(path)
            report.append({"angle":n,"original":str(original.relative_to(ROOT)),"size":list(im.size),"prepared":str(path.relative_to(ROOT))})
            print("INPUT",n,cropped.size,path.stat().st_size,flush=True)
    return generated,report

def find_glb(result):
    candidates=[]
    def walk(x):
        if isinstance(x,(list,tuple)):
            for a in x:walk(a)
        elif isinstance(x,dict):
            for name,value in x.items():
                if name in ("data","blob"):continue
                walk(value)
        elif isinstance(x,(str,Path)):
            p=Path(str(x))
            if p.suffix.lower()==".glb" and p.is_file():
                candidates.append(p)
    walk(result)
    return candidates

def validate(path):
    raw=path.read_bytes()
    if len(raw)<100000 or raw[:4]!=b"glTF":
        raise RuntimeError("TRELLIS devolvió un archivo no GLB o vacío")
    magic,version,total=struct.unpack_from("<4sII",raw)
    if version!=2 or total!=len(raw):
        raise RuntimeError("GLB de TRELLIS corrupto/incompleto")
    import trimesh
    scene=trimesh.load(str(path),force="scene",process=False)
    mesh=scene.dump(concatenate=True)
    dims=mesh.bounds[1]-mesh.bounds[0]
    if len(mesh.faces)<3000 or min(dims)<.0001:
        raise RuntimeError("TRELLIS produjo malla sin volumen suficiente")
    return {"bytes":len(raw),"faces":len(mesh.faces),"vertices":len(mesh.vertices),"dims":dims.tolist()}

def main():
    paths,report=prepare()
    started=time()
    space="trellis-community/TRELLIS"
    print("CONECTAR",space,flush=True)
    client=Client(space,verbose=False)
    try:
        # El tab "Multiple Images" de Gradio configura una variable gr.State.
        # Sin elegir el tab, el servicio corre modalidad de UNA sola imagen.
        for endpoint in ("/start_session","/lambda_1"):
            try:
                value=client.predict(api_name=endpoint)
                print("SESSION",endpoint,str(value)[:100],flush=True)
            except Exception as e:
                print("SESSION_ENDPOINT_NOT_READY",endpoint,type(e).__name__,str(e)[:300],flush=True)
        gallery=[{"image":handle_file(str(p)),"caption":None} for p in paths]
        print("ENVIANDO 8 VISTAS, no texto ni fotografías en carrusel",flush=True)
        job=client.submit(
            image=None,
            multiimages=gallery,
            seed=27,
            ss_guidance_strength=7.5,
            ss_sampling_steps=12,
            slat_guidance_strength=3.0,
            slat_sampling_steps=12,
            multiimage_algo="multidiffusion",
            mesh_simplify=0.95,
            texture_size=1024,
            api_name="/generate_and_extract_glb",
        )
        print("TRELLIS_EN_COLA",flush=True)
        output=job.result(timeout=620)
        print("TRELLIS_RESPUESTA",type(output).__name__,str(output)[:1600],flush=True)
        matches=find_glb(output)
        if not matches:
            raise RuntimeError("El servicio no devolvió un archivo .glb descargable. No se publicará resultado ficticio.")
        candidate=max(matches,key=lambda p:p.stat().st_size)
        params=validate(candidate)
        shutil.copyfile(candidate,DEST)
        result={"status":"candidato_3d_real_sin_aprobacion_visual","motor":"trellis-community/TRELLIS",
                "metodo":"8 vistas horizontales alimentadas a la red multivista, no proyección 2D",
                "vista_superior_inferior":"Conservadas como referencia pero no enviadas a esta generación 8 horizontales",
                "seed":27,"modo":"multidiffusion","duracion_segundos":round(time()-started),
                "modelo":{"filename":DEST.name,**params},"inputs":report}
        (HERE/"resultado.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
        print("TRELLIS_EXITO_MALLA_3D",json.dumps(params),flush=True)
    except Exception as e:
        print("TRELLIS_NO_GENERADO:",type(e).__name__,str(e)[:1500],flush=True)
        raise

if __name__=="__main__":
    main()
