"""Recortar por el sitio web de remove.bg usando Playwright (SIN API).

El proceso gratuito NO inicia sesión, NO usa claves API, NO compra créditos,
y solo descarga la vista previa gratuita. Si el sitio cambia o pide
interacción humana, la acción falla claramente sin saltar protecciones.
"""
import os
import re
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

ROOT = Path.cwd().resolve()
DEFAULT_IN = "experimentos/pikachu-surf-3ia/referencia-original.png"
DEFAULT_OUT = "experimentos/pikachu-castillo-terror/personaje-removebg-web.png"
MAX_SOURCE_BYTES = 22 * 1024 * 1024


def ruta_repo(value: str, *, dest: bool = False) -> Path:
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise ValueError("La ruta debe ser relativa y permanecer dentro del repositorio.")
    if dest and (p.suffix.lower() != ".png" or p.parts[0] not in ("experimentos", "recortes")):
        raise ValueError("Destino no permitido: debe ser PNG bajo experimentos/ o recortes/.")
    path = (ROOT / p).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("La ruta sale del repositorio.")
    return path


def main() -> None:
    origen = ruta_repo(os.getenv("IMAGE_PATH", DEFAULT_IN))
    destino = ruta_repo(os.getenv("OUTPUT_PATH", DEFAULT_OUT), dest=True)
    if not origen.is_file():
        raise FileNotFoundError(f"No existe la imagen de origen: {origen.relative_to(ROOT)}")
    if origen.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        raise ValueError("El origen debe ser JPG, PNG o WebP.")
    if origen.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("La imagen supera los 22 MB.")
    with Image.open(origen) as img:
        img.verify()

    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_name(destino.stem + ".temporal.png")
    print(f"ORIGEN: {origen.relative_to(ROOT)}")
    print("Modo: navegador web anónimo, descarga Preview/Free, sin API, sin pagos.")

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context(locale="en-US", accept_downloads=True,
                                          viewport={"width": 1280, "height": 850})
            page = context.new_page()
            page.goto("https://www.remove.bg/", wait_until="domcontentloaded", timeout=60000)

            with page.expect_file_chooser(timeout=20000) as chooser:
                page.get_by_role("button", name="Upload Image").first.click()
            chooser.value.set_files(str(origen))
            page.wait_for_url(re.compile(r"www\.remove\.bg/upload"), timeout=60000)

            download_btn = page.get_by_role("button", name=re.compile(r"^Download", re.I)).first
            download_btn.wait_for(state="visible", timeout=90000)
            # El menú ofrece Preview/Free y, según la imagen, Max/HD.
            # Seleccionar EXCLUSIVAMENTE Preview evita consumir créditos.
            download_btn.click()
            free_btn = page.get_by_role("button", name=re.compile(r"Preview.*Free", re.I)).first
            free_btn.wait_for(state="visible", timeout=15000)

            with page.expect_download(timeout=60000) as download:
                free_btn.click()
            download.value.save_as(str(tmp))
            context.close()
            browser.close()

        with Image.open(tmp) as output:
            output.load()
            if output.format != "PNG":
                raise ValueError(f"remove.bg entregó {output.format}, no PNG.")
            rgba = output.convert("RGBA")
            alpha = rgba.getchannel("A")
            minimum, maximum = alpha.getextrema()
            if maximum == 0 or minimum == 255:
                raise ValueError("Resultado inválido: no contiene sujeto y transparencia.")
            rgba.save(destino, "PNG", optimize=True)
            print(f"OK: {destino.relative_to(ROOT)} | {rgba.width}x{rgba.height} RGBA | alpha={minimum}..{maximum}")
            print("Aviso: el sitio gratuito puede reducir las imágenes grandes a una vista previa.")
    except (PlaywrightTimeout, Exception) as error:
        print(f"ERROR EN remove.bg WEB: {type(error).__name__}: {error}")
        print("No se evita CAPTCHA, pago ni bloqueo del sitio; no se modifica el PNG existente.")
        raise
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
