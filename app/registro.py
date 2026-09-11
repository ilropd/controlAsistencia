import time
from datetime import datetime

from app.cargar_json import cargar_datos
from app.guardar_json import guardar_datos
from utils.pantalla import limpiar_pantalla
from utils.horas import calcular_tiempo_trabajado
from utils.messages import msg
from utils.validators import horas, validar_id_empleado


def crear_registro():
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print("Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).")
        input("Pressione enter para continuar...")
        limpiar_pantalla()
        return

    fecha = datetime.now().strftime("%d/%m/%Y")
    entrada, salida = horas()
    horas_trabajadas = calcular_tiempo_trabajado(entrada, salida)

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


# 7. Función
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


# 9. Función
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


def actualizar_registro():
    datos = cargar_datos()

    empleado_id = input(msg("id_del_empleado")).upper()
    if not validar_id_empleado(empleado_id):
        print(msg("formato_de_id_invalido"))
        input(msg("press_enter"))
        limpiar_pantalla()
        return None

    for data in datos:
        if data["empleado"] == empleado_id:
            print(f"{msg("registro_encontrado")} {data}")

            '''
            nueva_entrada = input(f"{"nueva_entrada"} [{data['entrada']}]: ") or data['entrada']
            if not validar_formato_hora(nueva_entrada):
                print("Hora de entrada inválida.")
                return

            nueva_salida = input(f"Nueva salida [{data['salida']}]: ") or data['salida']
            if nueva_salida != "Pendiente" and not validar_formato_hora(nueva_salida):
                print("Hora de salida inválida.")
                return
            '''
            nueva_entrada, nueva_salida = horas()

            data['entrada'] = nueva_entrada.strftime("%H:%M")
            data['salida'] = nueva_salida.strftime("%H:%M")
            if nueva_salida != "Pendiente":
                data['horas_trabajadas'] = (
                    calcular_tiempo_trabajado(nueva_entrada, nueva_salida)
                )
            else:
                data['horas_trabajadas'] = "Pendiente"

            guardar_datos(datos)
            print(msg("registro_actualizado"))
            return None
    print(msg("registro_no_encontrado"))
    return None
