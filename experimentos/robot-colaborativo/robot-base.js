/**
 * Copia experimental, independiente, del lenguaje visual de robots2.js.
 * No modifica ni reemplaza el robot original de Claude.
 * Convención de articulaciones compartida con Claude: userData.body, head, arms[2], feet[2].
 */
import * as THREE from 'three';

const shell = (color, extra = {}) => new THREE.MeshPhysicalMaterial({
  color, roughness: .27, metalness: .09, clearcoat: 1, clearcoatRoughness: .15, ...extra
});
const basic = color => new THREE.MeshBasicMaterial({color, toneMapped:false});

function part(parent, geo, mat, x=0,y=0,z=0) {
  const mesh = new THREE.Mesh(geo,mat);
  mesh.position.set(x,y,z); mesh.castShadow=true; mesh.receiveShadow=true;
  parent.add(mesh); return mesh;
}
function badgeTexture() {
  const c=document.createElement('canvas'); c.width=c.height=256;
  const ctx=c.getContext('2d');
  ctx.fillStyle='#087b64';ctx.beginPath();ctx.roundRect(5,5,246,246,48);ctx.fill();
  ctx.strokeStyle='#91ffdc';ctx.lineWidth=9;
  for(let n=0;n<6;n++){ctx.save();ctx.translate(128,128);ctx.rotate(n*Math.PI/3);
    ctx.beginPath();ctx.ellipse(0,-45,23,49,0,0,Math.PI*2);ctx.stroke();ctx.restore();}
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(128,128,18,0,Math.PI*2);ctx.fill();
  const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;return tex;
}

export function crearRobotChatGPT(){
  const root=new THREE.Group();root.name='robot-chatgpt-prueba';
  const body=new THREE.Group();root.add(body);body.name='cuerpo';
  const white=shell(0xf5f7fc), green=shell(0x22cda1), trim=shell(0x85ffe0,{metalness:.25});
  const visor=shell(0x080f20,{roughness:.09,metalness:.28,clearcoat:1});
  // Torso y placa, basados en la misma silueta chibi que robots2.js.
  const torso=part(body,new THREE.SphereGeometry(.27,48,32),white,0,.48,0);torso.scale.set(1,1.07,.89);
  const cintura=part(body,new THREE.TorusGeometry(.236,.03,12,48),green,0,.30,0);cintura.rotation.x=Math.PI/2;
  const badge=part(body,new THREE.PlaneGeometry(.18,.18),new THREE.MeshStandardMaterial({map:badgeTexture(),roughness:.35}),0,.49,.248);badge.rotation.x=-.06;
  // Cabeza sobredimensionada, visor oscuro y ojos luminosos.
  const head=new THREE.Group();head.name='cabeza';head.position.set(0,1,0);body.add(head);
  const helmet=part(head,new THREE.SphereGeometry(.39,56,40),white,0,.015,0);helmet.scale.set(1.10,.95,1);
  const crown=part(head,new THREE.SphereGeometry(.393,56,40,0,Math.PI*2,0,.80),green,0,.018,0);crown.scale.set(1.10,.95,1);
  crown.rotation.x=-.20;
  const shield=part(head,new THREE.SphereGeometry(.345,56,40),visor,0,-.038,.084);shield.scale.set(1.08,.75,.94);
  const eyes=[];
  for(const side of [-1,1]){
    const eye=part(head,new THREE.SphereGeometry(.055,24,16),basic(0x6fffe2),side*.142,-.059,.407);
    eye.scale.set(1.22,.66,.40);eyes.push(eye);
    const glow=part(head,new THREE.SphereGeometry(.078,20,12),new THREE.MeshBasicMaterial({color:0x4effc4,transparent:true,opacity:.11,depthWrite:false}),side*.142,-.059,.400);
    glow.scale.set(1.45,.72,.15);
  }
  const mouth=part(head,new THREE.TorusGeometry(.044,.008,8,24,Math.PI),basic(0x6fffe2),0,-.164,.409);
  mouth.rotation.z=Math.PI;mouth.visible=false;
  // Auriculares verdes; elemento distintivo del robot ChatGPT original.
  for(const side of [-1,1]){
    const cup=part(head,new THREE.CylinderGeometry(.132,.132,.079,36),white,side*.414,-.016,0);cup.rotation.z=Math.PI/2;
    const ring=part(head,new THREE.TorusGeometry(.108,.023,12,40),green,side*.462,-.016,0);ring.rotation.y=Math.PI/2;
    const disc=part(head,new THREE.CylinderGeometry(.074,.074,.012,28),trim,side*.465,-.016,0);disc.rotation.z=Math.PI/2;
  }
  const arc=part(head,new THREE.TorusGeometry(.413,.024,12,48,Math.PI),green,0,.005,0);arc.rotation.z=0;
  const arms=[];
  for(const side of [-1,1]){
    const joint=new THREE.Group();joint.name=side<0?'brazo-izquierdo':'brazo-derecho';
    joint.position.set(side*.29,.65,0);body.add(joint);
    const upper=part(joint,new THREE.CapsuleGeometry(.068,.19,8,16),green,side*.072,-.154,.012);upper.rotation.z=side*.20;
    part(joint,new THREE.SphereGeometry(.087,24,16),white,side*.11,-.31,.035);
    arms.push(joint);
  }
  const feet=[];
  for(const side of [-1,1]){
    const pivot=new THREE.Group();pivot.name=side<0?'pie-izquierdo':'pie-derecho';
    pivot.position.set(side*.14,.125,.035);root.add(pivot);
    const foot=part(pivot,new THREE.SphereGeometry(.118,24,16),green,0,0,.065);foot.scale.set(1,.66,1.36);
    feet.push(pivot);
  }
  root.userData={body,head,arms,feet,eyes,mouth,blink:0,robotId:'chatgpt',revision:'experimento-1'};
  return root;
}
