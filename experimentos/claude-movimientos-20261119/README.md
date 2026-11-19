# Claude 3D — 12 movimientos y recorrido libre (primer piloto)

**Fecha:** 19/11/2026.

## Objetivo
Aprovechar el **mismo Claude 3D articulado que ya teníamos** sin rehacerlo ni alterar su versión de carrera y su visor anterior. Crear una biblioteca de acciones exportadas dentro de un archivo GLB nuevo y un visor 360° para que Claude camine y gire por un escenario.

## Archivos
- `resultado/Claude_Biblioteca_12_Movimientos.glb`: copia GLB con el esqueleto de Claude y **12 clips nuevos** además del clip original, validado por GitHub Actions.
- `resultado/informe.json`: lista de clips, duración, bucle, huesos y estado.
- `generar_biblioteca.py`: script Blender 3.x que **importa** el Claude original con huesos, crea 12 acciones y las empaqueta como pistas NLA separadas. No reemplaza ni edita la fuente.
- `index.html`: visor 3D y prueba interactiva, compatible con navegador móvil.
- `.github/workflows/claude-biblioteca-movimientos-20261119.yml`: proceso de generación y verificación.

## Movimientos (12)
1. Reposo (loop).
2. Caminar lento (loop).
3. Correr (loop).
4. Saludar.
5. Girar 90° a la izquierda.
6. Girar 90° a la derecha.
7. Frenar.
8. Saltar.
9. Agarrar un objeto.
10. Soltar un objeto.
11. Sentarse.
12. Levantarse.

El GLB conserva además el clip de carrera original. El visor ofrece botones para cada acción, controles direccionales de recorrido (avance y retroceso con flechas), velocidad 0,4×–2×, giro de cámara 360°, encuadre y zoom. Incluye una esfera de prueba para agarrar/soltar. El **movimiento por el escenario se controla desde el visor**; los clips de caminata/carrera del archivo son *en el lugar* para poder reutilizarlos en cualquier dirección.

## Qué está comprobado y qué falta
- Ejecutado en GitHub Actions con Blender, sin servicios pagos.
- El GLB contiene 15 huesos y las 12 pistas de animación requeridas (más una animación heredada).
- La integridad binaria y los nombres de los clips se comprobaron automáticamente.
- **Pendiente:** validar visualmente cada acción, las transiciones y la interacción del visor en el celular; no declarar aprobación ni naturalidad perfecta hasta entonces.

## Enlaces
- [**Abrir visor interactivo de Claude**](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/claude-movimientos-20261119/index.html)
- [GLB nuevo con movimientos](https://github.com/gvelazcamp/videos-ia/blob/main/experimentos/claude-movimientos-20261119/resultado/Claude_Biblioteca_12_Movimientos.glb)
- [Workflow de generación](https://github.com/gvelazcamp/videos-ia/actions/workflows/claude-biblioteca-movimientos-20261119.yml)

## Seguridad de cambios
**No se modificó** `experimentos/claude-limpio-corriendo-20261119/`, TRELLIS, los modelos de Gemini, Grok o ChatGPT, ni los workflows existentes. Este primer piloto vive en su propia carpeta. Los otros personajes no reciben animaciones hasta que se confirme la prueba.
