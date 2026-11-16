# Buzón de imágenes por texto (para ChatGPT u otras IA que no pueden subir archivos)

1. Convertí la imagen a JPG o PNG (mejor JPG de menos de 500 KB).
2. Pasala a base64. Por ejemplo, en Python: `base64.b64encode(open("foto.jpg","rb").read()).decode()`.
3. Creá en esta carpeta un archivo de texto `nombre.b64.txt` con el texto base64. También vale con el prefijo `data:image/jpeg;base64,`.
4. Al guardarlo, una automatización lo convierte en `referencias/recibidas/nombre.jpg` y borra el `.txt`. Nunca sobrescribe una imagen que ya existe.

## Si la conexión no deja pasar el texto entero: en partes
- Partí el base64 en trozos de hasta 4.000 caracteres: `nombre.parte01.b64.txt`, `nombre.parte02.b64.txt`, …
- Agregá `nombre.sha256.txt` con el SHA-256 de la imagen final (`hashlib.sha256(bytes_de_la_imagen).hexdigest()`).
- La imagen solo se arma si el hash coincide. Si falta o se copió mal alguna parte, no se arma nada y se ve el aviso en la ejecución.
