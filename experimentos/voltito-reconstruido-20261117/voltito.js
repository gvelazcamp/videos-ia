// VOLTITO – nueva construcción 3D del personaje a partir de sus vistas.
// No importa ni reutiliza la geometría de voltito-3d-alta-calidad.
// Only the verified, local Three.js library is reused.
import * as T from "../voltito-3d-alta-calidad-20261117/three.module.js";

const el=document.getElementById("visor");
const info=document.getElementById("info");
const bar=document.getElementById("angle");
const degree=document.getElementById("degree");
const estado=document.getElementById("estado");
const autoButton=document.getElementById("auto");
const resetButton=document.getElementById("reset");

const scene=new T.Scene();
const camera=new T.PerspectiveCamera(37,1,.05,120);
camera.position.set(0,2.38,9.1);
camera.lookAt(0,2.13,0);
const renderer=new T.WebGLRenderer({antialias:true,alpha:true,powerPreference:"high-performance"});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
renderer.outputColorSpace=T.SRGBColorSpace;
renderer.toneMapping=T.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.43;
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=T.PCFSoftShadowMap;
el.insertBefore(renderer.domElement,el.firstChild);
scene.add(new T.HemisphereLight(0xe4fff8,0x91734b,2.9));
const mainLight=new T.DirectionalLight(0xffecd0,3.2);
mainLight.position.set(-4,8,7);
mainLight.castShadow=true;
mainLight.shadow.mapSize.set(1024,1024);
mainLight.shadow.camera.left=-6;
mainLight.shadow.camera.right=6;
mainLight.shadow.camera.top=8;
mainLight.shadow.camera.bottom=-6;
mainLight.shadow.bias=-.0003;
scene.add(mainLight);
const rimLight=new T.DirectionalLight(0x64ede2,2.0);
rimLight.position.set(4,3,-5);scene.add(rimLight);
const softLight=new T.PointLight(0xffc77c,14,10);
softLight.position.set(1.6,4,5);scene.add(softLight);

// Palette sampled visually from approved frontal and side/back drawings.
const GOLD=0xffcb55, LIGHTGOLD=0xffd871, SHADOWGOLD=0xe5a835;
const TEAL=0x27dac4, INNER=0x31cbbc, DARKTEAL=0x129f9b;
const FUR=new T.MeshStandardMaterial({color:GOLD,roughness:1,metalness:0});
const HEAD=new T.MeshStandardMaterial({color:LIGHTGOLD,roughness:1,metalness:0});
const TUMMY=new T.MeshStandardMaterial({color:0xffe9cc,roughness:.99});
const EAR=new T.MeshStandardMaterial({color:0xffca59,roughness:.88,side:T.DoubleSide});
const EARDEEP=new T.MeshStandardMaterial({color:INNER,roughness:.68,side:T.DoubleSide});
const EARBONE=new T.MeshStandardMaterial({color:0xe9b45f,roughness:.95});
const TEALMAT=new T.MeshPhysicalMaterial({color:TEAL,metalness:.05,roughness:.24,clearcoat:1,clearcoatRoughness:.17});
const GLOWMAT=new T.MeshPhysicalMaterial({color:0x2beed9,roughness:.2,metalness:.18,clearcoat:1});
const DARKMAT=new T.MeshStandardMaterial({color:DARKTEAL,roughness:.38,metalness:.07});
const PATCH=new T.MeshStandardMaterial({color:0xad754d,roughness:.83});
const NOSE=new T.MeshPhysicalMaterial({color:0x805444,roughness:.5,clearcoat:.12});
const MOUTHCOLOR=new T.MeshStandardMaterial({color:0x4f242e,roughness:.96});
const TONGUE=new T.MeshStandardMaterial({color:0xee8a7a,roughness:.95});
const EYERIM=new T.MeshPhysicalMaterial({color:0x0a223f,roughness:.14,clearcoat:1});
const EYE=new T.MeshPhysicalMaterial({color:0x1263a0,roughness:.10,metalness:.12,clearcoat:1,clearcoatRoughness:.03});
const IRIS=new T.MeshPhysicalMaterial({color:0x159bc6,roughness:.14,clearcoat:.92});
const PUPIL=new T.MeshPhysicalMaterial({color:0x061f38,roughness:.06,clearcoat:1});
const WHITE=new T.MeshBasicMaterial({color:0xffffff});

const model=new T.Group();
scene.add(model);
function obj(n,g,m,x=0,y=0,z=0){
 const a=new T.Mesh(g,m);a.name=n;a.position.set(x,y,z);
 a.castShadow=true;a.receiveShadow=true;model.add(a);return a;
}
function ell(n,m,p,s,seg=44){
 const a=obj(n,new T.SphereGeometry(1,seg,Math.floor(seg*.72)),m,...p);
 a.scale.set(...s);return a;
}
function line(n,points,r,mat){
 const c=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)));
 return obj(n,new T.TubeGeometry(c,points.length*11,r,7,false),mat);
}
function bolt(n,coords,z,thick,mat){
 const s=new T.Shape();
 s.moveTo(coords[0][0],coords[0][1]);
 for(let i=1;i<coords.length;i++)s.lineTo(coords[i][0],coords[i][1]);
 s.closePath();
 const g=new T.ExtrudeGeometry(s,{depth:thick,bevelEnabled:true,steps:1,curveSegments:4,bevelThickness:.027,bevelSize:.033,bevelSegments:3});
 const m=obj(n,g,mat,0,0,z);return m;
}

// Very rounded foot pads, plush body, cream belly, two brown spots.
ell("cuerpo dorado",FUR,[0,1.025,-.05],[.70,.84,.62],58);
ell("vientre color crema",TUMMY,[0,.99,.489],[.49,.66,.233],48);
ell("pecho cremoso",TUMMY,[0,1.48,.47],[.355,.22,.15],30);
for(const s of [-1,1]){
 ell("pie "+s,FUR,[s*.43,.19,.31],[.38,.2,.43],36);
 ell("dedos "+s,HEAD,[s*.48,.13,.65],[.25,.09,.13],28);
 for(let i=0;i<3;i++){
  line("ranura de dedo",[[s*(.23+i*.1),.17,.718],[s*(.26+i*.1),.115,.73]],.006,EARBONE);
 }
 const arm=ell("brazo redondo "+s,FUR,[s*.71,1.16,.14],[.255,.37,.31],36);
 arm.rotation.z=s*.17;
 ell("unión turquesa "+s,DARKMAT,[s*.86,1.08,.175],[.07,.255,.25],28);
 ell("centro de unión "+s,TEALMAT,[s*.9,1.08,.178],[.035,.18,.182],28);
 ell("mancha café "+s,PATCH,[s*.315,1.28,.702],[.151,.114,.047],24);
}

// Head: a separate full rounded 3-D sculpt, not a flat image.
ell("cabeza principal",HEAD,[0,2.51,.025],[.997,.892,.812],66);
ell("cachete izquierdo",HEAD,[-.73,2.17,.25],[.29,.28,.44],34);
ell("cachete derecho",HEAD,[.73,2.17,.25],[.29,.28,.44],34);
ell("hocico amarillo",HEAD,[0,2.15,.722],[.43,.228,.245],38);

// Pair of real volumetric leaf-shaped ears.
// Each ear is curved with two external gold surfaces, gold side thickness,
// inset teal surfaces on BOTH front and rear like the reference.
function leafGeometry(sign,which,inside=false,back=false){
 const N=42,M=16,xyz=[],indices=[];
 const tx=which===0?1.36:1.50;
 const ty=which===0?1.05:1.37;
 const rootX=which===0?.47:.52, rootY=3.18;
 const peakWidth=which===0?.33:.345;
 for(let i=0;i<=N;i++){
  const t=i/N;
  const f=inside?.11+.82*t:t;
  const x=sign*(rootX+tx*f +.05*Math.sin(Math.PI*f));
  const y=rootY+ty*f;
  const z=-.09+.05*f+.055*Math.sin(Math.PI*f);
  const width=peakWidth*Math.pow(Math.max(.00001,Math.sin(Math.PI*f)),.78)*(inside?.68:1);
  const tangentX=tx+.05*Math.PI*Math.cos(Math.PI*f),tangentY=ty;
  const L=Math.hypot(tangentX,tangentY);
  const nx=tangentY/L,ny=-tangentX/L;
  for(let j=0;j<=M;j++){
   const u=2*j/M-1;
   const yy=y+ny*width*u;
   const xx=x+sign*nx*width*u;
   const swell=Math.sqrt(Math.max(0,1-u*u));
   const zz=z+(back?-1:1)*((inside?.105:.075)+(inside?.015:.07)*swell);
   xyz.push(xx,yy,zz);
  }
 }
 for(let i=0;i<N;i++)for(let j=0;j<M;j++){
  const a=i*(M+1)+j,b=a+M+1;
  if(!back)indices.push(a,b,a+1,a+1,b,b+1);
  else indices.push(a,a+1,b,a+1,b+1,b);
 }
 const g=new T.BufferGeometry();
 g.setAttribute("position",new T.Float32BufferAttribute(xyz,3));
 g.setIndex(indices);g.computeVertexNormals();return g;
}
for(let s of [-1,1]){
 const j=s===-1?0:1;
 obj("oreja exterior delantera "+s,leafGeometry(s,j,false,false),EAR);
 obj("oreja exterior posterior "+s,leafGeometry(s,j,false,true),EAR);
 obj("oreja panel turquesa delantero "+s,leafGeometry(s,j,true,false),EARDEEP);
 obj("oreja panel turquesa trasero "+s,leafGeometry(s,j,true,true),EARDEEP);
 // Golden ridge emphasizes the leaf structure.
 for(const back of [false,true]){
   const pts=[];
   for(let k=0;k<=14;k++){
     const f=.16+.68*k/14,rootX=j===0?.47:.52,rootY=3.18;
     const tx=j===0?1.36:1.50,ty=j===0?1.05:1.37;
     pts.push([s*(rootX+tx*f+.05*Math.sin(Math.PI*f)),rootY+ty*f,-.09+.05*f+(back?-.18:.18)]);
   }
   line("nervadura hoja",pts,.012,EARBONE);
 }
}

// Three separate turquoise forehead spikes, built as pointed 3D forms.
function spike(x,h,scale){
 const base=new T.CylinderGeometry(.008,.097,h,15,5);
 const m=obj("copete turquesa",base,TEALMAT,x,3.33+h*.36,.15);
 m.scale.set(scale,1,scale);m.rotation.z=-x*.28;
 ell("punta copete",GLOWMAT,[x,3.33+h*.84,.15],[.021,.035,.024],14);
}
spike(-.166,.35,.85);spike(0,.48,1.08);spike(.17,.35,.85);

// Glossy oversized blue eyes + iris and vivid reflection.
for(const s of [-1,1]){
 const eyex=s*.426;
 const eyeZ=.728;
 ell("contorno ojo azul "+s,EYERIM,[eyex,2.54,eyeZ],[.212,.268,.142],46);
 ell("iris azul "+s,EYE,[eyex,2.535,eyeZ+.105],[.176,.22,.093],38);
 ell("brillo azul "+s,IRIS,[eyex,2.48,eyeZ+.178],[.105,.14,.034],30);
 ell("pupila "+s,PUPIL,[eyex,2.576,eyeZ+.186],[.107,.145,.036],30);
 ell("reflejo blanco "+s,WHITE,[eyex-.059,2.65,eyeZ+.21],[.055,.072,.017],26);
 ell("brillo secundario "+s,WHITE,[eyex+.073,2.447,eyeZ+.215],[.022,.026,.01],16);
 // Each turquoise cheek zigzag has depth and an angular sharp outline.
 const z= .54;
 const xx=s*.72;
 const shape=[
 [xx-s*.15,2.28],[xx+s*.075,2.415],[xx+s*.013,2.293],
 [xx+s*.166,2.305],[xx-s*.067,2.073],[xx-s*.014,2.204]
 ];
 bolt("rayo de mejilla "+s,shape,z,.057,TEALMAT);
}
// Big joyful smile, rose tongue, fang, nose.
ell("boca sonriente",MOUTHCOLOR,[0,2.142,.925],[.255,.205,.061],35);
ell("lengua rosa",TONGUE,[0,2.057,.985],[.155,.077,.029],23);
ell("nariz pequeña",NOSE,[0,2.34,.929],[.08,.056,.039],26);
line("contorno sonrisa",[[ -.26,2.21,.93],[-.15,2.095,.987],[0,2.065,.99],[.16,2.095,.987],[.26,2.21,.93]],.016,NOSE);
const fang=new T.Shape();
fang.moveTo(.125,2.278);fang.lineTo(.19,2.264);fang.lineTo(.155,2.19);fang.closePath();
obj("colmillo",new T.ExtrudeGeometry(fang,{depth:.018,bevelEnabled:false}),WHITE,0,0,.982);

// Bright turquoise forked lightning rod tail, fully extruded and beveled.
// It is anchored behind the torso and remains physical when rotated.
bolt("cola eléctrica segmento base",[
[-.34,.96],[-.49,1.13],[-1.06,1.53],[-1.26,1.43],[-.97,1.09],[-.48,.82]
],-.71,.16,TEALMAT);
bolt("cola eléctrica zeta",[
[-1.02,1.51],[-1.32,1.88],[-1.18,2.08],[-1.66,2.10],[-1.47,1.78],[-1.68,1.55],[-1.3,1.45]
],-.71,.17,GLOWMAT);
bolt("punta bifurcada arriba",[
[-1.55,2.04],[-2.25,2.26],[-2.38,2.17],[-1.95,2.04],[-1.67,2.00]
],-.71,.13,TEALMAT);
bolt("punta bifurcada abajo",[
[-1.65,1.56],[-2.28,1.43],[-2.44,1.32],[-1.81,1.35],[-1.49,1.46]
],-.71,.12,TEALMAT);
ell("anclaje cola",DARKMAT,[-.4,1.04,-.59],[.14,.16,.06],25);
ell("botón cola",GLOWMAT,[-.42,1.04,-.65],[.08,.09,.04],23);

// Dorsal fur is plain gold, as in the back view.
// Fine individual fur fibers produce a non-plastic look without using planes.
let seed=435123;
function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;}
const hairGeo=new T.ConeGeometry(.0037,.025,3,1);
hairGeo.translate(0,.0125,0);
const matHair=new T.MeshStandardMaterial({color:0xffffff,roughness:1,side:T.DoubleSide});
function fibers(name,n,cx,cy,cz,rx,ry,rz,base,variation){
 const im=new T.InstancedMesh(hairGeo,matHair,n);
 im.name=name;
 const instance=new T.Object3D();
 const c0=new T.Color(base),c1=new T.Color(variation);
 const up=new T.Vector3(0,1,0);
 for(let i=0;i<n;i++){
  const a=rand()*2-1,theta=rand()*Math.PI*2;
  const b=Math.sqrt(1-a*a),nx=b*Math.cos(theta),ny=a,nz=b*Math.sin(theta);
  const center=new T.Vector3(cx+nx*rx,cy+ny*ry,cz+nz*rz);
  const normal=new T.Vector3(nx/rx,ny/ry,nz/rz).normalize();
  instance.position.copy(center);
  instance.quaternion.setFromUnitVectors(up,normal);
  instance.scale.setScalar(.52+rand()*.64);
  instance.updateMatrix();im.setMatrixAt(i,instance.matrix);
  const cc=c0.clone().lerp(c1,rand()*.45);im.setColorAt(i,cc);
 }
 im.instanceMatrix.needsUpdate=true;
 im.castShadow=false;
 im.frustumCulled=false;
 model.add(im);
}
fibers("pelaje fino cabeza",9000,0,2.51,.025,.999,.895,.813,0xffd36d,0xeab34a);
fibers("pelaje fino cuerpo",5500,0,1.025,-.05,.702,.842,.624,0xffcb57,0xeab449);
for(const s of [-1,1]){
 fibers("pelaje brazo "+s,1050,s*.71,1.16,.14,.258,.375,.313,0xffc953,0xe7af43);
 fibers("pelaje pie "+s,900,s*.43,.19,.31,.382,.202,.433,0xffc85c,0xe7ad48);
}

// Floor stays stationary while the model turns, its shadow communicates depth.
const base=new T.Mesh(
 new T.CircleGeometry(3.2,90),
 new T.MeshStandardMaterial({color:0x164853,roughness:1,transparent:true,opacity:.54})
);
base.rotation.x=-Math.PI/2;base.position.y=-.013;base.receiveShadow=true;scene.add(base);
const pad=new T.Mesh(new T.CylinderGeometry(1.26,1.37,.11,100),
 new T.MeshStandardMaterial({color:0x12404a,metalness:.24,roughness:.45}));
pad.position.y=-.12;pad.receiveShadow=true;scene.add(pad);
const rim=new T.Mesh(new T.TorusGeometry(1.26,.017,8,100),
 new T.MeshBasicMaterial({color:0x57f3de}));
rim.rotation.x=Math.PI/2;rim.position.y=-.062;scene.add(rim);

let angle=0,autorotate=false,drag=false,lastX=0,lastDist=0,lastT=0;
const fingers=new Map();
function show(){
 const deg=((Math.round(angle*180/Math.PI)%360)+360)%360;
 degree.textContent=deg+"°";bar.value=deg;
 const labels=["Frente","Tres cuartos","Costado","Tres cuartos","Espalda","Tres cuartos","Costado","Tres cuartos"];
 estado.textContent=labels[Math.round(deg/45)%8]+" · reconstrucción 3D nueva";
}
function turn(v){angle=((v%(Math.PI*2))+Math.PI*2)%(Math.PI*2);model.rotation.y=angle;show();}
function resize(){
 const w=el.clientWidth,h=el.clientHeight;
 renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
}
if(typeof ResizeObserver!=="undefined")new ResizeObserver(resize).observe(el);
window.addEventListener("resize",resize);resize();
el.addEventListener("pointerdown",e=>{
 fingers.set(e.pointerId,{x:e.clientX,y:e.clientY});
 drag=true;autorotate=false;autoButton.textContent="▶ Girar";lastX=e.clientX;
 el.setPointerCapture(e.pointerId);
});
el.addEventListener("pointermove",e=>{
 if(!fingers.has(e.pointerId))return;
 fingers.set(e.pointerId,{x:e.clientX,y:e.clientY});
 if(fingers.size===2){
  const [a,b]=[...fingers.values()];
  const dist=Math.hypot(a.x-b.x,a.y-b.y);
  if(lastDist>0)camera.position.z=T.MathUtils.clamp(camera.position.z+(lastDist-dist)*.02,6.3,13.5);
  lastDist=dist;return;
 }
 lastDist=0;
 const dx=e.clientX-lastX;lastX=e.clientX;turn(angle+dx*.013);
});
for(const event of ["pointerup","pointercancel","lostpointercapture"]){
 el.addEventListener(event,e=>{fingers.delete(e.pointerId);lastDist=0;drag=fingers.size>0;});
}
bar.addEventListener("input",()=>{autorotate=false;autoButton.textContent="▶ Girar";turn(+bar.value*Math.PI/180);});
autoButton.addEventListener("click",()=>{autorotate=!autorotate;autoButton.textContent=autorotate?"Ⅱ Pausar":"▶ Girar";});
resetButton.addEventListener("click",()=>{autorotate=false;autoButton.textContent="▶ Girar";camera.position.z=9.1;turn(0);});
function tick(t){if(autorotate&&lastT)turn(angle+(t-lastT)*.00062);lastT=t;renderer.render(scene,camera);requestAnimationFrame(tick);}
info.style.display="none";
turn(0);requestAnimationFrame(tick);
// Diagnostic hook used only to validate true 3D in automated Chrome screenshots.
window.__VOLTITO_RECONSTRUCCION__={
 getMeshCount:()=>model.children.filter(c=>c.isMesh||c.isInstancedMesh).length,
 getRotation:()=>model.rotation.y,
 geometryInfo:()=>({group:1,meshCount:model.children.length,head:model.getObjectByName("cabeza principal")?.isMesh,
 ears:model.children.filter(c=>c.name.startsWith("oreja exterior")).length,fur:model.children.filter(c=>c.isInstancedMesh).length})
};
