import json
import time
import uuid
from datetime import datetime, date

from util.limpiar_pantalla import limpiar_pantalla
from util.validators import validar_id_empleado
from .repositorio import cargar, guardar

json_data = cargar()


def crear_registro():
    datos = json_data
    empleado_id = input(f"ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(empleado_id):
        print(f"Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).")
        time.sleep(2)
        limpiar_pantalla()
        return None
    fecha = datetime.now()
    '''
    while True:

        try:
            fecha = datetime.strptime(input(f"Fecha (DD/MM/YYYY): "), "%d/%m/%Y").date()

            if fecha > date.today():
                print("La fecha no puede ser posterior a hoy.")
                continue
            break
        except ValueError:
            print(f"Fecha inválida. Use el formato DD/MM/YYYY.")
'''
    while True:
        try:
            entrada = datetime.strptime(
                input(f"Hora de entrada (HH:MM): "),
                "%H:%M"
            ).time()
            break
        except ValueError:
            print(f"Hora inválida. Use el formato HH:MM.")
    while True:
        try:
            salida = input(f"Hora de salida (HH:MM, presione Enter si queda pendiente): ")
            if salida == "":
                break
            salida = datetime.strptime(salida, "%H:%M").time()

            if salida <= entrada:
                print("La hora de salida debe ser posterior a la hora de entrada.")
                continue
            break
        except ValueError:
            print(f"Hora inválida. Use el formato HH:MM.")

    registro = {
        "id": str(uuid.uuid4()),
        "empleado": empleado_id,
        "fecha": fecha.isoformat(),
        "entrada": entrada.isoformat(),
        "salida": salida.isoformat() if salida is not "" else None
    }

    datos["data"].append(registro)
    guardar(datos)

    print("Registro guardado exitosamente.")
    return None


def leer(empleado=None, fecha=None):
    registros = json_data["data"]
    # Filtrar por empleado
    if empleado:
        registros = [
            registro for registro in registros
            if registro.get("empleado") == empleado
        ]

    # Filtrar por fecha
    if fecha:
        registros = [
            registro for registro in registros
            if registro.get("fecha") == fecha
        ]

    if not registros:
        print("No se encontraron registros.")
        return

    for registro in registros:
        entrada = registro.get("entrada")
        salida = registro.get("salida")

        # Calcular tiempo trabajado
        if entrada and salida:
            hora_entrada = datetime.strptime(entrada, "%H:%M:%S")
            hora_salida = datetime.strptime(salida, "%H:%M:%S")

            worktime = hora_salida - hora_entrada

            # Convertir a horas/minutos
            total_seconds = int(worktime.total_seconds())
            horas, resto = divmod(total_seconds, 3600)
            minutos, segundos = divmod(resto, 60)

            worktime_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        else:
            worktime_str = "Pendiente"

        print(f"ID:        {registro.get('id')}")
        print(f"Empleado:  {registro.get('empleado')}")
        print(f"Fecha:     {datetime.fromisoformat(registro.get('fecha')).strftime("%d/%m/%Y")}")
        print(f"Entrada:   {entrada}")
        print(f"Salida:    {salida or 'Pendiente'}")
        print(f"Worktime:  {worktime_str}")
        print("-" * 40)


def eliminar_empleado():
    registros = json_data.get("data", [])
    empleado_id = input("ingrese ID de empleado: ").upper()
    if not validar_id_empleado(empleado_id):
        print(f"Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).")
        time.sleep(2)
        limpiar_pantalla()
        return None

    # Buscar registros del empleado
    registros_usuario = [
        registro for registro in registros
        if registro.get("empleado") == empleado_id
    ]

    if not registros_usuario:
        print(f"No se encontró el usuario: {empleado_id}")
        return False

    # Eliminar todos sus registros
    json_data["data"] = [
        registro for registro in registros
        if registro.get("empleado") != empleado_id
    ]

    with open("data/asistencia.json", "w", encoding="utf-8") as archivo:
        json.dump(json_data, archivo, indent=4, ensure_ascii=False)

    print(f"Usuario {empleado_id} eliminado correctamente.")
    print(f"Registros eliminados: {len(registros_usuario)}")

    return True
