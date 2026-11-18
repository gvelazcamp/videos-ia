# Voltito — prueba TRELLIS.2 (18/11/2026)

**Resultado actual: generación de previsualización conseguida, exportación GLB bloqueada por la cuota gratuita ZeroGPU. No existe archivo GLB de TRELLIS.2 todavía.**

## Prueba ejecutada

- **Motor:** microsoft/TRELLIS.2 (Space oficial ZeroGPU), con respaldo de henrybit/TRELLIS-2-4B-Demo.
- **Fuente:** [Voltito diagonal 45° del proyecto de 10 vistas](../voltito-3d-10-vistas-20261118/voltito-045.png), PNG transparente.
- **Entrada preparada:** [entrada-voltito-45.png](entrada-voltito-45.png), 768×768, personaje completo.
- **Parámetros:** resolución 512, semilla 27, parámetros oficiales de muestreo, extracción solicitada a 100.000 caras con textura 1024.
- **Generación:** el primer servicio entregó una previsualización HTML extensa (~3.063.651 caracteres). Al pedir /extract_glb, respondió **«You have exceeded your ZeroGPU quota»**.
- **Segundo servicio:** también rechazó la generación por la cuota compartida.
- **Resultado verificable:** [resultado.json](resultado.json). No se creó ni publicó un modelo falso.

## Reintento sin terminal

[GitHub Actions — Voltito TRELLIS.2](../../.github/workflows/voltito-trellis2-generar-20261118.yml). Abrir la pestaña Actions, elegir este workflow y ejecutar **Run workflow** cuando se reponga la cuota del servicio. El proceso ya está configurado para guardar únicamente un GLB genuino validado, o el informe del error.

Nota: el proveedor no asegura disponibilidad futura, la cuota se aplica también al exportar el GLB y GitHub Actions no incluye una GPU equivalente. No pagar ni utilizar una API de pago sin autorización expresa de Gonzalo.

## Comparación con modelos anteriores

- [TRELLIS original: 8 imágenes, GLB real y visor aprobado](../voltito-trellis-prueba-20261118/index.html).
- [Hunyuan: malla 3D real y proceso anterior](../voltito-3d-10-vistas-20261118/index.html).

El experimento TRELLIS.2 está aislado y **no reemplazó ninguna versión anterior**.

## Limitación de entradas

La API oficial de TRELLIS.2 en la prueba acepta **una sola vista**, mientras que el TRELLIS original sí permitió ocho vistas. Las otras nueve vistas de Voltito se conservan como referencias comparativas, no se entregaron al modelo TRELLIS.2.
