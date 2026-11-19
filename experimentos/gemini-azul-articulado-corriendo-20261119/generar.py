#!/usr/bin/env python3
# Gemini azul corregido según imagen compartida por el usuario: GLB con rig real y carrera frontal de 5 segundos.
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
teal=mat('Gemini azul eléctrico original',(0.004,.065,.65),.31,.01)
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
 curve=bpy.data.curves.new('Texto_Gemini','FONT');curve.body=s;curve.size=size
 curve.align_x='CENTER';curve.align_y='CENTER';curve.extrude=.0015;curve.bevel_depth=.0006
 o=bpy.data.objects.new('Rotulo legible: '+s,curve)
 bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.convert(target='MESH')
 return add(bpy.context.object,'Texto original Gemini',bone,material)
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
# Torso azul eléctrico con insignia Gemini, dos estrellas brillantes y placa Gemini.
sphere('Cuerpo verde turquesa',(0,0,1.265),(.60,.465,.63),teal,'torso',48)
# Insignia GEMINI de dos estrellas iridiscentes + dos arcos orbitales.
# Construida con geometría 3D real sobre el torso, no una pegatina PNG.
azul_cielo=mat('Gemini chispa cian',(.035,.78,1.0),.20)
lavanda=mat('Gemini chispa violeta',(.43,.30,1),.20)
rosa=mat('Gemini chispa rosada',(1,.33,.82),.20)
blanco_borde=mat('Gemini reflejo blanco',(0.96,.98,1),.18)
def linea_emblema(nombre,puntos,grosor,material):
 for i in range(len(puntos)-1):
  rod(nombre,puntos[i],puntos[i+1],grosor,material,'torso',10)
def estrella_gemini(cx,cz,s,mat1,mat2):
 # Simétrica, cuatro puntas suaves; una mayor a la izquierda y otra a la derecha.
 pts=[]
 for i in range(8):
  ang=math.pi/2+i*math.pi/4
  rr=(s if i%2==0 else s*.31)
  pts.append((cx+rr*math.cos(ang),-.492,cz+rr*math.sin(ang)))
 pts.append(pts[0])
 for i in range(8):
  linea_emblema('Bordes estrella Gemini', [pts[i],pts[i+1]],.010,mat1 if i<4 else mat2)
 # Segundo trazo blanco más fino para brillo central.
 inner=[]
 for i in range(8):
  a=math.pi/2+i*math.pi/4
  rr=(s*.84 if i%2==0 else s*.25)
  inner.append((cx+rr*math.cos(a),-.503,cz+rr*math.sin(a)))
 inner.append(inner[0])
 linea_emblema('Reflejo estrellas Gemini',inner,.0045,blanco_borde)
estrella_gemini(-.075,1.470,.127,azul_cielo,lavanda)
estrella_gemini(.128,1.413,.080,rosa,lavanda)
# Órbitas finas cruzadas como en la referencia Gemini.
for direction,material in ((1,azul_cielo),(-1,lavanda)):
 points_orbit=[]
 for i in range(26):
  t=(i/25)*math.pi*1.42+(.22 if direction==1 else 3.34)
  x=.008+.232*math.cos(t)
  z=1.457+.067*math.sin(t)*direction
  points_orbit.append((x,-.478,z))
 linea_emblema('Órbita Gemini iridiscente',points_orbit,.0075,material)
# Placa de identidad frontal, con forma de pastilla y texto negro.
box('Placa blanca Gemini',(0,-.471,1.015),(.64,.052,.163),labelwhite,'torso',.06)
textbody('Gemini',(0,-.51,1.011),.130,letter,'torso')
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
rig=bpy.context.object;rig.name='Gemini_Armature'
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
 rig.animation_data.action.name='Gemini_CORRER_hacia_camara_5s'
scene.frame_set(1)
glb=out/'Gemini_3D_Corriendo_Articulado.glb'
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
 'personaje':'Gemini azul y blanco corregido de la imagen aprobada; dos estrellas y placa Gemini',
 'glb':glb.name,'esqueleto':joints,'canales_animacion':channels,
 'clips':[a.get('name') for a in g['animations']],
 'duracion_segundos':5,'tecnica':'Blender, huesos y piezas 3D separadas',
 'regla':'No sustituir modelos originales ni deformar vertices manualmente.'}
(out/'informe.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('GEMINI_GLB_VALIDADO '+json.dumps(report,ensure_ascii=False))
# Render de 10 PNG SEPARADOS para modelado y verificación de Gemini (NO collage).
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
 scene.render.filepath=str(vistas/('gemini_'+name+'.png'))
 bpy.ops.render.render(write_still=True)
 print('GEMINI_VISTA_INDEPENDIENTE_GENERADA',name)
# Además de 10 vistas para 3D, cuatro poses consecutivas de carrera frontal.
cam.location=(0,-8.5,1.9)
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
for fr in (1,4,7,10):
 scene.frame_set(fr)
 scene.render.filepath=str(out/f'carrera_{fr:02d}.png')
 bpy.ops.render.render(write_still=True)
# Archivo ZIP con 10 PNG INDEPENDIENTES; el ZIP no incluye collage.
import zipfile
zpath=out/'Gemini_10_imagenes_separadas.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(vistas.glob('gemini_*.png')):
  z.write(p,arcname=p.name)
assert len(list(vistas.glob('gemini_*.png')))==10
with zipfile.ZipFile(zpath) as z:assert len(z.namelist())==10
print('GEMINI_10_PNG_SEPARADOS_GUARDADOS',str(zpath))
