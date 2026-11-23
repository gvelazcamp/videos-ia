// Destino 3D procedural para Camino de la Serpiente.
// No modifica la escena existente ni requiere PNG, Remove.bg o descargas.
export function createKaioGoal(THREE,scene,path){
 const goalT=1009, landing=path(1016);
 const center=landing.clone().add(new THREE.Vector3(0,-18,-17));
 const planet=new THREE.Group();planet.position.copy(center);scene.add(planet);
 const mat=(color,extra={})=>new THREE.MeshStandardMaterial({color,roughness:.86,fog:false,...extra});
 const sphere=(parent,r,x,y,z,m,segments=24)=>{
  const o=new THREE.Mesh(new THREE.SphereGeometry(r,segments,16),m);
  o.position.set(x,y,z);parent.add(o);return o;
 };
 const cube=(parent,w,h,d,x,y,z,m)=>{
  const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);
  o.position.set(x,y,z);parent.add(o);return o;
 };
 const tube=(parent,r1,r2,h,x,y,z,m)=>{
  const o=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,12),m);
  o.position.set(x,y,z);parent.add(o);return o;
 };
 const grass=mat(0x80cf43),trim=mat(0xeaca48),wood=mat(0x956028);
 const R=22;
 sphere(planet,R,0,0,0,grass,48);
 sphere(planet,R*1.045,0,0,0,new THREE.MeshBasicMaterial({color:0xb3f78b,transparent:true,opacity:.085,depthWrite:false,fog:false}),40);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(23,.38,7,72),
  new THREE.MeshBasicMaterial({color:0xe4ff9c,transparent:true,opacity:.45,fog:false}));
 rim.rotation.set(.25,.34,0);planet.add(rim);
 const surface=(x,z)=>Math.sqrt(Math.max(0,R*R-x*x-z*z));
 // Casa pequeña con techo rojo y ventanas.
 const home=new THREE.Group();home.position.set(-8,surface(-8,-4),-4);planet.add(home);
 cube(home,10,6.7,8,0,3.35,0,mat(0xf8e9cb));
 const roof=new THREE.Mesh(new THREE.ConeGeometry(7.75,4.1,4),mat(0xd34130));
 roof.rotation.y=Math.PI/4;roof.position.y=8.7;home.add(roof);
 cube(home,2.2,4.1,.22,0,2.1,4.15,mat(0x845533));
 for(const x of [-3.1,3.1]){
  cube(home,1.9,1.7,.24,x,4.5,4.14,mat(0x8be2fc));
  cube(home,.17,1.7,.32,x,4.5,4.33,mat(0xffffff));
 }
 // Árbol y autito rojo.
 const tree=new THREE.Group();tree.position.set(10,surface(10,-3.8),-3.8);planet.add(tree);
 tube(tree,.9,1.1,7,0,3.6,0,wood);
 sphere(tree,4.6,0,8.5,0,mat(0x218a44));
 sphere(tree,3.1,-2.2,7.6,1.2,mat(0x34ad57));
 const car=new THREE.Group();car.position.set(-2,surface(-2,-9),-9);car.rotation.y=-.32;planet.add(car);
 cube(car,6.1,1.7,3.4,0,1.7,0,mat(0xdb302d));
 cube(car,3.25,1.5,3.1,-.5,3,0,mat(0xf66041));
 cube(car,2.2,.85,3.2,-.5,3.2,.05,mat(0x8bd6ed));
 for(const x of [-2.1,2.1])for(const z of [-1.7,1.7]){
  const wheel=new THREE.Mesh(new THREE.CylinderGeometry(.76,.76,.5,14),mat(0x242432));
  wheel.rotation.x=Math.PI/2;wheel.position.set(x,.95,z);car.add(wheel);
 }
 // Kaio-sama estilizado, cuerpo redondo oscuro, cara azul, gafas y antenas.
 // Se ubica en el extremo frontal para verlo al llegar.
 const kaio=new THREE.Group();kaio.position.set(4,surface(4,9.2)+.2,9.2);planet.add(kaio);
 const dark=mat(0x171932),blue=mat(0x5aafe8),black=mat(0x090d18,.32),gold=mat(0xe7ab3e);
 sphere(kaio,2.7,0,3.1,0,dark);
 sphere(kaio,2.1,0,7,0,blue);
 for(const side of [-1,1]){
  sphere(kaio,.8,side*2.02,7,0,blue);
  sphere(kaio,1.02,side*.98,7.16,1.76,black);
  const arm=tube(kaio,.76,.86,3.4,side*2.5,3.45,0,dark);arm.rotation.z=side*.33;
  sphere(kaio,.88,side*3,1.83,.3,blue);
  tube(kaio,1,1.05,1.45,side*1.15,.84,0,dark);
  const curve=new THREE.CatmullRomCurve3([
    new THREE.Vector3(side*.85,8.55,0),
    new THREE.Vector3(side*1.12,10.8,.1),
    new THREE.Vector3(side*1.65,12.3,.5)]);
  kaio.add(new THREE.Mesh(new THREE.TubeGeometry(curve,12,.12,6),black));
  sphere(kaio,.32,side*1.65,12.3,.5,black,12);
 }
 cube(kaio,.52,.2,.2,0,7.14,2.05,black);
 sphere(kaio,.6,0,6.24,2.03,blue);
 sphere(kaio,.84,-.82,5.88,1.76,black);
 sphere(kaio,.84,.82,5.88,1.76,black);
 const belt=new THREE.Mesh(new THREE.TorusGeometry(2.38,.20,8,30),gold);
 belt.rotation.x=Math.PI/2;belt.position.y=3.9;kaio.add(belt);
 sphere(kaio,.88,0,4.7,2.66,gold);
 sphere(kaio,.47,0,4.73,3.34,dark);
 // Puerta simbólica al final del camino, sin obstáculos en la ruta.
 const finish=new THREE.Group();finish.position.copy(path(goalT));scene.add(finish);
 for(const s of [-1,1]){
  tube(finish,.34,.34,7,s*5,3.5,0,trim);
  sphere(finish,.55,s*5,7.1,0,trim);
 }
 cube(finish,10,.65,.65,0,7.38,0,trim);
 const lamp=new THREE.PointLight(0xffeed0,75,135,2);
 lamp.position.copy(center).add(new THREE.Vector3(0,29,23));scene.add(lamp);
 return {center,goalT,planet,kaio};
}
