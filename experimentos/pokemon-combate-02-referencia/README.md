# Pikachu vs. Cubone — Combate 02, estilo ilustrado aprobado

## Videos listos para ver

- **[Reproducir versión móvil de 2,9 MB](https://cdn.jsdelivr.net/gh/gvelazcamp/videos-ia@main/experimentos/pokemon-combate-02-referencia/pikachu-vs-cubone-estilo-aprobado-movil.mp4)** — abre directamente en navegador; `video/mp4`, streaming. Formato H.264 Constrained Baseline + AAC, 480×854, con faststart.
- **[Reproducir versión de calidad completa](https://cdn.jsdelivr.net/gh/gvelazcamp/videos-ia@main/experimentos/pokemon-combate-02-referencia/pikachu-vs-cubone-estilo-aprobado.mp4)** — H.264 + AAC, 540×960, ~11 MB.
- [MP4 móvil en GitHub](pikachu-vs-cubone-estilo-aprobado-movil.mp4).
- [MP4 original en GitHub](pikachu-vs-cubone-estilo-aprobado.mp4).

**Duración:** 61,04 s, vertical 9:16. **Narración:** voz de Gemini ya generada y guardada en `../pokemon-combate-01/voz-gemini-charon.mp3`. No se volvió a gastar crédito ni a generar una voz.

## Estilo visual

Esta versión responde a la imagen elegida por el usuario como **referencia visual exacta**, no a los dibujos simplificados del primer video. Se conserva la misma composición 2D: castillo de piedra, cielo violeta, gran luna rosada, llamas, escudos, Pikachu, Cubone y paneles de combate con niveles, turnos, vida y ataques.

La imagen original suministrada por el usuario se conserva en [assets/referencia-estilo-aprobado.png](assets/referencia-estilo-aprobado.png). Se separaron sus dos personajes con máscaras para animarlos sin redibujarlos; las máscaras y el fondo tratado están en `assets/`.

La animación incluye desplazamientos y giros de los personajes, relámpagos, hueso volador, arcos de acero, líneas de velocidad, partículas, chispas, daño progresivo de PS y placa de victoria. Se preservan los detalles visuales de la **imagen aprobada**. Es una **animación 2D por capas**, no una animación 3D de extremidades independiente; cuando los sprites se mueven, pueden verse pequeñas zonas reconstruidas del fondo.

## Combate (ficción audiovisual)

- Pikachu usa Rayo. No afecta a Cubone de tipo Tierra.
- Cubone ataca con Hueso Palo.
- Pikachu responde con Ataque Rápido; Cubone con Cabezazo.
- Pikachu usa Cola Férrea; Cubone lanza Huesomerang.
- Ataque Rápido final de Pikachu. Cubone queda fuera de combate.
- Victoria con una invitación a elegir el próximo rival.

El resultado, niveles y valores de daño son **creativos**, no un simulador exacto de una generación de juegos. Los nombres, personajes y elementos Pokémon pertenecen a sus titulares. Este es un fan video no oficial.

## Código y reconstrucción automática

- `render_referencia.py` — usa la ilustración de referencia, segmentación local con OpenCV, generación de efectos en PIL, FFmpeg, animación de barras y mezcla con voz existente.
- [GitHub Actions](https://github.com/gvelazcamp/videos-ia/actions/workflows/pokemon-combate-02-referencia.yml) — recrea ambos MP4 y guarda los assets en esta carpeta, sin alterar ninguna versión previa.
- No hay ninguna publicación automática en Instagram, TikTok o Play Store ni cambios en Girá y Adiviná.

En Android, **usar el enlace de reproducción directa** de arriba, no el visor de archivos de la aplicación GitHub, que a veces no reproduce archivos MP4.
