from gradio_client import Client,handle_file
from pathlib import Path
ROOT=Path.cwd()
SRC=ROOT/"experimentos/voltito-hunyuan-4v-20261118/voltito-frente.png"
ALT=ROOT/"experimentos/voltito-hunyuan-4v-20261118/voltito-espalda.png"
c=Client("trellis-community/TRELLIS",verbose=False)
F=lambda p:handle_file(str(p))
tests=[
("gallery_tuples",[(F(SRC),None),(F(ALT),None)]),
("gallery_objects",[{"image":F(SRC),"caption":None},{"image":F(ALT),"caption":None}]),
("gallery_files",[F(SRC),F(ALT)]),
("gallery_lists",[[F(SRC),None],[F(ALT),None]]),
("gallery_objects_blank",[{"image":F(SRC)},{"image":F(ALT)}]),
]
for name,images in tests:
    try:
        print("PROBANDO",name,flush=True)
        r=c.predict(images=images,api_name="/preprocess_images")
        print("ACEPTADO",name,type(r).__name__,str(r)[:600],flush=True)
    except Exception as e:
        print("FALLA",name,type(e).__name__,str(e)[:320],flush=True)
print("FIN",flush=True)
