import json

from constantes.const import FILE_NAME


def guardar_datos(datos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
