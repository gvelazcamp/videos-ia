"""Proyección experimental de las 4 imágenes de Voltito sobre la malla Hunyuan 3D.
Se transfieren colores de los PNG originales, NO se crean nuevas poses ni se
modifica el fichero original. La geometría ya generada puede girarse 360°.
El resultado es CANDIDATO, sujeto a comparación visual humana.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image
import trimesh
from scipy.ndimage import distance_transform_edt, map_coordinates
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
IMAGES=HERE
INPUT=HERE/"voltito-4v-sin-texturas.glb"
OUTPUT=HERE/"voltito-4v-colores.glb"
if not INPUT.is_file():raise RuntimeError("Falta malla 3D auténtica, no hacer sustitución")
scene=trimesh.load(str(INPUT),force="scene",process=False)
mesh=scene.dump(concatenate=True)
v=np.asarray(mesh.vertices,dtype=np.float64)
normals=np.asarray(mesh.vertex_normals,dtype=np.float64)
if len(v)<20000 or mesh.faces.shape[0]<50000:
    raise RuntimeError("La geometría generada está incompleta")
normlen=np.linalg.norm(normals,axis=1)
normals=normals/np.maximum(normlen[:,None],1e-8)
mid=(v.min(axis=0)+v.max(axis=0))/2
# GLB de frente en +Z, perfil izquierdo en -X, espalda -Z, derecho +X.
viewinfo=[
 ("frente",np.array([0,0,1]),0,+1),
 ("izquierda",np.array([-1,0,0]),2,-1),
 ("espalda",np.array([0,0,-1]),0,-1),
 ("derecha",np.array([1,0,0]),2,+1)
]
maxV,minV=v.max(axis=0),v.min(axis=0)
weighted=np.zeros((len(v),3),dtype=np.float64)
total=np.zeros(len(v),dtype=np.float64)
report={}
for name,direction,axis,sign in viewinfo:
    with Image.open(IMAGES/f"voltito-{name}.png") as im:
        im.load()
        rgba=np.asarray(im.convert("RGBA"),dtype=np.uint8)
    h,w=rgba.shape[:2]
    # Crop transparent canvas; keep exact pixel content and aspect.
    alpha=rgba[:,:,3]
    ys,xs=np.where(alpha>15)
    if len(xs)<10000:raise ValueError("Imagen PNG vacía: "+name)
    xmin,xmax=int(xs.min()),int(xs.max())
    ymin,ymax=int(ys.min()),int(ys.max())
    # Ortho projection: front u = x, back u = -x,
    # right u = z, left u = -z. Vertical world Y points upwards.
    worldaxis=v[:,axis]
    if sign<0:
        uvx=(maxV[axis]-worldaxis)/max(1e-8,maxV[axis]-minV[axis])
    else:
        uvx=(worldaxis-minV[axis])/max(1e-8,maxV[axis]-minV[axis])
    u=xmin+uvx*(xmax-xmin)
    yfrac=(maxV[1]-v[:,1])/max(1e-8,maxV[1]-minV[1])
    yy=ymin+yfrac*(ymax-ymin)
    xy=np.vstack([np.clip(yy,0,h-1),np.clip(u,0,w-1)])
    # Preserve all fur/eye/cheek texture pixels, but eliminate white/black
    # halos by sampling the nearest opaque pixel at transparent boundaries.
    mask=alpha>90
    if not mask.any():raise RuntimeError("No visible color in "+name)
    dist,idx=distance_transform_edt(~mask,return_indices=True)
    image=rgba[:,:,:3][idx[0],idx[1]].astype(np.float32)
    rgb=np.stack([map_coordinates(image[:,:,ch],xy,order=1,mode="nearest") for ch in range(3)],axis=1)
    sampled_alpha=map_coordinates(alpha.astype(np.float32),xy,order=1,mode="constant",cval=0)/255.
    outward=np.clip(normals@direction,0,1)
    # Extra priority to the closest surface-facing camera, to retain
    # cheeks, irises, ears and tail rather than blending them to grey.
    confidence=np.maximum(outward,.0)**5
    confidence*=np.maximum(.07,sampled_alpha)**1.1
    confidence[outward<.075]=0
    weighted+=rgb*confidence[:,None]
    total+=confidence
    report[name]={"pixels":len(xs),"mean_weight":float(confidence.mean()),"active_vertices":int((confidence>.04).sum())}
base=np.array([247.,192.,66.])
rgbout=np.where(total[:,None]>.0001,weighted/np.maximum(total[:,None],1e-4),base)
rgbout=np.uint8(np.clip(rgbout,0,255))
# glTF vertex colors are LINEAR, while the PNG reference pixels are sRGB.
# Writing sRGB bytes directly would double-apply gamma and wash out Voltito.
srgb=rgbout.astype(np.float32)/255.0
linear=np.where(srgb<=0.04045,srgb/12.92,((srgb+0.055)/1.055)**2.4)
rgbout=np.uint8(np.clip(np.round(linear*255.0),0,255))
# Explicit RGBA vertex color for portable glTF 2.0.
mesh.visual=trimesh.visual.ColorVisuals(mesh=mesh,vertex_colors=np.c_[rgbout,np.full(len(v),255,dtype=np.uint8)])
mesh.export(str(OUTPUT),file_type="glb")
out=OUTPUT.read_bytes()
if not out.startswith(b"glTF") or len(out)<1_000_000:
    raise RuntimeError("GLB colorido inválido")
(HERE/"proyeccion-diagnostico.json").write_text(json.dumps({
 "status":"candidato_vistas_unificadas_sin_aprobacion_visual",
 "vertices":len(v),"faces":len(mesh.faces),"color_range":rgbout.min(axis=0).tolist(),
 "input_views":report,"bytes":len(out)
},indent=2,ensure_ascii=False))
print("CANDIDATO 3D CON COLORES DE FOTOS:",len(v),"vértices",len(mesh.faces),"caras",len(out),"bytes",flush=True)
