# Editor de escenarios modulares 3D (19/11/2026)

Editor independiente para **copiar, mover y colocar cuadrados de terreno** como piezas de un videojuego, usando los mismos GLB originales creados con Blender. No regenera las mallas ni modifica los escenarios anteriores.

## Abrir

**[Editor 3D: copiar y colocar escenarios](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/editor-escenarios-modulares-20261119/index.html)**

## Funciones

- Carga los dos modelos reales, ambos de **18 × 18 m**: pasto completamente liso y pasto con árboles y montañitas.
- Inicia con el escenario de árboles en el centro; se puede agregar pasto liso o más copias del mismo.
- **Copiar seleccionado**: activa la colocación de una copia; después, tocar un lugar vacío del escenario o del plano superior. Se puede continuar colocando sucesivamente.
- **Duplicar a izquierda, derecha, adelante y atrás** en la casilla contigua mediante botones.
- **Mover**: arrastrar un terreno en el escenario a una casilla libre. También se puede tocar una casilla vacía del plano superior para llevar allí el terreno seleccionado.
- **Plano superior 9 × 9**: coordenadas de -4 a 4 en cada eje, encastre automático de cuadrícula, máximo 40 terrenos por rendimiento.
- Girar cámara, vista 3D y vista desde arriba, zoom, ajuste de encuadre.
- Eliminar (excepto el último cuadrado), deshacer, reiniciar.
- Guardar automáticamente en almacenamiento local del navegador, exportar/importar un archivo JSON con las posiciones. Ese archivo JSON es el mapa, **no un GLB combinado ni una exportación de Blender**.

## Fuentes originales (intactas)

- [Escenario 01: pasto liso](../escenario-pasto-liso-20261119/resultado/escenario_pasto_liso_elevado.glb)
- [Escenario 02: árboles y colinas](../escenario-pasto-arboles-montanitas-20261119/resultado/escenario_pasto_arboles_montanitas.glb)

Las piezas quedan alineadas en coordenadas múltiplos de 18 m, sin alterar su geometría original. Los bordes del terreno encastran sin huecos en la plataforma base; las montañitas y los árboles se conservan en cada copia. Cualquier cambio de terreno se guarda como diseño de composición, no reescribe los archivos originales.

**Precaución:** la geometría del escenario 02 puede tener árboles en los bordes; al unir cuadrados cercanos las copas pueden visualmente superponerse. Corregir eso requeriría otro pedido. Este editor es una primera prueba de composición.
