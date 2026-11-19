#!/usr/bin/env python3
"""Escenario 02: conservar la plataforma 18 x 18 m y agregar árboles y colinas suaves.
Blender en GitHub Actions; proyecto/GLB originales del Escenario 01 intactos.
"""
import json
import math
import struct
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resultado"
OUT.mkdir(parents=True, exist_ok=True)

ANCHO = LARGO = 18.0
TIERRA_H = 1.20
BASE_PASTO = 1.28
GRID = 52

# Tres montañitas redondeadas; los bordes permanecen planos.
COLINAS = (
    (-4.5, 3.5, 1.75, 2.15),
    (4.2, 3.8, 1.55, 2.1),
    (3.8, -3.8, 1.25, 1.9),
)
ARBOLES = (
    (-7.0, -6.1, "pino", 1.00),
    (-7.1, 0.7, "redondo", 1.15),
    (-7.1, 6.9, "pino", 0.85),
    (-2.0, 7.1, "redondo", 1.06),
    (2.0, 7.0, "pino", 0.95),
    (7.1, 6.8, "redondo", 0.98),
    (7.2, 0.8, "pino", 1.10),
    (7.0, -6.7, "redondo", 1.04),
    (0.1, -7.0, "pino", 0.90),
    (-5.9, -3.4, "redondo", 0.92),
)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


def material(nombre, rgb):
    mat = bpy.data.materials.new(nombre)
    mat.diffuse_color = (*rgb, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = 0.95
    return mat


pasto = material("Pasto verde", (0.19, 0.51, 0.10))
tierra = material("Canto de tierra marrón", (0.36, 0.235, 0.145))
madera = material("Troncos marrón", (0.36, 0.20, 0.10))
hojas = [
    material("Hojas verde bosque", (0.075, 0.32, 0.085)),
    material("Hojas verde vivo", (0.11, 0.43, 0.10)),
    material("Hojas verde claro", (0.21, 0.53, 0.14)),
]


def altura(x, y):
    borde = max(0.0, min(1.0, (9.0 - abs(x)) / 1.25, (9.0 - abs(y)) / 1.25))
    suave = borde * borde * (3.0 - 2.0 * borde)
    onda = sum(
        a * math.exp(-0.5 * ((x - cx) ** 2 + (y - cy) ** 2) / (sigma ** 2))
        for cx, cy, a, sigma in COLINAS
    )
    return BASE_PASTO + suave * onda


def caja(nombre, dimensiones, centro, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centro)
    obj = bpy.context.object
    obj.name = nombre
    obj.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


base = caja("Plataforma base de tierra", (ANCHO, LARGO, TIERRA_H),
            (0, 0, TIERRA_H / 2), tierra)

# Una sola superficie continua con colinas: no son conos ni imágenes pegadas.
vertices = []
caras = []
for iy in range(GRID + 1):
    y = -LARGO / 2 + LARGO * iy / GRID
    for ix in range(GRID + 1):
        x = -ANCHO / 2 + ANCHO * ix / GRID
        vertices.append((x, y, altura(x, y)))
for iy in range(GRID):
    for ix in range(GRID):
        k = iy * (GRID + 1) + ix
        caras.append((k, k + 1, k + GRID + 2, k + GRID + 1))

# Cerrar los bordes del césped hasta la base marrón, sin huecos visibles.
perimetro = []
perimetro.extend(range(GRID + 1))
perimetro.extend(iy * (GRID + 1) + GRID for iy in range(1, GRID + 1))
perimetro.extend(GRID * (GRID + 1) + ix for ix in range(GRID - 1, -1, -1))
perimetro.extend(iy * (GRID + 1) for iy in range(GRID - 1, 0, -1))
inicios = []
for indice in perimetro:
    x, y, _ = vertices[indice]
    inicios.append(len(vertices))
    vertices.append((x, y, TIERRA_H))
for i in range(len(perimetro)):
    j = (i + 1) % len(perimetro)
    caras.append((perimetro[i], inicios[i], inicios[j], perimetro[j]))

mesh = bpy.data.meshes.new("Malla de terreno ondulado continuo")
mesh.from_pydata(vertices, [], caras)
mesh.update()
cesped = bpy.data.objects.new("Césped con tres montañitas suaves", mesh)
bpy.context.collection.objects.link(cesped)
cesped.data.materials.append(pasto)
for face in mesh.polygons:
    face.use_smooth = face.index < GRID * GRID

# El borde sigue horizontal; cada colina se puede recorrer como malla real.
assert all(abs(altura(9.0, v) - BASE_PASTO) < 1e-8 for v in (-9, -3, 0, 5, 9))
assert max(v[2] for v in vertices) > BASE_PASTO + 1.35


def cilindro(nombre, xy, z, radio, largo):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=radio, depth=largo,
                                        location=(xy[0], xy[1], z))
    obj = bpy.context.object
    obj.name = nombre
    obj.data.materials.append(madera)
    return obj


def copa_esferica(nombre, xy, z, radio, verde):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radio,
                                          location=(xy[0], xy[1], z))
    obj = bpy.context.object
    obj.name = nombre
    obj.data.materials.append(verde)
    return obj


def copa_pino(nombre, xy, z, radio, alto, verde):
    bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=radio, radius2=0.0,
                                    depth=alto, location=(xy[0], xy[1], z))
    obj = bpy.context.object
    obj.name = nombre
    obj.data.materials.append(verde)
    return obj


for n, (x, y, tipo, tamaño) in enumerate(ARBOLES, start=1):
    piso = altura(x, y)
    tronco_h = (1.45 if tipo == "redondo" else 1.70) * tamaño
    cilindro(f"Arbol {n:02d} - tronco", (x, y), piso + tronco_h / 2,
             0.16 * tamaño, tronco_h)
    if tipo == "redondo":
        copa_esferica(f"Arbol {n:02d} - copa baja", (x, y),
                      piso + tronco_h + 0.52 * tamaño, 0.94 * tamaño, hojas[n % 3])
        copa_esferica(f"Arbol {n:02d} - copa alta", (x + 0.16 * tamaño, y),
                      piso + tronco_h + 1.05 * tamaño, 0.80 * tamaño, hojas[(n + 1) % 3])
    else:
        for nivel, (sube, radio) in enumerate(((0.38, 1.00), (0.94, 0.77), (1.45, 0.55)), start=1):
            copa_pino(f"Arbol {n:02d} - pino capa {nivel}", (x, y),
                      piso + tronco_h + sube * tamaño,
                      radio * tamaño, 1.27 * tamaño, hojas[(n + nivel) % 3])

# Exportar únicamente mallas, sin cámara ni luces.
mallas = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
assert len(ARBOLES) == 10 and len(mallas) > 25
bpy.ops.object.select_all(action="DESELECT")
for obj in mallas:
    obj.select_set(True)
bpy.context.view_layer.objects.active = cesped
glb_path = OUT / "escenario_pasto_arboles_montanitas.glb"
bpy.ops.export_scene.gltf(
    filepath=str(glb_path), export_format="GLB", use_selection=True,
    export_materials="EXPORT", export_apply=True,
)
raw = glb_path.read_bytes()
assert raw[:4] == b"glTF" and struct.unpack_from("<I", raw, 8)[0] == len(raw)
jlen = struct.unpack_from("<I", raw, 12)[0]
gltf = json.loads(raw[20:20 + jlen])
assert len(gltf.get("meshes", [])) >= 25

# Cámara y luces para imagen de vista previa / .blend editable.
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.camera_add(location=(25, -29, 27))
cam = bpy.context.object
cam.rotation_euler = (Vector((0, 0, 1.35)) - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.type = "ORTHO"
cam.data.ortho_scale = 32.5
bpy.context.scene.camera = cam
for position, energy, size in (((-8, -12, 16), 1700, 12), ((8, 8, 13), 1100, 11)):
    bpy.ops.object.light_add(type="AREA", location=position)
    light = bpy.context.object
    light.data.energy = energy
    light.data.size = size
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.eevee.taa_render_samples = 32
scene.render.film_transparent = True
scene.render.resolution_x = 1100
scene.render.resolution_y = 820
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = str(OUT / "vista_previa.png")
scene.world.color = (0.15, 0.15, 0.15)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "escenario_pasto_arboles_montanitas.blend"))
bpy.ops.render.render(write_still=True)
assert (OUT / "vista_previa.png").read_bytes()[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10))
info = {
    "version": "Escenario 02 - arboles y montanitas",
    "base": "Escenario 01, 18 x 18 metros, plataforma de 1.28 m",
    "arboles": len(ARBOLES),
    "montanitas": len(COLINAS),
    "altura_base_m": BASE_PASTO,
    "altura_maxima_terreno_m": round(max(altura(x, y) for x, y, _ in vertices), 3),
    "tipo_colinas": "lomas redondeadas integradas al mismo terreno",
    "mallas_exportadas": len(gltf.get("meshes", [])),
    "original_intacto": "experimentos/escenario-pasto-liso-20261119/",
    "archivos": [
        "escenario_pasto_arboles_montanitas.glb",
        "escenario_pasto_arboles_montanitas.blend",
        "vista_previa.png"
    ]
}
(OUT / "informe.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("ESCENARIO_02_VALIDADO", info)
