"""Publica un PNG individual de Voltito con transparencia real.
Usa únicamente la imagen original ya aprobada en el repositorio.
No cambia modelos 3D, vistas anteriores ni otros assets.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
SOURCE = ROOT / "experimentos/voltito-realista-360-20261117/voltito-hoja-original.png"
OUTPUT = DIR / "voltito-sonriente-transparente.png"

def main():
    with Image.open(SOURCE) as image:
        image.load()
        if image.size != (1536, 1152):
            raise ValueError(f"Referencia inesperada: {image.size}")
        original = image.convert("RGB")

    # La figura grande ocupa la izquierda de la lámina. Los textos y
    # botones de la ficha quedan fuera del componente conexo principal.
    rgb = np.asarray(original.crop((20, 0, 585, 865)))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    raw = np.uint8((hsv[:, :, 1] > 44) & (hsv[:, :, 2] > 65)) * 255
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=2)
    contours, _ = cv2.findContours(raw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No se detectó al personaje")
    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 150000:
        raise ValueError("La silueta es demasiado pequeña; no publicar recorte")

    alpha = np.zeros(raw.shape, dtype=np.uint8)
    cv2.drawContours(alpha, [largest], -1, 255, -1)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

    # Eliminar la sombra gris del suelo que rodea los pies sin perder
    # los tonos amarillos de las patas.
    for y in range(790, alpha.shape[0]):
        factor = np.clip((hsv[y, :, 1].astype(np.float32) - 24) / 42, 0, 1)
        alpha[y, :] = np.rint(alpha[y, :].astype(np.float32) * factor).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (5, 5), .8)

    cutout = Image.fromarray(np.dstack((rgb, alpha)), "RGBA")
    bbox = cutout.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Máscara vacía")
    left = max(0, bbox[0] - 5)
    top = max(0, bbox[1] - 5)
    right = min(cutout.width, bbox[2] + 5)
    bottom = min(cutout.height, bbox[3] + 5)
    cutout = cutout.crop((left, top, right, bottom))
    cutout = cutout.resize((cutout.width * 2, cutout.height * 2), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (1250, 1880), (0, 0, 0, 0))
    canvas.alpha_composite(cutout, ((canvas.width-cutout.width)//2, (canvas.height-cutout.height)//2))
    DIR.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, "PNG", optimize=True)

    with Image.open(OUTPUT) as check:
        check.load()
        assert check.format == "PNG" and check.mode == "RGBA"
        assert check.size == (1250, 1880)
        assert check.getchannel("A").getextrema() == (0, 255)
        assert check.getpixel((0, 0))[3] == 0
        assert check.getpixel((check.width-1, check.height-1))[3] == 0
    print("PNG transparente validado:", OUTPUT.relative_to(ROOT), "1250x1880")

if __name__ == "__main__":
    main()
