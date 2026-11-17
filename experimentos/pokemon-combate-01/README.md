# Pokémon Arena 01 — Pikachu vs Cubone

**[Ver el video](pokemon-pikachu-vs-cubone.mp4)** · Formato vertical 9:16 · 540×960 · 61 segundos · narración en español rioplatense de Gemini.

Primer experimento de **videojuego narrado** con combate animado, inspirado en el ritmo de los reels de Pokémon con cuadros de ataques y barras de vida. No es una pantalla fija ni un juego interactivo: se renderizan fotogramas con movimiento de personajes, huesos, electricidad, chispas, golpes, barras de energía, menú de ataques y cambios de turno.

## Trama y resultados (pelea de ficción)

| Turno | Acción | Efecto |
|---|---|---|
| 1 | Pikachu usa **Rayo** | No afecta a Cubone: es de tipo Tierra |
| 1 | Cubone usa **Hueso Palo** | Pikachu pasa de 51 a 29 PS |
| 2 | Pikachu usa **Ataque Rápido** | Cubone de 54 a 38 PS |
| 2 | Cubone usa **Cabezazo** | Pikachu pasa a 17 PS |
| 3 | Pikachu usa **Cola Férrea** | Cubone pasa a 18 PS |
| 3 | Cubone lanza **Huesomerang** | Falla por poco |
| 4 | Pikachu remata con **Ataque Rápido** | Cubone llega a cero y Pikachu gana |

Los números de daño y el resultado de la batalla son **ficción para este video**, no una simulación exacta de los juegos ni una batalla oficial. Sí respetamos una mecánica importante: **un ataque Eléctrico no afecta a Pokémon de tipo Tierra**, como Cubone.

## Archivos

- `pokemon-pikachu-vs-cubone.mp4`: video final.
- `voz-gemini-charon.mp3`: locución generada por el sistema gratuito Gemini conectado al puente.
- `render_combate.py`: dibuja el escenario, la interfaz y los efectos; sincroniza los turnos con la duración de la voz, sintetiza música/efectos originales y monta el MP4.
- `assets/pikachu-original.png`: recorte transparente del Pikachu usado en escenas anteriores.
- `assets/cubone-oficial.png`: arte de Cubone desde los recursos de PokéAPI.
- [Workflow GitHub Actions](https://github.com/gvelazcamp/videos-ia/actions/workflows/pokemon-combate-01.yml): reconstrucción y publicación del MP4.

## Qué se conserva

No se editaron los proyectos del surf, castillo, París, historia de Cubone V1/V2 ni Girá y Adiviná. El combate es un proyecto nuevo y autocontenido. El guion y las animaciones son originales, tomando como referencia **el montaje y los elementos de videojuego** de un reel de Instagram (`DfFWUJJuE6o`), sin usar cuadros ni audio de ese reel.

**Aviso:** los personajes Pokémon son propiedad de sus respectivos titulares. Fan animation no oficial; no afiliada a The Pokémon Company o Nintendo.
