from gradio_client import Client,handle_file
from pathlib import Path
import traceback
ROOT=Path.cwd()
SRC=ROOT/"experimentos/voltito-hunyuan-4v-20261118/voltito-frente.png"
ALT=ROOT/"experimentos/voltito-hunyuan-4v-20261118/voltito-espalda.png"
print("CLIENT",flush=True)
c=Client("trellis-community/TRELLIS",verbose=False)
checks=[
    ("/preprocess_image",lambda:c.predict(image=handle_file(str(SRC)),api_name="/preprocess_image")),
    ("/preprocess_images",lambda:c.predict(images=[(handle_file(str(SRC)),None),(handle_file(str(ALT)),None)],api_name="/preprocess_images")),
]
for name,run in checks:
    try:
        print("PROBANDO",name,flush=True)
        r=run()
        print("ACEPTADO",name,type(r).__name__,str(r)[:800],flush=True)
    except Exception as e:
        print("FALLA",name,type(e).__name__,str(e)[:800],flush=True)
print("PRUEBA_FINALIZADA",flush=True)
