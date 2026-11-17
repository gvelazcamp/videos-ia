#!/usr/bin/env python3
"""Mockup fotográfico de remera con la ilustración original Goku + Snorlax.
No altera juegos, videos ni el puente de las IA.
"""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import math
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "fuente-original.webp"
SHIRT = ROOT / "remera-goku-snorlax-real.png"
PRINT = ROOT / "estampado-goku-snorlax-transparente.png"
PHOTO_URLS = [
    "https://mockups-design-com.b-cdn.net/wp-content/uploads/2021/08/Hanging_T-Shirt_Mockup_2.jpg",
    "https://mockups-design.com/wp-content/uploads/2021/08/Hanging_T-Shirt_Mockup_2.jpg",
]

def mockup_fotografico() -> Image.Image:
    for url in PHOTO_URLS:
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TShirtPreview/1.0)"})
            with urlopen(req, timeout=40) as r:
                raw = r.read(10 * 1024 * 1024)
            img = Image.open(BytesIO(raw)).convert("RGB")
            if img.width < 700 or img.height < 500:
                raise ValueError("Foto demasiado pequeña")
            # Coordenadas calibradas para la fotografía real (1000 x 667).
            return img.resize((1000, 667), Image.Resampling.LANCZOS)
        except Exception as exc:
            print("No se pudo leer la foto:", type(exc).__name__, str(exc)[:160])
    raise RuntimeError("No se consiguió el mockup fotográfico. Se conserva la fuente y no se publica una remera falsa.")

def formar_estampado(fuente: Image.Image, w: int, h: int, margen: int) -> Image.Image:
    tinta = fuente.convert("RGB").resize((w, h), Image.Resampling.LANCZOS).convert("RGBA")
    # Bordes suavemente difuminados, tipo estampa fotográfica con transición al algodón.
    mascara = Image.new("L", (w, h))
    d = ImageDraw.Draw(mascara)
    d.rounded_rectangle((margen, margen, w-margen-1, h-margen-1),
                        radius=max(16, 5*margen), fill=255)
    mascara = mascara.filter(ImageFilter.GaussianBlur(margen*1.7))
    # Mantiene los colores originales en el centro.
    tinta.putalpha(mascara)
    return tinta

def aplicar_luz_de_tela(base: Image.Image, tinta: Image.Image, x: int, y: int) -> None:
    # Sombra y brillo reales de la remera modifican ligeramente el estampado.
    w, h = tinta.size
    fondo = np.asarray(base.crop((x,y,x+w,y+h)).convert("RGB"), dtype=np.float32)
    arte = np.asarray(tinta, dtype=np.uint8).copy()
    luz = fondo.mean(axis=2)/245
    luz = np.clip(0.79 + 0.21*luz, 0.81, 1.01)
    rgb = np.clip(arte[:,:,:3].astype(np.float32) * luz[:,:,None],0,255).astype(np.uint8)
    arte[:,:,:3] = rgb
    base.paste(Image.fromarray(arte,"RGBA"),(x,y),Image.fromarray(arte[:,:,3],"L"))

def main() -> None:
    assert SOURCE.is_file(), f"Falta {SOURCE.name}"
    fuente = Image.open(SOURCE).convert("RGB")
    assert fuente.width >= 200 and fuente.height >= 150
    base = mockup_fotografico()
    # Foto original 1000 x 667. Área imprimible centrada en el torso.
    print_w, print_h = 268, 201
    x, y = 368, 272
    tinta = formar_estampado(fuente, print_w, print_h, 5)
    aplicar_luz_de_tela(base, tinta, x, y)
    out = base.resize((1600,1067),Image.Resampling.LANCZOS)
    SHIRT.parent.mkdir(parents=True,exist_ok=True)
    out.save(SHIRT,format="PNG",optimize=True)

    # También deja el diseño separado sin remera, con transparencia efectiva.
    estampado = formar_estampado(fuente,1200,900,25)
    estampado.save(PRINT,format="PNG",optimize=True)
    with Image.open(PRINT) as i:
        lo,hi = i.getchannel("A").getextrema()
        assert lo == 0 and hi == 255, "Estampado sin transparencia real"
    with Image.open(SHIRT) as i:
        assert i.size == (1600,1067)
    print("OK: remera fotografica",SHIRT.stat().st_size,"bytes")
    print("OK: estampado transparente",PRINT.stat().st_size,"bytes")

if __name__ == "__main__":
    main()
