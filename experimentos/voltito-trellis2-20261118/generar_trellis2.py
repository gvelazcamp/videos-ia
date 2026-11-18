"""PRUEBA GRATUITA TRELLIS.2: modelo 3D genuino de Voltito desde UNA vista.
No alterar originales / generar una imagen falsa ni sustituir el TRELLIS 1.
El Space oficial acepta UNA imagen; las demás vistas quedan para evaluación.
"""
from pathlib import Path
import json,struct,shutil,traceback
from PIL import Image
from gradio_client import Client,handle_file
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/"experimentos/voltito-3d-10-vistas-20261118/voltito-045.png"
OUTPUT=HERE/"voltito-trellis2-candidato.glb"
STATUS=HERE/"resultado.json"
SPACES=["microsoft/TRELLIS.2","henrybit/TRELLIS-2-4B-Demo"]
SEED=27
def log(*x):print(*x,flush=True)
def prepare():
    with Image.open(SOURCE) as im:
        im.load()
        if im.mode!="RGBA" or im.getchannel("A").getextrema()!=(0,255):
            raise ValueError("Vista 45 grados de Voltito no tiene alfa real")
        b=im.getchannel("A").point(lambda x:255 if x>16 else 0).getbbox()
        if b is None:raise ValueError("Referencia vacia")
        # El objeto queda completo, centrado, sin estirarlo ni reinterpretarlo.
        crop=im.crop(b)
        crop.thumbnail((704,704),Image.Resampling.LANCZOS)
        canvas=Image.new("RGBA",(768,768),(0,0,0,0))
        canvas.alpha_composite(crop,((768-crop.width)//2,(768-crop.height)//2))
        destination=HERE/"entrada-voltito-45.png"
        canvas.save(destination,"PNG",optimize=True)
        log("VISTA_PREPARADA",str(destination.relative_to(ROOT)),crop.size,destination.stat().st_size)
        return destination
def find_glb(payload):
    candidates=[]
    def rec(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in ("blob","data"):continue
                rec(v)
        elif isinstance(x,(list,tuple)):
            for v in x:rec(v)
        elif isinstance(x,(str,Path)):
            p=Path(str(x))
            if p.suffix.lower()==".glb" and p.is_file():candidates.append(p)
    rec(payload)
    if not candidates:raise ValueError("La API no devolvio GLB descargable")
    return max(candidates,key=lambda p:p.stat().st_size)
def check_glb(path):
    raw=path.read_bytes()
    if len(raw)<100000 or raw[:4]!=b"glTF":raise ValueError("GLB vacio o invalido")
    magic,version,total=struct.unpack_from("<4sII",raw)
    if version!=2 or total!=len(raw):raise ValueError("GLB corrupto/incompleto")
    import trimesh
    mesh=trimesh.load(str(path),force="scene",process=False).dump(concatenate=True)
    dims=mesh.bounds[1]-mesh.bounds[0]
    if len(mesh.faces)<3000 or min(dims)<.0001:raise ValueError("Malla 3D sin caras/profundidad")
    return {"bytes":len(raw),"faces":int(len(mesh.faces)),"vertices":int(len(mesh.vertices)),"dimensions":[float(x) for x in dims]}
def main():
    input_file=prepare()
    record={"estado":"prueba_en_curso","fecha_utc":datetime.now(timezone.utc).isoformat(),
        "fuente":str(SOURCE.relative_to(ROOT)),
        "modelo":"TRELLIS.2-4B",
        "vistas_entregadas_al_modelo":1,
        "vistas_disponibles_para_comparacion":10,
        "aclaracion":"La API oficial de TRELLIS.2 admite una sola vista. No fingir reconstruccion de diez vistas ni exportar falso GLB.",
        "pruebas":[]}
    for space in SPACES:
        trial={"space":space}
        record["pruebas"].append(trial)
        log("ESPACIO",space)
        try:
            client=Client(space,verbose=False)
            try:client.predict(api_name="/start_session")
            except Exception as e:log("AVISO_SESION",type(e).__name__,str(e)[:200])
            # El pipeline oficial llama a /image_to_3d y devuelve HTML de
            # previsualizacion; mantiene el estado de latentes en Gradio.
            params={
                "image":handle_file(str(input_file)), "seed":SEED,
                "resolution":"512",
                "ss_guidance_strength":7.5,
                "ss_guidance_rescale":0.7,
                "ss_sampling_steps":12,
                "ss_rescale_t":5.0,
                "shape_slat_guidance_strength":7.5,
                "shape_slat_guidance_rescale":0.5,
                "shape_slat_sampling_steps":12,
                "shape_slat_rescale_t":3.0,
                "tex_slat_guidance_strength":1.0,
                "tex_slat_guidance_rescale":0.0,
                "tex_slat_sampling_steps":12,
                "tex_slat_rescale_t":3.0,
            }
            log("GENERANDO_TRELLIS2",space,"512 voxel")
            job=client.submit(**params,api_name="/image_to_3d")
            preview=job.result(timeout=630)
            trial["preview_type"]=type(preview).__name__
            log("PREVIEW_GENERADO",type(preview).__name__,len(str(preview)))
            # La extracción usa el MISMO cliente/sesion Gradio.
            job2=client.submit(decimation_target=100000,texture_size=1024,api_name="/extract_glb")
            extracted=job2.result(timeout=250)
            log("EXTRACCION",type(extracted).__name__,str(extracted)[:350])
            candidate=find_glb(extracted)
            geometry=check_glb(candidate)
            shutil.copy2(candidate,OUTPUT)
            trial.update({"estado":"exito","geometria":geometry})
            record.update({"estado":"candidato_3d_real_sin_aprobacion_visual","space":space,"geometry":geometry,"output":OUTPUT.name})
            STATUS.write_text(json.dumps(record,ensure_ascii=False,indent=2))
            log("TRELLIS2_GLB_REAL_VERIFICADO",geometry)
            return
        except Exception as exc:
            trial.update({"estado":"fallo","error":type(exc).__name__+": "+str(exc)[:1100]})
            log("INTENTO_FALLIDO",space,trial["error"])
            continue
    record["estado"]="sin_generacion_3d"
    STATUS.write_text(json.dumps(record,ensure_ascii=False,indent=2))
    log("SIN_GLB_TRELLIS2_NINGUN_SERVICIO")
if __name__=="__main__":main()
