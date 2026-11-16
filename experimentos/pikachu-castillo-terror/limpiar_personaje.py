#!/usr/bin/env python3
"""Genera PNG transparente desde la foto original; sin redibujar el personaje.

Limitado a experimento pikachu-castillo-terror, preservando la imagen original.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'experimentos/pikachu-surf-3ia/referencia-original.png'
OLD = ROOT / 'experimentos/pikachu-surf-3ia/recorte-personaje.webp'
OUTPUT = HERE / 'personaje-original-transparente.png'

def build(original, previous):
    original = original.convert('RGBA')
    previous = previous.convert('RGBA')
    if original.size != (298, 342) or previous.size != original.size:
        raise ValueError('Referencia inesperada; no modificar el PNG')
    array = np.array(original)
    old_alpha = np.array(previous)[:, :, 3]
    r, g, b = [array[:, :, i].astype(np.float32) for i in range(3)]
    yy, xx = np.indices((342, 298))
    yellow = (r > 175) & (g > 187) & (r / np.maximum(g, 1) < 1.175) & (g - b > 100) & (b < 131)
    cheek_area = ((xx > 94) & (xx < 125) & (yy > 103) & (yy < 172)) | ((xx > 215) & (xx < 258) & (yy > 127) & (yy < 190))
    red = (r > 137) & (r - g > 55) & (g < 168) & (b < 165) & cheek_area
    seed = ((yellow | red) & (old_alpha > 12)).astype(np.uint8) * 255
    disk5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    disk3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    seed = cv2.morphologyEx(seed, cv2.MORPH_CLOSE, disk5)
    seed = cv2.morphologyEx(seed, cv2.MORPH_OPEN, disk3)
    contours, _ = cv2.findContours(seed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    alpha = np.zeros(seed.shape, dtype=np.uint8)
    for contour in contours:
        if cv2.contourArea(contour) > 15:
            cv2.drawContours(alpha, [contour], -1, 255, -1)
    # Conserva la franja de la cola, no los restos del fondo marrón.
    details = Image.new('L', original.size, 0)
    brush = ImageDraw.Draw(details)
    brush.polygon([(91,133),(97,154),(91,160),(77,182),(73,189),(70,203),
                   (68,221),(72,241),(80,257),(67,253),(62,239),(62,225),
                   (58,216),(60,205),(64,194),(70,181),(78,166)], fill=255)
    alpha = np.maximum(alpha, np.minimum(np.asarray(details), old_alpha))
    alpha = cv2.dilate(alpha, disk3, iterations=1)
    alpha = np.minimum(alpha, old_alpha)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0.6)
    # Une los pies al cuerpo sin recuperar el sombreado rectangular del suelo.
    bridges = Image.new('L', original.size, 0)
    brush = ImageDraw.Draw(bridges)
    brush.polygon([(75,293),(93,303),(109,306),(128,302),(128,311),
                   (119,315),(114,322),(108,330),(97,338),(83,341),
                   (77,329),(76,316)], fill=255)
    brush.polygon([(204,300),(228,295),(240,293),(245,305),(250,327),
                   (248,340),(237,338),(220,326),(211,319)], fill=255)
    alpha = np.maximum(alpha, np.minimum(np.asarray(bridges), old_alpha))
    array[:, :, 3] = alpha
    result = Image.fromarray(array, 'RGBA')
    if result.getpixel((0, 0))[3] != 0 or result.getpixel((150, 200))[3] < 250:
        raise ValueError('Fallo del canal alfa; detener')
    return result

if __name__ == '__main__':
    result = build(Image.open(SOURCE), Image.open(OLD))
    result.save(OUTPUT, optimize=True)
    print('PNG RGBA generado:', OUTPUT, OUTPUT.stat().st_size, 'bytes', result.size)
