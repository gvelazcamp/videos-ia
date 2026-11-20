"""Reconstruccion volumetrica MULTIVISTA de 8 imagenes autenticas.
ALTERNATIVA SIN TRELLIS mientras la cuota gratuita ZeroGPU esta agotada.
Produce malla 3D real con colores de las imagenes, no billboards. Blender hace el rig despues.
"""
import math, sys
from pathlib import Path
import numpy as np
import cv2
import trimesh
from PIL import Image
from skimage import measure

args=sys.argv[1:]
if len(args)!=2:raise SystemExit("uso: visualhull.py CARPETA_8_VISTAS SALIDA.glb")
root=Path(args[0]).resolve(); out=Path(args[1]).resolve()
out.parent.mkdir(parents=True,exist_ok=True)
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
imgs=[np.array(Image.open(root/n).convert("RGBA")) for n in names]
assert all(x.shape==(512,512,4) for x in imgs),"Vistas invalidas"
alpha=[cv2.morphologyEx(im[:,:,3],cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))>70 for im in imgs]
angles=[i*math.pi/4 for i in range(8)]
NX=112;NY=112;NZ=196
xs=np.linspace(-1,1,NX,dtype="float32")
ys=np.linspace(-1,1,NY,dtype="float32")
zs=np.linspace(0,3,NZ,dtype="float32")
x,y,z=np.meshgrid(xs,ys,zs,indexing="ij")
score=np.zeros(x.shape,dtype=np.uint8)
for j,a in enumerate(angles):
 u=np.rint(256+220*(x*np.cos(a)+y*np.sin(a))).astype("int32")
 v=np.rint(482-452*z/3).astype("int32")
 valid=(u>=0)&(u<512)&(v>=0)&(v<512)
 projection=np.zeros(score.shape,dtype=bool)
 projection[valid]=alpha[j][v[valid],u[valid]]
 score+=projection.astype(np.uint8)
vol=(score>=7).astype("uint8")
print("VOLUMEN",int(vol.sum()),flush=True)
if vol.sum()<1000:raise RuntimeError("No hay volumen multivista utilizable")
vol=cv2.morphologyEx(vol.reshape(NX*NY,NZ),cv2.MORPH_CLOSE,np.ones((2,2),np.uint8)).reshape(NX,NY,NZ)
verts,faces,normals,_=measure.marching_cubes(vol.astype("float32"),0.5,spacing=(2/(NX-1),2/(NY-1),3/(NZ-1)))
verts[:,0]-=1;verts[:,1]-=1
colors=np.full((len(verts),4),255,dtype="uint8")
pixels=[]; visibles=[]
for j,a in enumerate(angles):
 u=np.rint(256+220*(verts[:,0]*np.cos(a)+verts[:,1]*np.sin(a))).astype("int32")
 v=np.rint(482-452*verts[:,2]/3).astype("int32")
 valid=(u>=0)&(u<512)&(v>=0)&(v<512)
 sampled=np.full((len(verts),4),255,dtype="uint8")
 sampled[valid]=imgs[j][v[valid],u[valid]]
 pixels.append(sampled)
 visibles.append(valid&(sampled[:,3]>70))
view_scores=np.stack([normals[:,0]*np.sin(a)-normals[:,1]*np.cos(a) for a in angles],axis=1)
view_scores[~np.stack(visibles,axis=1)]=-999
best=view_scores.argmax(axis=1)
for j in range(8):
 chosen=best==j
 colors[chosen,:3]=pixels[j][chosen,:3]
colors[:,3]=255
mesh=trimesh.Trimesh(vertices=verts,faces=faces,process=False,vertex_colors=colors)
mesh.export(str(out))
if out.stat().st_size<100000:raise RuntimeError("No se genero GLB volumetrico")
print("MALLA_REAL_MULTIVISTA",out,len(verts),len(faces),out.stat().st_size,flush=True)
