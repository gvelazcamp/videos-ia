#!/usr/bin/env python3
"""Añade un panel que cambia automáticamente con cada turno, sin alterar la animación base.
Fuente: video aprobado (02). Salida: video distinto (03), mismos cuadros salvo la zona del menú.
No incluye controles para el espectador; es un reel, no un juego interactivo.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
W, H, FPS = 540, 960, 24
Y_PANEL = 729
HEIGHT = H - Y_PANEL

DEFAULT_SOURCE = HERE.parent / "pokemon-combate-02-referencia" / "pikachu-vs-cubone-estilo-aprobado.mp4"
OUTPUT = HERE / "pikachu-vs-cubone-panel-automatico.mp4"
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
for candidate in ["/usr/share/fonts/truetype/higgsfield/Metropolis-ExtraBold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
    if Path(candidate).exists():
        FONT_FILE = candidate
        break

# Esta tabla corresponde a los tiempos de la voz ORIGINAL de Gemini y los ataques de la pelea 02.
# (inicio, fin, atacante, ataque activo). No hay que inventar nuevos turnos.
TIMELINE = [
    (0.00,  7.90, "PIKACHU", None),
    (7.90, 16.80, "PIKACHU", "RAYO"),
    (16.80,22.50, "CUBONE",  "HUESO PALO"),
    (22.50,27.30, "PIKACHU", "ATAQUE RÁPIDO"),
    (27.30,32.20, "CUBONE",  "CABEZAZO"),
    (32.20,39.50, "PIKACHU", "COLA FÉRREA"),
    (39.50,45.00, "CUBONE",  "HUESOMERANG"),
    (45.00,54.60, "PIKACHU", "ATAQUE RÁPIDO"),
    (54.60,62.00, "PIKACHU", None),
]

# Posiciones fijas de los cuatro poderes, cambian al alternar Pokémon.
# Cubone conserva su tipo Tierra: NO le adjudicamos habilidades eléctricas.
POWERS = {
    "PIKACHU": [
        ("RAYO", "ELÉCTRICO", "PP 15/15", "#ffe06e", "⚡"),
        ("ATAQUE RÁPIDO", "NORMAL", "PP 30/30", "#e9eff7", "➤"),
        ("COLA FÉRREA", "ACERO", "PP 15/15", "#c2d5e7", "◆"),
        ("IMPACTRUENO", "ELÉCTRICO", "PP 30/30", "#ffd36c", "✦"),
    ],
    "CUBONE": [
        ("HUESO PALO", "TIERRA", "PP 20/20", "#f2d5ac", "◈"),
        ("CABEZAZO", "NORMAL", "PP 15/15", "#ede2d3", "➤"),
        ("HUESOMERANG", "TIERRA", "PP 10/10", "#dfa769", "↗"),
        ("EXCAVAR", "TIERRA", "PP 10/10", "#dcc09b", "▼"),
    ],
}

THEMES = {
    "PIKACHU": dict(outer="#a0c9ff", edge="#719aee", inside="#172541",
                   bar="#293c74", title="#fff4dd", badge="#ffe680", highlight="#fff5a0",
                   dark="#272945", subtitle="TIPO ELÉCTRICO"),
    "CUBONE": dict(outer="#f0be8e", edge="#c67a4e", inside="#38283c",
                  bar="#744255", title="#fff0dc", badge="#f4b16c", highlight="#ffde9b",
                  dark="#3a3040", subtitle="TIPO TIERRA"),
}

FONTS = {}
def font(size):
    if size not in FONTS:
        FONTS[size] = ImageFont.truetype(FONT_FILE, size)
    return FONTS[size]

def txt(d, xy, s, size, color, stroke=0):
    d.text((round(xy[0]), round(xy[1])), s, font=font(size), fill=color,
           stroke_width=stroke, stroke_fill="#232035")

def centered(d, mid, y, s, size, color):
    bounds = d.textbbox((0, 0), s, font=font(size))
    txt(d, (mid - (bounds[2] - bounds[0]) / 2, y), s, size, color)

def rgb(s):
    return tuple(int(s.strip("#")[i:i+2], 16) for i in (0, 2, 4))

def blended(a, b, fraction):
    aa, bb = rgb(a), rgb(b)
    return tuple(int(aa[i] * (1-fraction) + bb[i] * fraction) for i in range(3))

def round_box(d, box, color, outline, radius=12, width=2):
    d.rounded_rectangle(box, radius=radius, fill=color, outline=outline, width=width)

def icon(d, x, y, kind, color):
    """Símbolos sencillos dibujados en PIL; nada de fuentes de emojis no disponibles."""
    if kind == "RAYO":
        d.polygon([(x-7,y+8),(x+1,y-10),(x+11,y-10),(x+4,y),
                   (x+10,y),(x-3,y+15),(x,y+4)],fill=color,outline="#382d3b")
    elif kind == "ATAQUE RÁPIDO":
        d.polygon([(x-10,y-8),(x-2,y),(x-10,y+8),(x-5,y+8),
                   (x+5,y),(x-5,y-8)],fill=color)
        d.polygon([(x+1,y-8),(x+11,y),(x+1,y+8),(x+6,y)],fill=color)
    elif kind == "COLA FÉRREA":
        d.polygon([(x-10,y+10),(x+4,y-11),(x+11,y-8),(x-2,y+13)],
                  fill=color,outline="#425064")
        d.line((x-5,y+6,x+8,y-7),fill="#fcffff",width=2)
    elif kind in ("HUESO PALO","HUESOMERANG"):
        d.line((x-10,y+8,x+9,y-10),fill="#66505a",width=8)
        d.line((x-10,y+8,x+9,y-10),fill="#fff1d8",width=6)
        for xx,yy in ((x-10,y+8),(x+9,y-10)):
            d.ellipse((xx-5,yy-5,xx+5,yy+5),fill="#fff1d8",outline="#715664",width=1)
    elif kind == "CABEZAZO":
        d.ellipse((x-10,y-9,x+10,y+9),fill=color,outline="#5b5260",width=2)
        d.line((x-1,y-6,x+8,y+1),fill="#fef7ea",width=3)
    elif kind == "EXCAVAR":
        d.polygon([(x-11,y-8),(x+11,y-8),(x,y+12)],fill=color,outline="#615060")
        d.polygon([(x-5,y-3),(x+5,y-3),(x,y+5)],fill="#81634f")
    else:
        d.line((x-10,y,x+10,y),fill=color,width=5)
        d.line((x,y-10,x,y+10),fill=color,width=5)

def current_phase(seconds):
    for i, (a, b, mon, attack) in enumerate(TIMELINE):
        if a <= seconds < b:
            return i, mon, attack
    return len(TIMELINE)-1, "PIKACHU", None

def button_rect(k):
    return (16 if k%2==0 else 274, 83 if k<2 else 150,
            266 if k%2==0 else 524, 144 if k<2 else 211)

def render_panel(mon, selected, intro=False, victory=False):
    """Panel completo transparente superpuesto sólo en los últimos 231 píxeles."""
    C = THEMES[mon]
    p = Image.new("RGBA",(W,HEIGHT),(0,0,0,0))
    d = ImageDraw.Draw(p)

    # Sombra desplazada y borde biselado del mismo estilo arcade de la ilustración.
    d.rounded_rectangle((1,13,539,232),radius=21,fill=(10,12,31,200))
    d.polygon([(0,25),(23,1),(101,1),(116,14),(424,14),
               (440,1),(519,1),(539,23),(539,230),(0,230)],
              fill=C["edge"])
    d.polygon([(4,28),(27,6),(99,6),(114,20),(425,20),
               (441,6),(514,6),(535,28),(535,226),(4,226)],
              fill=C["outer"])
    d.polygon([(9,30),(30,11),(96,11),(109,24),(430,24),
               (444,11),(510,11),(530,30),(530,219),(9,219)],
              fill=C["inside"])
    d.line([(15,36),(525,36)],fill=blended(C["inside"],C["outer"],.38),width=2)
    d.line([(17,218),(524,218)],fill=blended(C["inside"],C["outer"],.65),width=3)

    # Visera superior con nombre del Pokémon atacante; sin interacción del usuario.
    d.polygon([(143,16),(154,7),(386,7),(397,16),
               (386,50),(153,50)],fill=C["bar"])
    d.line([(147,16),(156,11),(385,11),(393,16)],fill=C["outer"],width=3)
    if victory:
        head="¡VICTORIA DE PIKACHU!"
    elif intro:
        head="¡PREPARADOS PARA COMBATIR!"
    else:
        head="ATACA  ·  "+mon
    centered(d,270,18,head,19 if len(head)<24 else 16,C["title"])

    # Badges de tipo en ambas esquinas y pequeñas luces del HUD.
    d.rounded_rectangle((21,56,185,80),radius=7,fill=C["bar"],outline=C["edge"],width=2)
    txt(d,(31,60),C["subtitle"],11,C["badge"])
    for j in range(4):
        x=454+j*18
        d.ellipse((x,61,x+10,71),fill=C["badge"] if j<2 else "#6b6684",
                  outline=C["outer"],width=1)

    # Botones en 2 columnas, con esmalte sombreado y contorno luminoso.
    for k,(name,kind,pp,color,symbol) in enumerate(POWERS[mon]):
        x1,y1,x2,y2=button_rect(k)
        chosen = (name==selected and not victory and not intro)
        outer = C["highlight"] if chosen else "#9f95aa"
        d.rounded_rectangle((x1+2,y1+5,x2+2,y2+5),radius=11,fill="#14192f")
        d.rounded_rectangle((x1,y1,x2,y2),radius=12,fill=outer,
                            outline="#fff5e6" if chosen else "#b3abc5",width=2)
        d.rounded_rectangle((x1+5,y1+5,x2-5,y2-5),radius=9,
                            fill=blended(color,"#fff9eb",.1 if chosen else .30))
        d.line([(x1+11,y1+7),(x2-13,y1+7)],fill="#fffaf0",width=2)
        d.line([(x1+10,y2-8),(x2-10,y2-8)],fill="#987885",width=2)
        # Tipo+nombre en español; no se agregan ataques nuevos a la narración.
        icon(d,x1+28,y1+28,name,"#5d5163" if not chosen else "#433448")
        size=17 if len(name)<13 else 14
        txt(d,(x1+51,y1+10),name,size,"#211e2d")
        txt(d,(x1+53,y1+37),pp,12,"#524453")
        if chosen:
            # Selección de ataque como videojuego: 4 esquinas brillantes rojas.
            corner="#ff574e" if mon=="PIKACHU" else "#f3aa5e"
            for x,sg in ((x1+6,1),(x2-6,-1)):
                for y,yg in ((y1+6,1),(y2-6,-1)):
                    d.line([(x,y+11*yg),(x,y),(x+11*sg,y)],fill=corner,width=4)
                    d.line([(x+1,y+8*yg),(x+1,y+1),(x+8*sg,y+1)],fill="#fff4d8",width=1)
    # Etiqueta de progreso del sistema: no es un menú clicable.
    return p

def pulse(panel, seconds, mon, selected):
    if not selected:
        return panel
    k=next((i for i,z in enumerate(POWERS[mon]) if z[0]==selected),None)
    if k is None:
        raise ValueError(f"Ataque no existe para {mon}: {selected}")
    p=panel.copy()
    d=ImageDraw.Draw(p)
    x1,y1,x2,y2=button_rect(k)
    wave=(1+math.sin(seconds*8.2))/2
    gl=THEMES[mon]["highlight"]
    # Dos contornos que laten: no cambian las elecciones ni los ataques.
    width=2+round(wave*3)
    d.rounded_rectangle((x1-2,y1-2,x2+2,y2+2),radius=13,
                        outline=gl,width=width)
    spark_x=x1+14+int((x2-x1-28)*((seconds*.5)%1))
    d.ellipse((spark_x-3,y1-3,spark_x+3,y1+3),fill="#fffbe2")
    return p

def paste_frame(base, t, cache):
    idx,mon,attack=current_phase(t)
    if idx not in cache:
        cache[idx]=render_panel(mon,attack,intro=(idx==0),victory=(idx==len(TIMELINE)-1))
    overlay=pulse(cache[idx],t,mon,attack)
    # All pixels above Y_PANEL come directly from the original film, unchanged.
    base.paste(overlay,(0,Y_PANEL),overlay)
    return base

def meta(path):
    proc=subprocess.run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(path)],
                        check=True,capture_output=True,text=True)
    return json.loads(proc.stdout)

def preview(src,dest):
    cache={}
    samples=[2,11,19,25,30,36,42,50,58]
    dest.mkdir(parents=True,exist_ok=True)
    for t in samples:
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-ss",str(t),"-i",str(src),
             "-frames:v","1","-f","image2pipe","-vcodec","png","pipe:1"]
        r=subprocess.run(cmd,check=True,capture_output=True)
        import io
        im=Image.open(io.BytesIO(r.stdout)).convert("RGB")
        paste_frame(im,t,cache).save(dest/f"revision-{t:02d}.jpg",quality=85,optimize=True)
    print(f"PREVIEW: {len(samples)} frames",flush=True)

def render(src,dest):
    info=meta(src)
    video=next((s for s in info["streams"] if s.get("codec_type")=="video"),None)
    assert video and video["width"]==W and video["height"]==H, "Video base inesperado"
    assert 60<=float(info["format"]["duration"])<=62, "Duración base inesperada"
    assert any(s.get("codec_type")=="audio" for s in info["streams"]), "Falta narración original"
    tmp=dest.with_suffix(".sin-audio.mp4")
    n=int(math.ceil(float(info["format"]["duration"])*FPS))
    decoder=subprocess.Popen(["ffmpeg","-nostdin","-loglevel","error","-i",str(src),
                             "-f","rawvideo","-pix_fmt","rgb24","-vsync","0","pipe:1"],
                            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    encoder=subprocess.Popen(["ffmpeg","-nostdin","-y","-loglevel","error",
                             "-f","rawvideo","-pix_fmt","rgb24","-video_size",f"{W}x{H}",
                             "-framerate",str(FPS),"-i","pipe:0","-c:v","libx264",
                             "-preset","veryfast","-crf","23","-pix_fmt","yuv420p",
                             "-movflags","+faststart",str(tmp)],
                            stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    cache={}
    pixels=W*H*3
    i=0
    try:
        while True:
            frame=decoder.stdout.read(pixels)
            if not frame:
                break
            while len(frame)<pixels:
                more=decoder.stdout.read(pixels-len(frame))
                if not more:raise RuntimeError("Fotograma incompleto")
                frame+=more
            image=Image.frombytes("RGB",(W,H),frame)
            paste_frame(image,i/FPS,cache)
            encoder.stdin.write(image.tobytes())
            i+=1
            if i%240==0:print(f"VIDEO: {i} cuadros",flush=True)
        encoder.stdin.close()
        if decoder.wait()!=0 or encoder.wait()!=0:
            raise RuntimeError("Error decodificando o codificando el video")
        if not (n-2<=i<=n+2):raise RuntimeError(f"Duración inesperada {i} vs {n}")
    finally:
        if encoder.poll() is None:encoder.kill()
        if decoder.poll() is None:decoder.kill()
    # Copiamos sin tocar la voz, la música ni efectos del MP4 anterior.
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-i",str(tmp),
                    "-i",str(src),"-map","0:v:0","-map","1:a:0","-c:v","copy",
                    "-c:a","copy","-movflags","+faststart",str(dest)],check=True)
    print(f"MP4 FINAL: {dest} ({dest.stat().st_size} bytes)",flush=True)
    if tmp.exists():tmp.unlink()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=DEFAULT_SOURCE)
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--preview",action="store_true")
    parser.add_argument("--preview-dir",type=Path,default=HERE/"revision")
    args=parser.parse_args()
    if not args.input.exists():raise FileNotFoundError(f"Falta video base: {args.input}")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    if args.preview:preview(args.input,args.preview_dir)
    else:render(args.input,args.output)

if __name__=="__main__":main()
