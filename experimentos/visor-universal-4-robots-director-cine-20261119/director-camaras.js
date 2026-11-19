// Director de cámaras 3D independiente. No altera animaciones, GLB ni el motor del visor.
// Configurado para la orientación actual del visor: los personajes miran a +Z.
export function createDirectorDeCamaras(THREE,camera,worldRoot,getState){
  const names={
    original:'Cámara original 360°',
    frontal:'Cámara frontal',
    seguimiento:'Cámara de seguimiento',
    subjetiva:'Cámara subjetiva (ojos del robot)',
    aerea:'Cámara aérea',
    primerPlano:'Primer plano',
    orbital:'Cámara orbital 360°',
    libre:'Cámara libre',
    automatica:'Cámara automática'
  };
  const autoShots=['frontal','seguimiento','primerPlano','aerea','orbital','subjetiva'];
  const shotSelect=document.getElementById('cinemaShotSelect');
  const shotText=document.getElementById('cinemaNow');
  const secondsInput=document.getElementById('cinemaSeconds');
  const secondsText=document.getElementById('cinemaSecondsValue');
  const nextButton=document.getElementById('cinemaNext');
  const resetButton=document.getElementById('cinemaOriginal');
  let mode='original',autoSeconds=0,shotIndex=0,orbitAngle=0;
  let flyYaw=0,flyPitch=0;
  const flyPosition=new THREE.Vector3(),pressed=new Set();
  const target=new THREE.Vector3(),look=new THREE.Vector3(),desired=new THREE.Vector3();
  const flyForward=new THREE.Vector3(),flyRight=new THREE.Vector3();
  const fastClamp=THREE.MathUtils.clamp;
  const updateLabel=()=>{
    const active=mode==='automatica'?autoShots[shotIndex]:mode;
    shotText.textContent=mode==='automatica'?'Automática · '+names[active]:names[mode];
  };
  const setMode=next=>{
    if(!Object.prototype.hasOwnProperty.call(names,next))return;
    if(next==='libre'){
      flyPosition.copy(camera.position);
      const {height}=getState();
      const p=worldRoot.position;
      const to=new THREE.Vector3(p.x,height*.55,p.z).sub(flyPosition).normalize();
      flyYaw=Math.atan2(to.x,to.z);
      flyPitch=Math.asin(fastClamp(to.y,-1,1));
    }
    mode=next;
    autoSeconds=0;shotIndex=0;
    if(next==='orbital')orbitAngle=0;
    shotSelect.value=next;
    pressed.clear();
    if(next==='original'&&camera.fov!==38){
      camera.fov=38;camera.updateProjectionMatrix();
    }
    updateLabel();
  };
  const moveCamera=(dt)=>{
    if(mode==='original')return false; // La cámara anterior queda exactamente como estaba.
    const {height,distance,yaw}=getState();
    const wx=worldRoot.position.x,wz=worldRoot.position.z;
    const fx=Math.sin(yaw),fz=Math.cos(yaw);
    target.set(wx,height*.52,wz);
    let active=mode,fov=38;
    if(mode==='automatica'){
      autoSeconds+=dt;
      const duration=Math.max(2,Number(secondsInput.value)||4);
      if(autoSeconds>=duration){
        autoSeconds-=duration;
        shotIndex=(shotIndex+1)%autoShots.length;
        updateLabel();
      }
      active=autoShots[shotIndex];
    }
    desired.copy(target);look.copy(target);
    if(active==='frontal'){
      desired.set(wx+fx*distance,height*.60,wz+fz*distance);
    }else if(active==='seguimiento'){
      desired.set(wx-fx*distance*.76,height*1.05,wz-fz*distance*.76);
      look.x+=fx*1.2;look.z+=fz*1.2;
    }else if(active==='subjetiva'){
      desired.set(wx+fx*.20,height*.79,wz+fz*.20);
      look.set(desired.x+fx*5,desired.y-.02,desired.z+fz*5);
      fov=60;
    }else if(active==='aerea'){
      desired.set(wx+fx*.35,height*3+1,wz+fz*distance*.35);
      look.y=height*.52;
    }else if(active==='primerPlano'){
      const r=Math.max(1.35,height*.73);
      desired.set(wx+fx*r,height*.87,wz+fz*r);
      look.y=height*.81;
      fov=33;
    }else if(active==='orbital'){
      orbitAngle+=dt*.48;
      const a=orbitAngle+yaw;
      desired.set(wx+distance*.8*Math.sin(a),height*.9,wz+distance*.8*Math.cos(a));
    }else if(active==='libre'){
      const c=Math.cos(flyPitch);
      flyForward.set(Math.sin(flyYaw)*c,Math.sin(flyPitch),Math.cos(flyYaw)*c);
      flyRight.set(flyForward.z,0,-flyForward.x).normalize();
      const speed=Math.max(.75,height)*dt;
      if(pressed.has('KeyI'))flyPosition.addScaledVector(flyForward,speed);
      if(pressed.has('KeyK'))flyPosition.addScaledVector(flyForward,-speed);
      if(pressed.has('KeyJ'))flyPosition.addScaledVector(flyRight,-speed);
      if(pressed.has('KeyL'))flyPosition.addScaledVector(flyRight,speed);
      if(pressed.has('KeyU'))flyPosition.y+=speed;
      if(pressed.has('KeyO'))flyPosition.y-=speed;
      camera.position.copy(flyPosition);
      look.copy(flyPosition).addScaledVector(flyForward,8);
      camera.lookAt(look);
      if(camera.fov!==38){camera.fov=38;camera.updateProjectionMatrix();}
      return true;
    }
    // Las transiciones de posición son suaves sin afectar el desplazamiento de los robots.
    camera.position.lerp(desired,fastClamp(dt*4,0,1));
    camera.lookAt(look);
    if(camera.fov!==fov){camera.fov=fov;camera.updateProjectionMatrix();}
    return true;
  };
  const drag=(dx,dy)=>{
    if(mode==='original')return false;
    if(mode==='libre'){
      flyYaw+=dx*.008;
      flyPitch=fastClamp(flyPitch+dy*.006,-1.45,1.45);
    }else if(mode==='orbital'){
      orbitAngle+=dx*.008;
    }
    return true;
  };
  shotSelect.addEventListener('change',event=>setMode(event.target.value));
  secondsInput.addEventListener('input',()=>secondsText.textContent=secondsInput.value+' s');
  nextButton.addEventListener('click',()=>{
    if(mode!=='automatica')setMode('automatica');
    shotIndex=(shotIndex+1)%autoShots.length;
    autoSeconds=0;updateLabel();
  });
  resetButton.addEventListener('click',()=>setMode('original'));
  document.addEventListener('keydown',event=>{
    if(mode==='libre'&&['KeyI','KeyK','KeyJ','KeyL','KeyU','KeyO'].includes(event.code)){
      pressed.add(event.code);event.preventDefault();
    }
  });
  document.addEventListener('keyup',event=>pressed.delete(event.code));
  window.addEventListener('blur',()=>pressed.clear());
  updateLabel();
  return {setMode,drag,update:moveCamera,getMode:()=>mode};
}
