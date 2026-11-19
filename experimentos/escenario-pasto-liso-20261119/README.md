# Escenario 01 — pasto liso elevado

**Prueba de escenario de videojuego generada con Blender mediante GitHub Actions.**

El escenario contiene exclusivamente:
- Una plataforma cuadrada de 18 × 18 metros.
- Superficie de pasto **completamente plana**, verde uniforme, sin ondulaciones ni texturas con relieve.
- Costados de tierra marrón; superficie transitable a 1,28 m del nivel inferior.

No incluye árboles, piedras, montañas, rampas, construcciones ni robots. Es una base inicial para añadir elementos después, sin cambiar el diseño actual.

## Ver y descargar

- [Visor interactivo 360°](https://raw.githack.com/gvelazcamp/videos-ia/main/experimentos/escenario-pasto-liso-20261119/index.html)
- [GLB real del escenario](resultado/escenario_pasto_liso_elevado.glb)
- [Proyecto Blender editable](resultado/escenario_pasto_liso.blend)
- [Imagen de prueba](resultado/vista_previa.png)
- [Informe técnico](resultado/informe.json)

## Generación

El script `generar.py` usa `bpy`, crea dos mallas simples con materiales propios, valida la planitud y exporta `GLB`, `.blend` y `PNG`.

Workflow exclusivo: `.github/workflows/escenario-pasto-liso-20261119.yml`. Se ejecuta en el runner GitHub (no requiere instalar Blender localmente). Solo añade archivos en esta carpeta; no modifica los cuatro robots ni sus bibliotecas de movimientos. La visualización se considera probada solo tras una ejecución exitosa de Actions.
