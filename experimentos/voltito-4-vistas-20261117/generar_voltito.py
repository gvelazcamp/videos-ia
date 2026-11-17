"""Voltito: personaje eléctrico ORIGINAL, cuatro vistas.
Genera cuatro sprites transparentes y una lámina de referencia.
No toca ningún archivo fuera de su carpeta.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT = Path(__file__).resolve().parent
ROOT.mkdir(parents=True, exist_ok=True)
VISTAS = ["frente", "izquierda", "derecha", "espalda"]

DEFS = """
<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFE887"/>
    <stop offset=".50" stop-color="#FFC64D"/>
    <stop offset="1" stop-color="#F29A3A"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFF3B7"/>
    <stop offset=".75" stop-color="#FFDB71"/>
    <stop offset="1" stop-color="#F2AE4A"/>
  </linearGradient>
  <linearGradient id="teal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#B4FFF0"/>
    <stop offset=".58" stop-color="#35D9C4"/>
    <stop offset="1" stop-color="#1A8D9F"/>
  </linearGradient>
  <linearGradient id="belly" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFF4CE"/>
    <stop offset="1" stop-color="#E4FFDD"/>
  </linearGradient>
  <radialGradient id="glow">
    <stop offset="0" stop-color="#FFFFFA"/>
    <stop offset=".25" stop-color="#DFFFFB"/>
    <stop offset="1" stop-color="#28DECB"/>
  </radialGradient>
</defs>
"""

# Cuerpo compacto y patas distintas a Pikachu; orejas como hojas, mejillas de rayos
# turquesas, copete azul y cola en zigzag con punta bifurcada.
FRONT = """
<!-- Cola eléctrica detrás del cuerpo -->
<path d="M343 381 L389 326 L367 294 L458 225 L426 312 L467 343 L399 430 L360 452 Z"
  fill="url(#teal)" stroke="#214C59" stroke-width="10" stroke-linejoin="round"/>
<path d="M388 341 L414 306 L404 326 L435 337 L398 391" fill="none"
  stroke="#EFFFF8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<!-- Orejas asimétricas de hoja -->
<path d="M179 217 Q126 163 113 73 Q169 91 219 182 L229 239 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M113 73 Q144 92 160 121 L142 144 Q126 118 113 73 Z"
  fill="url(#teal)" stroke="#394650" stroke-width="6"/>
<path d="M282 218 Q326 96 397 61 Q403 163 327 236 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M397 61 Q386 108 361 135 L341 124 Q370 82 397 61 Z"
  fill="url(#teal)" stroke="#394650" stroke-width="6"/>
<path d="M178 196 Q167 145 161 132 M335 186 Q355 144 370 118"
  fill="none" stroke="#FFF4B1" stroke-width="8" stroke-linecap="round" opacity=".8"/>
<!-- Patitas -->
<path d="M178 514 Q135 531 135 564 Q144 595 198 585 L234 554 L237 507 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M300 514 Q353 519 363 557 Q359 591 312 590 L274 554 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M159 578 L169 568 M184 587 L194 576 M323 583 L313 570 M345 574 L333 566"
  stroke="#8E6D45" stroke-width="5" stroke-linecap="round"/>
<!-- Brazos detrás -->
<path d="M163 388 Q120 385 115 427 Q109 454 141 464 L189 437 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M341 386 Q382 385 391 427 Q390 460 361 468 L324 440 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M119 445 Q135 439 147 447 M374 447 Q359 437 346 443"
  stroke="#EFFFF8" stroke-width="8" stroke-linecap="round"/>
<!-- Cuerpo -->
<path d="M168 363 Q145 409 162 492 Q178 553 249 557 Q325 563 347 497 Q359 440 339 360 Z"
  fill="url(#gold)" stroke="#394650" stroke-width="11"/>
<path d="M208 412 Q188 478 222 519 Q251 545 291 515 Q318 472 296 409 Z"
  fill="url(#belly)" opacity=".97"/>
<path d="M252 420 L273 452 L256 453 L268 478 L229 442 L250 441 Z"
  fill="#39CFC0" stroke="#189898" stroke-width="2" stroke-linejoin="round"/>
<!-- Cabeza ancha, ojos azul marino -->
<path d="M144 255 Q153 188 220 174 Q271 155 328 192 Q364 218 366 286 Q368 351 302 388 Q248 412 191 386 Q128 357 140 289 Z"
  fill="url(#sun)" stroke="#394650" stroke-width="11" stroke-linejoin="round"/>
<path d="M176 230 Q199 194 245 193" stroke="#FFFFDD" stroke-width="13"
  stroke-linecap="round" fill="none" opacity=".66"/>
<!-- Copete único -->
<path d="M224 174 L214 140 L242 156 L256 115 L272 158 L299 145 L283 182 Z"
  fill="url(#teal)" stroke="#394650" stroke-width="8" stroke-linejoin="round"/>
<!-- Ojos -->
<ellipse cx="203" cy="278" rx="23" ry="29" fill="#263B55"/>
<ellipse cx="299" cy="278" rx="23" ry="29" fill="#263B55"/>
<ellipse cx="196" cy="268" rx="8" ry="10" fill="white"/>
<ellipse cx="292" cy="268" rx="8" ry="10" fill="white"/>
<circle cx="213" cy="291" r="4" fill="#73FFF1"/>
<circle cx="309" cy="291" r="4" fill="#73FFF1"/>
<path d="M176 249 Q194 235 212 244 M292 244 Q311 236 324 249"
  stroke="#845C3C" stroke-width="6" stroke-linecap="round" fill="none"/>
<!-- Rayos de mejillas turquesa -->
<path d="M156 304 L171 313 L164 330 L188 328 L177 353 L178 335 L153 337 Z"
  fill="url(#teal)" stroke="#168E99" stroke-width="3" stroke-linejoin="round"/>
<path d="M345 303 L330 313 L337 330 L313 328 L324 352 L323 335 L348 336 Z"
  fill="url(#teal)" stroke="#168E99" stroke-width="3" stroke-linejoin="round"/>
<path d="M246 304 Q252 300 258 304 L251 316 Z" fill="#714A46"/>
<path d="M232 329 Q250 351 272 329" fill="none" stroke="#794B43" stroke-width="6" stroke-linecap="round"/>
<circle cx="180" cy="357" r="5" fill="#FFF9CF"/>
<circle cx="321" cy="355" r="5" fill="#FFF9CF"/>
"""

SIDE_LEFT = """
<!-- Vista hacia la izquierda: punta del hocico a la izquierda, cola atrás -->
<path d="M330 374 L383 342 L367 300 L452 240 L426 309 L468 344 L401 424 L347 441 Z"
  fill="url(#teal)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M379 357 L416 331 L407 352 L434 353" fill="none"
 stroke="#EFFFFB" stroke-width="7" stroke-linecap="round"/>
<!-- Oreja posterior -->
<path d="M276 224 Q323 110 380 76 Q390 150 315 244 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M380 76 Q367 112 351 128 L336 119 Q361 90 380 76 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="5"/>
<!-- Patas con perspectiva -->
<path d="M230 510 Q198 525 196 558 Q196 588 247 591 L286 560 L285 513 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M306 510 Q356 520 365 555 Q369 583 331 590 L292 562 Z"
 fill="#EFA744" stroke="#394650" stroke-width="10"/>
<!-- Cuerpo profile -->
<path d="M203 374 Q175 412 190 485 Q206 550 284 553 Q348 546 358 485 Q358 420 331 366 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="11"/>
<path d="M203 406 Q186 463 219 508 Q238 527 258 527 Q233 461 261 401 Z"
 fill="url(#belly)"/>
<!-- Brazo que alcanza al frente -->
<path d="M204 408 Q157 415 148 456 Q154 476 182 468 L237 432 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M160 453 L183 451" stroke="#EFFFF3" stroke-width="7" stroke-linecap="round"/>
<!-- Cara lateral con hocico anguloso -->
<path d="M309 202 Q262 181 212 205 Q162 221 154 263 L99 295 Q91 315 113 333 Q120 378 181 388 Q261 410 318 365 Q356 333 352 277 Q350 228 309 202 Z"
 fill="url(#sun)" stroke="#394650" stroke-width="11" stroke-linejoin="round"/>
<path d="M147 277 Q157 233 200 223" fill="none" stroke="#FFFFD7" stroke-width="10"
 stroke-linecap="round" opacity=".65"/>
<!-- Oreja delantera visible -->
<path d="M211 217 Q163 128 145 59 Q224 87 257 194 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M145 59 Q174 83 188 117 L165 134 Q152 94 145 59 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="5"/>
<path d="M206 195 L194 159 L221 171 L243 132 L251 183 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="8" stroke-linejoin="round"/>
<!-- Un ojo grande de perfil -->
<ellipse cx="184" cy="277" rx="22" ry="29" fill="#263B55"/>
<ellipse cx="179" cy="269" rx="8" ry="10" fill="white"/>
<circle cx="195" cy="294" r="4" fill="#73FFF1"/>
<!-- Hocico y sonrisa -->
<path d="M101 300 L121 294 L121 310 Z" fill="#704A46"/>
<path d="M122 334 Q145 352 173 332" fill="none"
 stroke="#794B43" stroke-width="6" stroke-linecap="round"/>
<!-- Marca rayo de la mejilla -->
<path d="M222 308 L237 316 L229 332 L255 328 L238 359 L240 340 L218 342 Z"
 fill="url(#teal)" stroke="#168E99" stroke-width="4" stroke-linejoin="round"/>
<!-- Aleta dorsal turquesa -->
<path d="M332 378 L351 397 L339 421" fill="none" stroke="#D78B33" stroke-width="9" stroke-linecap="round"/>
"""

BACK = """
<!-- Cola saliendo del costado derecho -->
<path d="M339 385 L391 337 L366 301 L460 233 L427 315 L463 350 L399 430 L359 448 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M399 359 L423 328 L412 357" fill="none" stroke="#E5FFF2" stroke-width="7"/>
<!-- Orejas vista posterior -->
<path d="M177 216 Q122 158 115 71 Q179 92 227 195 Z"
 fill="#E4A447" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M115 71 Q137 88 154 117 L141 134 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="5"/>
<path d="M279 199 Q325 92 395 58 Q399 153 327 230 Z"
 fill="#E7A648" stroke="#394650" stroke-width="10" stroke-linejoin="round"/>
<path d="M395 58 Q369 88 352 119 L373 131 Z"
 fill="url(#teal)" stroke="#394650" stroke-width="5"/>
<!-- Patas -->
<path d="M181 510 Q143 529 141 567 Q149 591 202 583 L229 544 Z"
 fill="#EBA04A" stroke="#394650" stroke-width="10"/>
<path d="M307 510 Q355 528 361 560 Q357 590 309 586 L271 549 Z"
 fill="#EBA04A" stroke="#394650" stroke-width="10"/>
<!-- Brazos -->
<path d="M164 381 Q112 407 118 441 Q130 466 170 450 L194 406 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<path d="M333 381 Q386 408 387 439 Q370 470 331 450 L307 409 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="10"/>
<!-- Cuerpo visto de atrás -->
<path d="M163 353 Q142 402 164 486 Q190 551 247 559 Q318 567 345 491 Q358 414 335 355 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="11"/>
<!-- Tres rayas dorsales asimétricas -->
<path d="M187 396 L233 414 L210 439 L169 420 Z"
 fill="#CF8443" opacity=".90" />
<path d="M315 397 L273 414 L297 441 L342 420 Z"
 fill="#CF8443" opacity=".90" />
<path d="M226 460 L253 472 L237 495 L207 482 Z"
 fill="#CF8443" opacity=".75"/>
<path d="M286 461 L260 473 L274 497 L302 484 Z"
 fill="#CF8443" opacity=".75"/>
<!-- Cabeza por detrás -->
<path d="M142 254 Q152 187 222 175 Q271 157 330 196 Q362 222 362 289 Q359 360 298 386 Q242 402 185 379 Q132 353 142 254 Z"
 fill="url(#gold)" stroke="#394650" stroke-width="11" stroke-linejoin="round"/>
<!-- Copete azul trasero -->
<path d="M216 177 L213 147 L240 159 L254 121 L272 159 L302 145 L286 184 Z"
 fill="#269D9D" stroke="#394650" stroke-width="8" stroke-linejoin="round"/>
<!-- Espiral de energía dorsal (no coincide con marca frontal) -->
<path d="M230 295 Q252 270 276 298 Q280 315 260 319 Q246 319 246 309 Q248 304 256 304"
 fill="none" stroke="#FFF3B5" stroke-width="12" stroke-linecap="round"/>
<path d="M211 349 Q254 357 302 343" fill="none" stroke="#EDB263" stroke-width="8" stroke-linecap="round"/>
"""

def svg_for_view(view: str) -> str:
    if view == "frente":
        artwork = FRONT
    elif view == "izquierda":
        artwork = SIDE_LEFT
    elif view == "derecha":
        # Un solo modelo lateral espejado: posiciones opuestas consistentes.
        artwork = '<g transform="translate(500 0) scale(-1 1)">' + SIDE_LEFT + '</g>'
    elif view == "espalda":
        artwork = BACK
    else:
        raise ValueError(view)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="700" '
        'viewBox="0 0 500 700">\n' + DEFS +
        '<g stroke-linecap="round" stroke-linejoin="round">\n' + artwork +
        '</g>\n</svg>\n'
    )

def getfont(size: int, bold: bool = False):
    options = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    )
    for p in options:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def make_sheet():
    width, height = 2200, 1010
    sheet = Image.new("RGB", (width, height), "#F4F8F8")
    draw = ImageDraw.Draw(sheet)
    # Cabecera editorial
    draw.rounded_rectangle((44, 26, 2156, 158), radius=34, fill="#17394A")
    draw.text((84, 53), "VOLTITO", font=getfont(67, True), fill="#FFF4BC")
    draw.text((472, 79), "Personaje eléctrico original  •  Hoja de cuatro vistas",
              font=getfont(27), fill="#C6EFEB")
    titles = ["FRENTE", "COSTADO IZQUIERDO", "COSTADO DERECHO", "ESPALDA"]
    colors = ["#E8F8F3", "#FFF8E8", "#E8F6FB", "#FFF2E6"]
    for i, view in enumerate(VISTAS):
        left = 35 + i * 545
        right = left + 520
        draw.rounded_rectangle((left, 188, right, 956), radius=28, fill="#FFFFFF", outline="#DCE8E7", width=3)
        draw.rounded_rectangle((left+18, 208, right-18, 839), radius=22, fill=colors[i])
        # sombra de suelo debajo de cada personaje, fuera del PNG individual
        draw.ellipse((left+118, 744, left+410, 782), fill="#D7E5E0")
        png = ROOT / f"voltito-{view}.png"
        with Image.open(png) as img:
            sprite = img.convert("RGBA")
            sprite.thumbnail((485, 620), Image.Resampling.LANCZOS)
            px = left + (520 - sprite.width) // 2
            py = 204 + (630 - sprite.height) // 2
            sheet.paste(sprite, (px, py), sprite)
        bb = draw.textbbox((0,0), titles[i], font=getfont(27, True))
        tw = bb[2]-bb[0]
        draw.text((left+260-tw/2, 871), titles[i], font=getfont(27, True), fill="#193A49")
        draw.text((left+35, 914), f"Vista {i+1} / 4", font=getfont(19), fill="#6D8490")
    sheet.save(ROOT/"voltito-cuatro-vistas.png", "PNG", optimize=True)
    with Image.open(ROOT/"voltito-cuatro-vistas.png") as im:
        im.load()
        assert im.size == (width, height) and im.format == "PNG"
    print("Lámina completa de cuatro vistas lista", width, height)

def main():
    for view in VISTAS:
        svg = svg_for_view(view)
        svg_path = ROOT / f"voltito-{view}.svg"
        png_path = ROOT / f"voltito-{view}.png"
        svg_path.write_text(svg, encoding="utf-8")
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png_path),
                         output_width=1000, output_height=1400)
        with Image.open(png_path) as im:
            im.load()
            assert im.format == "PNG" and im.mode == "RGBA"
            low, hi = im.getchannel("A").getextrema()
            assert low == 0 and hi == 255
            print(view, im.size, "RGBA transparente verificado", low, hi)
    make_sheet()

if __name__ == "__main__":
    main()
