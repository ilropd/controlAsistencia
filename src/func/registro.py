import time
from datetime import datetime

from .func_json import cargar_datos, guardar_datos
from util.calc_horas import calcular_horas
from util.limpiar_pantalla import limpiar_pantalla
from util.validators import validar_formato_hora, validar_id_empleado


def crear_registro():
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print("❌ Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).❌")
        time.sleep(5)  # Aplico un Temporizador.
        limpiar_pantalla()
        return

    # Gestionamos formato de fechas y horas.
    fecha = datetime.now().strftime("%Y-%m-%d")
    entrada = input("Hora de entrada (HH:MM): ")
    if not validar_formato_hora(entrada):
        print("Formato de hora inválido. Use HH:MM.")
        return

    salida = input("Hora de salida (HH:MM, presione Enter si queda pendiente): ")
    horas_trabajadas = 0.0
    if salida:
        if not validar_formato_hora(salida):
            print("Formato de hora de salida inválido.")
            return
        horas_trabajadas = calcular_horas(entrada, salida)

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas
    }

    # Alta de registros en el archivo.
    datos.append(registro)
    guardar_datos(datos)
    print("Registro guardado exitosamente.")


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


def actualizar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a actualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    for r in datos:
        if r["id"] == reg_id:
            print(f"Registro encontrado: {r}")
            nueva_entrada = input(f"Nueva entrada [{r['entrada']}]: ") or r['entrada']
            if not validar_formato_hora(nueva_entrada):
                print("Hora de entrada inválida.")
                return

            nueva_salida = input(f"Nueva salida [{r['salida']}]: ") or r['salida']
            if nueva_salida != "Pendiente" and not validar_formato_hora(nueva_salida):
                print("Hora de salida inválida.")
                return

            r['entrada'] = nueva_entrada
            r['salida'] = nueva_salida
            if nueva_salida != "Pendiente":
                r['horas_trabajadas'] = calcular_horas(nueva_entrada, nueva_salida)
            else:
                r['horas_trabajadas'] = 0.0

            guardar_datos(datos)
            print("Registro actualizado correctamente.")
            return
    print("Registro no encontrado.")


def eliminar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    nuevos_datos = [r for r in datos if r["id"] != reg_id]
    if len(nuevos_datos) == len(datos):
        print("Registro no encontrado.")
    else:
        guardar_datos(nuevos_datos)
        print("Registro eliminado correctamente.")