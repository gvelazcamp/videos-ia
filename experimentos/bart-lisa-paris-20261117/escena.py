"""Montaje aislado: Bart y Lisa patinando en París.
Reutiliza el PNG de Bart existente y el recorte de Lisa generado por remove.bg.
No cambia ni sobrescribe otros recursos del repositorio.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw

DIR = Path(__file__).parent
W, H = 1600, 900
BART = Path("experimentos/bart-patinando-20261117/bart-patinando-transparente.png")
LISA_URLS = [
    "https://image.pngaaa.com/529/590529-middle.png",
    "https://pngimg.com/uploads/simpsons/simpsons_PNG1.png",
]
PARIS_URLS = [
    "https://images.unsplash.com/photo-1758066277646-66d7eff85a66?auto=format&fit=crop&w=1920&q=88",
    "https://upload.wikimedia.org/wikipedia/commons/9/90/Eiffel_Tower_from_Rue_de_l%27Universit%C3%A9-5830121627.jpg",
]


def fetch_image(urls, dest: Path):
    failures = []
    for url in urls:
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; personal art project)"}), timeout=35) as res:
                raw = res.read(18_000_000)
            with Image.open(BytesIO(raw)) as im:
                im.load()
                if min(im.size) < 150:
                    raise ValueError("resolución insuficiente")
                im.convert("RGBA").save(dest)
                print(f"Fuente descargada {url} | {im.size}")
                return
        except Exception as exc:
            failures.append(f"{url}: {type(exc).__name__} {exc}")
    raise RuntimeError("No se pudo obtener la referencia:\n" + "\n".join(failures))


def resize_subject(path: Path, height: int) -> Image.Image:
    with Image.open(path) as im:
        src = im.convert("RGBA")
    alpha = src.getchannel("A")
    if alpha.getextrema() == (255, 255):
        raise ValueError(f"El sujeto no contiene transparencia: {path}")
    bb = alpha.getbbox()
    if not bb:
        raise ValueError(f"No hay píxeles visibles en el PNG: {path}")
    src = src.crop(bb)
    return src.resize((round(src.width * height / src.height), height), Image.Resampling.LANCZOS)


def paste_at_bottom(canvas: Image.Image, subject: Image.Image, center_x: int, baseline: int):
    x = int(center_x - subject.width / 2)
    y = baseline - subject.height
    if x < 0 or x + subject.width > canvas.width or y < 0 or y + subject.height > canvas.height:
        raise ValueError("Composición fuera del lienzo")
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((center_x - subject.width * .33, baseline - 18, center_x + subject.width * .33, baseline + 16), fill=(15, 22, 30, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(13))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(subject, (x, y))


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    if not BART.is_file():
        raise FileNotFoundError(f"No existe Bart original: {BART}")

    lisa_ref = DIR / "lisa-referencia.png"
    lisa_cut = DIR / "lisa-transparente.png"
    bg_ref = DIR / "paris-referencia.png"

    # La primera fase descarga fuentes; la segunda compone luego de Remove.bg.
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "preparar":
        fetch_image(LISA_URLS, lisa_ref)
        fetch_image(PARIS_URLS, bg_ref)
        return

    if len(sys.argv) != 2 or sys.argv[1] != "montar":
        raise SystemExit("Uso: python escena.py preparar|montar")
    for path in (lisa_cut, bg_ref):
        if not path.is_file():
            raise FileNotFoundError(f"Falta {path}; ejecutar la preparación y el recorte web")

    with Image.open(bg_ref) as bg:
        base = ImageOps.fit(bg.convert("RGB"), (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
    base = ImageEnhance.Color(base).enhance(1.08)
    base = ImageEnhance.Contrast(base).enhance(1.04)
    canvas = base.convert("RGBA")

    # Los personajes se sitúan en los laterales; la Torre Eiffel queda visible.
    lisa = resize_subject(lisa_cut, height=535)
    bart = resize_subject(BART, height=540)
    paste_at_bottom(canvas, lisa, center_x=395, baseline=866)
    paste_at_bottom(canvas, bart, center_x=1200, baseline=872)

    out = DIR / "bart-y-lisa-patinando-en-paris.png"
    canvas.convert("RGB").save(out, format="PNG", optimize=True)
    with Image.open(out) as check:
        check.verify()
    print(f"Imagen terminada: {out} | {W}x{H}")


if __name__ == "__main__":
    main()
