import re
from datetime import datetime
from utils.messages import msg


def horas():
    while True:
        try:
            entrada = datetime.strptime(
                input(msg("hora_de_entrada")),
                "%H:%M"
            ).time()
            break
        except ValueError:
            print(msg("hora_invalida"))

    while True:
        try:
            salida = input(msg("hora_de_salida"))
            if salida == "":
                break
            salida = datetime.strptime(salida, "%H:%M").time()

            if salida <= entrada:
                print(msg("hora_salida_posterior_hora_entrada"))
                continue
            break
        except ValueError:
            print(msg("hora_invalida"))

    return entrada , salida

def validar_id_empleado(emp_id):
    patron = r"[A-Z]{3}\d{3}"
    return bool(re.fullmatch(patron, emp_id))
