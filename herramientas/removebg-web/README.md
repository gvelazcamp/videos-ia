# remove.bg (sitio web) integrado a GitHub, sin API

Esta carpeta permite que **GitHub Actions abra la página oficial remove.bg con Chromium**, suba una imagen del repositorio y descargue un **PNG transparente** usando la opción **Preview / Free**.

- Sin API, sin claves y sin instalación en la computadora del usuario.
- **No necesita una cuenta para recortes gratuitos de baja resolución.** Esto **no significa que una sesión personal ya esté conectada**.
- No activa pagos, no selecciona HD ni compra créditos.
- Los resultados se guardan en GitHub en una ruta explícita; no se reemplazan ni se modifican los otros robots o páginas.
- Se usan selectores normales de la interfaz. Si el servicio pide CAPTCHA, login, pago o cambia su web, el flujo falla y explica el paso; **no evade barreras**.
- Para gestionar una cuenta personal mediante sesión web persistente haría falta iniciar sesión de forma segura en un navegador remoto y almacenar el estado cifrado, siempre fuera del repositorio. No pedir contraseña en comentarios o archivos.

## Uso

1. Abrí [Actions](https://github.com/gvelazcamp/videos-ia/actions/workflows/removebg-web-sin-api.yml).
2. «Run workflow» → «Run workflow». Por defecto toma `experimentos/pikachu-surf-3ia/referencia-original.png` y escribe `experimentos/pikachu-castillo-terror/personaje-removebg-web.png`.
3. Para otra imagen ya existente en GitHub, cambiá las rutas de entrada y salida al ejecutar manualmente.
4. Si falla, mirá el registro de la ejecución en Actions. No cambies el HTML original hasta verificar el recorte.

La herramienta usa **remove.bg oficial**, no el paquete Python `rembg`.

**Importante:** remove.bg anunció el fin de su web independiente para el **1 de diciembre de 2026 a las 9:00 CET**, al migrar su servicio a Canva. Este flujo es una prueba de integración, no una solución garantizada a largo plazo. Una alternativa ejecutable en GitHub sin API sería `rembg` (proyecto distinto).

**Fuente:** https://www.remove.bg/ (aviso visible en la página).
