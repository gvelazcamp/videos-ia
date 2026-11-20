#!/usr/bin/env python3
"""Rig real sobre GLB del goblin navideno generado por TRELLIS. No declara identidad verificada.
Se ejecuta SOLAMENTE sobre resultado nuevo de Guardia Azul y no toca modelos existentes.
Uso: blender -b --python <este_script> -- <trellis_input.glb> <output_dir>
"""
import bpy, math, sys, json, struct
from pathlib import Path
from mathutils import Vector

args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if len(args)!=2: raise SystemExit("Se requieren GLB origen y carpeta de salida")
source=Path(args[0]).resolve()
out=Path(args[1]).resolve(); out.mkdir(parents=True,exist_ok=True)
if source.suffix.lower()!=".glb" or not source.is_file():raise SystemExit("Falta entrada GLB real de TRELLIS")
if "duende-navideno-articulado-20261120" not in source.parts:raise SystemExit("Se esperaba carpeta exclusiva del personaje")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[ob for ob in bpy.data.objects if ob.type=="MESH"]
if not meshes:raise RuntimeError("TRELLIS no contiene malla real")
bpy.context.view_layer.update()
points=[ob.matrix_world @ v.co for ob in meshes for v in ob.data.vertices]
mn=Vector([min(p[i] for p in points) for i in range(3)])
mx=Vector([max(p[i] for p in points) for i in range(3)])
height=mx.z-mn.z
if height<=0.005:raise RuntimeError("Malla TRELLIS sin altura válida")
cx=(mn.x+mx.x)/2;cy=(mn.y+mx.y)/2;w=mx.x-mn.x
def J(x,z):return (cx+x*w, cy, mn.z+z*height)
# Blender Z-up. Huesos con jerarquia real y geometria interpolada por vertex groups.
BONES=[
 ("Root",None,J(0,.01),J(0,.08)),
 ("Cadera","Root",J(0,.43),J(0,.54)),
 ("Columna","Cadera",J(0,.54),J(0,.66)),
 ("Pecho","Columna",J(0,.66),J(0,.75)),
 ("Cuello","Pecho",J(0,.75),J(0,.82)),
 ("Cabeza","Cuello",J(0,.82),J(0,.96)),
 ("Hombro_izquierdo","Pecho",J(-.27,.74),J(-.40,.64)),
 ("Codo_izquierdo","Hombro_izquierdo",J(-.40,.64),J(-.46,.51)),
 ("Muneca_izquierda","Codo_izquierdo",J(-.46,.51),J(-.45,.44)),
 ("Hombro_derecho","Pecho",J(.27,.74),J(.40,.64)),
 ("Codo_derecho","Hombro_derecho",J(.40,.64),J(.46,.51)),
 ("Muneca_derecha","Codo_derecho",J(.46,.51),J(.45,.44)),
 ("Cadera_izquierda","Cadera",J(-.16,.45),J(-.18,.35)),
 ("Rodilla_izquierda","Cadera_izquierda",J(-.18,.35),J(-.19,.27)),
 ("Tobillo_izquierdo","Rodilla_izquierda",J(-.19,.27),J(-.18,.08)),
 ("Cadera_derecha","Cadera",J(.16,.45),J(.18,.35)),
 ("Rodilla_derecha","Cadera_derecha",J(.18,.35),J(.19,.27)),
 ("Tobillo_derecho","Rodilla_derecha",J(.19,.27),J(.18,.08)),
]
bpy.ops.object.armature_add(enter_editmode=False, location=(0,0,0))
rig=bpy.context.object;rig.name="Duende_Navideno_Trellis_Rig"
rig.data.name="Esqueleto_Duende_Navideno"
bpy.ops.object.mode_set(mode="EDIT")
# Delete armature default single bone; rebuild from stable names.
for bone in list(rig.data.edit_bones):rig.data.edit_bones.remove(bone)
for name,parent,head,tail in BONES:
 bone=rig.data.edit_bones.new(name)
 bone.head=Vector(head); bone.tail=Vector(tail)
 if parent:bone.parent=rig.data.edit_bones[parent]
 bone.use_connect=False
bpy.ops.object.mode_set(mode="OBJECT")

def influence(pos):
 x=(pos.x-cx)/max(w,.01);z=(pos.z-mn.z)/height
 lado="izquierda" if x<0 else "derecha"
 lado_masculino="izquierdo" if x<0 else "derecho"
 if z>.79:return "Cabeza"
 if z>.73:return "Cuello" if abs(x)<.15 else "Hombro_"+lado_masculino
 if .51<=z<=.73 and abs(x)>.27:
  return ("Hombro_" if z>.63 else "Codo_")+lado_masculino
 if .38<=z<.52 and abs(x)>.28:return "Muneca_"+lado
 if z<.45:
  if z<.12:return "Tobillo_"+lado_masculino
  if z<.27:return "Rodilla_"+lado
  return "Cadera_"+lado
 if z>.63:return "Pecho"
 if z>.53:return "Columna"
 return "Cadera"

for ob in meshes:
 # El parent original se retira conservando transformaciones del mundo
 world=ob.matrix_world.copy()
 ob.parent=None
 ob.matrix_world=world
 groups={name:ob.vertex_groups.new(name=name) for name,_,_,_ in BONES}
 for v in ob.data.vertices:
  coord=ob.matrix_world @ v.co
  groups[influence(coord)].add([v.index],1.0,"REPLACE")
 ob.parent=rig
 ob.matrix_parent_inverse=rig.matrix_world.inverted()
 mod=ob.modifiers.new("Rig duende navideno","ARMATURE")
 mod.object=rig
# Clips básicos, no confundir con animación validada cuadro por cuadro.
sequence={
 "Reposo":{},
 "Caminar":{"Hombro_izquierdo":[.0,.35,.0,-.35,.0],"Hombro_derecho":[.0,-.35,.0,.35,.0],"Cadera_izquierda":[.0,-.30,.0,.30,.0],"Cadera_derecha":[.0,.30,.0,-.30,.0]},
 "Correr":{"Hombro_izquierdo":[0,.65,0,-.65,0],"Hombro_derecho":[0,-.65,0,.65,0],"Cadera_izquierda":[0,-.55,0,.55,0],"Cadera_derecha":[0,.55,0,-.55,0],"Rodilla_izquierda":[0,.35,0,.15,0],"Rodilla_derecha":[0,.15,0,.35,0]},
 "Girar_cabeza":{"Cabeza":[0,.4,0,-.4,0]},
 "Saludar":{"Hombro_derecho":[0,-.65,-.8,-.65,0],"Codo_derecho":[0,-.5,-.5,-.5,0]},
 "Agacharse":{"Cadera_izquierda":[0,.35,.5,.3,0],"Cadera_derecha":[0,.35,.5,.3,0],"Pecho":[0,.22,.42,.18,0],"Cabeza":[0,-.13,-.22,-.10,0]},
 "Cargar_Poder_Violeta":{"Hombro_izquierdo":[0,-.65,-.9,-1.10,0],"Hombro_derecho":[0,-.65,-.9,-1.10,0],"Codo_izquierdo":[0,-.42,-.7,-.70,0],"Codo_derecho":[0,-.42,-.7,-.70,0]},
 "Ataque":{"Hombro_izquierdo":[0,-.65,-1.25,-.30,0],"Hombro_derecho":[0,-.65,-1.25,-.30,0],"Pecho":[0,.12,.48,.15,0]},
}
rig.animation_data_create()
for name,channels in sequence.items():
 action=bpy.data.actions.new(name=name)
 action.use_fake_user=True
 rig.animation_data.action=action
 for bone_name,values in channels.items():
  pb=rig.pose.bones.get(bone_name)
  if not pb:raise RuntimeError("Hueso no disponible: "+bone_name)
  pb.rotation_mode="XYZ"
  for frame,value in zip((1,8,15,22,29),values):
   pb.rotation_euler=(value,0,0) if bone_name!="Cabeza" else (0,value,0)
   pb.keyframe_insert(data_path="rotation_euler",frame=frame,group=bone_name)
  pb.rotation_euler=(0,0,0)
 track=rig.animation_data.nla_tracks.new();track.name=name
 strip=track.strips.new(name,1,action)
 strip.action_frame_end=29
rig.animation_data.action=None
bpy.context.scene.frame_set(1)
# Excluir todo excepto estos meshes + armature, conservar PBR y UV de TRELLIS.
bpy.ops.object.select_all(action="DESELECT")
for ob in meshes+[rig]: ob.hide_set(False);ob.select_set(True)
bpy.context.view_layer.objects.active=rig
path=out/"duende_navideno_3d_articulado.glb"
bpy.ops.export_scene.gltf(filepath=str(path),export_format="GLB",use_selection=True,export_animations=True,export_nla_strips=True,export_skins=True)
if not path.is_file() or path.stat().st_size<100000:raise RuntimeError("GLB articulado ausente o demasiado pequeño")
raw=path.read_bytes()
if raw[:4]!=b"glTF":raise RuntimeError("No es GLB binario")
chunk=struct.unpack_from("<I",raw,12)[0]
data=json.loads(raw[20:20+chunk].decode("utf-8"))
if not data.get("skins"):raise RuntimeError("GLB final no posee skin real")
if not data.get("animations"):raise RuntimeError("GLB final no exportó animaciones")
bpy.ops.wm.save_as_mainfile(filepath=str(out/"duende_navideno_3d_articulado.blend"))
report={"estado":"candidato_reconstruido_y_riggeado_sin_aprobacion_visual","origen":str(source),"metodo_reconstruccion":("TRELLIS" if "trellis-3d" in source.parts else "Visual hull multivista, NO TRELLIS"),"salida":str(path),"mallas_importadas":len(meshes),"esqueleto":len(BONES),"clips_blender":list(sequence),"clips_glb":len(data["animations"]),"altura_modelo":height,"advertencias":["Asignación automática de pesos por posición; revisar deformación de articulaciones","La consistencia de vistas laterales no garantiza parecido con la foto original","No reemplazar modelos previos sin aprobación"]}
(out/"duende_rig_reporte.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
print("DUENDE_RIG_CANDIDATO",json.dumps(report,ensure_ascii=False))
