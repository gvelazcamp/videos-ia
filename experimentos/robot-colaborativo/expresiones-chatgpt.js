/**
 * Área de ChatGPT: expresiones faciales y gestos.
 * INTERFAZ: aplicarExpresion(bot, nombre, segundos, {caminando:boolean})
 * NO editar animacion-claude.js; Claude será su responsable.
 */
export const EXPRESIONES=['contento','pensando','sorprendido','festejando','triste','hablando'];

function pulso(t, velocidad=1){return Math.sin(t*velocidad);}
function parpadeo(t){
  // Cierre muy breve cada ~3.6 s; la fase varía suavemente para no verse mecánico.
  const fase=(t+.22*Math.sin(t*.29))%3.6;
  return fase>3.39?Math.max(.06,Math.abs(fase-3.48)/.09):1;
}
export function aplicarExpresion(bot,nombre,t,{caminando=false}={}){
  const u=bot.userData;
  if(!u?.head||!u?.eyes||!u?.arms)throw Error('Robot incompatible: faltan head, eyes o arms en userData');
  const expr=EXPRESIONES.includes(nombre)?nombre:'contento';
  const [izq,der]=u.eyes;
  // Reiniciar solamente propiedades gestionadas por este módulo.
  u.head.rotation.set(0,0,0);
  u.mouth.visible=false;
  izq.position.y=der.position.y=-.059;
  izq.scale.set(1.22,.66,.40);der.scale.set(1.22,.66,.40);
  izq.rotation.z=der.rotation.z=0;
  if(!caminando){
    for(const arm of u.arms)arm.rotation.set(0,0,0);
    u.body.position.y=0;
  }
  if(expr==='contento'){
    u.head.rotation.z=.045*pulso(t,2.3);
    if(!caminando)u.body.position.y=.013*(1+pulso(t,3));
  }
  if(expr==='pensando'){
    u.head.rotation.z=-.14;u.head.rotation.y=.14;
    izq.scale.y=.32;der.scale.y=.41;
    if(!caminando)u.arms[1].rotation.set(-.65,0,1.25);
  }
  if(expr==='sorprendido'){
    izq.scale.y=der.scale.y=1.22;u.mouth.visible=true;
    u.head.rotation.x=-.11;
    if(!caminando){u.arms[0].rotation.z=-1.7;u.arms[1].rotation.z=1.7;}
  }
  if(expr==='festejando'){
    u.head.rotation.z=.12*pulso(t,6);
    if(!caminando){u.body.position.y=Math.abs(pulso(t,5.5))*.10;u.arms[0].rotation.z=-2.5;u.arms[1].rotation.z=2.5;}
  }
  if(expr==='triste'){
    izq.scale.y=der.scale.y=.28;
    izq.rotation.z=.18;der.rotation.z=-.18;
    u.head.rotation.x=.16;
    if(!caminando){u.arms[0].rotation.z=.22;u.arms[1].rotation.z=-.22;}
  }
  if(expr==='hablando'){
    u.mouth.visible=true;
    u.mouth.scale.y=.5+Math.abs(pulso(t,11))*.9;
    u.head.rotation.x=.04*pulso(t,4.2);
    if(!caminando)u.arms[1].rotation.z=1.2+.3*pulso(t,4);
  }
  // Parpadeo: se aplica al final. Se mantiene al cambiar de emoción.
  const blink=parpadeo(t);
  izq.scale.y*=blink;der.scale.y*=blink;
  u.blink=blink;
}
