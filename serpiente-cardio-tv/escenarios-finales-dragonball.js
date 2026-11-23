// Escenarios de llegada construidos con geometria real THREE.js.
// Se crean solamente al elegir un trayecto. No modifica el Camino original.
import {createKaioGoal} from './planeta-kaio-multiruta.js';

export function createDestinationWorld(THREE,scene,path,km){
 const owned=[];
 const group=new THREE.Group();scene.add(group);
 const mat=(color,props={})=>new THREE.MeshStandardMaterial({color,roughness:.82,...props});
 const grass=mat(0x5db849),darkGrass=mat(0x348a42),sand=mat(0xf4d18a),
   white=mat(0xf4f5e4),stone=mat(0x9c8d70),glass=mat(0x419bc9,{metalness:.2,roughness:.32}),
   brown=mat(0x82542e),red=mat(0xd7523b),bark=mat(0x795132);
 const part=(parent,geometry,material,x=0,y=0,z=0)=>{
  const o=new THREE.Mesh(geometry,material);o.position.set(x,y,z);parent.add(o);return o;
 };
 const box=(parent,w,h,d,x,y,z,m)=>part(parent,new THREE.BoxGeometry(w,h,d),m,x,y,z);
 const ball=(parent,r,x,y,z,m,detail=22)=>part(parent,new THREE.SphereGeometry(r,detail,14),m,x,y,z);
 const cylinder=(parent,rt,rb,h,x,y,z,m,n=24)=>part(parent,new THREE.CylinderGeometry(rt,rb,h,n),m,x,y,z);
 const ellipsoid=(parent,w,h,d,x,y,z,m)=>{
  const o=ball(parent,1,x,y,z,m,36);o.scale.set(w,h,d);return o;
 };
 function sign(parent,label,w,x,y,z,color=0x183c57){
  const c=document.createElement('canvas');c.width=512;c.height=140;
  const ctx=c.getContext('2d');ctx.clearRect(0,0,512,140);
  ctx.fillStyle='#f8f7e8';ctx.fillRect(0,0,512,140);
  ctx.strokeStyle='#26475b';ctx.lineWidth=12;ctx.strokeRect(5,5,502,130);
  ctx.fillStyle='#183c57';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.font='bold 62px system-ui';ctx.fillText(label,256,71,470);
  const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;
  const p=part(parent,new THREE.PlaneGeometry(w,w*140/512),
    new THREE.MeshBasicMaterial({map:texture,transparent:true,side:THREE.DoubleSide}),x,y,z);
  owned.push(texture);return p;
 }
 function leafyTree(parent,x,z,scale=1){
  const g=new THREE.Group();g.position.set(x,1,z);g.scale.setScalar(scale);parent.add(g);
  cylinder(g,.8,1.05,7,0,3.5,0,bark);
  ellipsoid(g,4.4,4.2,4.3,0,9,0,darkGrass);
  ball(g,2.8,-2,8,1,grass);ball(g,2.6,2,10,-.8,grass);
 }
 function palm(parent,x,z,scale=1){
  const g=new THREE.Group();g.position.set(x,1,z);g.scale.setScalar(scale);parent.add(g);
  const trunk=cylinder(g,.46,.85,10,0,5.2,0,bark,12);trunk.rotation.z=.1;
  for(let i=0;i<7;i++){
   const a=i*Math.PI*2/7;
   const leaf=ellipsoid(g,4.8,.43,1.45,Math.sin(a)*3.35,10,Math.cos(a)*3.35,grass);
   leaf.rotation.y=a;leaf.rotation.z=Math.sin(a)*.24;
  }
  ball(g,1.15,0,10.3,0,grass);
 }
 // Colocar cada mundo alineado con el extremo del camino seleccionado.
 const origin=path(km*1000+21);
 group.position.copy(origin);
 let focus=origin.clone().add(new THREE.Vector3(0,8,-5));
 if(km===10){
  // Reutilizar el planeta 3D existente, ahora en la meta de 10 km.
  scene.remove(group);
  const kaio=createKaioGoal(THREE,scene,t=>path(t+9000));
  kaio.finish.visible=false;
  // Suavizar el encuentro entre el borde frontal del planeta y el corredor.
  kaio.planet.position.y-=7;
  kaio.center.y-=7;
  // La referencia a Kaio 3D se conserva como respaldo.
  const pos=new THREE.Vector3();kaio.kaio.getWorldPosition(pos);
  const loader=new THREE.TextureLoader();
  loader.load('./assets-kaio/kaio-real.webp',texture=>{
   if(!kaio.planet.parent)return;
   texture.colorSpace=THREE.SRGBColorSpace;
   owned.push(texture);
   const width=texture.image?.width||500,height=texture.image?.height||700;
   const sprite=new THREE.Sprite(new THREE.SpriteMaterial({
    map:texture,transparent:true,alphaTest:.02,depthWrite:false
   }));
   const heightOnPlanet=9.5;
   sprite.scale.set(heightOnPlanet*width/height,heightOnPlanet,1);
   const cx=8,cz=17,r=kaio.radius;
   const cy=Math.sqrt(r*r-cx*cx-cz*cz);
   sprite.position.copy(kaio.center).add(new THREE.Vector3(cx,cy+heightOnPlanet*.50+.2,cz+.9));
   scene.add(sprite);
   kaio.kaio.visible=false;
   kaio._illustration=sprite;
  },undefined,()=>{});
  focus.copy(kaio.center).add(new THREE.Vector3(0,7,0));
  return {group:kaio.planet,focus,dispose(){
   if(kaio._illustration)scene.remove(kaio._illustration);
   scene.remove(kaio.planet);scene.remove(kaio.finish);
   for(const x of owned)x.dispose?.();
  }};
 }
 const isKame=km===15,isBulma=km===5;
 // Isla / parque completo: suelo, subsuelo y ambiente del destino.
 ellipsoid(group,isBulma?33:25,4,isBulma?28:23,0,-3.2,-3,isKame?sand:grass);
 ellipsoid(group,isBulma?33:25,2.8,isBulma?28:23,0,-6,-3,stone);
 if(isKame){
  cylinder(group,33,33,.65,0,-5.9,-3,mat(0x30b6d8,{transparent:true,opacity:.80}),48);
  ellipsoid(group,27,2,24,0,-3.5,-3,sand);
  // Casita rosa sobre la isla.
  box(group,15,10,12,0,6,-8,mat(0xf3a7b7));
  const roof=part(group,new THREE.ConeGeometry(11.6,6.2,4),red,0,13.8,-8);
  roof.rotation.y=Math.PI/4;
  box(group,3,5,.3,0,3.5,-1.83,brown);
  for(const x of [-4.5,4.5]){
   box(group,2.3,2.3,.28,x,7,-1.8,white);
   box(group,1.65,1.65,.32,x,7,-1.6,glass);
  }
  sign(group,'KAME HOUSE',14,0,11,-1.65);
  palm(group,-14,-9,.85);palm(group,14,-10,1);
  palm(group,-19,4,.7);
  focus=origin.clone().add(new THREE.Vector3(0,8,-9));
 }else if(isBulma){
  // Capsule Corp, edificio en cúpula con dos torres y ventanas.
  cylinder(group,16.5,17,11,0,6,-9,mat(0xf3db8c),38);
  const cap=part(group,new THREE.SphereGeometry(16.5,38,18,0,Math.PI*2,0,Math.PI/2),
    mat(0xead191),0,11.2,-9);
  const belt=cylinder(group,17,17,1,0,10,-9,mat(0x7d9aa6),38);
  for(let i=0;i<14;i++){
   const a=(i/14)*Math.PI*2;
   const x=Math.sin(a)*16.4,z=-9+Math.cos(a)*16.4;
   const panel=box(group,4.2,2.4,.35,x,8.2,z,glass);
   panel.rotation.y=a;
  }
  for(const x of [-13.4,13.4]){
   cylinder(group,4.2,4.2,22,x,11,-9,mat(0xeacf89),18);
   cylinder(group,4.45,4.45,.9,x,22,-9,mat(0x657783),18);
   box(group,3.2,2,.5,x,16,-4.8,glass);
  }
  box(group,5.4,6,.55,0,3,7.7,mat(0xba5c61));
  sign(group,'CAPSULE',13,0,11.6,7.95);
  leafyTree(group,-24,-9,.75);leafyTree(group,23,-13,.86);
  focus=origin.clone().add(new THREE.Vector3(0,12,-7));
 }else if(km===20){
  // Casa de Goku: vivienda blanca redondeada y anexo naranja, árboles.
  const house=ellipsoid(group,12.5,10.5,10.5,0,8,-7,white);
  cylinder(group,11.2,11.2,3.5,0,4,-7,white,28);
  const side=box(group,12,8,11,-11,5,-7,mat(0xe9b37c));
  const sideRoof=part(group,new THREE.ConeGeometry(9.2,5.2,4),mat(0xd57c49),-11,11.5,-7);
  sideRoof.rotation.y=Math.PI/4;
  const front=box(group,4.3,7,.4,0,3.5,3,stone);
  box(group,3.1,5.8,.5,0,3,3.25,mat(0x95643b));
  for(const x of [-7,7]){
   const glassPane=box(group,3.3,3.1,.35,x,8,1.5,glass);
   glassPane.rotation.y=x<0?-.45:.45;
  }
  sign(group,'CASA GOKU',10,0,14,3.5);
  leafyTree(group,20,-9,1.4);
  leafyTree(group,-22,-17,.95);
  leafyTree(group,19,10,.7);
  focus=origin.clone().add(new THREE.Vector3(0,9,-6));
 }
 // Sendero corto que enlaza físicamente la carretera con la isla.
 const walkway=box(group,8.2,.28,27,0,.25,12.5,isKame?sand:white);
 for(let j=0;j<13;j++){
  box(group,8.15,.08,.12,0,.44,0+j*2.1,mat(0x9aa3a6));
 }
 // Vegetación y luces de llegada, sin carteles gigantes flotantes.
 const light=new THREE.PointLight(0xffedbb,42,145,2);
 light.position.set(0,20,13);group.add(light);
 return {group,focus,dispose(){
  scene.remove(group);
  group.traverse(o=>{o.geometry?.dispose?.();});
  for(const x of owned)x.dispose?.();
 }};
}
