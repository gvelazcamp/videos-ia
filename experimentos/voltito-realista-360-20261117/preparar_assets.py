"""Extrae las 4 vistas del Voltito de la lámina suministrada por el usuario.

No inventa vistas ni sustituye el diseño original.
Los recortes se guardan exclusivamente en este nuevo experimento.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from io import BytesIO
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageDraw

HERE = Path(__file__).resolve().parent
HERE.mkdir(parents=True, exist_ok=True)
SOURCE_URL = "https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/0f216be5-1845-4ae7-a374-8ed71fb5bf21.png"
ORIGINAL = HERE / "voltito-hoja-original.png"
BOXES = {
    "frente": (590, 20, 825, 345),
    "izquierda": (840, 20, 1030, 345),
    "derecha": (1050, 20, 1237, 345),
    "espalda": (1260, 20, 1520, 345),
}
CANVAS_SIZE = (460, 560)

def load_reference():
    if not ORIGINAL.exists():
        with urlopen(Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=65) as res:
            data = res.read(12_000_000)
        with Image.open(BytesIO(data)) as src:
            src.load()
            if src.size != (1536, 1152):
                raise ValueError(f"Dimensiones inesperadas {src.size}; evitar recortes incorrectos.")
            src.convert("RGB").save(ORIGINAL, "PNG", optimize=True)
    result = Image.open(ORIGINAL).convert("RGB")
    if result.size != (1536, 1152):
        raise ValueError("Referencia incompatible con los límites de recorte")
    return result

def cutout(image):
    rgb = np.asarray(image)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    saturation = hsv[:, :, 1]
    bright = hsv[:, :, 2]
    # Fondo gris muy poco saturado; pelaje y detalles del macaco son de color vivo.
    raw = np.uint8((saturation > 43) & (bright > 85)) * 255
    raw[:9, :] = 0
    raw[-2:, :] = 0
    raw[:, :4] = 0
    raw[:, -4:] = 0
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=2)
    contours, _ = cv2.findContours(raw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No hay figura en el recorte")
    largest = max(contours, key=cv2.contourArea)
    mask = np.zeros(raw.shape, np.uint8)
    cv2.drawContours(mask, [largest], -1, 255, -1)
    mask = cv2.GaussianBlur(mask, (3, 3), .6)
    rgba = Image.fromarray(np.dstack([rgb, mask]), "RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("La máscara dejó el recorte vacío")
    return rgba.crop(bbox)

def make_sprite(image):
    sprite = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    im = image.copy()
    im.thumbnail((418, 505), Image.Resampling.LANCZOS)
    x = (CANVAS_SIZE[0] - im.width) // 2
    y = 536 - im.height
    sprite.alpha_composite(im, (x, y))
    return sprite

def main():
    source = load_reference()
    for name, box in BOXES.items():
        cut = cutout(source.crop(box))
        sprite = make_sprite(cut)
        destination = HERE / f"voltito-{name}.png"
        sprite.save(destination, "PNG", optimize=True)
        with Image.open(destination) as check:
            check.load()
            assert check.size == CANVAS_SIZE and check.mode == "RGBA"
            assert check.getchannel("A").getextrema() == (0, 255)
        print(f"{name}: PNG con transparencia {destination}, {cut.size}")
    # Miniatura para que GitHub muestre un adelanto sin ejecutar JS.
    preview = Image.new("RGB", (1720, 660), "#edf5f3")
    d = ImageDraw.Draw(preview)
    for i, view in enumerate(BOXES):
        with Image.open(HERE / f"voltito-{view}.png") as sprite:
            target = sprite.copy()
            target.thumbnail((390, 510), Image.Resampling.LANCZOS)
            preview.paste(target, (35+i*424, 35), target)
        d.text((70+i*424, 568), view.upper(), fill="#244b57", stroke_width=0)
    preview.save(HERE / "vista-previa.png", "PNG", optimize=True)
    print("Preparación completa.")

if __name__ == "__main__":
    main()
