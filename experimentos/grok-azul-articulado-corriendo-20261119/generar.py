#!/usr/bin/env python3
# Mascota Grok original del usuario: GLB con rig real y carrera frontal de 5 segundos.
# CANDIDATO independiente. No modificar ni reemplazar a Claude o modelos previos.
import bpy,sys,json,math,struct
from pathlib import Path
from mathutils import Vector,Euler
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1:raise SystemExit('Uso: blender -b -P generar.py -- destino')
out=Path(args[0]).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,rgba,rough=.36,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*rgba,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF')
 b.inputs['Base Color'].default_value=(*rgba,1)
 b.inputs['Roughness'].default_value=rough
 b.inputs['Metallic'].default_value=metal
 return m
teal=mat('Grok azul eléctrico original',(0.004,.065,.65),.31,.01)
white=mat('Casco y guantes blancos',(.94,.95,.99),.24,.05)
black=mat('Visor negro brillante',(.012,.015,.022),.15,.13)
labelwhite=mat('Placa blanca',(.97,.975,1),.29)
letter=mat('Texto negro',(.006,.008,.014),.48)
light=mat('Ojos blancos luminosos',(1,1,1),.20)
light.use_nodes=True
bs=light.node_tree.nodes.get('Principled BSDF')
if 'Emission Color' in bs.inputs: bs.inputs['Emission Color'].default_value=(1,1,1,1)
elif 'Emission' in bs.inputs: bs.inputs['Emission'].default_value=(1,1,1,1)
if 'Emission Strength' in bs.inputs: bs.inputs['Emission Strength'].default_value=1.5
parts=[]
def add(o,name,bone,material,sm=True):
 o.name=name;o.data.materials.append(material)
 if sm and o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 parts.append((o,bone));return o
def sphere(n,loc,scale,material,bone,segments=36):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=24,location=loc)
 o=bpy.context.object;o.scale=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 return add(o,n,bone,material)
def rod(n,a,b,r,material,bone,vertices=20):
 a,b=Vector(a),Vector(b);direction=b-a
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=direction.length,location=(a+b)*.5)
 o=bpy.context.object;o.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
 return add(o,n,bone,material)
def box(n,loc,scale,material,bone,bevel=.07):
 bpy.ops.mesh.primitive_cube_add(location=loc)
 o=bpy.context.object;o.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Bordes redondos','BEVEL');mod.width=bevel;mod.segments=5
  o.modifiers.new('Normales','WEIGHTED_NORMAL')
 return add(o,n,bone,material,False)
def textbody(s,loc,size,material,bone):
 curve=bpy.data.curves.new('Texto_Grok','FONT');curve.body=s;curve.size=size
 curve.align_x='CENTER';curve.align_y='CENTER';curve.extrude=.0015;curve.bevel_depth=.0006
 o=bpy.data.objects.new('Rotulo legible: '+s,curve)
 bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.convert(target='MESH')
 return add(bpy.context.object,'Texto original Grok',bone,material)
# Geometría del modelo de referencia: cabeza blanca y grande, antenita.
sphere('Casco blanco redondo',(0,0,2.17),(.68,.55,.51),white,'cabeza',48)
sphere('Visor negro ovalado',(0,-.535,2.205),(.54,.066,.205),black,'cabeza',48)
sphere('Bola antena', (0,0,2.87),(.115,.115,.115),teal,'cabeza')
rod('Base antena',(0,0,2.665),(0,0,2.79),.058,teal,'cabeza')
# Dos ojos cerrados brillantes en arco, sin boca.
for sign in (-1,1):
 cx=sign*.239
 for i in range(15):
  t1=math.pi*.11+math.pi*.78*i/15
  t2=math.pi*.11+math.pi*.78*(i+1)/15
  p1=(cx+.128*math.cos(t1),-.605,2.177+.088*math.sin(t1))
  p2=(cx+.128*math.cos(t2),-.605,2.177+.088*math.sin(t2))
  rod('Ojo cerrado luminoso',p1,p2,.0155,light,'cabeza',10)
# Torso redondito verde turquesa, logo blanco y placa Grok.
sphere('Cuerpo verde turquesa',(0,0,1.265),(.60,.465,.63),teal,'torso',48)
# Estrella de Grok de CUATRO puntas, con borde blanco e interior naranja-rosa.
# Se crea como geometría REAL (no sticker deformado) y va en el torso azul.
star_white=mat('Borde blanco de estrella',(.99,.99,1),.26)
star_yellow=mat('Estrella centro amarillo',(1,.72,.035),.21)
star_orange=mat('Estrella centro naranja',(1,.31,.035),.22)
star_pink=mat('Estrella puntas rosadas',(1,.055,.36),.21)
star_blue=mat('Estrella centro luminoso',(.98,.80,.21),.2)
def make_star(name,scale,y,materials):
 xz=[]
 for k in range(8):
  a=math.pi/2+math.pi*k/4
  r=(.203 if k%2==0 else .094)*scale
  xz.append((r*math.cos(a),1.47+r*math.sin(a)))
 verts=[(0,y,1.47)]+[(x,y,z) for x,z in xz]
 faces=[(0,k+1,(k+1)%8+1) for k in range(8)]
 mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(verts,[],faces);mesh.update()
 ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob)
 add(ob,name,'torso',materials[0],False)
 for m in materials[1:]:ob.data.materials.append(m)
 for i,p in enumerate(ob.data.polygons):p.material_index=(i//2)%len(materials)
 return ob
make_star('Borde estrella Grok',1.12,-.462,[star_white])
make_star('Diamante estrella multicolor Grok',.96,-.473,[star_yellow,star_orange,star_pink,star_blue])
# Placa de identidad frontal, con forma de pastilla y texto negro.
box('Placa blanca Grok',(0,-.471,1.015),(.49,.052,.163),labelwhite,'torso',.06)
textbody('Grok',(0,-.51,1.011),.16,letter,'torso')
# Piezas separadas para que las articulaciones NO deformen el personaje.
points={
 'cadera':((0,0,.79),(0,0,1.00)),
 'torso':((0,0,1.00),(0,0,1.72)),
 'cabeza':((0,0,1.72),(0,0,2.26))
}
parents={'torso':'cadera','cabeza':'torso'}
sphere('Union cadera',(0,0,.785),(.43,.33,.19),teal,'cadera')
for side,sgn in [('L',1),('R',-1)]:
 x=sgn
 points.update({
  'brazo_'+side:((x*.57,0,1.52),(x*.735,0,1.17)),
  'antebrazo_'+side:((x*.735,0,1.17),(x*.765,0,1.105)),
  'mano_'+side:((x*.765,0,1.105),(x*.77,0,.98)),
  'pierna_'+side:((x*.225,0,.76),(x*.225,0,.49)),
  'pantorrilla_'+side:((x*.225,0,.49),(x*.225,-.005,.345)),
  'pie_'+side:((x*.225,-.005,.345),(x*.225,-.17,.21))})
 parents.update({
  'brazo_'+side:'torso','antebrazo_'+side:'brazo_'+side,'mano_'+side:'antebrazo_'+side,
  'pierna_'+side:'cadera','pantorrilla_'+side:'pierna_'+side,'pie_'+side:'pantorrilla_'+side})
 # Hombrera y manga en bloque unido al hueso de brazo.
 sphere('Hombro '+side,(x*.585,0,1.53),(.18,.19,.17),teal,'brazo_'+side)
 rod('Brazo manga '+side,(x*.61,0,1.47),(x*.735,0,1.19),.155,teal,'brazo_'+side)
 sphere('Codo oculto '+side,(x*.735,0,1.17),(.137,.145,.14),teal,'antebrazo_'+side)
 sphere('Puño blanco '+side,(x*.77,-.01,1.065),(.167,.15,.155),white,'mano_'+side)
 sphere('Pulgar blanco '+side,(x*.77-x*.13,-.075,1.057),(.072,.082,.09),white,'mano_'+side)
 # Muslo corto, rodilla interior articulada y bota grande.
 xx=x*.225
 rod('Muslo '+side,(xx,0,.78),(xx,0,.49),.162,teal,'pierna_'+side)
 sphere('Rodilla '+side,(xx,0,.49),(.157,.16,.15),teal,'pantorrilla_'+side)
 rod('Pantorrilla '+side,(xx,0,.49),(xx,-.015,.345),.15,teal,'pantorrilla_'+side)
 sphere('Bota ancha '+side,(xx,-.115,.211),(.241,.33,.182),teal,'pie_'+side)
 sphere('Sola de bota '+side,(xx,-.114,.094),(.246,.331,.065),teal,'pie_'+side)
# Huesos y skin rígido en cada objeto; no se deforman vértices a mano.
bpy.ops.object.armature_add(location=(0,0,0))
rig=bpy.context.object;rig.name='Grok_Armature'
bpy.ops.object.mode_set(mode='EDIT')
rig.data.edit_bones.remove(rig.data.edit_bones[0])
for name,(a,b) in points.items():
 bone=rig.data.edit_bones.new(name);bone.head=a;bone.tail=b
for child,parent in parents.items():
 rig.data.edit_bones[child].parent=rig.data.edit_bones[parent]
 rig.data.edit_bones[child].use_connect=False
bpy.ops.object.mode_set(mode='OBJECT')
for ob,name in parts:
 group=ob.vertex_groups.new(name=name)
 group.add(list(range(len(ob.data.vertices))),1.0,'REPLACE')
 old=ob.matrix_world.copy();ob.parent=rig;ob.matrix_world=old
 mod=ob.modifiers.new('Rig sin deformaciones','ARMATURE');mod.object=rig
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=121;scene.render.fps=24
for bone in rig.pose.bones:bone.rotation_mode='QUATERNION'
# Carrera 5 segundos hacia -Y (la cámara frontal), con zancada alternada.
for frame in range(1,122,2):
 t=(frame-1)/24.0
 phase=2*math.pi*2.2*t
 rig.location=(0,-1.15*t/5,.026*abs(math.sin(phase)))
 rig.keyframe_insert(data_path='location',frame=frame)
 poses={'torso':(-.065,0,.016*math.sin(phase)),
        'cabeza':(.03,0,-.01*math.sin(phase))}
 for side,offset in [('L',0),('R',math.pi)]:
  s=math.sin(phase+offset)
  # El codo se flexiona y la mano acompaña; no hay brazos rígidos oscilando.
  poses['brazo_'+side]=(-.74*s,0,.075*s)
  poses['antebrazo_'+side]=(-.19-.34*max(0,-s),0,0)
  poses['mano_'+side]=(.11*s,0,0)
  poses['pierna_'+side]=(.85*s,.05*s,0)
  poses['pantorrilla_'+side]=(.17+1.00*max(0,-s),0,0)
  poses['pie_'+side]=(-.18-.26*max(0,-s),0,0)
 for name,angles in poses.items():
  pb=rig.pose.bones[name];pb.rotation_quaternion=Euler(angles,'XYZ').to_quaternion()
  pb.keyframe_insert(data_path='rotation_quaternion',frame=frame)
if rig.animation_data and rig.animation_data.action:
 rig.animation_data.action.name='Grok_CORRER_hacia_camara_5s'
scene.frame_set(1)
glb=out/'Grok_3D_Corriendo_Articulado.glb'
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',export_animations=True,export_skins=True,export_frame_range=True)
raw=glb.read_bytes()
if raw[:4]!=b'glTF':raise RuntimeError('No es GLB')
size=struct.unpack_from('<I',raw,12)[0]
g=json.loads(raw[20:20+size])
if not g.get('skins') or not g.get('animations'):raise RuntimeError('GLB sin rig o clip')
joints=len(g['skins'][0]['joints'])
channels=sum(len(ani['channels']) for ani in g['animations'])
if joints<15 or channels<40:raise RuntimeError('Rig incompleto: huesos=%s canales=%s'%(joints,channels))
report={'estado':'CANDIDATO - pendiente de revision visual',
 'personaje':'Grok azul y blanco de la imagen proporcionada',
 'glb':glb.name,'esqueleto':joints,'canales_animacion':channels,
 'clips':[a.get('name') for a in g['animations']],
 'duracion_segundos':5,'tecnica':'Blender, huesos y piezas 3D separadas',
 'regla':'No sustituir modelos originales ni deformar vertices manualmente.'}
(out/'informe.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('GROK_GLB_VALIDADO '+json.dumps(report,ensure_ascii=False))
# Render de 10 PNG SEPARADOS para modelado y verificación de Grok (NO collage).
# Cada imagen usa el MISMO modelo geométrico: vistas realmente consistentes.
bpy.ops.object.camera_add(location=(0,-8.5,2.2))
cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=3.30;scene.camera=cam
for loc,power in [((-3,-5,6),1000),((4,-3,4),600),((1,5,3),400)]:
 bpy.ops.object.light_add(type='AREA',location=loc)
 lamp=bpy.context.object;lamp.data.energy=power;lamp.data.size=3.8
 lamp.rotation_euler=(Vector((0,0,1.45))-lamp.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=25
scene.render.resolution_x=530;scene.render.resolution_y=650
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard'
scene.world.color=(.18,.18,.20)
scene.frame_set(1)
views=[
 ('01_frente',0,0),('02_45_izquierda',45,0),
 ('03_perfil_izquierdo',90,0),('04_135_trasera',135,0),
 ('05_espalda',180,0),('06_225_trasera',225,0),
 ('07_perfil_derecho',270,0),('08_315_frente',315,0),
 ('09_desde_arriba',0,40),('10_desde_abajo',0,-25)]
vistas=out/'vistas';vistas.mkdir(exist_ok=True)
target=Vector((0,0,1.47))
for name,angle,tilt in views:
 a=math.radians(angle);e=math.radians(tilt)
 cam.location=(8.5*math.sin(a)*math.cos(e),-8.5*math.cos(a)*math.cos(e),1.47+8.5*math.sin(e))
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(vistas/('grok_'+name+'.png'))
 bpy.ops.render.render(write_still=True)
 print('GROK_VISTA_INDEPENDIENTE_GENERADA',name)
# Además de 10 vistas para 3D, cuatro poses consecutivas de carrera frontal.
cam.location=(0,-8.5,1.9)
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
for fr in (1,4,7,10):
 scene.frame_set(fr)
 scene.render.filepath=str(out/f'carrera_{fr:02d}.png')
 bpy.ops.render.render(write_still=True)
# Archivo ZIP con 10 PNG INDEPENDIENTES; el ZIP no incluye collage.
import zipfile
zpath=out/'Grok_10_imagenes_separadas.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(vistas.glob('grok_*.png')):
  z.write(p,arcname=p.name)
assert len(list(vistas.glob('grok_*.png')))==10
with zipfile.ZipFile(zpath) as z:assert len(z.namelist())==10
print('GROK_10_PNG_SEPARADOS_GUARDADOS',str(zpath))
