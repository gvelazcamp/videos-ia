"""Diagnóstico público de TRELLIS.2 ANTES de generar (no gasta GPU).
Las imágenes de Voltito permanecen en el repositorio ya existente.
"""
import json
from urllib.request import Request,urlopen
from pathlib import Path

SPACES=["microsoft/TRELLIS.2","henrybit/TRELLIS-2-4B-Demo","opsiclear-admin/Trellis.2.multiview"]
report={}
for space in SPACES:
    item={"space":space}
    print("EXPLORANDO:",space,flush=True)
    try:
        req=Request("https://huggingface.co/api/spaces/"+space,headers={"User-Agent":"Mozilla/5.0"})
        with urlopen(req,timeout=32) as response: data=json.loads(response.read(2500000))
        runtime=data.get("runtime") or {}
        item["status"]=runtime.get("stage")
        item["hardware"]=runtime.get("hardware")
        item["sdk"]=data.get("sdk")
        item["host"]=data.get("host")
        print("ESTADO",item["status"],"GPU",item["hardware"],flush=True)
        candidates=[]
        if item["host"]:
            h=item["host"]
            if not h.startswith("https://"):h="https://"+h
            candidates.extend([h+"/gradio_api/info",h+"/info"])
        slug=space.lower().replace("/","-").replace(".","-")
        candidates+=["https://"+slug+".hf.space/gradio_api/info","https://"+slug+".hf.space/info"]
        for endpoint in dict.fromkeys(candidates):
            try:
                with urlopen(Request(endpoint,headers={"User-Agent":"Mozilla/5.0"}),timeout=28) as response:
                    info=json.loads(response.read(8_000_000))
                named=info.get("named_endpoints") or {}
                item["api_endpoint"]=endpoint
                item["api"]={}
                for name,spec in named.items():
                    item["api"][name]={
                        "parameters":[{"name":p.get("parameter_name"),"type":p.get("type"),"example":str(p.get("example"))[:140]} for p in spec.get("parameters",[])],
                        "returns":[{"type":r.get("type"),"label":r.get("label")} for r in spec.get("returns",[])],
                    }
                print("API_OK",endpoint,list(named),flush=True)
                break
            except Exception as e:
                item.setdefault("api_errors",[]).append(str(e)[:170])
    except Exception as e:
        item["error"]=f"{type(e).__name__}: {e}"
        print("NO_DISPONIBLE",item["error"][:350],flush=True)
    report[space]=item
dest=Path(__file__).with_name("disponibilidad.json")
dest.write_text(json.dumps(report,indent=2,ensure_ascii=False))
print("GUARDADO",dest,flush=True)
