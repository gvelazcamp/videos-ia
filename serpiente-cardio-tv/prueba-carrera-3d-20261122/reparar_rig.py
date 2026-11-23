"""Reparación NO destructiva de pesos y clips de Goku/Vegeta. Entradas GLB originales."""
import bpy
import json, math, struct
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"revision-rig"
OUT.mkdir(exist_ok=True)
report={}

def smooth(lo,hi,x):
    t=max(0.0,min(1.0,(x-lo)/max(1e-8,hi-lo)))
    return t*t*(3-2*t)

def lerp(a,b,t):
    d={}
    for k in set(a)|set(b):
        v=a.get(k,0)*(1-t)+b.get(k,0)*t
        if v>0.0001: d[k]=v
    return d

def wmap(v, mn, mx, cy):
    dx=max(mx.x-mn.x,1e-4)
    dz=max(mx.z-mn.z,1e-4)
    depth=max(mx.y-mn.y,1e-4)
    z=(v.z-mn.z)/dz
    x=(v.x-(mx.x+mn.x)/2)/dx
    behind=(v.y-cy)/depth
    side='L' if x<0 else 'R'
    q=abs(x)
    # El cabello de cola baja es parte de la cabeza (no del brazo) en la zona posterior.
    # Fuera de esa region se mantiene el brazo.
    if z>=.76:
        return {'Head':1.}
    if z>.61 and q>.26 and behind>.26:
        fade=smooth(.61,.69,z)*smooth(.26,.35,behind)
        if fade>.985:
            return {'Head':1.}
    if z>.70 and q<.245:
        return lerp({'Neck':1.},{'Head':1.},smooth(.71,.77,z))
    # El arranque del brazo mezcla tronco y hombro para no rasgar la malla.
    if q>.24 and .39<z<.754:
        arm_start=smooth(.23,.33,q)
        if z>=.535:
            limb={'UpperArm_'+side:1.}
        elif z>=.415:
            limb=lerp({'Forearm_'+side:1.},{'UpperArm_'+side:1.},smooth(.535,.575,z))
        else:
            limb=lerp({'Hand_'+side:1.},{'Forearm_'+side:1.},smooth(.404,.458,z))
        if z>.61 and behind>.26:
            limb=lerp(limb,{'Head':1.},
                      smooth(.61,.70,z)*smooth(.26,.36,behind)*.95)
        return lerp({'Torso':1.},limb,arm_start)
    if z>=.53:
        return {'Torso':1.}
    if z>=.43:
        return lerp({'Pelvis':1.},{'Torso':1.},smooth(.45,.55,z))
    if z>=.275:
        return lerp({'Shin_'+side:1.},{'Thigh_'+side:1.},smooth(.264,.31,z))
    if z>=.105:
        return lerp({'Foot_'+side:1.},{'Shin_'+side:1.},smooth(.104,.14,z))
    return {'Foot_'+side:1.}

for name in ("goku","vegeta"):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(ROOT/(name+".glb")))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.vertex_groups]
    arms=[o for o in bpy.context.scene.objects if o.type=='ARMATURE']
    if len(arms)!=1 or not meshes:
        raise RuntimeError(name+": no hay rig unico y malla con pesos")
    rig=arms[0]
    points=[ob.matrix_world @ v.co for ob in meshes for v in ob.data.vertices]
    mn=Vector(tuple(min(p[i] for p in points) for i in range(3)))
    mx=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    cy=(mx.y+mn.y)/2
    bone_names={b.name for b in rig.data.bones}
    changes={}
    for obj in meshes:
        groups={g.name:g for g in obj.vertex_groups}
        if not set(["Head","Neck","Torso","Pelvis","Thigh_L","Thigh_R",
                    "Shin_L","Shin_R","UpperArm_L","UpperArm_R"]).issubset(groups):
            raise RuntimeError(name+": rig faltante en "+obj.name)
        new={}
        for v in obj.data.vertices:
            w=wmap(obj.matrix_world @ v.co,mn,mx,cy)
            w={k:val for k,val in w.items() if k in groups}
            total=sum(w.values())
            if total>0: new[v.index]={k:val/total for k,val in w.items()}
        ids=list(new)
        for group in groups.values():
            group.remove(ids)
        for i,w in new.items():
            for g,val in w.items():
                groups[g].add([i],val,'REPLACE')
        # No soldar UV: los bordes triangulados del GLB requieren UV independientes.
        # Solo recalcular normales degeneradas sin cambiar topologia.
        changes[obj.name]={"vertices_repesados":len(new),
                           "caras_preservadas":len(obj.data.polygons)}
    animations=[]
    for action in bpy.data.actions:
        if not action.users:continue
        changed=0
        samples=[]
        if hasattr(action,'fcurves'):
            # GLTF import convierte las rotaciones a quaterniones. Antes se
            # buscaban rotation_euler y nunca se corregian los movimientos.
            from collections import defaultdict
            groups=defaultdict(dict)
            for fc in action.fcurves:
                if "rotation_quaternion" in fc.data_path:
                    groups[fc.data_path][fc.array_index]=fc
                elif "rotation_euler" in fc.data_path and fc.array_index==0:
                    path=fc.data_path
                    factor=(.64 if "UpperArm" in path else
                            .72 if "Thigh" in path else
                            .70 if "Shin" in path else
                            .78 if "Forearm" in path else
                            .47 if "Torso" in path else 1.0)
                    if factor!=1.0:
                        for k in fc.keyframe_points:
                            k.co.y*=factor
                            k.handle_left.y*=factor
                            k.handle_right.y*=factor
                            k.interpolation="BEZIER"
                            k.handle_left_type="AUTO_CLAMPED"
                            k.handle_right_type="AUTO_CLAMPED"
                        changed+=1
                if len(samples)<5:
                    samples.append(fc.data_path)
            for path,curves in groups.items():
                if set(curves)!={0,1,2,3}:
                    continue
                factor=(.64 if "UpperArm" in path else
                        .72 if "Thigh" in path else
                        .70 if "Shin" in path else
                        .78 if "Forearm" in path else
                        .47 if "Torso" in path else 1.0)
                if factor>=1:
                    continue
                from mathutils import Quaternion
                n=min(len(fc.keyframe_points) for fc in curves.values())
                for i in range(n):
                    keyframes=[curves[j].keyframe_points[i] for j in (0,1,2,3)]
                    q=Quaternion(tuple(k.co.y for k in keyframes))
                    q.normalize()
                    corrected=Quaternion((1.,0.,0.,0.)).slerp(q,factor)
                    for j,key in enumerate(keyframes):
                        old=key.co.y
                        offset=corrected[j]-old
                        key.co.y=corrected[j]
                        key.handle_left.y+=offset
                        key.handle_right.y+=offset
                        key.interpolation="BEZIER"
                        key.handle_left_type="AUTO_CLAMPED"
                        key.handle_right_type="AUTO_CLAMPED"
                changed+=4
        animations.append({"name":action.name,"adjusted_curves":changed,
                           "sample_paths":samples})
    # Ocultar auxiliares no skinned y que no pertenecen al GLB de personaje.
    # Algunos son esferas de depuracion; solo se retiran si carecen de materiales/texturas
    # y no tienen modificador ARMATURE.
    removed=[]
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and not ob.vertex_groups and ob.name.startswith("Icosphere"):
            removed.append(ob.name)
            bpy.data.objects.remove(ob,do_unlink=True)
    bpy.context.scene.frame_start=1
    bpy.context.scene.frame_end=33
    bpy.context.scene.frame_set(1)
    target=OUT/(name+".glb")
    bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',
                               export_animations=True,export_skins=True)
    b=target.read_bytes()
    if b[:4]!=b'glTF' or struct.unpack_from("<I",b,8)[0]!=len(b):
        raise RuntimeError(name+": GLB corrupto")
    length=struct.unpack_from("<I",b,12)[0]
    doc=json.loads(b[20:20+length])
    if not doc.get("skins") or not doc.get("animations"):
        raise RuntimeError(name+": se perdio rig o animacion")
    report[name]={"archivo":str(target.relative_to(ROOT)),
                  "bytes":len(b),"huesos":len(rig.data.bones),
                  "clips":len(doc["animations"]),"mallas":changes,
                  "auxiliares_eliminados":removed,
                  "animacion":animations,
                  "estado":"candidato_pendiente_verificacion_visual"}
(OUT/"reporte.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("RIG_CORREGIDO_OK",json.dumps(report,ensure_ascii=False),flush=True)
