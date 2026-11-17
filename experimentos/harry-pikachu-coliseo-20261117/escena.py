"""Montaje fan art Harry Potter + Pikachu Impactrueno en Coliseo de Roma.
Solo crea archivos en esta carpeta, reutilizando Remove.bg web del puente.
No sustituye ninguno de los experimentos anteriores.
"""
from __future__ import annotations

import io
import json
import math
import random
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
W, H = 1600, 900
RNG = random.Random(37116)
SOURCE_URLS = {
    "harry": [
        "https://image.pngaaa.com/943/236943-middle.png",
        "https://www.kindpng.com/picc/m/48-487943_harry-potter-png-transparent-harry-potter-uniform-gryffindor.png",
        "https://clipart-library.com/images_k/harry-potter-transparent-background/harry-potter-transparent-background-10.jpg",
    ],
    "pikachu": [
        "https://w7.pngwing.com/pngs/359/444/png-transparent-pikachu-art-t-shirt-pikachu-mammal-vertebrate-computer-wallpaper.png",
        "https://www.vhv.rs/dpng/d/248-2489032_thunderbolt-drawing-pikachu-transparent-cartoons-pikachu-thunderbolt-no.png",
        "https://www.pngall.com/wp-content/uploads/5/Cute-Pikachu.png",
    ],
    "coliseo": [
        "https://upload.wikimedia.org/wikipedia/commons/9/98/Colosseum_interior_2012.jpg",
        "https://assets.editorial.aetnd.com/uploads/2023/01/stadium-roman-coliseum-gettyimages-548844599.jpg?crop=2048%3A1152%2Csmart&height=1152&quality=75&width=2048",
        "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=2000&q=85",
    ],
}

def download_image(name: str, dest: Path) -> str:
    errors = []
    for url in SOURCE_URLS[name]:
        try:
            req = Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                "Accept": "image/avif,image/webp,image/png,image/jpeg,image/*;q=0.8",
            })
            with urlopen(req, timeout=28) as response:
                content = response.read(15_000_001)
            if len(content) > 15_000_000:
                raise ValueError("Referencia mayor a 15 MB")
            with Image.open(io.BytesIO(content)) as im:
                im.load()
                if min(im.size) < 240:
                    raise ValueError(f"Imagen demasiado pequeña: {im.size}")
                im = ImageOps.exif_transpose(im)
                im.convert("RGB").save(dest, "PNG", optimize=True)
                print(f"REFERENCIA {name}: {url} | {im.size} -> {dest.relative_to(ROOT)}", flush=True)
            return url
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {exc} ({url})")
            print(f"Intento fallido {name}: {errors[-1]}", flush=True)
    raise RuntimeError(f"No hay referencia descargable para {name}. " + " ; ".join(errors))

def preparar() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    sources = {}
    for item in ("harry", "pikachu", "coliseo"):
        sources[item] = download_image(item, DIR / f"{item}-referencia.png")
    (DIR / "fuentes.json").write_text(json.dumps(sources, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

def rgba_person(path: Path, h: int, flip: bool = False) -> Image.Image:
    with Image.open(path) as input_im:
        input_im.load()
        rgba = input_im.convert("RGBA")
    alpha = rgba.getchannel("A")
    lo, hi = alpha.getextrema()
    if lo == hi or hi < 200:
        raise ValueError(f"Recorte inválido (sin transparencia y sujeto): {path} ({lo},{hi})")
    bb = alpha.getbbox()
    if not bb:
        raise ValueError(f"PNG vacío: {path}")
    rgba = rgba.crop(bb)
    if flip:
        rgba = ImageOps.mirror(rgba)
    width = round(h*rgba.width/rgba.height)
    if width > 850:
        h = round(h*850/width)
        width = 850
    rgba = rgba.resize((width, h), Image.Resampling.LANCZOS)
    return rgba

def place_person(canvas: Image.Image, person: Image.Image, center: int, baseline: int):
    left = center - person.width//2
    top = baseline - person.height
    if left < 0 or top < 0 or left+person.width > W or top+person.height > H:
        raise ValueError(f"Personaje fuera de escena: {left}, {top}, {person.size}")
    shadow = Image.new("RGBA", canvas.size)
    d = ImageDraw.Draw(shadow)
    d.ellipse((center-person.width*.44, baseline-18,
               center+person.width*.44, baseline+19), fill=(9, 11, 17, 143))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
    # Refuerzo de contraste, preservando pixeles transparentes.
    canvas.alpha_composite(person, (left, top))
    return (left, top, left+person.width, top+person.height)

def glow_dots(layer: Image.Image, center: tuple[int,int], color, count: int, area: int):
    d = ImageDraw.Draw(layer)
    cx, cy = center
    for _ in range(count):
        dx = int(RNG.gauss(0, area*.45))
        dy = int(RNG.gauss(0, area*.45))
        rr = RNG.randint(1, 5)
        opacity = RNG.randint(80, 240)
        d.ellipse((cx+dx-rr,cy+dy-rr,cx+dx+rr,cy+dy+rr), fill=(*color,opacity))

def jagged_line(start, end, steps=12, wobble=26):
    sx,sy=start;ex,ey=end
    pts=[(sx,sy)]
    for i in range(1,steps):
        t=i/steps
        jitter=RNG.uniform(-wobble,wobble)
        pts.append((int(sx+(ex-sx)*t + jitter*.38),
                    int(sy+(ey-sy)*t+jitter)))
    pts.append((ex,ey))
    return pts

def add_effects(canvas: Image.Image, harry_bounds, pikachu_bounds):
    # Los efectos se trazan DESPUÉS de recortar y colocar los personajes.
    # Magia celeste sale de la dirección de la varita; la electricidad amarilla desde Pikachu.
    bx,by,bx2,by2 = harry_bounds
    px,py,px2,py2 = pikachu_bounds
    # La localización de la varita varía entre fotografías; el origen se sitúa
    # ligeramente por encima/delante de Harry para simular que la sostiene.
    wand = (int(bx + (bx2-bx)*.45), int(by + (by2-by)*.24))
    cheeks = (int(px + (px2-px)*.35), int(py + (py2-py)*.53))
    collision = (810, 465)
    glow = Image.new("RGBA",canvas.size,(0,0,0,0))
    d=ImageDraw.Draw(glow)

    # Luz ambiental sobre los rivales.
    d.ellipse((wand[0]-110,wand[1]-110,wand[0]+110,wand[1]+110), fill=(18,200,255,75))
    d.ellipse((cheeks[0]-130,cheeks[1]-130,cheeks[0]+130,cheeks[1]+130),fill=(255,218,48,72))
    d.ellipse((collision[0]-100,collision[1]-100,collision[0]+100,collision[1]+100),
              fill=(255,255,230,165))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(48)))
    bolts=Image.new("RGBA",canvas.size,(0,0,0,0))
    b=ImageDraw.Draw(bolts)
    # Hechizo azul desde Harry, chispas hacia el punto de encuentro.
    magic = jagged_line(wand,collision,steps=18,wobble=38)
    b.line(magic, fill=(32,210,255,240),width=13,joint="curve")
    b.line(magic, fill=(210,255,255,255),width=4,joint="curve")
    # Impactrueno desde Pikachu con un tronco principal y 4 ramificaciones.
    bolt = jagged_line(cheeks,collision,steps=14,wobble=55)
    b.line(bolt,fill=(255,180,10,255),width=20,joint="curve")
    b.line(bolt,fill=(255,250,85,255),width=11,joint="curve")
    b.line(bolt,fill=(255,255,238,255),width=4,joint="curve")
    for k in (3,5,7,9):
        x,y=bolt[k]
        branch=(x+RNG.randint(-95,95), y+RNG.randint(-105,100))
        b.line(jagged_line((x,y),branch,steps=5,wobble=15),
               fill=(255,237,64,220),width=5,joint="curve")
    # Órbita de luz del choque.
    for radius,width in ((73,5),(47,5),(28,4)):
        b.arc((collision[0]-radius,collision[1]-radius,
               collision[0]+radius,collision[1]+radius),
               start=RNG.randint(0,70),end=330,fill=(224,252,255,210),width=width)
    b.ellipse((collision[0]-17,collision[1]-17,
               collision[0]+17,collision[1]+17),fill=(255,255,255,240))
    glow_dots(b, wand,(72,230,255),150,210)
    glow_dots(b,cheeks,(255,227,39),150,180)
    glow_dots(b,collision,(255,255,222),130,200)
    halo=bolts.filter(ImageFilter.GaussianBlur(15))
    halo.putalpha(halo.getchannel("A").point(lambda v: min(210,int(v*.8))))
    canvas.alpha_composite(halo)
    canvas.alpha_composite(bolts)
    print(f"Efectos: varita {wand}; mejillas {cheeks}; impacto {collision}",flush=True)

def componer():
    bg = DIR / "coliseo-referencia.png"
    with Image.open(bg) as src:
        src.load()
        base = ImageOps.fit(src.convert("RGB"), (W,H), Image.Resampling.LANCZOS,
                            centering=(.5,.53))
    base = ImageEnhance.Contrast(base).enhance(1.12)
    base = ImageEnhance.Color(base).enhance(0.94)
    scene=base.convert("RGBA")

    # Viñeta sutil para dar profundidad a la escena.
    vignette=Image.new("RGBA",(W,H),(0,0,0,0))
    vd=ImageDraw.Draw(vignette)
    for i in range(90):
        a=int(19*(1-i/90))
        vd.rectangle((i*6,i*4,W-i*6,H-i*4),outline=(7,12,25,a),width=7)
    scene.alpha_composite(vignette)

    harry=rgba_person(DIR/"harry-transparente.png",height_for_harry())
    pika=rgba_person(DIR/"pikachu-transparente.png",410,flip=True)
    hb=place_person(scene,harry,center=390,baseline=852)
    pb=place_person(scene,pika,center=1190,baseline=815)
    add_effects(scene,hb,pb)
    outfile=DIR/"harry-potter-pikachu-impactrueno-coliseo.png"
    scene.convert("RGB").save(outfile,"PNG",optimize=True)
    with Image.open(outfile) as verify:
        verify.load()
        assert verify.size==(W,H) and verify.format=="PNG"
    print("IMAGEN FINAL VERIFICADA:",outfile,"|", W, H,flush=True)

def height_for_harry():
    return 640

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv)>1 else ""
    if command=="preparar":
        preparar()
    elif command=="componer":
        componer()
    else:
        raise SystemExit("Uso: escena.py preparar|componer")
