// Destino 3D procedural para Camino de la Serpiente.
// No modifica la escena existente ni requiere PNG, Remove.bg o descargas.
export function createKaioGoal(THREE,scene,path){
 const goalT=1009, landing=path(1016);
 // Planeta ADELANTE del corredor y POR ENCIMA de las nubes.
 // Antes estaba 18 metros por debajo del camino y se ocultaba bajo las nubes.
 const center=landing.clone().add(new THREE.Vector3(0,14,-24));
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
 const grass=mat(0x69bc35),trim=mat(0xf1e5bf),wood=mat(0x956028);
 const R=22;
 sphere(planet,R,0,0,0,grass,56);
 // Camino de ladrillos blancos que rodea el planeta, pegado a su superficie.
 // Geometría real, NO billboard plano; vista desde cualquier ángulo.
 const band=new THREE.Group();band.rotation.z=-.27;planet.add(band);
 const bandGeometry=new THREE.SphereGeometry(R+.095,72,10,0,Math.PI*2,Math.PI/2-.122,.244);
 const bandMaterial=mat(0xeae7d5,{side:THREE.DoubleSide});
 band.add(new THREE.Mesh(bandGeometry,bandMaterial));
 // Rayas de las baldosas para reconocer la pista circular.
 const seams=mat(0xbdb5a2,{side:THREE.DoubleSide});
 for(let i=0;i<80;i++){
  const a=i*Math.PI*2/80,pts=[];
  for(let j=0;j<=5;j++){
   const phi=-.120+j*.048,r=R+.16;
   pts.push(new THREE.Vector3(r*Math.cos(phi)*Math.cos(a),
    r*Math.sin(phi),r*Math.cos(phi)*Math.sin(a)));
  }
  const seam=new THREE.Mesh(
   new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),5,.043,4,false),seams);
  band.add(seam);
 }
 // Aro del camino visible desde el frente sin transparencias que oculten edificios.
 const rim=new THREE.Mesh(new THREE.TorusGeometry(R+.10,.13,7,100),trim);
 rim.rotation.x=Math.PI/2;rim.rotation.z=.16;planet.add(rim);
 const surface=(x,z)=>Math.sqrt(Math.max(0,R*R-x*x-z*z));
 // Casita AMARILLA de cúpula redonda, como el planeta de Kaio-sama.
 function domeHouse(px,pz,scale=1,rotation=0){
  const g=new THREE.Group();g.position.set(px,surface(px,pz),pz);
  g.rotation.y=rotation;g.scale.setScalar(scale);planet.add(g);
  const cream=mat(0xecc665),wall=mat(0xf1d78a),outline=mat(0xf8f2d5);
  const door=mat(0x583671),glass=mat(0x83cbe5),terracotta=mat(0xd3a23b);
  tube(g,5,5,3.15,0,1.58,0,wall);
  const roof=new THREE.Mesh(new THREE.SphereGeometry(5.23,32,16,0,Math.PI*2,0,Math.PI/2),cream);
  roof.position.y=3.07;g.add(roof);
  const crown=tube(g,.55,.70,1.65,0,8.22,0,outline);
  sphere(g,.84,0,9.18,0,terracotta);
  // Puerta arqueada hacia el corredor (z positivo).
  cube(g,2.7,3.0,.28,0,1.65,5.08,outline);
  const entrance=cube(g,2.18,2.62,.34,0,1.49,5.25,door);
  const top=new THREE.Mesh(new THREE.SphereGeometry(1.12,16,8,0,Math.PI*2,0,Math.PI/2),door);
  top.position.set(0,2.82,5.25);g.add(top);
  for(const x of [-3.13,3.13]){
   const window=new THREE.Mesh(new THREE.SphereGeometry(.95,16,10),glass);
   window.scale.set(1,.66,.20);window.position.set(x,3.30,3.72);g.add(window);
  }
  // Placas curvas de la cúpula.
  const ring=new THREE.Mesh(new THREE.TorusGeometry(5.1,.19,8,48),outline);
  ring.rotation.x=Math.PI/2;ring.position.y=3.10;g.add(ring);
  return g;
 }
 domeHouse(-8,7,.76,-.36);
 domeHouse(-10,-7,.53,.55);
 // Árbol y autito rojo.
 const tree=new THREE.Group();tree.position.set(10,surface(10,-4),-4);planet.add(tree);
 tube(tree,.9,1.1,7,0,3.6,0,wood);
 sphere(tree,4.6,0,8.5,0,mat(0x218a44));
 sphere(tree,3.1,-2.2,7.6,1.2,mat(0x34ad57));
 const car=new THREE.Group();car.position.set(-5,surface(-5,12),12);car.rotation.y=-.32;planet.add(car);
 cube(car,6.1,1.7,3.4,0,1.7,0,mat(0xdb302d));
 cube(car,3.25,1.5,3.1,-.5,3,0,mat(0xf66041));
 cube(car,2.2,.85,3.2,-.5,3.2,.05,mat(0x8bd6ed));
 for(const x of [-2.1,2.1])for(const z of [-1.7,1.7]){
  const wheel=new THREE.Mesh(new THREE.CylinderGeometry(.76,.76,.5,14),mat(0x242432));
  wheel.rotation.x=Math.PI/2;wheel.position.set(x,.95,z);car.add(wheel);
 }
 // Kaio-sama estilizado, cuerpo redondo oscuro, cara azul, gafas y antenas.
 // Se ubica en el extremo frontal para verlo al llegar.
 const kaio=new THREE.Group();kaio.position.set(9,surface(9,10)+.2,10);kaio.rotation.y=0;kaio.scale.setScalar(.92);planet.add(kaio);
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
 // Luces para que la esfera y el personaje se distingan desde el corredor.
 const front=new THREE.DirectionalLight(0xfff7de,1.3);
 front.position.copy(center).add(new THREE.Vector3(2,26,55));scene.add(front);
 // Puerta simbólica al final del camino, sin obstáculos en la ruta.
 const finish=new THREE.Group();finish.position.copy(path(goalT));scene.add(finish);
 for(const s of [-1,1]){
  tube(finish,.34,.34,7,s*5,3.5,0,trim);
  sphere(finish,.55,s*5,7.1,0,trim);
 }
 cube(finish,10,.65,.65,0,7.38,0,trim);
 const lamp=new THREE.PointLight(0xffeed0,75,135,2);
 lamp.position.copy(center).add(new THREE.Vector3(0,29,23));scene.add(lamp);
 return {center,goalT,planet,kaio,finish,radius:R};
}
