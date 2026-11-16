import * as THREE from 'three';
import {crearRobotChatGPT} from './robot-base.js';
import {EXPRESIONES,aplicarExpresion} from './expresiones-chatgpt.js';

const canvas=document.getElementById('robot-canvas');
const viewport=document.getElementById('visor');
const message=document.getElementById('estado');
const walkButton=document.getElementById('caminar');
const led=document.getElementById('claude-led');
const claudeStatus=document.getElementById('claude-estado');

let renderer;
try{
 renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'default'});
}catch(err){message.textContent='No se pudo iniciar WebGL en este dispositivo.';throw err;}
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.3;
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(38,1,.1,100);
camera.position.set(2,1.55,4.7);
camera.lookAt(0,.65,0);
scene.add(new THREE.HemisphereLight(0xc5e6ff,0x1b1d42,2.1));
const key=new THREE.DirectionalLight(0xffffff,4);
key.position.set(-2,5,5);key.castShadow=true;key.shadow.mapSize.set(1024,1024);
key.shadow.camera.left=-4;key.shadow.camera.right=4;key.shadow.camera.top=4;key.shadow.camera.bottom=-4;
scene.add(key);
const rim=new THREE.PointLight(0x52ffbe,30,5);rim.position.set(1.8,2,-1.2);scene.add(rim);
const pedestal=new THREE.Group();scene.add(pedestal);
const top=new THREE.Mesh(new THREE.CylinderGeometry(1.15,1.2,.15,64),new THREE.MeshPhysicalMaterial({color:0x363367,metalness:.25,roughness:.3}));
top.position.y=-.02;top.receiveShadow=true;pedestal.add(top);
const ring=new THREE.Mesh(new THREE.TorusGeometry(1.12,.036,12,90),new THREE.MeshBasicMaterial({color:0x3dffcc,toneMapped:false}));
ring.rotation.x=Math.PI/2;ring.position.y=.07;pedestal.add(ring);
const base=new THREE.Mesh(new THREE.CylinderGeometry(1.17,1.13,.25,64),new THREE.MeshStandardMaterial({color:0x211f46,roughness:.6}));
base.position.y=-.18;pedestal.add(base);
const robot=crearRobotChatGPT();robot.position.set(0,.11,0);scene.add(robot);
let expression='contento',walking=false,walkModule=null;
let angle=-.13,dragging=false,lastX=0;
function setExpr(v){expression=v;document.querySelectorAll('[data-expr]').forEach(el=>{
 const active=el.dataset.expr===v;el.setAttribute('aria-pressed',String(active));
});document.querySelector('#mood-name').textContent=v;}
for(const name of EXPRESIONES){
 const b=document.createElement('button');b.type='button';b.className='mood';b.dataset.expr=name;b.textContent=name;
 b.addEventListener('click',()=>setExpr(name));document.getElementById('expresiones').append(b);
}
setExpr(expression);
walkButton.addEventListener('click',()=>{
 if(!walkModule)return;
 walking=!walking;walkButton.textContent=walking?'Detener caminata':'Iniciar caminata';
 walkButton.setAttribute('aria-pressed',String(walking));
});
viewport.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;viewport.setPointerCapture(e.pointerId);});
viewport.addEventListener('pointermove',e=>{if(!dragging)return;angle+=(e.clientX-lastX)*.012;lastX=e.clientX;});
viewport.addEventListener('pointerup',()=>dragging=false);
viewport.addEventListener('pointercancel',()=>dragging=false);
const sizeObserver=new ResizeObserver(()=>{
 const w=Math.max(viewport.clientWidth,100),h=Math.max(viewport.clientHeight,100);
 renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
});sizeObserver.observe(viewport);
// Contrato de integración: Claude agrega SU ARCHIVO sin tocar la parte de ChatGPT.
// Al estar disponible, el visor habilita caminar sin necesidad de rehacer nada.
try{
 const mod=await import('./animacion-claude.js');
 if(typeof mod.aplicarCaminata!=='function')throw Error('Falta aplicarCaminata exportada');
 walkModule=mod;walkButton.disabled=false;walkButton.textContent='Iniciar caminata';led.classList.add('ok');
 claudeStatus.textContent='Módulo de caminata recibido y listo';
}catch(_){
 walkButton.disabled=true;
 claudeStatus.textContent='Pendiente: Claude todavía no entregó su módulo';
}
const clock=new THREE.Clock();
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function animate(){
 const t=clock.getElapsedTime();
 aplicarExpresion(robot,expression,t,{caminando:walking});
 if(walkModule&&walking){
   // Claude anima después de la expresión, para evitar que uno pise al otro.
   walkModule.aplicarCaminata(robot,t,1);
 }else if(!walking){
   // Reset de caminar al volver al reposo, sin modificar la lógica de Claude.
   for(const [i,foot] of robot.userData.feet.entries()){foot.rotation.set(0,0,0);foot.position.set((i===0?-1:1)*.14,.125,.035);}
   robot.userData.body.rotation.set(0,0,0);
   robot.position.x=0;robot.position.y=.11;
 }
 robot.rotation.y=angle+(dragging?0:(reducedMotion?0:Math.sin(t*.5)*.08));
 ring.material.color.setHex(walking?0x57b9ff:0x3dffcc);
 renderer.render(scene,camera);requestAnimationFrame(animate);
}
animate();
message.textContent='Vista previa 3D activa. Elegí una expresión y girá el robot con el dedo.';
