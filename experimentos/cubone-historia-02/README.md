# Cubone — La noche en que alguien se quedó · Versión 2

**Objetivo:** conservar el reel emotivo de Cubone ya producido y sumar objetos informativos y una interfaz de videojuego, tomando como referencia los recursos visuales del reel de Instagram `DfC2hENuoaH` (Pokédex, Poké Balls, carteles y fichas de objetos), **sin copiar sus imágenes, guion, audio ni animaciones**.

**Video final:** [cubone-historia-02.mp4](cubone-historia-02.mp4) (MP4 9:16, 540×960, ~61,75 s).

## Cambios sobre la versión 1

| Minutos/segundos | Elemento nuevo | Propósito |
| --- | --- | --- |
| 00:01–00:06 | Pokédex roja con Cubone #0104, Tierra, Solitario y Poké Ball | Presentar al protagonista como una entrada del videojuego |
| 00:07–00:14 | Ficha «OBJETO · 01 — CRÁNEO» con el cráneo visualmente separado de Cubone | Explicar que era de su madre (dato oficial) |
| 00:18–00:27 | Ficha «OBJETO · 02 — HUESO» con dibujo del hueso individual | Mostrar el objeto que utiliza para luchar |
| 00:35–00:40 | «¡ENCUENTRO! — EEVEE #0133» y Poké Ball decorativa | Presentar al acompañante de nuestra ficción |
| 00:59–01:01 | Ficha final «Pokédex #0104 — Una historia que sigue...» | Remate visual del episodio |

Los paneles tienen apariciones y salidas animadas, leve desplazamiento y sonidos originales de interfaz. La voz de Gemini, el relato, las escenas, los fondos y la música original de la **versión 1 no se alteraron**. La Poké Ball es parte de la interfaz: **Cubone no captura a Eevee ni nadie captura a Cubone** en este relato.

## Datos oficiales frente a ficción

- **Oficial:** Cubone #0104 es de tipo Tierra, conocido como Pokémon Solitario, lleva el cráneo de su madre fallecida y llora al recordarla; su hueso es un objeto empleado para combatir.
- **Ficción del video:** el encuentro esperanzador con Eevee, la lucecita del bosque y el final acompañados. No figuran así en la Pokédex.
- No se afirma que el hueso también haya pertenecido a su madre.

Referencia oficial: <https://www.pokemon.com/us/pokedex/0104>. Las ilustraciones de Cubone y Eevee que aparecen como referencias provienen de la recopilación de sprites de PokeAPI, con los derechos de Pokémon y de los personajes pertenecientes a sus titulares. Los fondos de bosque y atardecer fueron seleccionados desde OpenGameArt con licencia CC0. Este es un experimento no oficial de fan art, no una publicación de Pokémon.

## Archivos independientes

- `render/generar_overlays.py` — dibuja paneles transparentes PNG, fichas de cráneo/hueso, Poké Balls, metadatos en JSON.
- `render/render_v2.py` — superpone los paneles sobre el video original y añade sonidos de interfaz sin cambiar el archivo base.
- `objetos/` — PNGs individuales y `escenas.json`, generados en GitHub Actions.
- `cubone-historia-02.mp4` — nuevo video completo.

La versión 1 está en `../cubone-historia-01/`. El flujo usa GitHub Actions `.github/workflows/cubone-historia-02.yml` para reconstruirla desde los assets y la voz ya archivada en GitHub y crear el MP4 de la versión 2.

**Sin cambios a** Girá y Adiviná, otras historias, la animación de Pikachu ni el juego de París.
