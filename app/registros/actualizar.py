from datetime import datetime

from app.cargar_json import cargar_datos
from app.guardar_json import guardar_datos
from utils.horas import calcular_tiempo_trabajado
from utils.mensajes import msg
from utils.pantalla import limpiar_pantalla
from utils.validators import validar_id_empleado


def actualizar_registro():
    # Carga en memoria todos los registros almacenados para poder
    # localizar y modificar el correspondiente al empleado.
    datos = cargar_datos()

    # Solicita el identificador del empleado hasta que se introduzca
    # un valor válido y exista al menos un registro asociado.
    while True:
        try:
            empleado_id = input(msg("id_del_empleado")).upper()

            # Valida que el identificador introducido cumpla el formato
            # establecido para los empleados.
            if not validar_id_empleado(empleado_id):
                raise ValueError

            # Obtiene todos los registros asociados al empleado indicado.
            coincidencias = [
                data for data in datos
                if data.get("empleado") == empleado_id
            ]

            # Si no existe ningún registro, informa al usuario y permite
            # volver a introducir el identificador.
            if not coincidencias:
                print(msg("registro_no_encontrado"))
                input(msg("press_enter"))
                limpiar_pantalla()
                continue

            # Cuando solo existe un registro, se muestra directamente
            # y se continúa con la selección de la fecha.
            if len(coincidencias) == 1:
                print(msg("registro_encontrado"))
                print(coincidencias[0])
                break

            # Si existen varios registros para el mismo empleado,
            # se muestran todos para informar al usuario.
            print(msg("registros_encontrados"))
            for coincidencia in coincidencias:
                print(coincidencia)
                print("-" * len(coincidencia))
            break

        except ValueError:
            # Gestiona tanto un identificador con formato incorrecto
            # como cualquier error de validación asociado al mismo.
            print(msg("formato_de_id_invalido"))
            input(msg("press_enter"))
            limpiar_pantalla()
            continue

    # Solicita la fecha del registro que se desea modificar.
    while True:
        try:
            fecha = datetime.strptime(
                input(msg("introduzca_fecha_para_cambios.")),
                "%d/%m/%Y"
            ).date()

            # Busca entre los registros del empleado aquel cuya fecha
            # coincida con la seleccionada por el usuario.
            data_encontrada = next(
                (
                    data for data in coincidencias
                    if data.get("fecha") == fecha.strftime("%d/%m/%Y")
                ),
                None
            )

            # Si no existe un registro para esa combinación de empleado
            # y fecha, se solicita al usuario que seleccione otra fecha.
            if data_encontrada is None:
                print(msg("no_hay_registros_para_id_fecha_seleccionada."))
                print(msg("seleccione_otra_fecha."))
                input(msg("press_enter"))
                limpiar_pantalla()
                continue

            break

        except ValueError:
            # Controla las fechas introducidas con un formato no válido.
            print(msg("fecha_invalida"))
            input(msg("press_enter"))
            limpiar_pantalla()
            continue

    # Solicita una nueva hora de entrada.
    # Al pulsar Enter sin introducir ningún valor, se conserva la hora actual.
    while True:
        try:
            entrada = input(
                f'{msg("hora_de_entrada")}\n'
                f'{msg("presione_enter_mantener_valor_actual")}'
            )

            if entrada == "":
                entrada = None
                break

            entrada = datetime.strptime(entrada, "%H:%M").time()
            break

        except ValueError:
            # La hora debe respetar el formato de 24 horas HH:MM.
            print(msg("hora_invalida"))

    # Solicita una nueva hora de salida.
    # También permite establecer el estado "Pendiente".
    while True:
        try:
            salida = input(
                f'{msg("hora_de_salida")}\n'
                f'{msg("presione_enter_mantener_valor_actual")}'
            )

            # Un valor vacío indica que se debe conservar la hora actual.
            if salida == "":
                salida = None
                break

            # Permite indicar que la jornada todavía no ha finalizado.
            if salida.lower() == "pendiente":
                salida = "Pendiente"
                break

            salida = datetime.strptime(salida, "%H:%M").time()

            # Si se ha introducido una nueva hora de entrada, comprueba
            # que la salida sea posterior a dicha entrada.
            if entrada is not None and salida <= entrada:
                print(msg("hora_salida_posterior_hora_entrada"))
                continue

            break

        except ValueError:
            # Controla cualquier hora de salida que no cumpla el formato
            # esperado.
            print(msg("hora_invalida"))

    # Actualiza la hora de entrada únicamente si el usuario ha introducido
    # un nuevo valor. Si es None, se mantiene el valor existente.
    if entrada is not None:
        data_encontrada["entrada"] = entrada.strftime("%H:%M")

    # Actualiza la hora de salida cuando se ha proporcionado un nuevo valor.
    if salida is not None:
        if salida == "Pendiente":
            # Si la salida queda pendiente, las horas trabajadas también
            # permanecen pendientes de cálculo.
            data_encontrada["salida"] = "Pendiente"
            data_encontrada["horas_trabajadas"] = "Pendiente"

        else:
            data_encontrada["salida"] = salida.strftime("%H:%M")

        # Calcula de nuevo las horas trabajadas únicamente cuando existen
        # una entrada y una salida válidas y la salida no está pendiente.
        if (
            data_encontrada.get("entrada")
            and data_encontrada.get("salida")
            and data_encontrada["salida"] != "Pendiente"
        ):
            data_encontrada["horas_trabajadas"] = calcular_tiempo_trabajado(
                data_encontrada["entrada"],
                data_encontrada["salida"]
            )

    # Persiste los cambios realizados en el almacenamiento de datos.
    guardar_datos(datos)

    # Informa al usuario de que la actualización se ha completado.
    print(msg("registro_actualizado"))
    input(msg("press_enter"))
    limpiar_pantalla()
