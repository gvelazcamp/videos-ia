"""Prueba GRATIS de reconstrucción 3D REAL, desde 4 fotos de Voltito.
No utiliza Three.js para inventar mallas. Utiliza la demo pública Hunyuan3D-2mv
y guarda candidato GLB sólo si la respuesta contiene una malla glTF válida.
No se publican resultados de aspecto no revisado como 'aprobados'.
"""
from pathlib import Path
from gradio_client import Client, handle_file
from PIL import Image
import json, shutil, struct, sys
from urllib.request import Request, urlopen
from urllib.parse import quote
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/"experimentos/voltito-360-fiel-nuevas-vistas-20261118"
SOURCES={
    "frente":"voltito-frente.png",
    "espalda":"voltito-espalda.png",
    "izquierda":"voltito-izquierda.png",
    "derecha":"voltito-derecha.png",
}
WORK=HERE/"input"
WORK.mkdir(parents=True,exist_ok=True)
for kind,name in SOURCES.items():
    with Image.open(SOURCE/name) as image:
        image.load()
        if image.mode!="RGBA" or image.getchannel("A").getextrema()!=(0,255):
            raise RuntimeError(f"PNG fuente sin transparencia real: {kind}")
        bbox=image.getchannel("A").getbbox()
        if not bbox:raise RuntimeError(f"PNG vacío: {kind}")
        crop=image.crop(bbox)
        crop.thumbnail((700,900),Image.Resampling.LANCZOS)
        dest=WORK/f"{kind}.png"
        crop.save(dest,"PNG",optimize=True)
        print("Referencia",kind,crop.size,"OK",flush=True)
print("Conectando a demostración PÚBLICA de Hunyuan3D-2mv. No hay compra ni uso de API paga.",flush=True)
client=Client("tencent/Hunyuan3D-2mv",verbose=False)
try:
    result=client.predict(
        caption=None,
        image=None,
        mv_image_front=handle_file(str(WORK/"frente.png")),
        mv_image_back=handle_file(str(WORK/"espalda.png")),
        mv_image_left=handle_file(str(WORK/"izquierda.png")),
        mv_image_right=handle_file(str(WORK/"derecha.png")),
        steps=5,
        guidance_scale=5.0,
        seed=1234,
        octree_resolution=256,
        check_box_rembg=False,
        num_chunks=8000,
        randomize_seed=False,
        api_name="/shape_generation",
    )
except Exception as e:
    print("HUNYUAN_NO_DISPONIBLE:",type(e).__name__,str(e)[:2800],flush=True)
    raise
print("Respuesta multivista",str(result)[:1700],flush=True)
if not isinstance(result,(tuple,list)) or len(result)<2:
    raise RuntimeError("Respuesta inválida del generador 3D")
mesh_white=result[0]
mesh_textured=None
def read_from_space(data):
    # Gradio returns gr.update(value="/tmp/gradio/…/white_mesh.glb")
    # not a local downloaded file. Fetch the exact artifact over the public
    # Space file endpoint: no credentials, no paid API, no replacement model.
    if isinstance(data,dict):
        data=data.get("path") or data.get("value") or data.get("url")
    if not data:
        raise RuntimeError("Servicio no publicó ruta GLB")
    p=Path(str(data))
    if p.is_file():
        return p.read_bytes()
    service=str(getattr(client,"src","https://tencent-hunyuan3d-2mv.hf.space")).rstrip("/")
    remote_path=str(data)
    if not remote_path.startswith("/tmp/gradio/") or not remote_path.endswith(".glb"):
        raise ValueError("Ruta del fichero de salida inesperada: "+remote_path[:250])
    paths=[
        service+"/gradio_api/file="+quote(remote_path,safe="/"),
        service+"/file="+quote(remote_path,safe="/"),
    ]
    for url in paths:
        try:
            with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=75) as resp:
                raw=resp.read(60_000_001)
            if raw[:4]==b"glTF" and len(raw)<60_000_000:
                print("Malla descargada del endpoint publico:",len(raw),flush=True)
                return raw
            print("Fichero remoto invalido",url,raw[:80],flush=True)
        except Exception as exc:
            print("Ruta fallida:",type(exc).__name__,str(exc)[:250],flush=True)
    raise RuntimeError("Malla generada pero la descarga publica no esta disponible")

for name,file in (("sin-texturas",mesh_white),):
    raw=read_from_space(file)
    if len(raw)<40000 or raw[:4]!=b"glTF":raise RuntimeError(f"Malla GLB inválida: {name}")
    magic,version,total=struct.unpack_from("<4sII",raw)
    if version!=2 or total!=len(raw):raise RuntimeError(f"GLB incompleto: {name}")
    output=HERE/f"candidato-voltito-{name}.glb"
    output.write_bytes(raw)
    print("MALLA_3D_REAL",name,output,len(raw),flush=True)
(HERE/"estado.json").write_text(json.dumps({"resultado":"solo_geometria_sin_texturas_y_sin_aprobacion_visual","base":"cuatro_png_originales","modelo":"Hunyuan3D-2mv","malla":"GLB auténtico no verificado por similitud visual"},ensure_ascii=False,indent=2))
