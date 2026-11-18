"""Exporta la geometría volumétrica de Voltito a glTF binario (GLB).
Usa sólo Three.js local y su exportador oficial, sin pagar APIs.
"""
from pathlib import Path
from threading import Thread
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
import struct,json
ROOT=Path(__file__).resolve().parents[2]
DIR=Path(__file__).resolve().parent
class Silent(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    server=ThreadingHTTPServer(("127.0.0.1",8842),lambda *a,**kw:Silent(*a,directory=str(ROOT),**kw))
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,args=["--no-sandbox","--enable-webgl","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
            page=browser.new_page(viewport={"width":420,"height":840},accept_downloads=True)
            problems=[]
            page.on("pageerror",lambda e:problems.append(str(e)))
            page.goto("http://127.0.0.1:8842/experimentos/voltito-reconstruido-20261117/index.html",wait_until="domcontentloaded",timeout=65000)
            page.wait_for_function("window.__VOLTITO_RECONSTRUCCION__ !== undefined",timeout=60000)
            page.wait_for_function("window.__VOLTITO_RECONSTRUCCION__.model.getObjectByName('cabeza principal').material.map?.image?.complete===true",timeout=30000)
            with page.expect_download(timeout=120000) as download_info:
                page.evaluate("""async () => {
                    const { GLTFExporter } = await import('./GLTFExporter.js');
                    const exporter = new GLTFExporter();
                    const group = window.__VOLTITO_RECONSTRUCCION__.model;
                    const buffer = await exporter.parseAsync(group,{binary:true,onlyVisible:true,maxTextureSize:2048});
                    const anchor = document.createElement('a');
                    anchor.href = URL.createObjectURL(new Blob([buffer],{type:'model/gltf-binary'}));
                    anchor.download = 'voltito-reconstruido.glb';
                    anchor.click();
                }""")
            download_info.value.save_as(DIR/"voltito-reconstruido.glb")
            if problems:raise ValueError("Errores JS: "+str(problems))
            browser.close()
        file=DIR/"voltito-reconstruido.glb"
        raw=file.read_bytes()
        magic,version,total=struct.unpack_from("<4sII",raw,0)
        if magic!=b"glTF" or version!=2 or total!=len(raw) or len(raw)<40000:
            raise ValueError("El GLB está incompleto")
        chunk_len,chunk_type=struct.unpack_from("<II",raw,12)
        if chunk_type!=0x4e4f534a:raise ValueError("No tiene cabecera JSON glTF")
        obj=json.loads(raw[20:20+chunk_len].rstrip(b' \x00'))
        if len(obj.get("meshes",[]))<25:raise ValueError("La malla 3D está incompleta")
        print("GLB OK:",file.name, len(raw),"bytes",len(obj["meshes"]),"mallas")
    finally:
        server.shutdown()
if __name__=="__main__":main()
