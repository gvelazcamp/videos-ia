"""Inspeccionar sin pago las APIs de TRELLIS que acepten múltiples fotos.
No generar ni tocar los GLB de Voltito durante este diagnóstico.
"""
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json,os
from pathlib import Path
SPACES=[
    "trellis-community/TRELLIS",
    "tur-learning/TRELLIS",
    "opsiclear-admin/Trellis.2.multiview",
    "microsoft/TRELLIS.2",
]
records={}
for space in SPACES:
    rec={"space":space}
    print("=== SPACE",space,"===",flush=True)
    try:
        req=Request("https://huggingface.co/api/spaces/"+space,headers={"User-Agent":"voltito-probe/1.0"})
        with urlopen(req,timeout=30) as resp:
            obj=json.loads(resp.read(4_000_000))
        rec["status"]=obj.get("runtime",{}).get("stage")
        rec["hardware"]=obj.get("runtime",{}).get("hardware",{})
        rec["sdk"]=obj.get("sdk")
        rec["private"]=obj.get("private")
        rec["host"]=obj.get("host")
        print("STATE",rec["status"],"HW",str(rec["hardware"])[:500],flush=True)
        # Check API without image upload, credits or GPU invocation.
        slug=space.lower().replace("/","-").replace(".","-")
        candidate=[
            "https://"+slug+".hf.space/gradio_api/info",
            "https://"+slug+".hf.space/info",
        ]
        for url in candidate:
            try:
                with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=35) as response:
                    info=json.loads(response.read(6_000_000))
                named=info.get("named_endpoints",{})
                rec["api_base"]=url.rsplit("/",2)[0]
                rec["endpoints"]=[{"name":k,"parameters":[{"name":p.get("parameter_name"),"type":(p.get("type") or {}).get("type"),"component":p.get("component"),"example":str(p.get("example"))[:200]} for p in v.get("parameters",[])],"returns":[t.get("type") for t in v.get("returns",[])]} for k,v in named.items()]
                print("API OK",url, "ENDPOINTS",list(named),flush=True)
                break
            except Exception as err:
                rec.setdefault("probe_errors",[]).append(type(err).__name__+": "+str(err)[:180])
    except Exception as err:
        rec["error"]=type(err).__name__+": "+str(err)[:320]
        print("SPACE ERROR",rec["error"],flush=True)
    records[space]=rec
Path(__file__).with_name("diagnostico-servicios.json").write_text(json.dumps(records,indent=2,ensure_ascii=False))
print("RESULTADO COMPLETO",json.dumps(records,ensure_ascii=False)[:20000],flush=True)
