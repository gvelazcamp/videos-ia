# Voltito — TRELLIS multivista (prueba experimental, noviembre de 2026)

## Resultado

- [Visor 3D real en el navegador](index.html)
- [Modelo candidato TRELLIS (.glb)](voltito-trellis-multivista-candidato.glb)
- [Resultado técnico y rutas de entrada](resultado.json)
- [Script reproducible](generar_trellis.py)
- [Capturas de prueba móvil](captura-trellis-frente.png)

**Motor:** TRELLIS de Microsoft, utilizado mediante la instancia comunitaria pública `trellis-community/TRELLIS` de Hugging Face ZeroGPU. No se empleó una API paga ni se descargaron pesos TRELLIS al runner de GitHub (sin GPU). El servidor remoto puede cambiar, saturarse o limitar solicitudes.

## Qué se hizo realmente

1. Se emplearon **ocho PNG horizontales existentes**, de 0°, 45°, 90°, 135°, 180°, 225°, 270° y 315°, con alfa transparente.
2. Se prepararon a escala uniforme de 512×512 para el servicio.
3. TRELLIS generó desde esas referencias un **modelo 3D real** en `multidiffusion`, no una rotación de imágenes planas.
4. Se descargó un GLB auténtico y se verificó su encabezado glTF, caras, vértices y dimensiones.
5. Se probó el visor WebGL en Chrome móvil desde 0°, 37°, 128°, 180° y 315°, y con movimientos verticales.

El GLB pesa ~1,44 MB y tiene ~9.840 caras. Su apariencia **todavía puede diferir del diseño aprobado de Voltito**: revisar especialmente suavidad del pelaje, ojos, orejas y cola antes de utilizarlo en el juego.

Las dos referencias de **arriba y abajo** existen, pero no se enviaron a esta prueba: la generación fue con ocho vistas horizontales. No afirmar «10 vistas alimentadas al modelo».

## Cómo reproducirlo

Workflow de GitHub Actions: [voltito-trellis-generar-20261118.yml](../../.github/workflows/voltito-trellis-generar-20261118.yml), con entradas y opciones fijadas en `generar_trellis.py`. Hubo un error inicial por formato de la galería de Gradio; se solucionó al pasar objetos `{"image":handle_file(...),"caption":None}`.

Para un personaje futuro, sustituir únicamente las referencias por las de ese personaje y usar una carpeta nueva. **Nunca editar** modelos, imágenes o workflows aprobados sin autorización.

## Estado de versiones

- [Voltito Hunyuan 3D (anterior, intacto)](../voltito-3d-10-vistas-20261118/index.html).
- [Segundo experimento TRELLIS](index.html) — candidato independiente, sujeto a evaluación visual.
- El visor permite giro continuo y una opción «Sombras» para comparar la textura sin sombras con la iluminación realista.
