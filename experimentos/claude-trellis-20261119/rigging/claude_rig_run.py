#!/usr/bin/env python3
"""Probar un rig esquelético auténtico en una COPIA del GLB de Claude."""
import bpy, json, math, struct, sys
from pathlib import Path
from mathutils import Vector, Quaternion

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(argv)!=2: raise SystemExit("Uso: blender -b -P SCRIPT -- ORIGEN.glb DESTINO_DIR")
source,out=Path(argv[0]).resolve(),Path(argv[1]).resolve()
if not source.is_file(): raise RuntimeError("No existe el GLB fuente")
out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
if not meshes: raise RuntimeError("GLB sin malla")
bpy.context.view_layer.update()
coords=[o.matrix_world @ v.co for o in meshes for v in o.data.vertices]
lo=Vector((min(v[0] for v in coords),min(v[1] for v in coords),min(v[2] for v in coords)))
hi=Vector((max(v[0] for v in coords),max(v[1] for v in coords),max(v[2] for v in coords)))
span=hi-lo
if min(span.x,span.y,span.z)<.0001: raise RuntimeError("Geometría inválida")
cx,cy=(hi.x+lo.x)*.5,(hi.y+lo.y)*.5
z0=lo.z;H=span.z;W=span.x

bpy.ops.object.armature_add(enter_editmode=False,location=(0,0,0))
rig=bpy.context.object;rig.name='Claude_Armadura';rig.data.name='Claude_Huesos'
bpy.ops.object.mode_set(mode='EDIT')
rig.data.edit_bones.remove(rig.data.edit_bones[0])
p={
'cadera':((0,0,.28),(0,0,.43)),
'pecho':((0,0,.43),(0,0,.72)),
'cabeza':((0,0,.72),(0,0,.90)),
'brazo_L':((+.32,0,.68),(+.40,0,.52)),
'antebrazo_L':((+.40,0,.52),(+.42,0,.37)),
'brazo_R':((-.32,0,.68),(-.40,0,.52)),
'antebrazo_R':((-.40,0,.52),(-.42,0,.37)),
'pierna_L':((+.14,0,.35),(+.15,0,.18)),
'pantorrilla_L':((+.15,0,.18),(+.15,0,.075)),
'pie_L':((+.15,0,.075),(+.15,-.085,.07)),
'pierna_R':((-.14,0,.35),(-.15,0,.18)),
'pantorrilla_R':((-.15,0,.18),(-.15,0,.075)),
'pie_R':((-.15,0,.075),(-.15,-.085,.07))}
parent={
'pecho':'cadera','cabeza':'pecho',
'brazo_L':'pecho','antebrazo_L':'brazo_L',
'brazo_R':'pecho','antebrazo_R':'brazo_R',
'pierna_L':'cadera','pantorrilla_L':'pierna_L','pie_L':'pantorrilla_L',
'pierna_R':'cadera','pantorrilla_R':'pierna_R','pie_R':'pantorrilla_R'}
for name,(a,b) in p.items():
 e=rig.data.edit_bones.new(name)
 e.head=(cx+W*a[0],cy+H*a[1],z0+H*a[2])
 e.tail=(cx+W*b[0],cy+H*b[1],z0+H*b[2])
 e.roll=0
for child,pa in parent.items():
 rig.data.edit_bones[child].parent=rig.data.edit_bones[pa]
 rig.data.edit_bones[child].use_connect=False
bpy.ops.object.mode_set(mode='OBJECT')

def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)))
 return t*t*(3-2*t)

for ob in meshes:
 groups={n:ob.vertex_groups.new(name=n) for n in p}
 for v in ob.data.vertices:
  pos=ob.matrix_world @ v.co
  y=(pos.z-z0)/H;x=(pos.x-cx)/max(W*.5,1e-6);lateral=abs(x)
  head=smooth(.66,.82,y)
  arm=smooth(.45,.72,lateral)*smooth(.33,.46,y)*(1-smooth(.69,.77,y))
  leg=smooth(.14,.38,lateral)*(1-smooth(.26,.41,y))
  head*=1-arm;arm*=1-leg
  rest=max(0,1-head-arm-leg)
  weights={'cabeza':head,'pecho':rest*smooth(.29,.48,y),'cadera':rest*(1-smooth(.29,.48,y))}
  side='L' if x>=0 else 'R'
  forearm=1-smooth(.41,.55,y)
  weights['brazo_'+side]=arm*(1-forearm)
  weights['antebrazo_'+side]=arm*forearm
  shin=1-smooth(.13,.26,y)
  foot=1-smooth(.045,.105,y)
  weights['pierna_'+side]=leg*(1-shin)
  weights['pantorrilla_'+side]=leg*shin*(1-foot)
  weights['pie_'+side]=leg*shin*foot
  total=sum(weights.values())
  if total<.001: raise RuntimeError("Pesos de rigging invalidos")
  for name,val in weights.items():
   if val>.00001: groups[name].add([v.index],val/total,'REPLACE')
 mod=ob.modifiers.new('Claude_Esqueleto','ARMATURE')
 mod.object=rig

scene=bpy.context.scene
scene.render.fps=24;scene.frame_start=1;scene.frame_end=121
for bone in rig.pose.bones: bone.rotation_mode='QUATERNION'
root=rig.pose.bones['cadera']
root_basis=root.bone.matrix_local.to_quaternion()
for f in range(1,122,2):
 t=(f-1)/24;phase=t*2*math.pi*2.5
 displacement=Vector((0,-H*1.05*t/5,H*.012*abs(math.sin(phase*2))))
 root.location=root_basis.inverted() @ displacement
 root.keyframe_insert(data_path='location',frame=f,group='AvanceFrontal')
 for side,offset in [('L',0),('R',math.pi)]:
  s=math.sin(phase+offset)
  poses={
   'pierna_'+side:s*.47,
   'pantorrilla_'+side:max(0,-s)*.68+.12,
   'pie_'+side:-max(0,-s)*.2,
   'brazo_'+side:-s*.62,
   'antebrazo_'+side:.24+max(0,s)*.25}
  for name,angle in poses.items():
   pb=rig.pose.bones[name]
   pb.rotation_quaternion=Quaternion((1,0,0),angle)
   pb.keyframe_insert(data_path='rotation_quaternion',frame=f,group='Extremidades')
 for name,angle in [('pecho',.045),('cabeza',-.045)]:
  pb=rig.pose.bones[name];pb.rotation_quaternion=Quaternion((1,0,0),angle)
  pb.keyframe_insert(data_path='rotation_quaternion',frame=f)

if rig.animation_data and rig.animation_data.action:
 rig.animation_data.action.name='Correr_hacia_camara_5s'
scene.frame_set(1)
target=out/'claude-corriendo-articulado.glb'
bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',export_animations=True)
raw=target.read_bytes()
if raw[:4]!=b'glTF': raise RuntimeError('Exportación GLB inválida')
length=struct.unpack_from('<I',raw,12)[0]
gltf=json.loads(raw[20:20+length])
if not gltf.get('skins') or not gltf.get('animations'):
 raise RuntimeError('No tiene esqueleto o animación GLB real')
channels=sum(len(a.get('channels',[])) for a in gltf['animations'])
if channels<10: raise RuntimeError('Faltan canales de movimiento en brazos/piernas')
report={'estado':'CANDIDATO PENDIENTE REVISION VISUAL','huesos':len(p),
 'vertices':sum(len(o.data.vertices) for o in meshes),
 'clips':[a.get('name') for a in gltf['animations']],
 'canales':channels,'duracion_segundos':5,'origen':str(source),
 'nota':'Modelo no aprobado; comprobar manos y pies antes de considerarlo definitivo.'}
(out/'diagnostico.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print('CLAUDE_RIGGING_RESULTADO '+json.dumps(report,ensure_ascii=False))
