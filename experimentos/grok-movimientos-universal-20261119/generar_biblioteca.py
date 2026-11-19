#!/usr/bin/env python3
"""Banco de animaciones Blender para Grok GRIS riggeado EXISTENTE.
No reconstruye ni sobreescribe el modelo ni los GLB previos.
Requiere Blender 3.x: blender -b -P generar_biblioteca.py -- fuente.glb carpeta_resultado
"""
import bpy, sys, math, json, struct
from pathlib import Path
from mathutils import Euler, Vector, Quaternion

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(argv)!=2:raise SystemExit("Uso: blender -b -P generar_biblioteca.py -- GROK_GRIS.glb DESTINO")
source=Path(argv[0]).resolve();out=Path(argv[1]).resolve()
assert source.is_file(),"Archivo original no encontrado"
out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
rig=next((o for o in bpy.context.scene.objects if o.type=='ARMATURE'),None)
assert rig is not None,"Grok gris original sin armature"
required=['cadera','torso','cabeza']+[part+'_'+side for side in 'LR' for part in ('brazo','antebrazo','mano','pierna','pantorrilla','pie')]
missing=[name for name in required if name not in rig.pose.bones]
assert not missing,"No existen los huesos: "+str(missing)
scene=bpy.context.scene
scene.render.fps=24
scene.frame_start=1
for pb in rig.pose.bones:pb.rotation_mode='QUATERNION'
# Limpiar SOLO los vínculos de animación en la copia de escena importada.
rig.animation_data_clear()
rig.animation_data_create()
actions=[]
frames_per_sec=24

def clip(name,duration,func,loop=False):
 total=int(round(duration*frames_per_sec))
 action=bpy.data.actions.new(name)
 rig.animation_data.action=action
 rig.location=(0,0,0)
 rig.rotation_mode='XYZ'
 for frame in range(1,total+2,2):
  t=(frame-1)/frames_per_sec
  angles,loc,rotation=func(t,duration)
  salute_q=saludo_quaternions(t,duration) if name=='04_Saludar' else {}
  rig.location=loc
  rig.rotation_euler=rotation
  rig.keyframe_insert(data_path='location',frame=frame)
  rig.keyframe_insert(data_path='rotation_euler',frame=frame)
  for pb in rig.pose.bones:
   pb.rotation_quaternion=salute_q.get(pb.name) if pb.name in salute_q else Euler(angles.get(pb.name,(0,0,0)),'XYZ').to_quaternion()
   pb.keyframe_insert(data_path='rotation_quaternion',frame=frame,group='Huesos')
 # Asegurar fotograma final exacto sin disparidad de duración.
 frame=total+1;t=duration
 angles,loc,rotation=func(t,duration)
 salute_q=saludo_quaternions(t,duration) if name=='04_Saludar' else {}
 rig.location=loc;rig.rotation_euler=rotation
 rig.keyframe_insert(data_path='location',frame=frame)
 rig.keyframe_insert(data_path='rotation_euler',frame=frame)
 for pb in rig.pose.bones:
  pb.rotation_quaternion=salute_q.get(pb.name) if pb.name in salute_q else Euler(angles.get(pb.name,(0,0,0)),'XYZ').to_quaternion()
  pb.keyframe_insert(data_path='rotation_quaternion',frame=frame,group='Huesos')
 rig.animation_data.action=None
 track=rig.animation_data.nla_tracks.new()
 track.name=name
 strip=track.strips.new(name,1,action)
 strip.action_frame_start=1
 strip.action_frame_end=total+1
 strip.repeat=1
 strip.blend_type='REPLACE'
 strip.extrapolation='NOTHING'
 actions.append({'nombre':name,'duracion_s':duration,'bucle':bool(loop),'accion':action.name})
 print("CLIP_CLAUDE",name,duration)
def base():
 return {}
def osc(t,duration,cadence):
 return math.sin(2*math.pi*cadence*t)
def caminar(t,d,vel=1.0):
 phase=2*math.pi*1.25*vel*t
 q={}
 for side,off in (('L',0),('R',math.pi)):
  v=math.sin(phase+off)
  q['pierna_'+side]=(.38*v,0,0)
  q['pantorrilla_'+side]=(.09+.53*max(0,-v),0,0)
  q['pie_'+side]=(-.12-.19*max(0,-v),0,0)
  q['brazo_'+side]=(-.44*v,0,0)
  q['antebrazo_'+side]=(-.18-.14*max(0,v),0,0)
  q['mano_'+side]=(.08*v,0,0)
 q['torso']=(-.025,0,.012*math.sin(phase))
 q['cabeza']=(.018,0,-.01*math.sin(phase))
 return q,(0,0,.016*abs(math.sin(phase))), (0,0,0)
def correr(t,d):
 phase=2*math.pi*2.40*t;q={}
 for side,off in (('L',0),('R',math.pi)):
  v=math.sin(phase+off)
  q['pierna_'+side]=(.84*v,0,.05*v)
  q['pantorrilla_'+side]=(.19+.95*max(0,-v),0,0)
  q['pie_'+side]=(-.18-.34*max(0,-v),0,0)
  q['brazo_'+side]=(-.87*v,0,.11*v)
  q['antebrazo_'+side]=(-.29-.38*max(0,-v),0,0)
  q['mano_'+side]=(.14*v,0,0)
 q['torso']=(-.07,0,.025*math.sin(phase))
 q['cabeza']=(.045,0,-.012*math.sin(phase))
 return q,(0,0,.038*abs(math.sin(phase))), (0,0,0)
def idle(t,d):
 pulse=math.sin(t*math.pi*2/2.6)
 return {'torso':(.012*pulse,0,0),'cabeza':(-.014*pulse,0,0)},(0,0,0),(0,0,0)
def saludo(t,d):
 # SOLO gesto de cabeza; brazo, antebrazo y mano se calculan con quaterniones
 # del esqueleto real para que el brazo SUBA, no gire hacia atrás.
 enter=max(0,min(1,t/.38,(d-t)/.38))
 return {'cabeza':(0,0,-.08*enter)},(0,0,0),(0,0,0)

def saludo_quaternions(t,d):
 # La anterior rotación Euler Z giraba el brazo sobre su eje local (torcía
 # el hombro y parecía extenderlo hacia atrás). Apuntar cada segmento a una
 # dirección en el ESPACIO DEL RIG, sin depender del roll local del hueso.
 enter=max(0,min(1,t/.38,(d-t)/.38))
 smooth=enter*enter*(3-2*enter)
 if smooth<=0: return {}
 upper=rig.data.bones['brazo_R']
 lower=rig.data.bones['antebrazo_R']
 upper_rest=(upper.tail_local-upper.head_local).normalized()
 lower_rest=(lower.tail_local-lower.head_local).normalized()
 upper_goal=Vector((-.24,-.33,.23)).normalized() # levantar codo DELANTE del pecho (frente = -Y)
 wave=math.sin(2*math.pi*2.7*t)
 lower_goal=Vector((-.06+.06*wave,-.33,.30)).normalized() # mano alta y visiblemente delante de Claude
 up_global=upper_rest.rotation_difference(upper_goal)
 low_global=lower_rest.rotation_difference(lower_goal)
 up_rest_q=upper.matrix_local.to_quaternion()
 low_rest_q=lower.matrix_local.to_quaternion()
 up_local=(up_rest_q.inverted() @ up_global @ up_rest_q).normalized()
 # Compensar el giro del hueso padre al orientar el antebrazo: su nueva
 # dirección es verdaderamente hacia arriba, no hacia la espalda.
 low_local=(low_rest_q.inverted() @ up_global.inverted() @ low_global @ low_rest_q).normalized()
 identity=Quaternion((1,0,0,0))
 return {
  'brazo_R':identity.slerp(up_local,smooth),
  'antebrazo_R':identity.slerp(low_local,smooth),
  'mano_R':Euler((0,.22*wave*smooth,.08*wave*smooth),'XYZ').to_quaternion(),
 }
def salto(t,d):
 p=t/d
 z=.53*math.sin(math.pi*p) if p<1 else 0
 fold=max(0,math.sin(math.pi*p))
 q={}
 for side in 'LR':
  q['pierna_'+side]=(-.38*fold,0,0)
  q['pantorrilla_'+side]=(.58*fold,0,0)
  q['brazo_'+side]=(-.72*fold,0,(-1 if side=='R' else 1)*.17*fold)
 return q,(0,0,z),(0,0,0)
def girar(t,d,sign):
 p=max(0,min(1,t/d))
 p=p*p*(3-2*p)
 # Giro 90° alrededor del eje vertical Z de Blender, GLB lo convierte a Y.
 return {'torso':(0,0,.08*sign*math.sin(math.pi*p))},(0,0,0),(0,0,sign*math.pi/2*p)
def frenar(t,d):
 p=max(0,min(1,t/d));g=1-p
 q={}
 for side,off in (('L',0),('R',math.pi)):
  q['pierna_'+side]=(.32*math.sin(2*math.pi*1.15*t+off)*g,0,0)
  q['brazo_'+side]=(-.32*math.sin(2*math.pi*1.15*t+off)*g,0,0)
  q['pantorrilla_'+side]=(.12*g,0,0)
 return q,(0,0,0),(0,0,0)
def agarrar(t,d):
 # Cierra la distancia acercando el brazo al frente y levantando el antebrazo.
 p=max(0,min(1,t/d));p=p*p*(3-2*p)
 q={'brazo_R':(-.85*p,0,-.30*p),
    'antebrazo_R':(-.88*p,0,0),
    'mano_R':(.25*p,0,0),
    'cabeza':(.08*p,0,0)}
 return q,(0,0,0),(0,0,0)
def soltar(t,d):
 q,loc,rot=agarrar(d-t,d)
 return q,loc,rot
def sentar(t,d):
 p=max(0,min(1,t/d));p=p*p*(3-2*p)
 q={'cadera':(.15*p,0,0),'torso':(.15*p,0,0)}
 for side in 'LR':
  q['pierna_'+side]=(-1.24*p,0,0)
  q['pantorrilla_'+side]=(1.40*p,0,0)
  q['brazo_'+side]=(-.21*p,0,0)
 return q,(0,0,-.23*p),(0,0,0)
def levantar(t,d):
 return sentar(d-t,d)
def quieto(t,d):
 return {},(0,0,0),(0,0,0)

clip('01_Reposo',2.6,idle,True)
clip('02_Caminar_lento',3.2,caminar,True)
clip('03_Correr',2.0,correr,True)
clip('04_Saludar',2.2,saludo)
clip('05_Girar_izquierda_90',1.1,lambda t,d:girar(t,d,1))
clip('06_Girar_derecha_90',1.1,lambda t,d:girar(t,d,-1))
clip('07_Frenar',.75,frenar)
clip('08_Saltar',1.25,salto)
clip('09_Agarrar_objeto',1.3,agarrar)
clip('10_Soltar_objeto',1.1,soltar)
clip('11_Sentarse',1.3,sentar)
clip('12_Levantarse',1.3,levantar)

rig.animation_data.action=None
scene.frame_set(1)
result=out/'Grok_Gris_Biblioteca_12_Movimientos.glb'
# Blender 3.x: una NLA track con nombre propio se exporta como clip independiente.
bpy.ops.export_scene.gltf(filepath=str(result),export_format='GLB',
 export_animations=True,export_skins=True,export_nla_strips=True)
raw=result.read_bytes()
if raw[:4]!=b'glTF' or struct.unpack_from('<I',raw,8)[0]!=len(raw):
 raise RuntimeError('No se exportó GLB íntegro')
length=struct.unpack_from('<I',raw,12)[0]
meta=json.loads(raw[20:20+length])
found=[a.get('name','') for a in meta.get('animations',[])]
print('GROK_GRIS_CLIPS_EXPORTADOS',found)
if not meta.get('skins') or len(meta['skins'][0]['joints'])<15:
 raise RuntimeError('El GLB nuevo perdió el esqueleto')
if len(found)<len(actions):
 raise RuntimeError(f'No se exportaron 12 animaciones separadas: {found}')
for a in actions:
 if not any(a['nombre'] in name for name in found):
  raise RuntimeError('Animación perdida: '+a['nombre'])
report={'archivo':result.name,'origen':source.name,
        'estado':'CANDIDATO, pendiente de revisión visual',
        'huesos':len(meta['skins'][0]['joints']),
        'clips':actions,
        'clips_exportados':found,
        'integridad':'GLB con skins y animaciones separadas verificado'}
(out/'informe.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('GROK_GRIS_BIBLIOTECA_VERIFICADA',len(found),'animaciones')
# Auditar exclusivamente SALUDAR a mitad de gesto desde frente y 45 grados.
# Las pistas NLA se silencian durante la renderización, sin tocar su exportación.
wave_action=next((x for x in bpy.data.actions if x.name.startswith('04_Saludar')),None)
assert wave_action is not None
for tr in rig.animation_data.nla_tracks: tr.mute=True
rig.animation_data.action=wave_action
scene.frame_set(29)
bpy.context.view_layer.update()
shoulder=rig.matrix_world @ rig.pose.bones['brazo_R'].head
wrist=rig.matrix_world @ rig.pose.bones['antebrazo_R'].tail
print('SALUDO_POSICIONES',tuple(round(v,3) for v in shoulder),tuple(round(v,3) for v in wrist))
assert wrist.z > shoulder.z+.13, 'SALUDAR no levanta la mano por encima del hombro'
assert wrist.y < shoulder.y-.25, 'SALUDAR no lleva la mano hacia el frente (-Y) del cuerpo'
# Dos renders sirven para confirmar la dirección en la propia malla, no solo en huesos.
bpy.ops.object.camera_add(location=(0,-8,2.8))
cam=bpy.context.object;scene.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=3.5
for light_pos,energy in [((-4,-5,6),700),((4,-3,3),450)]:
 bpy.ops.object.light_add(type='AREA',location=light_pos)
 lamp=bpy.context.object;lamp.data.energy=energy;lamp.data.size=3
scene.render.engine='CYCLES';scene.cycles.samples=12
scene.render.resolution_x=450;scene.render.resolution_y=540
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
for name,position in [('saludo_frontal',(0,-8,2.8)),('saludo_45_grados',(5.5,-5.5,2.8))]:
 cam.location=position
 cam.rotation_euler=(Vector((0,0,1.4))-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(out/(name+'.png'))
 bpy.ops.render.render(write_still=True)
 print('SALUDO_RENDER_VALIDADO',name)

