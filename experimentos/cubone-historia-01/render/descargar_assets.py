#!/usr/bin/env python3
"""Descarga SOLO los seis recursos visuales revisados para la historia original de Cubone.

No descarga fan art ajeno. Los personajes son propiedad de sus titulares.
Los paisajes están publicados con licencia CC0 en OpenGameArt.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets"
URLS = {
    "cubone.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/104.png",
    "marowak.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/105.png",
    "eevee.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
    "bosque-01.png": "https://opengameart.org/sites/default/files/fundo_arvore01.png",
    "bosque-02.png": "https://opengameart.org/sites/default/files/fundo_arvore02.png",
    "atardecer.png": "https://opengameart.org/sites/default/files/sunset_0.png",
}

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, url in URLS.items():
        dst = DEST / name
        if dst.exists() and dst.stat().st_size > 500:
            data = dst.read_bytes()
        else:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 cubone-video/1.0"})
            with urlopen(req, timeout=45) as resp:
                data = resp.read(10_000_001)
            if len(data) > 10_000_000:
                raise ValueError(f"Archivo demasiado grande: {name}")
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"No es PNG: {name}")
            dst.write_bytes(data)
        manifest[name] = {"url": url, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        print(f"Asset {name}: {len(data)} bytes", flush=True)
    (DEST / "fuentes.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+"\n", encoding="utf8")

if __name__ == "__main__":
    main()
