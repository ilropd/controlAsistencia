from datetime import datetime

from json_utils.cargar_json import cargar_datos
from json_utils.guardar_json import guardar_datos
from utils.horas import calcular_tiempo_trabajado

from utils.mensajes import msg
from utils.pantalla import limpiar_pantalla
from utils.validators import validar_id_empleado


def crear_registro():
    # Carga los registros existentes para poder añadir el nuevo registro
    # sin sobrescribir la información almacenada previamente.
    datos = cargar_datos()

    emp_id = input("ID del empleado (ej. EMP001): ").upper()

    # Valida que el identificador del empleado cumpla el formato establecido
    # antes de continuar con la creación del registro.
    if not validar_id_empleado(emp_id):
        print(
            "Formato de ID inválido. Debe ser 3 letras y 3 números "
            "(ej. EMP001)."
        )
        input("Presione Enter para continuar...")
        limpiar_pantalla()
        return

    # Obtiene la fecha actual y la almacena con el formato utilizado
    # por el resto de la aplicación.
    fecha = datetime.now().strftime("%d/%m/%Y")

    # Comprueba si el empleado ya tiene un registro asociado a la fecha actual.
    # any() devuelve True cuando encuentra al menos un registro que coincide
    # con ambos criterios, evitando así la creación de registros duplicados.
    if any(
            data.get("empleado") == emp_id
            and data.get("fecha") == fecha
            for data in datos
    ):
        print(msg("registro_ya_existente"))
        input("Presione Enter para continuar...")
        limpiar_pantalla()
        return

    # Solicita la hora de entrada hasta que el usuario introduzca
    # un valor válido con el formato HH:MM.
    while True:
        try:
            entrada = input(f'{msg("hora_de_entrada")}')
            entrada = datetime.strptime(entrada, "%H:%M").time()
            break

        except ValueError:
            print(msg("hora_invalida"))

    # La hora de salida es opcional, ya que un registro puede permanecer
    # abierto mientras el empleado todavía se encuentra trabajando.
    while True:
        try:
            salida = input(f'{msg("hora_de_salida")}')

            if not salida:
                break

            salida = datetime.strptime(salida, "%H:%M").time()

            # Impide registrar una hora de salida anterior o igual
            # a la hora de entrada.
            if salida <= entrada:
                print(msg("hora_salida_posterior_hora_entrada"))
                continue

            break

        except ValueError:
            print(msg("hora_invalida"))

    # Calcula el tiempo trabajado cuando existe una hora de salida.
    # Si el registro continúa abierto, se indica que el cálculo está pendiente.
    if salida:
        horas_trabajadas = calcular_tiempo_trabajado(
            entrada.strftime("%H:%M"),
            salida.strftime("%H:%M")
        )
    else:
        horas_trabajadas = "Pendiente"

    # Genera el identificador del nuevo registro tomando como referencia
    # el último identificador almacenado. Si no existen registros,
    # comienza la numeración en 1.
    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada.strftime("%H:%M"),
        "salida": salida.strftime("%H:%M") if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas
    }

    # Añade el nuevo registro a la colección existente y persiste
    # los cambios en el archivo de almacenamiento.
    datos.append(registro)
    guardar_datos(datos)

    print("Registro guardado exitosamente.")
