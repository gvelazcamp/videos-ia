#!/usr/bin/env python3
"""El último pulso: demostración de cine 3D 40s en Blender con los 4 GLB reales.
Sin narración Charon: la banda sonora de esta prueba será ambiental original.
No sobrescribe modelos, guiones ni bibliotecas.
"""
import bpy, sys, json, math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=2:raise SystemExit('Uso: blender -b -P generar_corto.py -- REPO SALIDA')
repo=Path(args[0]).resolve();out=Path(args[1]).resolve();out.mkdir(parents=True,exist_ok=True)
FPS=8;DURATION=40;END=FPS*DURATION
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'
sc.display.shading.color_type='MATERIAL'
sc.display.shading.show_shadows=True
sc.display.shading.show_cavity=True
sc.display.shading.cavity_type='BOTH'
sc.render.resolution_x=360;sc.render.resolution_y=640;sc.render.resolution_percentage=100
sc.render.fps=FPS;sc.frame_start=1;sc.frame_end=END
sc.render.image_settings.file_format='PNG'
sc.render.image_settings.color_mode='RGB'
sc.render.filepath=str(out/'frame_')
world=sc.world or bpy.data.worlds.new('Cielo azul');sc.world=world
world.use_nodes=True
world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.012,.023,.061,1)
world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.7

def mat(name,rgba,metal=0,rough=.4,emission=None):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgba,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF')
 b.inputs['Base Color'].default_value=(*rgba,1)
 b.inputs['Metallic'].default_value=metal
 b.inputs['Roughness'].default_value=rough
 if emission:
  if b.inputs.get('Emission'):b.inputs['Emission'].default_value=(*emission,1)
  if b.inputs.get('Emission Color'):b.inputs['Emission Color'].default_value=(*emission,1)
  if b.inputs.get('Emission Strength'):b.inputs['Emission Strength'].default_value=2
 return m
dark=mat('Grafito profundo',(.01,.025,.05),.4)
silver=mat('Plata futurista',(.21,.30,.38),.7)
blue=mat('Energía azul',(.03,.35,.65),.15,emission=(.04,.68,1))
white=mat('Luz de bordes',(.65,.80,.9),.4)
gold=mat('Luz solar',(.8,.4,.04),.4,emission=(1,.55,.07))
def cyl(name,r,d,loc,material,vert=32):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vert,radius=r,depth=d,location=loc)
 o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
def cube(name,size,loc,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material);return o
def hoop(name,loc,major,minor,material):
 bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=loc,major_radius=major,minor_radius=minor)
 o=bpy.context.object;o.name=name;o.data.materials.append(material);return o

cyl('Isla circular futurista',8.5,.32,(0,0,-.20),dark,64)
hoop('Circunferencia brillante',(0,0,.004),8.2,.06,blue)
for q in (-6,-4,-2,0,2,4,6):
 cube('Cuadrícula suelo',(.02,13,.008),(q,0,.001),silver)
for q in (-5,-3,-1,1,3,5):
 cube('Cuadrícula suelo',(13,.02,.008),(0,q,.001),silver)
for x,y in [(-5,-3),(5,-3),(-5,3),(5,3)]:
 cyl('Antena vertical',.11,2.6,(x,y,1.3),silver,12)
 hoop('Aro de señal',(x,y,2.7),.28,.04,blue)
battery_y=2.1
cyl('Soporte de batería',1.1,.22,(0,battery_y,.12),silver)
cyl('Cuerpo de batería',.66,1.2,(0,battery_y,.79),dark)
core=cyl('Núcleo de energía animado',.48,.9,(0,battery_y,.80),blue)
cyl('Tapa de batería',.7,.12,(0,battery_y,1.45),silver)
for z in (.40,.7,1.0,1.28):
 hoop('Contorno de carga',(0,battery_y,z),.66,.032,white)
bpy.ops.object.light_add(type='POINT',location=(0,battery_y,1.4))
light=bpy.context.object;light.name='Batería con energía variable'
for sec,power,color,sz in [(0,650,(.05,.73,1),1),(11,640,(.05,.73,1),1),
                           (17,180,(1,.13,.04),.57),(24,20,(1,.015,.01),.12),
                           (31,80,(1,.18,.08),.35),(35,1000,(1,.59,.10),1.1),
                           (40,1450,(1,.83,.42),1.3)]:
 frame=min(END,1+sec*FPS)
 light.data.energy=power;light.data.color=color
 light.data.keyframe_insert('energy',frame=frame)
 light.data.keyframe_insert('color',frame=frame)
 core.scale.z=sz;core.keyframe_insert('scale',frame=frame)

models=[
 ('ChatGPT','experimentos/chatgpt-movimientos-universal-20261119/resultado/ChatGPT_Biblioteca_12_Movimientos.glb',-3.8,-.65),
 ('Claude','experimentos/claude-movimientos-20261119/resultado-saludo-verificado/Claude_Biblioteca_12_Movimientos.glb',-1.35,-1.35),
 ('Gemini','experimentos/gemini-movimientos-universal-20261119/resultado/Gemini_Biblioteca_12_Movimientos.glb',1.35,-1.35),
 ('Grok','experimentos/grok-gris-movimientos-universal-20261119/resultado/Grok_Biblioteca_12_Movimientos.glb',3.8,-.65)
]
actors=[]
for name,glb,x,y in models:
 path=repo/glb;assert path.is_file(),str(path)
 before=set(bpy.data.objects);oldacts=set(bpy.data.actions)
 bpy.ops.import_scene.gltf(filepath=str(path))
 imported=[o for o in bpy.data.objects if o not in before]
 rigs=[o for o in imported if o.type=='ARMATURE']
 assert rigs,name+' sin esqueleto'
 rig=rigs[0]
 assert len(rig.pose.bones)>=15
 root=bpy.data.objects.new('Movimiento por escena '+name,None);sc.collection.objects.link(root)
 for obj in imported:
  if obj.parent not in imported:
   old=obj.matrix_world.copy();obj.parent=root;obj.matrix_world=old
 root.location=(x,y,0)
 desired=['Reposo','Caminar_lento','Correr','Saludar','Saltar']
 clips={}
 if rig.animation_data:
  for tr in rig.animation_data.nla_tracks:
   for strip in tr.strips:
    for n in desired:
     if n.lower() in (tr.name+' '+strip.name+' '+strip.action.name).lower():clips[n]=strip.action
 for act in bpy.data.actions:
  if act not in oldacts:
   for n in desired:
    if n.lower() in act.name.lower() and n not in clips:clips[n]=act
 assert len(clips)==len(desired),'Faltan clips para '+name+':'+str(list(clips))
 rig.animation_data_create();rig.animation_data.action=None
 for tr in list(rig.animation_data.nla_tracks):rig.animation_data.nla_tracks.remove(tr)
 track=rig.animation_data.nla_tracks.new();track.name='Secuencia del corto '+name
 actions=[(0,6,'Reposo'),(6,12,'Caminar_lento'),(12,17,'Reposo'),
          (17,21,'Saludar'),(21,25,'Reposo'),(25,32,'Correr'),
          (32,35,'Saltar'),(35,40,'Reposo')]
 for k,(t0,t1,clipname) in enumerate(actions):
  action=clips[clipname]
  length=max(1,action.frame_range[1]-action.frame_range[0])
  st=track.strips.new(clipname+'_'+str(k),1+t0*FPS,action)
  st.action_frame_start=action.frame_range[0]
  st.action_frame_end=action.frame_range[1]
  # Blender source animation is at 24 fps, but this preview is rendered at 8 fps.
  # Scale each NLA strip to the exact scene duration; repeating cannot shorten
  # it, and would cause strips to overlap and abort the Blender render.
  st.repeat=1
  st.scale=((t1-t0)*FPS)/length
  assert abs((st.frame_end-st.frame_start)-(t1-t0)*FPS)<=1.01,(name,clipname,st.frame_start,st.frame_end)
  st.extrapolation='NOTHING';st.blend_type='REPLACE'
 for seconds,px,py in [(0,x,y),(6,x,y),(12,x*.77,y+.3),
                        (24,x*.77,y+.3),(32,x*.55,y+1.05),(40,x*.55,y+1.05)]:
  root.location=(px,py,0)
  root.keyframe_insert('location',frame=max(1,min(END,1+seconds*FPS)))
 actors.append(name)
 print('ROBOT_REAL',name,'huesos',len(rig.pose.bones),'clips',sorted(clips))

def area(name,xyz,energy,color,size):
 bpy.ops.object.light_add(type='AREA',location=xyz)
 lamp=bpy.context.object;lamp.name=name;lamp.data.energy=energy
 lamp.data.color=color;lamp.data.size=size
 lamp.rotation_euler=(Vector((0,0,1))-lamp.location).to_track_quat('-Z','Y').to_euler()
area('Luz lateral azul',(-5,-5,8),1250,(.45,.7,1),8)
area('Luz de contraluz',(5,5,7),1200,(1,.6,.35),7)
area('Luz general',(0,-6,9),900,(1,1,1),9)

bpy.ops.object.camera_add(location=(0,-14,7))
cam=bpy.context.object;cam.name='DIRECTOR: 8 tomas cinematográficas';sc.camera=cam
cam.data.lens=32;cam.data.clip_end=200
shots=[
 (0,5,(0,-15,7),(2,-13,6),(0,1,1),(0,1,1),24),
 (5,11,(-6,-10,4),(-3,-8,3.5),(-1,0,1.4),(-1,1,1.4),34),
 (11,17,(0,-6,3),(0,-3.6,2.3),(0,2.1,.9),(0,2.1,.9),50),
 (17,22,(5,-4,4),(2.5,-5,3),(1,0,1.5),(1,0,1.5),45),
 (22,26,(1,4,8),(0,3,11),(0,.5,0),(0,.5,0),28),
 (26,32,(-6,-7,3),(-4,-5,2.5),(-2,0,1.4),(0,2,1.5),34),
 (32,36,(0,-9,5),(-2,-6,4),(0,1,1.2),(0,2,1),38),
 (36,40,(0,-6,3.7),(0,-15,7.2),(0,2.1,1),(0,1,1.3),29)]
def keycam(f,pos,look,lens):
 cam.location=Vector(pos);cam.rotation_euler=(Vector(look)-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.data.lens=lens
 cam.keyframe_insert('location',frame=f)
 cam.keyframe_insert('rotation_euler',frame=f)
 cam.data.keyframe_insert('lens',frame=f)
for a,b,p0,p1,l0,l1,lens in shots:
 keycam(1+a*FPS,p0,l0,lens)
 keycam(min(END,b*FPS),p1,l1,lens)
ends={min(END,b*FPS) for a,b,*_ in shots}
for fc in cam.animation_data.action.fcurves:
 for k in fc.keyframe_points:
  k.interpolation='CONSTANT' if round(k.co.x) in ends else 'LINEAR'
sc.frame_set(1)
report={'titulo':'El último pulso','duracion_objetivo_segundos':40,
        'fps_render':FPS,'fps_mp4':24,'robots':actors,
        'camaras_cinematograficas':len(shots),'modelo':'GLB articulados originales',
        'narracion':'No incluida: se requiere voz real Gemini Charon a velocidad 1.2',
        'audio':'Banda sonora sintetizada original para demostración técnica',
        'estado':'Renderizar secuencia 3D y montar MP4 con ffmpeg'}
(out/'informe_produccion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('VALIDACION_ESCENA_3D',len(actors),'robots',len(shots),'tomas',END,'frames')
bpy.ops.render.render(animation=True)
print('RENDER_3D_COMPLETADO',END)
