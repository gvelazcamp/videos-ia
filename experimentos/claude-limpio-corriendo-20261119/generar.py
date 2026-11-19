#!/usr/bin/env python3
"""Claude reconstruido para animación desde las 4 referencias del usuario.
   Crea modelo separado. NO sustituye el GLB TRELLIS existente."""
import bpy,sys,math,json,struct
from mathutils import Vector,Euler
from pathlib import Path
arg=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(arg)!=1:raise SystemExit("Uso: blender -b -P generar.py -- directorio")
out=Path(arg[0]).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,rough=.38,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
 p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
white=mat('Claude blanco',(.92,.94,.98),.27,.08)
black=mat('Visor negro',(.009,.011,.016),.15,.14)
orange=mat('Claude naranja',(.98,.31,.028),.29,.10)
light=mat('Claude naranja claro',(1,.48,.048),.32,.09)
dark=mat('Suelas',(.20,.17,.15),.6)
objects=[]
def sphere(name,xyz,size,material,bone,n=32):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=n,ring_count=20,location=xyz)
 o=bpy.context.object;o.name=name;o.scale=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 objects.append((o,bone));return o
def rod(name,a,b,r,material,bone,n=12):
 a,b=Vector(a),Vector(b);d=b-a
 bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=d.length,location=(a+b)*.5)
 o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
 o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 objects.append((o,bone));return o
def label(s,xyz,size,material,bone):
 c=bpy.data.curves.new('letra','FONT');c.body=s;c.size=size;c.align_x='CENTER';c.align_y='CENTER'
 c.extrude=.002;c.bevel_depth=.0007
 o=bpy.data.objects.new('Nombre CLAUDE',c);bpy.context.collection.objects.link(o)
 o.location=xyz;o.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
 bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
 o=bpy.context.object;o.data.materials.append(material);objects.append((o,bone))
# Cabeza y visor con expresiones legibles en malla 3D.
sphere('CASCO cabeza',(0,0,2.04),(.62,.47,.50),white,'cabeza',48)
sphere('PANTALLA cara negra',(0,-.437,2.045),(.525,.11,.255),black,'cabeza',48)
for side in (-1,1):
 for i in range(14):
  a=i*math.pi/14;b=(i+1)*math.pi/14
  p=(side*.242-.122*math.cos(a),-.545,2.055+.078*math.sin(a))
  q=(side*.242-.122*math.cos(b),-.545,2.055+.078*math.sin(b))
  rod('Ojos sonrientes',p,q,.014,white,'cabeza',8)
rod('Antena soporte',(0,0,2.51),(0,0,2.61),.067,orange,'cabeza')
sphere('Antena bolita',(0,0,2.66),(.125,.125,.125),light,'cabeza')
# Torso, emblemático logo y nombre Claude.
sphere('Cuello',(0,0,1.63),(.25,.23,.12),orange,'torso')
sphere('TORSO',(0,0,1.23),(.535,.39,.58),orange,'torso',48)
sphere('Logo blanco',(0,-.389,1.407),(.234,.052,.234),white,'torso')
sphere('Sol centro',(0,-.454,1.407),(.048,.02,.048),orange,'torso')
for i in range(14):
 a=i*2*math.pi/14
 rod('Rayos logo',(.077*math.cos(a),-.452,1.407+.077*math.sin(a)),
  (.18*math.cos(a),-.452,1.407+.18*math.sin(a)),.010,orange,'torso',8)
sphere('Placa nombre',(0,-.393,1.003),(.25,.06,.095),white,'torso')
label('Claude',(0,-.463,1.003),.108,black,'torso')
sphere('Cadera',(0,0,.79),(.38,.32,.23),orange,'cadera')
# Brazos y piernas separados, con articulaciones reales y skinning rígido.
points={'cadera':((0,0,.82),(0,0,.98)),
        'torso':((0,0,1),(0,0,1.63)),
        'cabeza':((0,0,1.63),(0,0,2.24))}
parents={'torso':'cadera','cabeza':'torso'}
for tag,sign in [('L',1),('R',-1)]:
 x=sign
 points.update({
 'brazo_'+tag:((x*.49,0,1.48),(x*.66,0,1.19)),
 'antebrazo_'+tag:((x*.66,0,1.19),(x*.715,0,.995)),
 'mano_'+tag:((x*.715,0,.995),(x*.715,0,.85)),
 'pierna_'+tag:((x*.225,0,.77),(x*.225,0,.42)),
 'pantorrilla_'+tag:((x*.225,0,.42),(x*.225,-.01,.18)),
 'pie_'+tag:((x*.225,-.01,.18),(x*.225,-.22,.16))})
 parents.update({'brazo_'+tag:'torso','antebrazo_'+tag:'brazo_'+tag,
 'mano_'+tag:'antebrazo_'+tag,'pierna_'+tag:'cadera','pantorrilla_'+tag:'pierna_'+tag,
 'pie_'+tag:'pantorrilla_'+tag})
 sphere('Hombro_'+tag,(x*.49,0,1.48),(.19,.19,.19),light,'brazo_'+tag)
 rod('Brazo_'+tag,(x*.53,0,1.47),(x*.66,0,1.19),.133,orange,'brazo_'+tag)
 sphere('Codo_'+tag,(x*.66,0,1.19),(.135,.135,.135),orange,'antebrazo_'+tag)
 rod('Antebrazo_'+tag,(x*.66,0,1.19),(x*.715,0,.99),.122,light,'antebrazo_'+tag)
 sphere('Guante_'+tag,(x*.715,-.02,.927),(.17,.155,.175),white,'mano_'+tag)
 sphere('Pulgar_'+tag,(x*.715-x*.12,-.11,.94),(.068,.067,.084),white,'mano_'+tag,24)
 xx=x*.225
 sphere('Cadera izquierda/derecha '+tag,(xx,0,.77),(.16,.17,.18),orange,'pierna_'+tag)
 rod('Muslo_'+tag,(xx,0,.75),(xx,0,.42),.16,orange,'pierna_'+tag)
 sphere('Rodilla_'+tag,(xx,0,.42),(.16,.16,.16),light,'pantorrilla_'+tag)
 rod('Pantorrilla_'+tag,(xx,0,.41),(xx,-.02,.18),.145,orange,'pantorrilla_'+tag)
 sphere('Bota_'+tag,(xx,-.09,.16),(.188,.259,.148),light,'pie_'+tag)
 sphere('Puntera_'+tag,(xx,-.26,.16),(.18,.11,.13),white,'pie_'+tag)
 sphere('Suela_'+tag,(xx,-.07,.069),(.18,.268,.049),dark,'pie_'+tag)
# Armature real 15 huesos. Cada pieza usa peso 1.0 en un hueso.
bpy.ops.object.armature_add(location=(0,0,0))
rig=bpy.context.object;rig.name='Claude_armature_articulada'
bpy.ops.object.mode_set(mode='EDIT');rig.data.edit_bones.remove(rig.data.edit_bones[0])
for name,(a,b) in points.items():
 bone=rig.data.edit_bones.new(name);bone.head=a;bone.tail=b
for child,par in parents.items():
 rig.data.edit_bones[child].parent=rig.data.edit_bones[par]
 rig.data.edit_bones[child].use_connect=False
bpy.ops.object.mode_set(mode='OBJECT')
for o,name in objects:
 if name is None:continue
 group=o.vertex_groups.new(name=name);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
 old=o.matrix_world.copy();o.parent=rig;o.matrix_world=old
 arm=o.modifiers.new('Skin rígido articulado','ARMATURE');arm.object=rig
scene=bpy.context.scene
scene.frame_start=1;scene.frame_end=121;scene.render.fps=24
for pb in rig.pose.bones:pb.rotation_mode='QUATERNION'
for frame in range(1,122,2):
 t=(frame-1)/24;phase=2*math.pi*2.4*t
 rig.location=(0,-.9*t/5,.045*abs(math.sin(phase)))
 rig.keyframe_insert(data_path='location',frame=frame)
 poses={'torso':(-.08,0,.025*math.sin(phase)),'cabeza':(.045,0,-.014*math.sin(phase))}
 for tag,offset in [('L',0),('R',math.pi)]:
  s=math.sin(phase+offset)
  poses['brazo_'+tag]=(-.95*s,0,.14*s)
  poses['antebrazo_'+tag]=(-.30-.40*max(0,-s),0,0)
  poses['mano_'+tag]=(.22*s,0,0)
  poses['pierna_'+tag]=(.98*s,.07*s,.12*s)
  poses['pantorrilla_'+tag]=(.22+1.08*max(0,-s),0,0)
  poses['pie_'+tag]=(-.18-.38*max(0,-s),0,0)
 for name,angles in poses.items():
  p=rig.pose.bones[name]
  p.rotation_quaternion=Euler(angles,'XYZ').to_quaternion()
  p.keyframe_insert(data_path='rotation_quaternion',frame=frame)
if rig.animation_data and rig.animation_data.action:
 rig.animation_data.action.name='Claude_CORRER_hacia_camara_5s'
scene.frame_set(1)
file=out/'Claude_3D_CARRERA_REAL.glb'
bpy.ops.export_scene.gltf(filepath=str(file),export_format='GLB',
 export_animations=True,export_skins=True,export_frame_range=True)
binary=file.read_bytes()
if binary[:4]!=b'glTF':raise RuntimeError('El resultado no es GLB')
length=struct.unpack_from('<I',binary,12)[0];g=json.loads(binary[20:20+length])
if not g.get('skins') or not g.get('animations'):raise RuntimeError('Falta esqueleto/animación')
bones=len(g['skins'][0]['joints']);channels=sum(len(a['channels']) for a in g['animations'])
if bones<12 or channels<12:raise RuntimeError('Los huesos no se mueven')
info={'archivo':file.name,'estado':'CANDIDATO, pendiente de inspección visual',
 'origen':'Reconstrucción original desde referencias del usuario',
 'huesos':bones,'canales':channels,'clips':[a.get('name') for a in g['animations']],
 'duracion_segundos':5,'geometria':'piezas 3D separadas, skin rígido real',
 'reemplaza_trellis':False}
(out/'informe.json').write_text(json.dumps(info,indent=2,ensure_ascii=False))
print('GLB_VALIDADO',json.dumps(info,ensure_ascii=False))
# Renders frontales independientes de Three.js para auditoría del movimiento.
bpy.ops.object.camera_add(location=(0,-8,3))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1.39))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=3.4;scene.camera=cam
for loc,power in [((-3,-4,5),800),((3,-3,3),500)]:
 bpy.ops.object.light_add(type='AREA',location=loc)
 o=bpy.context.object;o.data.energy=power;o.data.size=3
 o.rotation_euler=(Vector((0,0,1.3))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=22
scene.render.resolution_x=450;scene.render.resolution_y=540;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.world.color=(.12,.16,.19)
for frame in [1,5,9,13]:
 scene.frame_set(frame)
 scene.render.filepath=str(out/f'vista_{frame:02d}.png')
 bpy.ops.render.render(write_still=True)
print('AUDITORIA_DE_4_FOTOGRAMAS_LISTA')
