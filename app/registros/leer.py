import time

from json_utils.cargar_json import cargar_datos
from utils.pantalla import limpiar_pantalla


def leer_registros():
    datos = cargar_datos()
    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5)  # Aplico un Temporizador.
        limpiar_pantalla()
        return
    for r in datos:
        print(
            f"ID: {r['id']} | Empleado: {r['empleado']} | Fecha: {r['fecha']} | Entrada: {r['entrada']} | Salida: {r['salida']} | Horas: {r['horas_trabajadas']}")