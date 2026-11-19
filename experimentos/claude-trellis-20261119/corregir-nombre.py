#!/usr/bin/env python3
"""Corrige exclusivamente el nombre ilegible en GLB de TRELLIS de Claude.
La geometría y texturas originales se conservan. Genera archivo separado.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"claude-trellis-candidato.glb"
TARGET=ROOT/"claude-trellis-nombre-corregido.glb"
META=ROOT/"resultado-correccion.json"

def main():
    if not SOURCE.is_file() or SOURCE.stat().st_size<100_000:
        raise FileNotFoundError("Falta el GLB original de Claude")
    scene=trimesh.load(str(SOURCE),force="scene",process=False)
    original_geoms=len(scene.geometry)
    whole=scene.dump(concatenate=True)
    bounds=whole.bounds
    widths=bounds[1]-bounds[0]
    if not 0.8<widths[1]<1.2 or len(whole.faces)<3000:
        raise ValueError("La malla original no coincide con el modelo TRELLIS")
    cx=float((bounds[0,0]+bounds[1,0])/2)
    cy=float(bounds[0,1]+widths[1]*0.335)
    plate_w=float(widths[1]*0.205)
    plate_h=float(widths[1]*0.075)
    nx,ny=28,10
    vertices=[]
    uv=[]
    for j in range(ny+1):
        for i in range(nx+1):
            xx=cx+plate_w*(i/nx-0.5)
            yy=cy+plate_h*(j/ny-0.5)
            vertices.append([xx,yy,0])
            uv.append([i/nx,1-j/ny])
    verts=np.array(vertices,dtype=float)
    ray_origins=verts.copy()
    ray_origins[:,2]=float(bounds[1,2]+widths[2]+1)
    ray_directions=np.repeat(np.array([[0.,0.,-1.]]),len(verts),axis=0)
    locations,indices,_=whole.ray.intersects_location(ray_origins,ray_directions,multiple_hits=True)
    front_by_ray={}
    for point,idx in zip(locations,indices):
        idx=int(idx)
        front_by_ray[idx]=max(front_by_ray.get(idx,-np.inf),float(point[2]))
    center_idx=(ny//2)*(nx+1)+nx//2
    center_z=front_by_ray.get(center_idx)
    if center_z is None or not np.isfinite(center_z):
        raise ValueError("No se encontró la superficie frontal del torso de Claude")
    coverage=len(front_by_ray)/len(verts)
    if coverage<0.90:
        raise ValueError(f"Placa parcialmente fuera del cuerpo: cobertura {coverage:.1%}")
    for i in range(len(verts)):
        verts[i,2]=front_by_ray.get(i,center_z)+0.004
    faces=[]
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i
            b,c,d=a+1,a+nx+2,a+nx+1
            faces.extend([[a,b,c],[a,c,d]])
    W,H=1024,360
    texture=Image.new("RGBA",(W,H),(0,0,0,0))
    draw=ImageDraw.Draw(texture)
    draw.rounded_rectangle((7,7,W-8,H-8),radius=90,
            fill=(252,250,253,255),outline=(210,207,213,255),width=9)
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not Path(font_path).exists():
        raise FileNotFoundError("No hay tipografía legible en el entorno")
    font=ImageFont.truetype(font_path,225)
    draw.text((W/2,H/2+2),"Claude",font=font,
              fill=(15,15,18,255),anchor="mm",stroke_width=0)
    decal=trimesh.Trimesh(vertices=verts,faces=np.array(faces,dtype=np.int64),process=False)
    decal.visual=trimesh.visual.texture.TextureVisuals(
        uv=np.array(uv,dtype=float),image=texture)
    scene.add_geometry(decal,geom_name="Claude_nombre_corregido",node_name="Claude_nombre_corregido")
    scene.export(str(TARGET))
    validated=trimesh.load(str(TARGET),force="scene",process=False)
    if len(validated.geometry)<original_geoms+1 or TARGET.stat().st_size<=100_000:
        raise ValueError("No se obtuvo un GLB válido con la placa")
    with TARGET.open("rb") as fp:
        if fp.read(4)!=b"glTF":
            raise ValueError("Cabecera GLB inválida")
    metadata={
        "estado":"candidato con placa corregida, sin alterar modelo base",
        "origen":SOURCE.name,"salida":TARGET.name,
        "correccion":"Una única placa 3D frontal con texto exacto Claude",
        "texto":"Claude","posicion":{"x":cx,"y":cy,"z":center_z},
        "ancho_m":plate_w,"alto_m":plate_h,"cobertura_raycast":coverage,
        "geometrias_originales":original_geoms,
        "geometrias_finales":len(validated.geometry),
        "original_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "modificado_sha256":hashlib.sha256(TARGET.read_bytes()).hexdigest(),
        "bytes":TARGET.stat().st_size
    }
    META.write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding="utf-8")
    print("EXITO_NOMBRE_CLAUDE_GLTF",json.dumps(metadata,ensure_ascii=False),flush=True)

if __name__=="__main__":
    main()
