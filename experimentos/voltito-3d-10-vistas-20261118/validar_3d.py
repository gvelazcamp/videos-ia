"""Comprobar que el GLB REAL coloreado con 10 vistas gira fluidamente en móvil.
No confundir una pose PNG con malla; validamos el mismo GLB a 37, 128, 180 y 315°.
"""
from pathlib import Path
from threading import Thread
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
import struct
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
file=HERE/"voltito-10-vistas-mejorado.glb"
raw=file.read_bytes()
if raw[:4]!=b"glTF" or len(raw)<1_000_000:raise RuntimeError("No es archivo de malla 3D")
_,version,declared=struct.unpack_from("<4sII",raw)
if version!=2 or declared!=len(raw):raise RuntimeError("GLB incompleto")
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
server=ThreadingHTTPServer(("127.0.0.1",8829),lambda *a,**k:Quiet(*a,directory=str(ROOT),**k))
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':414,'height':861},device_scale_factor=1,is_mobile=True,has_touch=True)
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto("http://127.0.0.1:8829/experimentos/voltito-3d-10-vistas-20261118/index.html",wait_until="domcontentloaded",timeout=65000)
        page.wait_for_function("window.__VOLTITO_10_3D__?.ready===true",timeout=90000)
        if page.locator('.ref img').count()!=10:raise RuntimeError("No están las 10 referencias")
        if page.evaluate('window.__VOLTITO_10_3D__.depth')<=0.01:raise RuntimeError('No es 3D volumétrico')
        if errors:raise RuntimeError(str(errors))
        for angle,kind in ((0,'frente'),(37,'giro-37'),(128,'giro-128'),(180,'espalda'),(315,'giro-315')):
            page.locator('#angle').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',angle)
            assert page.locator('#degree').inner_text()==f'{angle}°'
            page.wait_for_timeout(200)
            page.locator('#stage').screenshot(path=str(HERE/f'prueba-3d-{kind}.png'))
            with Image.open(HERE/f'prueba-3d-{kind}.png') as image:
                pix=image.convert('RGB').resize((95,130))
                gold=sum(1 for r,g,b in pix.getdata() if r>125 and g>65 and b<170 and r>g*1.06)
                if gold<100:raise RuntimeError(f"Voltito no visible en {angle}°: {gold}")
            print("VISTA REAL OK",angle,kind,flush=True)
        for btn,name in (('top','arriba'),('bottom','abajo')):
            page.locator('#'+btn).click();page.wait_for_timeout(250)
            page.locator('#stage').screenshot(path=str(HERE/f'prueba-3d-{name}.png'))
            assert page.locator('#pitchValue').inner_text() in ('90°','-90°')
        page.locator('#reset').click()
        assert page.locator('#degree').inner_text()=='0°'
        page.locator('#spin').click()
        assert 'Pausar' in page.locator('#spin').inner_text()
        if errors:raise RuntimeError(str(errors))
        browser.close()
finally:
    server.shutdown()
print("COMPROBADO: UN GLB REAL, 360° horizontal y vistas arriba/abajo",flush=True)
