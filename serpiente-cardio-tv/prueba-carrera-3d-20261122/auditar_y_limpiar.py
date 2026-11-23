"""Auditoría conservadora de GLB articulados. Nunca sobrescribe originales."""
from pathlib import Path
from collections import deque
import bpy, bmesh, json, sys, math

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "candidatos-limpios"
OUT.mkdir(exist_ok=True)
report = {}

def bbox_object(obj):
    from mathutils import Vector
    return [[round(x, 4) for x in obj.matrix_world @ Vector(c)] for c in obj.bound_box]

def summarize_islands(mesh):
    # Geometría visible, agrupada por conectividad (sin modificar el original).
    neighbors = [[] for _ in mesh.vertices]
    for edge in mesh.edges:
        a,b = edge.vertices
        neighbors[a].append(b)
        neighbors[b].append(a)
    seen = bytearray(len(mesh.vertices))
    counts = []
    small = []
    for i in range(len(mesh.vertices)):
        if seen[i]:
            continue
        seen[i] = 1
        todo = [i]
        comp = []
        while todo:
            v = todo.pop()
            comp.append(v)
            for n in neighbors[v]:
                if not seen[n]:
                    seen[n] = 1
                    todo.append(n)
        counts.append(len(comp))
        if len(comp) < 15 and len(small)<30:
            coords = [mesh.vertices[v].co for v in comp]
            c = sum(coords,coords[0]*0) / len(coords)
            small.append({"vertices":len(comp),"centro_local":[round(float(z),3) for z in c]})
    return {"total":len(counts),"mas_grandes":sorted(counts,reverse=True)[:15],
            "grupos_pequenos_ejemplo":small}

def cleanup_mesh(mesh):
    # Solo elimina aristas/vértices SIN CARAS y corrige normales.
    # NO suprime mechones de pelo ni manos basándose en un criterio arbitrario.
    bm=bmesh.new()
    bm.from_mesh(mesh)
    antes={"verts":len(bm.verts),"faces":len(bm.faces)}
    libres=[v for v in bm.verts if len(v.link_faces)==0]
    if libres:
        bmesh.ops.delete(bm,geom=libres,context='VERTS')
    if bm.faces:
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return {**antes,"vertices_sin_caras_eliminados":len(libres)}

for name in ("goku","vegeta"):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    filepath=ROOT/(name+".glb")
    bpy.ops.import_scene.gltf(filepath=str(filepath))
    objects=list(bpy.context.scene.objects)
    meshes=[obj for obj in objects if obj.type=="MESH"]
    rigs=[obj for obj in objects if obj.type=="ARMATURE"]
    details=[]
    for obj in meshes:
        details.append({"objeto":obj.name,
            "vertices":len(obj.data.vertices),"caras":len(obj.data.polygons),
            "islas":summarize_islands(obj.data),
            "bounds_world":bbox_object(obj),
            "armature":next((m.object.name for m in obj.modifiers
                               if m.type=='ARMATURE' and m.object),None)})
    actions=[{"nombre":a.name,"frames":[float(a.frame_range[0]),float(a.frame_range[1])]}
             for a in bpy.data.actions if a.users>0]
    item={"mallas":details,
          "huesos":{o.name:len(o.data.bones) for o in rigs},
          "animaciones":actions}
    item["correcciones"]={obj.name:cleanup_mesh(obj.data) for obj in meshes}
    bpy.ops.export_scene.gltf(filepath=str(OUT/(name+".glb")),
            export_format='GLB',export_animations=True,export_skins=True)
    item["candidato_bytes"]=(OUT/(name+".glb")).stat().st_size
    report[name]=item

(OUT/"auditoria.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("AUDITORIA_LISTA")
for name,p in report.items():
    print(name,"mallas",len(p["mallas"]),"huesos",p["huesos"],
          "clips",p["animaciones"],"candidato",p["candidato_bytes"])
