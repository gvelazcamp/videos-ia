"""Mejorar la coloración del MODELO TRIDIMENSIONAL REAL Hunyuan existente
con las 10 vistas aportadas por Gonzalo.

Importante: Hunyuan3D-2mv sólo admite 4 entradas simultáneas para generar forma.
Aquí preservamos su malla real, proyectamos los otros ángulos sobre superficies
3D e incluimos arriba/abajo de forma conservadora. No utilizamos planos 2D.
El GLB resultante es un candidato NUEVO: no modifica el anterior aprobado.
"""
from pathlib import Path
import json,struct
import numpy as np
from PIL import Image
import trimesh
from scipy.ndimage import map_coordinates,distance_transform_edt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/"experimentos/voltito-hunyuan-4v-20261118"
INPUT=BASE/"voltito-4v-colores.glb"
OUTPUT=HERE/"voltito-10-vistas-mejorado.glb"
VIEWS=[
    ("frente",0,BASE,0.95),
    ("045",45,HERE,1.10),
    ("derecha",90,BASE,0.95),
    ("135",135,HERE,1.10),
    ("espalda",180,BASE,0.95),
    ("225",225,HERE,1.10),
    ("izquierda",270,BASE,0.95),
    ("315",315,HERE,1.10),
    ("superior",None,HERE,0.20),
    ("inferior",None,HERE,0.13),
]
if not INPUT.is_file():raise RuntimeError("No existe el GLB 3D real anterior")
loaded=trimesh.load(str(INPUT),force="scene",process=False)
mesh=loaded.dump(concatenate=True)
verts=np.asarray(mesh.vertices,dtype=np.float64)
normals=np.asarray(mesh.vertex_normals,dtype=np.float64)
normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-9)
if len(verts)<20000 or len(mesh.faces)<50000:
    raise RuntimeError("La geometría base 3D está incompleta")
vertex_old=np.asarray(mesh.visual.vertex_colors)
if len(vertex_old)!=len(verts):raise RuntimeError("La malla fuente no tiene colores válidos")
# Colores de glTF vienen como bytes lineales, por eso se combinan linealmente.
base_rgb=np.asarray(vertex_old[:,:3],dtype=np.float64)/255.
color_sum=np.zeros_like(base_rgb)
weights=np.zeros((len(verts),),dtype=np.float64)
ymin,ymax=float(verts[:,1].min()),float(verts[:,1].max())
report={}
for name,angle,folder,importance in VIEWS:
    path=folder/f"voltito-{name}.png"
    with Image.open(path) as im:
        im.load()
        if im.mode!="RGBA" or im.size!=(768,1024) or im.getchannel("A").getextrema()!=(0,255):
            raise ValueError("PNG distinto al aprobado: "+str(path))
        rgba=np.array(im,dtype=np.uint8)
    alpha=rgba[:,:,3]
    opaque=alpha>75
    if np.count_nonzero(opaque)<10000:raise ValueError("Máscara demasiado pequeña "+name)
    yy,xx=np.nonzero(opaque)
    xlo,xhi=float(xx.min()),float(xx.max())
    ylo,yhi=float(yy.min()),float(yy.max())
    if angle is None:
        # Sólo colorear caras hacia arriba/abajo, sin deformar el modelo.
        d=np.array([0.,1. if name=="superior" else -1.,0.])
        horiz=verts[:,0]
        # Superior: cabeza/cara en parte inferior de lámina (+Z -> abajo)
        # Inferior: boca hacia arriba y cola abajo (+Z -> arriba)
        vertproj=verts[:,2] if name=="superior" else -verts[:,2]
        side=(normals@d).clip(0,1)
        direction_weight=np.maximum(side,0)**10
        direction_weight[side<.87]=0
        importance=min(importance,.16)
    else:
        a=np.deg2rad(angle)
        d=np.array([np.sin(a),0.,np.cos(a)])
        horizontal=np.array([np.cos(a),0.,-np.sin(a)])
        horiz=verts@horizontal
        vertproj=verts[:,1]
        side=(normals@d).clip(0,1)
        direction_weight=side**7
        direction_weight[side<.12]=0
    ulo,uhi=np.percentile(horiz,[.05,99.95])
    vlo,vhi=np.percentile(vertproj,[.05,99.95])
    u=xlo+np.clip((horiz-ulo)/max(uhi-ulo,1e-7),0,1)*(xhi-xlo)
    if angle is None:
        v=ylo+np.clip((vertproj-vlo)/max(vhi-vlo,1e-7),0,1)*(yhi-ylo)
    else:
        v=ylo+np.clip((vhi-vertproj)/max(vhi-vlo,1e-7),0,1)*(yhi-ylo)
    coords=np.vstack([v,u])
    # Color nearest-opaque avoids reading white/transparent halos.
    idx=distance_transform_edt(~opaque,return_indices=True)[1]
    opaque_rgb=rgba[:,:,:3][idx[0],idx[1]]
    alpha_sample=map_coordinates(alpha.astype(np.float32),coords,order=1,mode="constant",cval=0)/255.
    rgb_sample=np.stack([
        map_coordinates(opaque_rgb[:,:,ch].astype(np.float32),coords,order=1,mode="nearest")
        for ch in range(3)
    ],axis=1)/255.
    # Convert actual PNG sRGB to glTF linear-space vertex colors.
    linear=np.where(rgb_sample<=.04045,rgb_sample/12.92,((rgb_sample+.055)/1.055)**2.4)
    confidence=importance*direction_weight*np.maximum(alpha_sample,0)**3
    # No color contribution from outside the actual silhouette.
    confidence[alpha_sample<.38]=0
    color_sum+=linear*confidence[:,None]
    weights+=confidence
    report[name]={
        "angle":angle if angle is not None else name,
        "image":str(path.relative_to(ROOT)),
        "pixels":int(np.count_nonzero(opaque)),
        "affected_vertices":int(np.count_nonzero(confidence>.012)),
        "weight_mean":round(float(confidence.mean()),5)
    }
    print("PROYECTADA VISTA",name,"vértices",report[name]["affected_vertices"],flush=True)
# Retener un 35% de color previo para evitar zonas sin información/mezclas falsas.
new_rgb=(base_rgb*.36+color_sum)/(weights[:,None]+.36)
new_rgb=np.clip(new_rgb,0,1)
new_rgba=np.c_[np.uint8(np.round(new_rgb*255)),np.full(len(verts),255,dtype=np.uint8)]
mesh.visual=trimesh.visual.ColorVisuals(mesh=mesh,vertex_colors=new_rgba)
mesh.export(str(OUTPUT),file_type="glb")
raw=OUTPUT.read_bytes()
if raw[:4]!=b"glTF" or len(raw)<2_000_000:raise RuntimeError("GLB de diez vistas inválido")
_,version,declared=struct.unpack_from("<4sII",raw,0)
if version!=2 or declared!=len(raw):raise RuntimeError("GLB incompleto")
report_data={"estado":"candidato experimental (sin aprobación visual)",
 "geometria":"Malla Hunyuan3D-2mv de las 4 vistas cardinales previamente reconstruidas",
 "mejora":"Proyección de colores sobre la geometría real desde 8 azimuts y superior/inferior",
 "no_es":"NO reconstrucción nativa de diez imágenes en el generador Hunyuan",
 "verts":len(verts),"faces":len(mesh.faces),"size_bytes":len(raw),"views":report}
(HERE/"diagnostico-10-vistas.json").write_text(json.dumps(report_data,indent=2,ensure_ascii=False))
print("GLB REAL MEJORADO CON DIEZ VISTAS",OUTPUT,len(raw),"bytes",flush=True)
