import json, re, sys, time
from datetime import datetime
from BorroPantalla import Borro  # Desde la aplicación BorroPantalla importo la funcion.
from utils.mensajes import msg

## Mejor usar esto para asegurar que el archivo JSON siempre esta en el mismo lugar,
## en la misma carpeta del archivo principal
# from pathlib import Path
# FILE_NAME = Path(__file__).parent / "asistencia.json"

FILE_NAME = "asistencia.json"


# 1. Función
def cargar_datos() -> list | None:
    """
    Carga y valida la estructura de los datos del archivo JSON.

    Comprueba que el contenido del archivo sea una lista y, si contiene registros,
    verifica que cada registro sea un diccionario con todos los campos requeridos.

    Returns:
        list:
            Lista de registros si el archivo tiene una estructura válida.
        []:
            Si el archivo no existe o la lista de registros está vacía.
        None:
        Si el archivo contiene una estructura no válida o está dañado.
    """
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # El archivo debe contener una lista
        if not isinstance(datos, list):
            print("\n❌ La estructura del archivo JSON no es válida.")
            return None

        # Si la lista está vacía, los datos son válidos
        if not datos:
            return datos

        campos_requeridos = {
            "id",
            "empleado",
            "fecha",
            "entrada",
            "salida",
            "horas_trabajadas",
        }

        # Verificamos la estructura de cada registro
        for registro in datos:
            if not isinstance(registro, dict):
                print("\n❌ La estructura de los registros no es válida.")
                return None

            if not campos_requeridos.issubset(registro):
                print("\n❌ Un registro no contiene todos los campos requeridos.")
                return None

        return datos
    # Si no hay archivo, el sistema devuelva la lista vacía
    except FileNotFoundError:
        return []

    # Si el archivo ya existe, el sistema devuelva None para salir el programa
    # Un usuario no pueda usar el programa si el archivo json está dañado
    except json.JSONDecodeError:
        print("\n❌ El archivo JSON está dañado.")
        return None


# 2. Función
def guardar_datos(datos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# 3. Función
def validar_formato_hora(hora_str):
    """Valida formato estricto de 24 horas (HH:MM)."""
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora_str.strip()))


# 4. Función
def validar_id_empleado(emp_id):
    """Valida que el ID tenga el formato: 3 letras mayúsculas + 3 dígitos (ej. EMP001)."""
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id.strip()))


# 5. Función
def calcular_horas(entrada, salida):
    """Calcula horas trabajadas en formato decimal."""
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = (t_salida - t_entrada).total_seconds()

    # Validar coherencia temporal
    if diferencia < 0:
        return None
    # horas = diferencia.total_seconds() / 3600
    # return round(horas, 2)
    return round(diferencia / 3600, 2)


# 5. Función.
def buscar_registro_existente(registros, empleado_id, fecha):
    """Busca si el empleado ya fichó en la fecha actual."""
    for reg in registros:
        if reg.get("empleado") == empleado_id and reg.get("fecha") == fecha:
            return reg
    return None


# Funcion para mostrar registros
def mostrar_registros(registros):
    """Muestra una lista de registros de asistencia en formato tabla.
    Args: registros(list): lista de registros que se va a mostrar
    Returns: Ninguno"""
    print(
        f"{'ID':<5} | "
        f"{'Empleado':<8} | "
        f"{'Fecha':<10} | "
        f"{'Entrada':<7} | "
        f"{'Salida':<9} | "
        f"{'Horas':<6}"
    )

    print("-" * 61)

    for r in registros:
        print(
            f"{r['id']:<5} | "
            f"{r['empleado']:<8} | "
            f"{r['fecha']:<10} | "
            f"{r['entrada']:<7} | "
            f"{r['salida']:<9} | "
            f"{r['horas_trabajadas']:<6}"
        )


def buscar_registro_por_id(registros, reg_id):
    """Busca un registro concreto por su ID.
    Args: registros(list), reg_id(int): id del registro
    Returns: dict: registro encontrado, None: registro no encontrado
    """
    for registro in registros:
        if registro["id"] == reg_id:
            return registro

    return None


def buscar_registros_por_empleado(datos, emp_id):
    """Obtiene todos los registros de un empleado
    Args: datos(list), emp_id(int): Id del empleado
    Retrns: list: Regsitros del empleado"""
    return [registro for registro in datos if registro["empleado"] == emp_id]


def solicitar_id_empleado():
    """Solicita y valida el Id de un empleado
    Returns: str: Id del empleado valido"""
    while True:
        emp_id = input("Ingrese el ID del empleado: ").strip().upper()

        if validar_id_empleado(emp_id):
            return emp_id

        print("ID de empleado inválido.")


def solicitar_registro_a_eliminar(registros_empleado):
    """Solicita un Id de registro hasta encontrar uno del empleado
    Args: registros_empleados(list): registros del empleado
    Returns: dict: registros selecionado para eliminar"""
    while True:
        try:
            reg_id = int(input("Ingrese el ID del registro a eliminar: ").strip())
        except ValueError:
            print("ID inválido.")
            continue

        registro_seleccionado = buscar_registro_por_id(registros_empleado, reg_id)

        if registro_seleccionado is None:
            print("El registro indicado no pertenece a este empleado.")
            continue

        return registro_seleccionado


def solicitar_opcion_eliminacion():
    """Muestra el menú de eliminacion y solicita una opcion valida
    Returns:opcion(str): opcion selecionada por el usuario"""
    while True:
        print("\n1. Eliminar un registro")
        print("2. Eliminar todos los registros")
        print("3. Cancelar")

        while True:
            opcion = input("Seleccione una opción: ").strip()

            if opcion in ("1", "2", "3"):
                return opcion

            print("Opción inválida.")


def solicitar_confirmacion(mensaje):
    """Solicita al usuario una confirmación mediante s/n.
    Args: mensaje(str): Mensaje que se mostrará
    Returns: booleano (True confirmacion, False si cancela)"""
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print("Opción invalida. Introduzca s o n")


def eliminar_un_registro(datos, registros_empleado):
    """Eliminar un registro de un empleado despues de solicitar confirmacion
    Args: datos(list), registros_empleados(list): registros pertencientes al empleado
    Returns: Ninguno"""

    registro_seleccionado = solicitar_registro_a_eliminar(registros_empleado)

    Borro()

    mostrar_registros([registro_seleccionado])

    if solicitar_confirmacion("¿Está seguro de que desea eliminar este registro?"):
        datos.remove(registro_seleccionado)
        guardar_datos(datos)
        print("\nRegistro eliminado correctamente.")
    else:
        print("Eliminación cancelada.")

    time.sleep(1)
    Borro()


def eliminar_todos_registros(datos, emp_id):
    """Elimina todos los registros de un empleado
    Args: datos(list), emp_id(str): Id del empleado
    Returns: Ninguno"""
    if solicitar_confirmacion(
        f"¿Está seguro de que desea eliminar todos los registros de {emp_id}?"
    ):
        datos = [registro for registro in datos if registro["empleado"] != emp_id]

        guardar_datos(datos)
        print("\nTodos los registros del empleado han sido eliminados.")
    else:
        print("Eliminación cancelada.")

    time.sleep(1)

def crear_registro():
    registros = cargar_datos()
    #  Captura del ID de empleado
    while True:
        Borro()
        print(f"--- 🔑 REGISTRO DE ASISTENCIA 🔑 ---")
        emp_id = input("ID del empleado (ej. EMP001) o 'C' para cancelar: ").strip().upper()
        if emp_id == 'C':
            print("Registro cancelado.")
            time.sleep(2)
            Borro()
            return

        if validar_id_empleado(emp_id):
            break
        Borro()
        
        print("Formato de ID no válido. Introduce ID válido (ej. EMP001)")
        time.sleep(2)
        Borro()

    #  Gestiona formato de fecha actual
    fecha = datetime.now().strftime("%Y-%m-%d")

    #  Comprobación de registro existente en el día
    registro_existente = buscar_registro_existente(registros, emp_id, fecha)

    if registro_existente:
        Borro()
        print(f"--- 🔑 REGISTRO DE ASISTENCIA 🔑 ---")
        print(f"\n El empleado {emp_id} ya tiene un registro hoy ({fecha}):")
        print(f"   Entrada actual: {registro_existente['entrada']}")
        print(f"   Salida actual : {registro_existente.get('salida', 'Pendiente')}")
        print("\n  Para realizar cambios, utiliza la opción 'Actualizar' en el menú principal.")
        input("\nPresiona ENTER para volver al menú...")
        time.sleep(3)  # Pausa previa para permitir lectura
        Borro()
        return

    #  Bucle independiente para la hora de entrada
    while True:
        Borro()
        print(f"--- 🔑 REGISTRAR ASISTENCIA 🔑 ---")
        print(f"Empleado: {emp_id} | Fecha: {fecha}\n")
        #cancelacion
        entrada = input("Hora de entrada (HH:MM) o 'C' para cancelar: ").strip()
        if entrada.upper() == "C":
            print("Operación cancelada.")
            time.sleep(1.5)
            Borro()
            return
        #autocorreción de formato
        if len(entrada) == 4 and entrada[1] == ":":
            entrada = "0" + entrada
            
        if validar_formato_hora(entrada):
            break
        print("Formato de hora inválido. Use HH:MM.")
        time.sleep(2)
            
    #  Bucle independiente para hora de salida
    while True:
        Borro()
        print(f"--- 🔑 REGISTRO DE ASISTENCIA 🔑 ---")
        print(f"Empleado: {emp_id} | Fecha: {fecha}")
        print(f"Entrada: {entrada}\n")
        #cancelacion
        salida = input("Hora de salida (HH:MM) o 'C' para cancelar: ").strip()
        if salida.upper() == "C":
            print("Operación cancelada.")
            time.sleep(1.5)
            return
        #autocorreción de formato
        if len(salida) == 4 and salida[1] == ":":
            salida = "0" + salida        
        #comprobación de formato
        if not validar_formato_hora(salida):
            print("Formato incorrecto. Usa HH:MM.")

            time.sleep(2)
            continue
        #comprobación de error de salida
        if salida <= entrada:
            print(f"La hora de salida ({salida}) NO VáLIDA.")
            print("Introduce nuevamente la hora de salida.\n")
            time.sleep(3)
            continue  # Reintenta la hora de salida
        
        break  
        
    # Cálculo de horas y creación de nuevo registro
    horas_totales = calcular_horas(entrada, salida)
    Borro()
    print("=== 🔑 REGISTRO DE ASISTENCIA 🔑 ===")
    print(f" • Empleado        : {emp_id}")
    print(f" • Fecha           : {fecha}")
    print(f" • Hora Entrada    : {entrada}")
    print(f" • Hora Salida     : {salida}")
    print(f" • Horas Totales   : {horas_totales} h")
    print("====================================")
    #confirmacion antes de seguir
    confirmar = input("\n¿Guardar este registro? s/n: ").strip().lower()
    if confirmar not in ("s", "si"):
        print("\nRegistro descartado.")
        time.sleep(2)
        Borro()
        return
    # asignacion de ID y guardado.
    nuevo_id = max([r.get("id", 0) for r in registros], default=0) + 1

    nuevo_registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida,
        "horas_trabajadas": horas_totales,
    }

    registros.append(nuevo_registro)
    guardar_datos(registros) # Persistencia en JSON
    
    print(f"\n Nuevo registro #{nuevo_id} guardado correctamente.")
    time.sleep(2)
    Borro()


# 7. Función
def leer_registros():
    datos = cargar_datos()

    if datos is None:
        return

    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5)  # Aplico un Temporizador.
        Borro()
        return

    mostrar_registros(datos)


# 8. Función
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
                data for data in datos if data.get("empleado") == empleado_id
            ]

            # Si no existe ningún registro, informa al usuario y permite
            # volver a introducir el identificador.
            if not coincidencias:
                print(msg("registro_no_encontrado"))
                input(msg("press_enter"))
                Borro()
                continue

            # Si existen varios registros para el mismo empleado,
            # se muestran todos para informar al usuario.
            if len(coincidencias) == 1:
                print(msg("registro_encontrado"))
            else:
                print(msg("registros_encontrados"))
            for coincidencia in coincidencias:
                print("-------------------------")
                for key, value in coincidencia.items():
                    print("".join(f"{str(key).upper()}: {value}"))
                print("-------------------------")
            break

        except ValueError:
            # Gestiona tanto un identificador con formato incorrecto
            # como cualquier error de validación asociado al mismo.
            print(msg("formato_de_id_invalido"))
            input(msg("press_enter"))
            Borro()
            continue

    # Solicita la fecha del registro que se desea modificar.
    while True:
        try:
            fecha = datetime.strptime(
                input(msg("introduzca_fecha_para_cambios.")), "%Y-%m-%d"
            ).date()

            # Busca entre los registros del empleado aquel cuya fecha
            # coincida con la seleccionada por el usuario.
            data_encontrada = next(
                (
                    data
                    for data in coincidencias
                    if data.get("fecha") == fecha.strftime("%Y-%m-%d")
                ),
                None,
            )

            # Si no existe un registro para esa combinación de empleado
            # y fecha, se solicita al usuario que seleccione otra fecha.
            if data_encontrada is None:
                print(msg("no_hay_registros_para_id_fecha_seleccionada."))
                print(msg("seleccione_otra_fecha."))
                input(msg("press_enter"))
                Borro()
                continue

            break

        except ValueError:
            # Controla las fechas introducidas con un formato no válido.
            print(msg("fecha_invalida"))
            input(msg("press_enter"))
            Borro()
            continue

    # Solicita una nueva hora de entrada.
    # Al pulsar Enter sin introducir ningún valor, se conserva la hora actual.
    while True:
        try:
            entrada = input(
                f"{msg('hora_de_entrada')}\n"
                f"{msg('presione_enter_mantener_valor_actual')}"
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
                f"{msg('hora_de_salida')}\n"
                f"{msg('presione_enter_mantener_valor_actual')}"
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
            data_encontrada["horas_trabajadas"] = calcular_horas(
                data_encontrada["entrada"], data_encontrada["salida"]
            )

    # Persiste los cambios realizados en el almacenamiento de datos.
    guardar_datos(datos)

    # Informa al usuario de que la actualización se ha completado.
    print(msg("registro_actualizado"))
    input(msg("press_enter"))
    Borro()


# 9. Función para Eliminar Registro
def eliminar_registro():
    """Gestiona el proceso para eliminar registros de un empleado
    Returns: Ninguno"""
    
    Borro()
    
    datos = cargar_datos()

    if datos is None:
        time.sleep(1)
        Borro()
        return

    if not datos:
        print("No hay registros en el sistema")
        time.sleep(1)
        Borro()
        return

    emp_id = solicitar_id_empleado()

    registros_empleado = buscar_registros_por_empleado(datos, emp_id)

    if not registros_empleado:
        print("No hay registros para este empleado.")
        time.sleep(1)
        Borro()
        return

    Borro()
    mostrar_registros(registros_empleado)

    opcion = solicitar_opcion_eliminacion()

    if opcion == "1":
        eliminar_un_registro(datos, registros_empleado)

    elif opcion == "2":
        eliminar_todos_registros(datos, emp_id)

    elif opcion == "3":
        print("Eliminación cancelada.")
        time.sleep(1)
        Borro()


# 10. Funcion
def salir_registro() -> None:
    """
    Solicita confirmación al usuario antes de salir del programa.
    Muestra una pregunta de confirmación y permite responder con 's'/'si' para salir o 'n'/'no' para continuar en el programa.
    Si la respuesta no es válida, vuelve a solicitar la confirmación.

    Returns:
        None: Si el usuario decide continuar, vuelve al menú principal.
    """
    while True:
        salir = (
            input("\n❓ ¿Está seguro de que desea salir del programa (s/n)? ")
            .strip()
            .lower()
        )

        if salir in ("s", "si"):
            print("\n👋 ¡Hasta pronto!")
            time.sleep(2)
            Borro()
            sys.exit(0)

        elif salir in ("n", "no"):
            Borro()
            return

        else:
            print(
                "\n❌ Opción no válida. Por favor, introduce 's' para Sí o 'n' para No."
            )
            time.sleep(2)

            # "\033[4A" — subir el cursor 4 líneas
            # # "\033[J" — limpiar la pantalla desde el cursor hacia abajo
            print("\033[4A\033[J", end="")


# 11. Función_
def menu() -> None:
    Borro()
    while True:
        menu = [
            "1. Registrar Entrada/Salida (Crear)",
            "2. Ver Registros (Leer)",
            "3. Actualizar Registro",
            "4. Eliminar Registro",
            "5. Salir",
        ]
        print("\n--- 🔑 CONTROL DE ASISTENCIA 🔑 ---\n")
        print("\n".join(menu))

        opcion = input("\nSeleccione una opción: ").strip()

        match opcion:
            case "1":
                crear_registro()
            case "2":
                leer_registros()
            case "3":
                actualizar_registro()
            case "4":
                eliminar_registro()
            case "5":
                salir_registro()
            case _:
                input(
                    "\n❌ Opción inválida en el menú. Pulsa [ENTER] para volver al menú principal."
                )
                Borro()


# Comienzo del program evitando interferencias de terceros. ❓
if __name__ == "__main__":
    menu()
