#!/usr/bin/env python3
"""Repara SOLO la placa del nombre de Claude TRELLIS.
Construye letras 3D vectoriales en geometría negra, no como textura
(impide que se inviertan por el mapeo UV o se superpongan dos etiquetas).
Crea un candidato NUEVO y conserva intactos los GLB previos.
"""
from functools import reduce
from pathlib import Path
import hashlib
import json

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import Polygon, box
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
import trimesh

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "claude-trellis-candidato.glb"
OUTPUT = HERE / "claude-trellis-nombre-legible.glb"
REPORT = HERE / "resultado-nombre-legible.json"

def triangles_from_shape(shape):
    triangles = shapely.constrained_delaunay_triangles(shape)
    if len(triangles.geoms) == 0:
        raise ValueError("La geometría de la placa o las letras está vacía")
    points, faces = [], []
    for tri in triangles.geoms:
        xy = np.array(tri.exterior.coords[:3], dtype=np.float64)
        if xy.shape != (3, 2):
            raise ValueError("Triángulo de geometría inválido")
        start = len(points)
        points.extend([[x, y, 0.] for x, y in xy])
        faces.append([start, start+1, start+2])
    return np.array(points,dtype=float), np.array(faces,dtype=np.int64)

def follow_surface(vertices, surface, z_top, amount, label):
    origins = np.array(vertices, copy=True)
    origins[:, 2] = z_top
    dirs = np.tile(np.array([[0.,0.,-1.]],dtype=float),(len(vertices),1))
    hits, ray_idx, _ = surface.ray.intersects_location(
        ray_origins=origins, ray_directions=dirs, multiple_hits=True
    )
    front = {}
    for hit, idx in zip(hits,ray_idx):
        idx = int(idx)
        front[idx] = max(front.get(idx,-np.inf), float(hit[2]))
    coverage = len(front)/len(vertices)
    if coverage < .985:
        raise ValueError(f"{label}: parte de la placa cae fuera del cuerpo ({coverage:.1%})")
    for i, v in enumerate(vertices):
        v[2] = front[i] + amount
    return coverage

def white_plate(cx,cy,width,height,original,top):
    # Geometría real con extremos redondeados; no usa transparencia de PNG.
    r = height * .28
    polygon = box(-width/2+r,-height/2+r,width/2-r,height/2-r).buffer(
        r, quad_segs=18
    )
    polygon = affinity.translate(polygon,xoff=cx,yoff=cy)
    vertices, faces = triangles_from_shape(polygon)
    # Más puntos para acompañar curvatura del abdomen, no atravesarlo.
    for _ in range(2):
        vertices,faces = trimesh.remesh.subdivide(vertices,faces)
    covered=follow_surface(vertices,original,top,.0045,"Placa blanca")
    mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
    mesh.visual.vertex_colors=np.tile(np.array([252,250,253,255],dtype=np.uint8),(len(vertices),1))
    return mesh,covered

def text_as_solid_geometry(cx,cy,width,height,original,top):
    # TextPath entrega las letras reales, legibles de izquierda a derecha.
    path=TextPath((0,0),"Claude",size=1.,
                  prop=FontProperties(family="DejaVu Sans",weight="bold"))
    outlines=[]
    for contour in path.to_polygons(closed_only=True):
        poly=Polygon(contour)
        if poly.is_valid and poly.area>1e-10:
            outlines.append(poly)
    if not outlines:
        raise ValueError("No se pudieron formar letras de Claude")
    shapes=reduce(lambda a,b:a.symmetric_difference(b),outlines)
    minx,miny,maxx,maxy=shapes.bounds
    tx=width*.825
    ty=height*.56
    shapes=affinity.scale(shapes,xfact=tx/(maxx-minx),
                         yfact=ty/(maxy-miny),origin=(minx,miny))
    shapes=affinity.translate(shapes,xoff=cx-tx/2-minx,yoff=cy-ty/2-miny)
    verts, faces = triangles_from_shape(shapes)
    coverage=follow_surface(verts,original,top,.0095,"Letras Claude")
    text=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
    text.visual.vertex_colors=np.tile(np.array([10,10,14,255],dtype=np.uint8),(len(verts),1))
    if not (text.bounds[0,0]<cx<text.bounds[1,0]):
        raise ValueError("El nombre no quedó centrado")
    return text,coverage,len(outlines)

def main():
    if not SOURCE.is_file() or SOURCE.stat().st_size<100_000:
        raise FileNotFoundError("Falta el GLB auténtico de Claude TRELLIS")
    if OUTPUT.exists():
        raise FileExistsError("No reemplazar sin revisar el candidato anterior")
    original=trimesh.load(str(SOURCE),force="scene",process=False)
    solid=original.dump(concatenate=True)
    bounds=solid.bounds
    dim=bounds[1]-bounds[0]
    if len(solid.faces)<3000 or not (.8<dim[1]<1.2):
        raise ValueError("El archivo no coincide con el TRELLIS original")
    cx=float((bounds[0,0]+bounds[1,0])/2)
    cy=float(bounds[0,1]+dim[1]*.326)
    width=float(dim[1]*.238)
    height=float(dim[1]*.096)
    top=float(bounds[1,2]+dim[2]+1)
    plaque,plate_cov=white_plate(cx,cy,width,height,solid,top)
    letters,text_cov,contours=text_as_solid_geometry(
        cx,cy,width,height,solid,top)
    original_count=len(original.geometry)
    original.add_geometry(plaque, geom_name="Claude_placa_blanca_v2",
                          node_name="Claude_placa_blanca_v2")
    original.add_geometry(letters,geom_name="Claude_letras_negras_legibles",
                          node_name="Claude_letras_negras_legibles")
    original.export(str(OUTPUT))
    check=trimesh.load(str(OUTPUT),force="scene",process=False)
    if len(check.geometry)!=original_count+2:
        raise ValueError("El nuevo GLB no tiene las dos geometrías correctas")
    if OUTPUT.read_bytes()[:4]!=b"glTF":
        raise ValueError("Cabecera GLB inválida")
    # El número de caras original permanece igual: únicamente se agregan dos objetos.
    report={
        "estado":"correccion_placa_3d_de_claude_generada",
        "fuente":SOURCE.name,"salida":OUTPUT.name,
        "cambio":"Placa sólida blanca y letras negras Claude como triángulos 3D, sin texturas UV",
        "texto_exacto":"Claude","orientacion":"letras en +X (izquierda a derecha)",
        "posicion":{"x":cx,"y":cy},
        "tamano_placa":[width,height],
        "cobertura_placa":plate_cov,
        "cobertura_letras":text_cov,
        "contornos_texto":contours,
        "caras_originales":int(len(solid.faces)),
        "caras_nuevo_total":int(len(check.dump(concatenate=True).faces)),
        "geometrias_originales":original_count,
        "geometrias_finales":len(check.geometry),
        "sha256_original":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "sha256_corregido":hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "bytes":OUTPUT.stat().st_size
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("EXITO_CLAUDE_NOMBRE_GEOMETRIA",json.dumps(report,ensure_ascii=False),flush=True)

if __name__=="__main__":
    main()
