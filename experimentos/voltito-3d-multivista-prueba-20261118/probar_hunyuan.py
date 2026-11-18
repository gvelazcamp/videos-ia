"""Comprobar servicio público gratuito para generar malla 3D de Voltito.
No intenta reproducir las imágenes con planos ni genera geometría manual.
"""
from gradio_client import Client
import json
print("Conectando servicio publico multivista Hunyuan3D...",flush=True)
client=Client("tencent/Hunyuan3D-2mv",verbose=False)
data=client.view_api(return_format="dict",print_info=False)
print("FUNCIONES_GRADIO", json.dumps(data,ensure_ascii=False,default=str)[:16000],flush=True)
