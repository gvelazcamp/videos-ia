# Gemini azul — personaje 3D articulado, 10 PNG individuales

**Referencia:** robot azul y blanco de la imagen aprobada por Gonzalo el 19/11/2026, con ojos de arcos blancos, antena azul, cuerpo azul eléctrico, dos estrellas brillantes cian/violeta/rosa y placa **«Gemini»**. El robot con placa «Grok» se había etiquetado incorrectamente; se conserva como un modelo distinto y no se sobrescribe.

## Entregables

- `resultado/Gemini_3D_Corriendo_Articulado.glb`: modelo GLB nuevo con armature y clip `Gemini_CORRER_hacia_camara_5s`.
- `resultado/Gemini_10_imagenes_separadas.zip`: diez PNG verdaderamente independientes, no un collage.
- `resultado/vistas/gemini_01_frente.png` a `gemini_10_desde_abajo.png`: frente, dos perfiles, atrás, diagonales, desde arriba y abajo.
- `resultado/carrera_01.png`, `carrera_04.png`, `carrera_07.png`, `carrera_10.png`: fotogramas de carrera como revisión.
- `generar.py`: código Blender/Python para materiales, geometría, dos estrellas, armature, animación y renders.
- `index.html`: visor Three.js para móvil, con botón Correr, control de zoom y descarga.

## Verificaciones

GitHub Actions genera y comprueba el formato GLB, existencia de esqueleto, canales de animación, diez PNG y cuatro poses. Esto no es suficiente para declarar el movimiento y diseño definitivamente aprobados; revisar visualmente.

[Ver Gemini 3D corriendo](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/gemini-azul-articulado-corriendo-20261119/index.html)

**Protección:** nunca modificar modelos, visores o workflows de Grok, Claude y ChatGPT. Iteraciones de Gemini únicamente en este directorio.
