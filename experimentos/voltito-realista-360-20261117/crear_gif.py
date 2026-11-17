"""Vista previa animada para el visor táctil de Voltito; no modifica las fuentes."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

DIR=Path(__file__).resolve().parent
names=["frente","izquierda","espalda","derecha"]
sprites=[Image.open(DIR/f"voltito-{n}.png").convert("RGBA") for n in names]
W,H=520,560
frames=[]
for i in range(48):
    a=i/48*4
    first=int(a)%4
    t=a-math.floor(a)
    next_one=(first+1)%4
    # Prepara un lienzo con luz central tenue, sin recortar las orejas o la cola.
    bg=Image.new("RGBA",(W,H),(11,42,51,255))
    d=ImageDraw.Draw(bg)
    for r in range(230,50,-2):
        color=(19,69+int((230-r)*.14),80+int((230-r)*.16),9)
        d.ellipse((W/2-r,H*.48-r,W/2+r,H*.48+r),fill=color)
    d.ellipse((108,487,412,512),fill=(3,19,27,130))
    def draw_sprite(index,opacity):
        if opacity<=0:return
        source=sprites[index]
        scale=.88*(1-.10*math.sin(math.pi*t))
        xlen=int(source.width*scale)
        ylen=int(source.height*.88)
        im=source.resize((xlen,ylen),Image.Resampling.LANCZOS)
        if opacity<1:
            im.putalpha(im.getchannel("A").point(lambda x:round(x*opacity)))
        bg.alpha_composite(im,((W-xlen)//2, H-ylen-28))
    blend=max(0.,min(1.,(t-.38)/.24))
    blend=blend*blend*(3-2*blend)
    draw_sprite(first,1-blend)
    draw_sprite(next_one,blend)
    d=ImageDraw.Draw(bg)
    d.rounded_rectangle((W//2-51,515,W//2+51,542),radius=13,fill=(8,25,34,210),outline=(125,218,203,120),width=1)
    label=f"{round(i*360/48):03}°"
    d.text((W//2-17,520),label,fill=(244,239,183),stroke_width=0)
    frames.append(bg.convert("RGB").quantize(colors=128,method=Image.Quantize.FASTOCTREE))
target=DIR/"voltito-giro-360.gif"
frames[0].save(target,save_all=True,append_images=frames[1:],duration=83,loop=0,disposal=2,optimize=True)
with Image.open(target) as test:
    assert test.n_frames>=40 and test.size==(W,H)
print(f"GIF 360 verificado: {test.n_frames} cuadros -> {target}")
