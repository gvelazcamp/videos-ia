# Gemini 3D: 12 animaciones para el visor universal

## Objetivo
Añadir **Gemini** al mismo visor donde ya están **ChatGPT y Claude**, sin modificar los personajes ni GLB anteriores.

## Fuente real
Se toma el Gemini azul creado previamente con cabeza blanca, cuerpo y antena azules, **dos estrellas iridiscentes** y placa **Gemini**:
`../gemini-azul-articulado-corriendo-20261119/resultado/Gemini_3D_Corriendo_Articulado.glb`.

## Salidas
- `generar_biblioteca.py`: usa el esqueleto existente de Gemini, no fabrica otro robot.
- `resultado/Gemini_Biblioteca_12_Movimientos.glb`: GLB independiente con 12 animaciones.
- `resultado/informe.json`: número de huesos y nombres de los clips.
- `resultado/saludo_frontal.png` y `resultado/saludo_45_grados.png`: inspección de la pose en Blender.

## Movimientos
1. Quieto.
2. Caminar lento.
3. Correr.
4. Saludar **levantando la mano hacia el frente**, sin enviarla detrás del cuerpo.
5. Girar izquierda 90°.
6. Girar derecha 90°.
7. Frenar.
8. Saltar.
9. Agarrar objeto.
10. Soltar objeto.
11. Sentarse.
12. Levantarse.

Las caminatas están animadas **en el lugar**, y el recorrido con flechas y velocidad es manejado por el visor. El código de saludo calcula la orientación según las direcciones originales de los huesos y valida la muñeca por delante del hombro (eje -Y de Blender) y más alta que este.

## Visor universal
[**Abrir visor 3D universal**](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/visor-3d-universal-20261119/index.html)

## Control de cambios
Este nuevo proyecto se crea en carpeta independiente. **No se toca el GLB ni el visor original de Gemini**, ni los archivos originales de Claude, ChatGPT o Grok.

La generación y el funcionamiento del modelo requieren verificación técnica con Blender y aprobación visual del usuario.
