import json
from pathlib import Path

MENSAJES_ARCH = Path(__file__).parent.parent / "config" / "mensajes.json"

with MENSAJES_ARCH.open(encoding="utf-8") as f:
    MENSAJES = json.load(f)


def msg(key):
    return MENSAJES[key]
