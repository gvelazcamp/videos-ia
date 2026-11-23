"""Inspect exact joints, weights, mesh and frame bounds of Goku and Vegeta. Read-only inputs."""
from pathlib import Path
import bpy, json, math
from mathutils import Vector

root=Path(__file__).resolve().parent
report={}

def desc(obj):
    world=obj.matrix_world
    corners=[world @ Vector(v) for v in obj.bound_box]
    return {"min":[round(min(c[i] for c in corners),4) for i in range(3)],
            "max":[round(max(c[i] for c in corners),4) for i in range(3)],
            "location":[round(v,4) for v in obj.location],
            "rotation":[round(v,4) for v in obj.rotation_euler],
            "scale":[round(v,4) for v in obj.scale]}

for name in ("goku","vegeta"):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(root/(name+".glb")))
    arms=[o for o in bpy.context.scene.objects if o.type=='ARMATURE']
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    arm=arms[0]
    bones={}
    for b in arm.data.bones:
        bones[b.name]={"head_world":[round(x,4) for x in arm.matrix_world @ b.head_local],
                       "tail_world":[round(x,4) for x in arm.matrix_world @ b.tail_local],
                       "parent":b.parent.name if b.parent else None,
                       "length":round(b.length,5)}
    meshes_info=[]
    for obj in meshes:
        weight_occ={}
        d=desc(obj)
        for group in obj.vertex_groups:
            accum=0.
            count=0
            for v in obj.data.vertices:
                for w in v.groups:
                    if w.group==group.index:
                        count+=1
                        accum+=w.weight
            weight_occ[group.name]={"count":count,"weight_sum":round(accum,2)}
        mat=obj.data.materials[0] if len(obj.data.materials)>0 else None
        meshes_info.append({"name":obj.name,"bound":d,"vertices":len(obj.data.vertices),"faces":len(obj.data.polygons),"group_stats":weight_occ,"material":mat.name if mat else None})
    frames={}
    for frame in (1,5,9,13,17,21,25,29,33):
        bpy.context.scene.frame_set(frame)
        dep=bpy.context.evaluated_depsgraph_get()
        moving={}
        for o in meshes:
            if not o.vertex_groups: continue
            ob=o.evaluated_get(dep)
            mesh=ob.to_mesh()
            xx=[(ob.matrix_world @ v.co) for v in mesh.vertices]
            moving[o.name]={"min":[round(min(v[i] for v in xx),4) for i in range(3)],
                            "max":[round(max(v[i] for v in xx),4) for i in range(3)]}
            ob.to_mesh_clear()
        frames[frame]=moving
    report[name]={"bones":bones,"meshes":meshes_info,"frames":frames,
                  "armature_transforms":{"location":list(arm.location),"rotation":list(arm.rotation_euler),"scale":list(arm.scale)}}

out=root/"diagnostico-rig.json"
out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print("DIAGNOSTICO_RIG_OK",str(out))
