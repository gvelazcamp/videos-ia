"""Montaje nuevo: Bart y Lisa sobre el escenario caricaturesco de París provisto por el usuario.
Conserva el escenario completo, usa recortes existentes y no altera la escena anterior.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFilter

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]
SOURCE_URL = "https://d2ol7oe51mr4n9.cloudfront.net/user_3I6MEpvFp5hLW0psUqgXdDfyZXe/a4b34166-357e-4577-adcd-ffcbdacdce6d.png"
BACKGROUND = DIR / "escenario-paris-caricatura-original.png"
OUTPUT = DIR / "bart-y-lisa-en-este-paris.png"
BART = ROOT / "experimentos/bart-patinando-20261117/bart-patinando-transparente.png"
LISA = ROOT / "experimentos/bart-lisa-paris-20261117/lisa-transparente.png"


def download_reference():
    if BACKGROUND.exists():
        with Image.open(BACKGROUND) as im:
            im.verify()
        print("Escenario ya descargado y verificado.")
        return
    req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=65) as response:
        raw = response.read(12_000_000)
    with Image.open(BytesIO(raw)) as im:
        im.load()
        if im.size != (1672, 941):
            raise ValueError(f"La imagen recibida no corresponde al escenario enviado: {im.size}")
        im.convert("RGB").save(BACKGROUND, format="PNG", optimize=True)
    print("Escenario del usuario guardado en Git:", BACKGROUND.name)


def load_and_scale(path: Path, height: int) -> Image.Image:
    with Image.open(path) as im:
        im.load()
        rgba = im.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema()[0] == 255:
        raise ValueError(f"Falta canal alfa transparente en {path}")
    bounds = alpha.getbbox()
    if not bounds:
        raise ValueError(f"Recorte completamente transparente en {path}")
    rgba = rgba.crop(bounds)
    target_width = round(rgba.width * height / rgba.height)
    return rgba.resize((target_width, height), Image.Resampling.LANCZOS)


def place(canvas: Image.Image, person: Image.Image, x_center: int, baseline: int):
    left = x_center - person.width // 2
    top = baseline - person.height
    if left < 0 or top < 0 or left + person.width > canvas.width or top + person.height > canvas.height:
        raise ValueError("El personaje se sale de la imagen")
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    rx = person.width * .38
    draw.ellipse((x_center-rx, baseline-17, x_center+rx, baseline+10), fill=(28, 36, 51, 115))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)))
    canvas.alpha_composite(person, (left, top))


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    download_reference()
    with Image.open(BACKGROUND) as source:
        canvas = source.convert("RGBA")
    if canvas.size != (1672, 941):
        raise ValueError("No se debe recortar ni deformar el escenario del usuario")

    lisa = load_and_scale(LISA, 320)
    bart = load_and_scale(BART, 380)
    # Sobre la vereda central: dejar visibles el café, la Torre Eiffel y el río.
    place(canvas, lisa, x_center=775, baseline=888)
    place(canvas, bart, x_center=1050, baseline=903)

    canvas.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    with Image.open(OUTPUT) as check:
        check.load()
        assert check.format == "PNG" and check.size == (1672, 941)
    print(f"Montaje final correcto: {OUTPUT}, 1672 × 941")


if __name__ == "__main__":
    main()
