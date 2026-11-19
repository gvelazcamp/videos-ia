# Grok gris (el último diseño correcto) — 3D articulado corriendo

**Referencia oficial:** última imagen proporcionada por el usuario en la conversación del 19/11/2026: robot chibi **GRIS**, cabeza grande plateada ovalada, visor negro con dos ojos blancos en arco, antena redonda gris, torso/brazos/piernas/botas gris grafito, manos blancas. Emblema pectoral **aro blanco con rayo/diagonal plateada** (NO la estrella de Gemini ni la estrella del Grok azul anterior), placa blanca **Grok**.

## Modelo y animación
- `resultado/Grok_Gris_3D_Corriendo_Articulado.glb`: 3D real con armature de Blender y clip de 5 segundos `Grok_CORRER_hacia_camara_5s`.
- El esqueleto usa 15 huesos: torso, cabeza, cadera y articulaciones de brazos, codos, manos, muslos, pantorrillas y pies. La carrera se desplaza hacia la cámara, alternando zancadas y balanceos de brazos.
- Las partes del cuerpo son mallas separadas y utilizan skinning rígido, no deformación procedural de vértices. Es una **reconstrucción**, no la misma malla exacta de la foto.

## Imágenes separadas
- `resultado/Grok_Gris_10_PNG_individuales.zip`: diez PNG desde distintos ángulos, transparentes, NO un collage.
- `resultado/vistas/`: vistas frontal, 45° izquierdo, perfil izquierdo, 135°, espalda, 225°, perfil derecho, 315°, superior e inferior.
- `resultado/carrera_01.png`, `carrera_04.png`, `carrera_07.png`, `carrera_10.png`: cuatro fotogramas de la carrera generados desde el GLB de Blender.

## Reutilización
- `generar.py` es el generador Blender/Python para crear el modelo y su animación.
- `index.html` es el visor Three.js para móvil y descarga del GLB y las diez imágenes.
- `.github/workflows/grok-gris-articulado-corriendo-20261119.yml` es el proceso gratuito de construcción.

[**Abrir visor Grok gris corriendo**](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/grok-gris-articulado-corriendo-20261119/index.html)

**Protección:** el Grok azul anterior, Gemini, Claude, ChatGPT y sus workflows NO se reemplazan. El candidato requiere revisión visual antes de considerarlo final.
