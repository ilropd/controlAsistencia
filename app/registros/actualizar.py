from datetime import datetime

from app.cargar_json import cargar_datos
from app.guardar_json import guardar_datos
from utils.horas import calcular_tiempo_trabajado
from utils.mensajes import msg
from utils.pantalla import limpiar_pantalla
from utils.validators import validar_id_empleado


def actualizar_registro():
    datos = cargar_datos()
    while True:
        try:
            empleado_id = input(msg("id_del_empleado")).upper()
            if not validar_id_empleado(empleado_id):
                raise ValueError

            coincidencias = [data for data in datos if data.get("empleado") == empleado_id]

            if not coincidencias:
                print(msg("registro_no_encontrado"))
                input(msg("press_enter"))
                limpiar_pantalla()
                continue

            if len(coincidencias) == 1:
                print(msg("registro_encontrado"))
                print(coincidencias[0])
                break

            print(msg("registros_encontrados"))
            for coincidencia in coincidencias:
                print(coincidencia)
                print("-" * (len(coincidencia)))
            break

        except ValueError:
            print(msg("formato_de_id_invalido"))
            input(msg("press_enter"))
            limpiar_pantalla()
            continue

    while True:
        try:
            fecha = datetime.strptime(input(msg("introduzca_fecha_para_cambios.")), "%d/%m/%Y").date()

            data_encontrada = next(
                (data for data in coincidencias if data.get("fecha") == fecha.strftime("%d/%m/%Y")),
                None)

            if data_encontrada is None:
                print(msg("no_hay_registros_para_id_fecha_seleccionada."))
                print(msg("seleccione_otra_fecha."))
                input(msg("press_enter"))
                limpiar_pantalla()
                continue

            break

        except ValueError:
            print(msg("fecha_invalida"))
            input(msg("press_enter"))
            limpiar_pantalla()
            continue

    while True:
        try:
            entrada = input(f'{msg("hora_de_entrada")}\n{msg("presione_enter_mantener_valor_actual")}')
            if entrada == "":
                entrada = None
                break

            entrada = datetime.strptime(entrada, "%H:%M").time()
            break

        except ValueError:
            print(msg("hora_invalida"))

    while True:
        try:
            salida = input(f'{msg("hora_de_salida")}\n{msg("presione_enter_mantener_valor_actual")}')
            if salida == "":
                salida = None
                break
            if salida.lower() == "pendiente":
                salida = "Pendiente"
                break

            salida = datetime.strptime(salida, "%H:%M").time()

            if entrada is not None and salida <= entrada:
                print(msg("hora_salida_posterior_hora_entrada"))
                continue
            break
        except ValueError:
            print(msg("hora_invalida"))

    if entrada is not None:
        data_encontrada["entrada"] = entrada.strftime("%H:%M")

    if salida is not None:
        if salida == "Pendiente":
            data_encontrada["salida"] = "Pendiente"
            data_encontrada["horas_trabajadas"] = "Pendiente"
        else:
            data_encontrada["salida"] = salida.strftime("%H:%M")

        if (
                data_encontrada.get("entrada")
                and data_encontrada.get("salida")
                and data_encontrada["salida"] != "Pendiente"
        ):
            data_encontrada["horas_trabajadas"] = calcular_tiempo_trabajado(
                data_encontrada["entrada"],
                data_encontrada["salida"]
            )


    guardar_datos(datos)

    print(msg("registro_actualizado"))
    input(msg("press_enter"))
    limpiar_pantalla()
