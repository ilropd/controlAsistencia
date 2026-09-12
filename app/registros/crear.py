from datetime import datetime

from app.cargar_json import cargar_datos
from app.guardar_json import guardar_datos
from utils.horas import calcular_tiempo_trabajado
from utils.mensajes import msg
from utils.pantalla import limpiar_pantalla
from utils.validators import validar_id_empleado


def crear_registro():
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print("Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).")
        input("Pressione enter para continuar...")
        limpiar_pantalla()
        return

    fecha = datetime.now().strftime("%d/%m/%Y")
    while True:
        try:
            entrada = input(f'{msg("hora_de_entrada")}')

            entrada = datetime.strptime(entrada, "%H:%M").time()
            break

        except ValueError:
            print(msg("hora_invalida"))

    while True:
        try:
            salida = input(f'{msg("hora_de_salida")}')

            if salida.lower() == "pendiente":
                salida = "Pendiente"
                break

            salida = datetime.strptime(salida, "%H:%M").time()

            if salida <= entrada:
                print(msg("hora_salida_posterior_hora_entrada"))
                continue
            break
        except ValueError:
            print(msg("hora_invalida"))
    if salida:
        horas_trabajadas = calcular_tiempo_trabajado(entrada.strftime("%H:%M"), salida.strftime("%H:%M"))
    else:
        horas_trabajadas = "Pendiente"

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada.strftime("%H:%M"),
        "salida": salida.strftime("%H:%M") if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas
    }

    # Alta de registros en el archivo.
    datos.append(registro)
    guardar_datos(datos)
    print("Registro guardado exitosamente.")



