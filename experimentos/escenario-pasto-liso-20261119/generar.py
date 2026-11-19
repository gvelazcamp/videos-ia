#!/usr/bin/env python3
"""Escenario 01: terreno de videojuego con pasto liso sobre plataforma elevada.
Generación real con Blender ejecutado por GitHub Actions. No modifica otros assets.
"""
import json
import struct
from pathlib import Path
import bpy
from mathutils import Vector

CARPETA = Path(__file__).resolve().parent
SALIDA = CARPETA / "resultado"
SALIDA.mkdir(parents=True, exist_ok=True)

# Escena limpia, sin importar ninguno de los modelos anteriores.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

ANCHO = 18.0
LARGO = 18.0
ALTURA_TIERRA = 1.20
ESPESOR_PASTO = 0.08
ALTURA_CIMA = ALTURA_TIERRA + ESPESOR_PASTO


def material(nombre, color, rugosidad=0.94):
    m = bpy.data.materials.new(nombre)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    shader = m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Roughness"].default_value = rugosidad
    return m


pasto = material("Pasto verde uniforme, SIN textura ni relieve", (0.16, 0.52, 0.085))
tierra = material("Borde de tierra marron", (0.34, 0.205, 0.12))


def bloque(nombre, ancho, largo, alto, z, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = nombre
    # Transformar a dimensiones reales antes de exportar: caja totalmente plana.
    obj.dimensions = (ancho, largo, alto)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


suelo = bloque("Base maciza de tierra", ANCHO, LARGO, ALTURA_TIERRA,
               ALTURA_TIERRA / 2, tierra)
césped = bloque("Pasto PLANO superficie jugable", ANCHO, LARGO, ESPESOR_PASTO,
                ALTURA_TIERRA + ESPESOR_PASTO / 2, pasto)

# Geometría jugable: la cara superior debe ser horizontal.
vertices_arriba = [v.co for v in césped.data.vertices if v.co.z > 0]
assert len(vertices_arriba) == 4
assert max(v.z for v in vertices_arriba) - min(v.z for v in vertices_arriba) < 1e-6
assert abs(césped.location.z + max(v.z for v in vertices_arriba) - ALTURA_CIMA) < 1e-5

# Exportar las dos mallas como .glb; nada de cámara, luces, robots u otros objetos.
bpy.ops.object.select_all(action="DESELECT")
for obj in (suelo, césped):
    obj.select_set(True)
bpy.context.view_layer.objects.active = césped
archivo = SALIDA / "escenario_pasto_liso_elevado.glb"
bpy.ops.export_scene.gltf(
    filepath=str(archivo), export_format="GLB", use_selection=True, export_materials="EXPORT",
    export_apply=True
)
raw = archivo.read_bytes()
assert raw[:4] == b"glTF" and struct.unpack_from("<I", raw, 8)[0] == len(raw)
n = struct.unpack_from("<I", raw, 12)[0]
gltf = json.loads(raw[20:20 + n])
assert len(gltf.get("meshes", [])) == 2, "Deben exportarse exactamente dos mallas"

# Crear cámara e iluminación SOLO para la vista previa y el proyecto editable .blend.
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.camera_add(location=(24, -29, 26))
camara = bpy.context.object
camara.name = "Camara isometrica"
objetivo = Vector((0, 0, 0.65))
camara.rotation_euler = (objetivo - camara.location).to_track_quat("-Z", "Y").to_euler()
camara.data.type = "ORTHO"
camara.data.ortho_scale = 31
bpy.context.scene.camera = camara

for ubicacion, potencia, tamaño in [
    ((-8, -12, 16), 1700, 12),
    ((8, 7, 13), 950, 10),
]:
    bpy.ops.object.light_add(type="AREA", location=ubicacion)
    luz = bpy.context.object
    luz.data.energy = potencia
    luz.data.size = tamaño

escena = bpy.context.scene
escena.render.engine = "BLENDER_EEVEE"
escena.render.film_transparent = True
escena.render.resolution_x = 1000
escena.render.resolution_y = 750
escena.render.resolution_percentage = 100
escena.render.image_settings.file_format = "PNG"
escena.render.image_settings.color_mode = "RGBA"
escena.render.filepath = str(SALIDA / "vista_previa.png")
escena.camera.data.lens = 45
escena.world.color = (0.15, 0.15, 0.15)
bpy.ops.wm.save_as_mainfile(filepath=str(SALIDA / "escenario_pasto_liso.blend"))
bpy.ops.render.render(write_still=True)

imagen = SALIDA / "vista_previa.png"
assert imagen.read_bytes()[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10)), "No se generó PNG válido"
datos = {
    "escenario": "01 - Pasto liso elevado",
    "generador": "Blender mediante GitHub Actions",
    "ancho_m": ANCHO, "largo_m": LARGO,
    "altura_tierra_m": ALTURA_TIERRA,
    "espesor_pasto_m": ESPESOR_PASTO,
    "altura_superficie_caminable_m": ALTURA_CIMA,
    "superficie": "completamente plana, sin montanas, rampas, arboles ni obstaculos",
    "salidas": [
        "escenario_pasto_liso_elevado.glb",
        "escenario_pasto_liso.blend",
        "vista_previa.png"
    ],
}
(SALIDA / "informe.json").write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
print("ESCENARIO_PASTO_LISO_OK", archivo.stat().st_size, "bytes")
