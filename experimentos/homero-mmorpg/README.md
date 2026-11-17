# Homero MMORPG — Demo

Juego de prueba autocontenido de Homero caminando. El contenido es una demo independiente y no modifica los vídeos existentes.

## Abrir el juego

Abrir directamente, sin htmlpreview:

https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/homero-mmorpg/index.html

## Avatar original

- `homero-original-mmorpg.png`: imagen PNG original de Homero de brazos cruzados (300 × 500, fondo transparente), copiada del puente privado `gvelazcamp/chatgpt-claude-puente/referencias-personales/homero-original-20261117.png`.
- El HTML la muestra a escala de personaje de mini-MMORPG (ancho responsive aproximado 37–84 px), manteniendo proporciones; conserva el avatar SVG anterior como respaldo si el PNG no carga.
- El movimiento existente por flechas/WASD/pantalla táctil se mantiene; el PNG conserva su diseño original y sus piernas se animan con máscaras SVG, mientras el cuerpo se desplaza por el mapa. No se generan dibujos alternativos.

## Casa Simpson — interior jugable (17/11/2026)

- Al acercarse a la puerta de **CASA SIMPSON** en Springfield aparece el botón **ENTRAR A CASA**; en PC también se puede usar la tecla **F**.
- Dentro aparece el living inspirado en la referencia: paredes rosas, piso verde, sofá naranja, cuadro de barco, mesa morada con lámpara y teléfono, lámpara de pie, alfombra de círculos y televisor.
- Homero puede caminar por el living con los controles existentes y usar **SALIR DE CASA** o **F** para regresar a la posición de Springfield donde estaba antes de entrar.
- Los seis objetos son archivos PNG independientes con transparencia en `assets/sofa.png`, `assets/mesa.png`, `assets/lampara.png`, `assets/cuadro.png`, `assets/alfombra.png` y `assets/televisor.png`.
- Son versiones optimizadas para el juego (hasta 256 px por eje). El exterior, las 8 donas, la tecla E para hablar y los controles actuales se conservan.

## Avatar articulado — Homero original de cuerpo entero

- Se usa `homero-original-parado.png`, copia exacta del PNG transparente aprobado en el puente `gvelazcamp/chatgpt-claude-puente/assets/homero-original-20261117/homero_transparente_para_juego.png`.
- Las extremidades se recortan con máscaras SVG **sin redibujar** la imagen: brazo izquierdo, brazo derecho y ambas piernas, con pivotes independientes para caminar y correr.
- El mismo avatar se usa afuera y dentro de la casa. Flechas/WASD, toque corto, mantener pulsado, CORRER/Shift, recolección de donas, HABLAR y ENTRAR/SALIR se conservan.
- El personaje se refleja al caminar a la izquierda. Si el PNG nuevo no carga, se mantiene el avatar de respaldo previo.
- Referencia de la imagen preexistente: https://www.instructables.com/Life-Sized-Homer-Simpson/; no se afirma ninguna licencia para explotación comercial.
