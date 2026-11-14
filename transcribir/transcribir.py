"""Transcribe videos públicos pedidos en transcribir/pedidos/<nombre>.txt (una URL por archivo).

Gratis: yt-dlp baja solo el audio y faster-whisper (modelo "small", CPU) lo transcribe.
Resultado: transcribir/resultados/<nombre>.md. No ejecuta nada del pedido salvo bajar la URL.
"""
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
import re, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
PEDIDOS, RESULTADOS = ROOT / "pedidos", ROOT / "resultados"
NOMBRE = re.compile(r"[a-z0-9][a-z0-9-]{0,80}\.txt\Z")
HOSTS = ("tiktok.com", "instagram.com", "youtube.com", "youtu.be")


def url_valida(texto):
    url = texto.strip().split()[0] if texto.strip() else ""
    p = urlparse(url)
    if p.scheme != "https" or not any(p.hostname == h or (p.hostname or "").endswith("." + h) for h in HOSTS):
        raise ValueError("URL no permitida (solo https de TikTok, Instagram o YouTube)")
    return url


def mmss(s):
    return f"{int(s // 60):02d}:{int(s % 60):02d}"


def main():
    from faster_whisper import WhisperModel
    RESULTADOS.mkdir(exist_ok=True)
    pendientes = [p for p in sorted(PEDIDOS.glob("*.txt")) if NOMBRE.fullmatch(p.name) and not (RESULTADOS / (p.stem + ".md")).exists()]
    if not pendientes:
        print("No hay pedidos nuevos."); return 0
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    fallas = 0
    for pedido in pendientes[:3]:
        destino = RESULTADOS / (pedido.stem + ".md")
        try:
            url = url_valida(pedido.read_text(encoding="utf-8"))
            with tempfile.TemporaryDirectory() as tmp:
                salida = Path(tmp) / "audio.%(ext)s"
                subprocess.run(["yt-dlp", "--no-playlist", "-x", "--audio-format", "mp3", "-o", str(salida), url],
                               check=True, timeout=600, stdin=subprocess.DEVNULL)
                audio = next(Path(tmp).glob("audio.*"))
                segs, info = modelo.transcribe(str(audio), language="es", vad_filter=True)
                lineas = [f"[{mmss(s.start)}] {s.text.strip()}" for s in segs]
            cuando = datetime.now(ZoneInfo("America/Montevideo")).isoformat(timespec="seconds")
            destino.write_text(
                f"# Transcripción automática — {pedido.stem}\n\nVideo: {url}\n\nFecha Montevideo: {cuando}\n\n"
                f"Herramienta: yt-dlp + faster-whisper (modelo small, español). Duración: {info.duration:.0f} s.\n"
                "Es una transcripción automática: puede tener errores en nombres o palabras poco claras.\n\n"
                + "\n".join(lineas) + "\n", encoding="utf-8")
            print(f"Transcripto: {pedido.name}")
        except Exception as exc:  # se registra el error sin datos sensibles
            fallas += 1
            destino.write_text(f"# Transcripción — {pedido.stem}\n\nERROR: no se pudo transcribir ({type(exc).__name__}: {str(exc)[:300]}).\n", encoding="utf-8")
            print(f"Falló {pedido.name}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
