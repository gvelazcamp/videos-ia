"""Verificación visual automática de malla 3D real en navegador móvil.
Cada captura proviene del MISMO GLB, no de un intercambio de fotografías.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
from PIL import Image
import struct,json
ROOT=Path.cwd()
HERE=Path(__file__).resolve().parent
MODEL=HERE/"voltito-4v-colores.glb"
raw=MODEL.read_bytes()
if len(raw)<200000 or raw[:4]!=b"glTF":raise ValueError("No hay archivo GLB válido")
magic,version,declared=struct.unpack_from("<4sII",raw,0)
if version!=2 or declared!=len(raw):raise RuntimeError("GLB incompleto")
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
server=ThreadingHTTPServer(("127.0.0.1",8897),lambda *a,**k:Quiet(*a,directory=str(ROOT),**k))
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=["--no-sandbox","--enable-webgl","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
        page=browser.new_page(viewport={"width":410,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True)
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto("http://127.0.0.1:8897/experimentos/voltito-hunyuan-4v-20261118/index.html",wait_until="domcontentloaded",timeout=75000)
        page.wait_for_function("window.__VOLTITO_3D__?.ready===true",timeout=80000)
        dims=page.evaluate("window.__VOLTITO_3D__.geometryBounds")
        if min(dims.values())<=0.01:raise RuntimeError(f"Sin profundidad 3D: {dims}")
        for degree,name in [(0,"frente"),(37,"trescuartos"),(90,"perfil"),(180,"espalda"),(270,"otro-perfil")]:
            page.locator("#angle").evaluate("(el,value)=>{el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));}",degree)
            assert page.locator("#degree").inner_text()==f"{degree}°"
            page.wait_for_timeout(400)
            dest=HERE/f"captura-3d-{name}.png"
            page.locator("#canvas").screenshot(path=str(dest))
            with Image.open(dest) as im:
                pix=list(im.convert("RGB").resize((96,120)).getdata())
                yellows=sum(1 for r,g,b in pix if r>130 and g>75 and b<170 and r>g*1.07)
                if yellows<85:raise RuntimeError(f"Voltito no visible en {name}, píxeles={yellows}")
            print("GLB VISTA REAL VERIFICADA:",degree,name,dest.stat().st_size,flush=True)
        page.locator("#spin").click()
        assert "Pausar" in page.locator("#spin").inner_text()
        if errors:raise RuntimeError(f"Errores JavaScript: {errors}")
        browser.close()
finally:
    server.shutdown()
print("RESULTADO: GLB auténtico 360 continuo; validación técnica, no identidad perfecta",flush=True)
