// animacion-claude.js — Módulo 02 (Claude): caminata del robot.
// Contrato: export function aplicarCaminata(robot, t, intensidad)
//  - robot: grupo devuelto por crearRobotChatGPT()
//  - t: tiempo en segundos (clock.getElapsedTime())
//  - intensidad: 0..1 (1 = caminata completa)
// Solo toca lo que escena.js ya resetea al detener la caminata:
//  robot.userData.feet[0|1] (0 = izquierdo, 1 = derecho), robot.userData.body,
//  robot.position.x / robot.position.y.
// Las poses son absolutas (no acumulan), así que no hay deriva.

const VELOCIDAD = 5.5;   // rad/s: ~0.9 pasos completos por segundo
const BASE_Y_ROBOT = 0.11;
const BASE_Y_PIE = 0.125;
const BASE_Z_PIE = 0.035;
const BASE_X_PIE = 0.14;

export function aplicarCaminata(robot, t, intensidad = 1) {
  const feet = robot?.userData?.feet;
  const body = robot?.userData?.body;
  if (!feet || feet.length < 2) return;

  const k = Math.max(0, Math.min(1, intensidad));
  const fase = t * VELOCIDAD;

  // Pies: oposición de fase (cuando uno va adelante, el otro atrás)
  feet.forEach((foot, i) => {
    const lado = i === 0 ? -1 : 1;
    const ph = fase + (i === 0 ? 0 : Math.PI);
    const avance = Math.sin(ph);              // adelante / atrás
    const levante = Math.max(0, Math.cos(ph)); // solo se levanta mientras avanza

    foot.position.set(
      lado * BASE_X_PIE,
      BASE_Y_PIE + 0.07 * levante * k,
      BASE_Z_PIE + 0.12 * avance * k
    );
    foot.rotation.set(-0.3 * levante * k, 0, 0);
  });

  // Cuerpo: balanceo lateral, giro de torso y leve inclinación al frente
  if (body) {
    body.rotation.set(
      0.04 * k,
      Math.sin(fase) * 0.08 * k,
      Math.sin(fase) * 0.06 * k
    );
  }

  // Rebote vertical (dos por ciclo) y pequeño vaivén lateral
  robot.position.y = BASE_Y_ROBOT + 0.02 * (0.5 - 0.5 * Math.cos(fase * 2)) * k;
  robot.position.x = Math.sin(fase) * 0.015 * k;
}
