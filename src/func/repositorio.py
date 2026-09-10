import json
from pathlib import Path

file_path = Path("data/asistencia.json")


def iniciar():
    if file_path.exists():
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = {"data": []}

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def cargar():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"data": []}
    except json.decoder.JSONDecodeError as e:
        raise ({f"JSON inválido en {file_path}"}) from e


def guardar(datos):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except OSError as e:
        raise RuntimeError(f"No se pudo guardar {file_path}") from e
    except TypeError as e:
        raise ValueError("Los datos contienen un objeto no serializable") from e
