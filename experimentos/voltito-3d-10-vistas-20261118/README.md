# Voltito — reconstrucción 3D con 10 referencias (18/11/2026)

## Modelo recomendado para revisar

- **Visor 3D real:** [index.html](index.html)
- **GLB de 14,49 MB:** [voltito-10-vistas-mejorado.glb](voltito-10-vistas-mejorado.glb)
- **Capturas verificadas:** [frente](prueba-3d-frente.png), [37°](prueba-3d-giro-37.png), [128°](prueba-3d-giro-128.png), [espalda](prueba-3d-espalda.png), [superior](prueba-3d-arriba.png), [inferior](prueba-3d-abajo.png).
- **Entradas:** 4 PNG cardinales del proyecto anterior + 4 diagonales y 2 verticales nuevos en esta carpeta.
- **Fidelidad:** candidato experimental, **no idéntico al arte original**. Los ojos y cola quedan más coherentes usando la geometría anterior y un ajuste conservador de colores. Las geometrías cenital/nadir no se reconstruyeron de forma nativa.

## Método verdadero

1. El modelo base del personaje es una **malla tridimensional real**, generada con **Hunyuan3D-2mv** desde frente, espalda, perfil izquierdo y perfil derecho. Es un GLB girable en cualquier ángulo, no una secuencia de fotografías.
2. Se separaron seis imágenes nuevas aportadas por Gonzalo: `045`, `135`, `225`, `315`, `superior`, `inferior`.
3. Se intentó la versión gratuita del sitio **Remove.bg**, pero el sitio devolvió un botón Download deshabilitado. Por eso se usó un **recorte local gratuito por segmentación de color**, validado para imágenes amarillas/turquesas sobre blanco: [recorte_local.py](recorte_local.py). Ninguna imagen se redibujó.
4. [colorear_10.py](colorear_10.py) conserva los colores previos de la cara y usa las diagonales y verticales solo en superficies 3D alineadas y con colores compatibles. Se preserva el 72% o más del color del modelo anterior en cada vértice.
5. [validar_3d.py](validar_3d.py) valida el mismo GLB en Chrome móvil desde varios ángulos. El [diagnóstico](diagnostico-10-vistas.json) registra entradas y cobertura.

**Limitación técnica:** Hunyuan3D-2mv admite 4 vistas simultáneas para generar geometría, no 10. Las 10 contribuyen en conjunto al modelo base y su coloración, pero esto NO equivale a geometría reconstruida directamente desde 10 cámaras.

## Variante NO aprobada (no usar como modelo final)

Se ensayó una segunda malla Hunyuan exclusivamente con las cuatro diagonales, visible en [alternativa-diagonal.html](alternativa-diagonal.html), pero las capturas revelaron **duplicaciones en ojos/cola y deformaciones**. No se reemplazó el GLB base por esa variante. Queda como experimento para investigación, **no como resultado recomendado**.

## Archivos anteriores preservados

- [Modelo anterior de 4 vistas](../voltito-hunyuan-4v-20261118/index.html)
- [Sus PNG y código original](../voltito-hunyuan-4v-20261118/)
- Sin modificación de otros juegos ni proyectos.
